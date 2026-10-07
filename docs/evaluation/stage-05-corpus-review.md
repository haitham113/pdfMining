# Stage 05 corpus review

Status: **human verified**. Haitham Ahmed confirmed the full-corpus review on 2026-10-07. The annotation filename retains `draft` for stable references; its contents are verified gold truth for the Stage 05 comparison corpus.

## Artifacts

- [15 PDF fixtures](../../output/pdf/stage-05-corpus/README.md): three matched language families × native/scanned/mixed, plus six targeted stress cases.
- [Manifest](stage-05-corpus-manifest.json): source rights and hashes, transformations, 20-page/25-MB checks, page geometry, languages, modalities, provider-use restriction.
- [Verified annotations](stage-05-corpus-gold-draft.json): 36 core question cases and six stress expectations, with original-visible-page normalized source regions.
- [Fixture builders](../../experiments/stage-05-corpus/build.py): throwaway generation code for review and repeatability. The two full World Bank source PDFs are intentionally outside Git.

## Source and rights check

The [publisher record](https://openknowledge.worldbank.org/entities/publication/582c44fd-db27-57b9-bc1c-60270b43bc02) identifies both *Land Matters* editions as CC BY 3.0 IGO. The exact source PDFs and source hashes are in the manifest. Their rights pages allow reuse with attribution and warn about separately credited components. Source PDF pages 19–20 were inspected visually in both editions: they are executive-summary prose pages without photos, figures, or tables. Attribution and adaptation notice accompany the fixtures in their README. The rest of the corpus is purpose-written and fictional. No private document is included.

The full English and Arabic reports have 131 and 117 pages respectively and are outside the MVP page limit; only two-page excerpts enter the corpus. All 15 final fixtures have at most two pages and are below 25 MB.

## Independent real-layout check

An independent four-page World Bank [water knowledge note](https://documents1.worldbank.org/curated/en/099052424151038179/pdf/P1790611ab765f07c19adc190a213586d42.pdf), *Preventing Rapid Corrosion of Handpumps Through Regulations*, was downloaded and inspected outside the 15 fixtures (SHA-256 `45dd9b7b57bbbb200148ee85819874315e93bfd928e08e700d5d5c9154209714`). It is about 1.19 MB, has a native text layer, a two-column page, and separately credited imagery. It was not redistributed or used as gold truth. This checks another real professional layout but does not add independent Arabic or scanned-report coverage.

## Machine review completed

- Counted 15 PDFs, 36 core cases (four semantic questions per family × three modalities), and six stress expectations.
- Reopened every PDF, checked page counts, byte limits, hashes, positive visible-page geometry, and normalized regions within `[0,1]`.
- Verified `pdftotext` returns text for native versions and none for image-only scanned versions; mixed versions retain partial native text. The bilingual mixed version has a scanned table region on a page that also contains native Arabic and English.
- Rendered and inspected all first pages and selected second pages; spot-checked region overlays for English, Arabic, bilingual, rotation, crop, and multi-page-table cases. The crop test has an intentionally hidden decoy outside its CropBox. The rotation and crop regions still need human viewer confirmation.
- The bilingual combined and derived-statistic questions require the numeric 2025 target shown in Arabic; the English text does not repeat that number.

## Human verification checklist

A bilingual reviewer opened the PDFs and used the annotation file as a checklist. The reviewer confirmed the full corpus, with no corrections reported.

- [x] Confirm the English and Arabic two-page excerpts are readable, correctly attributed, and free of separately credited visual components on those exact pages.
- [x] Confirm Arabic wording, digits, and right-to-left order in the three Arabic and three bilingual variants. The machine-extracted Arabic text can appear in visual order; judge the displayed PDF.
- [x] Confirm the 12 distinct core questions and expected answers below, including no answer for the two absent-data questions. Repeat the content check against all three modalities; the facts must match across variants.
- [x] Check every citation region on its **original displayed PDF page**. A region must cover the visible words or table cells claimed; fix any broad or shifted region. For scanned pages, OCR text is not yet gold—the visible image and reviewer judgment are.
- [x] Check the six stress expectations, especially the rotated 97.2%, cropped visible 71% versus hidden 99%, and continued-table North/West cells on different pages.
- [x] Record reviewer name, review date, disagreements, and adjudication. A reviewer must speak for themselves; agent self-review does not satisfy this gate.

| Family | Type | Question / expected answer to confirm |
| --- | --- | --- |
| English | Direct | Barren MENA land? **84%**. |
| English | Combined | Why modernize land administration? Scarcity and access problems, with registration, digital records, transparency, and accessible land information as priorities. |
| English | Statistic | Firms identifying land access as a major constraint? **23%** of manufacturing/service firms. |
| English | Insufficient | 2025 MENA property-tax revenue? **Not in excerpt; abstain.** |
| Arabic | Direct | ما نسبة الأراضي القاحلة؟ **٨٤٪**. |
| Arabic | Combined | لماذا تحديث إدارة الأراضي؟ الندرة وصعوبة الوصول؛ تسجيل الملكية ورقمنة السجلات والشفافية وإتاحة المعلومات. |
| Arabic | Statistic | ما نسبة الشركات التي تعد الحصول على الأراضي قيداً رئيسياً؟ **٢٣٪**. |
| Arabic | Insufficient | إيرادات ضريبة العقارات لعام ٢٠٢٥؟ **غير مذكورة؛ الامتناع.** |
| Bilingual | Direct | North Basin 2024 delivery? **12.4 million m³**. |
| Bilingual | Combined | 2025 target and observed status? **23.0 million m³ target in Arabic; no observed 2025 value; 2024 actual 21.5 million m³ in English.** |
| Bilingual | Table/statistic | Target minus 2024 delivered total? **1.5 million m³**, derived from Arabic target and English/table actual. |
| Bilingual | Insufficient | 2025 actual delivery? **Not reported; abstain.** |

Reviewer: **Haitham Ahmed (`haitham113`), project owner**  
Review date: **2026-10-07**  
Corrections/adjudication: **None reported. The reviewer confirmed the full corpus in conversation.**

## Known limits

These are controlled comparisons; the three variants of each family are correlated. The real World Bank pages are dense prose and have no table on the selected pages, so table evaluation relies on purpose-written bilingual and stress fixtures. The independent real-layout check is English/native only. Handwriting, broad chart reasoning, and sensitive private data remain out of MVP scope. Final release thresholds and a larger held-out validation set belong to later AI-evaluation decisions.
