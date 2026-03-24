import json
import os

# Adjust paths if needed:
PER_FILE = "data/cleaned/wikidata_lb_with_desc_ner.jsonl"      # people
OTHER_FILE = "data/raw/wikidata_lb_other_ner1.jsonl"           # ORG/LOC/DATE
OUTPUT_FILE = "data/cleaned/wikidata_lb_all_ner.jsonl"

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records

def main():
    print(f"Loading PER data from: {PER_FILE}")
    per_records = load_jsonl(PER_FILE)
    print(f"  PER records: {len(per_records)}")

    print(f"Loading ORG/LOC/DATE data from: {OTHER_FILE}")
    other_records = load_jsonl(OTHER_FILE)
    print(f"  OTHER records: {len(other_records)}")

    by_id = {}
    clashes = 0

    # First add PER data
    for rec in per_records:
        qid = rec.get("id")
        if not qid:
            continue
        by_id[qid] = rec

    # Then add ORG/LOC/DATE data (avoid duplicates)
    for rec in other_records:
        qid = rec.get("id")
        if not qid:
            continue

        if qid in by_id:
            # Same id appears in both (rare, but just in case)
            old = by_id[qid]
            if old.get("ner_tag") != rec.get("ner_tag"):
                clashes += 1
                # keep the first version; you could also handle differently
            continue

        by_id[qid] = rec

    print(f"Total unique ids after merge: {len(by_id)}")
    print(f"  Conflicts (same id, different ner_tag): {clashes}")

    # Write merged file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for rec in by_id.values():
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Merged dataset written to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
