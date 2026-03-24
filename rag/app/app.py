import json
import os
from pathlib import Path
from groq import Groq

import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification
from huggingface_hub import hf_hub_download, upload_file, InferenceClient

from dynamic_rag_luxnlp import DynamicLuxRAG, build_ner_prompt

# =========================
# CONFIG
# =========================
DATA_PATH = "Lux_Final.conll"
MEMORY_PATH = "rag_memory.jsonl"
APPROVED_PATH = "approved_examples.jsonl"
MODEL_REPO = "YashGavade10/luxnlp-xlmr-ner"
DATASET_REPO = "YashGavade10/luxnlp-rag-memory"
METRICS_PATH = "metrics.json"

# Real LLM config from Space secrets
HF_API_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_LLM_MODEL = os.getenv("HF_LLM_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct").strip()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# =========================
# LOAD DATASET MEMORY FROM HF DATASET REPO
# =========================
def ensure_memory_files():
    for filename in [MEMORY_PATH, APPROVED_PATH]:
        try:
            downloaded = hf_hub_download(
                repo_id=DATASET_REPO,
                repo_type="dataset",
                filename=filename,
                token=HF_API_TOKEN if HF_API_TOKEN else None,
            )
            Path(filename).write_text(
                Path(downloaded).read_text(encoding="utf-8"),
                encoding="utf-8"
            )
        except Exception:
            if not Path(filename).exists():
                Path(filename).write_text("", encoding="utf-8")


ensure_memory_files()

# =========================
# LOAD DYNAMIC RAG
# =========================
rag = DynamicLuxRAG(DATA_PATH, MEMORY_PATH)

# =========================
# LOAD XLM-R MODEL
# =========================
tokenizer = AutoTokenizer.from_pretrained(MODEL_REPO)
model = AutoModelForTokenClassification.from_pretrained(MODEL_REPO)
model.eval()
id2label = model.config.id2label


# =========================
# HELPERS
# =========================
def format_retrieval_results(results):
    if not results:
        return "No retrieved examples found."

    blocks = []
    for i, r in enumerate(results, 1):
        score = r.get("score", 0.0)
        source = r.get("source", "unknown")
        text = r.get("text", "")
        tagged_text = r.get("tagged_text", "")

        block = (
            f"Rank {i} | score={score:.4f} | source={source}\n"
            f"Sentence: {text}\n"
            f"Annotated:\n{tagged_text}"
        )
        blocks.append(block)

    return "\n\n" + ("\n" + "-" * 70 + "\n\n").join(blocks)


def parse_bio_block(text):
    tokens = []
    tags = []

    for line in (text or "").strip().splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) < 2:
            parts = line.split()

        if len(parts) < 2:
            continue

        token = parts[0].strip()
        tag = parts[-1].strip()

        if token:
            tokens.append(token)
            tags.append(tag)

    return tokens, tags


def normalize_llm_bio_output(raw_text: str):
    """
    Try to keep only BIO lines in format: token<TAB>tag
    Accepts lines with spaces too.
    """
    raw_text = (raw_text or "").strip()
    if not raw_text:
        return ""

    cleaned = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split("\t")
        if len(parts) < 2:
            parts = line.split()

        if len(parts) < 2:
            continue

        token = parts[0].strip()
        tag = parts[-1].strip()

        if token and tag:
            cleaned.append(f"{token}\t{tag}")

    return "\n".join(cleaned)


def predict_xlmr(sentence: str):
    sentence = (sentence or "").strip()
    if not sentence:
        return "Please enter a sentence."

    words = sentence.split()

    inputs = tokenizer(
        words,
        is_split_into_words=True,
        return_tensors="pt",
        truncation=True,
        padding=False,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    predictions = torch.argmax(outputs.logits, dim=-1)[0].tolist()
    word_ids = inputs.word_ids()

    result = []
    previous_word_idx = None

    for token_idx, word_idx in enumerate(word_ids):
        if word_idx is None:
            continue
        if word_idx == previous_word_idx:
            continue

        label_id = predictions[token_idx]
        label = id2label[label_id]
        result.append(f"{words[word_idx]}\t{label}")
        previous_word_idx = word_idx

    return "\n".join(result)

def call_llm_for_ner(prompt):
    if not GROQ_API_KEY or client is None:
        print("GROQ_API_KEY not found")
        return None

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Luxembourgish named entity recognition system. "
                        "Return BIO tags only. "
                        "Output exactly one token per line in this format: token<TAB>tag. "
                        "Do not explain anything."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.0,
        )

        content = response.choices[0].message.content.strip()
        normalized = normalize_llm_bio_output(content)

        return normalized if normalized else content

    except Exception as e:
        print(f"Groq error: {e}")
        return None

