import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt

LINE = re.compile(r"^(DATE|EVENT|LOC|MED|MISC|ORG|PER)\s+P=\s*([0-9.]+)\s+R=\s*([0-9.]+)\s+F1=\s*([0-9.]+)")

def read_f1(path):
    f1 = {}
    for line in open(path, encoding="utf-8"):
        m = LINE.match(line.strip())
        if m:
            label = m.group(1)
            f1[label] = float(m.group(4))
    return f1

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval_dev_txt", required=True)
    ap.add_argument("--eval_test_txt", required=True)
    ap.add_argument("--out_png", required=True)
    args = ap.parse_args()

    dev = read_f1(args.eval_dev_txt)
    test = read_f1(args.eval_test_txt)
    labels = sorted(dev.keys())

    dev_vals = [dev[l] for l in labels]
    test_vals = [test.get(l, 0.0) for l in labels]

    x = range(len(labels))
    plt.figure()
    plt.bar([i - 0.2 for i in x], dev_vals, width=0.4, label="DEV")
    plt.bar([i + 0.2 for i in x], test_vals, width=0.4, label="TEST")
    plt.xticks(list(x), labels)
    plt.ylim(0, 1.05)
    plt.title("Per-class F1 (DEV vs TEST)")
    plt.ylabel("F1")
    plt.legend()
    plt.tight_layout()

    out = Path(args.out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    print("Saved:", out)

if __name__ == "__main__":
    main()
