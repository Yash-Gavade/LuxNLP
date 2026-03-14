# scripts/updated_demo_ner.py
import argparse
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True, help="Checkpoint folder or final model folder")
    ap.add_argument("--tokenizer_dir", default="", help="Optional tokenizer folder (use base model folder)")
    ap.add_argument("--text", default="", help="Input text")
    args = ap.parse_args()

    model_path = str(Path(args.model_dir).resolve())
    tok_path = str(Path(args.tokenizer_dir).resolve()) if args.tokenizer_dir else model_path

    tokenizer = AutoTokenizer.from_pretrained(tok_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)

    nlp = pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    text = args.text.strip()
    if not text:
        print("Type a sentence (empty line to quit):")
        while True:
            text = input("> ").strip()
            if not text:
                break
            out = nlp(text)
            for ent in out:
                print(f"{ent['word']:<25} {ent['entity_group']:<10} {ent['score']:.3f}")
            print("-" * 40)
    else:
        out = nlp(text)
        for ent in out:
            print(f"{ent['word']:<25} {ent['entity_group']:<10} {ent['score']:.3f}")

if __name__ == "__main__":
    main()
