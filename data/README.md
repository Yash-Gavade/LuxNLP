# 📂 LuxNLP Dataset  

This directory contains all datasets used in the **LuxNLP project**, organized into different stages of the data pipeline.

---

## 📁 Structure  

```
data/
├── raw/        → original collected data  
├── cleaned/    → cleaned and filtered data  
├── processed/  → final model-ready datasets  
```

---

## 🔹 raw/  

This folder contains the **original datasets** collected from various sources.

### Sources include:
- LOD.lu  
- Leipzig Corpora  
- News articles and web text  

### Characteristics:
- Unprocessed and noisy  
- May contain inconsistencies  
- Used as the starting point of the pipeline  

---

## 🔹 cleaned/  

This folder contains **cleaned and normalized datasets**.

### Processing steps:
- Removal of noise and invalid entries  
- Text normalization  
- Filtering irrelevant or corrupted data  

### Purpose:
- Improve data quality  
- Prepare for annotation and structuring  

---

## 🔹 processed/  

This folder contains **final datasets used for model training**.

### Includes:
- Structured format (e.g., CoNLL)  
- Annotated entities (e.g., PER, LOC, ORG, DATE, etc.)  
- Balanced and curated samples  

### Purpose:
- Direct input for NER models  
- Evaluation and benchmarking  

---

## 🔄 Data Pipeline  

The overall workflow is:

```
raw → cleaned → processed
```

1. Raw data is collected  
2. Cleaning removes noise and standardizes text  
3. Processed data is structured and annotated  

---

## 🎯 Purpose  

The dataset is designed to support:

- Named Entity Recognition (NER)  
- Low-resource NLP research  
- Dataset-centric experimentation  
- Model training and evaluation  

---

## ⚠️ Notes  

- Raw data may contain inconsistencies and should not be used directly for training  
- Processed data is optimized for model performance  
- Large datasets may be partially included due to repository size limits  

---

## 🔬 Reproducibility  

To regenerate processed datasets, refer to:

- `src/preprocessing/`  
- `scripts/` pipeline  

---

## 📄 Related  

- Models → `models/`  
- Results → `results/`  
- Notebooks → `notebooks/`  
- Paper → `paper/`  
