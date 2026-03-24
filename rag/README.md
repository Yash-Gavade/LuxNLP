---
title: LuxNLP RAG 
emoji: 🚀
colorFrom: indigo
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
sdk_version: 6.9.0
---
# 🇱🇺 LuxNLP – Luxembourgish NER + Retrieval-Augmented Generation (RAG)

> 🧠 Low-Resource NLP System for Luxembourgish  
> 🔍 Entity-Aware Retrieval + Contextual Generation  
> 🚀 Interactive Hugging Face Space  

---

## 📌 Overview  

LuxNLP is a hybrid NLP system combining Named Entity Recognition (NER) with a Retrieval-Augmented Generation (RAG) pipeline to improve understanding and response generation for Luxembourgish.

Designed for low-resource settings, it leverages custom datasets, weak supervision, and entity-guided retrieval.

---

## 🧠 System Architecture  

Input → Tokenization → NER (XLM-R) → Entity Extraction → Retrieval → Context Injection → Generation  

---

## 🔍 Core Components  

### 1. Named Entity Recognition (NER)
- Model: XLM-RoBERTa  
- BIO tagging (B/I/O)  
- Entities: PER, LOC, ORG, DATE, PRODUCT, EVENT, MED  

---

### 2. Dataset (Lux_Final.conll)
Built using:
- LOD.lu → MED, EVENT, PRODUCT  
- Wikidata → PER, LOC, ORG, DATE  
- RTL + Leipzig → real text  
- Gazetteers → weak supervision  
- Synthetic templates → augmentation  

---

### 3. Retrieval Module  
- Uses extracted entities as query signals  
- Matches against dataset/text corpus  
- Retrieves relevant context  

---

### 4. Dynamic RAG Pipeline  

User Query  
↓  
NER → Entities  
↓  
Retrieve Context  
↓  
Inject into Prompt  
↓  
Generate Response  

---

### 5. Generation  
- Combines query + retrieved context  
- Produces grounded responses  

---

## 📂 Files  

- app.py → UI  
- dynamic_rag_luxnlp.py → RAG logic  
- Lux_Final.conll → dataset  
- metrics.json → evaluation  
- requirements.txt → dependencies  

---

## ⚙️ Workflow  

1. Input processing  
2. NER inference  
3. Entity extraction  
4. Retrieval  
5. Context construction  
6. Response generation  

---

## 📊 Evaluation  

Metrics:
- Precision  
- Recall  
- F1-score  

See metrics.json  

---

## 🚀 Why NER + RAG?  

- Improves context understanding  
- Reduces hallucination  
- Enhances entity grounding  

---

## ⚠️ Limitations  

- Low-resource constraints  
- Limited dataset  
- Lightweight retrieval  

---

## 👤 Author  

Yash Gavade  
M.Sc. NLP – Universität Trier  

---

## 🌟 Demo  

Use this Hugging Face Space to test Luxembourgish NER + RAG system