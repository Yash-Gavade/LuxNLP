import json
import os

# Input: your pure LB file (no fallback)
INPUT = "data/cleaned/wikidata_lb_pure.jsonl"

# Output: only LB entries WITH description
OUTPUT = "data/cleaned/wikidata_lb_with_description.jsonl"

os.makedirs("data/cleaned", exist_ok=True)

seen_ids = set()
total = 0
kept = 0

with open(INPUT, "r", encoding="utf-8") as f_in, \
     open(OUTPUT, "w", encoding="utf-8") as f_out:

    for line in f_in:
        total += 1
        line = line.strip()
        if not line:
            continue

        rec = json.loads(line)

        qid = rec.get("id", "").strip()
        label = rec.get("label_lb", "").strip()
        desc = rec.get("description_lb", "").strip()

        # Must have ID and label
        if not qid or not label:
            continue

        # Remove duplicates
        if qid in seen_ids:
            continue
        seen_ids.add(qid)

        # ❗ MUST HAVE NON-EMPTY description
        if not desc:
            continue

        clean_rec = {
            "id": qid,
            "label_lb": label,
            "description_lb": desc
        }

        f_out.write(json.dumps(clean_rec, ensure_ascii=False) + "\n")
        kept += 1

print("\nCLEANING DONE")
print("--------------------")
print(f"Total records processed: {total}")
print(f"Records with LB description: {kept}")
print(f"Saved cleaned file to: {OUTPUT}")
