# 🔮 Prediction Module

The `prediction/` directory contains scripts for running inference using trained NER models.

This module supports multiple prediction strategies, including baseline and transformer-based methods.

---

## 🎯 Purpose

* Perform NER inference on new text
* Load trained model checkpoints
* Generate labeled outputs in CoNLL format
* Support experimentation with multiple prediction approaches

---

## 📂 Files Overview

### `predict.py`

General prediction script.

---

### `predict_xlmr.py`

Prediction using trained XLM-R model.

---

### `predict_conll.py`

Generates predictions in CoNLL format.

---

### `predict_baseline.py`

Baseline model predictions (rule-based or simple models).

---

### `predict_checkpoint.py`

Loads model from checkpoint and predicts.

---

### `predict_model_baseline.py`

Baseline prediction using saved models.

---

## 🔄 Prediction Pipeline

```text
Input Text → Tokenization → Model Inference → Label Assignment → Output
```

---

## ⚙️ Example Usage

```bash
python scripts/model/prediction/predict_xlmr.py \
    --model_path model_output/ \
    --input_text "Den 12. Mee 2024 war zu Lëtzebuerg."
```

---

## 🧠 Output Format

* Tokenized text
* BIO labels
* Optional CoNLL formatted output

---

## 🧠 Key Features

✔ Supports multiple prediction modes
✔ Works with trained checkpoints
✔ Enables real-time inference
✔ Useful for demos and applications

---

## 🧠 Summary

This module enables LuxNLP to perform **real-world NER predictions**, making it usable beyond training.
