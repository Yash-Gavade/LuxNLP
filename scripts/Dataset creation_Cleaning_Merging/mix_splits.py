import random
from pathlib import Path

# -----------------------------
# EDIT THESE
# -----------------------------
OLD_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\new_pipeline_v2\BALANCED_4K6K_FOCUS"
NEW_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\generated_hard_splits"
OUT_DIR = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\processed\mixed_splits"

# Choose mix ratio:
# 0.5 = 50% old + 50% new
# 0.7 = 70% old + 30% new   (recommended)
OLD_RATIO = 0.8

# Keep same size as old splits
DEV_SIZE = 9644
TEST_SIZE = 9646

SEED = 42

OLD_DEV = str(Path(OLD_DIR) / "dev.conll")
OLD_TEST = str(Path(OLD_DIR) / "test.conll")
NEW_DEV = str(Path(NEW_DIR) / "dev_generated.conll")
NEW_TEST = str(Path(NEW_DIR) / "test_generated.conll")


# -----------------------------
# Helpers
# -----------------------------
def read_conll_sentences(path):
    sents, cur = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                if cur:
                    sents.append(cur)
                    cur = []
            else:
                cur.append(line.rstrip("\n"))
    if cur:
        sents.append(cur)
    return sents

def sent_text(sent):
    return " ".join(line.split()[0] for line in sent).strip().lower()

def write_conll(path, sents):
    with open(path, "w", encoding="utf-8") as f:
        for sent in sents:
            for line in sent:
                f.write(line + "\n")
            f.write("\n")


def sample_mixed(old_sents, new_sents, total, old_ratio):
    n_old = int(total * old_ratio)
    n_new = total - n_old

    random.shuffle(old_sents)
    random.shuffle(new_sents)

    out = []
    seen = set()

    # take old first
    for s in old_sents:
        if len(out) >= n_old:
            break
        t = sent_text(s)
        if t in seen:
            continue
        seen.add(t)
        out.append(s)

    # fill with new
    for s in new_sents:
        if len(out) >= n_old + n_new:
            break
        t = sent_text(s)
        if t in seen:
            continue
        seen.add(t)
        out.append(s)

    # if still short, top up from old then new (rare)
    for pool in (old_sents, new_sents):
        for s in pool:
            if len(out) >= total:
                break
            t = sent_text(s)
            if t in seen:
                continue
            seen.add(t)
            out.append(s)

    return out


def main():
    random.seed(SEED)

    old_dev = read_conll_sentences(OLD_DEV)
    old_test = read_conll_sentences(OLD_TEST)
    new_dev = read_conll_sentences(NEW_DEV)
    new_test = read_conll_sentences(NEW_TEST)

    out_dir = Path(OUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    dev_mixed = sample_mixed(old_dev, new_dev, DEV_SIZE, OLD_RATIO)
    test_mixed = sample_mixed(old_test, new_test, TEST_SIZE, OLD_RATIO)

    dev_path = out_dir / "dev_mixed.conll"
    test_path = out_dir / "test_mixed.conll"

    write_conll(dev_path, dev_mixed)
    write_conll(test_path, test_mixed)

    print("✅ Done")
    print("DEV:", dev_path)
    print("TEST:", test_path)
    print(f"Mix: {int(OLD_RATIO*100)}% old + {int((1-OLD_RATIO)*100)}% new")

if __name__ == "__main__":
    main()
