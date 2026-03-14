import re
import random
from collections import Counter, defaultdict
from pathlib import Path

# -----------------------------
# EDIT PATHS
# -----------------------------
OLD_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\new_pipeline_v2\BALANCED_4K6K_FOCUS"
NEW_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\generated_hard_splits"

# Where to write mixed splits
MIXED_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\mixed_splits"

# Mix ratio:
# 0.5 => 50% old + 50% new
# 0.7 => 70% old + 30% new  (recommended)
OLD_RATIO = 0.8

SEED = 42
MAKE_MIXED_FILES = True  # set False if you only want stats

OLD_TRAIN = str(Path(OLD_DIR) / "train.conll")
OLD_DEV   = str(Path(OLD_DIR) / "dev.conll")
OLD_TEST  = str(Path(OLD_DIR) / "test.conll")

NEW_DEV = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\new_pipeline_v2\BALANCED_4K6K_FOCUS\dev_mixed_3000.conll"
NEW_TEST = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\new_pipeline_v2\BALANCED_4K6K_FOCUS\test_mixed_3000.conll"


MIXED_DEV = str(Path(MIXED_DIR) / "dev_mixed.conll")
MIXED_TEST = str(Path(MIXED_DIR) / "test_mixed.conll")


# -----------------------------
# CoNLL parsing
# -----------------------------
def read_conll(path: str):
    """
    Returns list of sentences, where each sentence is list of (token, tag).
    Tag is last column. Token is first column.
    """
    sents = []
    cur = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sents.append(cur)
                    cur = []
                continue
            parts = line.split()
            token = parts[0]
            tag = parts[-1]
            cur.append((token, tag))
    if cur:
        sents.append(cur)
    return sents

def write_conll(path: str, sents):
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for sent in sents:
            for tok, tag in sent:
                f.write(f"{tok} {tag}\n")
            f.write("\n")

def sent_text(sent):
    # normalized text based only on tokens
    return " ".join(tok for tok, _ in sent).strip().lower()

def sample_mixed(old_sents, new_sents, total, old_ratio, seed=42):
    """
    Build a mixed split with total sentences:
      old_ratio portion from old, rest from new
    Keeps unique sentences by token text.
    """
    rnd = random.Random(seed)
    old = old_sents[:]
    new = new_sents[:]
    rnd.shuffle(old)
    rnd.shuffle(new)

    n_old = int(total * old_ratio)
    n_new = total - n_old

    out = []
    seen = set()

    # take old first
    for s in old:
        if len(out) >= n_old:
            break
        t = sent_text(s)
        if t in seen:
            continue
        seen.add(t)
        out.append(s)

    # then new
    for s in new:
        if len(out) >= n_old + n_new:
            break
        t = sent_text(s)
        if t in seen:
            continue
        seen.add(t)
        out.append(s)

    # top-up if needed
    for pool in (old, new):
        for s in pool:
            if len(out) >= total:
                break
            t = sent_text(s)
            if t in seen:
                continue
            seen.add(t)
            out.append(s)

    return out

def extract_spans(sent):
    """
    Extract entity spans from BIO tags.
    Returns list of (type, surface_text).
    """
    spans = []
    cur_tokens = []
    cur_type = None

    def flush():
        nonlocal cur_tokens, cur_type
        if cur_tokens and cur_type:
            spans.append((cur_type, " ".join(cur_tokens)))
        cur_tokens = []
        cur_type = None

    for tok, tag in sent:
        if tag == "O":
            flush()
            continue
        m = re.match(r"^(B|I)-(.+)$", tag)
        if not m:
            flush()
            continue
        bi, typ = m.group(1), m.group(2)

        if bi == "B":
            flush()
            cur_tokens = [tok]
            cur_type = typ
        else:  # I
            if cur_type == typ and cur_tokens:
                cur_tokens.append(tok)
            else:
                flush()
                cur_tokens = [tok]
                cur_type = typ

    flush()
    return spans

def stats_for_file(path: str):
    sents = read_conll(path)
    return stats_for_sents(path, sents)

def stats_for_sents(name_or_path: str, sents):
    n_sents = len(sents)
    n_tokens = sum(len(s) for s in sents)

    tag_counts = Counter()
    type_token_counts = Counter()
    span_counts = Counter()
    unique_entities = defaultdict(set)

    for sent in sents:
        for tok, tag in sent:
            tag_counts[tag] += 1
            m = re.match(r"^[BI]-(.+)$", tag)
            if m:
                type_token_counts[m.group(1)] += 1

        spans = extract_spans(sent)
        for typ, surface in spans:
            span_counts[typ] += 1
            unique_entities[typ].add(surface)

    label_types = sorted({re.sub(r"^[BI]-", "", t) for t in tag_counts.keys() if t.startswith(("B-","I-"))})

    return {
        "path": name_or_path,
        "sentences": n_sents,
        "tokens": n_tokens,
        "tag_counts": tag_counts,
        "label_types": label_types,
        "type_token_counts": type_token_counts,
        "span_counts": span_counts,
        "unique_entities": {k: len(v) for k, v in unique_entities.items()},
    }

