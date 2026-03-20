
# LuxNLP Model Data

This folder contains the **final dataset splits** used for training and evaluating the Luxembourgish Named Entity Recognition (NER) model.

## 📂 Files Overview

* **train.conll**
  Training dataset used to train the NER model.

* **dev.conll**
  Validation dataset used for tuning and model selection.

* **test.conll**
  Test dataset used for final evaluation.

## 🧠 Dataset Details

* Format: CoNLL (BIO tagging scheme)
* Language: Luxembourgish
* Entity types:

  * MED (Medical)
  * ORG (Organization)
  * LOC (Location)
  * EVENT
  * PRODUCT
  * DATE
  * PER (Person)

## ⚙️ Format Example

```text
Aarbechtsdokter    B-MED
huet               O
mir                O
gehollef           O
.                  O
```

## 🎯 Purpose

These splits are designed to:

* Train the NER model (`train.conll`)
* Validate model performance during training (`dev.conll`)
* Evaluate final model performance (`test.conll`)

All splits are:

* Cleaned and deduplicated
* Free from overlap (no data leakage)
* Properly structured for machine learning training

## 🚀 Usage

These files can be directly used for training NER models such as:

* XLM-RoBERTa


---

*Note: Minor noise may still exist.*
