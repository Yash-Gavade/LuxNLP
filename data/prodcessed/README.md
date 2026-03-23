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

## 🏗️ Dataset Construction Process  

The final dataset (**Lux_Final.conll**) is created through a combination of **data collection, extraction, annotation, and synthetic data generation** to address the low-resource nature of Luxembourgish.

---

### 🔹 1. Lexical & Knowledge-Based Extraction  

- **LOD.lu** was used as a primary source of structured entity information  
- Existing entries (e.g., names of locations, organizations, products) were extracted  
- Example sentences from LOD were converted into CoNLL format  

👉 These sources provided **high-quality entity seeds**  

---

### 🔹 2. Wikidata-Based Entity Expansion  

- Additional entities were extracted using **Wikidata**  
- These were mapped to Luxembourgish contexts where possible  
- Used to increase coverage of:
  - ORG  
  - LOC  
  - PER  
  - PRODUCT  

---

### 🔹 3. Real Text Collection  

Luxembourgish text was collected from multiple sources:

- RTL news articles  
- Leipzig Corpora  
- LOD example sentences  
- Additional curated Luxembourgish text  

👉 These sentences provided **natural linguistic context**  

---

### 🔹 4. Gazetteer-Based Weak Supervision  

- Extracted entities (from LOD + Wikidata) were used as **gazetteers**  
- These were matched against collected sentences  
- Automatic tagging was applied where matches were found  

👉 This step enabled **semi-automatic annotation**  

---

### 🔹 5. Synthetic Data Generation (IMPORTANT)  

To improve entity learning and address data scarcity, **synthetic sentences were generated using templates**.

### How it works:
- Sentence templates were created with **fixed structure + variable entity slots**
- One or more placeholders were replaced with real entities from gazetteers  

👉 This helps the model:
- Learn entity patterns  
- Improve generalization  
- Handle rare entity types  

---

### ✨ Example of Synthetic Data  

#### Template:
Ech hunn [PRODUCT] zu [LOC] kaaft.

#### Filled Samples:
Ech hunn Paracetamol zu Lëtzebuerg kaaft.  
Ech hunn iPhone zu Esch-sur-Alzette kaaft.  

#### Converted to CoNLL:
Ech           O  
hunn          O  
Paracetamol   B-PRODUCT  
zu            O  
Lëtzebuerg    B-LOC  
kaaft         O  
.             O  

---

### 🔹 6. Cleaning & Filtering  

- Removal of noisy or incorrect annotations  
- Deduplication of sentences  
- Manual inspection of critical samples  

---

### 🔹 7. Final Dataset Preparation  

- All data merged into Lux_Final.conll  
- Converted into BIO tagging format  
- Split into:
  - Train  
  - Dev  
  - Test  

👉 Ensures:

- No data leakage  
- Balanced distribution  
- Proper evaluation setup  


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
