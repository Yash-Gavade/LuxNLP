import argparse

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--text", required=True)
    ap.add_argument("--topk", type=int, default=3)
    args = ap.parse_args()

    tok = AutoTokenizer.from_pretrained(args.model_dir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(args.model_dir)
    model.eval()

    words = args.text.split()
    enc = tok(words, is_split_into_words=True, return_tensors="pt", truncation=True)
    word_ids = enc.word_ids(batch_index=0)

    with torch.no_grad():
        out = model(**{k:v for k,v in enc.items() if k!="token_type_ids"})
        probs = torch.softmax(out.logits, dim=-1)[0]  # [seq, labels]

    id2label = model.config.id2label
    last = None
    print("\nTEXT:", args.text)
    print("-"*60)

    for i, wid in enumerate(word_ids):
        if wid is None or wid == last:
            continue
        token = words[wid]

        p = probs[i]
        top = torch.topk(p, k=args.topk)
        preds = [(id2label[idx.item()], float(val.item())) for val, idx in zip(top.values, top.indices)]

        best_label = preds[0][0]
        best_prob  = preds[0][1]

        print(f"{token:18} {best_label:10} conf={best_prob:.3f}  top{args.topk}={preds}")
        last = wid

if __name__ == "__main__":
    main()
