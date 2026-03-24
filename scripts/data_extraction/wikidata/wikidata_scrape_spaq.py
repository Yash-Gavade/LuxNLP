import json
import os
import time

from SPARQLWrapper import JSON, SPARQLWrapper

# Save file here
OUTPUT_PATH = "data/raw/wikidata_lb.jsonl"
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

ENDPOINT = "https://query.wikidata.org/sparql"

LIMIT = 5000   # items per request
SLEEP = 2      # seconds between requests

# MAIN CLASSES 
CLASSES = [
    "wd:Q5",      # Person
    "wd:Q43229",  # organization
    "wd:Q515",    # city
    "wd:Q6256",   # country
]

def build_query(offset):
    classes = " ".join(CLASSES)
    return f"""
    SELECT ?item ?itemLabel ?itemDescription ?class ?classLabel WHERE {{
        VALUES ?class {{ {classes} }}
        ?item wdt:P31 ?class .

        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "lb". }}
    }}
    LIMIT {LIMIT}
    OFFSET {offset}
    """

def fetch(offset):
    s = SPARQLWrapper(ENDPOINT)
    s.addCustomHttpHeader("User-Agent", "LuxNLPBot/1.0 (student project)")
    s.setReturnFormat(JSON)
    s.setQuery(build_query(offset))
    return s.query().convert()


def main():
    offset = 0
    saved = 0

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        while True:
            print(f"Fetching: offset={offset}...")
            try:
                result = fetch(offset)
            except Exception as e:
                print("Error:", e)
                print("Retrying in 10 seconds...")
                time.sleep(10)
                continue

            rows = result["results"]["bindings"]
            if not rows:
                print("No more results. Finished.")
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

            print(f"Saved: {saved}")
            offset += LIMIT
            time.sleep(SLEEP)

    print(f"Total entities saved: {saved}")

if __name__ == "__main__":
    main()
