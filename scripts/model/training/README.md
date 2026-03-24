# 🏋️ Training Module

The `training/` directory contains scripts for fine-tuning the **XLM-RoBERTa model** on the Luxembourgish NER dataset.

---

## 🎯 Purpose

* Train the NER model on labeled CoNLL datasets
* Fine-tune pretrained transformer weights
* Save checkpoints for later use

---

## 📂 Files Overview

### `train_xlmr.py`

The main training script.

---

## ⚙️ Functionality

* Loads CoNLL formatted dataset
* Tokenizes input using XLM-R tokenizer
* Aligns labels with subword tokens
* Trains model using HuggingFace Trainer API
* Saves:

  * Model checkpoints
  * Training logs
  * Configuration files

---

## 🔄 Training Pipeline

```text
CoNLL Dataset → Tokenization → Label Alignment → Training → Checkpoints
```

---

## ⚙️ Example Usage

```bash
python scripts/model/training/train_xlmr.py \
    --train_file data/train.conll \
    --dev_file data/dev.conll \
    --output_dir model_output/
```

---

## 🧠 Key Features

✔ Supports BIO tagging
✔ Handles subword token alignment
✔ Saves intermediate checkpoints
✔ Compatible with HuggingFace ecosystem

---

## 📊 Output

* `pytorch_model.bin` → trained weights
* `config.json` → model config
* `trainer_state.json` → training logs

---

## 🧠 Summary

This module transforms annotated datasets into a **trained NER model capable of real-world predictions**.
