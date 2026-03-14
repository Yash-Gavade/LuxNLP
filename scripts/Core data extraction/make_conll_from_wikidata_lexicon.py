import json
from collections import Counter
from pathlib import Path

# Input: merged Wikidata NER lexicon (PER + ORG + LOC + DATE)
WIKIDATA_JSONL = "data/cleaned/wikidata_lb_all_ner.jsonl"

# Output: CoNLL-style file
OUT_CONLL = "data/processed/wikidata_lb_ner.conll"

# Only keep these tags (skip others if present)
ALLOWED_TAGS = {"PER", "ORG", "LOC", "DATE"}


def main():
    in_path = Path(WIKIDATA_JSONL)
    out_path = Path(OUT_CONLL)

    if not in_path.exists():
        raise SystemExit(f"Input JSONL not found: {in_path}")

    sentences = 0
    tokens = 0
    tag_counts = Counter()
    ner_counts = Counter()

    print(f"Reading Wikidata lexicon from: {in_path}")

    with in_path.open("r", encoding="utf-8") as f_in, \
         out_path.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            rec = json.loads(line)
            lemma = rec.get("label_lb")  # Luxembourgish label
            ner_tag = rec.get("ner_tag")

            if not lemma or not ner_tag:
                continue

            if ner_tag not in ALLOWED_TAGS:
                # skip anything we don't care about
                continue

            tokens_in_lemma = lemma.split()
            if not tokens_in_lemma:
                continue

            label = ner_tag.upper()
            b_tag = f"B-{label}"
            i_tag = f"I-{label}"

            sentences += 1
            ner_counts[label] += 1

            for i, tok in enumerate(tokens_in_lemma):
                tag = b_tag if i == 0 else i_tag
                tokens += 1
                tag_counts[tag] += 1
                f_out.write(f"{tok} {tag}\n")

            f_out.write("\n")  # sentence boundary

    print("\n=== WIKIDATA → CoNLL STATS (raw) ===")
    print(f"Sentences (entries) : {sentences}")
    print(f"Tokens              : {tokens}")

    print("\nEntities per type:")
    for t, cnt in ner_counts.items():
        print(f"  {t:5s}: {cnt:6d}")

    print("\nBIO tag counts:")
    for tag, cnt in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {tag:10s}: {cnt:6d}")

    print(f"\nCoNLL file written to: {out_path}")


if __name__ == "__main__":
    main()
