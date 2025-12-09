import csv
import json
import os

INPUT_JSONL = "data/cleaned/Lod.lu_entries_with_domains_and_translations.jsonl"
OUTPUT_JSONL = "data/cleaned/Lod.lu_en_lexicon.jsonl"
OUTPUT_CSV   = "data/cleaned/Lod.lu_en_lexicon.csv"

os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)


def main():
    total = 0
    kept = 0
    seen = set()  # for dedup: (lemma_lb_norm, meaning_en_norm)

    with open(INPUT_JSONL, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_JSONL, "w", encoding="utf-8") as f_out:

        for line in f_in:
            total += 1
            rec = json.loads(line)

            lemma = (rec.get("lemma_lb") or "").strip()
            meaning_en = (rec.get("meaning_en") or "").strip()
            pos = (rec.get("part_of_speech") or "").strip()
            categories = rec.get("categories") or []

            # Skip if no lemma or no English meaning
            if not lemma or not meaning_en:
                continue

            # normalise lemma (you can keep original in a separate field if you want)
            lemma_norm = lemma.strip()
            lemma_lower = lemma_norm.lower()

            meaning_norm = meaning_en.strip()

            key = (lemma_lower, meaning_norm)
            if key in seen:
                continue
            seen.add(key)

            new_rec = {
                "lemma_lb": lemma_norm,
                "lemma_lb_lower": lemma_lower,
                "meaning_en": meaning_norm,
                "part_of_speech": pos,
                "categories": categories,
            }

            f_out.write(json.dumps(new_rec, ensure_ascii=False) + "\n")
            kept += 1

    print(f"Total read: {total}")
    print(f"Kept after filtering: {kept}")
    print(f"JSONL written to: {OUTPUT_JSONL}")

    # Also write a CSV for easier viewing (without the lowercased field)
    with open(OUTPUT_JSONL, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f_csv:

        writer = csv.writer(f_csv)
        writer.writerow(["lemma_lb", "meaning_en", "part_of_speech", "categories"])

        for line in f_in:
            rec = json.loads(line)
            writer.writerow([
                rec["lemma_lb"],
                rec["meaning_en"],
                rec.get("part_of_speech", ""),
                ";".join(rec.get("categories", []))
            ])

    print(f"CSV written to: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
