
# LuxNLP Processed Dataset

This folder contains the **final processed datasets** used for training the Luxembourgish Named Entity Recognition (NER) model in the LuxNLP project.

## 📂 Files Overview

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

* **lod_lu.conll**
  Raw lexicon-based dataset extracted from LOD.lu.

* **Lod_lu_sentences.conll**
  Example sentences extracted from LOD and converted into CoNLL format.

* **wikidata.conll**
  Additional dataset created using Wikidata-based entity extraction.

* **All_Extracted_Sentences.txt**

Collection of all extracted Luxembourgish sentences from multiple sources, including:
-RTL news data
-LOD.lu example sentences
-Wikidata-based sentences

Additional generated and curated sentences
These sentences are collected before tokenization and BIO tagging.

## 🧠 Dataset Description

The final dataset (**Lux_Final.conll**) is created by combining:

* LOD-based lexical and example sentence extraction
* Wikidata-based entity data
* Additional manually curated and generated sentences
* Cleaning and semantic filtering steps

All data is converted into **CoNLL BIO format**, where:

* `B-XXX` → Beginning of entity
* `I-XXX` → Inside entity
* `O` → Outside entity

## 🎯 Purpose

This dataset is designed for:

* Training NER models (XLM-R)

## ⚙️ Format Example

```text
Aarbechtsdokter    B-MED
huet               O
mir                O
gehollef           O
.                  O
```

## 🚀 Usage

**Lux_Final.conll** was directly for training NER model.

---
