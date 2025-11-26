# 🇱🇺 LuxNLP

LuxNLP focuses on improving **Luxembourgish Named Entity Recognition (NER)** and related NLP resources.  
Because Luxembourgish is a low-resource language, our goal is to **collect, clean, and compare data** from **Wikidata** and existing NER datasets to build stronger, more complete models with an extended dataset.

## 🧠 Project Goal

- Scrape and extract **Luxembourgish metadata** from [Wikidata](https://www.wikidata.org/wiki/Wikidata:Main_Page)  
- Clean and filter entity data (people, places, organizations, dates)  
- Compare with existing Luxembourgish NER datasets  
- Fine-tune and evaluate **LuxBERT / NER-BERT** on the merged data  
- Save and publish cleaned data and baseline results in this repository


## 🧑🏼‍💻 Luxembourgish NLP Papers

# Papers

- **Text Generation Models for Luxembourgish with Limited Data: A Balanced Multilingual Strategy**
   Alistair Plum, Tharindu Ranasinghe, Christoph Purschke
   COLING Workshops 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:274656524)
   <details>
     <summary> Abstract </summary>
     This paper addresses the challenges in developing language models for less-represented languages, with a focus on Luxembourgish. Despite its active development, Luxembourgish faces a digital data scarcity, exacerbated by Luxembourg's multilingual context. We propose a novel text generation model based on the T5 architecture, combining limited Luxembourgish data with equal amounts, in terms of size and type, of German and French data. We hypothesise that a model trained on Luxembourgish, German, and French will improve the model's cross-lingual transfer learning capabilities and outperform monolingual and large multilingual models. To verify this, the study at hand explores whether multilingual or monolingual training is more beneficial for Luxembourgish language generation. For the evaluation, we introduce LuxGen, a text generation benchmark that is the first of its kind for Luxembourgish.
  </details>

