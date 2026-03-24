import csv
import json
import re
from collections import defaultdict
from pathlib import Path

# =========================================================
# PATHS
# =========================================================

BASE = Path("LuxNLP")


INPUT_SENTENCES = BASE / "data" / "cleaned" / "All_Extracted_Sentences.txt"

LOD_JSON = BASE / "data" / "cleaned" / "Lod.lu_en_lexicon.json"
WIKIDATA_CSV = BASE / "data" / "cleaned" / "wikidata_lb_all_ner.csv"
WIKIDATA_DESC_CSV = BASE / "data" / "cleaned" / "wikidata_lb_with_desc_ner.csv"

OUTPUT_CONLL = BASE / "data" / "processed" / "Lux_Final_gazetteer.conll"

# =========================================================
# TARGET LABELS
# =========================================================
ALLOWED_TAGS = {"PER", "LOC", "MED", "DATE", "EVENT", "PRODUCT", "ORG"}

# =========================================================
# TOKENIZATION
# =========================================================
TOKEN_PATTERN = re.compile(
    r"\d{1,2}/\d{1,2}/\d{4}"                      # 02/10/2014
    r"|\d{1,2}-\d{1,2}-\d{4}"                     # 02-10-2014
    r"|\d{1,2}\.\s+\w+\s+\d{4}"                   # 19. Mee 1993
    r"|\w+(?:[-'’]\w+)*"                          # words
    r"|[.,!?;:()/\"“”„'’%-]"                      # punctuation
)

def tokenize(text: str):
    return TOKEN_PATTERN.findall(text)

def normalize_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def normalize_match_text(text: str) -> str:
    text = text.lower().strip()
    text = text.replace("’", "'").replace("“", '"').replace("”", '"').replace("„", '"')
    text = re.sub(r"\s+", " ", text)
    return text

# =========================================================
# LOAD GAZETTEERS
# =========================================================
def add_entry(gazetteer, phrase, tag):
    phrase = normalize_text(str(phrase))
    if not phrase:
        return
    if tag not in ALLOWED_TAGS:
        return

    tokens = tokenize(phrase)
    if not tokens:
        return

    norm_tokens = tuple(normalize_match_text(t) for t in tokens)
    gazetteer[len(norm_tokens)].append((norm_tokens, tag, phrase))

