# Results

This directory contains the final evaluation outputs and prediction files for the LuxNLP Named Entity Recognition (NER) project. The results compare a fine-tuned XLM-RoBERTa model with a Retrieval-Augmented Generation (RAG) approach using Groq.

---

## Directory Structure

```
results/
├── metrics/
├── predictions/
├── figures/   
```

---

## Metrics

The `metrics/` folder contains evaluation summaries computed using gold-labeled CoNLL data.

### Files

* `xlmr_test_results.txt`
  → XLM-RoBERTa performance on the main test set

* `groq_rag_test_results.txt`
  → RAG (Groq) performance on the main test set

* `xlmr_survey_results.txt`
  → XLM-RoBERTa performance on the external survey dataset

* `xlmr_survey_results_filtered.txt`
  → Filtered XLM-RoBERTa results on the survey dataset

* `groq_rag_survey_results.txt`
  → RAG (Groq) performance on the survey dataset

---

## Predictions

The `predictions/` folder contains token-level BIO predictions in CoNLL format.

These files are used for evaluation, error analysis, and comparison between approaches.

### Files

* `test_predictions.conll`
  → XLM-RoBERTa predictions for the main test set

* `groq_rag_test_predictions.conll`
  → RAG predictions for the main test set

* `xlmr_survey_predictions_filtered.conll`
  → Filtered XLM-RoBERTa predictions on the survey dataset

* `groq_rag_survey_predictions.conll`
  → RAG predictions on the survey dataset

---

## Final Evaluation Summary

| Evaluation Set | Method                 | Precision | Recall | F1 Score |
| -------------- | ---------------------- | --------- | ------ | -------- |
| Main Test Set  | XLM-RoBERTa            | 0.8735    | 0.7756 | 0.8216   |
| Main Test Set  | Groq RAG               | 0.2332    | 0.6104 | 0.3375   |
| Survey Set     | XLM-RoBERTa            | 0.3607    | 0.1376 | 0.1992   |
| Survey Set     | XLM-RoBERTa (Filtered) | 0.3780    | 0.1376 | 0.2018   |
| Survey Set     | Groq RAG               | 0.0769    | 0.0035 | 0.0067   |

---

## Key Observations

* XLM-RoBERTa achieves the best overall performance with a strong balance between precision and recall.
* The RAG-based approach shows higher recall in the main test set but suffers from very low precision due to over-prediction of entities.
* On the survey dataset, both approaches show performance degradation due to domain mismatch.
* The RAG model performs particularly poorly on unseen survey data, indicating limited generalization capability.
* Filtering slightly improves XLM-RoBERTa precision but does not significantly affect recall.

---

## Notes

* The main test set is derived from the original training data distribution.
* The survey dataset is an external dataset and is **not used during training**, making it suitable for evaluating generalization.
* All metrics are computed using standard CoNLL evaluation (entity-level precision, recall, and F1 score).
* Accuracy is not reported as a primary metric due to class imbalance in NER tasks (dominance of the "O" label).

---

## Visualizations 

The `figures/` folder will include:

* Model comparison bar charts (Precision / Recall / F1)
* Confusion matrices for XLM-RoBERTa and RAG
* Additional performance visualizations

---

## Reproducibility

All results are generated using prediction files in the `predictions/` folder and evaluated against gold-labeled datasets using standard evaluation scripts.

---

## Conclusion

The results demonstrate that fine-tuned transformer-based models (XLM-RoBERTa) are significantly more reliable for structured NER tasks compared to retrieval-based approaches. While RAG provides contextual support, it lacks precision and consistency, especially in domain-shift scenarios.

