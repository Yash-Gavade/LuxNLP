from pathlib import Path
from typing import List, Tuple

import numpy as np
from datasets import Dataset, DatasetDict
from seqeval.metrics import (classification_report, f1_score, precision_score,
                             recall_score)
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          DataCollatorForTokenClassification, Trainer,
                          TrainingArguments)

# ======================
# CONFIG
# ======================
DATA_DIR = Path("data/processed/ner_splits_balanced")
DEV_PATH = DATA_DIR / "dev.conll"
TEST_PATH = DATA_DIR / "test.conll"

# Use your checkpoint
CKPT_DIR = "models/lux_ner_xlmr/checkpoint-2000"
MAX_LEN = 128


def read_conll(path: Path) -> List[List[Tuple[str, str]]]:
    sentences = []
    current = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                if current:
                    sentences.append(current)
                    current = []
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            token = " ".join(parts[:-1])
            tag = parts[-1]
            current.append((token, tag))
    if current:
        sentences.append(current)
    return sentences


def conll_to_hf(sentences):
    tokens, tags = [], []
    for sent in sentences:
        t, l = zip(*sent)
        tokens.append(list(t))
        tags.append(list(l))
    return Dataset.from_dict({"tokens": tokens, "ner_tags": tags})


def build_label_maps(ds: DatasetDict):
    labels = set()
    for split in ds:
        for tags in ds[split]["ner_tags"]:
            labels.update(tags)
    labels = sorted(labels)
    if "O" in labels:
        labels.remove("O")
        labels = ["O"] + labels
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}
    return labels, label2id, id2label


def align_labels(labels, word_ids, label2id):
    aligned = []
    prev = None
    for wid in word_ids:
        if wid is None:
            aligned.append(-100)
        else:
            lab = labels[wid]
            if wid == prev and lab.startswith("B-"):
                lab = "I-" + lab[2:]
            aligned.append(label2id.get(lab, label2id["O"]))
        prev = wid
    return aligned


def tokenize_and_align(tokenizer, label2id):
    def fn(examples):
        tok = tokenizer(
            examples["tokens"],
            is_split_into_words=True,
            truncation=True,
            max_length=MAX_LEN,
        )
        new_labels = []
        for i, labels in enumerate(examples["ner_tags"]):
            word_ids = tok.word_ids(batch_index=i)
            new_labels.append(align_labels(labels, word_ids, label2id))
        tok["labels"] = new_labels
        return tok
    return fn


def predict(trainer, dataset, id2label):
    out = trainer.predict(dataset)
    preds = np.argmax(out.predictions, axis=-1)
    labels = out.label_ids

    true_tags, pred_tags = [], []
    for p, l in zip(preds, labels):
        t_sent, p_sent = [], []
        for pi, li in zip(p, l):
            if li == -100:
                continue
            t_sent.append(id2label[li])
            p_sent.append(id2label[pi])
        true_tags.append(t_sent)
        pred_tags.append(p_sent)
    return true_tags, pred_tags


def main():
    dev = conll_to_hf(read_conll(DEV_PATH))
    test = conll_to_hf(read_conll(TEST_PATH))

    dsd = DatasetDict(validation=dev, test=test)
    labels, label2id, id2label = build_label_maps(dsd)

    print("Labels:", labels)

    tokenizer = AutoTokenizer.from_pretrained(CKPT_DIR, use_fast=True)
    model = AutoModelForTokenClassification.from_pretrained(CKPT_DIR)

    tokenized = dsd.map(
        tokenize_and_align(tokenizer, label2id),
        batched=True,
        remove_columns=["tokens", "ner_tags"],
    )

    args = TrainingArguments(
        output_dir="tmp_eval",
        per_device_eval_batch_size=32,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=args,
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),
    )

    print("\n=== DEV RESULTS ===")
    y_true, y_pred = predict(trainer, tokenized["validation"], id2label)
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall   :", recall_score(y_true, y_pred))
    print("F1       :", f1_score(y_true, y_pred))
    print(classification_report(y_true, y_pred))

    print("\n=== TEST RESULTS ===")
    y_true, y_pred = predict(trainer, tokenized["test"], id2label)
    print("Precision:", precision_score(y_true, y_pred))
    print("Recall   :", recall_score(y_true, y_pred))
    print("F1       :", f1_score(y_true, y_pred))
    print(classification_report(y_true, y_pred))


if __name__ == "__main__":
    main()
