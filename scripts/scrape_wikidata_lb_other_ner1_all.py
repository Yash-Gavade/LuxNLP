import json
import os
import time
import requests

# =====================================================
#  Scrape non-PER NER types for Luxembourgish (ORG/LOC/DATE)
# =====================================================

# Output file for ORG / LOC / DATE entities
OUTPUT_PATH =  "data/raw/wikidata_lb_other_ner1.jsonl"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

ENDPOINT = "https://query.wikidata.org/sparql"

LIMIT = 1000        # results per request
SLEEP = 2           # seconds between requests

# --- NER config -------------------------------------------------------
# We skip Q5 (human/PER) because you already collected that.
# Here we define other NER types we want, with multiple classes each.

NER_CONFIG = [
    # ---------- ORG ----------
    # organisation
    {"class": "wd:Q43229",   "ner_tag": "ORG",  "target_min": 3000, "target_max": 5000},
    # business enterprise / company
    {"class": "wd:Q4830453", "ner_tag": "ORG",  "target_min": 3000, "target_max": 5000},
    # university
    {"class": "wd:Q3918",    "ner_tag": "ORG",  "target_min": 3000, "target_max": 5000},
    # political party
    {"class": "wd:Q7278",    "ner_tag": "ORG",  "target_min": 3000, "target_max": 5000},

    # ---------- LOC ----------
    # city
    {"class": "wd:Q515",     "ner_tag": "LOC",  "target_min": 2000, "target_max": 4000},
    # country
    {"class": "wd:Q6256",    "ner_tag": "LOC",  "target_min": 2000, "target_max": 4000},
    # human settlement (villages, towns, etc.)
    {"class": "wd:Q486972",  "ner_tag": "LOC",  "target_min": 2000, "target_max": 4000},
    # geographical object (mountain, river, etc.)
    {"class": "wd:Q618123",  "ner_tag": "LOC",  "target_min": 2000, "target_max": 4000},

    # ---------- DATE ----------
    # year
    {"class": "wd:Q577",     "ner_tag": "DATE", "target_min": 3000, "target_max": 5000},
    # century
    {"class": "wd:Q205892",  "ner_tag": "DATE", "target_min": 3000, "target_max": 5000},
    # decade
    {"class": "wd:Q2334719", "ner_tag": "DATE", "target_min": 3000, "target_max": 5000},
]
# ---------------------------------------------------------------------


def build_query(class_qid: str, offset: int) -> str:
    """
    Build SPARQL query for a given Wikidata class and offset.
    Pure Luxembourgish only ("lb") – no English fallback.
    """
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
    """
    Execute SPARQL query and return JSON result.
    Uses requests, with a small fallback for weird control chars.
    """
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

            print(f"\n=== Collecting {ner_tag} from class {class_qid} ===")
            offset = 0
            # how many we already collected for this ner_tag (across classes)
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

                    # STRICT: require both label and description in Luxembourgish (non-empty)
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
                    saved_this_chunk += 1
                    total_saved += 1
                    collected_for_tag += 1
                    seen_ids.add(qid)

                    if collected_for_tag >= target_max:
                        break

                # ensure data is written even if you stop the script later
                f_out.flush()

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
