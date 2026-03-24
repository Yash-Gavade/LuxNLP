from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class SentenceExample:
    tokens: List[str]
    tags: List[str]
    source: str = "base"

    @property
    def text(self) -> str:
        return " ".join(self.tokens)

    @property
    def tagged_text(self) -> str:
        return "\n".join(f"{tok}\t{tag}" for tok, tag in zip(self.tokens, self.tags))


def load_conll(path: str | Path, source: str = "base") -> List[SentenceExample]:
    path = Path(path)
    examples: List[SentenceExample] = []
    tokens: List[str] = []
    tags: List[str] = []

    if not path.exists():
        return examples

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            line = raw.strip()

            if not line:
                if tokens:
                    examples.append(SentenceExample(tokens=tokens, tags=tags, source=source))
                    tokens, tags = [], []
                continue

            parts = line.split("\t")
            if len(parts) < 2:
                parts = line.split()

            if len(parts) < 2:
                continue

            token = parts[0]
            tag = parts[-1]

            tokens.append(token)
            tags.append(tag)

    if tokens:
        examples.append(SentenceExample(tokens=tokens, tags=tags, source=source))

    return examples


def load_jsonl_memory(path: str | Path) -> List[SentenceExample]:
    path = Path(path)
    examples: List[SentenceExample] = []

    if not path.exists():
        return examples

    with path.open("r", encoding="utf-8") as f:
        for raw in f:
            raw = raw.strip()
            if not raw:
                continue

            obj = json.loads(raw)
            tokens = obj.get("tokens", [])
            tags = obj.get("tags", [])
            source = obj.get("source", "memory")

            if tokens and tags and len(tokens) == len(tags):
                examples.append(SentenceExample(tokens=tokens, tags=tags, source=source))

    return examples


class DynamicLuxRAG:
    def __init__(self, conll_path: str | Path, memory_path: str | Path):
        self.conll_path = Path(conll_path)
        self.memory_path = Path(memory_path)

        self.base_examples: List[SentenceExample] = load_conll(self.conll_path, source="base")
        self.memory_examples: List[SentenceExample] = load_jsonl_memory(self.memory_path)

        self.examples: List[SentenceExample] = []
        self.base_vectorizer: TfidfVectorizer | None = None
        self.base_embeddings = None
        self.vectorizer: TfidfVectorizer | None = None
        self.embeddings = None

        self.rebuild_index()

    def rebuild_index(self):
        self.examples = self.base_examples + self.memory_examples

        # Base-only index
        base_texts = [ex.text for ex in self.base_examples] if self.base_examples else [""]
        self.base_vectorizer = TfidfVectorizer(lowercase=True, analyzer="word", ngram_range=(1, 2))
        self.base_embeddings = self.base_vectorizer.fit_transform(base_texts)

        # Full index (base + memory)
        all_texts = [ex.text for ex in self.examples] if self.examples else [""]
        self.vectorizer = TfidfVectorizer(lowercase=True, analyzer="word", ngram_range=(1, 2))
        self.embeddings = self.vectorizer.fit_transform(all_texts)

    def _retrieve_with_index(self, query: str, examples: List[SentenceExample], vectorizer, embeddings, k: int = 3):
        if not examples:
            return []

        query_emb = vectorizer.transform([query])
        scores = cosine_similarity(query_emb, embeddings)[0]
        top_idx = np.argsort(scores)[::-1][:k]

        results: List[Dict[str, Any]] = []
        for idx in top_idx:
            ex = examples[idx]
            results.append(
                {
                    "index": int(idx),
                    "score": float(scores[idx]),
                    "text": ex.text,
                    "tokens": ex.tokens,
                    "tags": ex.tags,
                    "tagged_text": ex.tagged_text,
                    "source": ex.source,
                }
            )
        return results

    def retrieve(self, query: str, k: int = 3):
        return self._retrieve_with_index(query, self.examples, self.vectorizer, self.embeddings, k=k)

    def retrieve_from_base(self, query: str, k: int = 3):
        return self._retrieve_with_index(query, self.base_examples, self.base_vectorizer, self.base_embeddings, k=k)

    def _make_key(self, tokens: List[str]) -> str:
        return " ".join(tokens).strip().casefold()

    def add_example(self, tokens: List[str], tags: List[str]) -> bool:
        if not tokens or not tags or len(tokens) != len(tags):
            raise ValueError("Invalid tokens/tags.")

        new_key = self._make_key(tokens)

        for ex in self.examples:
            if self._make_key(ex.tokens) == new_key:
                return False

        example = SentenceExample(tokens=tokens, tags=tags, source="memory")
        self.memory_examples.append(example)

        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        with self.memory_path.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps(
                    {
                        "tokens": tokens,
                        "tags": tags,
                        "source": "memory",
                        "text": " ".join(tokens),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )

        self.rebuild_index()
        return True


def build_ner_prompt(query: str, retrieved_examples: List[Dict[str, Any]]) -> str:
    blocks = []

    for i, ex in enumerate(retrieved_examples, start=1):
        block = (
            f"Example {i} (source={ex['source']})\n"
            f"Sentence: {ex['text']}\n"
            f"Annotated:\n{ex['tagged_text']}"
        )
        blocks.append(block)

    joined_examples = "\n\n".join(blocks)

    prompt = f"""
You are an NLP assistant for Luxembourgish named entity recognition.
Your task is to assign one BIO label to each token in the NEW SENTENCE.

Rules:
- Keep the original token order.
- Output exactly one line per token.
- Use the format: token<TAB>tag
- Do not explain anything.
- Use only BIO tags that fit the examples.

Retrieved similar annotated examples:

{joined_examples}

NEW SENTENCE:
{query}

Return only the token-tag lines for the NEW SENTENCE.
""".strip()

    return prompt