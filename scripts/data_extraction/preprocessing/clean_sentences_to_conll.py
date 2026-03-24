import csv
import json
import re
from pathlib import Path
from collections import defaultdict

# =========================================================
# BASE PATH
# =========================================================

BASE = Path("LuxNLP")


INPUT_SENTENCES = BASE / "data" / "cleaned" / "All_Extracted_Sentences_cleaned.txt"

# Gazetteers
LOD_JSON = BASE / "data" / "cleaned" / "Lod.lu_en_lexicon.json"
LOD_TRANSLATIONS_JSON = BASE / "data" / "cleaned" / "Lod.lu_entries_with_domains_and_translations.json"
WIKIDATA_ALL_CSV = BASE / "data" / "cleaned" / "wikidata_lb_all_ner.csv"
WIKIDATA_DESC_CSV = BASE / "data" / "cleaned" / "wikidata_lb_with_desc_ner.csv"

OUTPUT_CONLL = BASE / "data" / "processed" / "lu_Lux_Final_gazetteer_clean.conll"

ALLOWED_TAGS = {"PER", "LOC", "MED", "DATE", "EVENT", "PRODUCT", "ORG"}

# =========================================================
# TOKENIZATION
# =========================================================

TOKEN_PATTERN = re.compile(
    r"\d{1,2}/\d{1,2}/\d{4}"                                   # 02/10/2014
    r"|\d{1,2}-\d{1,2}-\d{4}"                                  # 02-10-2014
    r"|\d{1,2}\.\s+[A-Za-zÀ-ÿ]+(?:\s+\d{4})?"                  # 19. Mee 1993
    r"|\d{4}"                                                  # 2014
    r"|[A-Za-zÀ-ÿ0-9]+(?:[-'’][A-Za-zÀ-ÿ0-9]+)*"               # words
    r"|[.,!?;:()%/\"'„“”‘’\-]"                                 # punctuation
)

MONTHS_LB = {
    "januar", "februar", "mäerz", "abrëll", "mee", "juni",
    "juli", "august", "september", "oktober", "november", "dezember"
}

def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())

