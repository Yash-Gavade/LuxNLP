import json
import os

# cleaned pure-LB file WITH description (from previous step)
INPUT_CLEAN = "data/cleaned/wikidata_lb_with_description.jsonl"

# original raw file that still has class_id / class_label_lb
INPUT_RAW = "data/raw/wikidata_lb.jsonl"

# output: cleaned + NER type
OUTPUT = "data/cleaned/wikidata_lb_with_desc_ner.jsonl"

os.makedirs("data/cleaned", exist_ok=True)

# 1) Build map: id -> class info from raw file
id_to_class = {}

with open(INPUT_RAW, "r", encoding="utf-8") as f_raw:
    for line in f_raw:
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        qid = rec.get("id")
        if not qid:
            continue
        id_to_class[qid] = {
            "class_id": rec.get("class_id", ""),
            "class_label_lb": rec.get("class_label_lb", "")
        }

print(f"Loaded class info for {len(id_to_class)} ids from raw file.")

# 2) Mapping from Wikidata class -> NER tag
CLASS_TO_NER = {
    "Q5": "PER",        # human
    "Q43229": "ORG",    # organisation
    "Q515": "LOC",      # city
    "Q6256": "LOC",     # country
}

total = 0
matched = 0

with open(INPUT_CLEAN, "r", encoding="utf-8") as f_in, \
     open(OUTPUT, "w", encoding="utf-8") as f_out:

    for line in f_in:
        line = line.strip()
        if not line:
            continue
        total += 1

        rec = json.loads(line)
        qid = rec.get("id")
        if not qid:
            continue

        class_info = id_to_class.get(qid, {})
        class_id = class_info.get("class_id", "")
        class_label_lb = class_info.get("class_label_lb", "")

        # decide simple NER tag
        ner_tag = CLASS_TO_NER.get(class_id, "MISC")

        rec["class_id"] = class_id
        rec["class_label_lb"] = class_label_lb
        rec["ner_tag"] = ner_tag

        f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
        matched += 1

print(f"Total cleaned records read: {total}")
print(f"Records written with NER tag: {matched}")
print(f"Output saved to: {OUTPUT}")
