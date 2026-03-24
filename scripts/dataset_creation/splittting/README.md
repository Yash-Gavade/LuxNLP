# ✂️ Splitting Module

The `splitting/` directory contains scripts for dividing the dataset into **training, validation, and test sets**.

Proper splitting is essential for **fair evaluation and preventing data leakage**.

---

## 🎯 Purpose

* Create train/dev/test splits
* Maintain balanced distribution of entities
* Ensure reproducibility of experiments

---

## 📂 Files Overview

### `split_conll_70_15_15.py`

Splits dataset into:

* 70% training
* 15% validation
* 15% test

👉 Standard split for model training.

---

### `updated_split_conll.py`

Implements updated or customized splitting strategies.

👉 Useful for:

* Adjusting dataset distribution
* Handling special cases

---

## 🔄 Role in Pipeline

```text
Final Dataset → Splitting → Train / Dev / Test → Model Training
```

---

## ⚙️ Example Usage

```bash
python scripts/dataset_creation/splitting/split_conll_70_15_15.py
```

---

## 🧠 Summary

✔ Creates structured dataset splits
✔ Prevents data leakage
✔ Enables fair model evaluation

---

This module ensures that LuxNLP experiments are **valid, reproducible, and reliable**.
