import argparse
import random
from pathlib import Path


def read_conll_sentences(path):
    sentences = []
    current = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                if current:
                    sentences.append(current)
                    current = []
            else:
                current.append(line)

        if current:
            sentences.append(current)

    return sentences


def write_conll_sentences(sentences, path):
    with open(path, "w", encoding="utf-8") as f:
        for sent in sentences:
            for line in sent:
                f.write(line + "\n")
            f.write("\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_conll", required=True)
    parser.add_argument("--out_dir", required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)

    sentences = read_conll_sentences(args.in_conll)
    total = len(sentences)

    print(f"Total sentences: {total}")

    random.shuffle(sentences)

    n_train = int(0.70 * total)
    n_dev = int(0.15 * total)
    n_test = total - n_train - n_dev  # safe remainder

    train_sents = sentences[:n_train]
    dev_sents = sentences[n_train:n_train + n_dev]
    test_sents = sentences[n_train + n_dev:]

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    write_conll_sentences(train_sents, out_dir / "train.conll")
    write_conll_sentences(dev_sents, out_dir / "dev.conll")
    write_conll_sentences(test_sents, out_dir / "test.conll")

    print("Split complete ✅")
    print(f"Train: {len(train_sents)} ({len(train_sents)/total:.1%})")
    print(f"Dev:   {len(dev_sents)} ({len(dev_sents)/total:.1%})")
    print(f"Test:  {len(test_sents)} ({len(test_sents)/total:.1%})")


if __name__ == "__main__":
    main()
