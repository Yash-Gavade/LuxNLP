# 🧹 Cleaning Module

The `cleaning/` directory contains scripts for refining and improving dataset quality by removing noise, fixing inconsistencies, and validating data.

---

## 🎯 Purpose

* Remove noisy or invalid entries
* Fix labeling inconsistencies
* Normalize dataset structure
* Improve overall data quality

👉 Clean data is critical for achieving **high model performance**.

---

## 📂 Files Overview

### `clean_conll_stats.py`

Cleans and analyzes CoNLL dataset statistics.

👉 Ensures dataset structure is valid and consistent.

---

### `clean_lb_description.py`

Cleans LOD/Wikidata descriptions.

👉 Removes irrelevant or noisy text.

---

### `clean_wikidata_lb.py`

Cleans Wikidata-based data.

👉 Ensures entity consistency and removes duplicates.

---

## 🔄 Role in Pipeline

```text
Raw / Merged Data → Cleaning → Refined Dataset → Annotation
```

---

## ⚙️ Example Usage

```bash
python scripts/dataset_creation/cleaning/clean_conll_stats.py
```

---

## 🧠 Summary

✔ Improves dataset quality
✔ Removes inconsistencies and noise
✔ Ensures clean input for annotation

---

This module ensures that the dataset is **accurate, consistent, and reliable**.
