# 📊 Evaluation Module

The `evaluation/` directory contains scripts for measuring the performance of the trained NER model.

Evaluation is performed using both **token-level and span-level metrics**, ensuring a comprehensive analysis.

---

## 🎯 Purpose

* Evaluate model performance
* Compute precision, recall, and F1-score
* Analyze entity-level predictions
* Compare model outputs with ground truth

---

## 📂 Files Overview

### `eval_conll_tokens.py`

Token-level evaluation.

👉 Measures accuracy per token.

---

### `eval_conll_spans.py`

Span-level evaluation.

👉 Measures entity-level correctness.

---

### `eval_xlmr.py`

Evaluates predictions from XLM-R model.

---

### `eval_xlmr_conll_spanf1.py`

Computes **span-level F1 score**, the most important NER metric.

---

## 📊 Metrics

* Precision
* Recall
* F1 Score
* Token Accuracy
* Span-level Accuracy

---

## 🔄 Evaluation Pipeline

```text
Model Predictions → Compare with Ground Truth → Metrics Calculation → Reports
```

---

## ⚙️ Example Usage

```bash
python scripts/model/evaluation/eval_xlmr.py \
    --predictions predictions.txt \
    --labels test.conll
```

---

## 🧠 Key Insights

* Token-level metrics measure local accuracy
* Span-level metrics measure full entity correctness
* F1-score balances precision and recall

---

## 🧠 Summary

✔ Provides detailed evaluation metrics
✔ Supports both token and entity-level evaluation
✔ Essential for model comparison and improvement

---

This module ensures that LuxNLP results are **scientifically valid and measurable**.
