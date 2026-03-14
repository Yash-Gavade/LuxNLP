import torch
from transformers import AutoModelForTokenClassification, AutoTokenizer

MODEL_DIR = "models/xlmr_ner_final"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_DIR)
id2label = model.config.id2label

def predict(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**tokens).logits
    preds = torch.argmax(outputs, dim=-1)[0].tolist()
    words = tokenizer.convert_ids_to_tokens(tokens["input_ids"][0])
    result = []
    for w, p in zip(words, preds):
        if w.startswith("▁"):
            result.append((w[1:], id2label[p]))
    return result

tests = [
    "Den 12. Mee 2024 war d'Nationalfeierdag zu Lëtzebuerg .",
    "Ech schaffen bei Luxembourg Air Rescue zu Sandweiler .",
    "Zu Esch fënnt de Summerfestival 2023 statt .",
    "De Jean-Claude Juncker war Premierminister .",
    "Den Dokter huet Coronavirus diagnostizéiert .",
]

for t in tests:
    print("\nTEXT:", t)
    for w, l in predict(t):
        print(f"{w:15} {l}")
