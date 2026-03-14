import os
from pathlib import Path
from typing import List, Tuple

import numpy as np
from datasets import Dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
)

# Paths to your CoNLL splits (balanced)
DATA_DIR = Path("data/processed/ner_splits_balanced")
TRAIN_PATH = DATA_DIR / "train.conll"
DEV_PATH = DATA_DIR / "dev.conll"
TEST_PATH = DATA_DIR / "test.conll"

# Model checkpoint (multilingual – good for Luxembourgish)
MODEL_CHECKPOINT = "xlm-roberta-base"

# Where to save the trained model
OUTPUT_DIR = "models/lux_ner_xlmr"


def read_conll(path: Path) -> List[List[Tuple[str, str]]]:
    """
    Read a CoNLL file -> list of sentences.
    Each sentence is a list of (token, tag) pairs.
    """
    sentences = []
    current = []

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            # sentence boundary
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


def conll_to_hf(sentences: List[List[Tuple[str, str]]]) -> Dataset:
    """
    Convert list of sentences into a HuggingFace Dataset:
      {"tokens": [...], "ner_tags": [...]}
    """
    tokens = []
    tags = []
    for sent in sentences:
        sent_tokens, sent_tags = zip(*sent)
        tokens.append(list(sent_tokens))
        tags.append(list(sent_tags))
    return Dataset.from_dict({"tokens": tokens, "ner_tags": tags})


def build_label_list(datasets: DatasetDict):
    """
    Collect all unique tags from all splits, sort them,
    ensure 'O' is first, and add missing I-XXX tags for any B-XXX.
    """
    all_tags = set()
    for split in datasets:
        for tags in datasets[split]["ner_tags"]:
            all_tags.update(tags)

    all_tags = sorted(all_tags)
    if "O" in all_tags:
        all_tags.remove("O")
        all_tags = ["O"] + all_tags

    # Ensure for every B-XXX we also have I-XXX
    tag_set = set(all_tags)
    extra_i_tags = []
    for tag in list(tag_set):
        if tag.startswith("B-"):
            i_tag = "I-" + tag[2:]
            if i_tag not in tag_set:
                extra_i_tags.append(i_tag)

    all_tags.extend(sorted(extra_i_tags))
    return all_tags


def align_labels_with_tokens(labels, word_ids, label2id):
    """
    Align word-level labels to tokenized subwords.
    - For subwords of the same word: turn B-XXX into I-XXX
    - For special tokens: label = -100
    """
    aligned_labels = []
    previous_word_id = None
    for word_id in word_ids:
        if word_id is None:
            aligned_labels.append(-100)  # ignore padding/special tokens
        else:
            label_str = labels[word_id]
            # If same word as previous subword and label is B-XXX, convert to I-XXX
            if word_id == previous_word_id and label_str.startswith("B-"):
                label_str = "I-" + label_str[2:]
            # Safety: if something weird, fall back to 'O'
            if label_str not in label2id:
                label_str = "O"
            aligned_labels.append(label2id[label_str])
        previous_word_id = word_id
    return aligned_labels


def main():
    # === Load CoNLL data ===
    train_sents = read_conll(TRAIN_PATH)
    dev_sents = read_conll(DEV_PATH)
    test_sents = read_conll(TEST_PATH)

    print(f"Train sentences: {len(train_sents)}")
    print(f"Dev sentences  : {len(dev_sents)}")
    print(f"Test sentences : {len(test_sents)}")

    ds_train = conll_to_hf(train_sents)
    ds_dev = conll_to_hf(dev_sents)
    ds_test = conll_to_hf(test_sents)

    datasets = DatasetDict(
        train=ds_train,
        validation=ds_dev,
        test=ds_test,
    )

    # === Labels ===
    label_list = build_label_list(datasets)
    print("Labels:", label_list)
    label2id = {l: i for i, l in enumerate(label_list)}
    id2label = {i: l for l, i in label2id.items()}

    # === Tokenizer ===
    tokenizer = AutoTokenizer.from_pretrained(MODEL_CHECKPOINT, use_fast=True)

    def tokenize_and_align(examples):
        tokenized = tokenizer(
            examples["tokens"],
            truncation=True,
            is_split_into_words=True,
            max_length=128,
        )
        all_labels = examples["ner_tags"]
        new_labels = []

        for i, labels in enumerate(all_labels):
            word_ids = tokenized.word_ids(batch_index=i)
            aligned = align_labels_with_tokens(labels, word_ids, label2id)
            new_labels.append(aligned)

        tokenized["labels"] = new_labels
        return tokenized

    tokenized_datasets = datasets.map(
        tokenize_and_align,
        batched=True,
        remove_columns=["tokens", "ner_tags"],
    )

    # === Model ===
    model = AutoModelForTokenClassification.from_pretrained(
        MODEL_CHECKPOINT,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id,
    )

    # === Training config (simple / compatible) ===
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        learning_rate=5e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        num_train_epochs=5,
        weight_decay=0.01,
        logging_steps=100,
    )

    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)

    # === Very simple metric: token-level accuracy ===
    def compute_metrics(p):
        preds = np.argmax(p.predictions, axis=-1)
        labels = p.label_ids

        # mask out special tokens (-100)
        mask = labels != -100
        preds_flat = preds[mask]
        labels_flat = labels[mask]

        if labels_flat.size == 0:
            acc = 0.0
        else:
            acc = (preds_flat == labels_flat).mean().item()

        return {"accuracy": acc}

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    # === Train ===
    trainer.train()

    # === Evaluate on test set ===
    test_results = trainer.evaluate(tokenized_datasets["test"])
    print("\nTest results:", test_results)

    # Save final model
    trainer.save_model(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)


if __name__ == "__main__":
    main()
