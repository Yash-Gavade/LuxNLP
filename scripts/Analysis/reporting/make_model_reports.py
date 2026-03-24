import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer


# -----------------------------
# CoNLL parsing
# -----------------------------

def read_conll(path: Path):
    """
    Returns list of sentences: each sentence is list of (token, tag)
    """
    sents = []
    cur = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sents.append(cur)
                    cur = []
                continue
            parts = line.split()
            tok = parts[0]
            tag = parts[-1]
            cur.append((tok, tag))
    if cur:
        sents.append(cur)
    return sents


# -----------------------------
# BIO span extraction
# -----------------------------

def spans_from_bio(tags):
    """
    BIO spans -> list of (type, start, end_exclusive)
    """
    spans = []
    i = 0
    while i < len(tags):
        tag = tags[i]
        if tag.startswith("B-"):
            typ = tag[2:]
            j = i + 1
            while j < len(tags) and tags[j] == f"I-{typ}":
                j += 1
            spans.append((typ, i, j))
            i = j
        else:
            i += 1
    return spans


# -----------------------------
# Predict tags aligned to words
# -----------------------------

@torch.no_grad()
def predict_sentence(model, tokenizer, tokens, device, max_length=256):
    enc = tokenizer(
        tokens,
        is_split_into_words=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}
    logits = model(**enc).logits[0]  # [seq, labels]
    pred_ids = torch.argmax(logits, dim=-1).cpu().tolist()

    # align to words: take first subtoken for each word
    word_ids = tokenizer(tokens, is_split_into_words=True, truncation=True, max_length=max_length).word_ids()
    pred_word_tags = []
    seen = set()
    for idx, wid in enumerate(word_ids):
        if wid is None or wid in seen:
            continue
        seen.add(wid)
        pred_word_tags.append(model.config.id2label[int(pred_ids[idx])])

    return pred_word_tags