def load_wikidata_csv(path, gazetteer):
    if not path.exists():
        print(f"[WARN] Missing file: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            tag = row.get("ner_tag", "").strip().upper()
            if tag not in ALLOWED_TAGS:
                continue

            label = row.get("label_lb", "").strip()
            desc = row.get("description_lb", "").strip()
            class_label = row.get("class_label_lb", "").strip()

            add_entry(gazetteer, label, tag)

            if desc and len(desc.split()) <= 6:
                add_entry(gazetteer, desc, tag)
            if class_label and len(class_label.split()) <= 4:
                add_entry(gazetteer, class_label, tag)

def load_lod_json(path, gazetteer):
    if not path.exists():
        print(f"[WARN] Missing file: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict):
        iterable = data.values()
    else:
        iterable = data

    for item in iterable:
        if not isinstance(item, dict):
            continue

        candidate_terms = []
        candidate_tags = []

        for key in ["label", "label_lb", "term", "entity", "surface_form", "name"]:
            if key in item and item[key]:
                value = item[key]
                if isinstance(value, list):
                    candidate_terms.extend([x for x in value if isinstance(x, str)])
                elif isinstance(value, str):
                    candidate_terms.append(value)

        for key in ["translation", "translations", "en", "lb", "alias", "aliases"]:
            if key in item and item[key]:
                value = item[key]
                if isinstance(value, list):
                    candidate_terms.extend([x for x in value if isinstance(x, str)])
                elif isinstance(value, str):
                    candidate_terms.append(value)

        for key in ["ner_tag", "tag", "entity_type", "type", "category"]:
            if key in item and item[key]:
                value = item[key]
                if isinstance(value, list):
                    candidate_tags.extend(value)
                else:
                    candidate_tags.append(value)

        valid_tag = None
        for t in candidate_tags:
            t = str(t).strip().upper()
            if t in ALLOWED_TAGS:
                valid_tag = t
                break

        if not valid_tag:
            continue

        for term in candidate_terms:
            if isinstance(term, str):
                add_entry(gazetteer, term, valid_tag)

def build_gazetteer():
    gazetteer = defaultdict(list)

    load_lod_json(LOD_JSON, gazetteer)
    load_wikidata_csv(WIKIDATA_CSV, gazetteer)
    load_wikidata_csv(WIKIDATA_DESC_CSV, gazetteer)

    for n in list(gazetteer.keys()):
        seen = set()
        cleaned = []
        for norm_tokens, tag, phrase in gazetteer[n]:
            key = (norm_tokens, tag)
            if key not in seen:
                seen.add(key)
                cleaned.append((norm_tokens, tag, phrase))
        gazetteer[n] = cleaned

    return gazetteer

# =========================================================
# MATCHING
# =========================================================
def is_boundary_ok(tokens, start, end):
    return True

def apply_gazetteer(tokens, gazetteer):
    labels = ["O"] * len(tokens)
    norm_tokens = [normalize_match_text(t) for t in tokens]

    max_len = max(gazetteer.keys(), default=1)

    for span_len in range(max_len, 0, -1):
        if span_len not in gazetteer:
            continue

        entries = gazetteer[span_len]
        phrase_map = defaultdict(list)
        for norm_phrase, tag, phrase in entries:
            phrase_map[norm_phrase].append((tag, phrase))

        for i in range(len(tokens) - span_len + 1):
            if any(labels[j] != "O" for j in range(i, i + span_len)):
                continue

            span = tuple(norm_tokens[i:i + span_len])
            if span not in phrase_map:
                continue

            if not is_boundary_ok(tokens, i, i + span_len):
                continue

            tag = phrase_map[span][0][0]
            labels[i] = f"B-{tag}"
            for j in range(i + 1, i + span_len):
                labels[j] = f"I-{tag}"

    return labels

# =========================================================
# DATE RULES
# =========================================================
MONTHS_LB = {
    "januar", "februar", "mäerz", "abrëll", "mee", "juni",
    "juli", "august", "september", "oktober", "november", "dezember"
}

def apply_date_rules(tokens, labels):
    norm = [normalize_match_text(t) for t in tokens]

    i = 0
    while i < len(tokens):
        # Pattern 1: 19 . Mee 1993
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

        # Pattern 2: 19. Mee 1993
        if re.fullmatch(r"\d{1,2}\.\s+\w+\s+\d{4}", tokens[i], flags=re.IGNORECASE):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # Pattern 3: 02/10/2014
        if re.fullmatch(r"\d{1,2}/\d{1,2}/\d{4}", tokens[i]):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # Pattern 4: 02-10-2014
        if re.fullmatch(r"\d{1,2}-\d{1,2}-\d{4}", tokens[i]):
            if labels[i] == "O":
                labels[i] = "B-DATE"
            i += 1
            continue

        # Pattern 5: 2023
        if re.fullmatch(r"(19|20)\d{2}", norm[i]) and labels[i] == "O":
            labels[i] = "B-DATE"

        i += 1

    return labels

# =========================================================
# SENTENCE FILTERING
# =========================================================
def is_good_sentence(text):
    text = text.strip()
    if len(text) < 5:
        return False
    if len(text.split()) < 2:
        return False
    return True

# =========================================================
# WRITE CONLL
# =========================================================
def write_conll(sentences, gazetteer, out_path):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    total_sent = 0
    total_tokens = 0
    total_entities = 0
    total_sent_with_entity = 0

    with open(out_path, "w", encoding="utf-8") as f:
        for sentence in sentences:
            sentence = normalize_text(sentence)
            if not is_good_sentence(sentence):
                continue

            tokens = tokenize(sentence)
            if not tokens:
                continue

            labels = apply_gazetteer(tokens, gazetteer)
            labels = apply_date_rules(tokens, labels)

            has_entity = any(label != "O" for label in labels)
            if has_entity:
                total_sent_with_entity += 1

            for tok, lab in zip(tokens, labels):
                f.write(f"{tok}\t{lab}\n")
                total_tokens += 1
                if lab.startswith("B-"):
                    total_entities += 1
            f.write("\n")
            total_sent += 1

    print(f"Saved CoNLL: {out_path}")
    print(f"Sentences: {total_sent}")
    print(f"Sentences with entity: {total_sent_with_entity}")
    print(f"Tokens: {total_tokens}")
    print(f"Entities: {total_entities}")

# =========================================================
# MAIN
# =========================================================
def main():
    if not INPUT_SENTENCES.exists():
        raise FileNotFoundError(f"Missing input sentences file: {INPUT_SENTENCES}")

    with open(INPUT_SENTENCES, "r", encoding="utf-8") as f:
        sentences = [line.strip() for line in f if line.strip()]

    gazetteer = build_gazetteer()

    print("Gazetteer stats:")
    total_entries = sum(len(v) for v in gazetteer.values())
    print(f"Total entries: {total_entries}")
    print(f"Span lengths: {sorted(gazetteer.keys())[:10]} ...")

    write_conll(sentences, gazetteer, OUTPUT_CONLL)

if __name__ == "__main__":
    main()