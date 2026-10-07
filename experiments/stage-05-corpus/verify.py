"""Verify generated Stage 05 corpus integrity; not a product test suite."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
manifest = json.loads((ROOT / "docs/evaluation/stage-05-corpus-manifest.json").read_text())
gold = json.loads((ROOT / "docs/evaluation/stage-05-corpus-gold-draft.json").read_text())
entries = manifest["entries"]
assert len(entries) == 15
assert len(gold["core_questions"]) == 36
assert len(gold["stress_expectations"]) == 6
assert Counter((e["family"], e["variant"]) for e in entries if e["family"] != "stress") == Counter(
    {(family, mode): 1 for family in ("english", "arabic", "bilingual") for mode in ("native", "scanned", "mixed")}
)

entry_by_name = {}
for entry in entries:
    path = ROOT / entry["file"]
    assert path.exists(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"], path
    assert path.stat().st_size == entry["bytes"] <= 25_000_000, path
    reader = PdfReader(path)
    assert len(reader.pages) == entry["page_count"] <= 20, path
    assert len(entry["page_geometry"]) == entry["page_count"], path
    text = subprocess.check_output(["pdftotext", str(path), "-"], text=True).strip()
    if entry["variant"] == "scanned" or path.name == "stress-degraded-ocr.pdf":
        assert not text, f"Unexpected text layer: {path}"
    if entry["variant"] == "native":
        assert text, f"Missing native text: {path}"
    entry_by_name[path.name] = entry

expected_kinds = {"direct_fact", "combined_evidence", "table_or_statistic", "insufficient_evidence"}
for family in ("english", "arabic", "bilingual"):
    for mode in ("native", "scanned", "mixed"):
        cases = [c for c in gold["core_questions"] if c["family"] == family and c["variant"] == mode]
        assert len(cases) == 4
        assert {c["kind"] for c in cases} == expected_kinds
for case in gold["core_questions"]:
    assert case["pdf"] in entry_by_name
    if case["kind"] == "insufficient_evidence":
        assert case["expected_action"] == "abstain" and not case["claims"]
    for evidence in case["evidence"] + case.get("absence_context", []):
        assert 1 <= evidence["page"] <= entry_by_name[case["pdf"]]["page_count"]
        x0, y0, x1, y1 = evidence["rect_normalized"]
        assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1
for case in gold["stress_expectations"]:
    assert case["file"] in entry_by_name
    for evidence in case["evidence"]:
        assert 1 <= evidence["page"] <= entry_by_name[case["file"]]["page_count"]
        x0, y0, x1, y1 = evidence["rect_normalized"]
        assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1

print("OK: 15 PDFs, 36 core cases, six stress expectations, hashes, limits, modalities, and region bounds")
print("Human review status:", gold["status"])
