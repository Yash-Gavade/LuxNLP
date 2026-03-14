from __future__ import annotations

import re
from pathlib import Path

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


def read_conll(path: Path):
    sents = []
    toks, labs = [], []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if toks:
                    sents.append((toks, labs))
                    toks, labs = [], []
                continue
            p = re.split(r"\s+", line.strip())
            if len(p) >= 2:
                toks.append(p[0]); labs.append(p[-1])
    if toks:
        sents.append((toks, labs))
    return sents

def write_conll(tokens_list, pred_labels_list, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for toks, labs in zip(tokens_list, pred_labels_list):
            for t, y in zip(toks, labs):
                f.write(f"{t}\t{y}\n")
            f.write("\n")

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--in_conll", required=True)
    ap.add_argument("--out_conll", required=True)
    ap.add_argument("--max_len", type=int, default=256)
    ap.add_argument("--batch", type=int, default=16)
    args = ap.parse_args()

    model_dir = Path(args.model_dir)
    in_conll = Path(args.in_conll)
    out_conll = Path(args.out_conll)

    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    model.eval()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    id2label = model.config.id2label

    sents = read_conll(in_conll)
    tokens_list = [toks for toks, _ in sents]

    pred_labels_list = []

    # simple batching
    for i in range(0, len(tokens_list), args.batch):
        batch_tokens = tokens_list[i:i+args.batch]

        enc = tokenizer(
            batch_tokens,
            is_split_into_words=True,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=args.max_len,
        )

        enc = {k: v.to(device) for k, v in enc.items()}

        with torch.no_grad():
            logits = model(**enc).logits  # [B, T, C]
            pred_ids = logits.argmax(-1).cpu().tolist()

        # Convert to token-level BIO (align words)
        for b_idx, toks in enumerate(batch_tokens):
            word_ids = enc["input_ids"].new_tensor([0])  # placeholder
            # we need word_ids per example -> use tokenizer batch encoding API:
            # easiest: re-encode single sentence to access word_ids cleanly.
            single = tokenizer(
                toks,
                is_split_into_words=True,
                return_tensors="pt",
                padding=False,
                truncation=True,
                max_length=args.max_len,
            )
            single_ids = single["input_ids"].to(device)
            with torch.no_grad():
                single_logits = model(input_ids=single_ids, attention_mask=single["attention_mask"].to(device)).logits
            single_pred = single_logits.argmax(-1).squeeze(0).cpu().tolist()

            word_ids = single.word_ids()
            out_labs = ["O"] * len(toks)

            # take first subtoken prediction for each word
            seen_word = set()
            for pos, widx in enumerate(word_ids):
                if widx is None or widx in seen_word:
                    continue
                seen_word.add(widx)
                out_labs[widx] = id2label[single_pred[pos]]

            pred_labels_list.append(out_labs)

    write_conll(tokens_list, pred_labels_list, out_conll)
    print("✅ Wrote predictions to:", out_conll)

if __name__ == "__main__":
    main()
