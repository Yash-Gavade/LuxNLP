# scripts/new_export_eval_table.py
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

LINE = re.compile(r"^(DATE|EVENT|LOC|MED|MISC|ORG|PER|MICRO)\s+P=\s*([0-9.]+)\s+R=\s*([0-9.]+)\s+F1=\s*([0-9.]+)\s+TP=\s*([0-9]+)\s+FP=\s*([0-9]+)\s+FN=\s*([0-9]+)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval_txt", required=True)
    ap.add_argument("--out_csv", required=True)
    ap.add_argument("--title", required=True)
    args = ap.parse_args()

    out_path = Path(args.out_csv)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    with open(args.eval_txt, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = LINE.match(line)
            if m:
                rows.append(m.groups())

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["TITLE", args.title])
        w.writerow(["LABEL", "P", "R", "F1", "TP", "FP", "FN"])
        for label, p, r, f1, tp, fp, fn in rows:
            w.writerow([label, p, r, f1, tp, fp, fn])

    print("Wrote:", out_path)

if __name__ == "__main__":
    main()