# -----------------------------
# Metrics: per-type + overall
# -----------------------------
def compute_span_metrics(gold_sents, pred_sents):
    """
    gold_sents: list of (tokens, gold_tags) word-level
    pred_sents: list of pred_tags word-level
    Returns:
      per_type: dict type -> dict(tp, fp, fn, precision, recall, f1, support_gold)
      overall_micro: dict
    """
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)
    support_gold = defaultdict(int)

    all_types = set()

    for (tokens, gold_tags), pred_tags in zip(gold_sents, pred_sents):
        # truncate to same length
        n = min(len(gold_tags), len(pred_tags), len(tokens))
        gold_tags = gold_tags[:n]
        pred_tags = pred_tags[:n]

        gold_spans = spans_from_bio(gold_tags)
        pred_spans = spans_from_bio(pred_tags)

        gold_set = set(gold_spans)
        pred_set = set(pred_spans)

        for (typ, s, e) in gold_spans:
            support_gold[typ] += 1
            all_types.add(typ)
        for (typ, s, e) in pred_spans:
            all_types.add(typ)

        inter = gold_set & pred_set
        for (typ, s, e) in inter:
            tp[typ] += 1

        for (typ, s, e) in (pred_set - gold_set):
            fp[typ] += 1

        for (typ, s, e) in (gold_set - pred_set):
            fn[typ] += 1

    # per-type metrics
    per_type = {}
    for typ in sorted(all_types):
        tpi, fpi, fni = tp[typ], fp[typ], fn[typ]
        prec = tpi / (tpi + fpi) if (tpi + fpi) else 0.0
        rec = tpi / (tpi + fni) if (tpi + fni) else 0.0
        f1 = (2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0
        per_type[typ] = {
            "tp": tpi,
            "fp": fpi,
            "fn": fni,
            "precision": prec,
            "recall": rec,
            "f1": f1,
            "support_gold": support_gold[typ],
        }

    # overall micro
    TP = sum(tp.values())
    FP = sum(fp.values())
    FN = sum(fn.values())
    micro_p = TP / (TP + FP) if (TP + FP) else 0.0
    micro_r = TP / (TP + FN) if (TP + FN) else 0.0
    micro_f1 = (2 * micro_p * micro_r / (micro_p + micro_r)) if (micro_p + micro_r) else 0.0

    overall_micro = {
        "tp": TP,
        "fp": FP,
        "fn": FN,
        "precision": micro_p,
        "recall": micro_r,
        "f1": micro_f1,
        "support_gold": sum(support_gold.values()),
    }

    # macro (simple mean over types that have support)
    supported_types = [t for t in per_type if per_type[t]["support_gold"] > 0]
    if supported_types:
        macro_f1 = float(np.mean([per_type[t]["f1"] for t in supported_types]))
        macro_p = float(np.mean([per_type[t]["precision"] for t in supported_types]))
        macro_r = float(np.mean([per_type[t]["recall"] for t in supported_types]))
    else:
        macro_f1 = macro_p = macro_r = 0.0

    overall_macro = {"precision": macro_p, "recall": macro_r, "f1": macro_f1, "types_count": len(supported_types)}

    return per_type, overall_micro, overall_macro


# -----------------------------
# Charts
# -----------------------------
def plot_f1_bar(df_metrics, out_png: Path, title: str):
    plt.figure()
    x = df_metrics["type"].tolist()
    y = df_metrics["f1"].tolist()
    plt.bar(x, y)
    plt.ylim(0, 1)
    plt.ylabel("F1")
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_prf_bar(df_metrics, out_png: Path, title: str):
    plt.figure()
    x = np.arange(len(df_metrics))
    w = 0.25
    plt.bar(x - w, df_metrics["precision"].values, width=w, label="precision")
    plt.bar(x, df_metrics["recall"].values, width=w, label="recall")
    plt.bar(x + w, df_metrics["f1"].values, width=w, label="f1")
    plt.ylim(0, 1)
    plt.xticks(x, df_metrics["type"].tolist(), rotation=45, ha="right")
    plt.ylabel("Score")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_pie_support(df_metrics, out_png: Path, title: str):
    plt.figure()
    sizes = df_metrics["support_gold"].values
    labels = df_metrics["type"].tolist()
    # Avoid empty pie
    if sizes.sum() == 0:
        plt.text(0.5, 0.5, "No entity spans found", ha="center", va="center")
        plt.axis("off")
    else:
        plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def plot_learning_rate(model_dir: Path, out_png: Path, title: str):
    """
    Reads trainer_state.json if exists and plots learning_rate over steps.
    """
    state_path = model_dir / "trainer_state.json"
    if not state_path.exists():
        # create a placeholder plot
        plt.figure()
        plt.text(0.5, 0.5, "trainer_state.json not found\n(no LR history)", ha="center", va="center")
        plt.axis("off")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        plt.close()
        return

    with open(state_path, "r", encoding="utf-8") as f:
        state = json.load(f)

    lr_points = []
    for item in state.get("log_history", []):
        if "learning_rate" in item:
            step = item.get("step", None)
            lr = item.get("learning_rate", None)
            if step is not None and lr is not None:
                lr_points.append((step, lr))

    if not lr_points:
        plt.figure()
        plt.text(0.5, 0.5, "No learning_rate entries in trainer_state.json", ha="center", va="center")
        plt.axis("off")
        plt.title(title)
        plt.tight_layout()
        plt.savefig(out_png, dpi=200)
        plt.close()
        return

    lr_points.sort(key=lambda x: x[0])
    steps = [s for s, _ in lr_points]
    lrs = [lr for _, lr in lr_points]

    plt.figure()
    plt.plot(steps, lrs)
    plt.xlabel("Step")
    plt.ylabel("Learning rate")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


# -----------------------------
# Run one model evaluation
# -----------------------------

def evaluate_one_model(model_dir: Path, conll_path: Path, out_dir: Path, max_length: int, device: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load data
    sents = read_conll(conll_path)
    gold_sents = [([tok for tok, _ in sent], [tag for _, tag in sent]) for sent in sents]
    tokens_only = [x[0] for x in gold_sents]
    gold_tags_only = [x[1] for x in gold_sents]

    # Load model
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    model.to(device)
    model.eval()

    # Predict
    pred_sents = []
    for tokens in tokens_only:
        pred_tags = predict_sentence(model, tokenizer, tokens, device=device, max_length=max_length)
        pred_sents.append(pred_tags)

    # Metrics
    gold_pairs = list(zip(tokens_only, gold_tags_only))
    per_type, overall_micro, overall_macro = compute_span_metrics(gold_pairs, pred_sents)

    df = pd.DataFrame([
        {"type": typ, **vals} for typ, vals in per_type.items()
    ]).sort_values("type")

    # Add overall row
    overall_row = {
        "type": "OVERALL_MICRO",
        **overall_micro
    }
    df_overall = pd.DataFrame([overall_row])
    df_all = pd.concat([df, df_overall], ignore_index=True)

    # Save CSV
    df_all.to_csv(out_dir / "span_metrics.csv", index=False)

    # Save summary JSON
    summary = {
        "model_dir": str(model_dir),
        "eval_file": str(conll_path),
        "overall_micro": overall_micro,
        "overall_macro": overall_macro,
        "num_sentences": len(sents),
    }
    with open(out_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Charts (exclude OVERALL row for per-type plots)
    df_types = df.copy()
    plot_f1_bar(df_types, out_dir / "f1_per_type.png", title=f"F1 per entity type\n{model_dir.name}")
    plot_prf_bar(df_types, out_dir / "prf_per_type.png", title=f"Precision/Recall/F1 per type\n{model_dir.name}")
    plot_pie_support(df_types, out_dir / "gold_support_pie.png", title=f"Gold span distribution\n{model_dir.name}")
    plot_learning_rate(model_dir, out_dir / "learning_rate.png", title=f"Learning rate\n{model_dir.name}")

    # Also save a quick text report
    with open(out_dir / "report.txt", "w", encoding="utf-8") as f:
        f.write(f"MODEL: {model_dir}\n")
        f.write(f"EVAL : {conll_path}\n")
        f.write(f"SENTS: {len(sents)}\n\n")
        f.write("OVERALL MICRO:\n")
        f.write(json.dumps(overall_micro, indent=2) + "\n\n")
        f.write("OVERALL MACRO:\n")
        f.write(json.dumps(overall_macro, indent=2) + "\n\n")
        f.write("PER TYPE:\n")
        f.write(df.to_string(index=False) + "\n")

    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project_root", default=r"D:\DOWNLOADS\BRAVE\LuxNLP")
    ap.add_argument("--out_root", default=r"D:\DOWNLOADS\BRAVE\LuxNLP\model_reports")
    ap.add_argument("--max_length", type=int, default=256)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    project_root = Path(args.project_root)
    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)

    # -----------------------------
    # models + their test files
    # -----------------------------
    
    MODELS = [

        {
            "name": "xlmr_model",
            "model_dir": project_root / "models" / "xlmr_ner",
            "eval_conll": project_root / "data" / "processed" / "test.conll",
        },
    ]

    all_summaries = []

    for m in MODELS:
        name = m["name"]
        model_dir = Path(m["model_dir"])
        eval_conll = Path(m["eval_conll"])
        out_dir = out_root / name

        if not model_dir.exists():
            print(f"[SKIP] Model dir not found: {model_dir}")
            continue
        if not eval_conll.exists():
            print(f"[SKIP] Eval file not found: {eval_conll}")
            continue

        print(f"\n=== Evaluating: {name} ===")
        print("Model:", model_dir)
        print("Eval :", eval_conll)
        summary = evaluate_one_model(model_dir, eval_conll, out_dir, args.max_length, args.device)
        all_summaries.append(summary)
        print(f"✅ Done: {out_dir}")

    # Save master summary CSV
    rows = []
    for s in all_summaries:
        rows.append({
            "model_dir": s["model_dir"],
            "eval_file": s["eval_file"],
            "num_sentences": s["num_sentences"],
            "micro_precision": s["overall_micro"]["precision"],
            "micro_recall": s["overall_micro"]["recall"],
            "micro_f1": s["overall_micro"]["f1"],
            "macro_precision": s["overall_macro"]["precision"],
            "macro_recall": s["overall_macro"]["recall"],
            "macro_f1": s["overall_macro"]["f1"],
            "macro_types_count": s["overall_macro"]["types_count"],
        })

    if rows:
        pd.DataFrame(rows).to_csv(out_root / "summary_all_models.csv", index=False)
        print(f"\n✅ Wrote: {out_root / 'summary_all_models.csv'}")

    print(f"\n✅ All reports are in: {out_root}")


if __name__ == "__main__":
    main()
