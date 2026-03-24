# scripts/new_show_conll_stats_v2.py
import re
from collections import Counter
from pathlib import Path


def read_conll(path: Path):
    sents = []
    toks, labs = [], []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if toks:
                    sents.append((toks, labs))
                    toks, labs = [], []
                continue
            parts = re.split(r"\s+", line.strip())
            if len(parts) < 2:
                continue
            toks.append(parts[0])
            labs.append(parts[-1])
    if toks:
        sents.append((toks, labs))
    return sents

def main():
    path = Path(
        "data/processed/"
        "train.conll"
    )

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    sents = read_conll(path)

    sent_count = len(sents)
    token_count = 0
    label_counts = Counter()
    span_counts = Counter()

    for toks, labs in sents:
        token_count += len(toks)
        label_counts.update(labs)

        for y in labs:
            if y.startswith("B-"):
                span_counts[y[2:]] += 1

    print("\n📊 DATASET STATISTICS")
    print("=" * 50)
    print(f"Sentences        : {sent_count}")
    print(f"Tokens           : {token_count}")
    print("-" * 50)

    print("\nToken labels:")
    for lab, c in label_counts.most_common():
        print(f"  {lab:15s} {c}")

    print("\nEntity spans (B- tags):")
    for ent, c in span_counts.most_common():
        print(f"  {ent:15s} {c}")

    print("\nSummary:")
    print(f"  O tokens        : {label_counts['O']}")
    print(f"  Entity tokens   : {token_count - label_counts['O']}")
    print(f"  Total entities  : {sum(span_counts.values())}")

if __name__ == "__main__":
    main()
