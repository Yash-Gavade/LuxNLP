# 🤖 Model Module

The `model/` directory contains all components required for **training, evaluating, and deploying** the Luxembourgish Named Entity Recognition (NER) model.

This module is based on **XLM-RoBERTa (XLM-R)**, a multilingual transformer model that is fine-tuned for Luxembourgish NER tasks.

---

## 🎯 Objectives

* Train a transformer-based NER model
* Evaluate model performance using multiple metrics
* Perform inference on unseen text
* Support both baseline and advanced prediction pipelines

---

## 🧠 Model Overview

* **Model:** XLM-RoBERTa
* **Task:** Named Entity Recognition (NER)
* **Label Scheme:** BIO (Begin–Inside–Outside)
* **Entities:**

  * PER (Person)
  * LOC (Location)
  * ORG (Organization)
  * DATE
  * EVENT
  * MED
  * PRODUCT

---

## 📂 Submodules

### 🔹 `training/`

Handles model training and fine-tuning.

### 🔹 `evaluation/`

Evaluates model performance using token-level and span-level metrics.

### 🔹 `prediction/`

Performs inference and generates predictions.

---

## 🔄 Pipeline Overview

```text
Dataset → Training → Model → Evaluation → Prediction
```

---

## ⚙️ Requirements

* Python 3.10+
* Transformers (HuggingFace)
* PyTorch
* Scikit-learn
* seqeval

---

## 🧠 Summary

✔ Complete model lifecycle (train → eval → predict)
✔ Transformer-based multilingual NER
✔ Supports both research and production use

---

This module represents the **core intelligence of LuxNLP**, enabling accurate entity recognition for Luxembourgish text.
