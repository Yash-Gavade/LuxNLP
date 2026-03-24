import pandas as pd
import re
import numpy as np
from typing import List, Tuple


def change_column_names(df):
    """
    Convert survey questions into proper column names

    """

    new_columns = []

    # P-Columns (erste 5)
    for i in range(5):
        new_columns.append(f"P{i + 1}")

    # E-Columns (next 5)
    for i in range(5):
        new_columns.append(f"E{i + 1}")

    # M-Columns (Rest)
    remaining = df.shape[1] - 10
    for i in range(remaining):
        new_columns.append(f"M{i + 1}")

    df.columns = new_columns

    return df


# Tokenizer: Wörter (inkl. Apostroph), Zahlen, Satzzeichen
TOKEN_RE = re.compile(
    r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:'[A-Za-zÀ-ÖØ-öø-ÿ]+)?|\d+|[^\w\s]", re.UNICODE
)


def tokenize(text: str) -> List[str]:
    return TOKEN_RE.findall(text)


def extract_spans_with_tags(
    text: str, NER_cat: str
) -> Tuple[str, List[Tuple[str, int, int]]]:
    """
    Extract <P>...</P>, <E>...</R> and <M>...</M> Spans and returns:
    - clean_text: Text without Tags
    - spans: List (span_text, start_char, end_char) refering to clean_text
    """
    spans = []
    out = []
    i = 0
    clean_pos = 0

    while i < len(text):
        # fin next <P>, <E> or <M> tag
        start = text.find(f"<{NER_cat[0]}>", i)

        if start == -1:
            # append rest
            out.append(text[i:])
            break

        # Append text befor <Tag>
        before = text[i:start]
        out.append(before)
        clean_pos += len(before)

        # find </P>, </E> or </M>
        endtag = text.find(f"</{NER_cat[0]}>", start)
        if endtag == -1:
            out.append(text[start:])
            break

        # Content within <P>...</P>
        inner = text[start + 3 : endtag]
        inner_clean = inner

        out.append(inner_clean)

        span_start = clean_pos
        clean_pos += len(inner_clean)
        span_end = clean_pos

        spans.append((inner_clean, span_start, span_end))

        i = endtag + 4  # after </P>

    clean_text = "".join(out)
    return clean_text, spans


def token_char_offsets(text: str, tokens: List[str]) -> List[Tuple[int, int]]:
    """
    Finds the (start, end) offset of each token in the text (left-aligned, in sequential order).
    """

    offsets = []
    cursor = 0

    for tok in tokens:
        # skip whitespace
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        # find token ab cursor
        idx = text.find(tok, cursor)
        if idx == -1:
            # Fallback: if something fails, set None-Offsets
            offsets.append((-1, -1))
            continue
        start = idx
        end = idx + len(tok)
        offsets.append((start, end))
        cursor = end

    return offsets


def overlaps(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    return max(a_start, b_start) < min(a_end, b_end)


def conll_from_sentences(
    sentences: List[str], out_path: str = None, NER_CAT=None
) -> str:
    """
    Convert list of sentences into CoNLL.
    MarksTokens within <P>...</P> asPRODUCT (BIO). (same for Event and MEDICINE)
    """

    conll_lines = []

    for raw in sentences:
        clean_text, spans = extract_spans_with_tags(raw, NER_CAT)
        tokens = tokenize(clean_text)
        offsets = token_char_offsets(clean_text, tokens)

        # BIO tags initialisieren
        tags = ["O"] * len(tokens)

        # Für jeden <P> span: Tokens markieren, die im Char-Span überlappen
        for span_text, s_start, s_end in spans:
            token_idxs = [
                i
                for i, (t_start, t_end) in enumerate(offsets)
                if t_start != -1 and overlaps(t_start, t_end, s_start, s_end)
            ]
            if not token_idxs:
                continue
            tags[token_idxs[0]] = "B-" + NER_CAT
            for j in token_idxs[1:]:
                tags[j] = "I-" + NER_CAT

        # CoNLL Satzblock
        for tok, tag in zip(tokens, tags):
            conll_lines.append(f"{tok}\t{tag}")
        conll_lines.append("")  # Satztrenner

    conll_text = "\n".join(conll_lines)

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(conll_text)

    return conll_text


def main():
    # Load data
    survey_data = pd.read_csv(
        "Luxemburgesch Texter_ Produkter & Eventer beschreiwen.csv"
    )

    # Only grab NER-answers
    df = survey_data.iloc[:, 4:]

    # Change columns names
    df = change_column_names(df)

    print(df.shape)

    sentences = []

    for cat in ["PRODUCT", "EVENT", "MEDICINE"]:
        sentences = []

        for col in [f"{cat[0]}{i}" for i in range(1, 6)]:
            for val in df[col]:
                if isinstance(val, str) and val.strip():
                    sentences.append(val.strip())

        conll_from_sentences(
            sentences=sentences,
            out_path=f"survey_{cat.lower()}_from_tags.conll",
            NER_CAT=cat,
        )

    for path in ["product", "event", "medicine"]:
        with open(f"survey_{path}_from_tags.conll", "r", encoding="utf-8") as f:
            print(f.read())


if __name__ == "__main__":
    main()
