import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from new_conll_io import read_conll


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conll", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out_png", required=True)
    args = ap.parse_args()

    sents = read_conll(args.conll)
    o = 0
    total = 0
    for s in sents:
        for _, tag in s:
            total += 1
            if tag == "O":
                o += 1
    ent = total - o

    plt.figure()
    plt.pie([o, ent], labels=["O", "Entity"], autopct="%1.1f%%")
    plt.title(f"{args.title}: O vs Entity tokens")
    plt.tight_layout()

    out = Path(args.out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    print("Saved:", out)

if __name__ == "__main__":
    main()