def check_llm_status():
    lines = [
        f"GROQ_API_KEY loaded: {'Yes' if bool(GROQ_API_KEY) else 'No'}",
        "LLM provider: Groq",
        "LLM model: llama-3.1-8b-instant",
    ]

    if not GROQ_API_KEY or client is None:
        lines.append("LLM test call: Failed")
        lines.append("Error: GROQ_API_KEY secret is missing.")
        return "\n".join(lines)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Reply with OK only."},
                {"role": "user", "content": "OK"}
            ],
            temperature=0.0,
        )

        reply = response.choices[0].message.content.strip()
        lines.append("LLM test call: Success")
        lines.append(f"LLM response: {reply}")

    except Exception as e:
        lines.append("LLM test call: Failed")
        lines.append(f"Error: {type(e).__name__}: {e}")

    return "\n".join(lines)

    
def predict_rag(query: str, results):
    """
    True RAG flow:
    retrieve -> build prompt -> call LLM
    fallback to XLM-R if LLM fails
    """
    prompt = build_ner_prompt(query, results)
    llm_output = call_llm_for_ner(prompt)

    if llm_output and str(llm_output).strip():
        rag_prediction = str(llm_output).strip()
        mode = "real_llm"
    else:
        rag_prediction = predict_xlmr(query)
        mode = "fallback_xlmr"

    return rag_prediction, prompt, mode


def show_memory_status():
    return (
        f"Base dataset sentences: {len(rag.base_examples)}\n"
        f"Dynamic memory sentences: {len(rag.memory_examples)}\n"
        f"Total indexed sentences: {len(rag.examples)}\n"
        f"Memory file: {MEMORY_PATH}\n"
        f"Approved file: {APPROVED_PATH}\n"
        f"Dataset repo: {DATASET_REPO}\n"
        f"GROQ_API_KEY loaded: {'Yes' if GROQ_API_KEY else 'No'}\n"
        f"LLM provider: Groq\n"
        f"LLM model: llama-3.1-8b-instant"
    )


def sync_file_to_dataset_repo(local_file, repo_file):
    if not HF_API_TOKEN:
        raise RuntimeError("HF_TOKEN secret is missing. Cannot sync to dataset repo.")

    upload_file(
        path_or_fileobj=local_file,
        path_in_repo=repo_file,
        repo_id=DATASET_REPO,
        repo_type="dataset",
        token=HF_API_TOKEN,
        commit_message=f"Update {repo_file} from Space",
    )


def add_prediction_to_memory(predicted_bio):
    predicted_bio = (predicted_bio or "").strip()
    if not predicted_bio:
        return "No prediction available to add."

    tokens, tags = parse_bio_block(predicted_bio)
    if not tokens or len(tokens) != len(tags):
        return "Invalid BIO prediction format."

    try:
        added = rag.add_example(tokens, tags)
        if not added:
            return "Example already exists in base dataset or memory."

        approved_path = Path(APPROVED_PATH)
        with approved_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "tokens": tokens,
                        "tags": tags,
                        "text": " ".join(tokens),
                        "source": "approved",
                    },
                    ensure_ascii=False,
                ) + "\n"
            )

        sync_file_to_dataset_repo(MEMORY_PATH, MEMORY_PATH)
        sync_file_to_dataset_repo(APPROVED_PATH, APPROVED_PATH)

        return (
            f"Added to memory and synced to dataset repo.\n"
            f"Memory size is now {len(rag.memory_examples)}."
        )
    except Exception as e:
        return f"Error while adding to memory: {e}"


def run_static_rag(query, k):
    query = (query or "").strip()
    if not query:
        return "Please enter a Luxembourgish sentence.", ""

    base_results = rag.retrieve_from_base(query, k=int(k))
    prompt = build_ner_prompt(query, base_results)

    return format_retrieval_results(base_results), prompt


def run_dynamic_rag(query, k):
    query = (query or "").strip()
    if not query:
        return "Please enter a Luxembourgish sentence.", "", "", ""

    dynamic_results = rag.retrieve(query, k=int(k))
    rag_prediction, prompt, mode = predict_rag(query, dynamic_results)

    mode_text = (
        "Prediction mode: Real LLM"
        if mode == "real_llm"
        else "Prediction mode: Fallback to XLM-R (LLM unavailable or failed)"
    )

    return (
        format_retrieval_results(dynamic_results),
        prompt,
        rag_prediction,
        mode_text,
    )


