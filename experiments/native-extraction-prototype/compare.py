"""THROWAWAY: compare native extraction signals on the Stage 05 corpus."""

import json
import re
import subprocess
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "output/pdf/stage-05-corpus"
MANIFEST = json.loads((ROOT / "docs/evaluation/stage-05-corpus-manifest.json").read_text())


def poppler(path):
    start = time.perf_counter()
    text = subprocess.run(
        ["pdftotext", "-cropbox", str(path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    xml = subprocess.run(
        ["pdftotext", "-cropbox", "-bbox-layout", str(path), "-"],
        capture_output=True, text=True, check=True,
    ).stdout
    elapsed = time.perf_counter() - start
    root = ET.fromstring(xml)
    pages = []
    for page in root.iter("{http://www.w3.org/1999/xhtml}page"):
        words = [
            {"text": word.text or "", "box": [float(word.attrib[k]) for k in ("xMin", "yMin", "xMax", "yMax")]}
            for word in page.iter("{http://www.w3.org/1999/xhtml}word")
        ]
        pages.append({"width": float(page.attrib["width"]), "height": float(page.attrib["height"]), "words": words})
    return text, pages, elapsed


def mupdf(path):
    start = time.perf_counter()
    result = []
    with pymupdf.open(path) as doc:
        for page in doc:
            blocks = page.get_text("dict")["blocks"]
            words = [
                {"text": word[4], "box": list(pymupdf.Rect(word[:4]) * page.rotation_matrix)}
                for word in page.get_text("words")
            ]
            result.append({
                "text": page.get_text("text"),
                "width": page.rect.width,
                "height": page.rect.height,
                "rotation": page.rotation,
                "cropbox": list(page.cropbox),
                "rotation_matrix": list(page.rotation_matrix),
                "native_blocks": sum(block["type"] == 0 for block in blocks),
                "image_blocks": sum(block["type"] == 1 for block in blocks),
                "words": words,
            })
    return result, time.perf_counter() - start


def normalized(s):
    return "".join(c for c in unicodedata.normalize("NFKC", s) if unicodedata.category(c) != "Cf")


def key_tokens(s):
    return sorted(set(re.findall(r"\d+(?:[.,]\d+)?", normalized(s))))


def sample_words(pages, needles):
    found = []
    for page_number, page in enumerate(pages, 1):
        for word in page["words"]:
            if any(needle in normalized(word["text"]) for needle in needles):
                found.append({
                    "page": page_number,
                    "text": word["text"],
                    "box": [round(v, 4) for v in word["box"]],
                    "normalized": [round(word["box"][i] / (page["width"] if i % 2 == 0 else page["height"]), 5) for i in range(4)],
                })
    return found[:16]


def main():
    rows = []
    for fixture in MANIFEST["entries"]:
        path = CORPUS / Path(fixture["file"]).name
        pop_text, pop_pages, pop_seconds = poppler(path)
        for page, geometry in zip(pop_pages, fixture["page_geometry"]):
            page["declared_width"], page["declared_height"] = page["width"], page["height"]
            page["width"], page["height"] = geometry["visible_size_pt"]
        mu_pages, mu_seconds = mupdf(path)
        mu_text = "\n".join(page["text"] for page in mu_pages)
        row = {
            "id": fixture["id"],
            "modalities": fixture["page_modalities"],
            "poppler": {"seconds": round(pop_seconds, 4), "characters": len(pop_text), "words": sum(len(p["words"]) for p in pop_pages), "number_tokens": key_tokens(pop_text)},
            "pymupdf": {"seconds": round(mu_seconds, 4), "characters": len(mu_text), "words": sum(len(p["words"]) for p in mu_pages), "number_tokens": key_tokens(mu_text), "native_blocks": [p["native_blocks"] for p in mu_pages], "image_blocks": [p["image_blocks"] for p in mu_pages]},
        }
        if fixture["id"] in ("core-arabic-native", "core-bilingual-native", "core-english-native"):
            row["sample_words"] = {
                "poppler": sample_words(pop_pages, ["84", "23", "12.4", "21.5", "23.0"]),
                "pymupdf": sample_words(mu_pages, ["84", "23", "12.4", "21.5", "23.0"]),
            }
        if fixture["id"] == "stress-crop":
            row["crop"] = {"poppler_decoy": "99 percent" in pop_text, "pymupdf_decoy": "99 percent" in mu_text, "poppler_visible": "71 percent" in pop_text, "pymupdf_visible": "71 percent" in mu_text}
        if fixture["id"] == "stress-reading-order":
            cues = ["1. Finding", "The north pump", "No outage", "2. Action", "Replace the seal", "pressure at 12 bar", "Sidebar:"]
            row["reading_order"] = {"cues": cues, "poppler_positions": [pop_text.find(c) for c in cues], "pymupdf_positions": [mu_text.find(c) for c in cues]}
        if fixture["id"] == "stress-rotation":
            row["rotation"] = {"pymupdf_page": {k: mu_pages[0][k] for k in ("width", "height", "rotation", "cropbox", "rotation_matrix")}, "pymupdf_97_2": sample_words(mu_pages, ["97.2"]), "poppler_97_2": sample_words(pop_pages, ["97.2"])}
        rows.append(row)
    json.dump({"versions": {"pymupdf": pymupdf.VersionBind, "poppler": "pdftotext 26.01.0"}, "fixtures": rows}, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
