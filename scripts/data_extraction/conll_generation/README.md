# 📄 CoNLL Generation Module

The `conll_generation/` directory contains scripts for converting extracted data into the **CoNLL format (BIO tagging scheme)** used for Named Entity Recognition (NER).

This module is responsible for transforming raw or semi-structured data into **token-level labeled datasets** suitable for model training.

---

## 🎯 Purpose

* Convert different data sources into **standardized CoNLL format**
* Apply **BIO tagging (B-ENTITY, I-ENTITY, O)**
* Ensure consistency across datasets from multiple sources

👉 This is a critical step for preparing data for NER models.

---

## 📂 Files Overview

### `conll_from_gazetteers.py`

Generates CoNLL data using **gazetteer-based matching**.

👉 Uses predefined entity lists to label tokens.

---

### `conll_from_leipzig.py`

Converts **Leipzig corpus text** into CoNLL format.

👉 Useful for adding natural sentence structures.

---

### `conll_from_lod.py`

Converts **LOD.lu extracted data** into CoNLL format.

👉 Uses structured lexicon data for labeling.

---

### `conll_from_wikidata.py`

Generates CoNLL data from **Wikidata entities**.

👉 Provides large-scale entity coverage.

---

## 🔄 Role in Pipeline

```text
Extracted Data → CoNLL Generation → Dataset Creation → Model Training
```

---

## ⚙️ Example Usage

```bash
python scripts/data_extraction/conll_generation/conll_from_lod.py
```

---

## 🧠 Summary

✔ Converts multiple sources into unified format
✔ Applies BIO tagging
✔ Prepares training-ready NER data

---

This module ensures that all extracted data is **standardized, structured, and model-ready**.
