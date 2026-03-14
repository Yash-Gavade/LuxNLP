import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from new_conll_io import read_conll


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conll", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    sents = read_conll(args.conll)

    tag_counts = Counter()
    type_counts = Counter()

    for s in sents:
        for _, tag in s:
            tag_counts[tag] += 1
            if tag != "O":
                et = tag.split("-", 1)[1]  # PER, LOC, ...
                type_counts[et] += 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Pie 1: O vs Entity
    o = tag_counts.get("O", 0)
    ent = sum(type_counts.values())

    plt.figure()
    plt.pie([o, ent], labels=["O", "Entity"], autopct="%1.1f%%")
    plt.title(f"{args.title}: O vs Entity Tokens")
    plt.tight_layout()
    p1 = out_dir / f"{args.title}_pie_O_vs_entity.png"
    plt.savefig(p1, dpi=200)
    plt.close()

    # Pie 2: Entity-type distribution (excluding O)
    labels = sorted(type_counts.keys())
    values = [type_counts[l] for l in labels]

    plt.figure()
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title(f"{args.title}: Entity Tokens by Type")
    plt.tight_layout()
    p2 = out_dir / f"{args.title}_pie_entity_types.png"
    plt.savefig(p2, dpi=200)
    plt.close()

    print("Saved:", p1)
    print("Saved:", p2)

if __name__ == "__main__":
    main()
