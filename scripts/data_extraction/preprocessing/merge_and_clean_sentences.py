import re
from pathlib import Path

# =========================================================
# PATHS
# =========================================================
BASE = Path("LuxNLP-main")

INPUT_FILES = [
    BASE / "data" / "raw" / "ltz_newscrawl_2016_300K-sentences.txt",
    BASE / "data" / "raw" / "ltz_wikipedia_2021_100K-sentences.txt",
    BASE / "data" / "raw" / "ltz-lu_web_2020_1M-sentences.txt",
]

OUTPUT_MERGED = BASE / "data" / "raw" / "All_Extracted_Sentences_merged.txt"
OUTPUT_CLEANED = BASE / "data" / "cleaned" / "All_Extracted_Sentences_cleaned.txt"

# =========================================================
# CLEANING RULES
# =========================================================
BAD_PATTERNS = [
    r"<br\s*/?>",
    r"&nbsp;",
    r"&amp;",
    r"&quot;",
    r"&lt;",
    r"&gt;",
    r"https?://\S+",
    r"www\.\S+",
    r"\bmailto:\S+",
]

REJECT_PATTERNS = [
    r"^[^A-Za-zÀ-ÿ0-9]+$",   # only symbols
    r"^\d+$",               # only digits
]

def normalize_quotes(text: str) -> str:
    replacements = {
        "“": '"', "”": '"',
        "„": '"', "«": '"', "»": '"',
        "‘": "'", "’": "'",
        "…": "...",
        "\u00a0": " ",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def clean_line(line: str) -> str:
    line = line.strip()
    if not line:
        return ""

    line = normalize_quotes(line)

    # remove line numbers at start
    line = re.sub(r"^\s*\d+\s+", "", line)

    # remove bullets
    line = re.sub(r"^[•*·▪►]+\s*", "", line)

    # remove bad patterns
    for pat in BAD_PATTERNS:
        line = re.sub(pat, " ", line, flags=re.IGNORECASE)

    # remove repeated spaces
    line = re.sub(r"\s+", " ", line)

    # fix spaces before punctuation
    line = re.sub(r"\s+([,.;:!?])", r"\1", line)

    # strip unwanted edge chars
    line = line.strip(" \t-–—|<>\"'`")

    return line.strip()

def is_meaningful_sentence(line: str) -> bool:
    if not line:
        return False

    for pat in REJECT_PATTERNS:
        if re.fullmatch(pat, line):
            return False

    # must contain letters
    if not re.search(r"[A-Za-zÀ-ÿ]", line):
        return False

    # minimum length
    if len(line) < 15:
        return False

    # minimum token count
    if len(line.split()) < 3:
        return False

    # reject too many weird symbols
    weird = len(re.findall(r"[^A-Za-zÀ-ÿ0-9\s,.;:!?'\-()/%]", line))
    if weird > max(5, int(len(line) * 0.15)):
        return False

    return True

def deduplicate_keep_order(lines):
    seen = set()
    result = []
    for line in lines:
        key = line.casefold()
        if key not in seen:
            seen.add(key)
            result.append(line)
    return result

# =========================================================
# MAIN
# =========================================================
def main():
    merged_lines = []

    for file_path in INPUT_FILES:
        if not file_path.exists():
            print(f"[WARN] Missing file: {file_path}")
            continue

        print(f"Reading: {file_path}")
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.rstrip("\n")
                if line.strip():
                    merged_lines.append(line)

    # save merged raw
    OUTPUT_MERGED.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_MERGED, "w", encoding="utf-8") as f:
        for line in merged_lines:
            f.write(line + "\n")

    cleaned_lines = []
    for line in merged_lines:
        cleaned = clean_line(line)
        if is_meaningful_sentence(cleaned):
            cleaned_lines.append(cleaned)

    cleaned_lines = deduplicate_keep_order(cleaned_lines)

    OUTPUT_CLEANED.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_CLEANED, "w", encoding="utf-8") as f:
        for line in cleaned_lines:
            f.write(line + "\n")

    print("\nDone.")
    print(f"Total merged lines: {len(merged_lines)}")
    print(f"Total cleaned meaningful lines: {len(cleaned_lines)}")
    print(f"Saved merged file: {OUTPUT_MERGED}")
    print(f"Saved cleaned file: {OUTPUT_CLEANED}")

if __name__ == "__main__":
    main()