def normalize_match(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"').replace("„", '"')
    text = re.sub(r"\s+", " ", text)
    return text

def tokenize(text: str):
    return TOKEN_PATTERN.findall(text)

# =========================================================
# LOAD GAZETTEERS
# =========================================================

def add_phrase(gazetteer, phrase, tag):
    if not phrase or not isinstance(phrase, str):
        return

    phrase = normalize_space(phrase)
    if not phrase:
        return

    if tag not in ALLOWED_TAGS:
        return

    toks = tokenize(phrase)
    if not toks:
        return

    norm_toks = tuple(normalize_match(t) for t in toks)
    gazetteer[len(norm_toks)].append((norm_toks, tag, phrase))

def load_wikidata_csv(path, gazetteer):
    if not path.exists():
        print(f"[WARN] Missing: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row.get("ner_tag", "").strip().upper()
            if tag not in ALLOWED_TAGS:
                continue

            label = row.get("label_lb", "").strip()
            desc = row.get("description_lb", "").strip()

            add_phrase(gazetteer, label, tag)

            if desc and 1 <= len(desc.split()) <= 5:
                add_phrase(gazetteer, desc, tag)

def load_json_entries(path, gazetteer):
    if not path.exists():
        print(f"[WARN] Missing: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        items = data.values()
    else:
        items = data

    for item in items:
        if not isinstance(item, dict):
            continue

        possible_terms = []
        possible_tags = []

        for k in ["label", "label_lb", "term", "entity", "name", "surface_form", "lb", "entry"]:
            if k in item and item[k]:
                val = item[k]
                if isinstance(val, list):
                    possible_terms.extend([x for x in val if isinstance(x, str)])
                elif isinstance(val, str):
                    possible_terms.append(val)

        for k in ["translation", "translations", "alias", "aliases", "en"]:
            if k in item and item[k]:
                val = item[k]
                if isinstance(val, list):
                    possible_terms.extend([x for x in val if isinstance(x, str)])
                elif isinstance(val, str):
                    possible_terms.append(val)

        for k in ["ner_tag", "tag", "entity_type", "type", "category"]:
            if k in item and item[k]:
                val = item[k]
                if isinstance(val, list):
                    possible_tags.extend([str(x).upper() for x in val])
                else:
                    possible_tags.append(str(val).upper())

        tag = None
        for t in possible_tags:
            if t in ALLOWED_TAGS:
                tag = t
                break

        if not tag:
            continue

        for term in possible_terms:
            add_phrase(gazetteer, term, tag)

def dedupe_gazetteer(gazetteer):
    for span_len in list(gazetteer.keys()):
        seen = set()
        cleaned = []
        for tokens, tag, phrase in gazetteer[span_len]:
            key = (tokens, tag)
            if key not in seen:
                seen.add(key)
                cleaned.append((tokens, tag, phrase))
        gazetteer[span_len] = cleaned

# =========================================================
# CLEANING / FILTERING
# =========================================================

def is_good_sentence(sent: str) -> bool:
    sent = sent.strip()
    if len(sent) < 8:
        return False
    if len(sent.split()) < 2:
        return False
    if not re.search(r"[A-Za-zÀ-ÿ]", sent):
        return False

    weird = len(re.findall(r"[^A-Za-zÀ-ÿ0-9\s,.;:!?()/%'\-\"„“”‘’]", sent))
    if weird > max(6, int(len(sent) * 0.20)):
        return False

    return True

# =========================================================
# MATCHING
# =========================================================

def apply_gazetteer(tokens, gazetteer):
    labels = ["O"] * len(tokens)
    norm_tokens = [normalize_match(t) for t in tokens]
    max_span = max(gazetteer.keys(), default=1)

    for span_len in range(max_span, 0, -1):
        if span_len not in gazetteer:
            continue

        phrase_map = defaultdict(list)
        for norm_phrase, tag, phrase in gazetteer[span_len]:
            phrase_map[norm_phrase].append((tag, phrase))

        for i in range(len(tokens) - span_len + 1):
            if any(labels[j] != "O" for j in range(i, i + span_len)):
                continue

            span = tuple(norm_tokens[i:i + span_len])
            if span not in phrase_map:
                continue

            tag = phrase_map[span][0][0]
            labels[i] = f"B-{tag}"
            for j in range(i + 1, i + span_len):
                labels[j] = f"I-{tag}"

    return labels

def apply_date_rules(tokens, labels):
    norm = [normalize_match(t) for t in tokens]
    i = 0

    while i < len(tokens):
        # -------------------------------------------------
        # FORMAT 1: 19 . Mee 1993
        # Tokenized as: ["19", ".", "Mee", "1993"]
        # -------------------------------------------------
        if (
            i + 3 < len(tokens)
            and re.fullmatch(r"\d{1,2}", norm[i])
            and norm[i + 1] == "."
            and norm[i + 2] in MONTHS_LB
            and re.fullmatch(r"\d{4}", norm[i + 3])
        ):
            if all(labels[k] == "O" for k in range(i, i + 4)):
                labels[i] = "B-DATE"
                labels[i + 1] = "I-DATE"
                labels[i + 2] = "I-DATE"
                labels[i + 3] = "I-DATE"
            i += 4
            continue

        # -------------------------------------------------
        # FORMAT 2: 19. Mee 1993
        # Tokenized as one token by regex
        # -------------------------------------------------
        
        if re.fullmatch(r"\d{1,2}\.\s+[A-Za-zÀ-ÿ]+\s+\d{4}", tokens[i], flags=re.IGNORECASE):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # -------------------------------------------------
        # FORMAT 3: 02/10/2014
        # -------------------------------------------------
        
        if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", tokens[i]):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # -------------------------------------------------
        # FORMAT 4: 02-10-2014
        # -------------------------------------------------
        if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", tokens[i]):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # -------------------------------------------------
        # FORMAT 5: year only
        # -------------------------------------------------
        if re.fullmatch(r"(1[0-9]{3}|20[0-9]{2})", norm[i]) and labels[i] == "O":
            labels[i] = "B-DATE"

        i += 1

    return labels

# =========================================================
# WRITE CONLL
# =========================================================
def write_conll(sentences, gazetteer, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    sent_count = 0
    tok_count = 0
    ent_count = 0
    sent_with_entity = 0

    with open(out_path, "w", encoding="utf-8") as out:
        for sent in sentences:
            sent = normalize_space(sent)
            if not is_good_sentence(sent):
                continue

            tokens = tokenize(sent)
            if not tokens:
                continue

            labels = apply_gazetteer(tokens, gazetteer)
            labels = apply_date_rules(tokens, labels)

            has_entity = any(lab != "O" for lab in labels)
            if has_entity:
                sent_with_entity += 1

            for tok, lab in zip(tokens, labels):
                out.write(f"{tok}\t{lab}\n")
                tok_count += 1
                if lab.startswith("B-"):
                    ent_count += 1
            out.write("\n")
            sent_count += 1

    print(f"Saved: {out_path}")
    print(f"Sentences: {sent_count}")
    print(f"Sentences with entity: {sent_with_entity}")
    print(f"Tokens: {tok_count}")
    print(f"Entities: {ent_count}")

# =========================================================
# MAIN
# =========================================================
def main():
    if not INPUT_SENTENCES.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_SENTENCES}")

    gazetteer = defaultdict(list)

    load_json_entries(LOD_JSON, gazetteer)
    load_json_entries(LOD_TRANSLATIONS_JSON, gazetteer)
    load_wikidata_csv(WIKIDATA_ALL_CSV, gazetteer)
    load_wikidata_csv(WIKIDATA_DESC_CSV, gazetteer)
    dedupe_gazetteer(gazetteer)

    total_entries = sum(len(v) for v in gazetteer.values())
    print(f"Gazetteer entries: {total_entries}")

    with open(INPUT_SENTENCES, "r", encoding="utf-8", errors="ignore") as f:
        sentences = [line.strip() for line in f if line.strip()]

    write_conll(sentences, gazetteer, OUTPUT_CONLL)

if __name__ == "__main__":
    main()