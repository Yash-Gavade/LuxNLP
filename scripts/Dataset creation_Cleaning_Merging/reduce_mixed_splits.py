import random
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
SEED = 42
DEV_TARGET = 3000
TEST_TARGET = 3000

BASE_DIR = Path(r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\new_pipeline_v2\BALANCED_4K6K_FOCUS")

DEV_IN  = BASE_DIR / "dev_mixed.conll"
TEST_IN = BASE_DIR / "test_mixed.conll"

DEV_OUT  = BASE_DIR / f"dev_mixed_{DEV_TARGET}.conll"
TEST_OUT = BASE_DIR / f"test_mixed_{TEST_TARGET}.conll"


# -----------------------------
# Helpers
# -----------------------------
def read_conll_sentences(path: Path):
    sents, cur = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                if cur:
                    sents.append(cur)
                    cur = []
            else:
                cur.append(line)
    if cur:
        sents.append(cur)
    return sents

def write_conll_sentences(path: Path, sents):
    with open(path, "w", encoding="utf-8") as f:
        for sent in sents:
            for line in sent:
                f.write(line + "\n")
            f.write("\n")

def sent_text(sent):
    # normalized token-only text for dedup
    toks = []
    for ln in sent:
        parts = ln.split()
        if parts:
            toks.append(parts[0])
    return " ".join(toks).strip().lower()

def sample_unique(sents, target, seed=42):
    rnd = random.Random(seed)
    shuffled = sents[:]
    rnd.shuffle(shuffled)

    out = []
    seen = set()
    for s in shuffled:
        t = sent_text(s)
        if not t or t in seen:
            continue
        seen.add(t)
        out.append(s)
        if len(out) >= target:
            break

    if len(out) < target:
        print(f"[WARN] Only got {len(out)}/{target} unique sentences.")

    return out


def main():
    if not DEV_IN.exists():
        raise FileNotFoundError(f"Missing: {DEV_IN}")
    if not TEST_IN.exists():
        raise FileNotFoundError(f"Missing: {TEST_IN}")

    dev_sents = read_conll_sentences(DEV_IN)
    test_sents = read_conll_sentences(TEST_IN)

    print(f"Read DEV : {len(dev_sents)} sentences from {DEV_IN}")
    print(f"Read TEST: {len(test_sents)} sentences from {TEST_IN}")

    dev_small = sample_unique(dev_sents, DEV_TARGET, seed=SEED)
    test_small = sample_unique(test_sents, TEST_TARGET, seed=SEED + 1)  # different shuffle

    write_conll_sentences(DEV_OUT, dev_small)
    write_conll_sentences(TEST_OUT, test_small)

    print("\n✅ Wrote reduced splits:")
    print("DEV :", DEV_OUT, "->", len(dev_small), "sentences")
    print("TEST:", TEST_OUT, "->", len(test_small), "sentences")


if __name__ == "__main__":
    main()
