# 🔗 Merging Module

The `merging/` directory contains scripts for combining multiple datasets into a **single unified dataset**.

This module is crucial for building a **diverse and comprehensive NER dataset**.

---

## 🎯 Purpose

* Merge datasets from different sources (LOD, Wikidata, Leipzig, etc.)
* Combine lexicons and labeled data
* Remove duplicates and overlaps
* Ensure consistent structure across datasets

---

## 📂 Files Overview

### `merge_all_conll.py`

Combines all available CoNLL datasets.

👉 Produces a unified dataset.

---

### `merge_datasets.py`

General-purpose dataset merging script.

👉 Handles multiple input formats.

---

### `merge_leipzig_conll.py`

Merges Leipzig corpus data with other datasets.

---

### `merge_lod_wikidata.py`

Combines LOD and Wikidata datasets.

👉 Integrates structured and large-scale entity sources.

---

## 🔄 Role in Pipeline

```text
Multiple Data Sources → Merging → Unified Dataset → Cleaning / Annotation
```

---

## ⚙️ Example Usage

```bash
python scripts/dataset_creation/merging/merge_all_conll.py
```

---

## 🧠 Summary

✔ Combines multiple datasets
✔ Increases data diversity
✔ Removes duplicates
✔ Builds a unified dataset

---

This module enables LuxNLP to leverage **multi-source data for improved performance**.
