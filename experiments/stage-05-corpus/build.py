"""Throwaway Stage 05 PDF comparison-fixture builder; never used by the product.

Run `prepare` with the two publisher-hosted World Bank source PDFs in /tmp,
print the generated HTML files with headless Chrome, then run `finish`.
The manifest and human review notes are separate; this does not certify gold labels.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/pdf/stage-05-corpus"
WORK = Path("/tmp/pdfmining-stage05-corpus")
EN_SOURCE = Path("/tmp/pdfmining-land-matters-en.pdf")
AR_SOURCE = Path("/tmp/pdfmining-land-matters-ar.pdf")
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", FONT))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", FONT_BOLD))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def copy_pages(source: Path, page_numbers: list[int], dest: Path) -> None:
    reader = PdfReader(source)
    writer = PdfWriter()
    for one_based in page_numbers:
        writer.add_page(reader.pages[one_based - 1])
    with dest.open("wb") as stream:
        writer.write(stream)


def make_table_image(path: Path) -> None:
    image = Image.new("RGB", (1400, 328), "white")
    draw = ImageDraw.Draw(image)
    head = ImageFont.truetype(FONT_BOLD, 29)
    body = ImageFont.truetype(FONT, 28)
    xs = [0, 700, 1040, 1400]
    ys = [0, 82, 164, 246, 328]
    draw.rectangle((0, 0, 1400, 82), fill="#dbe7eb")
    for x in xs:
        draw.line((x, 0, x, 328), fill="#45616b", width=2)
    for y in ys:
        draw.line((0, y, 1400, y), fill="#45616b", width=2)
    rows = [
        ("Area", "Year", "Delivered (million m3)"),
        ("North Basin", "2024", "12.4"),
        ("South Basin", "2024", "9.1"),
        ("Delivered total", "2024", "21.5"),
    ]
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            draw.text((xs[j] + 18, ys[i] + 24), value, fill="#162b35", font=head if i == 0 else body)
    image.save(path)


def bilingual_html(table_image: bool) -> str:
    if table_image:
        table = '<img class="scanned-table" src="table-scan.png" alt="Scanned delivery table">'
    else:
        table = '''<table><thead><tr><th>Area / المنطقة</th><th>Year</th><th>Delivered (million m3)</th></tr></thead>
        <tbody><tr><td>North Basin</td><td>2024</td><td>12.4</td></tr>
        <tr><td>South Basin</td><td>2024</td><td>9.1</td></tr>
        <tr><td>Delivered total</td><td>2024</td><td>21.5</td></tr></tbody></table>'''
    return '''<!doctype html><html><head><meta charset="UTF-8"><style>
    @page{size:A4;margin:0}*{box-sizing:border-box}body{margin:0;color:#18313b;font-family:'DejaVu Sans',sans-serif}
    .page{width:210mm;height:297mm;padding:17mm 19mm;break-after:page;overflow:hidden}
    .page:last-child{break-after:auto}h1{font-size:20pt;color:#236e7a;margin:0 0 7mm}
    h2{font-size:12pt;color:#236e7a;margin:7mm 0 3mm}p{font-size:10pt;line-height:1.52;margin:0 0 4mm}
    .ar{font-family:'Noto Naskh Arabic';direction:rtl;text-align:right;font-size:15pt;line-height:1.55}
    table{width:100%;border-collapse:collapse;margin-top:5mm;font-size:9pt}th,td{border:1px solid #55717b;padding:3mm}
    th{background:#dbe7eb;text-align:left}.scanned-table{width:100%;height:auto;margin-top:5mm}
    .note{font-size:8pt;color:#556b73;margin-top:5mm}.footer{position:absolute;bottom:14mm;font-size:8pt;color:#657b84}
    </style></head><body>
    <section class="page"><h1>Regional Water Supply Review / مراجعة إمدادات المياه</h1>
    <h2>Delivered volumes / كميات التسليم</h2>
    <p>In 2024, North Basin delivered 12.4 million cubic metres and South Basin delivered 9.1 million cubic metres. The audited delivered total was 21.5 million cubic metres.</p>
    <p class="ar" lang="ar">في عام ٢٠٢٤، سلّم الحوض الشمالي ١٢٫٤ مليون متر مكعب، وسلّم الحوض الجنوبي ٩٫١ مليون متر مكعب. بلغ المجموع المدقق ٢١٫٥ مليون متر مكعب.</p>
    ''' + table + '''
    <p class="note">Purpose-written evaluation fixture. All values are fictional.</p></section>
    <section class="page"><h1>Targets and methods / الأهداف والمنهجية</h1>
    <h2>Approved target / الهدف المعتمد</h2>
    <p class="ar" lang="ar">الهدف المعتمد لعام ٢٠٢٥ هو ٢٣٫٠ مليون متر مكعب. هذا هدف مخطط وليس نتيجة تسليم فعلية لعام ٢٠٢٥.</p>
    <p>The Arabic target statement above is a plan, not an observed 2025 delivery. The 2024 actual remains 21.5 million cubic metres.</p>
    <h2>Data note / ملاحظة البيانات</h2>
    <p class="ar" lang="ar">لا يقدم هذا الموجز قيمة التسليم الفعلية لعام ٢٠٢٥. لا يجوز استنتاجها من الهدف المخطط.</p>
    <p>The report does not provide an observed 2025 delivery value. No claim about 2025 achievement can be supported from this document.</p>
    <p class="note">Purpose-written evaluation fixture. All values are fictional.</p></section>
    </body></html>'''


def make_stress_sources() -> None:
    # All six sources use deliberately simple fictional content with known truth.
    c = canvas.Canvas(str(WORK / "rotation-source.pdf"), pagesize=(612, 792))
    c.setFont("DejaVu-Bold", 19)
    c.drawString(70, 705, "Rotated inspection memorandum")
    c.setFont("DejaVu", 12)
    c.drawString(70, 650, "Verified pump uptime: 97.2 percent in 2024.")
    c.drawString(70, 624, "Target for 2025: 98.0 percent.")
    c.save()

    c = canvas.Canvas(str(WORK / "crop-source.pdf"), pagesize=(612, 792))
    c.setFont("DejaVu", 12)
    c.drawString(15, 750, "OUTSIDE CROP DECOY: 99 percent")
    c.setFont("DejaVu-Bold", 18)
    c.drawString(100, 655, "Cropped service memorandum")
    c.setFont("DejaVu", 12)
    c.drawString(100, 610, "Visible service coverage: 71 percent in 2024.")
    c.drawString(100, 585, "No 2025 observation is reported.")
    c.save()

    c = canvas.Canvas(str(OUT / "stress-reading-order.pdf"), pagesize=(612, 792))
    c.setFont("DejaVu-Bold", 18)
    c.drawString(50, 735, "Two-column maintenance note")
    c.setFont("DejaVu-Bold", 12)
    c.drawString(50, 680, "1. Finding")
    c.drawString(320, 680, "2. Action")
    c.setFont("DejaVu", 10)
    for i, line in enumerate(["The north pump failed its", "inspection on 6 May 2024.", "No outage was recorded."]):
        c.drawString(50, 655 - i * 19, line)
    for i, line in enumerate(["Replace the seal before", "30 June 2024; then verify", "pressure at 12 bar."]):
        c.drawString(320, 655 - i * 19, line)
    c.setStrokeColor(colors.HexColor("#8799a1"))
    c.line(300, 580, 300, 694)
    c.setFont("DejaVu", 9)
    c.drawString(50, 510, "Sidebar: 12 bar is a planned check, not a measured result.")
    c.save()

    c = canvas.Canvas(str(OUT / "stress-table-continuation.pdf"), pagesize=(612, 792))
    headers = ["District", "2023", "2024", "Unit"]
    rows = [["North", "12.1", "12.4", "million m3"], ["South", "8.7", "9.1", "million m3"],
            ["East", "4.0", "4.4", "million m3"], ["West", "3.8", "3.5", "million m3"]]
    for page_idx in (0, 1):
        c.setFont("DejaVu-Bold", 17)
        c.drawString(45, 735, "Annual delivery table" + (" (continued)" if page_idx else ""))
        c.setFont("DejaVu", 10)
        c.drawString(45, 702, "All figures are fictional. Values are delivered volumes, not targets.")
        x_edges = [45, 235, 335, 435, 567]
        y_top = 660
        for r in range(3):
            y = y_top - r * 45
            c.rect(45, y - 45, 522, 45, stroke=1, fill=0)
            for x in x_edges[1:-1]:
                c.line(x, y - 45, x, y)
        c.setFont("DejaVu-Bold", 10)
        for j, head in enumerate(headers):
            c.drawString(x_edges[j] + 7, y_top - 27, head)
        c.setFont("DejaVu", 10)
        for i, row in enumerate(rows[page_idx * 2:page_idx * 2 + 2]):
            for j, value in enumerate(row):
                c.drawString(x_edges[j] + 7, y_top - (i + 2) * 45 + 18, value)
        c.drawString(45, 455, "Continues on next page." if page_idx == 0 else "End of table.")
        c.showPage()
    c.save()

    c = canvas.Canvas(str(WORK / "degraded-source.pdf"), pagesize=(612, 792))
    c.setFont("DejaVu", 8)
    c.setFillColor(colors.HexColor("#777777"))
    c.drawString(62, 650, "Inspection note: valve integrity was 63 percent in 2024.")
    c.drawString(62, 630, "The result is provisional and must be reviewed against the visible page.")
    c.save()

    c = canvas.Canvas(str(OUT / "stress-conflicting-figures.pdf"), pagesize=(612, 792))
    for title, text in [
        ("Draft service report - 2 April 2025", "Draft 2024 leakage estimate: 18.4 percent."),
        ("Audited service report - 15 May 2025", "Audited 2024 leakage estimate: 17.9 percent. This supersedes the draft figure."),
    ]:
        c.setFont("DejaVu-Bold", 17)
        c.drawString(50, 710, title)
        c.setFont("DejaVu", 12)
        c.drawString(50, 660, text)
        c.showPage()
    c.save()


def prepare() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    if not EN_SOURCE.is_file() or not AR_SOURCE.is_file():
        raise SystemExit("Download the two publisher-hosted source PDFs to /tmp first.")
    copy_pages(EN_SOURCE, [19, 20], OUT / "core-english-native.pdf")
    copy_pages(AR_SOURCE, [19, 20], OUT / "core-arabic-native.pdf")
    make_table_image(WORK / "table-scan.png")
    (WORK / "core-bilingual-native.html").write_text(bilingual_html(False), encoding="utf-8")
    (WORK / "core-bilingual-mixed.html").write_text(bilingual_html(True), encoding="utf-8")
    make_stress_sources()
    print("Prepared source excerpts, HTML, and synthetic stress sources in", WORK)


def rasterize(source: Path, dest: Path, dpi: int = 180, degraded: bool = False) -> None:
    prefix = WORK / f"raster-{dest.stem}"
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(source), str(prefix)], check=True)
    images = []
    for path in sorted(WORK.glob(prefix.name + "-*.png")):
        im = Image.open(path).convert("RGB")
        if degraded:
            im = im.filter(ImageFilter.GaussianBlur(radius=1.8))
            im = im.resize((im.width // 2, im.height // 2)).resize(im.size)
            # Keep the degradation repeatable and visible without random noise.
            im = Image.blend(im, Image.new("RGB", im.size, "white"), 0.28)
        images.append(im)
    if not images:
        raise RuntimeError(f"No raster pages for {source}")
    images[0].save(dest, "PDF", resolution=dpi, save_all=True, append_images=images[1:])
    for im in images:
        im.close()


def mixed_pages(native: Path, scanned: Path, dest: Path) -> None:
    n = PdfReader(native)
    s = PdfReader(scanned)
    if len(n.pages) != 2 or len(s.pages) != 2:
        raise ValueError("Expected two pages in matched native/scanned sources")
    writer = PdfWriter()
    writer.add_page(n.pages[0])
    writer.add_page(s.pages[1])
    with dest.open("wb") as f:
        writer.write(f)


def finish() -> None:
    for lang in ("english", "arabic"):
        native = OUT / f"core-{lang}-native.pdf"
        scanned = OUT / f"core-{lang}-scanned.pdf"
        rasterize(native, scanned)
        mixed_pages(native, scanned, OUT / f"core-{lang}-mixed.pdf")
    bilingual_native = OUT / "core-bilingual-native.pdf"
    bilingual_mixed = OUT / "core-bilingual-mixed.pdf"
    if not bilingual_native.is_file() or not bilingual_mixed.is_file():
        raise SystemExit("Print the two bilingual HTML sources to the expected PDF paths first.")
    rasterize(bilingual_native, OUT / "core-bilingual-scanned.pdf")

    rotation = PdfReader(WORK / "rotation-source.pdf")
    writer = PdfWriter()
    writer.add_page(rotation.pages[0]).rotate(90)
    with (OUT / "stress-rotation.pdf").open("wb") as f:
        writer.write(f)

    crop = PdfReader(WORK / "crop-source.pdf")
    writer = PdfWriter()
    page = writer.add_page(crop.pages[0])
    page.cropbox.lower_left = (72, 72)
    page.cropbox.upper_right = (540, 720)
    with (OUT / "stress-crop.pdf").open("wb") as f:
        writer.write(f)

    rasterize(WORK / "degraded-source.pdf", OUT / "stress-degraded-ocr.pdf", dpi=90, degraded=True)
    files = sorted(OUT.glob("*.pdf"))
    if len(files) != 15:
        raise RuntimeError(f"Expected 15 PDFs, got {len(files)}")
    inventory = []
    for file in files:
        reader = PdfReader(file)
        inventory.append({"file": str(file.relative_to(ROOT)), "sha256": sha(file), "bytes": file.stat().st_size,
                          "pages": len(reader.pages), "page_geometry": [
                              {"media_box_pt": [float(p.mediabox.width), float(p.mediabox.height)],
                               "crop_box_pt": [float(p.cropbox.left), float(p.cropbox.bottom),
                                               float(p.cropbox.right), float(p.cropbox.top)],
                               "rotation": int(p.get("/Rotate", 0))} for p in reader.pages]})
    (WORK / "inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + "\n")
    print("Built", len(files), "PDFs; inventory at", WORK / "inventory.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "finish"])
    args = parser.parse_args()
    globals()[args.phase]()
