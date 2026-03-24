# scripts/new_predict_text_quick.py
from __future__ import annotations
import argparse
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True, help="Path to checkpoint folder, e.g. models/xlmr_ner/checkpoint-500")
    args = ap.parse_args()

    model_dir = args.model_dir

    tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    model.eval()

    id2label = model.config.id2label
    if isinstance(id2label, dict):
        # sometimes keys can be strings
        def get_label(i: int) -> str:
            return id2label.get(i, id2label.get(str(i), "O"))
    else:
        def get_label(i: int) -> str:
            return id2label[i]

    tests = [
        "Den 12. Mee 2024 war d'Nationalfeierdag zu Lëtzebuerg .",
        "Ech schaffen bei Luxembourg Air Rescue zu Sandweiler .",
        "Zu Esch fënnt Esch Festival 2024 den 5. Oktober 2024 statt .",
        "Ech hu Paracetamol an der Apdikt kaaft .",
        "De Jean-Claude Juncker war Premierminister .",
    ]

    for text in tests:
        words = text.split()
        enc = tokenizer(words, is_split_into_words=True, return_tensors="pt", truncation=True)
        word_ids = enc.word_ids(batch_index=0)

        with torch.no_grad():
            outputs = model(**{k: v for k, v in enc.items() if k != "token_type_ids"})
            pred_ids = outputs.logits.argmax(dim=-1)[0].tolist()

        print("\nTEXT:", text)
        last = None
        for i, wid in enumerate(word_ids):
            if wid is None or wid == last:
                continue
            print(f"{words[wid]:20} {get_label(pred_ids[i])}")
            last = wid

if __name__ == "__main__":
    main()
