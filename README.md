# 🧠 LuxNLP: Luxembourgish Named Entity Recognition

This project presents a **data-centric approach to Named Entity Recognition (NER)** for Luxembourgish, a low-resource language.

We construct a custom dataset from multiple sources and compare two approaches:

- 🔹 Fine-tuned **XLM-RoBERTa**
- 🔹 **Retrieval-Augmented Generation (RAG)** with LLMs

The goal is to evaluate performance under both:
- Standard test data
- Noisy real-world (survey) data

👉 The project focuses on building a complete end-to-end NER pipeline, including dataset creation, model training, and evaluation, highlighting how data quality and structure impact model performance in low-resource settings.


## 📊 Dataset

The **LuxNLP dataset (~61,000 sentences)** was constructed using:

- RTL news data  
- Leipzig corpora  
- LOD.lu (Luxembourgish Online Dictionary)  
- Wikidata  
- Synthetic template-based generation  

All data is annotated in **BIO (CoNLL) format**.

📁 Dataset location:
data/processed/model_data/

### 🔹 Data Split
- Train / Dev / Test split applied  
- Used for both XLM-R training and RAG retrieval  

---

## 🔄 Pipeline Overview

1. Data Collection (RTL, LOD.lu, Wikidata, Leipzig)
2. Weak Supervision (gazetteers + matching)
3. Data Cleaning & Deduplication
4. BIO Annotation (CoNLL format)
5. Model Training (XLM-R)
6. RAG Retrieval + Prompt Construction
7. Evaluation (test set + survey data)

---

## 🤖 Models

### 🔹 XLM-RoBERTa
- Base model: `xlm-roberta-base`
- Fine-tuned for token classification (NER)
- Strong baseline for low-resource languages

### 🔹 RAG + LLM
- Retrieves similar BIO-tagged examples
- Constructs few-shot prompts
- Uses LLM (via Groq API) for prediction
- Supports dynamic memory for improvement

---

## 📈 Results

| Dataset        | Method        | Precision | Recall | F1 Score |
|---------------|--------------|----------|--------|---------|
| Main Test     | XLM-R        | 0.8735   | 0.7756 | 0.8216  |
| Main Test     | RAG + LLM    | 0.2332   | 0.6104 | 0.3375  |
| Survey Data   | XLM-R        | 0.3607   | 0.1376 | 0.1992  |
| Survey Data   | RAG + LLM    | 0.0769   | 0.0035 | 0.0067  |

### 🔍 Key Insights

- **XLM-RoBERTa** provides stable and reliable predictions with high precision and balanced recall on the main test set.
- **RAG + LLM** achieves higher recall but suffers from very low precision due to over-generation of entities.

### 📉 Performance on Survey Data

Performance on the survey dataset is significantly lower for both approaches. This is expected due to the nature of the data:

- The survey data is **noisy, small-scale, and less structured**, unlike the training corpus.
- It contains **informal language, variability in expression, and inconsistent patterns**, which are difficult for models to generalize.
- There is also a **distribution shift**, as the survey data does not follow the same characteristics as the training data.

As a result:
- XLM-R struggles due to **limited exposure to such variations during training**
- RAG + LLM performs poorly due to **lack of reliable contextual matches and unstable predictions**

👉 Overall, this highlights the importance of **data quality, consistency, and domain alignment** in low-resource NLP settings.


## 📦 Trained Models

The trained XLM-R model is not included in this repository due to size limitations.

### 📥 Access

- 🔗 Hugging Face: https://huggingface.co/YashGavade10/luxnlp-xlmr-ner  
- 🔗 Google Drive: https://drive.google.com/drive/folders/1thHqVy1gYxhg3JmmcSKk4LLO7EPwq_rK?usp=drive_link  

---

## 🚀 Reproduction

### 1. Install dependencies
pip install -r requirements.txt

### 2. Train model
python/scripts/model/training/train_xlmr_ner.py

### 3. Evaluate
python scripts/model/evaluation/eval_xlmr.py

---

## 📂 Project Structure

data/
 └── processed/
      └── model_data/

models/
 └── xlmr/

scripts/
 ├── training
 ├── evaluation
 ├── rag_pipeline

results/
 ├── metrics
 ├── predictions
 ├── figures

rag/
 

---

## 🧪 Evaluation Strategy

- Entity-level Precision, Recall, F1
- Per-class analysis
- Confusion matrix analysis
- Evaluation on:
  - Standard test set
  - Survey (out-of-distribution data)

---

## 📌 Notes

- Due to GitHub size limits, model weights are stored externally
- Dataset is fully available in this repository
- All experiments are reproducible via provided scripts

---

## 📎 Repository

https://github.com/Yash-Gavade/LuxNLP

## 🔗 Hugging Face

* 🖥️ **App (Hugging Face Space)**
  https://huggingface.co/spaces/YashGavade10/Lux_Nlp

* 🤖 **NER Model (XLM-R)**
  https://huggingface.co/YashGavade10/luxnlp-xlmr-ner

* 📊 **Dynamic Memory Dataset**
  https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory

---

---

## 👨‍💻 Authors

- Yash Gavade 

---

## ⭐ Final Remark

This project demonstrates that **data-centric approaches combined with modern NLP techniques** can effectively build NER systems for low-resource languages like Luxembourgish.