def compare_approaches(query, k):
    query = (query or "").strip()
    if not query:
        return "Please enter a sentence.", "", "", ""

    rag_results = rag.retrieve(query, k=int(k))
    rag_prediction, prompt, mode = predict_rag(query, rag_results)
    xlmr_output = predict_xlmr(query)

    mode_text = (
        "RAG mode: Real LLM"
        if mode == "real_llm"
        else "RAG mode: Fallback to XLM-R (LLM unavailable or failed)"
    )

    return (
        rag_prediction,
        xlmr_output,
        prompt,
        format_retrieval_results(rag_results) + "\n\n" + mode_text,
    )


def load_metrics():
    path = Path(METRICS_PATH)
    if not path.exists():
        return (
            "No metrics.json found yet.\n\n"
            "Create a metrics file with your offline evaluation results and upload it to the Space."
        )

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return json.dumps(data, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Could not read metrics.json: {e}"


def load_case_studies_text():
    return (
        "Case Study 1: Both systems are correct\n"
        "Sentence: Den Jean huet Paracetamol zu Esch kaf .\n\n"
        "Gold / Expected:\n"
        "Jean -> PER\n"
        "Paracetamol -> MED\n"
        "Esch -> LOC\n\n"
        "Interpretation:\n"
        "- XLM-R correctly identifies the person, medicine, and location.\n"
        "- RAG also succeeds because similar examples with MED and LOC are likely retrievable.\n"
        "- This is a straightforward in-domain case where both approaches should perform well.\n\n"
        "------------------------------------------------------------\n\n"
        "Case Study 2: XLM-R is better\n"
        "Sentence: D'Konferenz gouf den 12. Mee 2024 zu Lëtzebuerg ofgehalen .\n\n"
        "Gold / Expected:\n"
        "12. Mee 2024 -> DATE\n"
        "Lëtzebuerg -> LOC\n\n"
        "Interpretation:\n"
        "- XLM-R may perform better here because date expressions are regular and well learned during token classification.\n"
        "- RAG may fail if the retrieved examples do not contain a closely matching date format.\n"
        "- This illustrates the strength of a fine-tuned model on structured and frequent entity patterns.\n\n"
        "------------------------------------------------------------\n\n"
        "Case Study 3: RAG is better\n"
        "Sentence: Hien huet Ibuprofen forte zu Ettelbréck kaf .\n\n"
        "Gold / Expected:\n"
        "Ibuprofen forte -> MED\n"
        "Ettelbréck -> LOC\n\n"
        "Interpretation:\n"
        "- RAG may perform better if it retrieves similar annotated medicine phrases from the corpus.\n"
        "- XLM-R may miss or partially tag rare medicine surface forms if they are underrepresented in training.\n"
        "- This highlights the value of retrieval for rare or lexically specific expressions.\n\n"
        "------------------------------------------------------------\n\n"
        "Case Study 4: Noisy survey-style example\n"
        "Sentence: ech hun gëschter paracetamol zu esch geholl an den dr huet mer gesot muer nees ze kommen\n\n"
        "Gold / Expected:\n"
        "paracetamol -> MED\n"
        "esch -> LOC\n\n"
        "Interpretation:\n"
        "- This sentence reflects noisy, non-standard, lower-case, survey-style input.\n"
        "- Both systems may degrade here because the wording is less formal and less similar to curated training examples.\n"
        "- This case is useful for discussing robustness under distribution shift.\n"
    )
    

# =========================
# UI
# =========================

with gr.Blocks(title="LuxNLP: RAG + XLM-R NER") as demo:
    gr.Markdown("# LuxNLP: RAG + XLM-R NER")
    gr.Markdown(
        "This interface combines **Static RAG**, **Dynamic RAG**, **XLM-RoBERTa prediction**, "
        "**side-by-side comparison**, and **precomputed evaluation metrics**."
    )
    gr.Markdown(
        "If a valid Hugging Face token is configured as a Space secret, the RAG branch uses a real LLM endpoint. "
        "Otherwise it falls back to XLM-R so the app remains usable."
    )

    with gr.Tab("Static RAG"):
        gr.Markdown("Retrieve similar BIO-annotated Luxembourgish sentences from the base dataset only.")
        static_query = gr.Textbox(
            label="Luxembourgish sentence",
            placeholder="De Jean schafft zu Lëtzebuerg ."
        )
        static_k = gr.Slider(1, 5, value=3, step=1, label="Top-k examples")
        static_btn = gr.Button("Run Static RAG")
        static_out = gr.Textbox(label="Retrieved Examples", lines=18)
        static_prompt = gr.Textbox(label="Generated Prompt", lines=18)

        static_btn.click(
            run_static_rag,
            inputs=[static_query, static_k],
            outputs=[static_out, static_prompt],
        )

    with gr.Tab("Dynamic RAG"):
        gr.Markdown("Retrieve from the base dataset plus approved new examples stored in dynamic memory.")
        dynamic_query = gr.Textbox(
            label="Luxembourgish sentence",
            placeholder="Hien huet Diabetis an ass zu Esch ."
        )
        dynamic_k = gr.Slider(1, 5, value=3, step=1, label="Top-k examples")
        dynamic_btn = gr.Button("Run Dynamic RAG")

        dynamic_out = gr.Textbox(label="Retrieved Examples", lines=16)
        dynamic_prompt = gr.Textbox(label="Generated Prompt", lines=14)
        predicted_bio = gr.Textbox(label="RAG Prediction", lines=12)
        prediction_mode = gr.Textbox(label="Prediction Mode", lines=2)

        dynamic_btn.click(
            run_dynamic_rag,
            inputs=[dynamic_query, dynamic_k],
            outputs=[dynamic_out, dynamic_prompt, predicted_bio, prediction_mode],
        )

        gr.Markdown("### Memory Update")
        add_btn = gr.Button("Add Prediction to Memory")
        add_status = gr.Textbox(label="Memory Update Status")
        memory_status_btn = gr.Button("Show Memory Status")
        memory_status_box = gr.Textbox(label="Memory Status", lines=8)

        add_btn.click(add_prediction_to_memory, inputs=predicted_bio, outputs=add_status)
        memory_status_btn.click(show_memory_status, outputs=memory_status_box)

    with gr.Tab("XLM-R"):
        gr.Markdown("Run direct BIO prediction using the fine-tuned XLM-RoBERTa model.")
        xlmr_query = gr.Textbox(
            label="Luxembourgish sentence",
            placeholder="D'Maria wunnt zu Dikrech ."
        )
        xlmr_btn = gr.Button("Run XLM-R Prediction")
        xlmr_out = gr.Textbox(label="Predicted BIO Tags", lines=18)

        xlmr_btn.click(
            predict_xlmr,
            inputs=[xlmr_query],
            outputs=[xlmr_out],
        )

    with gr.Tab("Compare"):
        gr.Markdown("Compare **RAG prediction** and **XLM-R prediction** side by side.")
        cmp_query = gr.Textbox(
            label="Luxembourgish sentence",
            placeholder="D'Maria wunnt zu Dikrech ."
        )
        cmp_k = gr.Slider(1, 5, value=3, step=1, label="Top-k examples")
        cmp_btn = gr.Button("Compare")

        with gr.Row():
            cmp_rag = gr.Textbox(label="RAG Prediction", lines=22)
            cmp_xlmr = gr.Textbox(label="XLM-R Prediction", lines=22)

        cmp_prompt = gr.Textbox(label="Generated RAG Prompt", lines=10)
        cmp_retrieval = gr.Textbox(label="Retrieved Examples and Mode", lines=18)

        cmp_btn.click(
            compare_approaches,
            inputs=[cmp_query, cmp_k],
            outputs=[cmp_rag, cmp_xlmr, cmp_prompt, cmp_retrieval],
        )

    with gr.Tab("Metrics"):
        gr.Markdown(
            "This tab shows precomputed evaluation results such as precision, recall, F1, and accuracy. "
            "These metrics should be calculated offline on gold-labeled data."
        )
        
        metrics_btn = gr.Button("Load Metrics")
        metrics_box = gr.Textbox(label="Evaluation Metrics", lines=20)

        metrics_btn.click(load_metrics, outputs=metrics_box)

    with gr.Tab("Case Studies"):
        gr.Markdown(
            "Representative qualitative comparison cases for presentation and discussion."
        )
        case_studies_box = gr.Textbox(
            label="Case Studies",
            value=load_case_studies_text(),
            lines=28
        )

    with gr.Tab("LLM Debug"):
        gr.Markdown("Use this tab to verify whether the Hugging Face LLM endpoint is working.")
        debug_btn = gr.Button("Check LLM")
        debug_box = gr.Textbox(label="LLM Debug Status", lines=10)
        debug_btn.click(check_llm_status, outputs=debug_box)

demo.launch()
