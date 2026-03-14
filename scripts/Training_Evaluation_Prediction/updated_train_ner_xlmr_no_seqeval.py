# scripts/updated_train_ner_xlmr_no_seqeval.py
import argparse
from pathlib import Path

import numpy as np
from datasets import Dataset, DatasetDict
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    DataCollatorForTokenClassification,
    TrainingArguments,
    Trainer,
)


def read_conll(path: Path):
    sentences, tags = [], []
    cur_tokens, cur_tags = [], []
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                if cur_tokens:
                    sentences.append(cur_tokens)
                    tags.append(cur_tags)
                    cur_tokens, cur_tags = [], []
                continue
            parts = line.split()
            token = " ".join(parts[:-1])
            tag = parts[-1]
            cur_tokens.append(token)
            cur_tags.append(tag)

    if cur_tokens:
        sentences.append(cur_tokens)
        tags.append(cur_tags)

    return sentences, tags


def build_label_maps(all_tags):
    uniq = sorted(set(t for seq in all_tags for t in seq))
    label2id = {lab: i for i, lab in enumerate(uniq)}
    id2label = {i: lab for lab, i in label2id.items()}
    return label2id, id2label


def align_labels(tokenizer, tokens, labels, label2id, max_length):
    enc = tokenizer(
        tokens,
        is_split_into_words=True,
        truncation=True,
        max_length=max_length,
    )
    word_ids = enc.word_ids()
    aligned = []
    prev = None

    for wid in word_ids:
        if wid is None:
            aligned.append(-100)
        elif wid != prev:
            aligned.append(label2id[labels[wid]])
        else:
            aligned.append(-100)
        prev = wid

    enc["labels"] = aligned
    return enc


def compute_token_metrics(preds, labels, id2label):
    """
    Simple metrics without seqeval:
    - token_acc: accuracy over all labeled tokens
    - token_acc_non_o: accuracy over non-O tokens only (more meaningful for NER)
    """
    preds = np.argmax(preds, axis=-1)

    correct = 0
    total = 0
    correct_non_o = 0
    total_non_o = 0

    for pred_seq, lab_seq in zip(preds, labels):
        for p_i, l_i in zip(pred_seq, lab_seq):
            if l_i == -100:
                continue
            total += 1
            if p_i == l_i:
                correct += 1

            gold = id2label[int(l_i)]
            if gold != "O":
                total_non_o += 1
                if p_i == l_i:
                    correct_non_o += 1

    token_acc = correct / total if total else 0.0
    token_acc_non_o = correct_non_o / total_non_o if total_non_o else 0.0
    return {"token_acc": token_acc, "token_acc_non_o": token_acc_non_o}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data_dir", required=True, help="Folder with train.conll/dev.conll/test.conll")
    ap.add_argument("--model_name", default="xlm-roberta-base")
    ap.add_argument("--out_dir", default="models/xlmr_ner_v3")
    ap.add_argument("--epochs", type=int, default=3)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--max_length", type=int, default=256)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load CoNLL splits
    train_t, train_l = read_conll(data_dir / "train.conll")
    dev_t, dev_l = read_conll(data_dir / "dev.conll")
    test_t, test_l = read_conll(data_dir / "test.conll")

    # Label mappings
    label2id, id2label = build_label_maps(train_l + dev_l + test_l)

    # Model + tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForTokenClassification.from_pretrained(
        args.model_name,
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
    )

    # Build HF datasets
    def make_ds(tokens, labels):
        ds = Dataset.from_dict({"tokens": tokens, "labels": labels})
        return ds.map(
            lambda x: align_labels(tokenizer, x["tokens"], x["labels"], label2id, args.max_length),
            batched=False,
            remove_columns=["tokens", "labels"],
        )

    dsd = DatasetDict({
        "train": make_ds(train_t, train_l),
        "validation": make_ds(dev_t, dev_l),
        "test": make_ds(test_t, test_l),
    })

    data_collator = DataCollatorForTokenClassification(tokenizer)

    # IMPORTANT: Older transformers does NOT support evaluation_strategy/save_strategy/etc.
    training_args = TrainingArguments(
        output_dir=str(out_dir),
        learning_rate=args.lr,
        per_device_train_batch_size=args.batch,
        per_device_eval_batch_size=args.batch,
        num_train_epochs=args.epochs,
        logging_steps=200,
        seed=args.seed,
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dsd["train"],
        eval_dataset=dsd["validation"],  # evaluation will run only if your transformers supports it
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=lambda p: compute_token_metrics(p.predictions, p.label_ids, id2label)
        if hasattr(p, "predictions") else {},
    )

    # Train
    trainer.train()
    print("Training finished.")

    # Evaluate on test (works even if older transformers)
    print("\nTest set evaluation:")
    try:
        test_out = trainer.predict(dsd["test"])
        metrics = compute_token_metrics(test_out.predictions, test_out.label_ids, id2label)
        print(metrics)
    except Exception as e:
        print("Could not run test predict metrics:", e)

    # Save model
    trainer.save_model(str(out_dir))
    tokenizer.save_pretrained(str(out_dir))
    print("\nSaved model to:", out_dir)


if __name__ == "__main__":
    main()
