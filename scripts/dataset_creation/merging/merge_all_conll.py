from pathlib import Path

IN_FILES = [
    "data/processed/lux_leipzig_ner.med_merged.conll",
    "data/processed/lod_lu_ner.clean.conll",
    "data/processed/wikidata_lb_ner.clean.conll",
]

OUT_CONLL = "data/processed/lux_full_ner.conll"


def main():
    out_path = Path(OUT_CONLL)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_lines = 0

    with out_path.open("w", encoding="utf-8") as f_out:
        for path_str in IN_FILES:
            path = Path(path_str)
            if not path.exists():
                raise SystemExit(f"Input file not found: {path}")

            print(f"Merging: {path}")
            with path.open("r", encoding="utf-8") as f_in:
                for line in f_in:
                    f_out.write(line)
                    total_lines += 1

            # Add a blank line between datasets
            f_out.write("\n")
            total_lines += 1

    print(f"\nMerged CoNLL written to: {out_path}")
    print(f"Total lines in merged file: {total_lines}")


if __name__ == "__main__":
    main()
