# scripts/new_conll_stats.py
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import List, Tuple

from new_conll_io import Sentence, read_conll


def _etype(tag: str) -> str | None:
    if tag == "O":
        return None
    if "-" in tag:
        return tag.split("-", 1)[1]
    return tag

def _has_any_entity(sent: Sentence) -> bool:
    return any(tag != "O" for _, tag in sent)

def _extract_entities(sent: Sentence) -> list[tuple[str, int, int]]:
    """
    Returns list of (etype, start_idx, end_idx_inclusive)
    BIO only (best-effort; ignores broken spans).
    """
    ents = []
    i = 0
    while i < len(sent):
        tok, tag = sent[i]
        if tag.startswith("B-"):
            et = tag.split("-", 1)[1]
            j = i + 1
            while j < len(sent) and sent[j][1] == f"I-{et}":
                j += 1
            ents.append((et, i, j - 1))
            i = j
        else:
            i += 1
    return ents

def conll_stats(path: str | Path, title: str = "") -> dict:
    sents = read_conll(path)
    tag_counts = Counter()
    etok_counts = Counter()
    ent_counts = Counter()
    sent_entity_counts = Counter()

    for sent in sents:
        for _, tag in sent:
            tag_counts[tag] += 1
            et = _etype(tag)
            if et:
                etok_counts[et] += 1

        # sentence-level label presence (collapsed)
        present = set()
        for _, tag in sent:
            et = _etype(tag)
            if et:
                present.add(et)
        for et in present:
            sent_entity_counts[et] += 1

        # entity spans
        for et, _, _ in _extract_entities(sent):
            ent_counts[et] += 1

    total_tokens = sum(tag_counts.values())
    total_sents = len(sents)
    total_entity_tokens = sum(etok_counts.values())

    report = {
        "title": title,
        "path": str(path),
        "total_sentences": total_sents,
        "total_tokens": total_tokens,
        "tag_counts": tag_counts,
        "entity_token_counts": etok_counts,
        "entity_span_counts": ent_counts,
        "sentences_with_type": sent_entity_counts,
        "pct_O": (tag_counts["O"] / total_tokens * 100) if total_tokens else 0.0,
        "pct_entity_tokens": (total_entity_tokens / total_tokens * 100) if total_tokens else 0.0,
        "sentences_with_any_entity": sum(1 for s in sents if _has_any_entity(s)),
    }
    return report

def print_stats(report: dict, topk_tags: int = 20) -> None:
    from math import isfinite
    print("\n" + "=" * 80)
    if report.get("title"):
        print(report["title"])
    print(f"File: {report['path']}")
    print(f"Sentences: {report['total_sentences']}")
    print(f"Tokens:    {report['total_tokens']}")
    print(f"Sentences with any entity: {report['sentences_with_any_entity']}")
    print(f"O%: {report['pct_O']:.2f}% | Entity-token%: {report['pct_entity_tokens']:.2f}%")

    print("\nTop BIO tags:")
    tc = report["tag_counts"]
    total = report["total_tokens"] or 1
    for tag, c in tc.most_common(topk_tags):
        print(f"  {tag:10s}  {c:8d}  ({c/total*100:6.2f}%)")

    print("\nEntity-token counts (collapsed B/I):")
    etc = report["entity_token_counts"]
    for et, c in etc.most_common():
        print(f"  {et:10s}  {c:8d}  ({c/total*100:6.2f}%)")

    print("\n#Entity spans by type:")
    esc = report["entity_span_counts"]
    for et, c in esc.most_common():
        print(f"  {et:10s}  {c:8d}")

    print("\n#Sentences containing type:")
    swt = report["sentences_with_type"]
    for et, c in swt.most_common():
        print(f"  {et:10s}  {c:8d}")

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--conll", required=True)
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    rep = conll_stats(args.conll, title=args.title)
    print_stats(rep)
