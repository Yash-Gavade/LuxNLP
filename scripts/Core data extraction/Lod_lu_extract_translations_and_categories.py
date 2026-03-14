import json
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

XML_PATH = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\raw\Lod.lu_250804-new-lod-art\new_lod-art.xml"
OUTPUT_JSONL = "data/cleaned/Lod.lu_entries_with_domains_and_translations.jsonl"

os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)


def strip_ns(tag: str) -> str:
    """Remove XML namespace if present: {ns}tag -> tag."""
    return tag.split("}", 1)[-1]


def get_lemma(entry):
    """Return lemma text (Luxembourgish word)."""
    for el in entry.iter():
        if strip_ns(el.tag) == "lemma" and el.text:
            return el.text.strip()
    return ""


def get_pos(entry):
    """Return part of speech, e.g. SUBST, VERB, INTERJ."""
    for el in entry.iter():
        if strip_ns(el.tag) == "partOfSpeech" and el.text:
            return el.text.strip()
    return ""


def get_categories(entry):
    """Return a list of category labels, e.g. ['A1', 'ANAT', 'MED']."""
    cats = []
    for el in entry.iter():
        if strip_ns(el.tag) == "category" and el.text:
            txt = el.text.strip()
            if txt:
                cats.append(txt)
    # deduplicate, preserve order
    seen = set()
    out = []
    for c in cats:
        if c not in seen:
            seen.add(c)
            out.append(c)
    return out


def get_translations(entry):
    """
    Extract translations per language from <meaning><targetLanguage lang="xx">...</targetLanguage>.
    We collect all descendant .text from inside targetLanguage, not just direct text.
    Returns: dict(lang -> list of strings)
    """
    translations = defaultdict(list)

    for meaning in entry.iter():
        if strip_ns(meaning.tag) != "meaning":
            continue

        for tl in meaning.iter():
            if strip_ns(tl.tag) != "targetLanguage":
                continue

            lang = tl.attrib.get("lang")
            if not lang:
                continue

            texts = []
            # collect all descendant text inside this targetLanguage
            for node in tl.iter():
                if node is tl:
                    continue
                if node.text:
                    txt = node.text.strip()
                    if txt:
                        texts.append(txt)

            if texts:
                combined = "; ".join(texts)
                translations[lang].append(combined)

    # dedup per language
    translations = {
        lang: sorted(set(values))
        for lang, values in translations.items()
    }
    return translations


def main():
    if not os.path.exists(XML_PATH):
        raise FileNotFoundError(f"XML not found: {XML_PATH}")

    print(f"Loading XML: {XML_PATH}")
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    entries = [el for el in root.iter() if strip_ns(el.tag) == "entry"]
    print(f"Found {len(entries)} <entry> elements")

    out_count = 0

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as out_f:
        for e in entries:
            lod_id = e.get("id", "").strip()

            lemma = get_lemma(e)
            pos = get_pos(e)
            categories = get_categories(e)
            translations = get_translations(e)

            # Build nice, flat fields for main languages
            meaning_de = "; ".join(translations.get("de", []))
            meaning_fr = "; ".join(translations.get("fr", []))
            meaning_en = "; ".join(translations.get("en", []))
            meaning_pt = "; ".join(translations.get("pt", []))

            # Skip completely empty entries
            if not lemma and not (meaning_de or meaning_fr or meaning_en or meaning_pt):
                continue

            record = {
                "lod_id": lod_id,
                "lemma_lb": lemma,
                "part_of_speech": pos,
                "categories": categories,      # includes things like 'MED', 'ANAT', ...
                "meaning_de": meaning_de,
                "meaning_fr": meaning_fr,
                "meaning_en": meaning_en,
                "meaning_pt": meaning_pt,
            }

            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_count += 1

    print(f"Saved {out_count} entries to {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
