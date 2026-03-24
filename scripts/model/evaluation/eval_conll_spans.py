from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

from new_conll_io import Sentence, read_conll


def extract_spans(sent: Sentence) -> List[Tuple[str, int, int]]:
    spans = []
    i = 0
    while i < len(sent):
        tag = sent[i][1]
        if tag.startswith("B-"):
            et = tag.split("-", 1)[1]
            j = i + 1
            while j < len(sent) and sent[j][1] == f"I-{et}":
                j += 1
            spans.append((et, i, j - 1))
            i = j
        else:
            i += 1
    return spans

def score(gold_path: str, pred_path: str) -> None:
    gold = read_conll(gold_path)
    pred = read_conll(pred_path)
    assert len(gold) == len(pred), "Sentence count mismatch"

    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)

    for gs, ps in zip(gold, pred):
        assert len(gs) == len(ps), "Token count mismatch in a sentence"
        gold_sp = set(extract_spans(gs))
        pred_sp = set(extract_spans(ps))

        for sp in pred_sp:
            if sp in gold_sp:
                tp[sp[0]] += 1
            else:
                fp[sp[0]] += 1
        for sp in gold_sp:
            if sp not in pred_sp:
                fn[sp[0]] += 1

    types = sorted(set(tp) | set(fp) | set(fn))
    print("\nSpan-based NER scores")
    print("=" * 60)

    def prf(t):
        T = tp[t]; Fp = fp[t]; Fn = fn[t]
        p = T / (T + Fp) if (T + Fp) else 0.0
        r = T / (T + Fn) if (T + Fn) else 0.0
        f1 = 2*p*r/(p+r) if (p+r) else 0.0
        return p, r, f1, T, Fp, Fn

    micro_T = micro_Fp = micro_Fn = 0
    for t in types:
        p, r, f1, T, Fp, Fn = prf(t)
        micro_T += T; micro_Fp += Fp; micro_Fn += Fn
        print(f"{t:8s}  P={p:6.3f}  R={r:6.3f}  F1={f1:6.3f}   TP={T:4d} FP={Fp:4d} FN={Fn:4d}")

    micro_p = micro_T / (micro_T + micro_Fp) if (micro_T + micro_Fp) else 0.0
    micro_r = micro_T / (micro_T + micro_Fn) if (micro_T + micro_Fn) else 0.0
    micro_f1 = 2*micro_p*micro_r/(micro_p+micro_r) if (micro_p+micro_r) else 0.0
    print("-" * 60)
    print(f"MICRO     P={micro_p:6.3f}  R={micro_r:6.3f}  F1={micro_f1:6.3f}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    args = ap.parse_args()
    score(args.gold, args.pred)
