# Native extraction comparison — throwaway experiment

**Question:** Which native PDF extractor gives Arabic/English text, page-local blocks and words, and defensible source boxes for the Stage 05 corpus?

**Hypothesis:** A layout-aware extractor can provide original-page word boxes for citations, but reading order, crop, rotation, and text-layer quality need separate checks.

## Samples and setup

- All 15 human-verified Stage 05 PDFs: nine matched Arabic/English/bilingual native, scanned, and mixed fixtures, plus six stress cases. The native decision concentrates on the six core native/mixed PDFs and native stress pages. Scanned pages are controls.
- Poppler `pdftotext` 26.01.0 (`-cropbox` plain text and `-cropbox -bbox-layout` XHTML); PyMuPDF 1.26.5 (`get_text("text")`, `get_text("dict")`, `get_text("words")`); PDF.js `pdfjs-dist` 6.3.289 (`getTextContent()` in Node 24.21.0).
- Reproduce from the repository root with Poppler and Node installed, plus a scratch Python environment containing `PyMuPDF==1.26.5`:

  ```sh
  python experiments/native-extraction-prototype/compare.py > experiments/native-extraction-prototype/results.json
  npm install --no-save --prefix experiments/native-extraction-prototype pdfjs-dist@6.3.289
  node experiments/native-extraction-prototype/pdfjs.mjs > experiments/native-extraction-prototype/pdfjs-results.json
  ```

The scripts and recorded JSON are disposable. They do not define the production adapter, quality thresholds, or full evaluation harness.

## Observations

| Case | Poppler | PyMuPDF | PDF.js |
| --- | --- | --- | --- |
| Core Arabic native | `-bbox-layout` retains 1,358 word records across two pages, including `%84` and `%23` at the reviewed first-page regions. Plain text presents readable Arabic with direction controls. | 1,399 word records and nearly identical boxes for those figures, but text order differs. | The World Bank Arabic text is broadly readable; this alone does not establish citation granularity. |
| Bilingual native target | A single word `٢٣٫٠` is at page 2 box `(375.26, 112.21, 396.66, 137.76)` points, inside the reviewed target region. | The target appears as `٠٫٣٢` in extracted text, reversing the numeric value. | The target appears as `٢٣٫٠`, but nearby Arabic is fragmented into many small text items/glyph forms. |
| Cropped page | Plain `pdftotext -cropbox` **includes** the hidden `99 percent` decoy. The `-bbox-layout -cropbox` word stream excludes it. The visible `71 percent` survives. | Excludes the decoy and retains `71 percent`. | Excludes the decoy and retains `71 percent`. |
| Rotated page | `97.2` box is `(647.12, 208.77, 659.12, 235.49)` points. XHTML declares `612 × 792`, although the displayed page is `792 × 612`; dividing by XHTML dimensions gives an invalid x coordinate. Using effective visible dimensions gives normalized `(0.81707, 0.34112, 0.83222, 0.38478)`, matching reviewed gold `(0.81692, 0.33987, 0.83333, 0.38562)`. | Word box needs its page rotation matrix applied; then it matches Poppler and gold. | Viewport reports `792 × 612` and rotation 90; item transforms still need the viewer viewport transform to become visible-page source regions. |
| Two columns | Flat plain text interleaves left and right paragraphs. XHTML blocks expose their positions, but its sequence still interleaves. | Default plain text follows the authored left-then-right prose for this fixture; sorted text interleaves columns. | Text items follow the authored left-then-right prose for this fixture. |
| Scanned and mixed controls | Scanned PDFs have no native words. Mixed PDFs retain native words only on native pages/regions. | Image blocks identify rasterized pages/regions while native words remain separate. | The same modality split is visible, but no OCR is attempted here. |

The comparison did **not** include a native PDF with a deliberately corrupted or invisible text layer, an independent Arabic professional layout, broad font coverage, malicious PDFs, or a meaningful VPS performance benchmark. Counts and timings are diagnostic, not accuracy or release scores. Word boxes were checked against selected verified gold regions; complete automatic region scoring and viewer overlays belong to the evidence-highlight ticket.

## Decision recommended to the owner

Use Poppler `pdftotext -bbox-layout` as the **primary native text and geometry stream**. Keep page, block, line, and word identity and a pinned extractor/version record. Build text from the checked layout stream, rather than trusting plain `pdftotext` output, because the latter leaked the cropped decoy in this fixture. Normalize Arabic presentation and direction carefully while retaining the original extracted word text for provenance.

Use an explicit adapter to translate each word/line region to [ADR 0001](../../docs/adr/0001-original-pdf-source-location-contract.md)'s normalized visible original page. The adapter must read effective CropBox and rotation, validate bounds, and record its transform. The rotated fixture shows why the XHTML page dimensions alone are insufficient. Preserve block geometry for a reading-order pass that groups columns and sidebars; never assume CLI order is semantic order.

Assess native text per page or region for coverage, readable characters, layout coherence, and agreement with the visible area. Send empty, missing, or demonstrably degraded regions to the selective OCR path being decided separately. If source text or coordinates cannot be validated, publish the limitation and page-level provenance without an exact highlight. The original PDF remains canonical; a later extractor changes the extraction revision, not old saved source references.

This is a **replaceable adapter choice**, not a commitment to Poppler for OCR, table reconstruction, or the browser viewer. PDF.js remains a plausible viewer library; its extraction behavior here does not make it the native source of record. PyMuPDF's Arabic number reversal in a decision-critical fixture makes it unsuitable as the sole native text extractor on this corpus.

## Primary API references

- [Poppler `pdftotext` manual](https://manpages.debian.org/testing/poppler-utils/pdftotext.1.en.html): `-bbox-layout`, `-cropbox`, and extraction modes.
- [PyMuPDF text extraction details](https://pymupdf.readthedocs.io/en/latest/app1.html): blocks, spans, words, and the limits of reading order.
- [PyMuPDF page coordinates](https://pymupdf.readthedocs.io/en/latest/page.html): crop, rotation, and transformation matrices.
- [PDF.js API](https://mozilla.github.io/pdf.js/api/draft/module-pdfjsLib.html): text content, page viewports, and transforms.
