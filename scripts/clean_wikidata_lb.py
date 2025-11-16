import json
import os

import pandas as pd

RAW = "data/raw/wikidata_lb.jsonl"
OUT = "data/cleaned/wikidata_lb_clean.csv"

os.makedirs(os.path.dirname(OUT), exist_ok=True)

def main():

    items = []
    with open(RAW, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line)
            if data.get("label_lb"):
                items.append(data)

    df = pd.DataFrame(items)

    df = df.drop_duplicates(subset=["id"])
    df = df.sort_values(by=["class_label_lb", "label_lb"])

    df.to_csv(OUT, index=False)
    print("Saved cleaned file:", OUT)

if __name__ == "__main__":
    main()
