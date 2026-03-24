# 🌍 Wikidata Extraction Module

The `wikidata/` directory contains scripts for extracting entity data from **Wikidata**.

This module provides **large-scale, diverse entity coverage** for Luxembourgish NER.

---

## 🎯 Purpose

* Collect entities from Wikidata
* Extract specific entity types (PER, LOC, ORG, etc.)
* Build datasets for NER

---

## 📂 Files Overview

### `wikidata_scrape_all.py`

Extracts all entity types.

---

### `wikidata_scrape_per.py`

Extracts person (PER) entities.

---

### `wikidata_scrape_spaq.py`

Extracts specialized entity categories.

---

## 🔄 Role in Pipeline

```text
Wikidata → Extraction → Entity Lists → CoNLL Generation
```

---

## ⚙️ Example Usage

```bash
python scripts/data_extraction/wikidata/wikidata_scrape_all.py
```

---

## 🧠 Summary

✔ Large-scale entity extraction
✔ Covers multiple entity types
✔ Complements LOD data

---

This module ensures **broad coverage and diversity of entities** in the dataset.
