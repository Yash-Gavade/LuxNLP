import json
from pathlib import Path
from collections import Counter

# Input: the cleaned LOD lexicon with ner_groups
LOD_NER_JSONL = "data/cleaned/Lod_lu_ner_categories.jsonl"

# Output: CoNLL-style file
OUT_CONLL = "data/processed/lod_lu_ner.conll"

NER_PRIORITY = ["MED", "EVENT", "PRODUCT"]


def choose_main_group(groups):
    """
    Decide which ner_group to use if there are several.
    Priority is defined in NER_PRIORITY.
    """
    if not groups:
        return None
    gset = set(groups)
    for g in NER_PRIORITY:
        if g in gset:
            return g
    return sorted(gset)[0]


def main():
    in_path = Path(LOD_NER_JSONL)
    out_path = Path(OUT_CONLL)

    if not in_path.exists():
        raise SystemExit(f"Input JSONL not found: {in_path}")

    sentences = 0
    tokens = 0
    tag_counts = Counter()
    group_counts = Counter()

    print(f"Reading LOD NER lexicon from: {in_path}")

    with in_path.open("r", encoding="utf-8") as f_in, \
         out_path.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            rec = json.loads(line)
            lemma = rec.get("lemma_lb")
            ner_groups = rec.get("ner_groups") or []

            main_group = choose_main_group(ner_groups)
            if main_group is None:
                continue

            if not lemma:
                continue

            tokens_in_lemma = lemma.split()
            label = main_group.upper()
            b_tag = f"B-{label}"
            i_tag = f"I-{label}"

            sentences += 1
            group_counts[main_group] += 1

            for i, tok in enumerate(tokens_in_lemma):
                tag = b_tag if i == 0 else i_tag
                tokens += 1
                tag_counts[tag] += 1
                f_out.write(f"{tok} {tag}\n")

            f_out.write("\n")  # sentence boundary

    print("\n=== LOD → CoNLL STATS ===")
    print(f"Sentences (entries) : {sentences}")
    print(f"Tokens              : {tokens}")

    print("\nEntities per group:")
    for g, cnt in group_counts.items():
        print(f"  {g:10s}: {cnt:6d}")

    print("\nBIO tag counts:")
    for tag, cnt in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {tag:12s}: {cnt:6d}")

    print(f"\nCoNLL file written to: {out_path}")


if __name__ == "__main__":
    main()
