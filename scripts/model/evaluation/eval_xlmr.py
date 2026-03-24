from pathlib import Path
from typing import List, Tuple

import numpy as np
from datasets import Dataset, DatasetDict
from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          DataCollatorForTokenClassification, Trainer,
                          TrainingArguments)

#  paths
DATA_DIR = Path("data/processed")
DEV_PATH  = DATA_DIR / "dev.conll"
TEST_PATH = DATA_DIR / "test.conll"

#  checkpoint to evaluate
CKPT_DIR = "models/lux_ner_xlmr/checkpoint-2000"


def read_conll(path: Path) -> List[List[Tuple[str, str]]]:
    sents, cur = [], []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                if cur:
                    sents.append(cur)
                    cur = []
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            token = " ".join(parts[:-1])
            tag = parts[-1]
            cur.append((token, tag))
    if cur:
        sents.append(cur)
    return sents


def conll_to_hf(sentences):
    tokens, tags = [], []
    for sent in sentences:
        t, y = zip(*sent)
        tokens.append(list(t))
        tags.append(list(y))
    return Dataset.from_dict({"tokens": tokens, "ner_tags": tags})


def align_labels_with_tokens(labels, word_ids, label2id):
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


def compute_f1_seqeval(pred_ids, label_ids, id2label):
    """
    Minimal seqeval-like micro F1 without installing evaluate/seqeval.
    (Good enough for quick check.)
    """
    def strip_special(seq):
        out = []
        for p, l in zip(seq[0], seq[1]):
            if l == -100:
                continue
            out.append((id2label[p], id2label[l]))
        return out

    y_true, y_pred = [], []
    for p, l in zip(pred_ids, label_ids):
        pairs = strip_special((p, l))
        y_pred.append([pp for pp, _ in pairs])
        y_true.append([ll for _, ll in pairs])

    # compute entity-level F1
    try:
        from seqeval.metrics import (accuracy_score, f1_score, precision_score,
                                     recall_score)
        return {
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred),
            "accuracy": accuracy_score(y_true, y_pred),
        }
    except Exception:
        
        correct = 0
        total = 0
        for yt, yp in zip(y_true, y_pred):
            for a, b in zip(yt, yp):
                total += 1
                correct += int(a == b)
        return {"token_accuracy": correct / total if total else 0.0}


def main():
    model = AutoModelForTokenClassification.from_pretrained(CKPT_DIR)
    tokenizer = AutoTokenizer.from_pretrained(CKPT_DIR, use_fast=True)

    # labels from model
    id2label = model.config.id2label
    label2id = {v: int(k) if isinstance(k, str) else k for k, v in id2label.items()}
    # fix if id2label keys are strings
    if any(isinstance(k, str) for k in id2label.keys()):
        id2label = {int(k): v for k, v in id2label.items()}
        label2id = {v: k for k, v in id2label.items()}

    dev = conll_to_hf(read_conll(DEV_PATH))
    test = conll_to_hf(read_conll(TEST_PATH))

    datasets = DatasetDict(validation=dev, test=test)

    def tokenize_and_align(examples):
        tok = tokenizer(examples["tokens"], is_split_into_words=True, truncation=True, max_length=128)
        new_labels = []
        for i, labels in enumerate(examples["ner_tags"]):
            wids = tok.word_ids(batch_index=i)
            new_labels.append(align_labels_with_tokens(labels, wids, label2id))
        tok["labels"] = new_labels
        return tok

    tokenized = datasets.map(tokenize_and_align, batched=True, remove_columns=["tokens", "ner_tags"])
    collator = DataCollatorForTokenClassification(tokenizer)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(output_dir="tmp_eval", per_device_eval_batch_size=32, report_to=[]),
        tokenizer=tokenizer,
        data_collator=collator,
    )

    print("\nEvaluating DEV...")
    dev_out = trainer.predict(tokenized["validation"])
    dev_metrics = compute_f1_seqeval(
        np.argmax(dev_out.predictions, axis=-1),
        dev_out.label_ids,
        id2label
    )
    print("DEV metrics:", dev_metrics)

    print("\nEvaluating TEST...")
    test_out = trainer.predict(tokenized["test"])
    test_metrics = compute_f1_seqeval(
        np.argmax(test_out.predictions, axis=-1),
        test_out.label_ids,
        id2label
    )
    print("TEST metrics:", test_metrics)


if __name__ == "__main__":
    main()
