# 📊 Analysis Module

The `Analysis/` directory contains all scripts related to **evaluation, debugging, reporting, and visualization** of the LuxNLP pipeline.

This module is used after model training to **analyze dataset quality, model performance, and prediction behavior**.

---

## 🧩 Submodules

### 🐞 debugging

Scripts for inspecting and diagnosing issues in datasets and model predictions.

**Includes:**

* Comparing **gold vs predicted labels**
* Inspecting NER outputs (CSV/CoNLL)
* Checking dataset statistics and anomalies

👉 Helps identify errors such as:

* Mislabelled entities
* Class imbalance
* Prediction inconsistencies

---

### 📏 metrics

Scripts for computing evaluation metrics.

**Includes:**

* **Token-level evaluation**
* **Span-level evaluation**

👉 Outputs:

* Precision
* Recall
* F1-score

These metrics are essential for evaluating **NER model performance**.

---

### 📝 reporting

Scripts for exporting results and generating structured reports.

**Includes:**

* Exporting evaluation tables (CSV/JSON)
* Saving dataset statistics
* Logging training configurations
* Generating model performance summaries

👉 Used for:

* Research reporting
* Paper results
* Reproducibility

---

### 📈 visualization

Scripts for generating plots and visual insights.

**Includes:**

* Entity/class distribution plots
* Dataset distribution analysis
* F1-score comparison charts
* Training curves

👉 Helps in:

* Understanding dataset structure
* Comparing model performance
* Presenting results visually

---

## 🔄 Role in Pipeline

This module is used in the final stages of the LuxNLP workflow:

```text
Model Training → Evaluation → Analysis → Reporting
```

It transforms raw outputs into **interpretable insights and visualizations**.

---

## ⚙️ Example Usage

```bash
# Compute evaluation metrics
python scripts/Analysis/metrics/eval_conll_tokens.py

# Debug predictions
python scripts/Analysis/debugging/debug_gold_vs_pred.py

# Generate plots
python scripts/Analysis/visualization/plot_f1.py
```

---

## 🧠 Summary

The `Analysis/` module enables:

✔ Detailed performance evaluation
✔ Debugging of model predictions
✔ Generation of reports for research
✔ Visualization of results

---

This module ensures that the LuxNLP system is **transparent, interpretable, and evaluation-driven**.
