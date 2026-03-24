# 📏 Metrics Module

The `metrics/` directory contains scripts for evaluating the performance of the LuxNLP Named Entity Recognition (NER) system.

This module computes **quantitative evaluation metrics** that measure how well the model predicts entity labels compared to ground truth annotations.

---

## 🎯 Purpose

The evaluation focuses on two levels:

* **Token-level evaluation** → correctness of each token label
* **Span-level evaluation** → correctness of complete entity spans

These metrics are essential for understanding both **fine-grained accuracy** and **entity-level performance**.

---

## 📂 Files Overview

### `eval_conll_tokens.py`

Performs **token-level evaluation**.

**Measures:**

* Accuracy of individual token predictions
* Precision, Recall, F1-score at token level

👉 Useful for:

* Checking overall labeling performance
* Detecting small prediction errors

---

### `eval_conll_spans.py`

Performs **span-level evaluation** (entity-level).

**Measures:**

* Correct detection of full entity spans (BIO format)
* Precision, Recall, F1-score for entities

👉 Important for:

* Real NER performance evaluation
* Measuring correct entity extraction

---

## 📊 Output Metrics

Both scripts typically compute:

* **Precision** → Correct predictions / Total predicted
* **Recall** → Correct predictions / Total actual
* **F1-score** → Harmonic mean of precision and recall

These metrics are computed per entity type (e.g., PER, LOC, ORG, etc.) and overall.

---

## 🔄 Role in Pipeline

```text
Model Prediction → Metrics Evaluation → Analysis → Reporting
```

This module transforms raw predictions into **measurable performance indicators**.

---

## ⚙️ Example Usage

```bash
# Token-level evaluation
python scripts/Analysis/metrics/eval_conll_tokens.py

# Span-level evaluation
python scripts/Analysis/metrics/eval_conll_spans.py
```

---

## 🧠 When to Use

Use this module when you want to:

✔ Evaluate model performance after training
✔ Compare multiple models or datasets
✔ Generate metrics for research papers
✔ Validate improvements in the pipeline

---

## 📌 Summary

The `metrics/` module provides:

✔ Standard NER evaluation metrics
✔ Token-level and entity-level analysis
✔ Reliable performance measurement
✔ Foundation for reporting and visualization

---

This module ensures that the LuxNLP system is evaluated in a **rigorous and reproducible way**.
