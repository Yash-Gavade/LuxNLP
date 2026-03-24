import json
from collections import Counter, defaultdict
from pathlib import Path
import csv

# Input: your existing LOD lexicon
LOD_JSONL = "data/cleaned/Lod.lu_en_lexicon.jsonl"

# Outputs
OUT_JSONL = "data/cleaned/Lod_lu_ner_categories.jsonl"
OUT_CSV = "data/cleaned/Lod_lu_ner_categories.csv"


ALLOWED_POS = {"SUBST"}  


CATEGORY_GROUPS = {
    # --- MED-like things ---
    # MED  : medical vocabulary
    # ANAT : anatomy
    # CORONA, CHIM, CHEEMESCHT-ELEMENT, BIOL, PSYCH : health / chemistry / biology
    "MEDICINE": {
        "MED", "ANAT", "CORONA",
        "CHIM", "CHEEMESCHT-ELEMENT",
        "BIOL", "PSYCH",
    },

    # --- EVENTS / CELEBRATIONS / SPORTS ---
    # FUSSBALL, SPORT  : football & sports
    # FEST, FEIERDEEG  : festivals, holidays
    # HALLOWEEN, KLEESCHEN : special holidays
    # SPILLPLAZ, THEATER   : activity / performance places
    "EVENT": {
        "FUSSBALL", "SPORT",
        "FEST", "FEIERDEEG",
        "HALLOWEEN", "KLEESCHEN",
        "SPILLPLAZ", "THEATER",
    },

    # --- PRODUCTS / THINGS / FOOD / ANIMALS ---
    # DEIER, VULL, FESCH : animals, birds, fish
    # IESSEN, GEMEIS, UEBST, GEDRENKS, KRAUTGEWIERZ : food/drinks
    # PLANTE, BLUMM : plants & flowers
    # GEFIER : vehicles
    "PRODUCT": {
        "DEIER", "VULL", "FESCH",
        "IESSEN", "GEMEIS", "UEBST",
        "GEDRENKS", "KRAUTGEWIERZ",
        "PLANTE", "BLUMM", "GEFIER",
    },
}


def main():
    lod_path = Path(LOD_JSONL)
    if not lod_path.exists():
        raise SystemExit(f"LOD file not found: {lod_path}")

    total_entries = 0
    entries_with_categories = 0
    pos_kept = Counter()
    pos_dropped = Counter()
    all_category_counts = Counter()
    group_counts = Counter()

    rows_for_output = []
    example_rows = defaultdict(list)

    print(f"Loading LOD lexicon from {lod_path} ...")

    with lod_path.open("r", encoding="utf-8") as f_in:
        for line in f_in:
            line = line.strip()
            if not line:
                continue
            total_entries += 1

            rec = json.loads(line)
            lemma = rec.get("lemma_lb")
            lemma_lower = rec.get("lemma_lb_lower") or (lemma or "").lower()
            meaning_en = rec.get("meaning_en")
            pos = rec.get("part_of_speech")
            cats = rec.get("categories") or []

            if cats:
                entries_with_categories += 1
                all_category_counts.update(cats)

            # POS filter
            if pos not in ALLOWED_POS:
                pos_dropped[pos] += 1
                continue
            pos_kept[pos] += 1

            # assign high-level groups based on CATEGORY_GROUPS
            matched_groups = set()
            for group_name, group_catset in CATEGORY_GROUPS.items():
                if any(c in group_catset for c in cats):
                    matched_groups.add(group_name)

            # skip entries that don't fall into any of our target groups
            if not matched_groups:
                continue

            out_rec = {
                "lemma_lb": lemma,
                "lemma_lb_lower": lemma_lower,
                "meaning_en": meaning_en,
                "part_of_speech": pos,
                "categories": cats,
                "ner_groups": sorted(matched_groups),
            }
            rows_for_output.append(out_rec)

            for g in matched_groups:
                group_counts[g] += 1
                # keep a few examples per group for inspection
                if len(example_rows[g]) < 5:
                    example_rows[g].append(out_rec)

    # === BASIC STATS ===
    print("\n=== LOD BASIC STATS ===")
    print(f"Total LOD entries                 : {total_entries}")
    print(f"Entries with non-empty categories : {entries_with_categories}")
    print(f"Entries after POS filter          : {sum(pos_kept.values())}")
    print(f"Entries assigned to any ner_group : {len(rows_for_output)}")

    print("\nPOS kept (by part_of_speech):")
    for p, cnt in pos_kept.items():
        print(f"  {p:10s} : {cnt:6d}")
    print("\nPOS dropped:")
    for p, cnt in pos_dropped.items():
        print(f"  {p:10s} : {cnt:6d}")

    print("\nTop 30 LOD category codes (raw):")
    for cat, cnt in all_category_counts.most_common(30):
        print(f"  {cat:20s} : {cnt:6d}")

    print("\n=== HIGH-LEVEL GROUP COUNTS ===")
    for g, cnt in group_counts.items():
        print(f"  {g:10s} : {cnt:6d}")

    print("\nExample entries per group:")
    for g, ex_list in example_rows.items():
        print(f"\n-- {g} --")
        for ex in ex_list:
            print(
                f"  lemma_lb='{ex['lemma_lb']}', "
                f"meaning_en='{ex['meaning_en']}', "
                f"categories={ex['categories']}"
            )

    # === WRITE DATASETS ===
    out_path_jsonl = Path(OUT_JSONL)
    out_path_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with out_path_jsonl.open("w", encoding="utf-8") as f_out:
        for rec in rows_for_output:
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\nLOD NER JSONL written to: {out_path_jsonl}")

    out_path_csv = Path(OUT_CSV)
    with out_path_csv.open("w", encoding="utf-8", newline="") as f_csv:
        fieldnames = [
            "lemma_lb",
            "lemma_lb_lower",
            "meaning_en",
            "part_of_speech",
            "categories",
            "ner_groups",
        ]
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames)
        writer.writeheader()
        for rec in rows_for_output:
            row = dict(rec)
            # turn list fields into pipe-separated strings for CSV
            row["categories"] = "|".join(row["categories"] or [])
            row["ner_groups"] = "|".join(rec["ner_groups"] or [])
            writer.writerow(row)
    print(f"LOD NER CSV written to: {out_path_csv}")


if __name__ == "__main__":
    main()
