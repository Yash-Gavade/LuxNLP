import json

input_json = "LuxNLP-main/data/cleaned/wikidata_lb_all_ner.json"
output_jsonl = "LuxNLP-main/data/cleaned/wikidata_lb_all_ner.jsonl"

with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)   # loads full list

with open(output_jsonl, "w", encoding="utf-8") as f:
    for item in data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("✅ Converted JSON → JSONL")