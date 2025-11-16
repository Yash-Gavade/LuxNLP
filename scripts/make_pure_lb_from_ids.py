import json
import os
import time

import requests

INPUT = "data/raw/wikidata_lb.jsonl"            # your current 30k file
OUTPUT = "data/cleaned/wikidata_lb_pure.jsonl"  # new file: pure Luxembourgish
BATCH_SIZE = 50                                 # max 50 ids per API call

API_URL = "https://www.wikidata.org/w/api.php"
HEADERS = {
    "User-Agent": "LuxNLP-Student-Project/1.0 (contact: your-email@example.com)"
}

os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

def load_ids():
    ids = []
    with open(INPUT, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            ids.append(rec["id"])
    return ids

def fetch_lb_batch(ids_batch):
    ids_str = "|".join(ids_batch)
    params = {
        "action": "wbgetentities",
        "ids": ids_str,
        "props": "labels|descriptions",
        "languages": "lb",          # IMPORTANT: only Luxembourgish, no fallback!
        "format": "json"
    }
    resp = requests.get(API_URL, params=params, headers=HEADERS, timeout=60)
    resp.raise_for_status()
    data = resp.json().get("entities", {})
    out = {}
    for qid, ent in data.items():
        labels = ent.get("labels", {})
        descs = ent.get("descriptions", {})
        label_lb = labels.get("lb", {}).get("value", "")
        desc_lb = descs.get("lb", {}).get("value", "")
        out[qid] = {
            "label_lb": label_lb,
            "description_lb": desc_lb
        }
    return out

def main():
    ids = load_ids()
    print(f"Loaded {len(ids)} ids from {INPUT}")

    lb_map = {}
    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i:i + BATCH_SIZE]
        print(f"Fetching Luxembourgish for ids {i}–{i + len(batch) - 1}...")
        try:
            lb_info = fetch_lb_batch(batch)
        except Exception as e:
            print("Error while calling API:", e)
            print("Sleeping 20 seconds and retrying this batch...")
            time.sleep(20)
            try:
                lb_info = fetch_lb_batch(batch)
            except Exception as e2:
                print("Failed again, skipping this batch:", e2)
                continue

        lb_map.update(lb_info)
        time.sleep(1)  # be polite to the API

    # write only items that actually have a Luxembourgish label
    total = 0
    kept = 0
    with open(OUTPUT, "w", encoding="utf-8") as f_out:
        for qid in ids:
            info = lb_map.get(qid, {})
            label = info.get("label_lb", "").strip()
            desc = info.get("description_lb", "").strip()

            total += 1
            if not label:
                continue   # skip if no LB label at all

            record = {
                "id": qid,
                "label_lb": label,
                "description_lb": desc
            }
            f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
            kept += 1

    print(f"Done. Total ids checked: {total}")
    print(f"Kept with real Luxembourgish label_lb: {kept}")
    print(f"Pure LB file saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
