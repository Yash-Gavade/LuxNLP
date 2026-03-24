# 🚀 LuxNLP RAG Module

### 🇱🇺 Retrieval-Augmented Generation for Luxembourgish NLP

---

## 🔗 Project Components

* 🖥️ **App (Hugging Face Space)**
  https://huggingface.co/spaces/YashGavade10/Lux_Nlp

* 🤖 **NER Model (XLM-R)**
  https://huggingface.co/YashGavade10/luxnlp-xlmr-ner

* 📊 **Dynamic Memory Dataset**
  https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory

---

# 🧠 1. Overview

The **LuxNLP RAG module** implements a hybrid pipeline that combines:

* Named Entity Recognition (NER)
* Retrieval over BIO-annotated datasets
* Dynamic memory storage
* Context-aware LLM generation

This system is designed for **low-resource Luxembourgish NLP**, where traditional large-scale datasets and models are limited.

Instead of relying purely on neural generation, the system introduces **retrieval-based grounding** to improve reliability, interpretability, and performance.

---

# 🎯 2. Core Idea

The key principle of this system is:

> **Use structured entity extraction to guide retrieval, and use retrieval to guide generation.**

This creates a pipeline where:

* NER extracts structured meaning
* Retrieval provides contextual evidence
* LLM generates grounded responses

---

# ⚙️ 3. High-Level Pipeline

```text
User Input
   ↓
NER (XLM-R)
   ↓
Entity Extraction
   ↓
Retrieval (Static + Dynamic)
   ↓
Context Construction
   ↓
LLM Generation (optional)
   ↓
Output + Memory Update
```

---

# 🧩 4. System Components

---

## 4.1 NER Layer (XLM-R)

The system uses a fine-tuned **XLM-RoBERTa model** for Luxembourgish NER.

### Responsibilities:

* Tokenization
* BIO tagging
* Entity span detection

### Supported Entities:

* PER (Person)
* LOC (Location)
* ORG (Organization)
* DATE
* EVENT
* MED
* PRODUCT

👉 This transforms raw text into structured semantic information.

---

## 4.2 Retrieval Layer

The retrieval module searches for similar examples in a BIO-tagged corpus.

### Retrieval Inputs:

* Original sentence
* Extracted entities
* Token patterns

### Retrieval Outputs:

* Similar sentences
* BIO labels
* Source metadata

---

### Types of Retrieval

#### 🔹 Static Retrieval

* Uses fixed dataset (`Lux_Final.conll`)
* No updates over time

#### 🔹 Dynamic Retrieval

* Uses memory dataset
* Includes newly stored examples
* Expands retrieval knowledge base

---

## 4.3 Context Construction

Retrieved examples are transformed into structured prompts.

### Context Includes:

* BIO-tagged examples
* Similar entity patterns
* Previous memory entries

👉 This step ensures the LLM receives **grounded input**, not raw queries.

---

## 4.4 Generation Layer (LLM)

An external LLM is optionally used to generate final responses.

### Behavior:

#### If LLM is available:

* Context + query → LLM → response

#### If LLM is NOT available:

* System falls back to:

  * NER output
  * retrieved examples

---

### Why LLM is optional:

* Ensures system works offline
* Maintains robustness
* Avoids dependency on API availability

---

# 🧠 5. Dynamic Memory (Key Innovation)

Dynamic memory allows the system to **store and reuse new examples**.

---

## Memory Flow

```text
New Input
   ↓
NER Output
   ↓
Create Structured Example
   ↓
Store in Memory Dataset
   ↓
Future Retrieval Uses It
```

---

## Dataset Structure

Each memory entry contains:

* tokens
* BIO tags
* full sentence
* source (`approved` or `memory`)

---

## Why Dynamic Memory Matters

* Expands dataset without retraining
* Improves retrieval quality over time
* Enables adaptive behavior
* Supports incremental learning (retrieval-level)


## RAG Pipeline

User Input
   ↓
Preprocessing
   ↓
NER (XLM-R)
   ↓
Entity Extraction
   ↓
Retrieval Query Construction
   ↓
Retrieve Top-k Contexts
   ↓
Context Formatting
   ↓
LLM Generation (if available)
   ↓
Final Output
   ↓
Memory Update (Dynamic RAG)

### ⚙️ Step-by-Step Working
#### 1. User Input

The pipeline starts when the user enters a Luxembourgish sentence.

Example:

Den Jean huet Paracetamol zu Esch kaf.

This is raw, unstructured input.

####  2. Preprocessing

Before passing to models:

normalize text
tokenize (or prepare for tokenizer)
handle punctuation / casing

👉 This ensures consistency for both:

NER model
retrieval module
####  3. NER (XLM-R)

The input is passed to your trained model:

👉 https://huggingface.co/YashGavade10/luxnlp-xlmr-ner

Output (BIO format):
Token	Label
Jean	B-PER
Paracetamol	B-MED
Esch	B-LOC
####  4. Entity Extraction

BIO tags are converted into structured entities:

PER → Jean
MED → Paracetamol
LOC → Esch

👉 This step is very important
Because:

Retrieval becomes entity-aware, not just text-based

####  5. Retrieval Query Construction

Now the system builds a retrieval query using:

original sentence
extracted entities
token structure
BIO pattern

👉 Example query representation:

Sentence: "Jean Paracetamol Esch"
Entities: [PER, MED, LOC]
####  6. Retrieval (Static + Dynamic)

