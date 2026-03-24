# 🏗️ Dataset Creation Module

The `dataset_creation/` directory contains scripts responsible for transforming extracted and preprocessed data into the **final structured NER dataset** used in the LuxNLP pipeline.

This module integrates multiple data sources and applies **cleaning, annotation, merging, conversion, and splitting** to produce a high-quality dataset in **CoNLL format**.

---

## 🎯 Purpose

The dataset creation module is designed to:

* Clean and normalize extracted datasets
* Merge multiple data sources (LOD, Wikidata, Leipzig, etc.)
* Add or refine entity annotations (BIO tagging)
* Convert different formats into CoNLL
* Split the dataset into **train / dev / test sets**

👉 This module produces the final dataset:

```text id="c8ow8e"
Lux_Final.conll
```

---

## 🧩 Submodules

### 🏷️ annotation

Scripts for adding or modifying entity labels.

**Responsibilities:**

* Assign NER tags based on class/type
* Standardize entity labeling across datasets

👉 Ensures consistent **BIO tagging scheme**.

---

### 🧹 cleaning

Scripts for cleaning and refining datasets.

**Includes:**

* Removing noise and invalid entries
* Fixing label inconsistencies
* Filtering low-quality data

👉 Improves dataset quality and reliability.

---

### 🔄 conversion

Scripts for converting external or custom formats into CoNLL.

**Includes:**

* Transforming survey or structured inputs into NER format

👉 Enables integration of additional data sources.

---

### 🔗 merging

Scripts for combining multiple datasets.

**Includes:**

* Merging LOD, Wikidata, Leipzig, and other datasets
* Combining lexicons and labeled data
* Removing duplicates across sources

👉 Creates a unified dataset with broader coverage.

---

### ✂️ splitting

Scripts for dividing the dataset into training, validation, and test sets.

**Includes:**

* Standard split (e.g., 70/15/15)
* Updated/custom split strategies

👉 Ensures proper evaluation and prevents data leakage.

---

## 🔄 Role in Pipeline

```text id="p1f5mb"
Data Extraction → Dataset Creation → Model Training → Evaluation
```

This module bridges **raw data processing and machine learning**.

---

## ⚙️ Example Workflow

```bash id="9h1gph"
# Step 1: Clean dataset
python scripts/dataset_creation/cleaning/clean_conll_stats.py

# Step 2: Merge datasets
python scripts/dataset_creation/merging/merge_all_conll.py

# Step 3: Add annotations
python scripts/dataset_creation/annotation/add_ner_type.py

# Step 4: Split dataset
python scripts/dataset_creation/splitting/split_conll_70_15_15.py
```

---

## 📊 Output

The final outputs include:

* `Lux_Final.conll` (main dataset)
* Train/dev/test splits
* Cleaned and merged datasets
* Intermediate processed files

---

## 🧠 Key Design Principles

* **Dataset-centric approach**
* **Multi-source integration**
* **High-quality annotation consistency**
* **Reproducible pipeline**

---

## 📌 Summary

The `dataset_creation/` module provides:

✔ Data cleaning and normalization
✔ Multi-source dataset merging
✔ Consistent NER annotation
✔ Flexible dataset splitting
✔ Final training-ready dataset

---

This module is the **core of the LuxNLP pipeline**, ensuring that the model is trained on **accurate, diverse, and well-structured data**.
