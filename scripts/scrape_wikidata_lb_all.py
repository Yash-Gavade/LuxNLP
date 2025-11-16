import json
import os
import time

import requests

# Where to save the output
OUTPUT_PATH = "data/raw/wikidata_lb.jsonl"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

ENDPOINT = "https://query.wikidata.org/sparql"

# How many results per page
LIMIT = 2000
SLEEP = 2  # seconds between requests (be nice to Wikidata)

# Main classes we want (you can extend this list later)
CLASSES = [
    "wd:Q5",      # human
    "wd:Q43229",  # organization
    "wd:Q515",    # city
    "wd:Q6256",   # country
]

def build_query(offset: int) -> str:
    classes = " ".join(CLASSES)
    # note: language fallback "lb,en" is often safer
    return f"""
    SELECT ?item ?itemLabel ?itemDescription ?class ?classLabel WHERE {{
      VALUES ?class {{ {classes} }}
      ?item wdt:P31 ?class .

      SERVICE wikibase:label {{
        bd:serviceParam wikibase:language "lb,en".
      }}
    }}
    LIMIT {LIMIT}
    OFFSET {offset}
    """

def fetch(offset: int) -> dict:
    query = build_query(offset)
    headers = {
        "User-Agent": "LuxNLPBot/1.0 (student project; mail@example.com)"
    }
    params = {
        "query": query,
        "format": "json"
    }

    resp = requests.get(ENDPOINT, headers=headers, params=params, timeout=60)
    resp.raise_for_status()

    # Try normal JSON parse first
    try:
        data = resp.json()
    except ValueError:
        # Fallback: allow weird control characters
        data = json.loads(resp.text, strict=False)

    return data

def main():
    offset = 0
    saved = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        while True:
            print(f"Fetching: offset={offset}...")
            try:
                result = fetch(offset)
            except Exception as e:
                print("Error while querying:", e)
                print("Retrying in 15 seconds...")
                time.sleep(15)
                continue

            rows = result.get("results", {}).get("bindings", [])
            if not rows:
                print("No more results. Stopping.")
                break

            for r in rows:
                record = {
                    "id": r["item"]["value"].split("/")[-1],
                    "label_lb": r.get("itemLabel", {}).get("value", ""),
                    "description_lb": r.get("itemDescription", {}).get("value", ""),
                    "class_id": r["class"]["value"].split("/")[-1],
                    "class_label_lb": r.get("classLabel", {}).get("value", "")
                }
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                saved += 1

            print(f"Saved this chunk: {len(rows)}, total saved: {saved}")
            offset += LIMIT
            time.sleep(SLEEP)

    print(f"Done. Total entities saved: {saved}")
    print(f"File written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
