# 🧹 Preprocessing Module

The `preprocessing/` directory contains scripts for cleaning and preparing raw text data before CoNLL conversion.

---

## 🎯 Purpose

* Remove noise and inconsistencies
* Normalize sentence structure
* Prepare clean input for NER tagging

---

## 📂 Files Overview

### `clean_extracted_sentences.py`

Cleans raw extracted sentences.

---

### `clean_sentences_to_conll.py`

Prepares sentences for CoNLL conversion.

---

### `merge_and_clean_sentences.py`

Merges multiple datasets and removes duplicates.

---

## 🔄 Role in Pipeline

```text
Raw Data → Cleaning → Normalized Text → CoNLL Generation
```

---

## 🧠 Summary

✔ Improves data quality
✔ Removes duplicates/noise
✔ Ensures consistency

---

This module ensures **clean, high-quality input data** for downstream processing.
