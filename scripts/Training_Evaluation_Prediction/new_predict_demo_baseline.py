from transformers import (AutoModelForTokenClassification, AutoTokenizer,
                          pipeline)

MODEL = "Davlan/xlm-roberta-base-ner-hrl"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForTokenClassification.from_pretrained(MODEL)

ner = pipeline(
    "ner",
    model=model,
    tokenizer=tokenizer,
    aggregation_strategy="simple"
)

tests = [
    "Den 12. Mee 2024 war d'Nationalfeierdag zu Lëtzebuerg.",
    "Ech schaffen bei Luxembourg Air Rescue zu Sandweiler.",
    "Jean-Claude Juncker war Premierminister vu Lëtzebuerg.",
    "E Concert ass den 15. August 2026 zu Esch."
]

for text in tests:
    print("\nTEXT:", text)
    for ent in ner(text):
        print(ent["word"], ent["entity_group"], round(ent["score"], 3))
