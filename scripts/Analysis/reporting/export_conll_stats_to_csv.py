# scripts/new_export_conll_stats_to_csv.py
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path

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
    ap.add_argument("--out_csv", required=True)
    args = ap.parse_args()

    sents = read_conll(args.conll)
    n_sents = len(sents)
    n_tokens = sum(len(s) for s in sents)

    tag_counts = Counter()
    type_token_counts = Counter()
    span_counts = Counter()
    sent_has_type = Counter()

    for s in sents:
        for tok, tag in s:
            tag_counts[tag] += 1
            if tag != "O":
                et = tag.split("-", 1)[1]
                type_token_counts[et] += 1

        spans = extract_spans(s)
        if spans:
            for t in set(spans):
                sent_has_type[t] += 1
            for t in spans:
                span_counts[t] += 1

    o_count = tag_counts.get("O", 0)
    entity_tok = n_tokens - o_count
    o_pct = (o_count / n_tokens * 100) if n_tokens else 0
    ent_pct = (entity_tok / n_tokens * 100) if n_tokens else 0

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    types = sorted(set(type_token_counts.keys()) | set(span_counts.keys()) | set(sent_has_type.keys()))

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["TITLE", args.title])
        w.writerow(["FILE", args.conll])
        w.writerow(["SENTENCES", n_sents])
        w.writerow(["TOKENS", n_tokens])
        w.writerow(["O_TOKENS", o_count])
        w.writerow(["O_PCT", f"{o_pct:.2f}"])
        w.writerow(["ENTITY_TOKEN_PCT", f"{ent_pct:.2f}"])
        w.writerow([])

        w.writerow(["TYPE", "ENTITY_TOKEN_COUNT", "ENTITY_TOKEN_PCT", "SPAN_COUNT", "SENTENCES_WITH_TYPE"])
        for t in types:
            tokc = type_token_counts.get(t, 0)
            tokp = (tokc / n_tokens * 100) if n_tokens else 0
            spc = span_counts.get(t, 0)
            sc  = sent_has_type.get(t, 0)
            w.writerow([t, tokc, f"{tokp:.2f}", spc, sc])

    print("Wrote:", out_path)

if __name__ == "__main__":
    main()
