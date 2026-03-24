import json
import os
import xml.etree.ElementTree as ET


XML_PATH = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\raw\Lod.lu_250804-new-lod-art\new_lod-art.xml"
OUTPUT_JSONL = "data/cleaned/Lod.lu.jsonl"
os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)



def strip_ns(tag: str) -> str:
    """Remove XML namespace if present: {ns}tag -> tag."""
    return tag.split("}", 1)[-1]


def find_first_text(entry, tag_names):
    """
    Find first non-empty .text in any element whose local tag name is in tag_names.
    tag_names is a set like {"orth", "lemma"}.
    """
    for el in entry.iter():
        if strip_ns(el.tag) in tag_names:
            if el.text:
                txt = el.text.strip()
                if txt:
                    return txt
    return ""


def find_all_texts(entry, tag_names):
    """Collect all .text values for tags in tag_names (for examples, synonyms, …)."""
    values = []
    for el in entry.iter():
        if strip_ns(el.tag) in tag_names:
            if el.text:
                txt = el.text.strip()
                if txt:
                    values.append(txt)
    return values


def main():
    if not os.path.exists(XML_PATH):
        raise FileNotFoundError(f"XML not found: {XML_PATH}")

    print(f"Loading XML: {XML_PATH}")
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    # find all <entry> elements
    entries = [el for el in root.iter() if strip_ns(el.tag) == "entry"]
    print(f"Found {len(entries)} <entry> elements")

    out_count = 0

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as out_f:
        for e in entries:
            lod_id = e.get("id", "").strip()

            # Heuristic: try several possible tag names for lemma & definition
            lemma = find_first_text(e, {"lemma", "headword", "orth", "form", "spelling"})
            definition = find_first_text(e, {"def", "definition", "gloss"})

           
            examples = find_all_texts(e, {"example", "cit"})

            # skip totally empty entries
            if not lemma and not definition:
                continue

            record = {
                "lod_id": lod_id,
                "lemma_lb": lemma,
                "definition_lb": definition,
                "examples_lb": examples,
            }

            out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
            out_count += 1

    print(f"Saved {out_count} entries to {OUTPUT_JSONL}")


if __name__ == "__main__":
    main()
