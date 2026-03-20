# LuxNLP Processed Dataset

This folder contains the **final processed datasets** used for training the Luxembourgish Named Entity Recognition (NER) model in the LuxNLP project.

## 📂 Files Overview

### 🔹 Main Dataset

* **Lux_Final.conll**
  Final combined dataset used for training.
  Contains BIO-tagged annotations for:

  * MED (Medical)
  * ORG (Organization)
  * LOC (Location)
  * EVENT
  * PRODUCT
  * DATE
  * PER (Person)

### 🔹 Source-based Datasets

* **lod_lu.conll**
  Raw lexicon-based dataset extracted from LOD.lu.

* **Lod_lu_sentences.conll**
  Example sentences extracted from LOD and converted into CoNLL format.

* **wikidata.conll**
  Additional dataset created using Wikidata-based entity extraction.

* **All_Extracted_Sentences.txt**
  Collection of all extracted Luxembourgish sentences from multiple sources:

  * RTL news data
  * LOD.lu example sentences
  * Wikidata-based sentences
  * Additional generated and curated sentences

  These sentences are collected before tokenization and BIO tagging.

---

## 📁 Model Training Data (`model_data/`)

This subfolder contains the **final dataset splits used for model training and evaluation**.

* **train.conll** → Training dataset
* **dev.conll** → Validation dataset
* **test.conll** → Test dataset

### ✔ Properties

* Cleaned and deduplicated
* No overlap between splits (no data leakage)
* Balanced and structured for NER training
* Derived from the final processed dataset

---

## 🧠 Dataset Description

The final dataset (**Lux_Final.conll**) is created by combining:

* LOD-based lexical and example sentence extraction
* Wikidata-based entity data
* RTL/news-style sentences
* Additional manually curated and generated sentences
* Cleaning and semantic filtering steps

All data is converted into **CoNLL BIO format**, where:

* `B-XXX` → Beginning of entity
* `I-XXX` → Inside entity
* `O` → Outside entity

---

## 🎯 Purpose

This dataset is designed for:

* Training NER models (XLM-R)
* Evaluation using proper train/dev/test splits
* Research on Luxembourgish low-resource NLP

---

## ⚙️ Format Example

```text
Aarbechtsdokter    B-MED
huet               O
mir                O
gehollef           O
.                  O
```

---

## 🚀 Usage

* Use **Lux_Final.conll** for full dataset experiments
* Use **model_data/train/dev/test.conll** for proper training and evaluation

---

*Note:  Minor noise may still exist.*
