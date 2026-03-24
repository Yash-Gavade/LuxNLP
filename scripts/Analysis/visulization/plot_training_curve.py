import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trainer_state", required=True)
    ap.add_argument("--out_png", required=True)
    args = ap.parse_args()

    data = json.load(open(args.trainer_state, encoding="utf-8"))
    hist = data.get("log_history", [])

    steps = []
    loss = []
    for e in hist:
        if "loss" in e and "step" in e:
            steps.append(e["step"])
            loss.append(e["loss"])

    if not steps:
        print("No (step, loss) entries found in log_history.")
        return

    plt.figure()
    plt.plot(steps, loss)
    plt.title("Training Loss vs Steps")
    plt.xlabel("Step")
    plt.ylabel("Loss")
    plt.tight_layout()

    out = Path(args.out_png)
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out, dpi=200)
    plt.close()
    print("Saved:", out)

if __name__ == "__main__":
    main()
