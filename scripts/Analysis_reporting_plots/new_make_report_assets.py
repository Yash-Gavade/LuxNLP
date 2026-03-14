# scripts/new_make_report_assets.py
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def run(cmd):
    print("RUN:", " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--split_dir", required=True, help="e.g. data/processed/.../split_70_15_15")
    ap.add_argument("--out_dir", required=True, help="e.g. outputs/report_assets")
    args = ap.parse_args()

    split = Path(args.split_dir)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    for name in ["train", "dev", "test"]:
        conll = split / f"{name}.conll"
        title = name.upper()

        run(["python", "scripts/new_export_conll_stats_to_csv.py",
             "--conll", str(conll),
             "--title", title,
             "--out_csv", str(out / f"{title}_stats.csv")])

        run(["python", "scripts/new_plot_conll_distributions.py",
             "--conll", str(conll),
             "--title", title,
             "--out_dir", str(out)])

    print("\nDONE ✅ Assets in:", out)

if __name__ == "__main__":
    main()
