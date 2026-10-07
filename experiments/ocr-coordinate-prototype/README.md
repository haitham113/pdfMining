# Throwaway OCR and coordinate probe

Issue: [Choose selective Arabic/English OCR and coordinate strategy](https://github.com/haitham113/pdfMining/issues/6). This is an architecture experiment, not application code or a release benchmark.

## Hypothesis

Local Tesseract 5 can provide usable Arabic/English text, word confidence, and original-page regions from selectively rendered pages/regions. Its output might be sufficient as the primary MVP OCR path if required bilingual facts survive.

## Samples and setup

Run `run.py` with Python/PyMuPDF and Tesseract 5.5.0 (`ara`/`eng` traineddata) on the human-verified Stage 05 corpus. The script renders only the chosen original PDF page or the scanned table image region at 180 dpi, sends that image to Tesseract TSV, and maps word boxes into ADR 0001's normalized visible-page coordinates using the raster origin, scale, crop, and rotation already applied by the renderer. All input remains local. The compared PDFs are English scanned page 1, Arabic scanned pages 1–2, bilingual scanned pages 1–2, the image-only table region of bilingual mixed page 1, and degraded/rotated stress pages. The selected pages are correlated corpus cases, not independent accuracy samples.

For this run, Ubuntu `tesseract-ocr`, `libtesseract5`, `libleptonica6`, and Arabic/English model packages were extracted under `/tmp/pdfmining-ocr-local`, with no system installation. `ara_best.traineddata` from [Tesseract's official higher-accuracy model repository](https://github.com/tesseract-ocr/tessdata_best) was also tried on the critical Arabic pages. Generated images and TSV-derived JSON are ignored; rerun the script to regenerate them. The script requires the Tesseract binary and traineddata at its stated `/tmp` paths.

## Observations

| Case | OCR observation | Decision impact |
| --- | --- | --- |
| English scanned page 1 | Correctly recovered the 84 percent statement; 553 words in 2.56 s. | Local English baseline is usable on this sample. |
| Arabic scanned page 1 | The visible ٨٤٪ became `(9084`; the visible ٢٣٪ became `9,023` in the corresponding line. The first token had 40.6 word confidence, but the page median was 92.7. | Page aggregate confidence would hide a critical numeric error. |
| Bilingual scanned page 2 | The Arabic-only ٢٠٢٥ / ٢٣٫٠ target became `7١76` / `١1,٠`; 98 words in 1.14 s. Higher-accuracy Arabic data still rendered the target/year incorrectly. | The required cross-language target and derived 1.5 difference cannot be trusted from this local OCR. |
| Bilingual mixed page 1, table image only | Recovered 12.4, 9.1, and 21.5 from 17 OCR words in 0.22 s. The 12.4 word mapped to normalized `[0.71198, 0.34493, 0.74627, 0.35300]`, inside the reviewed table region. | Region OCR can preserve native text elsewhere on the same page. |
| Degraded scan | Returned six largely meaningless tokens; median word confidence 33.5; no 63 percent. | Withhold factual claim and exact highlight; show page-level limitation. |
| Rotated page rendered to image | Recovered 97.2; OCR word region `[0.82071, 0.34248, 0.83182, 0.38301]` lies inside the human-reviewed region `[0.81692, 0.33987, 0.83333, 0.38562]`. | Raster-to-original mapping is feasible for this rotation, subject to viewer overlay verification. |

All 2,107 sampled OCR word boxes were within `[0,1]`. That bounds check is insufficient to prove visual alignment; the mixed table and rotation spot checks are stronger evidence. The renderer's image-object geometry for the mixed page locates the table at PDF points `(54, 251.25, 541.5, 365.25)`, matching the reviewed table area. A production selector must still distinguish text-bearing image regions from decorative images and prove that native text is actually usable.

## Conclusion and open gate

Reject Tesseract 5 as the sole primary OCR engine for the MVP on this corpus. The owner chose a hosted-first path conditional on a live corpus trial. No hosted call was run because no hosted OCR account is available yet; no hosted quality or latency claim follows from vendor documentation. Keep the original PDF canonical, retain the raw OCR confidence and transform provenance per source span, and route low-quality or failed regions to explicit partial results. Do not substitute aggregate confidence for verified critical figures or claim/evidence support.

The first hosted trial candidate is Google Document AI Enterprise OCR, with Azure Document Intelligence Read as an alternative. Both document Arabic support and word/page geometry; Google documents online processing in memory with no model training on customer data, while Azure documents temporary 24-hour result storage and a deletion API. These are documentation facts, not a completed configuration review or corpus result. See the [Google OCR processor list](https://docs.cloud.google.com/document-ai/docs/processors-list), [Google OCR response format](https://docs.cloud.google.com/document-ai/docs/handle-response), [Google security and retention](https://docs.cloud.google.com/document-ai/docs/security), [Azure language support](https://learn.microsoft.com/azure/ai-services/document-intelligence/language-support/ocr?view=doc-intel-4.0.0), [Azure word geometry](https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/prebuilt/read?view=doc-intel-4.0.0), and [Azure privacy and retention](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/document-intelligence/data-privacy-security?view=form-recog-3.0.0).

The hosted gate must use only eligible public/synthetic page or region images and check the Arabic ٨٤٪ and ٢٣٪, bilingual ٢٠٢٥ / ٢٣٫٠, mixed table cells, native-page avoidance, correct original-page transforms and highlights, degraded withholding, per-region failure recovery, latency/resource footprint, and provider training/retention configuration. A missed critical figure, wrong page, or fabricated exact region fails its case. Stage 06 must retain the provider behind a replaceable OCR adapter until that gate passes.
