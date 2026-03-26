# Metrics

This folder contains the final evaluation results for the LuxNLP Named Entity Recognition (NER) project.

All metrics are computed using gold-labeled CoNLL format and standard evaluation scripts, reporting **precision, recall, and F1 score**.

---

## Files

### Main Test Set

* **`xlmr_test_results.txt`**
  Results of the fine-tuned XLM-RoBERTa model on the main test dataset.
  This represents performance on data with a similar distribution to the training set.

* **`groq_rag_test_results.txt`**
  Results of the Groq-based RAG approach on the main test dataset.
  Used for comparison with the supervised XLM-R model.

---

### Survey Dataset (External Evaluation)

* **`xlmr_survey_results.txt`**
  XLM-RoBERTa performance on the external survey dataset.
  This dataset is not part of training and is used to evaluate generalization.

* **`xlmr_survey_results_filtered.txt`**
  Filtered version of XLM-RoBERTa results on the survey dataset.
  Filtering is applied to slightly improve precision and reduce noise.

* **`groq_rag_survey_results.txt`**
  RAG model performance on the survey dataset.
  Shows behavior under domain shift and limited generalization.

---

## Key Observations

* XLM-RoBERTa achieves strong and balanced performance on the main test set.
* The RAG approach shows higher recall but significantly lower precision due to over-prediction.
* Both models experience performance drops on the survey dataset due to domain mismatch.
* Filtering improves XLM-R precision slightly but does not significantly increase recall.

---

## Important Note

* The **main test set** follows the original dataset distribution.
* The **survey dataset** is external and not used during training.
* This allows evaluation of real-world generalization performance.

---

## Metric Details

* **Precision** → How many predicted entities are correct
* **Recall** → How many true entities are recovered
* **F1 Score** → Harmonic mean of precision and recall

Accuracy is not reported as a primary metric due to class imbalance in NER tasks, where most tokens belong to the non-entity ("O") class.

---

## Usage

These files can be used for:

* Model comparison (XLM-R vs RAG)
* Paper results and reporting
* Error analysis and evaluation
* Visualization (bar charts, confusion matrices)

---

## Summary

This folder provides the core quantitative evidence supporting the comparison between supervised (XLM-RoBERTa) and retrieval-based (RAG) approaches for Luxembourgish NER.
