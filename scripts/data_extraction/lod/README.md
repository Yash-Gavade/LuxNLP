# 📚 LOD Extraction Module

The `lod/` directory contains scripts for extracting and processing data from **LOD.lu (Luxembourg Open Data)**.

This module provides **high-quality lexical resources** for Luxembourgish NER.

---

## 🎯 Purpose

* Extract entity categories and labels
* Retrieve translations and multilingual mappings
* Build structured lexicons for NER

---

## 📂 Files Overview

### `lod_categories.py`

Extracts entity categories from LOD.

---

### `lod_extract.py`

Main extraction script for LOD data.

---

### `lod_extract_translations.py`

Extracts multilingual translations.

---

### `lod_inspect.py`

Inspects LOD structure and data.

---

### `lod_lexicon.py`

Builds lexicons for entity matching.

---

## 🔄 Role in Pipeline

```text
LOD Source → Extraction → Lexicon → CoNLL Generation
```

---

## 🧠 Summary

✔ Structured lexical extraction
✔ High-quality entity seeds
✔ Foundation for gazetteer-based tagging

---

This module provides **precise and reliable entity knowledge** for LuxNLP.
