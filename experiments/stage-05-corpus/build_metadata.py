"""Write the draft manifest and reviewable gold file for Stage 05 fixtures.

This is experimental fixture bookkeeping. A bilingual human must approve the
questions, answers, and regions before either file can be treated as gold.
"""

from __future__ import annotations

import hashlib
import json
import copy
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
PDF_DIR = ROOT / "output/pdf/stage-05-corpus"
DOC_DIR = ROOT / "docs/evaluation"
EN_SOURCE = Path("/tmp/pdfmining-land-matters-en.pdf")
AR_SOURCE = Path("/tmp/pdfmining-land-matters-ar.pdf")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def geometry(path: Path) -> list[dict]:
    pages = []
    for i, p in enumerate(PdfReader(path).pages, 1):
        crop = p.cropbox
        rotation = int(p.get("/Rotate", 0)) % 360
        visible_w = float(crop.width) if rotation in (0, 180) else float(crop.height)
        visible_h = float(crop.height) if rotation in (0, 180) else float(crop.width)
        pages.append({
            "page": i,
            "media_box_pt": [float(v) for v in (p.mediabox.left, p.mediabox.bottom, p.mediabox.right, p.mediabox.top)],
            "crop_box_pt": [float(v) for v in (crop.left, crop.bottom, crop.right, crop.top)],
            "rotation_degrees": rotation,
            "visible_size_pt": [visible_w, visible_h],
        })
    return pages


def region(page: int, width: float, height: float, box: tuple[float, float, float, float], hint: str,
           precision: str = "line_or_block") -> dict:
    x0, y0, x1, y1 = box
    return {"page": page, "rect_normalized": [round(x0 / width, 5), round(y0 / height, 5),
                                                 round(x1 / width, 5), round(y1 / height, 5)],
            "source_hint": hint, "precision": precision}


WB_W, WB_H = 576, 756
BI_W, BI_H = 594.96, 841.92
en = lambda page, box, hint: region(page, WB_W, WB_H, box, hint)
ar = lambda page, box, hint: region(page, WB_W, WB_H, box, hint)
bi = lambda page, box, hint: region(page, BI_W, BI_H, box, hint)


