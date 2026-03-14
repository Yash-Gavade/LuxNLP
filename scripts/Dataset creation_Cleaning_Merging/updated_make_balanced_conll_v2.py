# scripts/updated_make_balanced_conll_v2.py
import argparse
import random
from collections import Counter, defaultdict
from pathlib import Path

DEFAULT_LABEL_MAP = {
    "MEDICINE": "MED",
    "PRODUCT": "MISC",
    "HLOC": "LOC",
}

def read_sentences(path: Path):
    sentences, cur = [], []
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

def map_tag(tag: str, label_map: dict):
    if tag == "O":
        return "O"
    if "-" in tag:
        pref, typ = tag.split("-", 1)
        typ = label_map.get(typ, typ)
        return f"{pref}-{typ}"
    return tag

def sentence_entity_types(sent):
    """Return set of entity types (by B- tags) that appear in this sentence."""
    types = set()
    for _, t in sent:
        if t.startswith("B-"):
            types.add(t.split("-", 1)[1])
    return types

def count_tokens(sent):
    o = sum(1 for _, t in sent if t == "O")
    e = len(sent) - o
    return o, e

def main():
    ap = argparse.ArgumentParser("Balance CoNLL with label merge + per-type caps + O downsample")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--seed", type=int, default=42)

    # O vs entity token ratio
    ap.add_argument("--o_ratio", type=float, default=2.0)

    # Per-type caps (entity counts = number of B- occurrences)
    ap.add_argument("--cap", default="MED=60000",
                    help='Comma list like "MED=60000,PER=25000,LOC=5000". Default MED=60000')

    # Extra label mappings
    ap.add_argument("--map", default="", help='Extra mappings like "FOO=BAR,BAZ=MISC"')

    args = ap.parse_args()
    random.seed(args.seed)

    label_map = dict(DEFAULT_LABEL_MAP)
    if args.map.strip():
        for pair in args.map.split(","):
            if not pair.strip():
                continue
            k, v = pair.split("=", 1)
            label_map[k.strip()] = v.strip()

    caps = {}
    if args.cap.strip():
        for pair in args.cap.split(","):
            if not pair.strip():
                continue
            k, v = pair.split("=", 1)
            caps[k.strip()] = int(v.strip())

    in_path = Path(args.input)
    out_path = Path(args.output)

    print("Reading:", in_path)
    sents = read_sentences(in_path)
    print("Total sentences:", len(sents))

    # Map labels
    mapped = [[(tok, map_tag(tag, label_map)) for tok, tag in sent] for sent in sents]

    # Split into (contains entity) vs O-only
    entity_sents = [s for s in mapped if any(t != "O" for _, t in s)]
    o_only_sents = [s for s in mapped if all(t == "O" for _, t in s)]

    print("Entity sentences:", len(entity_sents))
    print("O-only sentences:", len(o_only_sents))

    # We will select entity sentences while respecting caps by counting B- tags
    b_counts = Counter()
    selected_entity = []

    # Shuffle for randomness
    random.shuffle(entity_sents)

    for sent in entity_sents:
        # Count how many B- of each type appear in this sentence
        local_b = Counter()
        for _, t in sent:
            if t.startswith("B-"):
                local_b[t.split("-", 1)[1]] += 1

        # Check caps: if adding this sentence would exceed cap for any capped type, skip
        ok = True
        for typ, add_n in local_b.items():
            if typ in caps and (b_counts[typ] + add_n) > caps[typ]:
                ok = False
                break

        if ok:
            selected_entity.append(sent)
            b_counts.update(local_b)

    print("\nSelected entity sentences:", len(selected_entity))
    print("Selected entity B-counts:")
    for k, v in b_counts.most_common():
        print(f"  {k:10s} {v}")

    # Now compute token budgets for O downsampling
    entity_o_tokens = 0
    entity_e_tokens = 0
    for s in selected_entity:
        o, e = count_tokens(s)
        entity_o_tokens += o
        entity_e_tokens += e

    o_budget_total = int(args.o_ratio * entity_e_tokens)
    remaining_o_budget = max(0, o_budget_total - entity_o_tokens)

    print("\nToken budget:")
    print("  Entity tokens:", entity_e_tokens)
    print("  O tokens inside selected entity sents:", entity_o_tokens)
    print("  O budget total (o_ratio):", o_budget_total)
    print("  Remaining O budget for O-only sents:", remaining_o_budget)

    # Sample O-only sentences up to remaining budget
    random.shuffle(o_only_sents)
    selected_o_only = []
    used_o = 0
    for s in o_only_sents:
        o, _ = count_tokens(s)
        if used_o + o > remaining_o_budget:
            continue
        selected_o_only.append(s)
        used_o += o

    final = selected_entity + selected_o_only
    random.shuffle(final)

    print("\nFinal dataset:")
    print("  Total sentences:", len(final))
    print("  O-only sentences:", len(selected_o_only))
    print("  O-only O tokens:", used_o)

    write_sentences(final, out_path)
    print("\nWrote:", out_path)

if __name__ == "__main__":
    main()
