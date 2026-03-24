# 🐞 Debugging Module

The `debugging/` directory contains scripts used to **inspect, analyze, and troubleshoot** both the dataset and model predictions in the LuxNLP pipeline.

This module helps identify issues such as **label mismatches, data inconsistencies, and prediction errors**, ensuring the quality and reliability of the NER system.

---

## 📂 Files Overview

### `conll_file_stats.py`

Computes statistics for CoNLL datasets.

**Outputs:**

* Number of sentences
* Number of tokens
* Entity distribution (PER, LOC, ORG, etc.)

👉 Useful for understanding dataset composition and detecting imbalance.

---

### `debug_gold_vs_pred.py`

Compares **gold (true labels)** with **model predictions**.

**Purpose:**

* Identify incorrect predictions
* Detect systematic errors
* Analyze confusion between entity types

👉 Essential for error analysis and model debugging.

---

### `inspect_ner_csv.py`

Inspects NER outputs stored in CSV format.

**Features:**

* View predictions in structured format
* Analyze entity spans and labels
* Debug exported model outputs

---

### `show_conll_stats.py`

Displays quick summary statistics of CoNLL datasets.

👉 Useful for:

* Fast inspection
* Verifying preprocessing steps
* Checking dataset integrity

---

## 🔄 Role in Pipeline

This module is typically used after model prediction:

```text
Model Prediction → Debugging → Analysis → Improvement
```

It enables a deeper understanding of:

* Where the model fails
* How the dataset behaves
* What needs to be improved

---

## ⚙️ Example Usage

```bash
# Compare gold vs predictions
python scripts/Analysis/debugging/debug_gold_vs_pred.py

# Inspect dataset statistics
python scripts/Analysis/debugging/conll_file_stats.py

# View CSV outputs
python scripts/Analysis/debugging/inspect_ner_csv.py
```

---

## 🧠 Summary

The `debugging/` module provides:

✔ Detailed inspection of datasets
✔ Error analysis for model predictions
✔ Validation of preprocessing steps
✔ Insights for improving model performance

---

This module is critical for making the LuxNLP pipeline **robust, accurate, and reliable**.
