


import argparse
import json
import re
from collections import defaultdict

#  tokenizer 

TOKEN_RE = re.compile(r"\w+|\S", re.UNICODE)

def tokenize(text: str):
    return TOKEN_RE.findall(text)


# gazetteer loading  

def add_phrase(gazetteer, tokens, label):
    key = tuple(t.lower() for t in tokens)
    if key:
        gazetteer[key] = label


def load_wikidata(path: str):
    """
    Expects JSONL with at least: label_lb, ner_tag
    """
    gaz = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            surface = obj.get("label_lb")
            label = obj.get("ner_tag")
            if not surface or not label:
                continue
            tokens = tokenize(surface)
            add_phrase(gaz, tokens, label)
    return gaz


def load_lod(path: str):
    """
    Expects JSONL with at least: lemma_lb, categories
    We map some categories to NER labels.
    Adjust category_to_ner if you like.
    """
    category_to_ner = {
        "ANAT": "ANAT",
        "MED": "MED",
        "BIO": "BIO",
        "CHEM": "CHEM",
    }

    gaz = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            lemma = obj.get("lemma_lb")
            cats = obj.get("categories", [])
            if not lemma:
                continue

            ner = None
            for c in cats:
                if c in category_to_ner:
                    ner = category_to_ner[c]
                    break
            if not ner:
                continue

            tokens = tokenize(lemma)
            add_phrase(gaz, tokens, ner)
    return gaz


def merge_gazetteers(*gazetteers):
    merged = {}
    for g in gazetteers:
        for phrase, label in g.items():
            merged.setdefault(phrase, label)
    return merged


#  matching + BIO tagging 

def build_length_index(gaz):
    idx = defaultdict(dict)
    for phrase, label in gaz.items():
        idx[len(phrase)][phrase] = label
    return idx


def tag_sentence(tokens, length_index):
    n = len(tokens)
    tags = ["O"] * n
    if not length_index:
        return tags

    lower = [t.lower() for t in tokens]
    max_len = max(length_index.keys())

    i = 0
    while i < n:
        matched = False
        for L in range(min(max_len, n - i), 0, -1):
            span = tuple(lower[i:i+L])
            label = length_index[L].get(span)
            if label:
                tags[i] = f"B-{label}"
                for j in range(i+1, i+L):
                    tags[j] = f"I-{label}"
                i += L
                matched = True
                break
        if not matched:
            i += 1
    return tags


# Leipzig sentence reader 

def iter_sentences(path: str):
    """
    Your file: each line is exactly one sentence.
    No ID column, no tab – we just strip and tokenize.
    """
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens = tokenize(line)
            yield tokens


# main 

def main(args):
    print("Loading gazetteers...")

    gaz_wiki = load_wikidata(args.wikidata)
    gaz_lod = load_lod(args.lod)

    gaz = merge_gazetteers(gaz_wiki, gaz_lod)
    print(f"  Wikidata entries : {len(gaz_wiki)}")
    print(f"  LOD entries      : {len(gaz_lod)}")
    print(f"  Total phrases    : {len(gaz)}")

    length_index = build_length_index(gaz)

    print("Tagging sentences and writing CoNLL...")
    sent_count = 0
    tok_count = 0
    ent_tok_count = 0

    with open(args.output, "w", encoding="utf-8") as out_f:
        for tokens in iter_sentences(args.sentences):
            tags = tag_sentence(tokens, length_index)

            for tok, tag in zip(tokens, tags):
                out_f.write(f"{tok}\t{tag}\n")
                tok_count += 1
                if tag != "O":
                    ent_tok_count += 1
            out_f.write("\n")
            sent_count += 1

    print("DONE.")
    print(f"Sentences     : {sent_count}")
    print(f"Tokens        : {tok_count}")
    print(f"Entity tokens : {ent_tok_count}")
    print(f"Output file   : {args.output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentences", required=True,
                        help="Leipzig sentences file (one sentence per line)")
    parser.add_argument("--lod", required=True,
                        help="LOD JSONL with lemma_lb + categories")
    parser.add_argument("--wikidata", required=True,
                        help="Wikidata JSONL with label_lb + ner_tag")
    parser.add_argument("--output", required=True,
                        help="Output CoNLL file")
    main(parser.parse_args())
