import json
import os
import re
from pathlib import Path

INPUT_TXT = "data/raw/lb_bible_raw.txt"
OUTPUT_JSONL = "data/cleaned/lb_bible_vocab.jsonl"

os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)


def main():
    text = Path(INPUT_TXT).read_text(encoding="utf-8")

    # simple tokenisation: keep letters (incl. accents), digits, apostrophes, hyphens
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9'’-]+", text)

    # normalise to lowercase
    tokens = [t.lower() for t in tokens]

    # unique words
    vocab = sorted(set(tokens))

    print(f"Total tokens (with duplicates): {len(tokens)}")
    print(f"Unique words: {len(vocab)}")

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f_out:
        for idx, word in enumerate(vocab, start=1):
            record = {
                "id": f"bible_{idx:06d}",   # bible_000001, bible_000002, ...
                "label_lb": word,          # the word itself
                "description_lb": "",      # empty for now
                "class_id": "",            # unknown
                "class_label_lb": "",      # unknown
                "ner_tag": "O"             # no entity label yet
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved JSONL vocab to: {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
