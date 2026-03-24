import argparse
from collections import Counter, defaultdict

from new_conll_io import read_conll


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", required=True)
    ap.add_argument("--pred", required=True)
    args = ap.parse_args()

    gold = read_conll(args.gold)
    pred = read_conll(args.pred)

    correct = 0
    total = 0

    labels = set()
    conf = defaultdict(lambda: defaultdict(int))

    for gs, ps in zip(gold, pred):
        for (_, g), (_, p) in zip(gs, ps):
            total += 1
            if g == p:
                correct += 1
            labels.add(g); labels.add(p)
            conf[g][p] += 1

    acc = correct / total if total else 0.0
    print("Token-level evaluation")
    print("="*60)
    print(f"Tokens: {total}")
    print(f"Accuracy: {acc:.4f}")

    # Micro P/R/F1 over non-O labels
    non_o = [l for l in labels if l != "O"]
    tp = fp = fn = 0
    for l in non_o:
        tp_l = conf[l][l]
        fp_l = sum(conf[g][l] for g in labels if g != l)
        fn_l = sum(conf[l][p] for p in labels if p != l)
        tp += tp_l; fp += fp_l; fn += fn_l

    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec  = tp / (tp + fn) if (tp + fn) else 0.0
    f1   = (2*prec*rec)/(prec+rec) if (prec+rec) else 0.0

    print("\nToken-level MICRO (excluding O)")
    print(f"P={prec:.4f}  R={rec:.4f}  F1={f1:.4f}")
    print(f"TP={tp} FP={fp} FN={fn}")

if __name__ == "__main__":
    main()
