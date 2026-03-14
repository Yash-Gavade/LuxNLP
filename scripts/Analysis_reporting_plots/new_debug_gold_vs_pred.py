# scripts/new_debug_gold_vs_pred.py
from __future__ import annotations

from new_conll_io import read_conll


def spans(sent):
    out = []
    i = 0
    while i < len(sent):
        tok, tag = sent[i]
        if tag.startswith("B-"):
            t = tag.split("-", 1)[1]
            j = i + 1
            while j < len(sent) and sent[j][1] == f"I-{t}":
                j += 1
            out.append((t, i, j, " ".join(x for x,_ in sent[i:j])))
            i = j
        else:
            i += 1
    return out

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    ap.add_argument("--type", default="DATE")
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()

    gold = read_conll(args.gold)
    pred = read_conll(args.pred)

    shown = 0
    for g, p in zip(gold, pred):
        gs = [s for s in spans(g) if s[0] == args.type]
        ps = [s for s in spans(p) if s[0] == args.type]
        if not gs and not ps:
            continue

        print("\n" + "="*80)
        print("SENT:", " ".join(tok for tok,_ in g))
        print("GOLD spans:", [x[3] for x in gs])
        print("PRED spans:", [x[3] for x in ps])

        shown += 1
        if shown >= args.n:
            break

if __name__ == "__main__":
    main()
