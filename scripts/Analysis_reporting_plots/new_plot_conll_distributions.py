# scripts/new_plot_conll_distributions.py
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from new_conll_io import Sentence, read_conll


def extract_spans(sent: Sentence):
    spans = []
    i = 0
    while i < len(sent):
        tag = sent[i][1]
        if tag.startswith("B-"):
            t = tag.split("-", 1)[1]
            j = i + 1
            while j < len(sent) and sent[j][1] == f"I-{t}":
                j += 1
            spans.append(t)
            i = j
        else:
            i += 1
    return spans

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conll", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--out_dir", required=True)
    args = ap.parse_args()

    sents = read_conll(args.conll)
    n_tokens = sum(len(s) for s in sents)

    type_token_counts = Counter()
    span_counts = Counter()

    for s in sents:
        for _, tag in s:
            if tag != "O":
                et = tag.split("-", 1)[1]
                type_token_counts[et] += 1
        for t in extract_spans(s):
            span_counts[t] += 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Span plot
    types = sorted(span_counts.keys())
    vals = [span_counts[t] for t in types]

    plt.figure()
    plt.bar(types, vals)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"{args.title} – Entity Spans per Type")
    plt.ylabel("Span count")
    plt.tight_layout()
    span_path = out_dir / f"{args.title}_spans.png"
    plt.savefig(span_path, dpi=200)
    plt.close()

    # Token plot
    types2 = sorted(type_token_counts.keys())
    vals2 = [type_token_counts[t] for t in types2]

    plt.figure()
    plt.bar(types2, vals2)
    plt.xticks(rotation=45, ha="right")
    plt.title(f"{args.title} – Entity Tokens per Type")
    plt.ylabel("Token count")
    plt.tight_layout()
    tok_path = out_dir / f"{args.title}_entity_tokens.png"
    plt.savefig(tok_path, dpi=200)
    plt.close()

    print("Saved:", span_path)
    print("Saved:", tok_path)

if __name__ == "__main__":
    main()