- **LuxBank: The First Universal Dependency Treebank for Luxembourgish**
   Alistair Plum, Caroline Döhmer, Emilia Milano, Anne-Marie Lutgen, Christoph Purschke
   arXiv.org 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:273877486)
   <details>
     <summary> Abstract </summary>
     The Universal Dependencies (UD) project has significantly expanded linguistic coverage across 161 languages, yet Luxembourgish, a West Germanic language spoken by approximately 400,000 people, has remained absent until now. In this paper, we introduce LuxBank, the first UD Treebank for Luxembourgish, addressing the gap in syntactic annotation and analysis for this `low-research' language. We establish formal guidelines for Luxembourgish language annotation, providing the foundation for the first large-scale quantitative analysis of its syntax. LuxBank serves not only as a resource for linguists and language learners but also as a tool for developing spell checkers and grammar checkers, organising existing text archives and even training large language models. By incorporating Luxembourgish into the UD framework, we aim to enhance the understanding of syntactic variation within West Germanic languages and offer a model for documenting smaller, semi-standardised languages. This work positions Luxembourgish as a valuable resource in the broader linguistic and NLP communities, contributing to the study of languages with limited research and resources.
  </details>

- **LuxemBERT: Simple and Practical Data Augmentation in Language Model Pre-Training for Luxembourgish**
   Cedric Lothritz, B. Lebichot, Kevin Allix, Lisa Veiber, Tégawendé F. Bissyandé, Jacques Klein, A. Boytsov, A. Goujon, C. Lefebvre
   International Conference on Language Resources and Evaluation 2022
   [open paper page](https://www.aclanthology.org/2022.lrec-1.543.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Forget NLI, Use a Dictionary: Zero-Shot Topic Classification for Low-Resource Languages with Application to Luxembourgish**
   Fred Philippy, Shohreh Haddadan, Siwen Guo
   SIGUL 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:268987336)
   <details>
     <summary> Abstract </summary>
     In NLP, zero-shot classification (ZSC) is the task of assigning labels to textual data without any labeled examples for the target classes. A common method for ZSC is to fine-tune a language model on a Natural Language Inference (NLI) dataset and then use it to infer the entailment between the input document and the target labels. However, this approach faces certain challenges, particularly for languages with limited resources. In this paper, we propose an alternative solution that leverages dictionaries as a source of data for ZSC. We focus on Luxembourgish, a low-resource language spoken in Luxembourg, and construct two new topic relevance classification datasets based on a dictionary that provides various synonyms, word translations and example sentences. We evaluate the usability of our dataset and compare it with the NLI-based approach on two topic classification tasks in a zero-shot manner. Our results show that by using the dictionary-based dataset, the trained models outperform the ones following the NLI-based approach for ZSC. While we focus on a single low-resource language in this study, we believe that the efficacy of our approach can also transfer to other languages where such a dictionary is available.
  </details>

- **Neural Text Normalization for Luxembourgish using Real-Life Variation Data**
   Anne-Marie Lutgen, Alistair Plum, Christoph Purschke, Barbara Plank
   COLING Workshops 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:274656616)
   <details>
     <summary> Abstract </summary>
     Orthographic variation is very common in Luxembourgish texts due to the absence of a fully-fledged standard variety. Additionally, developing NLP tools for Luxembourgish is a difficult task given the lack of annotated and parallel data, which is exacerbated by ongoing standardization. In this paper, we propose the first sequence-to-sequence normalization models using the ByT5 and mT5 architectures with training data obtained from word-level real-life variation data. We perform a fine-grained, linguistically-motivated evaluation to test byte-based, word-based and pipeline-based models for their strengths and weaknesses in text normalization. We show that our sequence model using real-life variation data is an effective approach for tailor-made normalization in Luxembourgish.
  </details>

- **LuxInstruct: A Cross-Lingual Instruction Tuning Dataset For Luxembourgish**
   Fred Philippy, Laura Bernardy, Siwen Guo, Jacques Klein, Tegawend'e F. Bissyand'e
   arXiv.org 2025
   [open paper page](https://api.semanticscholar.org/CorpusId:281891834)
   <details>
     <summary> Abstract </summary>
     Instruction tuning has become a key technique for enhancing the performance of large language models, enabling them to better follow human prompts. However, low-resource languages such as Luxembourgish face severe limitations due to the lack of high-quality instruction datasets. Traditional reliance on machine translation often introduces semantic misalignment and cultural inaccuracies. In this work, we address these challenges by creating a cross-lingual instruction tuning dataset for Luxembourgish, without resorting to machine-generated translations into it. Instead, by leveraging aligned data from English, French, and German, we build a high-quality dataset that preserves linguistic and cultural nuances. We provide evidence that cross-lingual instruction tuning not only improves representational alignment across languages but also the model's generative capabilities in Luxembourgish. This highlights how cross-lingual data curation can avoid the common pitfalls of machine-translated data and directly benefit low-resource language development.
  </details>

- **LuxIT: A Luxembourgish Instruction Tuning Dataset from Monolingual Seed Data**
   Julian Valline, Cedric Lothritz, Jordi Cabot
   arXiv.org 2025
   [open paper page](https://api.semanticscholar.org/CorpusId:282400853)
   <details>
     <summary> Abstract </summary>
     The effectiveness of instruction-tuned Large Language Models (LLMs) is often limited in low-resource linguistic settings due to a lack of high-quality training data. We introduce LuxIT, a novel, monolingual instruction tuning dataset for Luxembourgish developed to mitigate this challenge. We synthesize the dataset from a corpus of native Luxembourgish texts, utilizing DeepSeek-R1-0528, chosen for its shown proficiency in Luxembourgish. Following generation, we apply a quality assurance process, employing an LLM-as-a-judge approach. To investigate the practical utility of the dataset, we fine-tune several smaller-scale LLMs on LuxIT. Subsequent benchmarking against their base models on Luxembourgish language proficiency examinations, however, yields mixed results, with performance varying significantly across different models. LuxIT represents a critical contribution to Luxembourgish natural language processing and offers a replicable monolingual methodology, though our findings highlight the need for further research to optimize its application.
  </details>

- **LuxEmbedder: A Cross-Lingual Approach to Enhanced Luxembourgish Sentence Embeddings**
   Fred Philippy, Siwen Guo, Jacques Klein, Tegawend'e F. Bissyand'e
   International Conference on Computational Linguistics 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:274464739)
   <details>
     <summary> Abstract </summary>
     Sentence embedding models play a key role in various Natural Language Processing tasks, such as in Topic Modeling, Document Clustering and Recommendation Systems. However, these models rely heavily on parallel data, which can be scarce for many low-resource languages, including Luxembourgish. This scarcity results in suboptimal performance of monolingual and cross-lingual sentence embedding models for these languages. To address this issue, we compile a relatively small but high-quality human-generated cross-lingual parallel dataset to train LuxEmbedder, an enhanced sentence embedding model for Luxembourgish with strong cross-lingual capabilities. Additionally, we present evidence suggesting that including low-resource languages in parallel training datasets can be more advantageous for other low-resource languages than relying solely on high-resource language pairs. Furthermore, recognizing the lack of sentence embedding benchmarks for low-resource languages, we create a paraphrase detection benchmark specifically for Luxembourgish, aiming to partially fill this gap and promote further research.
  </details>

- **Testing Low-Resource Language Support in LLMs Using Language Proficiency Exams: the Case of Luxembourgish**
   Cedric Lothritz, Jordi Cabot
   arXiv.org 2025
   [open paper page](https://api.semanticscholar.org/CorpusId:277501816)
   <details>
     <summary> Abstract </summary>
     Large Language Models (LLMs) have become an increasingly important tool in research and society at large. While LLMs are regularly used all over the world by experts and lay-people alike, they are predominantly developed with English-speaking users in mind, performing well in English and other wide-spread languages while less-resourced languages such as Luxembourgish are seen as a lower priority. This lack of attention is also reflected in the sparsity of available evaluation tools and datasets. In this study, we investigate the viability of language proficiency exams as such evaluation tools for the Luxembourgish language. We find that large models such as Claude and DeepSeek-R1 typically achieve high scores, while smaller models show weak performances. We also find that the performances in such language exams can be used to predict performances in other NLP tasks in Luxembourgish.
  </details>

- **Letz Translate: Low-Resource Machine Translation for Luxembourgish**
   Yewei Song, Saad Ezzini, Jacques Klein, Tégawendé F. Bissyandé, C. Lefebvre, A. Goujon
   ICON 2023
   [open paper page](https://api.semanticscholar.org/CorpusId:257280138)
   <details>
     <summary> Abstract </summary>
     Natural language processing of Low-Resource Languages (LRL) is often challenged by the lack of data. Therefore, achieving accurate machine translation (MT) in a low-resource environment is a real problem that requires practical solutions. Research in multilingual models have shown that some LRLs can be handled with such models. However, their large size and computational needs make their use in constrained environments (e.g., mobile/IoT devices or limited/old servers) impractical. In this paper, we address this problem by leveraging the power of large multilingual MT models using knowledge distillation. Knowledge distillation can transfer knowledge from a large and complex teacher model to a simpler and smaller student model without losing much in performance. We also make use of high-resource languages that are related or share the same linguistic root as the target LRL. For our evaluation, we consider Luxembourgish as the LRL that shares some roots and properties with German. We build multiple resource-efficient models based on German, knowledge distillation from the multilingual No Language Left Behind (NLLB) model, and pseudo-translation. We find that our efficient models are more than 30% faster and perform only 4% lower compared to the large state-of-the-art NLLB model.
  </details>

- **Is Small Language Model the Silver Bullet to Low-Resource Languages Machine Translation?**
   Yewei Song, Lujun Li, Cedric Lothritz, Saad Ezzini, Lama Sleem, Niccolò Gentile, Radu State, Tegawend'e F. Bissyand'e, Jacques Klein
   unknown 2025
   [open paper page](https://api.semanticscholar.org/CorpusId:277467881)
   <details>
     <summary> Abstract </summary>
     Low-resource languages (LRLs) lack sufficient linguistic resources and are underrepresented in benchmark datasets, resulting in persistently lower translation quality than high-resource languages, especially in privacy-sensitive and resource-limited contexts. Firstly, this study systematically evaluates state-of-the-art smaller Large Language Models in 200 languages using the FLORES-200 benchmark, highlighting persistent deficiencies and disparities in the translation of LRLs. To mitigate these limitations, we investigate knowledge distillation from large pre-trained teacher models to Small Language Models (SLMs) through supervised fine-tuning. The results show substantial improvements; for example, the translation performance of English to Luxembourgish (EN to LB), measured by the LLM-as-a-Judge score, increases from 0.36 to 0.89 in the validation set for Llama-3.2-3B. We further investigate various fine-tuning configurations and tasks to clarify the trade-offs between data scale and training efficiency, verify that the model retains its general capabilities without significant catastrophic forgetting after training, and explore the distillation benefits to other LRLs on SLMs (Khasi, Assamese, and Ukrainian). In general, this work exposes the limitations and fairness issues of current SLMs in LRL translation and systematically explores the potential of using the distillation of knowledge from large to small models, offering practical, empirically grounded recommendations to improve LRL translation systems
  </details>

- **Publish or Hold? Automatic Comment Moderation in Luxembourgish News Articles**
   Tharindu Ranasinghe, Alistair Plum, Christoph Purschke, Marcos Zampieri
   Recent Advances in Natural Language Processing 2023
   [open paper page](https://www.aclanthology.org/2023.ranlp-1.104.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Attitudes Toward Multilingualism in Luxembourg. A Comparative Analysis of Online News Comments and Crowdsourced Questionnaire Data**
   Christoph Purschke
   Frontiers in Artificial Intelligence 2020
   [open paper page](https://www.ncbi.nlm.nih.gov/pubmed/33733199)
   <details>
     <summary> Abstract </summary>
     Attitudes are a fundamental characteristic of human activity. Their main function is the situational assessment of phenomena in practice to maintain action ability and to provide orientation in social interaction. In sociolinguistics, research into attitudes toward varieties and their speakers is a central component of the analysis of linguistic and cultural dynamics. In recent years, computational linguistics has also shown an increased interest in the social conditionality of language. To date, such approaches have lacked a linguistically based theory of attitudes, which, for example, enables an exact terminological differentiation between publicly taken stances and the assumed underlying attitudes. Against this backdrop, the present study contributes to the connection of sociolinguistic and computational linguistic approaches to the analysis of language attitudes. We model a free text corpus of user comments from the RTL.lu news platform using representation learning (Word2Vec). In the aggregated data, we look for contextual similarities between vector representations of words that provide evidence of stances toward multilingualism in Luxembourg. We then contrast this data with the results of a quantitative attitudes study, which was carried out as part of the crowdsourcing project “Schnëssen.” The combination of the different datasets enables the reconstruction of socially pertinent attitudes represented in public discourse. The results demonstrate the central importance of attitudes toward the different languages in Luxembourg for the cultural self-understanding of the population. We also introduce a tool for the automatic orthographic correction of Luxembourgish texts (spellux). In view of the ongoing standardization of Luxembourgish and a lack of rule knowledge in the population, orthographic variation—among other factors like code-switching or regional dialects—poses a great challenge for the automatic processing of text data. The correction tool enables the orthographic normalization of Luxembourgish texts and with that a consolidation of the vocabulary for the training of word embedding models.
  </details>

- **Comparing Pre-Training Schemes for Luxembourgish BERT Models**
   Cedric Lothritz, Saad Ezzini, Christoph Purschke, Tégawendé F. Bissyandé, Jacques Klein, Isabella Olariu, A. Boytsov, C. Lefebvre, Anne Goujon
   Conference on Natural Language Processing 2023
   [open paper page](https://www.aclanthology.org/2023.konvens-main.2.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Adapting Multilingual Embedding Models to Historical Luxembourgish**
   Andrianos Michail, Corina Julia Racl'e, Juri Opitz, Simon Clematide
   Proceedings of the 9th Joint SIGHUM Workshop on Computational Linguistics for Cultural Heritage, Social Sciences, Humanities and Literature (LaTeCH-CLfL 2025) 2025
   [open paper page](https://api.semanticscholar.org/CorpusId:276287441)
   <details>
     <summary> Abstract </summary>
     The growing volume of digitized historical texts requires effective semantic search using text embeddings. However, pre-trained multilingual models face challenges with historical content due to OCR noise and outdated spellings. This study examines multilingual embeddings for cross-lingual semantic search in historical Luxembourgish (LB), a low-resource language. We collect historical Luxembourgish news articles from various periods and use GPT-4o for sentence segmentation and translation, generating 20,000 parallel training sentences per language pair. Additionally, we create a semantic search (Historical LB Bitext Mining) evaluation set and find that existing models perform poorly on cross-lingual search for historical Luxembourgish. Using our historical and additional modern parallel training data, we adapt several multilingual embedding models through contrastive learning or knowledge distillation and increase accuracy significantly for all models. We release our adapted models and historical Luxembourgish-German/French/English bitexts to support further research.
  </details>

- **An Annotation Framework for Luxembourgish Sentiment Analysis**
   Joshgun Sirajzade, Daniela Gierschek, Christoph Schommer
   Workshop on Spoken Language Technologies for Under-resourced Languages 2020
   [open paper page](https://www.aclweb.org/anthology/2020.sltu-1.24.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Evaluating Data Augmentation Techniques for the Training of Luxembourgish Language Models**
   Isabella Olariu, Cedric Lothritz, Tégawendé F. Bissyandé, Jacques Klein
   Conference on Natural Language Processing 2023
   [open paper page](https://www.aclanthology.org/2023.konvens-main.18.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **ENRICH4ALL: A First Luxembourgish BERT Model for a Multilingual Chatbot**
   D. Anastasiou, Radu Ion, Valentin Badea, Olivier Pedretti, Patrick Gratz, Hoorieh Afkari, V. Maquil, Anders Ruge
   SIGUL 2022
   [open paper page](https://www.aclanthology.org/2022.sigul-1.27.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **The LuNa Open Toolbox for the Luxembourgish Language**
   Joshgun Sirajzade, Christoph Schommer
   Industrial Conference on Data Mining 2019
   [open paper page](http://orbilu.uni.lu/bitstream/10993/40407/1/CRC_industrial_paper_84.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Automatic language identity tagging on word and sentence-level in multilingual text sources: a case-study on Luxembourgish**
   T. Lavergne, G. Adda, M. Adda-Decker, L. Lamel
   International Conference on Language Resources and Evaluation 2014
   [open paper page](http://www.lrec-conf.org/proceedings/lrec2014/pdf/732_Paper.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Developments of “Lëtzebuergesch” Resources for Automatic Speech Processing and Linguistic Studies**
   M. Adda-Decker, Thomas Pellegrini, Éric Bilinski, G. Adda
   International Conference on Language Resources and Evaluation 2008
   [open paper page](http://www.lrec-conf.org/proceedings/lrec2008/pdf/855_paper.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **ASRLUX: AUTOMATIC SPEECH RECOGNITION FOR THE LOW-RESOURCE LANGUAGE LUXEMBOURGISH**
   Peter Gilles, Leopold Hillah, Nina Hosseini-Kivanani
   unknown 0
   [open paper page](https://guarant.cz/icphs2023/266.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Do Large Language Models Grasp The Grammar? Evidence from Grammar-Book-Guided Probing in Luxembourgish**
   Lujun Li, Yewei Song, Lama Sleem, Yiqun Wang, Yangjie Xu, Cedric Lothritz, Niccolò Gentile, Radu State, Tégawendé F. Bissyandé, Jacques Klein
   arXiv.org 2025
   [open paper page](https://arxiv.org/pdf/2510.24856.pdf)
   <details>
     <summary> Abstract </summary>
     Grammar refers to the system of rules that governs the structural organization and the semantic relations among linguistic units such as sentences, phrases, and words within a given language. In natural language processing, there remains a notable scarcity of grammar focused evaluation protocols, a gap that is even more pronounced for low-resource languages. Moreover, the extent to which large language models genuinely comprehend grammatical structure, especially the mapping between syntactic structures and meanings, remains under debate. To investigate this issue, we propose a Grammar Book Guided evaluation pipeline intended to provide a systematic and generalizable framework for grammar evaluation consisting of four key stages, and in this work we take Luxembourgish as a case study. The results show a weak positive correlation between translation performance and grammatical understanding, indicating that strong translations do not necessarily imply deep grammatical competence. Larger models perform well overall due to their semantic strength but remain weak in morphology and syntax, struggling particularly with Minimal Pair tasks, while strong reasoning ability offers a promising way to enhance their grammatical understanding.
  </details>

- **THE CASE OF LUXEMBOURGISH**
   I. Steiner, Sébastien Le Maguer, J. Manzoni, Peter Gilles, Jürgen Trouvain
   unknown 2017
   [open paper page](http://essv2017.coli.uni-saarland.de/pdfs/Steiner_1.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Language Resources for Historical Newspapers: the Impresso Collection**
   Maud Ehrmann, Matteo Romanello, S. Clematide, Phillip Ströbel, Raphaël Barman
   International Conference on Language Resources and Evaluation 2020
   [open paper page](https://www.aclweb.org/anthology/2020.lrec-1.121.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **The Study of Writing Variants in an Under-resourced Language: Some Evidence from Mobile N-Deletion in Luxembourgish**
   Natalie D. Snoeren, M. Adda-Decker, G. Adda
   International Conference on Language Resources and Evaluation 2010
   [open paper page](http://www.lrec-conf.org/proceedings/lrec2010/pdf/258_Paper.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Crowdsourcing the linguistic landscape of a multilingual country. Introducing Lingscape in Luxembourg**
   Christoph Purschke
    2017
   [open paper page](https://api.semanticscholar.org/CorpusId:54709078)
   <details>
     <summary> Abstract </summary>
     This paper introduces the citizen science mobile application Lingscape. This free research tool for Android and iOS smartphones uses a crowdsourcing approach for research on linguistic landscapes. The paper discusses the use of mobile applications and crowdsourcing in linguistics, methodological requirements and problems of an app-based approach to the study of linguistic landscapes, and the key features of the app Lingscape. It considers the Luxembourgish cultural super-diversity as well as existing studies about the Luxembourgish linguistic landscape to set the background for the pilotstudy.
  </details>

- **Die Erforschung der Luxemburger Wortbildung als Aufgabe. Eine Projektvorstellung**
   Heinz Sieburg, B. Weimann
   unknown 2016
   [open paper page](https://api.semanticscholar.org/CorpusId:114535953)
   <details>
     <summary> Abstract </summary>
     Research on Luxembourgish word formation – both from a historical and a synchronic perspective – is still at its very beginning. Its most challenging aspect is the complex multilingual situation in Luxembourg which arose due to the country’s intricate history. The research project “WBLUX” takes this unique situation into account; It has been designed as a multi-stage corpus-based tandem project as a cooperation between German and Luxembourgish studies. This paper commences by introducing the project design and the corpus concept, followed by a presentation of some exemplary corpus data.
  </details>

- **Schnëssen. Surveying language dynamics in Luxembourgish with a mobile research app**
   Nathalie Entringer, Peter Gilles, S. Martín, Christoph Purschke
   Linguistics Vanguard 2021
   [open paper page](https://api.semanticscholar.org/CorpusId:218790085)
   <details>
     <summary> Abstract </summary>
     Abstract The mobile app Schnëssen establishes a digital and participatory research platform to collect data on present-day spoken Luxembourgish through crowdsourcing and to present the results of data analysis to the general public. Users can participate in different kinds of audio recording tasks (translation, picture naming, reading, question) as well as in sociolinguistic surveys. All audio recordings are accessible to the public via an interactive map, which allows the participants to explore variation in Luxembourgish themselves. In the first year of data collection, roughly 210.000 recordings have be collected covering numerous variation phenomena on all linguistic levels. Additionally, over 2800 sociolinguistic questionnaires have been filled out. Compiling such amounts of data, the Schnëssen app represents the largest research corpus of spoken Luxembourgish.
  </details>

- **Codification in the shadow of standards: ideologies in early nineteenth-century metalinguistic texts on Luxembourgish**
   John Bellamy
   Language &amp; History 2024
   [open paper page](https://api.semanticscholar.org/CorpusId:267946044)
   <details>
     <summary> Abstract </summary>
     ABSTRACT Inspired by the ideological and multilingual turn in ‘third wave’ language standardisation studies (McLelland 2020, Walsh 2021), this paper demonstrates the value of these perspectives for historical analysis by exploring the implications of language ideologies for the early codification of Luxembourgish. As a ‘late’ standardised language (Vogl 2012), Luxembourgish provides a valuable case study for evaluating how existing powerful standard language regimes (Gal 2006) ideologically influence the discursive construction of a ‘late’ standard language, especially in multilingual borderlands. Ideologies of linguistic differentiation (Irvine & Gal 2000; Gal & Irvine 2019) are inherent in the standardisation process of Luxembourgish which sits between the Romance and Germanic language spheres of influence. The analysis focuses on metadiscourses of three early texts on Luxembourgish (Meyer 1829, Meyer & Gloden 1845, De la Fontaine 1855) in their discussions and proposals for codification. The diverse labelling of Luxembourgish in the texts forms part of a metadiscourse of differentiation and hierarchical contrast. Other core emergent discourses foreground affinities with Standard French and Standard German respectively but in differing ways that evoke the ideological notion of erasure. The final part of the analysis identifies further discourses that, in contrast, frame Luxembourgish as unique and different from other languages.
  </details>

- **The adaptation of MAIN to Luxembourgish**
   Constanze Weth, Cyril Wealer
   unknown 2020
   [open paper page](https://api.semanticscholar.org/CorpusId:225331825)
   <details>
     <summary> Abstract </summary>
     This paper describes the addition of Luxembourgish to the language versions of MAIN, the adaption process and the use of MAIN in Luxembourg. A short description of Luxembourg’s multilingual society and trilingual school system as well as an overview of selected morphosyntactic and syntactic features of Luxembourgish introduce the Luxembourgish version of MAIN.
  </details>

- **40. Komplexe Überdachung II: Luxemburg. Die Genese einer neuen Nationalsprache**
   P. Gilles
   unknown 2018
   [open paper page](https://doi.org/10.13140/rg.2.2.20119.88485)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Accepting a “New” Standard Variety: Comparing Explicit Attitudes in Luxembourg and Belgium**
   J. Vari, M. Tamburelli
   Languages 2021
   [open paper page](https://api.semanticscholar.org/CorpusId:238839049)
   <details>
     <summary> Abstract </summary>
     Language maintenance efforts aim to bolster attitudes towards endangered languages by providing them with a standard variety as a means to raise their status and prestige. However, the introduced variety can vary in its degrees of standardisation. This paper investigates whether varying degrees of standardisation surface in explicit attitudes towards standard varieties in endangered vernacular speech communities. Following sociolinguistic models of standardisation, we suggest that explicit attitudes towards the standard variety indicate its acceptance in vernacular speech communities, reflecting its overall degree of standardisation. We use the standardised Attitudes towards Language (AtoL) questionnaire to investigate explicit attitudes towards the respective standard varieties in two related vernacular speech communities—the Belgische Eifel in Belgium and the Éislek in Luxembourg. The vernacular of these speech communities, Moselle Franconian, is considered generally vulnerable (UNESCO), and the two speech communities have opted to introduce different standard varieties: Standard Luxembourgish in Luxembourg shows lower degrees of standardisation and is only partially implemented. In contrast, Standard German in the Belgian speech community is highly standardised and completely implemented. Results show that degrees of standardisation surface in speakers’ explicit attitudes. Our findings have important implications for the role of standardisation in language maintenance efforts.
  </details>

- **From status to corpus: Codification and implementation of spelling norms in Luxembourgish**
   Peter Gilles
   unknown 2015
   [open paper page](https://doi.org/10.1057/9781137361240_7)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Die Luxemburger Mehrsprachigkeit**
   Andreas Heinz, Fernand Fehlen
   unknown 2016
   [open paper page](https://doi.org/10.1515/9783839433140)
   <details>
     <summary> Abstract </summary>
     unknown
  </details>

- **Governing complex linguistic diversity in Barcelona, Luxembourg and Riga**
   P. Kraus, Vicent Climent‐Ferrando, Melanie Frank, N. García
   Nations and Nationalism 2020
   [open paper page](https://api.semanticscholar.org/CorpusId:230545193)
   <details>
     <summary> Abstract </summary>
     Contemporary migration has entailed the emergence of new forms of multilingualism in many European cities. The article uses the concept of complex diversity to analyse this dynamic. The concept points at settings where historical forms of multilingualism and more recent patterns of linguistic heterogeneity interact in ways that lead to particularly rich cultural configurations. The authors assess how local authorities deal with multilingualism in three cities that represent ‘ most complex ’ cases of diversity politics: Barcelona, Luxembourg and Riga. The focus is on policies related to public communication and on the approaches adopted to promote social and political inclusion in ever more multilingual urban environments. In normative terms, the article concludes that political responses to complex diversity should aim both at overcoming linguistic status inequalities based on historical structures of domination and at creating common spaces of communication for diverse citizens.
  </details>

- **Sprachliche Identifizierungen im luxemburgisch-deutschen Grenzraum**
   B. Weimann
   unknown 2014
   [open paper page](https://api.semanticscholar.org/CorpusId:176735044)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Luxembourgish: A Success Story? A Small National Language in a Multilingual Country**
   S. Ehrhart, Fernand Fehlen
   unknown 2011
   [open paper page](https://api.semanticscholar.org/CorpusId:151193664)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Small languages, education and citizenship: the paradoxical case of Luxembourgish**
   Kristine Horner, Jean-Jacques Weber
   unknown 2010
   [open paper page](https://doi.org/10.1515/ijsl.2010.045)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Building Large Monolingual Dictionaries at the Leipzig Corpora Collection: From 100 to 200 Languages**
   Dirk Goldhahn, Thomas Eckart, U. Quasthoff
   International Conference on Language Resources and Evaluation 2012
   [open paper page](http://www.lrec-conf.org/proceedings/lrec2012/pdf/327_Paper.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Aspect-Driven Structuring of Historical Dutch Newspaper Archives**
   H. Kroll, Christin Katharina Kreutz, Mirjam Cuper, B. M. Thang, Wolf-Tilo Balke
   International Conference on Theory and Practice of Digital Libraries 2023
   [open paper page](https://api.semanticscholar.org/CorpusId:259950937)
   <details>
     <summary> Abstract </summary>
     Digital libraries oftentimes provide access to historical newspaper archives via keyword-based search. Historical figures and their roles are particularly interesting cognitive access points in historical research. Structuring and clustering news articles would allow more sophisticated access for users to explore such information. However, real-world limitations such as the lack of training data, licensing restrictions and non-English text with OCR errors make the composition of such a system difficult and cost-intensive in practice. In this work we tackle these issues with the showcase of the National Library of the Netherlands by introducing a role-based interface that structures news articles on historical persons. In-depth, component-wise evaluations and interviews with domain experts highlighted our prototype's effectiveness and appropriateness for a real-world digital library collection.
  </details>

- **Monolinguisme politique dans une société plurilingue ? Le cas du Luxembourg**
   Núria Garcia
   unknown 2014
   [open paper page](https://doi.org/10.3917/RIPC.214.0017)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **The paradox of contemporary linguistic nationalism: the case of Luxembourg**
   N. García
   unknown 2014
   [open paper page](https://doi.org/10.1111/NANA.12043)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Capturing the influence of geopolitical ties from Wikipedia with reduced Google matrix**
   Samer El Zant, K. Jaffrès-Runser, D. Shepelyansky
   PLoS ONE 2018
   [open paper page](https://api.semanticscholar.org/CorpusId:3838037)
   <details>
     <summary> Abstract </summary>
     Interactions between countries originate from diverse aspects such as geographic proximity, trade, socio-cultural habits, language, religions, etc. Geopolitics studies the influence of a country’s geographic space on its political power and its relationships with other countries. This work reveals the potential of Wikipedia mining for geopolitical study. Actually, Wikipedia offers solid knowledge and strong correlations among countries by linking web pages together for different types of information (e.g. economical, historical, political, and many others). The major finding of this paper is to show that meaningful results on the influence of country ties can be extracted from the hyperlinked structure of Wikipedia. We leverage a novel stochastic matrix representation of Markov chains of complex directed networks called the reduced Google matrix theory. For a selected small size set of nodes, the reduced Google matrix concentrates direct and indirect links of the million-node sized Wikipedia network into a small Perron-Frobenius matrix keeping the PageRank probabilities of the global Wikipedia network. We perform a novel sensitivity analysis that leverages this reduced Google matrix to characterize the influence of relationships between countries from the global network. We apply this analysis to two chosen sets of countries (i.e. the set of 27 European Union countries and a set of 40 top worldwide countries). We show that with our sensitivity analysis we can exhibit easily very meaningful information on geopolitics from five different Wikipedia editions (English, Arabic, Russian, French and German).
  </details>

- **One Million Posts: A Data Set of German Online Discussions**
   Dietmar Schabus, M. Skowron, M. Trapp
   Annual International ACM SIGIR Conference on Research and Development in Information Retrieval 2017
   [open paper page](http://dl.acm.org/citation.cfm?id=3080711)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **SwissBERT: The Multilingual Language Model for Switzerland**
   Jannis Vamvas, Johannes Graen, Rico Sennrich
   Swiss Text Analytics Conference 2023
   [open paper page](https://api.semanticscholar.org/CorpusId:257687530)
   <details>
     <summary> Abstract </summary>
     We present SwissBERT, a masked language model created specifically for processing Switzerland-related text. SwissBERT is a pre-trained model that we adapted to news articles written in the national languages of Switzerland -- German, French, Italian, and Romansh. We evaluate SwissBERT on natural language understanding tasks related to Switzerland and find that it tends to outperform previous models on these tasks, especially when processing contemporary news and/or Romansh Grischun. Since SwissBERT uses language adapters, it may be extended to Swiss German dialects in future work. The model and our open-source code are publicly released at https://github.com/ZurichNLP/swissbert.
  </details>

- **Clustering Ideological Terms in Historical Newspaper Data with Diachronic Word Embeddings**
   Jani Marjanen, Lidia Pivovarova, Elaine Zosa, Jussi Kurunmäki
   HistoInformatics@TPDL 2019
   [open paper page](https://ceur-ws.org/Vol-2461/paper_4.pdf)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Bleu: a Method for Automatic Evaluation of Machine Translation**
   Kishore Papineni, Salim Roukos, T. Ward, Wei-Jing Zhu
   Annual Meeting of the Association for Computational Linguistics 2002
   [open paper page](https://www.aclweb.org/anthology/P02-1040.pdf)
   <details>
     <summary> Abstract </summary>
     Human evaluations of machine translation are extensive but expensive. Human evaluations can take months to finish and involve human labor that can not be reused. We propose a method of automatic machine translation evaluation that is quick, inexpensive, and language-independent, that correlates highly with human evaluation, and that has little marginal cost per run. We present this method as an automated understudy to skilled human judges which substitutes for them when there is need for quick or frequent evaluations.
  </details>

- **Climbing towards NLU: On Meaning, Form, and Understanding in the Age of Data**
   Emily M. Bender, Alexander Koller
   Annual Meeting of the Association for Computational Linguistics 2020
   [open paper page](https://www.aclweb.org/anthology/2020.acl-main.463.pdf)
   <details>
     <summary> Abstract </summary>
     The success of the large neural language models on many NLP tasks is exciting. However, we find that these successes sometimes lead to hype in which these models are being described as “understanding” language or capturing “meaning”. In this position paper, we argue that a system trained only on form has a priori no way to learn meaning. In keeping with the ACL 2020 theme of “Taking Stock of Where We’ve Been and Where We’re Going”, we argue that a clear understanding of the distinction between form and meaning will help guide the field towards better science around natural language understanding.
  </details>

- **ÚFAL at MultiLexNorm 2021: Improving Multilingual Lexical Normalization by Fine-tuning ByT5**
   David Samuel, Milan Straka
   WNUT 2021
   [open paper page](https://www.aclanthology.org/2021.wnut-1.54.pdf)
   <details>
     <summary> Abstract </summary>
     We present the winning entry to the Multilingual Lexical Normalization (MultiLexNorm) shared task at W-NUT 2021 (van der Goot et al., 2021a), which evaluates lexical-normalization systems on 12 social media datasets in 11 languages. We base our solution on a pre-trained byte-level language model, ByT5 (Xue et al., 2021a), which we further pre-train on synthetic data and then fine-tune on authentic normalization data. Our system achieves the best performance by a wide margin in intrinsic evaluation, and also the best performance in extrinsic evaluation through dependency parsing. The source code is released at https://github.com/ufal/multilexnorm2021 and the fine-tuned models at https://huggingface.co/ufal.
  </details>

- **A Survey of Resources and Methods for Natural Language Processing of Serbian Language**
   U. Marovac, A. Avdić, Nikola Milosevic
   arXiv.org 2023
   [open paper page](https://api.semanticscholar.org/CorpusId:258078889)
   <details>
     <summary> Abstract </summary>
     The Serbian language is a Slavic language spoken by over 12 million speakers and well understood by over 15 million people. In the area of natural language processing, it can be considered a low-resourced language. Also, Serbian is considered a high-inflectional language. The combination of many word inflections and low availability of language resources makes natural language processing of Serbian challenging. Nevertheless, over the past three decades, there have been a number of initiatives to develop resources and methods for natural language processing of Serbian, ranging from developing a corpus of free text from books and the internet, annotated corpora for classification and named entity recognition tasks to various methods and models performing these tasks. In this paper, we review the initiatives, resources, methods, and their availability.
  </details>

- **A Study into Pre-Training Strategies for Spoken Language Understanding on Dysarthric Speech**
   Pu Wang, B. BabaAli, H. V. Hamme
   Interspeech 2021
   [open paper page](https://api.semanticscholar.org/CorpusId:235435642)
   <details>
     <summary> Abstract </summary>
     End-to-end (E2E) spoken language understanding (SLU) systems avoid an intermediate textual representation by mapping speech directly into intents with slot values. This approach requires considerable domain-specific training data. In low-resource scenarios this is a major concern, e.g., in the present study dealing with SLU for dysarthric speech. Pretraining part of the SLU model for automatic speech recognition targets helps but no research has shown to which extent SLU on dysarthric speech benefits from knowledge transferred from other dysarthric speech tasks. This paper investigates the efficiency of pre-training strategies for SLU tasks on dysarthric speech. The designed SLU system consists of a TDNN acoustic model for feature encoding and a capsule network for intent and slot decoding. The acoustic model is pre-trained in two stages: initialization with a corpus of normal speech and finetuning on a mixture of dysarthric and normal speech. By introducing the intelligibility score as a metric of the impairment severity, this paper quantitatively analyzes the relation between generalization and pathology severity for dysarthric speech.
  </details>

- **Language Varieties of Italy: Technology Challenges and Opportunities**
   Alan Ramponi
   Transactions of the Association for Computational Linguistics 2022
   [open paper page](https://api.semanticscholar.org/CorpusId:252383238)
   <details>
     <summary> Abstract </summary>
     Italy is characterized by a one-of-a-kind linguistic diversity landscape in Europe, which implicitly encodes local knowledge, cultural traditions, artistic expressions, and history of its speakers. However, most local languages and dialects in Italy are at risk of disappearing within a few generations. The NLP community has recently begun to engage with endangered languages, including those of Italy. Yet, most efforts assume that these varieties are under-resourced language monoliths with an established written form and homogeneous functions and needs, and thus highly interchangeable with each other and with high-resource, standardized languages. In this paper, we introduce the linguistic context of Italy and challenge the default machine-centric assumptions of NLP for Italy’s language varieties. We advocate for a shift in the paradigm from machine-centric to speaker-centric NLP, and provide recommendations and opportunities for work that prioritizes languages and their speakers over technological advances. To facilitate the process, we finally propose building a local community towards responsible, participatory efforts aimed at supporting vitality of languages and dialects of Italy.
  </details>

- **Fake News Detection with the New German Dataset "GermanFakeNC"**
   Inna Vogel, P. Jiang
   International Conference on Theory and Practice of Digital Libraries 2019
   [open paper page](https://doi.org/10.1007/978-3-030-30760-8_25)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Comparison of Self-Supervised Speech Pre-Training Methods on Flemish Dutch**
   Jakob Poncelet, H. V. Hamme
   Automatic Speech Recognition & Understanding 2021
   [open paper page](https://api.semanticscholar.org/CorpusId:238215628)
   <details>
     <summary> Abstract </summary>
     Recent research in speech processing exhibits a growing interest in unsupervised and self-supervised representation learning from unlabelled data to alleviate the need for large amounts of annotated data. We investigate several popular pre-training methods and apply them to Flemish Dutch. We compare off-the-shelf English pre-trained models to models trained on an increasing amount of Flemish data. We find that the most important factors for positive transfer to downstream speech recognition tasks include a substantial amount of data and a matching pre-training domain. Ideally, we also finetune on an annotated subset in the target language. All pre-trained models improve linear phone separability in Flemish, but not all methods improve Automatic Speech Recognition. We experience superior performance with wav2vec 2.0 and we obtain a 30% WER improvement by finetuning the multilingually pre-trained XLSR-53 model on Flemish Dutch, after integration into an HMM-DNN acoustic model.
  </details>

- **Exploring the Landscape of Natural Language Processing Research**
   Tim Schopf, Karim Arabi, F. Matthes
   Recent Advances in Natural Language Processing 2023
   [open paper page](https://www.aclanthology.org/2023.ranlp-1.111.pdf)
   <details>
     <summary> Abstract </summary>
     As an efficient approach to understand, generate, and process natural language texts, research in natural language processing (NLP) has exhibited a rapid spread and wide adoption in recent years. Given the increasing research work in this area, several NLP-related approaches have been surveyed in the research community. However, a comprehensive study that categorizes established topics, identifies trends, and outlines areas for future research remains absent. Contributing to closing this gap, we have systematically classified and analyzed research papers in the ACL Anthology. As a result, we present a structured overview of the research landscape, provide a taxonomy of fields of study in NLP, analyze recent developments in NLP, summarize our findings, and highlight directions for future work.
  </details>

- **Improving BERT Pretraining with Syntactic Supervision**
   Georgios Tziafas, Konstantinos Kogkalidis, G. Wijnholds, M. Moortgat
   CLASP 2021
   [open paper page](https://api.semanticscholar.org/CorpusId:233324275)
   <details>
     <summary> Abstract </summary>
     Bidirectional masked Transformers have become the core theme in the current NLP landscape. Despite their impressive benchmarks, a recurring theme in recent research has been to question such models’ capacity for syntactic generalization. In this work, we seek to address this question by adding a supervised, token-level supertagging objective to standard unsupervised pretraining, enabling the explicit incorporation of syntactic biases into the network’s training dynamics. Our approach is straightforward to implement, induces a marginal computational overhead and is general enough to adapt to a variety of settings. We apply our methodology on Lassy Large, an automatically annotated corpus of written Dutch. Our experiments suggest that our syntax-aware model performs on par with established baselines, despite Lassy Large being one order of magnitude smaller than commonly used corpora.
  </details>

- **Dutch Named Entity Recognition and De-identification Methods for the Human Resource Domain**
   C. V. Toledo, F. V. Dijk, M. Spruit
   International Journal on Natural Language Computing 2020
   [open paper page](https://api.semanticscholar.org/CorpusId:234407470)
   <details>
     <summary> Abstract </summary>
     The human resource (HR) domain contains various types of privacy-sensitive textual data, such as e-mail correspondence and performance appraisal. Doing research on these documents brings several challenges, one of them anonymisation. In this paper, we evaluate the current Dutch text de-identification methods for the HR domain in four steps. First, by updating one of these methods with the latest named entity recognition (NER) models. The result is that the NER model based on the CoNLL 2002 corpus in combination with the BERTje transformer give the best combination for suppressing persons (recall 0.94) and locations (recall 0.82). For suppressing gender, DEDUCE is performing best (recall 0.53). Second NER evaluation is based on both strict de-identification of entities (a person must be suppressed as a person) and third evaluation on a loose sense of de-identification (no matter what how a person is suppressed, as long it is suppressed). In the fourth and last step a new kind of NER dataset is tested for recognising job titles in tezts.
  </details>

- **Lörres, Möppes, and the Swiss. (Re)Discovering regional patterns in anonymous social media data**
   Christoph Purschke, Dirk Hovy
   Journal of Linguistic Geography 2019
   [open paper page](https://doi.org/10.1017/jlg.2019.10)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **A systematic review of natural language processing applications for hydrometeorological hazards assessment**
   Achraf Tounsi, M. Temimi
   Natural Hazards 2023
   [open paper page](https://doi.org/10.1007/s11069-023-05842-0)
   <details>
     <summary> Abstract </summary>
     Natural language processing (NLP) is a promising tool for collecting data that are usually hard to obtain during extreme weather, like community response and infrastructure performance. Patterns and trends in abundant data sources such as weather reports, news articles, and social media may provide insights into potential impacts and early warnings of impending disasters. This paper reviews the peer-reviewed studies (journals and conference proceedings) that used NLP to assess extreme weather events, focusing on heavy rainfall events. The methodology searches four databases (ScienceDirect, Web of Science, Scopus, and IEEE Xplore) for articles published in English before June 2022. The preferred reporting items for systematic reviews and meta-analysis reviews and meta-analysis guidelines were followed to select and refine the search. The method led to the identification of thirty-five studies. In this study, hurricanes, typhoons, and flooding were considered. NLP models were implemented in information extraction, topic modeling, clustering, and classification. The findings show that NLP remains underutilized in studying extreme weather events. The review demonstrated that NLP could potentially improve the usefulness of social media platforms, newspapers, and other data sources that could improve weather event assessment. In addition, NLP could generate new information that should complement data from ground-based sensors, reducing monitoring costs. Key outcomes of NLP use include improved accuracy, increased public safety, improved data collection, and enhanced decision-making are identified in the study. On the other hand, researchers must overcome data inadequacy, inaccessibility, nonrepresentative and immature NLP approaches, and computing skill requirements to use NLP properly.
  </details>

- **Natural Language Processing of Student's Feedback to Instructors: A Systematic Review**
   Ayse Saliha Sunar, Md Saifuddin Khalid
   IEEE Transactions on Learning Technologies 2024
   [open paper page](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10310166)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Data-Driven Syllabification for Middle Dutch**
   Wouter Haverals, Folgert Karsdorp, M. Kestemont
   Digital Medievalist 2019
   [open paper page](https://api.semanticscholar.org/CorpusId:209073200)
   <details>
     <summary> Abstract </summary>
     The task of automatically separating Middle Dutch words into syllables is a challenging one. A first method was presented by Bouma and Hermans (2012), who combined a rule-based finite-state component with data-driven error correction. Achieving an average word accuracy of 96.5%, their system surely is a satisfactory one, although it leaves room for improvement. Generally speaking, rule-based methods are less attractive for dealing with a medieval language like Middle Dutch, where not only each dialect has its own spelling preferences, but where there is also much idiosyncratic variation among scribes. This paper presents a different method for the task of automatically syllabifying Middle Dutch words, which does not rely on a set of pre-defined linguistic information. Using a Recurrent Neural Network (RNN) with Long-Short-Term Memory cells (LSTM), we obtain a system which outperforms the rule-based method both in robustness and in effort.
  </details>

- **Comprehensive Implementation of TextCNN for Enhanced Collaboration between Natural Language Processing and System Recommendation**
   Xiaonan Xu, Zheng Xu, Zhipeng Ling, Zhengyu Jin, ShuQian Du
   International Conference on Image, Signal Processing, and Pattern Recognition (ISPP 2024) 2024
   [open paper page](https://arxiv.org/pdf/2403.09718.pdf)
   <details>
     <summary> Abstract </summary>
     Natural Language Processing (NLP) is an important branch of artificial intelligence that studies how to enable computers to understand, process, and generate human language. Text classification is a fundamental task in NLP, which aims to classify text into different predefined categories. Text classification is the most basic and classic task in natural language processing, and most of the tasks in natural language processing can be regarded as classification tasks. In recent years, deep learning has achieved great success in many research fields, and today, it has also become a standard technology in the field of NLP, which is widely integrated into text classification tasks. Unlike numbers and images, text processing emphasizes fine-grained processing ability. Traditional text classification methods generally require preprocessing the input model's text data. Additionally, they also need to obtain good sample features through manual annotation and then use classical machine learning algorithms for classification. Therefore, this paper analyzes the application status of deep learning in the three core tasks of NLP (including text representation, word order modeling, and knowledge representation). This content explores the improvement and synergy achieved through natural language processing in the context of text classification, while also taking into account the challenges posed by adversarial techniques in text generation, text classification, and semantic parsing. An empirical study on text classification tasks demonstrates the effectiveness of interactive integration training, particularly in conjunction with TextCNN, highlighting the significance of these advancements in text classification augmentation and enhancement.
  </details>

- **Vision, status, and research topics of Natural Language Processing**
   Xieling Chen, Haoran Xie, Xiaohui Tao
   Natural Language Processing Journal 2022
   [open paper page](https://doi.org/10.1016/j.nlp.2022.100001)
   <details>
     <summary> Abstract </summary>
     unknown
  </details>

- **Natural language processing applications for low-resource languages**
   Partha Pakray, Alexander Gelbukh, Sivaji Bandyopadhyay
   Natural Language Processing 2025
   [open paper page](https://doi.org/10.1017/nlp.2024.33)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Natural Language Processing (Almost) from Scratch**
   R. Collobert, J. Weston, L. Bottou, Michael Karlen, K. Kavukcuoglu, Pavel P. Kuksa
   Journal of machine learning research 2011
   [open paper page](https://arxiv.org/pdf/1103.0398.pdf)
   <details>
     <summary> Abstract </summary>
     We propose a unified neural network architecture and learning algorithm that can be applied to various natural language processing tasks including part-of-speech tagging, chunking, named entity recognition, and semantic role labeling. This versatility is achieved by trying to avoid task-specific engineering and therefore disregarding a lot of prior knowledge. Instead of exploiting man-made input features carefully optimized for each task, our system learns internal representations on the basis of vast amounts of mostly unlabeled training data. This work is then used as a basis for building a freely available tagging system with good performance and minimal computational requirements.
  </details>

- **Building a Digital Library of Web News**
   Nuno Maria, Mário J. Silva
   European Conference on Research and Advanced Technology for Digital Libraries 2000
   [open paper page](https://doi.org/10.1007/3-540-45268-0_36)
   <details>
     <summary> Abstract </summary>
     
  </details>

- **Meta-Learning for Phonemic Annotation of Corpora**
   Veronique Hoste, Walter Daelemans, E. Tjong Kim Sang, Steven Gillis
   International Conference on Machine Learning 2000
   [open paper page](https://api.semanticscholar.org/CorpusId:1275862)
   <details>
     <summary> Abstract </summary>
     We apply rule induction, classifier combination and meta-learning (stacked classifiers) to the problem of bootstrapping high accuracy automatic annotation of corpora with pronunciation information. The task we address in this paper consists of generating phonemic representations reflecting the Flemish and Dutch pronunciations of a word on the basis of its orthographic representation (which in turn is based on the actual speech recordings). We compare several possible approaches to achieve the text-topronunciation mapping task: memory-based learning, transformation-based learning, rule induction, maximum entropy modeling, combination of classifiers in stacked learning, and stacking of meta-learners. We are interested both in optimal accuracy and in obtaining insight into the linguistic regularities involved. As far as accuracy is concerned, an already high accuracy level (93% for Celex and 86% for Fonilex at word level) for single classifiers is boosted significantly with additional error reductions of 31% and 38% respectively using combination of classifiers, and a further 5% using combination of meta-learners, bringing overall word level accuracy to 96% for the Dutch variant and 92% for the Flemish variant. We also show that the application of machine learning methods indeed leads to increased insight into the linguistic regularities determining the variation between the two pronunciation variants studied.
  </details>

- **Semantic interpretation of Dutch spoken dialogue (short paper)**
   J. Geertzen
   International Conference on Computational Semantics 2009
   [open paper page](https://api.semanticscholar.org/CorpusId:54921922)
   <details>
     <summary> Abstract </summary>
     Semantic interpretation involves the process of 'translating' natural language to a representation of its meaning. It could be understood as the task of mapping syntax to semantics, assuming that the syntactic relationships in an utterance correspond to functional relationships in the meaning representation. Relevant work in this area often uses techniques from machine translation and machine learning in the mapping from natural language to meaning-representation languages (e.g. [9, 7]). These approaches can be robust, and thus would be useful in dealing with large quantities of utterances, but require large amounts of annotated data.
  </details>
