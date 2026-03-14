import argparse
import json
import os
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns  # Optional, but makes heatmaps prettier. If fails, we use matplotlib fallback.
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
    if not path.exists():
        print(f"⚠️ Warning: File not found {path}")
        return []
        
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

def count_entities_in_file(file_path: Path):
    """
    Reads a CoNLL file and counts the entity spans (BIO).
    """
    sents = read_conll(file_path)
    counts = Counter()
    for sent in sents:
        tags = [t for _, t in sent]
        spans = spans_from_bio(tags)
        for (typ, s, e) in spans:
            counts[typ] += 1
    return counts

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

    # macro
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
def plot_bar_chart(x, y, out_png, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(x, y, color='skyblue', edgecolor='black')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    for i, v in enumerate(y):
        plt.text(i, v + (max(y)*0.01), str(v), ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def plot_prf_bar(df_metrics, out_png: Path, title: str):
    plt.figure(figsize=(10, 6))
    x = np.arange(len(df_metrics))
    w = 0.25
    plt.bar(x - w, df_metrics["precision"].values, width=w, label="Precision")
    plt.bar(x, df_metrics["recall"].values, width=w, label="Recall")
    plt.bar(x + w, df_metrics["f1"].values, width=w, label="F1 Score")
    plt.ylim(0, 1.1)
    plt.xticks(x, df_metrics["type"].tolist(), rotation=45, ha="right")
    plt.ylabel("Score")
    plt.title(title)
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

def plot_confusion_matrix(gold_sents, pred_sents, out_png: Path):
    """
    Creates a token-level confusion matrix.
    We only take the entity type (e.g. 'PER', 'LOC') and ignore 'B-'/'I-' prefixes 
    to see the general confusion between categories.
    """
    y_true = []
    y_pred = []

    for (tokens, gold_tags), pred_tags in zip(gold_sents, pred_sents):
        # truncate
        n = min(len(gold_tags), len(pred_tags))
        g = gold_tags[:n]
        p = pred_tags[:n]
        
        # Clean tags: "B-PER" -> "PER", "O" -> "O"
        g_clean = [tag.split('-')[1] if '-' in tag else tag for tag in g]
        p_clean = [tag.split('-')[1] if '-' in tag else tag for tag in p]
        
        y_true.extend(g_clean)
        y_pred.extend(p_clean)

    # Filter out "O" (Outside) if it dominates the chart too much? 
    # Usually better to keep it to see False Positives.
    
    labels = sorted(list(set(y_true + y_pred)))
    
    # Remove MEDICINE if present in labels list just for display cleanliness
    if "MEDICINE" in labels: labels.remove("MEDICINE")

    # Create Matrix
    df_cm = pd.crosstab(pd.Series(y_true, name='Actual'), 
                        pd.Series(y_pred, name='Predicted')).reindex(index=labels, columns=labels, fill_value=0)

    plt.figure(figsize=(10, 8))
    # Log scale helps see small errors vs big 'O' counts
    try:
        sns.heatmap(df_cm, annot=True, fmt='d', cmap='Blues', norm=None) # Standard scale
    except:
        plt.imshow(df_cm, cmap='Blues')
        plt.colorbar()
        
    plt.title("Confusion Matrix (Token Level)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()

# -----------------------------
# Run one model evaluation
# -----------------------------
def evaluate_one_model(model_dir: Path, eval_conll: Path, train_conll: Path, out_dir: Path, max_length: int, device: str):
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Count Training Data (if exists)
    if train_conll and train_conll.exists():
        print(f"   Reading training data from: {train_conll.name}")
        train_counts = count_entities_in_file(train_conll)
        # Filter MEDICINE
        if "MEDICINE" in train_counts: del train_counts["MEDICINE"]
        
        # Plot Training Distribution
        t_labels = sorted(train_counts.keys())
        t_values = [train_counts[k] for k in t_labels]
        plot_bar_chart(t_labels, t_values, out_dir / "training_data_distribution.png", 
                       title="Training Data Count per Entity", ylabel="Number of Spans")
    else:
        print("⚠️ Training file not found. Skipping training count chart.")

    # 2. Load Evaluation Data
    sents = read_conll(eval_conll)
    gold_sents = [([tok for tok, _ in sent], [tag for _, tag in sent]) for sent in sents]
    tokens_only = [x[0] for x in gold_sents]
    gold_tags_only = [x[1] for x in gold_sents]

    # 3. Load model
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForTokenClassification.from_pretrained(model_dir)
    model.to(device)
    model.eval()

    # 4. Predict
    pred_sents = []
    for tokens in tokens_only:
        pred_tags = predict_sentence(model, tokenizer, tokens, device=device, max_length=max_length)
        pred_sents.append(pred_tags)

    # 5. Metrics
    gold_pairs = list(zip(tokens_only, gold_tags_only))
    per_type, overall_micro, overall_macro = compute_span_metrics(gold_pairs, pred_sents)

    df = pd.DataFrame([
        {"type": typ, **vals} for typ, vals in per_type.items()
    ]).sort_values("type")

    # CUSTOM FILTERING
    df = df[df["type"] != "MEDICINE"]
    df = df[df["support_gold"] > 0]

    # Save CSV
    df.to_csv(out_dir / "span_metrics.csv", index=False)

    # 6. Charts
    df_types = df.copy()
    plot_prf_bar(df_types, out_dir / "prf_performance.png", title="Model Performance (Precision/Recall/F1)")
    
    # 7. Confusion Matrix (New Analysis)
    plot_confusion_matrix(gold_pairs, pred_sents, out_dir / "confusion_matrix.png")

    print(f"✅ Generated Reports in: {out_dir}")
    return per_type

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project_root", default=r"D:\DOWNLOADS\BRAVE\LuxNLP")
    ap.add_argument("--out_root", default=r"D:\DOWNLOADS\BRAVE\LuxNLP\model_reports")
    ap.add_argument("--max_length", type=int, default=256)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    project_root = Path(args.project_root)
    out_root = Path(args.out_root)
    
    # -----------------------------
    # MODEL 3 CONFIGURATION
    # -----------------------------
    # I am assuming your training file is named 'train_mixed_3000.conll' based on your test filename.
    # If it is different, please rename it or change it here.
    
    model_name = "model_3_mixed_3000"
    model_dir = project_root / "models" / "xlmr_ner_mixed_3000"
    
    # Evaluation File
    eval_file = project_root / "data" / "processed" / "new_pipeline_v2" / "BALANCED_4K6K_FOCUS" / "test_mixed_3000.conll"
    
    # Training File (Attempting to guess location, otherwise will skip)
    train_file = project_root / "data" / "processed" / "new_pipeline_v2" / "BALANCED_4K6K_FOCUS" / "train.conll"
    
    out_dir = out_root / model_name

    print(f"\n=== Running Advanced Analysis for: {model_name} ===")
    evaluate_one_model(model_dir, eval_file, train_file, out_dir, args.max_length, args.device)

if __name__ == "__main__":
    main()