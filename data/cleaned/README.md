# LuxNLP Cleaned Dataset

This folder contains the **cleaned and structured datasets** after preprocessing, but before final conversion to CoNLL training format.

## 📂 Files Overview

* **Lod_lu_en_lexicon.jsonl**
  Processed LOD lexicon with cleaned entries and translations.

* **Lod_lu_entries_with_domains_and_translations.jsonl**
  LOD entries enriched with domain/category and translation information.

* **lod_lu_sentences.txt**
  Cleaned example sentences extracted from LOD.

* **wikidata_lb_all_ner.json / .csv**
  Cleaned Wikidata entity dataset.

* **wikidata_lb_with_desc_ner.json / .csv**
  Wikidata dataset enriched with descriptions and entity information.

* **All_Extracted_Sentences.txt**
  Combined and cleaned sentences from multiple sources:

  * RTL news
  * LOD.lu
  * Wikidata
  * Additional generated and curated data

## 🧠 Dataset Description

At this stage, the data is:

* Cleaned and filtered
* Structured and partially labeled
* Ready for conversion into CoNLL format

However:

* It is **not yet in BIO format**
* Final labeling and merging happens in the `processed/` folder

## 🎯 Purpose

* Intermediate step between raw and final dataset
* Ensures data quality and consistency
* Prepares data for final NER training pipeline

---

*Note: This data is cleaned but may still contain minor inconsistencies before final processing.*
