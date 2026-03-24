from pathlib import Path

# change if needed
input_conll = Path("LuxNLP-main/data/processed/Lux_Final.conll")
output_txt = Path("LuxNLP-main/data/processed/Lux_Final_sentences.txt")


def detokenize(tokens):
    text = ""
    no_space_before = {".", ",", "!", "?", ";", ":", "%", ")", "]", "}", "»"}
    no_space_after = {"(", "[", "{", "«"}

    for tok in tokens:
        if not text:
            text = tok
        elif tok in no_space_before:
            text += tok
        elif text[-1] in no_space_after:
            text += tok
        else:
            text += " " + tok
    return text.strip()


sentences = []
current_tokens = []

with open(input_conll, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        # blank line = end of sentence
        if not line:
            if current_tokens:
                sentences.append(detokenize(current_tokens))
                current_tokens = []
            continue

        parts = line.split()

        # first column is token
        token = parts[0]
        current_tokens.append(token)

# last sentence if file doesn't end with blank line
if current_tokens:
    sentences.append(detokenize(current_tokens))

with open(output_txt, "w", encoding="utf-8") as f:
    for sent in sentences:
        f.write(sent + "\n")

print(f"Done. Saved {len(sentences)} sentences to: {output_txt}")