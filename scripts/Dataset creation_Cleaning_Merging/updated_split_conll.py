# scripts/updated_split_conll.py
import argparse
import random
from pathlib import Path


def read_conll_sentences(path: Path):
    sents, cur = [], []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sents.append(cur)
                    cur = []
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            token = " ".join(parts[:-1])
            tag = parts[-1]
            cur.append((token, tag))
    if cur:
        sents.append(cur)
    return sents

def write_conll_sentences(sents, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for sent in sents:
            for tok, tag in sent:
                f.write(f"{tok} {tag}\n")
            f.write("\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--train", type=float, default=0.90)
    ap.add_argument("--dev", type=float, default=0.05)
    ap.add_argument("--test", type=float, default=0.05)
    args = ap.parse_args()

    assert abs((args.train + args.dev + args.test) - 1.0) < 1e-9, "train+dev+test must sum to 1.0"

    inp = Path(args.input)
    out_dir = Path(args.out_dir)

    sents = read_conll_sentences(inp)
    random.seed(args.seed)
    random.shuffle(sents)

    n = len(sents)
    n_train = int(n * args.train)
    n_dev = int(n * args.dev)
    n_test = n - n_train - n_dev

    train_s = sents[:n_train]
    dev_s = sents[n_train:n_train+n_dev]
    test_s = sents[n_train+n_dev:]

    write_conll_sentences(train_s, out_dir / "train.conll")
    write_conll_sentences(dev_s, out_dir / "dev.conll")
    write_conll_sentences(test_s, out_dir / "test.conll")

    print("Wrote:")
    print(" ", out_dir / "train.conll", len(train_s), "sentences")
    print(" ", out_dir / "dev.conll", len(dev_s), "sentences")
    print(" ", out_dir / "test.conll", len(test_s), "sentences")

if __name__ == "__main__":
    main()
