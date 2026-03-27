# 🚀 LuxNLP: RAG + XLM-R NER System

## 🔗 Project Links

- 🤗 **Live Demo (Hugging Face Space)**  
  https://huggingface.co/spaces/YashGavade10/Lux_Nlp  

- 🧠 **Trained XLM-R Model**  
  https://huggingface.co/YashGavade10/luxnlp-xlmr-ner  

- 📚 **RAG Memory Dataset**  
  https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory  

---

## 📌 Project Overview

LuxNLP is a **Named Entity Recognition (NER)** system for **Luxembourgish**, a low-resource language.

This project combines:
- Fine-tuned **XLM-RoBERTa (Transformer-based model)**
- **Retrieval-Augmented Generation (RAG)**
- Static and Dynamic retrieval strategies
- Real-time comparison between approaches

The goal is to analyze how **structured models (XLM-R)** and **retrieval-based methods (RAG + LLM)** behave under different conditions.

---

## 🖥️ Hugging Face Demo

The system is deployed as an interactive web application using Hugging Face Spaces.

👉 You can test the system here:  
https://huggingface.co/spaces/YashGavade10/Lux_Nlp  

---

## 🧾 Screenshots from Working System

> ⚠️ **Note:**  
> All images in this repository are **real screenshots taken from the working Hugging Face application**, demonstrating the actual system behavior, interface, and outputs.

### 🔹 Features Demonstrated in Screenshots
- Static RAG retrieval results  
- Dynamic RAG with memory updates  
- XLM-R NER predictions  
- Side-by-side comparison  
- LLM debug outputs  
- Evaluation metrics  

These screenshots serve as **proof of implementation and working pipeline**.

---

## ⚙️ System Architecture

### 🔁 Pipeline

1. Input Luxembourgish sentence  
2. Generate embeddings  
3. Retrieve top-k similar examples  
4. Construct prompt (RAG)  
5. Run LLM (optional)  
6. Run XLM-R model  
7. Display results and comparison  

---

## 🧠 Model Details

### 🔹 XLM-RoBERTa NER
- Fine-tuned on custom dataset  
- BIO tagging format  
- Supports 7 entity types:
  - `PER`, `LOC`, `ORG`, `MED`, `EVENT`, `PRODUCT`, `DATE`

👉 Model:  
https://huggingface.co/YashGavade10/luxnlp-xlmr-ner  

---

## 📚 Dataset

### 🔹 Data Sources
- RTL News  
- LOD.lu  
- Wikidata  
- Synthetic generated data  

### 🔹 RAG Memory
- Stores retrieved examples  
- Enables dynamic improvement  

👉 Dataset:  
https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory  

---

## 📊 Evaluation Results

| Dataset        | Method        | Precision | Recall | F1 Score |
|---------------|--------------|----------|--------|---------|
| Main Test     | XLM-R        | 0.8735   | 0.7756 | 0.8216  |
| Main Test     | RAG + LLM    | 0.2332   | 0.6104 | 0.3375  |
| Survey Data   | XLM-R        | 0.3607   | 0.1376 | 0.1992  |
| Survey Data   | RAG + LLM    | 0.0769   | 0.0035 | 0.0067  |

---

## 🔍 Key Observations

- **XLM-RoBERTa**
  - High precision  
  - Stable performance  
  - Reliable predictions  

- **RAG + LLM**
  - Higher recall  
  - Low precision  
  - Tends to over-predict entities  

- **Survey Dataset**
  - Noisy and domain-shifted  
  - Fewer entity types  
  - Causes performance drop  

---

## ⚠️ Important Notes

- Test set → similar to training distribution  
- Survey data → independent, noisy, limited  

➡️ This explains why performance drops significantly on survey data.

---

## 🚀 How to Use

1. Open the Hugging Face Space  
2. Enter a Luxembourgish sentence  
3. Select mode:
   - Static RAG  
   - Dynamic RAG  
   - XLM-R  
   - Compare  
4. Run and analyze output  

---

## 🔧 Technologies Used

- Python  
- Hugging Face Transformers  
- XLM-RoBERTa  
- Sentence Transformers / TF-IDF (fallback)  
- Gradio (UI)  
- Groq API (LLM integration)  

---

## 📌 Future Work

- Improve retrieval quality  
- Expand dataset  
- Reduce RAG over-prediction  
- Fine-tune LLM for NER tasks  

---

## 👨‍💻 Author

**Yash Gavade**  
LuxNLP Project – ML4NLU  

---

## ⭐ Final Statement

This project demonstrates that:

> Transformer-based models provide stability, while RAG-based systems offer flexibility — but combining both requires careful design, especially in low-resource scenarios.