CORE_QUESTIONS = {
    "english": [
        {"kind": "direct_fact", "question": "What share of MENA land does the report describe as barren?",
         "expected_answer": "84 percent.", "claims": ["84 percent of MENA land is described as barren."],
         "evidence": [en(1, (90, 208, 486, 223), "84 percent barren")], "support": "supported"},
        {"kind": "combined_evidence", "question": "Why does the report call for modernizing land administration systems?",
         "expected_answer": "Land is scarce and access is constrained; the report proposes better registration, digitized records, transparency, and accessible land information as priorities.",
         "claims": ["The report links land scarcity and access problems to a need for land-sector reform.",
                    "It prioritizes property registration, digitization, transparency, and land information access."],
         "evidence": [en(1, (90, 195, 486, 261), "scarcity, demand and supply"),
                      en(2, (90, 650, 486, 691), "land administration priorities")], "support": "supported"},
        {"kind": "table_or_statistic", "question": "What share of manufacturing and service firms identify land access as a major constraint?",
         "expected_answer": "23 percent.", "claims": ["23 percent of those firms identify land access as a major constraint."],
         "evidence": [en(1, (90, 351, 486, 390), "twenty-three percent of firms")],
         "statistic": {"value": 23, "unit": "percent", "status": "extracted", "population": "manufacturing and service firms"},
         "support": "supported"},
        {"kind": "insufficient_evidence", "question": "What was MENA's property-tax revenue in 2025?",
         "expected_answer": "Insufficient evidence: these pages do not report 2025 property-tax revenue.",
         "claims": [], "evidence": [], "support": "unsupported", "expected_action": "abstain"},
    ],
    "arabic": [
        {"kind": "direct_fact", "question": "ما نسبة الأراضي القاحلة في منطقة الشرق الأوسط وشمال أفريقيا وفق التقرير؟",
         "expected_answer": "٨٤٪.", "claims": ["يصف التقرير ٨٤٪ من أراضي المنطقة بأنها قاحلة."],
         "evidence": [ar(1, (90, 195, 486, 223), "٨٤٪ من الأراضي قاحلة")], "support": "supported"},
        {"kind": "combined_evidence", "question": "لماذا يدعو التقرير إلى تحديث أنظمة إدارة الأراضي؟",
         "expected_answer": "تتسم الأراضي بالندرة وتواجه عملية الحصول عليها عوائق؛ وتشمل الأولويات تسجيل الملكية ورقمنة السجلات وتحسين الشفافية وإتاحة المعلومات.",
         "claims": ["يربط التقرير الندرة وصعوبات الحصول على الأراضي بالحاجة إلى الإصلاح.",
                    "يوصي بتسجيل الملكية ورقمنة السجلات وتحسين الشفافية وإتاحة المعلومات."],
         "evidence": [ar(1, (90, 195, 486, 248), "ندرة الأراضي وعوائق الوصول"),
                      ar(2, (90, 416, 486, 443), "أولويات تحديث إدارة الأراضي")], "support": "supported"},
        {"kind": "table_or_statistic", "question": "ما نسبة شركات الصناعة والخدمات التي تعد الحصول على الأراضي قيداً رئيسياً؟",
         "expected_answer": "٢٣٪.", "claims": ["ترى ٢٣٪ من تلك الشركات أن الحصول على الأراضي قيد رئيسي."],
         "evidence": [ar(1, (90, 311, 486, 351), "٢٣٪ من الشركات")],
         "statistic": {"value": 23, "unit": "percent", "status": "extracted", "population": "manufacturing and service firms"},
         "support": "supported"},
        {"kind": "insufficient_evidence", "question": "ما إيرادات ضريبة العقارات في المنطقة عام ٢٠٢٥؟",
         "expected_answer": "الأدلة غير كافية: لا تذكر الصفحات إيرادات ضريبة العقارات لعام ٢٠٢٥.",
         "claims": [], "evidence": [], "support": "unsupported", "expected_action": "abstain"},
    ],
    "bilingual": [
        {"kind": "direct_fact", "question": "How much did North Basin deliver in 2024? / كم سلّم الحوض الشمالي في عام ٢٠٢٤؟",
         "expected_answer": "12.4 million cubic metres / ١٢٫٤ مليون متر مكعب.",
         "claims": ["North Basin delivered 12.4 million cubic metres in 2024."],
         "evidence": [bi(1, (53, 138, 526, 166), "North Basin observed amount")], "support": "supported"},
        {"kind": "combined_evidence", "question": "What was the 2025 target, and was it observed? / ما هدف ٢٠٢٥، وهل كان نتيجة فعلية؟",
         "expected_answer": "No. The document gives 21.5 million cubic metres as the audited 2024 actual and 23.0 million cubic metres as the planned 2025 target; it gives no 2025 actual.",
         "claims": ["The 2024 actual was 21.5 million cubic metres.", "The 2025 figure of 23.0 million cubic metres is a target, not an observed result."],
         "evidence": [bi(1, (53, 138, 526, 166), "English actual"),
                      bi(2, (82, 112, 542, 162), "Arabic target distinction")],
         "support": "supported", "cross_language_evidence_required": True},
        {"kind": "table_or_statistic", "question": "What is the gap between the 2024 delivered total and the 2025 target? / ما الفارق بين مجموع ٢٠٢٤ وهدف ٢٠٢٥؟",
         "expected_answer": "1.5 million cubic metres / ١٫٥ مليون متر مكعب.",
         "claims": ["The 2025 target exceeds the 2024 delivered total by 1.5 million cubic metres."],
         "evidence": [region(1, BI_W, BI_H, (53, 240, 542, 375), "table delivered total", "table_region"),
                      bi(2, (82, 112, 542, 162), "Arabic target")],
         "statistic": {"value": 1.5, "unit": "million cubic metres", "status": "derived", "formula": "23.0 - 21.5"},
         "support": "supported", "cross_language_evidence_required": True},
        {"kind": "insufficient_evidence", "question": "What was the actual delivery in 2025? / ما كمية التسليم الفعلية في ٢٠٢٥؟",
         "expected_answer": "Insufficient evidence: only a 2025 target is given, not an actual delivery.",
         "claims": [], "evidence": [], "support": "unsupported", "expected_action": "abstain",
         "absence_context": [bi(2, (80, 242, 542, 294), "document explicitly says no 2025 actual")]},
    ],
}


