import argparse
from pathlib import Path


def merge_conll_files(input_paths, output_path):
    sent_count = 0
    token_count = 0

    with open(output_path, "w", encoding="utf-8") as f_out:
        for i, in_path in enumerate(input_paths):
            in_path = Path(in_path)
            print(f"Merging: {in_path}")

            with in_path.open("r", encoding="utf-8") as f_in:
                prev_blank = False
                for line in f_in:
                    line = line.rstrip("\n")

                    if line.strip() == "":
                        # sentence boundary
                        sent_count += 1
                        prev_blank = True
                        f_out.write("\n")
                        continue

                    # normal token line: e.g. "Token TAG"
                    if line.strip():
                        token_count += 1
                        prev_blank = False
                        f_out.write(line + "\n")

                # ensure one blank line between files
                if not prev_blank:
                    f_out.write("\n")

    print("=== MERGE DONE ===")
    print(f"Sentences (approx): {sent_count}")
    print(f"Tokens            : {token_count}")
    print(f"Output            : {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple Leipzig CoNLL NER files into one."
    )
    parser.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="Input CoNLL files (space-separated).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output merged CoNLL file.",
    )

    args = parser.parse_args()
    merge_conll_files(args.inputs, args.output)


if __name__ == "__main__":
    main()
