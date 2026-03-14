import os

from pypdf import PdfReader  # pip install pypdf

PDF_PATH = r"D:\DOWNLOADS\BRAVE\LuxNLP\scripts\Lb_Bible.pdf"    # corrected path
OUTPUT_TXT = "data/raw/lb_bible_raw.txt"

os.makedirs(os.path.dirname(OUTPUT_TXT), exist_ok=True)

def main():
    reader = PdfReader(PDF_PATH)
    lines = []

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        # remove soft hyphens etc.
        text = text.replace("\u00ad", "")

        lines.append(f"### PAGE {i}\n{text}\n")

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Extracted {len(lines)} pages.")
    print(f"Saved: {OUTPUT_TXT}")

if __name__ == "__main__":
    main()
