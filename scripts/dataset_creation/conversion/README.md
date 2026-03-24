# 🔄 Conversion Module

The `conversion/` directory contains scripts for transforming external or custom datasets into **CoNLL format**, which is required for NER training.

---

## 🎯 Purpose

* Convert datasets into CoNLL format
* Integrate external or custom data sources
* Ensure compatibility with the LuxNLP pipeline

---

## 📂 Files Overview

### `survey_to_conll.py`

Converts survey or structured input data into CoNLL format.

**Functionality:**

* Tokenizes input text
* Assigns BIO labels
* Outputs NER-ready dataset

👉 Enables incorporation of **custom annotated data**.

---

## 🔄 Role in Pipeline

```text
External Data → Conversion → CoNLL Dataset → Merging
```

---

## ⚙️ Example Usage

```bash
python scripts/dataset_creation/conversion/survey_to_conll.py
```

---

## 🧠 Summary

✔ Converts external datasets into standard format
✔ Enables integration of new data sources
✔ Supports flexible dataset expansion

---

This module ensures that all data can be **uniformly processed within the pipeline**.