The system searches:

base dataset (Lux_Final.conll)
memory dataset (dynamic)

👉 https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory

Retrieval returns:
similar sentences
BIO annotations
source (approved or memory)
Example retrieved result:
De Jean schafft zu Lëtzebuerg.
De Patient huet Paracetamol géint d’Féiwer geholl.
####  7. Context Construction

Retrieved examples are formatted into a prompt.

Example prompt:
Input:
Den Jean huet Paracetamol zu Esch kaf.

Examples:
1. De Jean schafft zu Lëtzebuerg. [PER, LOC]
2. De Patient huet Paracetamol geholl. [MED]

Task:
Identify entities and explain.

👉 This makes the LLM grounded.

####  8. LLM Generation

If LLM is active (from your Space):

✔ uses context + query
✔ generates response

From your debug:

LLM: llama-3.1-8b-instant
Provider: Groq
Two cases:
✅ Case 1: LLM available
context → LLM → natural output
❌ Case 2: LLM not available
fallback:
NER output
retrieved examples

👉 This is very important design choice

####  9. Final Output

The system returns:

NER labels
retrieved examples
generated explanation (if LLM active)
🧠 MEMORY FLOW (DETAILED)

Now let’s go deeper into your memory flow (this is your strongest part).

####  🔁 Memory Flow Diagram
New Input
   ↓
NER Output
   ↓
Structured Example Creation
   ↓
Validation / Filtering
   ↓
Store in Memory Dataset
   ↓
Future Retrieval Uses It

#### ⚙️ Step-by-Step Memory Logic
####  1. New Input

User enters a sentence.

#### 2. NER Output

System generates BIO tags.

####  3. Structured Example Creation

The system converts prediction into dataset format:

{
  "tokens": ["Den", "Jean", "huet", "Paracetamol"],
  "tags": ["O", "B-PER", "O", "B-MED"],
  "text": "Den Jean huet Paracetamol",
  "source": "memory"
}
#### 4. Validation (IMPORTANT)

Before storing:

check duplicates
check quality
optional filtering

👉 This prevents noise in memory

#### 5. Store in Dataset

Stored in:

👉 https://huggingface.co/datasets/YashGavade10/luxnlp-rag-memory

Now dataset contains:

source	meaning
approved	original curated data
memory	dynamically added
#### 6. Future Retrieval

Next time:

👉 retrieval includes memory entries

So system improves without retraining

---

⚠️ Important:

This is **not weight-based learning**.
The model does not update its parameters.

Instead:

> Learning happens through **memory expansion and retrieval improvement**.

---

# 🔗 6. System Integration

---

## 6.1 Space → Model

The Hugging Face Space:

* sends input to XLM-R model
* receives BIO predictions

---

## 6.2 Space → Dataset

The Space:

* retrieves context from dataset
* loads memory examples
* displays retrieved results

---

## 6.3 Space → LLM

The Space:

* sends prompt to LLM
* receives generated output

---

## 6.4 Memory → Dataset

Dynamic RAG:

* adds new examples
* updates dataset
* enables future reuse

---

# 📊 7. Evaluation

Stored in:

```text
metrics/metrics.json
```

### Metrics:

* Precision
* Recall
* F1-score

---

## Evaluation Scope:

* NER performance
* Retrieval quality
* RAG effectiveness

---

# 🧪 8. Application Features

The Hugging Face Space includes:

* Static RAG
* Dynamic RAG
* XLM-R prediction
* Model comparison
* Metrics visualization
* Case studies
* LLM debugging

---

# 📂 9. Folder Structure

```text
rag/
├── app/
│   └── app.py
│
├── core/
│   └── rag_pipeline.py
│
├── data/
│   └── Lux_Final.conll
│
├── memory/
│   └── rag_memory.jsonl
│
├── metrics/
│   └── metrics.json
│
├── README.md
└── requirements.txt
```

---

# ⚡ 10. Why This Approach Works

Traditional approaches:

| Method         | Limitation                  |
| -------------- | --------------------------- |
| NER only       | No contextual understanding |
| LLM only       | Hallucination risk          |
| Retrieval only | No generation               |

---

## LuxNLP Solution

| Component | Role                     |
| --------- | ------------------------ |
| NER       | Structured understanding |
| Retrieval | Evidence grounding       |
| Memory    | Adaptive knowledge       |
| LLM       | Fluent generation        |

---

# ⚠️ 11. Limitations

* Limited Luxembourgish data
* Small retrieval corpus
* Basic retrieval (can improve with embeddings)
* Memory quality depends on inputs
* No automatic retraining loop

---

# 🚀 12. Future Work

* Dense vector retrieval (FAISS, embeddings)
* Better ranking using entity similarity
* Automated memory validation
* Continuous retraining loop
* Explainable retrieval

---

# 👤 13. Author

**Yash Gavade**
M.Sc. NLP
Universität Trier

---

# 🧠 14. Final Summary

LuxNLP RAG is a **hybrid NLP system** that connects:

* Transformer-based NER
* Retrieval over structured datasets
* Dynamic memory expansion
* Optional LLM-based generation

👉 In simple terms:

> **NER finds entities → retrieval finds evidence → memory stores knowledge → LLM generates grounded output**

---

This makes LuxNLP a **robust, explainable, and adaptive RAG system for low-resource languages**.
