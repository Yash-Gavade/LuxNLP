# 🏷️ Annotation Module

The `annotation/` directory contains scripts responsible for assigning and standardizing **Named Entity Recognition (NER) labels** within the dataset.

This module ensures that all data follows a consistent **BIO tagging scheme**, which is essential for training NER models.

---

## 🎯 Purpose

* Assign entity labels based on class/type
* Standardize annotation across multiple datasets
* Ensure consistency in BIO tagging

👉 This module transforms raw or partially labeled data into **fully annotated NER datasets**.

---

## 📂 Files Overview

### `add_ner_type.py`

Adds NER labels to the dataset based on entity type.

**Functionality:**

* Maps entities to predefined labels (PER, LOC, ORG, DATE, etc.)
* Applies BIO tagging format (B-, I-, O)
* Ensures label consistency across datasets

👉 This is the **core annotation script** in the pipeline.

---

## 🔄 Role in Pipeline

```text
Merged Data → Annotation → Labeled Dataset → Model Training
```

---

## ⚙️ Example Usage

```bash
python scripts/dataset_creation/annotation/add_ner_type.py
```

---

## 🧠 Summary

✔ Assigns consistent NER labels
✔ Applies BIO tagging scheme
✔ Prepares data for model training

---

This module ensures that the dataset is **properly labeled, standardized, and ready for learning**.
