import json
import os
import time

import requests

# Output file for non-PER entities
OUTPUT_PATH = "data/raw/wikidata_lb_other_ner.jsonl"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

ENDPOINT = "https://query.wikidata.org/sparql"

LIMIT = 1000        # results per request
SLEEP = 2           # seconds between requests

# --- NER config -------------------------------------------------------
# We skip Q5 (human/PER) because you already have it.
# Here we define other NER types we want.
NER_CONFIG = [
    # Organisations
    {"class": "wd:Q43229", "ner_tag": "ORG",  "target_min": 10000, "target_max": 20000},

    # Locations: cities and countries (both LOC)
    {"class": "wd:Q515",   "ner_tag": "LOC",  "target_min": 10000, "target_max": 25000},
    {"class": "wd:Q6256",  "ner_tag": "LOC",  "target_min": 10000, "target_max": 25000},

    # Dates: years
    {"class": "wd:Q577",   "ner_tag": "DATE", "target_min": 10000, "target_max": 25000},
]

# ---------------------------------------------------------------------

def build_query(class_qid: str, offset: int) -> str:
    # Pure Luxembourgish only (no English fallback)
    return f"""
    SELECT ?item ?itemLabel ?itemDescription ?class ?classLabel WHERE {{
      VALUES ?class {{ {class_qid} }}
      ?item wdt:P31 ?class .

      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "lb".
      }}
    }}
    LIMIT {LIMIT}
    OFFSET {offset}
    """


def fetch(class_qid: str, offset: int) -> dict:
    query = build_query(class_qid, offset)
    headers = {
        "User-Agent": "LuxNLPBot/1.0 (student project; mail@example.com)"
    }
    params = {
        "query": query,
        "format": "json"
    }

    resp = requests.get(ENDPOINT, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    try:
        return resp.json()
    except ValueError:
        # allow weird control chars if any
        return json.loads(resp.text, strict=False)


def main():
    seen_ids = set()
    total_saved = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        # keep per-ner_tag counts
        tag_counts = {}

        for cfg in NER_CONFIG:
            class_qid = cfg["class"]
            ner_tag = cfg["ner_tag"]
            target_min = cfg["target_min"]
            target_max = cfg["target_max"]

            print(f"\n=== Collecting {ner_tag} from {class_qid} ===")
            offset = 0
            collected_for_tag = tag_counts.get(ner_tag, 0)

            while collected_for_tag < target_max:
                print(f"[{ner_tag}] Fetching offset={offset} (current count={collected_for_tag})")
                try:
                    result = fetch(class_qid, offset)
                except Exception as e:
                    print("Error while querying:", e)
                    print("Retrying in 20 seconds...")
                    time.sleep(20)
                    continue

                rows = result.get("results", {}).get("bindings", [])
                if not rows:
                    print(f"[{ner_tag}] No more results for class {class_qid}.")
                    break

                saved_this_chunk = 0

                for r in rows:
                    qid = r["item"]["value"].split("/")[-1]
                    if qid in seen_ids:
                        continue

                    label_lb = r.get("itemLabel", {}).get("value", "").strip()
                    desc_lb = r.get("itemDescription", {}).get("value", "").strip()
                    class_id = r["class"]["value"].split("/")[-1]
                    class_label_lb = r.get("classLabel", {}).get("value", "")

                    # Require both label and description in Luxembourgish (no empty text)
                    if not label_lb or not desc_lb:
                        continue

                    record = {
                        "id": qid,
                        "label_lb": label_lb,
                        "description_lb": desc_lb,
                        "class_id": class_id,
                        "class_label_lb": class_label_lb,
                        "ner_tag": ner_tag,
                    }

                    f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                    seen_ids.add(qid)
                    total_saved += 1
                    collected_for_tag += 1
                    saved_this_chunk += 1

                    if collected_for_tag >= target_max:
                        break

                print(f"[{ner_tag}] Saved this chunk: {saved_this_chunk}, total for tag: {collected_for_tag}")

                # if this chunk gave us nothing useful, stop to avoid infinite loop
                if saved_this_chunk == 0:
                    print(f"[{ner_tag}] No usable rows in this chunk, stopping for this class.")
                    break

                offset += LIMIT
                time.sleep(SLEEP)

            tag_counts[ner_tag] = collected_for_tag
            print(f"[{ner_tag}] Finished with {collected_for_tag} items (target {target_min}-{target_max}).")

    print("\n=== DONE ===")
    print(f"Total unique entities saved (all tags): {total_saved}")
    for tag, cnt in tag_counts.items():
        print(f"  {tag}: {cnt} items")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
