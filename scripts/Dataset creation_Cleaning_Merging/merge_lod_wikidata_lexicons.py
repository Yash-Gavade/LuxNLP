import os
import json

import pandas as pd

# input files 
WIKIDATA_CSV = "data/cleaned/wikidata_lb_with_desc_ner.csv"


LOD_JSONL = "data/cleaned/Lod.lu_en_lexicon.jsonl"


OUTPUT_CSV = "data/cleaned/LuxNLP_lexicon_merged.csv"
OUTPUT_JSONL = "data/cleaned/LuxNLP_lexicon_merged.jsonl"

os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)


def main():
    # 1) Load Wikidata NER lexicon
    print(f"Loading Wikidata lexicon from {WIKIDATA_CSV}")
    wd = pd.read_csv(WIKIDATA_CSV)

    # Expect columns like: id, label_lb, description_lb, class_id, class_label_lb, ner_tag
    if "label_lb" not in wd.columns:
        raise ValueError("Wikidata CSV must have a 'label_lb' column.")

    wd["lemma_lower"] = wd["label_lb"].astype(str).str.strip().str.lower()

    print("Wikidata sample:")
    print(wd.head())

    # 2) Load LOD English lexicon
    print(f"\nLoading LOD lexicon from {LOD_JSONL}")
    lod = pd.read_json(LOD_JSONL, lines=True)

    # Expect columns: lemma_lb, lemma_lb_lower, meaning_en, part_of_speech, categories
    if "lemma_lb" not in lod.columns:
        raise ValueError("LOD JSONL must have a 'lemma_lb' column.")

    # robust: if lemma_lb_lower is missing, recompute
    if "lemma_lb_lower" in lod.columns:
        lod["lemma_lower"] = lod["lemma_lb_lower"].astype(str).str.strip().str.lower()
    else:
        lod["lemma_lower"] = lod["lemma_lb"].astype(str).str.strip().str.lower()

    print("LOD sample:")
    print(lod.head())

    # 3) Merge on lemma_lower (outer join => keep everything)
    merged = pd.merge(
        wd,
        lod,
        on="lemma_lower",
        how="outer",
        suffixes=("_wd", "_lod"),
    )

    # 4) Build a unified lemma field (prefer Wikidata label if present)
    merged["lemma_lb"] = merged["label_lb"].fillna(merged["lemma_lb"])

    # Flags to know where each row comes from
    merged["has_wikidata"] = merged["id"].notna()
    merged["has_lod"] = merged["meaning_en"].notna()

    # Some basic stats
    total_rows = len(merged)
    from_wd_only = ((merged["has_wikidata"]) & (~merged["has_lod"])).sum()
    from_lod_only = ((merged["has_lod"]) & (~merged["has_wikidata"])).sum()
    from_both = ((merged["has_wikidata"]) & (merged["has_lod"])).sum()

    print("\n=== MERGE STATS ===")
    print(f"Total rows in merged lexicon: {total_rows}")
    print(f"  Wikidata only: {from_wd_only}")
    print(f"  LOD only:      {from_lod_only}")
    print(f"  Both sources:  {from_both}")


    cols_order = [
        # core lemma
        "lemma_lb",
        "lemma_lower",

        # Wikidata (NER) info
        "id",
        "label_lb",
        "description_lb",
        "class_id",
        "class_label_lb",
        "ner_tag",

        # LOD info
        "meaning_en",
        "part_of_speech",
        "categories",

        # source flags
        "has_wikidata",
        "has_lod",
    ]

    # keep only columns that actually exist
    cols_order = [c for c in cols_order if c in merged.columns]
    merged = merged[cols_order]

    # 6) Save CSV
    merged.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"\nMerged CSV written to: {OUTPUT_CSV}")

    # 7) Save JSONL
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f_out:
        for _, row in merged.iterrows():
            rec = {}
            for c in merged.columns:
                val = row[c]

                # Convert NaN to None for JSON, but only for scalar-like values
                if not isinstance(val, (list, dict)) and not pd.api.types.is_list_like(val):
                    # scalar case: float, str, int, etc.
                    if isinstance(val, float) and pd.isna(val):
                        val = None
                # For lists/arrays we keep them as they are

                rec[c] = val

            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Merged JSONL written to: {OUTPUT_JSONL}")



if __name__ == "__main__":
    main()
