import argparse
from pathlib import Path
from statistics import mean, median


def read_conll(path):
    """
    Reads a simple CoNLL file with format:
        TOKEN TAG
    Sentences are separated by blank lines.
    Returns: list of sentences, each a list of (token, tag).
    """
    sentences = []
    current = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
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


def write_conll(sentences, path):
    """Write sentences back to CoNLL format."""
    with open(path, "w", encoding="utf-8") as f:
        for sent in sentences:
            for token, tag in sent:
                f.write(f"{token} {tag}\n")
            f.write("\n")


def collect_stats(sentences):
    tag_counts = {}
    ent_type_counts = {}       
    entity_counts = {}        
    token_per_sentence = []

    for sent in sentences:
        token_per_sentence.append(len(sent))

        prev_tag = "O"
        prev_type = None

        for token, tag in sent:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

            if tag == "O":
                prev_tag = "O"
                prev_type = None
                continue

           
            if "-" in tag:
                prefix, etype = tag.split("-", 1)
            else:
                prefix, etype = "O", None

            if prefix in {"B", "I"} and etype:
                
                ent_type_counts[etype] = ent_type_counts.get(etype, 0) + 1

               
                if prefix == "B" or prev_tag == "O" or prev_type != etype:
                    entity_counts[etype] = entity_counts.get(etype, 0) + 1

                prev_tag = prefix
                prev_type = etype
            else:
                prev_tag = tag
                prev_type = None

    total_sents = len(sentences)
    total_tokens = sum(token_per_sentence) if token_per_sentence else 0

   
    if token_per_sentence:
        min_len = min(token_per_sentence)
        max_len = max(token_per_sentence)
        avg_len = mean(token_per_sentence)
        med_len = median(token_per_sentence)
    else:
        min_len = max_len = avg_len = med_len = 0

    stats = {
        "total_sentences": total_sents,
        "total_tokens": total_tokens,
        "min_sent_len": min_len,
        "max_sent_len": max_len,
        "avg_sent_len": avg_len,
        "median_sent_len": med_len,
        "tag_counts": tag_counts,
        "ent_type_token_counts": ent_type_counts,
        "ent_type_counts": entity_counts,
    }
    return stats


def print_stats(label, stats):
    print(f"\n=== {label} ===")
    print(f"Sentences        : {stats['total_sentences']}")
    print(f"Tokens           : {stats['total_tokens']}")
    print(
        f"Sentence length  : min={stats['min_sent_len']}, "
        f"max={stats['max_sent_len']}, "
        f"avg={stats['avg_sent_len']:.2f}, "
        f"median={stats['median_sent_len']}"
    )

    tag_counts = stats["tag_counts"]
    total_tokens = stats["total_tokens"] or 1
    print("\nTag distribution (BIO tags):")
    for tag, cnt in sorted(tag_counts.items(), key=lambda x: (-x[1], x[0])):
        pct = 100.0 * cnt / total_tokens
        print(f"  {tag:10s} : {cnt:8d}  ({pct:5.2f}%)")

    print("\nEntity-token distribution by type (collapsed B-/I-):")
    for etype, cnt in sorted(
        stats["ent_type_token_counts"].items(),
        key=lambda x: (-x[1], x[0]),
    ):
        pct = 100.0 * cnt / total_tokens
        print(f"  {etype:10s} : {cnt:8d}  ({pct:5.2f}%)")

    print("\nNumber of entities by type:")
    for etype, cnt in sorted(
        stats["ent_type_counts"].items(),
        key=lambda x: (-x[1], x[0]),
    ):
        print(f"  {etype:10s} : {cnt:8d}")


def clean_sentences(sentences, max_len=200, min_len=1):
    """
    Basic cleaning:
      - drop sentences with length < min_len
      - drop sentences with length > max_len
    More rules can be added later if needed.
    """
    cleaned = []
    for sent in sentences:
        n = len(sent)
        if n < min_len:
            continue
        if n > max_len:
            continue
        cleaned.append(sent)
    return cleaned


def main():
    parser = argparse.ArgumentParser(
        description="Clean a CoNLL NER file and print detailed BIO stats."
    )
    parser.add_argument("--input", required=True, help="Input CoNLL file.")
    parser.add_argument("--output", required=True, help="Output cleaned CoNLL file.")
    parser.add_argument(
        "--max-len",
        type=int,
        default=200,
        help="Maximum sentence length (tokens) to keep (default: 200).",
    )
    parser.add_argument(
        "--min-len",
        type=int,
        default=1,
        help="Minimum sentence length (tokens) to keep (default: 1).",
    )

    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    print(f"Reading from: {in_path}")
    sentences = read_conll(in_path)

    raw_stats = collect_stats(sentences)
    print_stats("RAW DATA", raw_stats)

    cleaned = clean_sentences(sentences, max_len=args.max_len, min_len=args.min_len)

    cleaned_stats = collect_stats(cleaned)
    print_stats("CLEANED DATA", cleaned_stats)

    write_conll(cleaned, out_path)
    print(f"\nCleaned CoNLL written to: {out_path}")


if __name__ == "__main__":
    main()
