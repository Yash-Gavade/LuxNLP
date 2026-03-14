from pathlib import Path

IN_CONLL = "data/processed/lux_leipzig_ner.clean.conll"
OUT_CONLL = "data/processed/lux_leipzig_ner.med_merged.conll"

# Mapping from old tag → new tag
TAG_MAP = {
    "B-MED": "B-MEDICINE",
    "I-MED": "I-MEDICINE",
    "B-ANAT": "B-MEDICINE",
    "I-ANAT": "I-MEDICINE",
    # everything else (PER, O, etc.) stays the same
}


def remap():
    in_path = Path(IN_CONLL)
    out_path = Path(OUT_CONLL)

    if not in_path.exists():
        raise SystemExit(f"Input CoNLL not found: {in_path}")

    num_lines = 0
    num_tags_changed = 0

    with in_path.open("r", encoding="utf-8") as f_in, \
         out_path.open("w", encoding="utf-8") as f_out:

        for line in f_in:
            num_lines += 1
            stripped = line.strip()
            if not stripped:
                f_out.write("\n")
                continue

            parts = stripped.split()
            if len(parts) < 2:
                # unexpected line format, just copy
                f_out.write(line)
                continue

            token = " ".join(parts[:-1])
            tag = parts[-1]
            new_tag = TAG_MAP.get(tag, tag)
            if new_tag != tag:
                num_tags_changed += 1

            f_out.write(f"{token} {new_tag}\n")

    print(f"Remapped file written to: {out_path}")
    print(f"Total lines       : {num_lines}")
    print(f"Tags changed      : {num_tags_changed}")


if __name__ == "__main__":
    remap()