STRESS = [
    {"file": "stress-rotation.pdf", "focus": "page rotation", "question": "What was verified pump uptime in 2024?",
     "expected_answer": "97.2 percent.", "expected_behavior": "Exact visible-page highlight only after rotation transform is verified; otherwise page-only fallback.",
     "evidence": [region(1, 792, 612, (647, 208, 660, 236), "97.2 vertical text after page rotation")],
     "review_note": "Rotated PDF bbox requires viewer-coordinate check."},
    {"file": "stress-crop.pdf", "focus": "nondefault crop", "question": "What is visible service coverage in 2024?",
     "expected_answer": "71 percent; the 99 percent decoy lies outside the visible CropBox.",
     "expected_behavior": "Use visible cropped page coordinates; never cite or answer from the outside-crop decoy.",
     "evidence": [region(1, 468, 648, (28, 100, 300, 114), "visible 71 percent line")],
     "review_note": "Review with viewer honoring CropBox; default pdftoppm rendering may show MediaBox."},
    {"file": "stress-reading-order.pdf", "focus": "two-column reading order", "question": "What action follows the north-pump finding?",
     "expected_answer": "Replace the seal before 30 June 2024, then verify pressure at 12 bar.",
     "expected_behavior": "Read left finding then right action; keep sidebar separate from observed results.",
     "reading_order": ["left heading", "left finding", "right heading", "right action", "sidebar"],
     "evidence": [region(1, 612, 792, (50, 102, 200, 200), "left finding"),
                  region(1, 612, 792, (320, 102, 470, 200), "right action")]},
    {"file": "stress-table-continuation.pdf", "focus": "multi-page table", "question": "What were North and West delivered volumes in 2024?",
     "expected_answer": "North: 12.4 million m3; West: 3.5 million m3.",
     "expected_behavior": "Join the continued table across pages while preserving each cell's page and region.",
     "table_cells": [{"page": 1, "row": "North", "column": "2024", "value": 12.4},
                     {"page": 2, "row": "West", "column": "2024", "value": 3.5}],
     "evidence": [region(1, 612, 792, (45, 170, 567, 215), "North row"),
                  region(2, 612, 792, (45, 215, 567, 260), "West row")]},
    {"file": "stress-degraded-ocr.pdf", "focus": "degraded scan", "question": "What valve-integrity value is shown?",
     "expected_answer": "The visible page appears to show 63 percent, but extraction should warn or withhold if OCR confidence is inadequate.",
     "expected_behavior": "Do not fabricate an exact span or high-support factual answer; page-only fallback or explicit uncertainty is acceptable.",
     "evidence": [region(1, 612, 792, (55, 130, 380, 165), "blurred valve integrity line", "approximate_page_region")],
     "allow_page_only_fallback": True},
    {"file": "stress-conflicting-figures.pdf", "focus": "draft-versus-audited figures", "question": "What was the audited 2024 leakage estimate?",
     "expected_answer": "17.9 percent; the earlier 18.4 percent was a draft superseded by the audit.",
     "expected_behavior": "Cite both draft and audited pages when explaining the conflict; do not silently select the draft.",
     "evidence": [region(1, 612, 792, (50, 125, 425, 155), "draft 18.4 percent"),
                  region(2, 612, 792, (50, 125, 565, 155), "audited 17.9 percent supersedes draft")]},
]


