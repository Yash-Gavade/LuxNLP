# scripts/new_predict_conll.py
from __future__ import annotations
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from new_conll_io import read_conll, write_conll

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--tokenizer_dir", required=True)
    ap.add_argument("--in_conll", required=True)
    ap.add_argument("--out_conll", required=True)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_dir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(args.model_dir)
    model.to(args.device)
    model.eval()

    id2label = model.config.id2label

    sentences = read_conll(args.in_conll)
    out_sents = []

    for sent in sentences:
        words = [t for t, _ in sent]

        enc = tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            truncation=True
        )

        word_ids = enc.word_ids(batch_index=0)

        enc = {k: v.to(args.device) for k, v in enc.items()}

        with torch.no_grad():
            logits = model(**enc).logits  
        pred_ids = logits.argmax(dim=-1)[0].tolist()

        out_sent = []
        last_wid = None
        for i, wid in enumerate(word_ids):
            if wid is None:
                continue
            if wid == last_wid:
                continue
            tag = id2label[pred_ids[i]]
            out_sent.append((words[wid], tag))
            last_wid = wid

        if len(out_sent) != len(words):
            fixed = []
            out_map = {i: tag for i, (_, tag) in enumerate(out_sent)}
            for i, w in enumerate(words):
                fixed.append((w, out_map.get(i, "O")))
            out_sent = fixed

        out_sents.append(out_sent)

    write_conll(out_sents, args.out_conll)
    print(f"Predictions written to: {args.out_conll}")

if __name__ == "__main__":
    main()
