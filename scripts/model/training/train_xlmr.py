import argparse
import numpy as np
import re
from typing import Dict, List, Tuple

import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification,
    set_seed,
)

# -------------------------
# CoNLL Reader
# -------------------------
def read_conll(path: str) -> List[Tuple[List[str], List[str]]]:
    """
    Reads a CoNLL file with: TOKEN ... TAG (TAG in last column)
    Returns list of (tokens, tags).
    """
    sents = []
    tokens, tags = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if tokens:
                    sents.append((tokens, tags))
                    tokens, tags = [], []
                continue
            parts = line.split()
            tokens.append(parts[0])
            tags.append(parts[-1])
    if tokens:
        sents.append((tokens, tags))
    return sents

def get_label_list(*splits) -> List[str]:
    labels = set()
    for sents in splits:
        for _, tags in sents:
            for t in tags:
                labels.add(t)
    labels = sorted(labels)
    # Ensure O first for stability
    if "O" in labels:
        labels.remove("O")
        labels = ["O"] + labels
    return labels

# -------------------------
# Tokenize + Align labels
# -------------------------
def tokenize_and_align(examples, tokenizer, label2id, max_length: int):
    tokenized = tokenizer(
        examples["tokens"],
        is_split_into_words=True,
        truncation=True,
        max_length=max_length,
    )

    labels = []
    for i, word_labels in enumerate(examples["tags"]):
        word_ids = tokenized.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)
            elif word_idx != previous_word_idx:
                label_ids.append(label2id[word_labels[word_idx]])
            else:
                
                label_ids.append(-100)
            previous_word_idx = word_idx
        labels.append(label_ids)

    tokenized["labels"] = labels
    return tokenized

# -------------------------
# Span-level F1 (BIO)
# -------------------------
def bio_to_spans(tags: List[str]) -> set:
    """
    Convert BIO tags to spans: (TYPE, start, endExclusive)
    Only spans starting with B- are counted.
    """
    spans = set()
    i = 0
    while i < len(tags):
        tag = tags[i]
        if tag.startswith("B-"):
            typ = tag[2:]
            j = i + 1
            while j < len(tags) and tags[j] == f"I-{typ}":
                j += 1
            spans.add((typ, i, j))
            i = j
        else:
            i += 1
    return spans

def compute_metrics(eval_pred, id2label: Dict[int, str]):
    """
    Computes micro span-level precision/recall/F1 over all sequences.
    """
    predictions, labels = eval_pred
    pred_ids = np.argmax(predictions, axis=2)

    tp = fp = fn = 0

    for pred_seq, gold_seq in zip(pred_ids, labels):
        pred_tags = []
        gold_tags = []

        for pred_id, gold_id in zip(pred_seq, gold_seq):
            if gold_id == -100:
                continue
            pred_tags.append(id2label[int(pred_id)])
            gold_tags.append(id2label[int(gold_id)])

        gold_spans = bio_to_spans(gold_tags)
        pred_spans = bio_to_spans(pred_tags)

        tp += len(gold_spans & pred_spans)
        fp += len(pred_spans - gold_spans)
        fn += len(gold_spans - pred_spans)

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

# -------------------------
# Main
# -------------------------
def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--model_name_or_path", default="xlm-roberta-base")
    ap.add_argument("--train_file", required=True)
    ap.add_argument("--dev_file", required=True)
    ap.add_argument("--test_file", required=True)
    ap.add_argument("--output_dir", required=True)

    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--num_train_epochs", type=int, default=5)
    ap.add_argument("--learning_rate", type=float, default=2e-5)
    ap.add_argument("--weight_decay", type=float, default=0.01)
    ap.add_argument("--per_device_train_batch_size", type=int, default=8)
    ap.add_argument("--per_device_eval_batch_size", type=int, default=16)
    ap.add_argument("--max_length", type=int, default=256)

    ap.add_argument("--load_best_model_at_end", type=str, default="false")
    ap.add_argument("--metric_for_best_model", default="f1")
    ap.add_argument("--greater_is_better", type=str, default="true")

    args = ap.parse_args()

    set_seed(args.seed)

    # Read data
    train_sents = read_conll(args.train_file)
    dev_sents = read_conll(args.dev_file)
    test_sents = read_conll(args.test_file)

    label_list = get_label_list(train_sents, dev_sents, test_sents)
    label2id = {l: i for i, l in enumerate(label_list)}
    id2label = {i: l for l, i in label2id.items()}

    print("Labels:", label_list)
    print("Train sentences:", len(train_sents))
    print("Dev sentences:", len(dev_sents))
    print("Test sentences:", len(test_sents))

    tokenizer = AutoTokenizer.from_pretrained(args.model_name_or_path, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(
        args.model_name_or_path,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id,
    )

    # Convert to HF datasets
    def to_dataset(sents):
        return Dataset.from_dict({
            "tokens": [t for t, _ in sents],
            "tags":   [y for _, y in sents],
        })

    train_ds = to_dataset(train_sents)
    dev_ds = to_dataset(dev_sents)
    test_ds = to_dataset(test_sents)

    # Tokenize
    train_tok = train_ds.map(lambda x: tokenize_and_align(x, tokenizer, label2id, args.max_length), batched=True)
    dev_tok   = dev_ds.map(lambda x: tokenize_and_align(x, tokenizer, label2id, args.max_length), batched=True)
    test_tok  = test_ds.map(lambda x: tokenize_and_align(x, tokenizer, label2id, args.max_length), batched=True)

    # --- TrainingArguments: compatibility mode ---
    ta_kwargs = dict(
        output_dir=args.output_dir,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        num_train_epochs=args.num_train_epochs,
        per_device_train_batch_size=args.per_device_train_batch_size,
        per_device_eval_batch_size=args.per_device_eval_batch_size,
        logging_steps=50,
        save_total_limit=3,
        report_to="none",
    )

    try:
        training_args = TrainingArguments(**ta_kwargs)
    except TypeError:
        ta_kwargs.pop("report_to", None)
        training_args = TrainingArguments(**ta_kwargs)

    data_collator = DataCollatorForTokenClassification(tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        eval_dataset=dev_tok,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=lambda p: compute_metrics(p, id2label),
    )

    # Train
    trainer.train()

    # Evaluate on DEV
    print("\n=== DEV EVAL ===")
    dev_metrics = trainer.evaluate(dev_tok)
    for k, v in dev_metrics.items():
        if isinstance(v, float):
            print(f"{k}: {v:.4f}")
        else:
            print(f"{k}: {v}")

    # Final eval on TEST
    print("\n=== FINAL TEST EVAL ===")
    test_metrics = trainer.evaluate(test_tok)
    for k, v in test_metrics.items():
        if isinstance(v, float):
            print(f"{k}: {v:.4f}")
        else:
            print(f"{k}: {v}")

    # Save model + tokenizer
    trainer.save_model(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    print(f"\n Saved to: {args.output_dir}")

if __name__ == "__main__":
    main()
