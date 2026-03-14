from __future__ import annotations

import argparse

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


def merge_bio(tokens, labels):
    """Merge BIO tokens into entity spans."""
    spans = []
    cur_type = None
    cur_tokens = []

    def flush():
        nonlocal cur_type, cur_tokens
        if cur_type and cur_tokens:
            spans.append((cur_type, " ".join(cur_tokens)))
        cur_type, cur_tokens = None, []

    for tok, lab in zip(tokens, labels):
        if lab == "O":
            flush()
            continue
        pref, et = lab.split("-", 1)
        if pref == "B":
            flush()
            cur_type = et
            cur_tokens = [tok]
        elif pref == "I":
            if cur_type == et:
                cur_tokens.append(tok)
            else:
                # broken BIO -> start new
                flush()
                cur_type = et
                cur_tokens = [tok]
    flush()
    return spans

def predict(text: str, tokenizer, model):
    words = text.strip().split()
    if not words:
        return [], [], []

    enc = tokenizer(words, is_split_into_words=True, return_tensors="pt", truncation=True)
    word_ids = enc.word_ids(batch_index=0)

    with torch.no_grad():
        out = model(**{k:v for k,v in enc.items() if k != "token_type_ids"})
        pred_ids = out.logits.argmax(dim=-1)[0].tolist()

    # map prediction back to original words (ignore subwords)
    tokens, labels = [], []
    last = None
    for i, wid in enumerate(word_ids):
        if wid is None or wid == last:
            continue
        tokens.append(words[wid])
        lab = model.config.id2label[pred_ids[i]]
        labels.append(lab)
        last = wid

    spans = merge_bio(tokens, labels)
    return tokens, labels, spans

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True, help="e.g. models/xlmr_lux_ner_70_15_15")
    args = ap.parse_args()

    tokenizer = AutoTokenizer.from_pretrained(args.model_dir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(args.model_dir)
    model.eval()

    print("\nLuxNLP NER Demo (type 'exit' to quit)")
    print("Model:", args.model_dir)

    while True:
        text = input("\nEnter Luxembourgish text> ").strip()
        if text.lower() in {"exit", "quit"}:
            break

        tokens, labels, spans = predict(text, tokenizer, model)

        print("\nToken predictions:")
        for t, l in zip(tokens, labels):
            print(f"{t:20} {l}")

        print("\nExtracted entities:")
        if not spans:
            print("(none)")
        else:
            for et, s in spans:
                print(f"{et:8} -> {s}")

if __name__ == "__main__":
    main()