def main() -> None:
    DOC_DIR.mkdir(parents=True, exist_ok=True)
    en_hash, ar_hash = sha(EN_SOURCE), sha(AR_SOURCE)
    files = sorted(PDF_DIR.glob("*.pdf"))
    assert len(files) == 15
    entries = []
    for path in files:
        name = path.name
        core = name.startswith("core-")
        family = name.split("-")[1] if core else "stress"
        variant = name.removesuffix(".pdf").split("-")[-1] if core else "targeted"
        if family == "english":
            rights = {"basis": "World Bank CC BY 3.0 IGO, text-only excerpt from publisher report",
                      "source_url": "https://documents1.worldbank.org/curated/en/099559508272442561/pdf/IDU13ee887eb13670145571be091c0095f45be26.pdf",
                      "publisher_record": "https://openknowledge.worldbank.org/entities/publication/582c44fd-db27-57b9-bc1c-60270b43bc02",
                      "source_sha256": en_hash, "source_pdf_pages": [19, 20],
                      "third_party_page_review": "Selected executive-summary pages are prose-only; no separately credited photos, figures, or tables appear on the selected pages.",
                      "attribution": "Corsi, Anna, and Harris Selod. 2023. Land Matters. World Bank. doi:10.1596/978-1-4648-1661-1. CC BY 3.0 IGO."}
        elif family == "arabic":
            rights = {"basis": "World Bank CC BY 3.0 IGO, text-only excerpt from publisher Arabic edition",
                      "source_url": "https://documents1.worldbank.org/curated/en/099605208272415635/pdf/IDU1238311ae1eae41426918dc5170a628fd0af2.pdf",
                      "publisher_record": "https://openknowledge.worldbank.org/entities/publication/582c44fd-db27-57b9-bc1c-60270b43bc02",
                      "source_sha256": ar_hash, "source_pdf_pages": [19, 20],
                      "third_party_page_review": "Selected executive-summary pages are prose-only; no separately credited photos, figures, or tables appear on the selected pages.",
                      "attribution": "كورسي، آنا وهاريس سيلود. 2023. أهمية الأراضي. البنك الدولي. doi:10.1596/978-1-4648-1889-9. CC BY 3.0 IGO."}
        else:
            rights = {"basis": "Purpose-written fictional fixture created for this project; no external document, private data, or third-party visual component reused.",
                      "source_url": None, "source_sha256": None, "source_pdf_pages": None,
                      "third_party_page_review": "No third-party source components."}
        if core:
            if family == "bilingual":
                transforms = {"native": "Author HTML printed by Chromium with Unicode Arabic/English text and native table.",
                              "scanned": "Rasterize the matched native PDF at 180 dpi; every page becomes image-only.",
                              "mixed": "Author same content as native, with the page-1 table replaced by an image-only table region."}
                modes = {"native": ["native", "native"], "scanned": ["scanned", "scanned"],
                         "mixed": ["native plus scanned table region", "native"]}
                languages = ["Arabic and English on same page", "Arabic and English on same page"]
            else:
                transforms = {"native": "Extract source PDF pages 19 and 20 into a two-page excerpt.",
                              "scanned": "Rasterize the matched excerpt at 180 dpi; every page becomes image-only.",
                              "mixed": "Keep excerpt page 1 native and substitute rasterized page 2."}
                modes = {"native": ["native", "native"], "scanned": ["scanned", "scanned"],
                         "mixed": ["native", "scanned"]}
                languages = [family, family]
            transform = transforms[variant]
            modalities = modes[variant]
        else:
            transform = {
                "stress-rotation.pdf": "Rotate a native one-page fictional note by 90 degrees.",
                "stress-crop.pdf": "Set a nondefault CropBox that hides a conflicting decoy outside the visible page.",
                "stress-reading-order.pdf": "Author a two-column native page with a separate sidebar.",
                "stress-table-continuation.pdf": "Author a two-page table with repeated header and continuation label.",
                "stress-degraded-ocr.pdf": "Rasterize a low-contrast 8-point native note at 90 dpi, blur, rescale, and fade.",
                "stress-conflicting-figures.pdf": "Author draft and superseding audited figures on two native pages.",
            }[name]
            modalities = ["scanned" if name == "stress-degraded-ocr.pdf" else "native"] * len(geometry(path))
            languages = ["English"] * len(modalities)
        entry = {"id": name.removesuffix(".pdf"), "file": str(path.relative_to(ROOT)),
                 "sha256": sha(path), "bytes": path.stat().st_size, "page_count": len(geometry(path)),
                 "page_geometry": geometry(path), "family": family, "variant": variant,
                 "correlation_group": family if core else name.removesuffix(".pdf"),
                 "rights": rights, "transformation": transform, "page_languages": languages,
                 "page_modalities": modalities,
                 "provider_use": "Public/synthetic fixture only; external use still requires the provider controls and disclosure in ADR 0002.",
                 "gold_review_status": "pending bilingual human review"}
        entries.append(entry)
    manifest = {"schema_version": "0.1", "status": "fixture files verified; gold annotations await bilingual human review",
                "mvp_limits": {"max_pages": 20, "initial_byte_target": 25_000_000},
                "source_location_contract": "ADR 0001: normalized top-left coordinates on the visible original page after crop and rotation",
                "license_notes": "World Bank pages are short CC BY 3.0 IGO excerpts. Attribute the original, identify adaptations, and do not imply World Bank endorsement. The two full publisher PDFs stay outside this repository; only excerpts are fixtures.",
                "entries": entries}
    (DOC_DIR / "stage-05-corpus-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    cases = []
    for family, family_questions in CORE_QUESTIONS.items():
        for variant in ("native", "scanned", "mixed"):
            filename = f"core-{family}-{variant}.pdf"
            for n, q in enumerate(family_questions, 1):
                row = {"id": f"{family}-{variant}-q{n}", "pdf": filename,
                       "family": family, "variant": variant, **copy.deepcopy(q)}
                if family == "bilingual" and variant == "mixed" and q["kind"] == "table_or_statistic":
                    row["evidence"][0]["source_hint"] = "scanned page-1 table region"
                cases.append(row)
    gold = {"schema_version": "0.1", "status": "draft; not human-verified gold",
            "coordinate_space": "Original visible PDF page after effective crop/rotation; top-left origin; normalized [x0,y0,x1,y1]",
            "evidence_rules": ["A wrong cited page fails the case.", "A guessed exact rectangle fails the case.",
                               "An unsupported factual claim presented confidently fails the case.",
                               "Page-only fallback is allowed when exact location is unreliable and is explicitly marked."],
            "core_case_count": len(cases), "core_questions": cases,
            "table_truth": {"core-bilingual": {"rows": [
                {"area": "North Basin", "year": 2024, "delivered_million_m3": 12.4},
                {"area": "South Basin", "year": 2024, "delivered_million_m3": 9.1},
                {"area": "Delivered total", "year": 2024, "delivered_million_m3": 21.5}],
                "page": 1, "region": region(1, BI_W, BI_H, (53, 240, 542, 375), "entire table", "table_region"),
                "target_outside_table": {"page": 2, "value": 23.0, "unit": "million cubic metres", "type": "planned target"}}},
            "stress_expectations": STRESS}
    (DOC_DIR / "stage-05-corpus-gold-draft.json").write_text(json.dumps(gold, ensure_ascii=False, indent=2) + "\n")
    print("Wrote manifest for", len(entries), "PDFs and", len(cases), "core cases")


if __name__ == "__main__":
    main()
