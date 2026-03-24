import re
from pathlib import Path

INPUT_FILE = Path(r"D:\DOWNLOADS\BRAVE\LuxNLP-main\LuxNLP-main\data\processed\All_Extracted_Sentences.txt")
OUTPUT_CLEAN = Path(r"D:\DOWNLOADS\BRAVE\LuxNLP-main\LuxNLP-main\data\processed\All_Extracted_Sentences_cleaned.txt")
OUTPUT_FILTERED = Path(r"D:\DOWNLOADS\BRAVE\LuxNLP-main\LuxNLP-main\data\processed\All_Extracted_Sentences_meaningful.txt")

# Common noisy patterns seen in your file
BAD_PATTERNS = [
    r"<br\s*/?>",                  # html breaks
    r"&nbsp;",
    r"Forgot your password\??",
    r"Editus\.lu",
    r"industr[iey]\.lu",
    r"Aachen\.lu.*?>",             # site/forum navigation fragments
]

# Very noisy / fragment-like lines to reject
REJECT_PATTERNS = [
    r"^[^A-Za-zÀ-ÿ0-9]*$",         # only symbols
    r"^[\"'“”‘’‚‛`\-–—.,;:!?()\[\]{}<>€£%/\\+*=#@&|~^_ ]+$",
    r"^\d+$",                      # only number
    r"^\d+\s*$",                   # only number with spaces
    r"^[A-Z0-9 .,:;!?\-_/\\()]+$", # mostly code-like / all caps junk
]

def normalize_unicode_quotes(text: str) -> str:
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

    # remove leading line numbers like: 1 sentence...
    line = re.sub(r"^\s*\d+\s+", "", line)

    # remove leading bullets
    line = re.sub(r"^[•*!;·]+\s*", "", line)

    line = normalize_unicode_quotes(line)

    # remove html / website junk
    for pat in BAD_PATTERNS:
        line = re.sub(pat, " ", line, flags=re.IGNORECASE)

    # remove repeated punctuation noise at beginning
    line = re.sub(r"^[\"'`]+", "", line)
    line = re.sub(r"^[)\]}>\-–—.,;:!?]+\s*", "", line)

    # normalize spaces around punctuation
    line = re.sub(r"\s+", " ", line)
    line = re.sub(r"\s+([,.;:!?])", r"\1", line)
    line = re.sub(r"([(\[{\"]) +", r"\1", line)
    line = re.sub(r" +([)\]}\"])", r"\1", line)

    # remove duplicated quotes around whole line
    line = re.sub(r'^[\'"](.+)[\'"]$', r"\1", line)

    # strip again
    line = line.strip(" \t-–—\"'")

    return line.strip()

def is_meaningful_sentence(line: str) -> bool:
    if not line:
        return False

    # reject obvious junk
    for pat in REJECT_PATTERNS:
        if re.fullmatch(pat, line):
            return False

    # too short
    if len(line) < 20:
        return False

    # must contain letters
    if not re.search(r"[A-Za-zÀ-ÿ]", line):
        return False

    # reject very symbol-heavy lines
    symbol_count = len(re.findall(r"[^A-Za-zÀ-ÿ0-9\s,.;:!?'\-()]", line))
    if symbol_count > max(6, len(line) * 0.20):
        return False

    # should have at least 4 tokens
    tokens = line.split()
    if len(tokens) < 4:
        return False

    # reject navigation-like / metadata-like lines
    nav_keywords = [
        "username", "password", "newsletter", "menu", "postkaart",
        "formulaire", "posting", "site", "forum"
    ]
    lowered = line.lower()
    if sum(kw in lowered for kw in nav_keywords) >= 2:
        return False

    # reject many weird fragments like unmatched brackets ratio
    if abs(line.count("(") - line.count(")")) > 1:
        return False
    if abs(line.count('"') % 2) == 1 and len(line) < 35:
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

def main():
    raw_lines = INPUT_FILE.read_text(encoding="utf-8", errors="ignore").splitlines()

    cleaned_all = []
    meaningful_only = []

    for raw in raw_lines:
        line = clean_line(raw)
        if line:
            cleaned_all.append(line)
            if is_meaningful_sentence(line):
                meaningful_only.append(line)

    cleaned_all = deduplicate_keep_order(cleaned_all)
    meaningful_only = deduplicate_keep_order(meaningful_only)

    OUTPUT_CLEAN.write_text("\n".join(cleaned_all), encoding="utf-8")
    OUTPUT_FILTERED.write_text("\n".join(meaningful_only), encoding="utf-8")

    print(f"Total raw lines: {len(raw_lines)}")
    print(f"Cleaned lines: {len(cleaned_all)}")
    print(f"Meaningful lines: {len(meaningful_only)}")
    print(f"Saved cleaned file: {OUTPUT_CLEAN}")
    print(f"Saved meaningful file: {OUTPUT_FILTERED}")

if __name__ == "__main__":
    main()