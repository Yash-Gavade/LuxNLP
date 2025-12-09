#!/usr/bin/env python3


import argparse
from collections import Counter


def is_valid_tag(tag: str) -> bool:
    """Return True if tag is a valid BIO tag or 'O'."""
    if tag == "O":
        return True
    if tag.startswith("B-") and len(tag) > 2:
        return True
    if tag.startswith("I-") and len(tag) > 2:
        return True
    return False

def clean_conll(input_path: str, output_path: str):
    total_tokens = 0
    total_sentences = 0
    fixed_missing = 0
    fixed_empty = 0
    fixed_dot = 0
    fixed_invalid = 0
    label_counter_before = Counter()
    label_counter_after = Counter()

    with open(input_path, "r", encoding="utf-8") as fin, \
         open(output_path, "w", encoding="utf-8") as fout:

        for line in fin:
            stripped = line.rstrip("\n")

            # Sentence boundary
            if stripped.strip() == "":
                fout.write("\n")
                total_sentences += 1
                continue

            parts = stripped.split()
            token = parts[0]

            # If no tag column → assign O
            if len(parts) == 1:
                old_tag = ""
                new_tag = "O"
                fixed_missing += 1

            else:
                old_tag = parts[1]
                label_counter_before[old_tag] += 1

                # Empty or whitespace tag
                if old_tag.strip() == "":
                    new_tag = "O"
                    fixed_empty += 1

                # Tag is '.' or '-' → invalid
                elif old_tag in {".", "-"}:
                    new_tag = "O"
                    fixed_dot += 1

                # Invalid tag (not BIO or O)
                elif not is_valid_tag(old_tag):
                    new_tag = "O"
                    fixed_invalid += 1

                # Valid → keep
                else:
                    new_tag = old_tag

            label_counter_after[new_tag] += 1
            total_tokens += 1

            fout.write(f"{token}\t{new_tag}\n")

    # Print stats
    print("========== CLEANING STATS ==========")
    print(f"Input file : {input_path}")
    print(f"Output file: {output_path}")
    print(f"Total sentences:   {total_sentences:,}")
    print(f"Total tokens:      {total_tokens:,}")
    print()
    print(f"Fixed missing tags : {fixed_missing}")
    print(f"Fixed empty tags   : {fixed_empty}")
    print(f"Fixed '.'/'-' tags : {fixed_dot}")
    print(f"Fixed invalid tags : {fixed_invalid}")
    print()
    print("Label distribution BEFORE cleaning:")
    for lab, cnt in label_counter_before.most_common(20):
        print(f"  {lab:10} {cnt}")
    print()
    print("Label distribution AFTER cleaning:")
    for lab, cnt in label_counter_after.most_common(20):
        print(f"  {lab:10} {cnt}")
    print("=====================================\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    clean_conll(args.input, args.output)

if __name__ == "__main__":
    main()
