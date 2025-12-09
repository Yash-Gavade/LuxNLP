import xml.etree.ElementTree as ET

XML_PATH = r"D:\DOWNLOADS\BRAVE\LuxNLP\data\raw\Lod.lu_250804-new-lod-art\new_lod-art.xml"

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[-1]

def print_entry(entry, max_depth=3, indent=0):
    """Pretty-print one <entry> subtree (limited depth)."""
    if indent > max_depth:
        return
    tag = strip_ns(entry.tag)
    attrs = dict(entry.attrib)
    text = (entry.text or "").strip()
    indent_str = "  " * indent
    print(f"{indent_str}<{tag} attrs={attrs}> text={text[:80]!r}")
    for child in list(entry):
        print_entry(child, max_depth=max_depth, indent=indent+1)

def main():
    print(f"Loading XML: {XML_PATH}")
    tree = ET.parse(XML_PATH)
    root = tree.getroot()

    # get first few <entry> elements
    entries = [el for el in root.iter() if strip_ns(el.tag) == "entry"]
    print(f"Found {len(entries)} <entry> elements\n")

    for i, e in enumerate(entries[:3], start=1):
        print(f"\n=== ENTRY {i} ===")
        print_entry(e, max_depth=4)

if __name__ == "__main__":
    main()
