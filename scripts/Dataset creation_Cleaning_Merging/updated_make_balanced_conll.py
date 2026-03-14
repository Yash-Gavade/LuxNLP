# scripts/updated_make_balanced_conll.py
import argparse
import random
from collections import Counter
from pathlib import Path

DEFAULT_LABEL_MAP = {
    # merge / normalize
    "MEDICINE": "MED",
    "DRUG": "MED",
    "DISEASE": "MED",
    "PRODUCT": "MISC",
    "HLOC": "LOC",
    # you can add more here
    # "WORK_OF_ART": "MISC",
}

# If after mapping you still want to merge some into MISC:
DEFAULT_FORCE_TO_MISC = set()  # e.g., {"EVENT"} if you decide later


def read_sentences(path: Path):
    sentences = []
    cur = []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sentences.append(cur)
                    cur = []
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            token = " ".join(parts[:-1])
            tag = parts[-1]
            cur.append((token, tag))
    if cur:
        sentences.append(cur)
    return sentences


def write_sentences(sentences, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for sent in sentences:
            for tok, tag in sent:
                f.write(f"{tok} {tag}\n")
            f.write("\n")


def map_tag(tag: str, label_map: dict, force_to_misc: set):
    if tag == "O":
        return "O"
    if "-" in tag:
        pref, typ = tag.split("-", 1)
        typ2 = label_map.get(typ, typ)
        if typ2 in force_to_misc:
            typ2 = "MISC"
        return f"{pref}-{typ2}"
    return tag


def collect_entity_type_counts(sentences):
    """
    Count entities by type (not tokens). Entity begins at B-XXX
    """
    counts = Counter()
    for sent in sentences:
        for _, tag in sent:
            if tag.startswith("B-"):
                counts[tag.split("-", 1)[1]] += 1
    return counts


def has_any_entity(sent):
    return any(tag != "O" for _, tag in sent)


def count_o_tokens(sent):
    return sum(1 for _, t in sent if t == "O")


def count_entity_tokens(sent):
    return sum(1 for _, t in sent if t != "O")


def main():
    ap = argparse.ArgumentParser(
        description="Create an updated balanced CoNLL: label merge + O downsample."
    )
    ap.add_argument("--input", required=True, help="Input CoNLL file.")
    ap.add_argument("--output", required=True, help="Output CoNLL file.")
    ap.add_argument(
        "--seed", type=int, default=42, help="Random seed (default: 42)."
    )
    ap.add_argument(
        "--o_ratio",
        type=float,
        default=2.0,
        help="Keep at most O_tokens <= o_ratio * entity_tokens (default: 2.0).",
    )
    ap.add_argument(
        "--min_entities_per_type",
        type=int,
        default=0,
        help="Drop entity types with fewer than this many B-entities AFTER mapping (default: 0).",
    )
    ap.add_argument(
        "--map",
        default="",
        help='Optional extra mappings like "FOO=BAR,BAZ=MISC".',
    )
    args = ap.parse_args()

    random.seed(args.seed)

    in_path = Path(args.input)
    out_path = Path(args.output)

    label_map = dict(DEFAULT_LABEL_MAP)
    if args.map.strip():
        for pair in args.map.split(","):
            pair = pair.strip()
            if not pair:
                continue
            k, v = pair.split("=", 1)
            label_map[k.strip()] = v.strip()

    force_to_misc = set(DEFAULT_FORCE_TO_MISC)

    print(f"Reading: {in_path}")
    sents = read_sentences(in_path)
    print(f"Total sentences: {len(sents)}")

    # 1) apply mapping
    mapped = []
    for sent in sents:
        mapped.append([(tok, map_tag(tag, label_map, force_to_misc)) for tok, tag in sent])

    # 2) optionally drop rare entity types (by entity count)
    if args.min_entities_per_type > 0:
        ent_counts = collect_entity_type_counts(mapped)
        allowed = {t for t, c in ent_counts.items() if c >= args.min_entities_per_type}
        print(f"Entity types kept (>= {args.min_entities_per_type} entities): {sorted(allowed)}")

        def filter_sentence(sent):
            # convert disallowed entity tags to O
            new = []
            for tok, tag in sent:
                if tag == "O":
                    new.append((tok, tag))
                    continue
                if "-" in tag:
                    pref, typ = tag.split("-", 1)
                    if typ not in allowed:
                        new.append((tok, "O"))
                    else:
                        new.append((tok, tag))
                else:
                    new.append((tok, tag))
            return new

        mapped = [filter_sentence(s) for s in mapped]

    # split: entity sentences vs O-only
    entity_sents = [s for s in mapped if has_any_entity(s)]
    o_only_sents = [s for s in mapped if not has_any_entity(s)]

    # count tokens in entity sentences
    entity_tokens = sum(count_entity_tokens(s) for s in entity_sents)
    o_tokens_in_entity_sents = sum(count_o_tokens(s) for s in entity_sents)

    # allowed O budget: ratio * entity_tokens
    o_budget_total = int(args.o_ratio * entity_tokens)

    # we already have O tokens inside entity sentences; remaining budget for O-only sentences:
    remaining_o_budget = max(0, o_budget_total - o_tokens_in_entity_sents)

    print("\n--- After mapping ---")
    print(f"Entity sentences: {len(entity_sents)}")
    print(f"O-only sentences: {len(o_only_sents)}")
    print(f"Entity tokens:    {entity_tokens}")
    print(f"O tokens (inside entity sents): {o_tokens_in_entity_sents}")
    print(f"O budget total (o_ratio={args.o_ratio}): {o_budget_total}")
    print(f"Remaining O budget for O-only sents: {remaining_o_budget}")

    # sample O-only sentences until we hit remaining_o_budget
    random.shuffle(o_only_sents)
    selected_o_only = []
    used_o = 0
    for s in o_only_sents:
        o_cnt = count_o_tokens(s)
        if used_o + o_cnt > remaining_o_budget:
            continue
        selected_o_only.append(s)
        used_o += o_cnt

    final = entity_sents + selected_o_only
    random.shuffle(final)

    print("\n--- Final selection ---")
    print(f"Selected total sentences: {len(final)}")
    print(f"Selected O-only sentences: {len(selected_o_only)}")
    print(f"Selected O-only O tokens: {used_o}")

    # show entity counts by type
    ent_counts_final = collect_entity_type_counts(final)
    print("\nEntities by type (B- counts):")
    for t, c in ent_counts_final.most_common():
        print(f"  {t:12s} {c}")

    write_sentences(final, out_path)
    print(f"\nWrote: {out_path}")


if __name__ == "__main__":
    main()
