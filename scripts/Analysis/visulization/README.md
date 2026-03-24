# 📈 Visualization Module

The `visualization/` directory contains scripts for generating **plots and visual insights** from the LuxNLP pipeline.

This module helps transform raw metrics and dataset statistics into **interpretable visual representations**, making it easier to analyze model performance and dataset characteristics.

---

## 🎯 Purpose

The visualization module is used to:

* Understand dataset structure and distribution
* Analyze model performance visually
* Compare results across experiments
* Create figures for reports and research papers

👉 It plays a key role in making results **intuitive and presentation-ready**.

---

## 📂 Files Overview

### `plot_class_distribution.py`

Visualizes the distribution of entity classes.

**Shows:**

* Frequency of labels (PER, LOC, ORG, DATE, etc.)

👉 Useful for detecting **class imbalance**.

---

### `plot_conll_distributions.py`

Plots dataset-level distributions.

**Includes:**

* Sentence length distribution
* Token distribution
* Dataset statistics overview

👉 Helps in understanding dataset characteristics.

---

### `plot_entity.py`

Visualizes entity occurrences and patterns.

👉 Useful for:

* Inspecting entity frequency
* Understanding entity coverage

---

### `plot_f1.py`

Plots model performance metrics.

**Includes:**

* F1-score comparison
* Per-entity performance

👉 Used for evaluating and comparing models.

---

### `plot_training_curve.py`

Plots training progress over time.

**Shows:**

* Loss curves
* Training vs validation performance

👉 Helps in diagnosing:

* Overfitting
* Underfitting

---

## 🔄 Role in Pipeline

```text id="e7qphd"
Metrics → Visualization → Reporting → Presentation
```

This module converts numerical outputs into **clear and interpretable visual insights**.

---

## ⚙️ Example Usage

```bash id="l1y5sn"
# Plot class distribution
python scripts/Analysis/visualization/plot_class_distribution.py

# Plot F1 scores
python scripts/Analysis/visualization/plot_f1.py

# Plot training curve
python scripts/Analysis/visualization/plot_training_curve.py
```

---

## 📊 Output

Typical outputs include:

* Bar charts (class distribution, F1 scores)
* Line plots (training curves)
* Distribution plots (dataset statistics)

These outputs are useful for:

* Research papers
* Presentations
* Model comparison

---

## 🧠 When to Use

Use this module when you want to:

✔ Understand dataset structure visually
✔ Analyze model performance trends
✔ Compare different models or datasets
✔ Generate figures for reports and publications

---

## 📌 Summary

The `visualization/` module provides:

✔ Clear graphical representation of results
✔ Insight into dataset and model behavior
✔ Support for analysis and reporting
✔ Publication-ready figures

---

This module ensures that LuxNLP results are **interpretable, insightful, and visually compelling**.
