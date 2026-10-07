"""Throwaway OCR probe for issue 6; runs against the checked Stage 05 fixtures."""

import csv
import io
import json
import os
import subprocess
import time
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent / "results"
OUT.mkdir(exist_ok=True)
TESS = "/tmp/pdfmining-ocr-local/usr/bin/tesseract"
ENV = os.environ | {
    "LD_LIBRARY_PATH": "/tmp/pdfmining-ocr-local/usr/lib/x86_64-linux-gnu",
    "TESSDATA_PREFIX": "/tmp/pdfmining-ocr-local/usr/share/tesseract-ocr/5/tessdata",
    "OMP_THREAD_LIMIT": "1",
}

CASES = [
    ("core-english-scanned.pdf", 1, None, "eng"),
    ("core-arabic-scanned.pdf", 1, None, "ara"),
    ("core-arabic-scanned.pdf", 2, None, "ara"),
    ("core-bilingual-scanned.pdf", 1, None, "eng+ara"),
    ("core-bilingual-scanned.pdf", 2, None, "eng+ara"),
    ("core-bilingual-mixed.pdf", 1, (0.08908, 0.28506, 0.91099, 0.44541), "eng+ara"),
    ("stress-degraded-ocr.pdf", 1, None, "eng"),
    ("stress-rotation.pdf", 1, None, "eng"),
]

results = []
for filename, page_number, region, languages in CASES:
    doc = fitz.open(ROOT / "output/pdf/stage-05-corpus" / filename)
    page = doc[page_number - 1]
    page_rect = page.rect  # visible crop and page rotation applied by PyMuPDF
    clip = None
    if region:
        clip = fitz.Rect(
            region[0] * page_rect.width,
            region[1] * page_rect.height,
            region[2] * page_rect.width,
            region[3] * page_rect.height,
        )
    pix = page.get_pixmap(matrix=fitz.Matrix(2.5, 2.5), clip=clip, alpha=False)
    image_path = OUT / f"{Path(filename).stem}-p{page_number}{'-region' if region else ''}.png"
    pix.save(image_path)
    start = time.perf_counter()
    proc = subprocess.run(
        [TESS, str(image_path), "stdout", "-l", languages, "--psm", "3", "tsv"],
        env=ENV, capture_output=True, text=True, check=True,
    )
    seconds = time.perf_counter() - start
    words = []
    for row in csv.DictReader(io.StringIO(proc.stdout), delimiter="\t"):
        if row["level"] != "5" or not row["text"].strip():
            continue
        left, top, width, height = (int(row[k]) for k in ("left", "top", "width", "height"))
        # Tesseract coordinates are relative to the rendered page or clipped region.
        x0 = (pix.x + left) / 2.5 / page_rect.width
        y0 = (pix.y + top) / 2.5 / page_rect.height
        x1 = (pix.x + left + width) / 2.5 / page_rect.width
        y1 = (pix.y + top + height) / 2.5 / page_rect.height
        words.append({
            "text": row["text"], "confidence": float(row["conf"]),
            "rect_normalized": [round(v, 5) for v in (x0, y0, x1, y1)],
            "line": [row[k] for k in ("block_num", "par_num", "line_num")],
        })
    item = {
        "pdf": filename, "page": page_number, "region": region, "languages": languages,
        "render_px": [pix.width, pix.height], "raster_origin_px": [pix.x, pix.y],
        "visible_page_pt": [page_rect.width, page_rect.height],
        "seconds": round(seconds, 3), "words": words,
        "text": " ".join(w["text"] for w in words), "stderr": proc.stderr.strip(),
    }
    results.append(item)
    print(f"{filename} p{page_number} {languages}: {seconds:.2f}s, {len(words)} words")
    print("  " + item["text"][:250])

(OUT / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
