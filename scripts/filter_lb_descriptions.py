# scripts/filter_lb_descriptions.py
import json

INPUT = "data/raw/wikidata_lb.jsonl"
OUTPUT = "data/cleaned/wikidata_lb_has_desc.jsonl"

kept = 0
total = 0

with open(INPUT, "r", encoding="utf-8") as f_in, \
     open(OUTPUT, "w", encoding="utf-8") as f_out:
    for line in f_in:
        total += 1
        if not line.strip():
            continue
        rec = json.loads(line)
        desc = rec.get("description_lb", "").strip()
        if desc:
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
            kept += 1

print(f"Total records: {total}")
print(f"With non-empty description_lb: {kept}")
print(f"Saved to {OUTPUT}")
