# scripts/new_eval_xlmr_conll_spanf1.py
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


# -----------------------------
# CoNLL IO
# -----------------------------
def read_conll(path: Path):
    sents = []
    toks, gold = [], []
    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if toks:
                    sents.append((toks, gold))
                    toks, gold = [], []
                continue
            parts = re.split(r"\s+", line.strip())
            if len(parts) < 2:
                continue
            toks.append(parts[0])
            gold.append(parts[-1])
    if toks:
        sents.append((toks, gold))
    return sents


def write_conll(tokens_and_labels, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        for toks, labs in tokens_and_labels:
            for t, y in zip(toks, labs):
                f.write(f"{t}\t{y}\n")
            f.write("\n")


# -----------------------------
# Span extraction (BIO)
# -----------------------------
def spans_from_bio(labels):
    spans = []
    i = 0
    while i < len(labels):
        y = labels[i]
        if y.startswith("B-"):
            typ = y[2:]
            j = i + 1
            while j < len(labels) and labels[j] == f"I-{typ}":
                j += 1
            spans.append((i, j, typ))
            i = j
        else:
            i += 1
    return spans


def span_f1(gold_labels, pred_labels):
    """
    Exact-match spans: (start, end, type)
    """
    g = set(spans_from_bio(gold_labels))
    p = set(spans_from_bio(pred_labels))

    tp = len(g & p)
    fp = len(p - g)
    fn = len(g - p)

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return tp, fp, fn, prec, rec, f1


def per_type_span_f1(gold_labels, pred_labels):
    g_spans = spans_from_bio(gold_labels)
    p_spans = spans_from_bio(pred_labels)

    g_by = defaultdict(set)
    p_by = defaultdict(set)

    for s in g_spans:
        g_by[s[2]].add(s)
    for s in p_spans:
        p_by[s[2]].add(s)

    all_types = sorted(set(g_by.keys()) | set(p_by.keys()))
    rows = {}
    for t in all_types:
        g = g_by[t]
        p = p_by[t]
        tp = len(g & p)
        fp = len(p - g)
        fn = len(g - p)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
        rows[t] = (tp, fp, fn, prec, rec, f1)
    return rows


# -----------------------------
# Prediction
# -----------------------------
def predict_sentence(model, tokenizer, tokens, id2label, device, max_len=256):
    """
    Predict one sentence while preserving word-level alignment (one label per original token).
    """
    enc = tokenizer(
        tokens,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        max_length=max_len,
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        out = model(**enc)
        logits = out.logits  # [1, seq, num_labels]
        pred_ids = logits.argmax(dim=-1)[0].tolist()

    word_ids = enc["input_ids"].new_tensor([0])  # dummy just to keep type
    # Get word_ids via tokenizer API
    # transformers returns list on CPU; we use the original encoding object:
    word_id_list = tokenizer(tokens, is_split_into_words=True, truncation=True, max_length=max_len).word_ids()

    # Choose first subtoken label for each word
    pred_word = ["O"] * len(tokens)
    seen = set()
    for idx, wid in enumerate(word_id_list):
        if wid is None:
            continue
        if wid in seen:
            continue
        seen.add(wid)
        pred_word[wid] = id2label[pred_ids[idx]]

    # Basic BIO repair to avoid I- starting incorrectly
    repaired = []
    prev_tag = "O"
    prev_type = None
    for lab in pred_word:
        if lab == "O":
            repaired.append("O")
            prev_tag, prev_type = "O", None
            continue
        if "-" not in lab:
            repaired.append("O")
            prev_tag, prev_type = "O", None
            continue
        tag, typ = lab.split("-", 1)
        if tag == "B":
            repaired.append(lab)
            prev_tag, prev_type = "B", typ
        elif tag == "I":
            if prev_tag == "O" or prev_type != typ:
                repaired.append(f"B-{typ}")
                prev_tag, prev_type = "B", typ
            else:
                repaired.append(lab)
                prev_tag, prev_type = "I", typ
        else:
            repaired.append("O")
            prev_tag, prev_type = "O", None

    return repaired


def evaluate_split(model_dir: Path, conll_path: Path, out_pred: Path, max_len: int):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_dir, local_files_only=True)
    model = AutoModelForTokenClassification.from_pretrained(model_dir, local_files_only=True).to(device)
    model.eval()

    id2label = model.config.id2label

    sents = read_conll(conll_path)
    preds_out = []
    gold_all = []
    pred_all = []

    for tokens, gold in sents:
        pred = predict_sentence(model, tokenizer, tokens, id2label, device, max_len=max_len)
        preds_out.append((tokens, pred))
        gold_all.append(gold)
        pred_all.append(pred)

    # Write prediction file
    write_conll(preds_out, out_pred)

    # Compute micro span F1
    tp = fp = fn = 0
    for g, p in zip(gold_all, pred_all):
        tpi, fpi, fni, _, _, _ = span_f1(g, p)
        tp += tpi
        fp += fpi
        fn += fni

    prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0

    # Per-type
    per_type = Counter()
    per_type_tp = Counter()
    per_type_fp = Counter()
    per_type_fn = Counter()

    for g, p in zip(gold_all, pred_all):
        rows = per_type_span_f1(g, p)
        for t, (tpi, fpi, fni, _, _, _) in rows.items():
            per_type_tp[t] += tpi
            per_type_fp[t] += fpi
            per_type_fn[t] += fni
            per_type[t] += 1

    return (prec, rec, f1, tp, fp, fn, per_type_tp, per_type_fp, per_type_fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True, help="Path to local HF model dir, e.g. models/xlmr_all_hard_v1")
    ap.add_argument("--split_dir", required=True, help="Folder containing train/dev/test conll files")
    ap.add_argument("--out_dir", required=True, help="Where to write predictions + eval txt")
    ap.add_argument("--max_len", type=int, default=256)
    args = ap.parse_args()

    model_dir = Path(args.model_dir)
    split_dir = Path(args.split_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dev = split_dir / "dev.conll"
    test = split_dir / "test.conll"

    # DEV
    dev_pred = out_dir / "pred_dev.conll"
    prec, rec, f1, tp, fp, fn, ttp, tfp, tfn = evaluate_split(model_dir, dev, dev_pred, args.max_len)
    dev_txt = out_dir / "eval_dev.txt"
    with dev_txt.open("w", encoding="utf-8") as f:
        f.write(f"DEV micro span-F1 (exact match)\n")
        f.write(f"TP={tp} FP={fp} FN={fn}\n")
        f.write(f"P={prec:.4f} R={rec:.4f} F1={f1:.4f}\n\n")
        f.write("Per-type:\n")
        for t in sorted(set(list(ttp.keys()) + list(tfp.keys()) + list(tfn.keys()))):
            tp_t, fp_t, fn_t = ttp[t], tfp[t], tfn[t]
            p_t = tp_t / (tp_t + fp_t) if (tp_t + fp_t) else 0.0
            r_t = tp_t / (tp_t + fn_t) if (tp_t + fn_t) else 0.0
            f1_t = 2*p_t*r_t/(p_t+r_t) if (p_t+r_t) else 0.0
            f.write(f"{t:10s} TP={tp_t} FP={fp_t} FN={fn_t} P={p_t:.4f} R={r_t:.4f} F1={f1_t:.4f}\n")

    # TEST
    test_pred = out_dir / "pred_test.conll"
    prec, rec, f1, tp, fp, fn, ttp, tfp, tfn = evaluate_split(model_dir, test, test_pred, args.max_len)
    test_txt = out_dir / "eval_test.txt"
    with test_txt.open("w", encoding="utf-8") as f:
        f.write(f"TEST micro span-F1 (exact match)\n")
        f.write(f"TP={tp} FP={fp} FN={fn}\n")
        f.write(f"P={prec:.4f} R={rec:.4f} F1={f1:.4f}\n\n")
        f.write("Per-type:\n")
        for t in sorted(set(list(ttp.keys()) + list(tfp.keys()) + list(tfn.keys()))):
            tp_t, fp_t, fn_t = ttp[t], tfp[t], tfn[t]
            p_t = tp_t / (tp_t + fp_t) if (tp_t + fp_t) else 0.0
            r_t = tp_t / (tp_t + fn_t) if (tp_t + fn_t) else 0.0
            f1_t = 2*p_t*r_t/(p_t+r_t) if (p_t+r_t) else 0.0
            f.write(f"{t:10s} TP={tp_t} FP={fp_t} FN={fn_t} P={p_t:.4f} R={r_t:.4f} F1={f1_t:.4f}\n")

    print("✅ Wrote:")
    print(dev_pred)
    print(dev_txt)
    print(test_pred)
    print(test_txt)
    print("\nOpen eval_dev.txt / eval_test.txt to see F1.")


if __name__ == "__main__":
    main()
