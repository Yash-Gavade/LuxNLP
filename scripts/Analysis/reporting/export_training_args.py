import argparse
import csv
import json
from pathlib import Path
import torch

def get(obj, name, default="N/A"):
    return getattr(obj, name, default)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model_dir", required=True)
    ap.add_argument("--out_csv", required=True)
    args = ap.parse_args()

    model_dir = Path(args.model_dir)
    training_args_path = model_dir / "training_args.bin"
    trainer_state_path = model_dir / "trainer_state.json"

    if not training_args_path.exists():
        raise FileNotFoundError(f"Missing {training_args_path}")


    training_args = torch.load(training_args_path, weights_only=False)

    trainer_state = {}
    if trainer_state_path.exists():
        with open(trainer_state_path, encoding="utf-8") as f:
            trainer_state = json.load(f)


    rows = [
        ("Task", "Named Entity Recognition (NER)"),
        ("Language", "Luxembourgish"),
        ("Model family", "XLM-RoBERTa (token classification)"),
        ("Output directory", str(get(training_args, "output_dir"))),

        ("Num train epochs", get(training_args, "num_train_epochs")),
        ("Train batch size", get(training_args, "per_device_train_batch_size")),
        ("Eval batch size", get(training_args, "per_device_eval_batch_size")),
        ("Learning rate", get(training_args, "learning_rate")),
        ("Weight decay", get(training_args, "weight_decay")),
        ("Warmup steps", get(training_args, "warmup_steps")),
        ("LR scheduler type", get(training_args, "lr_scheduler_type")),
        ("Gradient clipping (max_grad_norm)", get(training_args, "max_grad_norm")),
        ("Seed", get(training_args, "seed")),
        ("FP16", get(training_args, "fp16")),
        ("Logging steps", get(training_args, "logging_steps")),
        ("Save strategy", get(training_args, "save_strategy")),
        ("Save steps", get(training_args, "save_steps")),
        ("Evaluation strategy", get(training_args, "evaluation_strategy")),
        ("Eval steps", get(training_args, "eval_steps")),
        ("Load best model at end", get(training_args, "load_best_model_at_end")),
        ("Metric for best model", get(training_args, "metric_for_best_model")),
        ("Greater is better", get(training_args, "greater_is_better")),
    ]

    if "best_model_checkpoint" in trainer_state:
        rows.append(("Best checkpoint (trainer_state)", trainer_state["best_model_checkpoint"]))
    if "best_metric" in trainer_state:
        rows.append(("Best metric (trainer_state)", trainer_state["best_metric"]))
    if "log_history" in trainer_state and trainer_state["log_history"]:

        last = trainer_state["log_history"][-1]
        if "train_loss" in last:
            rows.append(("Final train_loss (trainer_state)", last["train_loss"]))

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Hyperparameter", "Value"])
        for k, v in rows:
            writer.writerow([k, v])

    print("Training hyperparameters exported to:", out_csv)

if __name__ == "__main__":
    main()