def print_summary(name: str, st):
    print(f"\n=== {name} ===")
    print(f"File: {st['path']}")
    print(f"Sentences: {st['sentences']}")
    print(f"Tokens:    {st['tokens']}")
    print(f"Label types (from BIO): {st['label_types'] or ['(none)']}")

    o = st["tag_counts"].get("O", 0)
    ent = st["tokens"] - o
    if st["tokens"] > 0:
        print(f"O tokens:  {o}  ({o/st['tokens']:.2%})")
        print(f"ENT tokens:{ent} ({ent/st['tokens']:.2%})")

    if st["span_counts"]:
        print("\nPer-type entity spans / unique entities / entity-token-count:")
        for typ in sorted(st["span_counts"].keys()):
            print(f"  {typ:<12} spans={st['span_counts'][typ]:>6} | unique={st['unique_entities'].get(typ,0):>6} | ent_tokens={st['type_token_counts'].get(typ,0):>7}")

    print("\nTop tags (up to 15):")
    for tag, c in st["tag_counts"].most_common(15):
        print(f"  {tag:<12} {c}")

def compare_splits(a_name, a, b_name, b):
    print(f"\n=== Compare: {a_name} vs {b_name} ===")
    print(f"Sentences: {a['sentences']}  vs  {b['sentences']}  (Δ {b['sentences']-a['sentences']:+})")
    print(f"Tokens:    {a['tokens']}  vs  {b['tokens']}  (Δ {b['tokens']-a['tokens']:+})")

    a_types = set(a["label_types"])
    b_types = set(b["label_types"])
    print(f"Label types only in {a_name}: {sorted(a_types - b_types)}")
    print(f"Label types only in {b_name}: {sorted(b_types - a_types)}")

    all_types = sorted(set(a["type_token_counts"].keys()) | set(b["type_token_counts"].keys()))
    if all_types:
        print("\nEntity-token-count by TYPE:")
        for typ in all_types:
            print(f"  {typ:<12} {a_name}={a['type_token_counts'].get(typ,0):>7} | {b_name}={b['type_token_counts'].get(typ,0):>7}")

def main():
    # Old
    old_train = stats_for_file(OLD_TRAIN)
    old_dev   = stats_for_file(OLD_DEV)
    old_test  = stats_for_file(OLD_TEST)

    # New
    new_dev   = stats_for_file(NEW_DEV)
    new_test  = stats_for_file(NEW_TEST)

    # Optionally create mixed splits
    mixed_dev_stats = None
    mixed_test_stats = None

    if MAKE_MIXED_FILES:
        random.seed(SEED)

        old_dev_sents = read_conll(OLD_DEV)
        old_test_sents = read_conll(OLD_TEST)
        new_dev_sents = read_conll(NEW_DEV)
        new_test_sents = read_conll(NEW_TEST)

        dev_total = len(old_dev_sents)
        test_total = len(old_test_sents)

        mixed_dev_sents = sample_mixed(old_dev_sents, new_dev_sents, dev_total, OLD_RATIO, seed=SEED)
        mixed_test_sents = sample_mixed(old_test_sents, new_test_sents, test_total, OLD_RATIO, seed=SEED)

        write_conll(MIXED_DEV, mixed_dev_sents)
        write_conll(MIXED_TEST, mixed_test_sents)

        mixed_dev_stats = stats_for_sents(MIXED_DEV, mixed_dev_sents)
        mixed_test_stats = stats_for_sents(MIXED_TEST, mixed_test_sents)

    # Print summaries
    print_summary("OLD TRAIN", old_train)
    print_summary("OLD DEV", old_dev)
    print_summary("OLD TEST", old_test)

    print_summary("NEW DEV (generated)", new_dev)
    print_summary("NEW TEST (generated)", new_test)

    if mixed_dev_stats and mixed_test_stats:
        print_summary(f"MIXED DEV ({int(OLD_RATIO*100)}% old + {int((1-OLD_RATIO)*100)}% new)", mixed_dev_stats)
        print_summary(f"MIXED TEST ({int(OLD_RATIO*100)}% old + {int((1-OLD_RATIO)*100)}% new)", mixed_test_stats)

        # Comparisons
        compare_splits("OLD DEV", old_dev, "MIXED DEV", mixed_dev_stats)
        compare_splits("OLD TEST", old_test, "MIXED TEST", mixed_test_stats)

        compare_splits("NEW DEV", new_dev, "MIXED DEV", mixed_dev_stats)
        compare_splits("NEW TEST", new_test, "MIXED TEST", mixed_test_stats)

        print(f"\n✅ Mixed files written to:\n  {MIXED_DEV}\n  {MIXED_TEST}")

    # Old vs New comparisons
    compare_splits("OLD DEV", old_dev, "NEW DEV", new_dev)
    compare_splits("OLD TEST", old_test, "NEW TEST", new_test)

    print("\n✅ Done.")

if __name__ == "__main__":
    main()
