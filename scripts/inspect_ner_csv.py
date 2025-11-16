import pandas as pd

CSV = "data/cleaned/wikidata_lb_all_ner.csv"

df = pd.read_csv(CSV)

print("Rows:", len(df))
print("\nCounts per ner_tag:")
print(df["ner_tag"].value_counts())

print("\nExample PER:")
print(df[df["ner_tag"] == "PER"].head(5))

print("\nExample LOC:")
print(df[df["ner_tag"] == "LOC"].head(5))

print("\nExample ORG:")
print(df[df["ner_tag"] == "ORG"].head(5))

print("\nExample DATE:")
print(df[df["ner_tag"] == "DATE"].head(5))
