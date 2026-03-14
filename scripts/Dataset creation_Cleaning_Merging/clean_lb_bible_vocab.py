import json
import os

INPUT_JSONL = "data/cleaned/lb_bible_vocab.jsonl"
OUTPUT_JSONL = "data/cleaned/lb_bible_vocab_clean.jsonl"

os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)

# words of length 1 that we still want to keep (you can add more)
ALLOWED_SHORT = {"a", "i", "d", "e"}

def is_all_digits(s: str) -> bool:
    s = s.replace(".", "").replace(",", "")
    return s.isdigit()

def has_letter(s: str) -> bool:
    return any(ch.isalpha() for ch in s)

def main():
    total = 0
    kept = 0
    removed_digits = 0
    removed_too_short = 0
    removed_no_letters = 0

    out_f = open(OUTPUT_JSONL, "w", encoding="utf-8")

    with open(INPUT_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            total += 1
            rec = json.loads(line)

            word = rec["label_lb"].strip()

            # normalise apostrophes etc.
            word = word.replace("’", "'")
            rec["label_lb"] = word

            # 1) drop pure numbers (verse numbers etc.)
            if is_all_digits(word):
                removed_digits += 1
                continue

            # 2) drop tokens with no letters at all
            if not has_letter(word):
                removed_no_letters += 1
                continue

            # 3) drop super short junk (len 1) unless allowed
            if len(word) == 1 and word not in ALLOWED_SHORT:
                removed_too_short += 1
                continue

            # you could still keep description/class/ner_tag as they are
            out_f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1

    out_f.close()

    print(f"Total entries read:      {total}")
    print(f"Kept after cleaning:     {kept}")
    print(f"Removed (digits):        {removed_digits}")
    print(f"Removed (no letters):    {removed_no_letters}")
    print(f"Removed (too short):     {removed_too_short}")
    print(f"Output written to:       {OUTPUT_JSONL}")

if __name__ == "__main__":
    main()
