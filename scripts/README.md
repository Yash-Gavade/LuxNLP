# 📂 Scripts Module

This directory contains all core processing, modeling, and analysis scripts used in the **LuxNLP pipeline**.

The scripts are organized into modular components to reflect the complete workflow of the project, from raw data extraction to model training, evaluation, and analysis.

---

## 🧩 Structure Overview

The `scripts/` folder is divided into the following submodules:

### 🔍 1. Analysis

Contains scripts for:

* Debugging model outputs and datasets
* Computing evaluation metrics (span-level, token-level)
* Generating reports and exporting results
* Visualizing performance (F1 scores, distributions, training curves)

👉 Used for **evaluation, diagnostics, and result interpretation**

---

### 🌐 2. data_extraction

Handles data collection and preprocessing from external sources:

* **LOD.lu extraction** (lexicons, translations, categories)
* **Wikidata scraping** (entities like PER, LOC, ORG, DATE, etc.)
* Conversion of raw data into **CoNLL format**
* Cleaning and normalization of extracted text

👉 Forms the **foundation of dataset construction**

---

### 🏗️ 3. dataset_creation

Responsible for building the final NER dataset:

* Cleaning and filtering datasets
* Merging multiple sources (LOD, Wikidata, Leipzig, etc.)
* Converting formats (e.g., survey → CoNLL)
* Adding annotations and entity labels
* Splitting into **train / dev / test sets**

👉 Produces the final dataset: `Lux_Final.conll`

---

### 🤖 4. model

Contains all model-related scripts:

* **Training**: Fine-tuning XLM-R for Luxembourgish NER
* **Evaluation**: Computing precision, recall, F1 scores
* **Prediction**: Running inference on text or datasets

👉 Core module for **machine learning experiments and results**

---

## 🔄 Pipeline Flow

The scripts follow a structured pipeline:

```text
data_extraction → dataset_creation → model → analysis
```

1. Extract and preprocess raw data
2. Construct structured NER dataset (CoNLL format)
3. Train and evaluate NER models (XLM-R)
4. Analyze results and generate reports/visualizations

---

## ⚙️ Usage

Each submodule can be executed independently depending on the task.

Example:

```bash
# Train model
python scripts/model/training/train_xlmr.py

# Evaluate model
python scripts/model/evaluation/eval_xlmr.py

# Run prediction
python scripts/model/prediction/predict.py
```

---

## 🧠 Notes

* Scripts are modular and can be reused independently
* Naming is kept consistent across modules (`train`, `eval`, `predict`)
* Intermediate outputs (datasets, metrics, plots) are stored separately

---

## 📌 Summary

The `scripts/` directory represents the **complete LuxNLP pipeline implementation**, covering:

✔ Data engineering
✔ Dataset construction
✔ Model training and evaluation
✔ Performance analysis and visualization

---

This modular design ensures clarity, scalability, and reproducibility of the LuxNLP project.

