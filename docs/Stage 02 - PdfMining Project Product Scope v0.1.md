# PdfMining — Project / Product Scope

## 1. Document Control

| Field | Value |
|---|---|
| Product | PdfMining |
| Document | Project / Product Scope |
| Version | v0.1 |
| Status | Draft for approval |
| Primary Source | Stage 01 — PdfMining Product / Feature Brief |
| Supporting Source | Stage 00 — Product Discovery Decision Summary |

---

## 2. Purpose of This Document

This document defines the approved project and product boundary for the first production-style PdfMining release.

It controls:

- what the MVP must include;
- what the MVP intentionally does not include;
- the supported end-to-end user journeys;
- the supported PDF and language scenarios;
- the boundaries of structured extraction, chat, citations, evidence verification, export, privacy, and platform behavior;
- the project deliverables required for the MVP to be considered complete;
- assumptions, constraints, dependencies, accepted limitations, and scope risks.

This scope is the contract that later requirements and design stages must elaborate without silently expanding or shrinking the release boundary.

Stage 03 — PRD may define detailed user-facing behavior, states, interactions, edge cases, and acceptance criteria. Stage 04 — SRS may formalize system requirements. Stage 05 — Wayfinder / Architecture Decisions and Stage 06 — Technical Design may determine how approved behavior is implemented. None of those stages may add or remove material product scope without a recorded scope change.

---

## 3. Project Objective

The PdfMining MVP must deliver a usable, evidence-first web product that allows an authenticated individual professional to investigate a supported PDF from upload through structured analysis, grounded question answering, evidence inspection, exact source navigation where coordinates are reliable, and optional structured-statistics export.

At completion, the product must be able to:

- accept supported native, scanned, and mixed native/scanned PDFs;
- handle Arabic, English, and mixed-language document content;
- preserve the original uploaded PDF unchanged as the canonical source;
- extract a useful internal representation, applying OCR selectively where required;
- produce a concise document overview;
- surface useful statistics and KPIs with provenance;
- reconstruct tables only when sufficiently reliable;
- distinguish directly extracted metrics from derived metrics;
- answer document questions using document evidence only;
- support contextual follow-up questions;
- attach statement-level evidence to document-derived factual claims;
- assess and communicate Evidence Support as High, Medium, or Low;
- navigate from citations to the correct page and, where reliable coordinates exist, the exact highlighted source region;
- retain private document history until the user deletes the document;
- remove document-specific data when the user deletes a document;
- export structured statistics to CSV and Excel with provenance;
- expose processing states, partial failures, OCR limitations, uncertainty, and unsupported cases instead of hiding them.

The MVP is complete only when these capabilities form a coherent end-to-end user experience, not merely when individual technical components exist.

---

## 4. MVP Release Definition

For PdfMining, **MVP** means the first complete release in which a user can perform the following vertical journey:

> Sign in → upload a supported PDF → provide a valid password if required → observe document processing → receive usable results even when a non-critical processing capability partially fails → review a concise overview and extracted information → search/filter statistics and inspect reliable reconstructed tables → ask questions and contextual follow-ups → receive document-grounded answers → inspect statement-level supporting evidence and Evidence Support → navigate to the original PDF page and highlighted source region when reliable coordinates exist → optionally export structured statistics with provenance → later return to or delete the document.

The release must support this journey for representative:

- native/text PDFs;
- scanned/image PDFs;
- mixed native/scanned PDFs;
- Arabic documents;
- English documents;
- mixed Arabic/English documents.

The MVP does **not** mean universal PDF understanding. It is deliberately bounded by document limits, supported languages, known OCR/table limitations, and a document-only evidence policy.

The initial configured document boundary is:

- **maximum pages: 20**;
- **file-size target: approximately 25 MB**, configuration-controlled.

These limits are part of the MVP scope baseline. Large-document behavior beyond this boundary is post-MVP.

---

## 5. Target Users in Scope

### 5.1 Primary MVP Users

The primary audience is **individual professionals working with information-heavy documents**, including:

- analysts;
- consultants;
- researchers;
- engineers;
- managers;
- other business professionals.

Typical documents include business reports, financial or operational reports, tenders and specifications, and research/report-style PDFs.

**Supported MVP workflows for these users:**

- privately upload and retain PDFs;
- investigate native, scanned, Arabic, English, and mixed-language PDFs;
- obtain a concise document overview;
- locate structured statistics and KPIs;
- inspect reliable table reconstructions;
- distinguish extracted and derived metrics;
- ask document questions and follow-up questions;
- inspect citations and Evidence Support;
- navigate to supporting evidence in the original PDF;
- export structured statistics with provenance;
- delete a document and its document-specific derived data.

**Not targeted in the MVP:**

- shared team or organization workflows;
- casual consumer PDF chat as a primary positioning;
- multi-document research workspaces;
- enterprise administration;
- collaborative review/annotation workflows.

### 5.2 Secondary Users

No separate secondary MVP audience is approved.

Business teams and organizations are a post-MVP product direction and must receive separate product discovery before their detailed behavior is defined.

---

## 6. Supported End-to-End User Workflows

### Workflow W1 — Authenticate and Access Private Documents

**Included outcome:**  
A user can authenticate into a private individual account and access only their own documents, analysis history, conversations, statistics, citations, and derived artifacts.

**Scope notes:**  
The MVP is single-user at the account/workspace level. Strict per-user isolation is a product requirement.

**Not included:**  
Teams, organizations, shared workspaces, collaborative roles, enterprise SSO, or organization administration.

### Workflow W2 — Upload a PDF

**Included outcome:**  
A user can upload a PDF within the configured limits. If the PDF is password-protected, the user may provide the valid password for processing.

**Scope notes:**  
PDF is the only accepted document format. Initial limits are 20 pages and approximately 25 MB, configuration-controlled.

**Not included:**  
DOCX, PPTX, spreadsheets, images as standalone uploads, or password/encryption bypass.

### Workflow W3 — Process Native, Scanned, or Mixed PDFs

**Included outcome:**  
PdfMining processes native text directly and applies OCR selectively to scanned pages or regions where required. The original PDF remains unchanged.

**Scope notes:**  
Common page rotation should be handled. OCR output should retain usable text, coordinates, reading order, and confidence where available. Processing states and limitations must be visible.

**Not included:**  
A guarantee that every malformed, degraded, handwritten, or visually complex PDF can be successfully interpreted.

### Workflow W4 — Review Document Overview and Processing Quality

**Included outcome:**  
The user can receive a concise automatic document overview and understand whether the document completed processing, partially completed, required OCR, or encountered limitations.

**Scope notes:**  
Poor OCR quality, partial failures, and unsupported content must be disclosed rather than hidden.

**Not included:**  
A guarantee that the overview captures every relevant fact in the document.

### Workflow W5 — Explore Statistics, KPIs, and Reliable Tables

**Included outcome:**  
The user can inspect automatically extracted quantitative facts and KPIs, search/filter them, inspect source provenance, view reliable structured table reconstructions, and distinguish extracted values from derived metrics.

**Scope notes:**  
Useful extraction is required; exhaustive numeric discovery is not guaranteed. Derived values must be explicitly labeled and traceable to source evidence.

**Not included:**  
Full BI/dashboard functionality, guaranteed discovery of every number, chart numerical interpretation, or perfect reconstruction of arbitrarily complex tables.

### Workflow W6 — Ask Document Questions

**Included outcome:**  
The user can ask natural-language questions about one document in Arabic or English and ask contextual follow-up questions.

**Scope notes:**  
Answers must be grounded in the uploaded document. Conversation history may clarify intent but is not evidence.

**Not included:**  
Multi-document chat, external web search, or general model knowledge presented as evidence.

### Workflow W7 — Inspect Citations and Evidence Support

**Included outcome:**  
Document-derived factual claims can be associated with statement-level citations, source previews, page references, one or multiple supporting passages, and High/Medium/Low Evidence Support.

**Scope notes:**  
The product should show the minimal sufficient supporting evidence set while permitting additional supporting evidence where useful. Unsupported factual claims should normally be withheld.

**Not included:**  
Evidence Support presented as a probability of universal factual truth or as generic model confidence.

### Workflow W8 — Navigate to Exact Original Evidence

**Included outcome:**  
Selecting a citation can take the user to the relevant page in the original PDF and, when reliable source coordinates exist, to the exact source region highlighted in yellow.

**Scope notes:**  
Native coordinates are used for native text; OCR coordinates are used for scanned content. Exact highlighting is conditional on coordinate reliability.

**Not included:**  
Simulated or fabricated exact highlighting when reliable coordinates cannot be established.

### Workflow W9 — Export Structured Statistics

**Included outcome:**  
The user can export structured statistics to CSV or Excel with enough provenance to remain traceable to document evidence.

**Scope notes:**  
Exported derived metrics must remain distinguishable from directly extracted values.

**Not included:**  
Chat transcript export, standalone citation export, or guaranteed arbitrary table export unless later added by scope change.

### Workflow W10 — Return to or Delete a Document

**Included outcome:**  
The user can return to previously processed private documents and delete a selected document.

**Scope notes:**  
Document deletion must remove the original PDF and associated document-specific derived artifacts, conversations, statistics, and evidence/citation data.

**Not included:**  
Organization-level retention policies or shared-document lifecycle management.

---

## 7. Functional Scope

### 7.1 User Accounts and Access

**MVP Included**

- authenticated individual accounts;
- private per-user access;
- strict isolation of original files and derived data;
- access to each user's own document and analysis history.

**Conditional / Limited**

- account UX details, password policy, recovery flows, and session behavior are requirements-stage concerns and are not defined here.

**Deferred**

- team and organization accounts;
- collaborative roles;
- enterprise identity integration.

**Out of Scope**

- shared workspace access in MVP.

### 7.2 Document Upload and Management

**MVP Included**

- PDF-only upload;
- initial configurable limit of 20 pages;
- approximately 25 MB file-size target, configuration-controlled;
- password-protected PDF processing when a valid password is supplied;
- private document history;
- document-specific deletion.

**Conditional / Limited**

- documents that cannot be parsed, decrypted with the supplied password, or processed sufficiently may fail with a visible error.

**Deferred**

- very large documents;
- additional document types.

**Out of Scope**

- password/encryption bypass.

### 7.3 PDF Processing

**MVP Included**

- processing of native, scanned, and mixed PDFs;
- visible processing states;
- graceful partial processing;
- common page-rotation handling;
- preservation of the original PDF;
- creation of a normalized internal representation.

**Conditional / Limited**

- complex/degraded PDFs may yield partial results;
- no universal parsing guarantee.

**Deferred**

- broader large-document processing at higher scale.

**Out of Scope**

- silently replacing the uploaded PDF with a regenerated canonical PDF.

### 7.4 Native PDF Extraction

**MVP Included**

- extract native text and document structure useful for analysis;
- preserve source relationships and coordinates where available;
- map citations/highlights to the original PDF.

**Conditional / Limited**

- unusual fonts, encodings, layout structures, or broken text layers may reduce extraction quality.

**Deferred**

- no separate advanced-native-layout feature is committed beyond the approved MVP behavior.

**Out of Scope**

- guaranteed extraction completeness for every native PDF.

### 7.5 Scanned PDF / OCR Handling

**MVP Included**

- OCR where required rather than indiscriminately for the whole document;
- OCR for scanned pages in mixed documents;
- retention of OCR text, source coordinates, reading order, and confidence where available;
- user-visible OCR quality/confidence disclosure;
- citation/highlight mapping using OCR coordinates.

**Conditional / Limited**

- quality depends on scan resolution, language, layout, rotation, noise, and OCR capability;
- exact highlighting is available only when coordinates are reliable.

**Deferred**

- handwriting understanding.

**Out of Scope**

- claiming OCR accuracy or completeness that has not been benchmarked.

### 7.6 Arabic and English Support

**MVP Included**

- Arabic document content;
- English document content;
- mixed Arabic/English document content;
- natural-language document interaction in Arabic and English;
- RTL-aware product behavior where Arabic text is presented.

**Conditional / Limited**

- mixed-language/code-switched questions may be handled where understandable, but no separate code-switching accuracy guarantee is established at scope level.

**Deferred**

- additional languages.

**Out of Scope**

- representing languages beyond Arabic and English as supported MVP languages.

### 7.7 Structured Statistics / KPI Extraction

**MVP Included**

- automatic extraction of useful quantitative facts and KPIs;
- provenance to supporting source evidence;
- explicit distinction between extracted and derived metrics;
- derived calculations when justified by source evidence;
- statistics search and filtering;
- comparison of conflicting values when surfaced from the same document;
- identification of repeated supporting evidence where relevant.

**Conditional / Limited**

- extraction coverage is best-effort;
- semantic labeling may be limited by source clarity;
- repeated or ambiguous metrics may require contextual presentation rather than forced deduplication.

**Deferred**

- advanced analytics across collections of documents;
- full dashboard/BI behavior.

**Out of Scope**

- guaranteed discovery of every numeric value or metric.

### 7.8 Tables and Structured Content

**MVP Included**

- structured table reconstruction when sufficiently reliable;
- extraction of statistics/KPIs from reliable table content with provenance.

**Conditional / Limited**

- scanned tables, merged cells, multi-page tables, nested structures, and visually complex tables may be partially reconstructed or withheld;
- the product must prefer no structured table over a confidently wrong reconstruction.

**Deferred**

- advanced table reconstruction guarantees;
- general-purpose table editing.

**Out of Scope**

- perfect reconstruction of arbitrary tables.

### 7.9 Document Chat / Q&A

**MVP Included**

- single-document Q&A;
- Arabic and English questions and responses;
- conversation-aware follow-up questions;
- document-only grounding;
- insufficient-evidence behavior;
- answers that combine evidence from multiple locations in the same document when required.

**Conditional / Limited**

- answer quality depends on available extraction/OCR and evidence quality;
- unsupported factual content should normally be removed before display.

**Deferred**

- multi-document chat.

**Out of Scope**

- external web/general-knowledge content used as evidence.

### 7.10 Citations

**MVP Included**

- statement/claim-level citations for document-derived factual claims where appropriate;
- page references;
- source text preview;
- one or multiple supporting passages;
- evidence across multiple pages where required;
- minimal sufficient evidence presentation;
- navigation from citation to source.

**Conditional / Limited**

- source-region precision depends on coordinate reliability;
- exact coordinate claims must be suppressed when mapping is unreliable.

**Deferred**

- standalone citation export.

**Out of Scope**

- page-only citation behavior as the sole evidence model for claims that require finer traceability.

### 7.11 Evidence Support / Verification

**MVP Included**

- verification of whether selected evidence supports a generated claim;
- user-visible High / Medium / Low Evidence Support;
- uncertain wording when support is not strong;
- normal suppression of unsupported factual claims.

**Conditional / Limited**

- High/Medium/Low internal thresholds will be calibrated empirically;
- low support is not the same as no support;
- calibration is not a public accuracy guarantee.

**Deferred**

- formal probability calibration;
- enterprise-configurable verification policies.

**Out of Scope**

- displaying Evidence Support as probability that the answer is factually true.

### 7.12 PDF Viewer and Exact Source Highlighting

**MVP Included**

- view the original uploaded PDF;
- exact page navigation;
- source-region navigation where reliable;
- yellow highlighting for cited evidence;
- native-coordinate and OCR-coordinate overlays as appropriate.

**Conditional / Limited**

- exact region highlighting is omitted or downgraded when coordinates are unreliable.

**Deferred**

- collaborative PDF annotations.

**Out of Scope**

- editing the canonical evidence or source PDF.

### 7.13 Search / Filter / Sort

**MVP Included**

- search within extracted statistics;
- filtering of structured statistics.

**Conditional / Limited**

- default ordering and basic presentation may be defined in the PRD;
- user-configurable advanced sorting is not an approved MVP requirement.

**Deferred**

- cross-document search;
- advanced faceted analytics.

**Out of Scope**

- search across document collections, because collections are post-MVP.

### 7.14 Export

**MVP Included**

- CSV export of structured statistics;
- Excel export of structured statistics;
- provenance sufficient to trace exported metrics back to evidence;
- extracted-vs-derived distinction retained in export.

**Conditional / Limited**

- values originating from reliable tables may appear through the statistics export where they meet the structured-statistic criteria.

**Deferred**

- arbitrary full-table export;
- chat export;
- standalone citation export.

**Out of Scope**

- regeneration of a modified PDF as the new canonical source.

### 7.15 Document History

**MVP Included**

- private history of processed documents;
- ability to return to previously processed documents;
- retention until user deletion;
- document-specific deletion of associated data.

**Conditional / Limited**

- organization-level retention and shared history are not applicable to the single-user MVP.

**Deferred**

- team/organization history policies.

**Out of Scope**

- shared document libraries.

### 7.16 Error and Partial-Processing Behavior

**MVP Included**

- meaningful visible states such as Uploaded, Extracting, OCR if required, Analyzing, Ready;
- visible failures and known limitations;
- graceful degradation so one failed capability does not unnecessarily invalidate successful capabilities;
- poor OCR disclosure;
- unsupported-content disclosure.

**Conditional / Limited**

- exact retry interaction is not fixed at this scope stage;
- no public availability or recovery SLA is established.

**Deferred**

- enterprise operational guarantees.

**Out of Scope**

- silently presenting failed or uncertain processing as fully successful.

---

## 8. Document Scope

| Document Scenario | MVP Status | Expected Behavior |
|---|---|---|
| PDF files | Included | Accepted as the only upload format, subject to configured limits. |
| Non-PDF files | Out of Scope | Rejected/not offered in MVP. |
| Native/text PDFs | Included | Extract native text/structure and map evidence to original coordinates where available. |
| Scanned/image PDFs | Included | OCR required pages; preserve OCR text, coordinates, reading order, and confidence where available. |
| Mixed native/scanned PDFs | Included | Use native extraction where available and OCR selectively where needed. |
| Arabic PDFs | Included | First-class supported document language. |
| English PDFs | Included | First-class supported document language. |
| Mixed Arabic/English PDFs | Included | Supported as an MVP document scenario. |
| Up to 20 pages | Included | Initial configured maximum. |
| More than 20 pages | Deferred | Large-document support is post-MVP unless the configured MVP limit is formally changed. |
| Approximately 25 MB or less | Included target | Initial configuration target; exact enforcement remains configuration-controlled. |
| Files above configured size | Deferred/Rejected | Not part of the supported MVP boundary. |
| Password-protected PDFs | Included conditionally | Process when the user supplies a valid password. |
| Encrypted PDFs without a valid password | Out of Scope | No password/encryption bypass. |
| Common page rotations | Included | Common rotations should be handled automatically. |
| Native text tables | Included conditionally | Reconstruct when sufficiently reliable. |
| Scanned/image tables | Limited | OCR/reconstruct when sufficiently reliable; otherwise disclose/withhold structured output. |
| Merged-cell tables | Limited | Best-effort; no reconstruction guarantee. |
| Multi-page tables | Limited | Best-effort; no guarantee of correct cross-page reconstruction. |
| Nested/visually complex tables | Limited | May be partially reconstructed or withheld. |
| Images | Accepted as document content | Preserved in the original PDF; no general image-understanding commitment. |
| Charts/graphs | Accepted as document content, interpretation excluded | May be visible in the PDF; numerical chart interpretation is not an MVP capability. |
| Arbitrary diagrams | Accepted visually, understanding excluded | No arbitrary multimodal diagram understanding. |
| Malformed/corrupted PDFs | Limited | Attempt normal processing only; failures must be visible. Repair is not guaranteed. |
| Handwritten documents/content | Out of Scope | Handwriting understanding is not supported. |
| Very low-resolution/degraded scans | Limited | Best-effort OCR with quality/confidence disclosure; results may be incomplete or unusable. |
| Unusual fonts/encodings/layouts | Limited | Best-effort extraction; limitations must remain visible. |

The document boundary is deliberately representative rather than universal. “PDF support” does not mean every syntactically valid PDF is guaranteed to yield complete or exact extraction.

---

## 9. PDF Source-of-Truth and Derivative Scope

### 9.1 Canonical Artifact

The **original uploaded PDF remains unchanged and is the canonical source of truth** for the document.

It must remain the authoritative visual and citation reference for the lifetime of the document in PdfMining.

### 9.2 Internal Normalization

PdfMining may create a normalized internal document representation containing elements required for product behavior, including:

- pages;
- text blocks and spans;
- text;
- reading order;
- bounding boxes;
- OCR content;
- tables;
- images;
- source coordinates;
- extraction confidence where available.

Internal normalization does not create a new canonical PDF.

### 9.3 Scanned PDF Derivative

PdfMining may optionally generate a searchable OCR PDF with an invisible text layer as a convenience derivative.

Such a derivative:

- may preserve original page imagery where possible;
- must not replace or overwrite the original upload;
- must not become the canonical citation source;
- must not be treated as evidence superior to the original document.

The derivative is optional and its presence is not required for the core citation model.

### 9.4 Highlighting

Citation highlighting must map back to the original PDF using:

- native source coordinates for native text;
- OCR source coordinates for scanned content.

If reliable source coordinates cannot be established, PdfMining must disclose that limitation and must not simulate an exact-location highlight.

### 9.5 Traceability Contract

The intended traceability chain is:

```text
Original PDF
→ Page
→ Block / Span
→ Text / OCR Text
→ Source Coordinates
→ Extracted Structure / Retrieval Context
→ Citation
→ Highlighted Original Evidence
```

Later architecture may change how intermediate data is represented, but it must preserve this user-visible source relationship.

---

## 10. Statistics / KPI Extraction Scope

### 10.1 Definition

For MVP scope, an **extractable structured statistic/KPI** is a quantitative fact that can be associated with sufficient semantic context and provenance in the document.

Typical included forms may include:

- counts;
- percentages;
- monetary values;
- ratios;
- rates;
- named KPIs;
- quantitative values associated with labels;
- quantitative values located in reliable tables;
- the surrounding sentence, row, label, or other context needed to understand the metric;
- source page and evidence reference.

### 10.2 Capability Classification

| Capability | MVP Classification | Scope Boundary |
|---|---|---|
| Automatically discover useful statistics/KPIs | Included | Useful coverage is required; exhaustive discovery is not guaranteed. |
| Extract counts/percentages/monetary values/rates/ratios | Included where context is clear | Must retain meaningful context and provenance. |
| Extract values from reliable tables | Included | Subject to table reconstruction reliability. |
| Associate contextual source text | Included | Enough context must remain available for verification. |
| Preserve page/evidence provenance | Included | Core requirement. |
| Infer semantic metric names | Limited | May infer/normalize labels when justified by document context; ambiguous semantics must remain visible. |
| Distinguish extracted vs derived | Included | Required. |
| Calculate derived metrics | Included conditionally | Only when justified by source evidence; must be labeled derived. |
| Compare conflicting values in one document | Included | Product should support investigation of conflicting values when surfaced. |
| Identify repeated evidence | Included/limited | Repetition may be surfaced; no guarantee of perfect global deduplication. |
| Deduplicate repeated metrics | Limited | Avoid misleading duplicates where practical, but no completeness guarantee. |
| Discover every numeric value | Excluded as a guarantee | The MVP does not promise exhaustive numeric extraction. |
| Numerical interpretation of charts | Out of Scope | Post-MVP candidate only. |
| Advanced cross-document analytics | Deferred | Requires future multi-document scope. |

The MVP must not imply that absence from the statistics view proves that a metric is absent from the PDF.

---

## 11. Table Scope

PdfMining includes **structured table extraction where reconstruction is sufficiently reliable**.

| Table Scenario | MVP Status | Expected Behavior |
|---|---|---|
| Native text table with clear structure | Included | Reconstruct and expose structured content when sufficiently reliable. |
| Scanned table | Limited | OCR and reconstruct where sufficiently reliable; otherwise disclose limitation or withhold structured output. |
| Image-based table | Limited | Same reliability rule as scanned tables. |
| Merged cells | Limited | Best-effort; may be withheld or simplified if relationships are ambiguous. |
| Multi-page table | Limited | Best-effort; no guarantee of correct cross-page joining. |
| Nested/irregular table | Limited | May not be reconstructed. |
| Extremely visual table | Limited | No guarantee of semantic reconstruction. |
| Statistics derived from a reliable table | Included | May be surfaced with provenance. |
| Arbitrary full-table CSV/Excel export | Deferred | MVP export commitment is structured statistics with provenance, not general table export. |
| Perfect table reconstruction | Out of Scope | Explicitly not guaranteed. |

A table should not be presented as confidently structured if the system cannot establish a sufficiently trustworthy reconstruction.

The original table remains viewable in the source PDF regardless of whether structured reconstruction succeeds.

---

## 12. Chart / Visual Content Scope

Charts, graphs, images, and diagrams may exist inside PDFs accepted by the MVP, but their presence does not imply full visual understanding.

| Capability | MVP Status |
|---|---|
| Display charts/images as part of the original PDF | Included |
| Preserve chart/image regions in the canonical PDF | Included |
| Extract nearby native/OCR text such as captions where it is ordinary document text | Limited / incidental |
| Dedicated chart-type detection | Not required for MVP |
| Read chart labels as a chart-specific semantic feature | Not required / limited to ordinary text extraction |
| Extract numerical values encoded visually in charts/graphs | Out of Scope |
| Reason quantitatively about charts/graphs | Out of Scope |
| Arbitrary diagram understanding | Out of Scope |
| Treat a chart region itself as verified numerical evidence | Out of Scope for MVP |
| Highlight textual evidence near/within visual content when reliable text/OCR coordinates exist | Conditional |
| General visual-evidence highlighting without reliable textual/OCR grounding | Out of Scope |

Full chart intelligence is post-MVP. If a document answer depends on a value visible only in a chart, PdfMining must not pretend that value has been reliably extracted unless a future approved capability supports it.

---

## 13. Chat / RAG Scope

### 13.1 Included Behavior

The MVP supports:

- chat about **one uploaded document at a time**;
- Arabic questions and responses;
- English questions and responses;
- mixed Arabic/English document evidence;
- contextual follow-up questions;
- answers grounded in the uploaded document;
- answers that combine evidence from multiple locations in the same document where required;
- multiple citations when a claim requires more than one supporting passage;
- retention of document-associated conversation history until the document is deleted;
- explicit insufficient-evidence responses when the document does not establish the requested fact.

### 13.2 Grounding Contract

- The uploaded document is the evidence source.
- External model knowledge must not silently fill evidence gaps.
- Conversation history may help determine what the user means, but conversation history is not evidence.
- Prompt-like instructions contained inside a PDF are untrusted document data and must not override application behavior, security rules, or user isolation.
- Document-derived factual claims should be traceable to supporting evidence where appropriate.
- Unsupported factual claims should normally be removed before presentation.
- Medium-support claims may be shown only with wording that reflects inference or uncertainty.
- Poor OCR or extraction quality should reduce downstream confidence/support rather than be hidden.

### 13.3 Deferred / Excluded Chat Behavior

- multi-document chat: deferred;
- web search as evidence: out of scope;
- general-knowledge answers presented as sourced from the document: out of scope;
- autonomous agent actions: not part of the approved MVP;
- organization/shared chat history: deferred.

This section defines product behavior only and does not prescribe the retrieval, chunking, reranking, embedding, or generation implementation.

---

## 14. Citation Scope

### 14.1 MVP Citation Contract

For document-derived factual claims, the citation experience should operate primarily at **statement/claim level**.

A citation should be capable of resolving to:

> **Document → Page → Source Region / Span → Source Text → Coordinates**

The MVP includes:

- statement/claim-level citations where appropriate;
- page number/reference;
- source text preview;
- one supporting passage or multiple supporting passages;
- evidence across multiple pages where required;
- minimal sufficient supporting evidence as the primary display principle;
- access to additional supporting evidence where useful;
- click/select-to-source navigation;
- exact region highlighting when reliable coordinates exist;
- OCR-based citations for scanned content;
- citations/provenance for structured statistics and reliable table-derived values;
- suppression or explicit insufficiency behavior for unsupported statements.

### 14.2 Citation Numbering

A specific numbering scheme is **not a scope-level requirement**. The PRD may define presentation identifiers or numbering as long as the user can unambiguously associate each claim with its evidence.

### 14.3 Guarantees vs Best Effort

**MVP guarantees at the product-contract level:**

- citations must refer to the original uploaded PDF, not a replacement canonical derivative;
- page navigation must identify the correct supporting page for a displayed citation;
- exact-region highlighting must only be shown when reliable coordinates exist;
- the product must not fabricate exact coordinate certainty;
- multiple supporting sources must be allowed when one passage is insufficient.

**Best-effort / conditional behavior:**

- precise source-region granularity where layout/OCR mapping is degraded;
- complex table-region citations;
- source mappings in malformed or low-quality documents.

A correct textual answer paired with a wrong citation or highlight is a quality failure, not an acceptable tradeoff.

---

## 15. Evidence Support Scope

### 15.1 Meaning

**Evidence Support** represents:

> **How strongly the selected source evidence supports a specific generated claim.**

It is a relationship between a claim and the evidence selected from the uploaded document.

It does **not** represent:

- vector similarity;
- retrieval relevance by itself;
- OCR confidence;
- generic model confidence;
- probability that the generated answer is factually true;
- probability that a claim is universally true.

> **The evidence-support indicator must not be represented as a probability that the generated answer is factually true.**

### 15.2 MVP User-Facing Representation

The MVP displays categorical labels:

- **High** — selected evidence directly and strongly supports the claim;
- **Medium** — evidence provides meaningful but incomplete, inferential, or qualified support; answer wording must reflect that uncertainty;
- **Low** — evidence is weak/ambiguous and must not be presented using stronger language than justified.

No user-facing percentage is required for MVP.

An **unsupported** claim is not merely “Low.” Unsupported factual claims should normally be removed before the answer is shown, or the answer should explicitly state that the document does not establish the claim.

### 15.3 Calibration

Internal thresholds for High/Medium/Low are intentionally **not fixed in this scope**. They must be empirically calibrated using representative claim/evidence evaluation data.

Calibration is a validation activity, not an unresolved MVP scope decision.

---

## 16. Search, Filtering and Export Scope

### 16.1 Search and Filtering

**MVP Included**

- search within extracted statistics/KPIs;
- filtering of structured statistics;
- locating metrics while retaining provenance.

**Not required as an MVP commitment**

- advanced user-configurable sorting;
- faceted search across document collections;
- cross-document search.

The PRD may define default ordering and basic controls without expanding the scope into analytics/dashboard behavior.

### 16.2 Export

**MVP Included**

- CSV export of structured statistics;
- Excel export of structured statistics;
- provenance information sufficient to trace an exported metric back to source evidence;
- distinction between extracted and derived values.

**Deferred / Not Included**

- arbitrary full-document export;
- regenerated PDF export as a new canonical artifact;
- general-purpose full-table export;
- standalone citation export;
- chat transcript export;
- multi-document export packages.

---

## 17. Authentication and User Data Scope

### 17.1 Individual Accounts

The MVP includes authenticated, private, single-user accounts.

The account boundary must ensure that one user cannot access another user's:

- original PDFs;
- OCR/extracted text;
- normalized representations;
- retrieval data;
- statistics;
- conversations;
- citations/evidence artifacts;
- other document-derived data.

### 17.2 Document Ownership and History

- Uploaded documents belong to the authenticated account that uploaded them.
- Documents remain in the user's private history until explicitly deleted.
- The user can return to previously processed documents and associated analysis.

### 17.3 Document Deletion

Deleting a document must remove document-specific:

- original PDF;
- optional OCR/searchable derivatives;
- normalized document representations;
- extracted artifacts;
- retrieval/chunk/embedding artifacts where present;
- statistics;
- associated conversations;
- evidence/citation artifacts;
- unnecessary temporary processing artifacts associated with the deleted document.

The exact storage topology is a Technical Design concern; complete logical deletion behavior is a product requirement.

### 17.4 Not Included in MVP

- teams;
- organizations;
- shared workspaces;
- role-based collaboration;
- enterprise SSO;
- organization admin portal;
- billing/subscriptions.

---

## 18. Security and Privacy Scope

### 18.1 MVP Requirements

The MVP requires:

- strict isolation of each user's documents and derived data;
- encryption in transit;
- encryption at rest;
- secure handling of stored documents and derived artifacts;
- document-specific deletion;
- minimization of document content sent to external AI providers;
- provider configurations that preferably do not use submitted data for model training and minimize or disable retention where available;
- operational logs that minimize document content;
- exclusion of secrets such as PDF passwords from logs;
- cleanup of unnecessary temporary artifacts after failed processing;
- treatment of PDF content as untrusted data;
- understandable disclosure of external processing/privacy behavior where relevant.

### 18.2 Retention

Documents and their document-specific analysis data remain stored until explicitly deleted by the user.

No organization-level retention policy is part of MVP scope.

### 18.3 External Providers

External AI/OCR-related providers may be used. Product behavior must not assume a single permanent provider.

Only the minimum necessary content should be sent for a given processing task where external processing is used.

### 18.4 Hosting

- The MVP is hosted on the project's **existing VPS**.
- Hosting-region selection is not offered.
- Multi-region deployment is not included.
- Configurable regional data residency is not included.
- The physical hosting location is an infrastructure fact to disclose where relevant, not a user-selectable product feature.

### 18.5 Compliance Boundary

The MVP does **not** claim certifications or regulated-industry compliance such as:

- SOC 2 certification;
- ISO 27001 certification;
- HIPAA compliance/certification;
- government security certification;
- other enterprise/regulatory attestations not separately established.

Ordinary confidential professional/business documents are within the intended usage direction, subject to the stated privacy behavior and without unsupported compliance claims.

---

## 19. Non-Functional Scope

### 19.1 Performance

The following are **validation targets, not public SLAs**:

| Scenario | Initial Validation Target |
|---|---|
| Typical native PDF within the initial document limit | Roughly 30–60 seconds |
| OCR-heavy PDF within the initial document limit | Roughly 2–3 minutes |
| Typical chat question | Approximately 5–10 seconds |
| Preliminary engineering concurrency scenario | Approximately 10 simultaneously active users |

These targets must be benchmarked on representative documents and the actual hosting environment.

Grounding/citation correctness must not be silently sacrificed merely to meet latency targets.

### 19.2 Reliability

The MVP requires:

- visible failed-processing states;
- graceful degradation;
- continued usability of successful capabilities when another non-critical capability fails;
- no silent conversion of partial processing into a “fully successful” state;
- preservation of source truth even when downstream extraction fails.

No public uptime SLA, recovery-time SLA, or automatic-retry guarantee is established at this stage.

### 19.3 Usability

The MVP requires:

- a document-centered desktop experience;
- the original PDF visible alongside analysis/chat through an appropriate workspace;
- responsive mobile web behavior using switchable views rather than forcing the desktop split-screen layout;
- clear processing states;
- visible limitations;
- Arabic/RTL-aware presentation where appropriate.

Detailed wireframes and interaction patterns belong in later product/design requirements.

### 19.4 Scalability

The MVP is designed for initial validation rather than enterprise scale.

The only approved preliminary concurrency target is approximately 10 simultaneously active users as an engineering validation scenario.

Higher concurrency, very large documents, organization-scale usage, and distributed/multi-region operation are post-MVP concerns.

### 19.5 Accessibility

No specific accessibility certification or numeric conformance target was approved in Stage 01.

The MVP must therefore **not claim** WCAG or other accessibility conformance unless later requirements explicitly define and validate it.

---

## 20. Platform Scope

| Delivery Surface | MVP Status | Boundary |
|---|---|---|
| Web application | Included | Primary product surface. |
| Desktop browser | Included | Primary document-centered split-screen experience. |
| Mobile-responsive web | Included | Responsive switchable views for smaller screens. |
| Native iOS app | Out of Scope | Future discovery required. |
| Native Android app | Out of Scope | Future discovery required. |
| Browser extension | Out of Scope | Not approved for MVP. |
| Public API | Out of Scope | Not approved for MVP. |
| Desktop native application | Out of Scope | Not approved for MVP. |

Specific supported browser versions are a later requirements/QA decision and are not fixed in this scope.

---

## 21. MVP Deliverables

### 21.1 Product Deliverables

Stage 1 development is complete only when the following tangible product outputs exist:

1. **Functioning PdfMining web application** implementing the approved end-to-end MVP journey.
2. **Authentication and private single-user document access**.
3. **PDF upload and management experience** with the approved initial document limits.
4. **Document-processing capability** for representative native, scanned, and mixed PDFs.
5. **Selective OCR behavior** with quality/confidence disclosure.
6. **Normalized internal document representation** sufficient to support approved product behavior while preserving the original PDF.
7. **Concise automatic document overview**.
8. **Structured statistics/KPI extraction** with provenance and extracted/derived distinction.
9. **Reliable-table presentation** when reconstruction is sufficiently trustworthy.
10. **Single-document grounded chat** with contextual follow-up questions.
11. **Statement-level citation experience** with source previews and multiple sources where needed.
12. **Evidence verification and High/Medium/Low Evidence Support**.
13. **Original-PDF viewer** with page navigation and exact yellow highlighting where reliable coordinates exist.
14. **CSV and Excel statistics export** with provenance.
15. **Private document history and complete document-specific deletion**.
16. **Visible processing states, partial failures, errors, OCR limitations, and uncertainty**.
17. **Deployment on the project's existing VPS** suitable for MVP use.
18. **Representative evaluation/test PDF set** spanning Arabic, English, mixed-language, native, scanned, and mixed native/scanned cases.
19. **Documented validation results** for the provisional performance and quality dimensions before making stronger claims.
20. **Source repository and sufficient technical/deployment documentation** to operate and continue development of the MVP.

### 21.2 Portfolio Deliverables

Because PdfMining is also intended as a flagship AxioStack AI portfolio project, Stage 1 should additionally produce:

- a credible demo flow using representative documents;
- examples showing structured extraction with provenance;
- examples showing grounded answers and claim/evidence verification;
- examples of navigation to exact original evidence where coordinates are reliable;
- examples that visibly communicate OCR limitations, insufficient evidence, and partial processing;
- a portfolio/case-study presentation that does not imply unsupported completeness or accuracy guarantees.

Portfolio material does not override product truth or conceal accepted limitations.

---

## 22. Explicitly Out of Scope

The following are explicitly outside the PdfMining MVP boundary:

1. Non-PDF document ingestion such as DOCX, PPTX, spreadsheets, or standalone image uploads.
2. Multi-document chat.
3. Document collections/workspaces.
4. Team accounts and organization accounts.
5. Shared collaborative workspaces.
6. Collaborative annotations/review workflows.
7. Organization-level roles and collaborative RBAC behavior.
8. Very large-document support beyond the configured MVP boundary.
9. Handwriting understanding.
10. Numerical interpretation of charts or graphs.
11. Arbitrary multimodal diagram understanding.
12. Guaranteed discovery of every statistic, KPI, or numeric value.
13. Guaranteed extraction completeness.
14. Perfect reconstruction of arbitrarily complex tables.
15. Guaranteed reconstruction of merged, nested, or multi-page tables.
16. Full BI/dashboard functionality.
17. External web search or web content used as document evidence.
18. General model knowledge presented as evidence when the PDF does not establish a claim.
19. Editable canonical evidence or editing the original PDF as the evidence source.
20. Password cracking, encryption bypass, or access to protected PDFs without a valid user-supplied password.
21. Configurable hosting-region selection.
22. Multi-region deployment and configurable regional data residency.
23. Enterprise/regulatory certification claims not separately established, including HIPAA/government certification claims.
24. Enterprise SSO.
25. Organization administration portals.
26. Billing and subscription management.
27. Native mobile applications.
28. Browser extensions.
29. A public developer API.
30. Chat transcript export or standalone citation export.
31. Regeneration of a new PDF that replaces the original upload as the canonical source.

A capability not explicitly included elsewhere must not be inferred merely because it is common in comparable AI products.

---

## 23. Post-MVP / Future Scope

The following themes are approved directions or plausible candidates already identified in prior stages. They are **not commitments** until separately discovered and scoped.

### 23.1 Additional Document Reach

- additional document formats;
- very large documents;
- future revised page/file-size limits based on benchmarking.

### 23.2 Advanced Visual Document Understanding

- numerical chart/graph understanding;
- richer diagram understanding;
- improved complex-table reconstruction;
- advanced visual evidence extraction.

### 23.3 Multi-Document Knowledge Work

- document collections/workspaces;
- multi-document search;
- multi-document chat;
- cross-document comparison and analytics.

### 23.4 Team and Organization Use

- business teams;
- organizations;
- shared documents/workspaces;
- organization-level access management;
- collaboration;
- future organization retention/governance behavior.

### 23.5 Enterprise Controls

Potential enterprise requirements may later include stronger governance, SSO, auditability, compliance evidence, and regional data controls, but none are approved MVP commitments.

### 23.6 Provider and AI Evolution

- additional AI/OCR/verification providers;
- improved quality/cost/latency options;
- configurable verification policies after sufficient validation.

Provider/model choices remain a Technical Design/evaluation matter rather than a fixed product promise.

### 23.7 Advanced Analytics and Export

- broader metric analysis;
- cross-document analytics;
- richer table export;
- additional report/export formats.

---

## 24. Dependencies

| Dependency | Why It Matters | Scope Boundary |
|---|---|---|
| Existing VPS hosting environment | MVP must be deployable on the already-owned hosting environment. | Exact deployment architecture is deferred. |
| Persistent document/data storage capability | Required for original PDFs, history, derived data, and deletion semantics. | Storage technology is not fixed here. |
| PDF parsing/rendering capability | Required to display the original PDF and map source evidence. | Exact library/provider is deferred. |
| OCR capability supporting Arabic and English | Required for scanned/mixed documents. | Exact OCR technology is deferred. |
| AI language-model capability | Required for overview, document Q&A, and semantic synthesis. | Exact model/provider is deferred. |
| Retrieval/evidence-selection capability | Required for document-grounded Q&A. | Algorithm and embedding choices are deferred. |
| Evidence verification capability | Required for claim/evidence verification and Evidence Support. | Exact JEV/verification implementation is deferred. |
| Representative Arabic/English/mixed sample PDFs | Required to validate extraction, OCR, grounding, and citations. | Evaluation corpus must reflect approved document scenarios. |
| Representative native/scanned/mixed PDFs | Required to validate the complete processing boundary. | Must include realistic professional layouts. |
| Evaluation data for claim/evidence support | Required to calibrate High/Medium/Low Evidence Support. | Numeric thresholds are not set in scope. |
| External provider privacy/configuration options where used | Needed to minimize content transmission, training use, and retention. | Provider selection remains replaceable. |
| Spreadsheet export capability | Required for CSV/Excel statistics export. | Exact implementation is deferred. |

A dependency identifies something the project needs to succeed; it does not prescribe the architecture.

---

## 25. Assumptions

| ID | Assumption | Impact if False |
|---|---|---|
| A1 | The initial 20-page and ~25 MB limits are sufficient to demonstrate the product's core value. | MVP value may require revisiting the document boundary. |
| A2 | Representative professional native PDFs within the limits can be processed usefully. | Extraction scope or quality targets may need adjustment. |
| A3 | Representative scanned PDFs are sufficiently legible for OCR to produce useful text and coordinates. | Scanned-document usefulness and citation precision will fall. |
| A4 | Arabic, English, and mixed-language OCR/analysis can reach useful quality on representative samples. | A core MVP differentiator would be weakened and require remediation before release acceptance. |
| A5 | Table reconstruction is useful when the product withholds structures it cannot reconstruct reliably. | The table feature may need narrower acceptance criteria. |
| A6 | High/Medium/Low Evidence Support can be empirically calibrated to be meaningful to users. | The indicator may need redesign before being presented as a product differentiator. |
| A7 | OCR, retrieval, generation, and verification can be operated at an acceptable cost for the intended direction. | Provider choices, processing policy, or future commercial model may need change. |
| A8 | Users have legal/organizational permission to upload the documents they process. | Usage may create legal/privacy risk outside the intended operating assumptions. |
| A9 | Users have network access to the web application and any permitted external processing dependencies. | The product may not function as intended; offline behavior is not in scope. |
| A10 | External processing is permissible for the user's document under the disclosed provider/privacy configuration where such providers are used. | Some documents may be unsuitable for processing until alternative deployment/privacy behavior exists. |
| A11 | The existing VPS can support the initial validation workload after implementation benchmarking. | Hosting capacity or technical design may need revision without changing the product boundary. |
| A12 | Reliable source coordinates can be produced for a meaningful portion of representative native and OCR content. | Exact highlighting would be available less often, weakening a core differentiator. |

Assumptions must be tested where practical rather than converted into guarantees.

---

## 26. Constraints

### 26.1 Product Constraints

- MVP is PDF-only.
- Initial document maximum is 20 pages.
- Initial file-size target is approximately 25 MB and configuration-controlled.
- Large-document support is post-MVP.
- Accounts are private and single-user.
- Document chat is single-document.
- Answers are document-only grounded.
- Original uploaded PDF remains the source of truth.
- Exact highlighting is shown only when coordinates are reliable.
- Extracted and derived metrics must remain distinguishable.
- Partial processing must degrade gracefully.

### 26.2 Language and Document Constraints

- Arabic and English are first-class supported languages.
- Mixed Arabic/English document content is included.
- Handwriting understanding is excluded.
- Chart/graph numerical interpretation is excluded.
- Arbitrary diagram understanding is excluded.
- Complex table reconstruction is conditional rather than guaranteed.

### 26.3 Privacy and Security Constraints

- strict per-user isolation;
- encryption in transit and at rest;
- minimal external transmission of document content;
- logging must minimize sensitive document text and exclude secrets such as PDF passwords;
- documents remain stored until user deletion;
- document deletion must remove associated document-specific artifacts;
- no unsupported regulated-industry compliance claims.

### 26.4 Hosting Constraints

- MVP runs on the project's existing VPS;
- no hosting-region selection;
- no multi-region deployment;
- no configurable data residency in MVP.

### 26.5 AI/Provider Constraints

- product behavior should remain provider-independent where practical;
- exact OCR, embedding, LLM, reranking, and verification providers/models are not fixed by this scope;
- grounding quality must not be sacrificed merely to hit latency targets;
- document contents are untrusted data and cannot override system rules.

### 26.6 Portfolio Constraints

The portfolio/demo representation must show actual limitations honestly and must not imply guaranteed completeness, perfect accuracy, or false citation precision.

---

## 27. Known Limitations Accepted for MVP

The following limitations are accepted product boundaries and should not automatically be treated as defects if the product behaves transparently within them:

- OCR can be inaccurate or incomplete on degraded scans.
- Arabic OCR quality can vary by font, scan quality, layout, and content.
- Mixed-language pages may be harder to extract reliably.
- Unusual fonts or broken text layers may reduce native extraction quality.
- Extremely complex layouts may disrupt reading order or source mapping.
- Handwriting is unsupported.
- Very low-resolution scans may not produce useful OCR.
- Chart/graph numerical values are not interpreted.
- Arbitrary diagrams are not semantically understood.
- Merged, nested, multi-page, and highly visual tables may not reconstruct correctly.
- Table extraction may be withheld when reconstruction is not sufficiently reliable.
- Automatic statistic/KPI extraction may miss relevant metrics.
- Metric labels may be semantically ambiguous.
- Repeated metrics/evidence may not be perfectly deduplicated.
- Derived metrics may be unavailable when evidence is insufficient or ambiguous.
- Exact source-region highlighting may be unavailable when reliable coordinates cannot be established.
- OCR confidence does not imply Evidence Support, and Evidence Support does not imply universal factual truth.
- High/Medium/Low Evidence Support thresholds will require empirical calibration.
- AI responses may be limited or withheld when the document does not supply adequate evidence.
- Processing and chat timings are validation targets, not guaranteed SLAs.
- A non-critical processing capability may fail while other successful capabilities remain usable.

QA should treat false precision, hidden failures, incorrect citations, or violations of the evidence contract as defects; it should not treat the accepted absence of excluded capabilities as defects.

---

## 28. Scope Risks and Mitigations

| Risk | Scope Impact | Mitigation |
|---|---|---|
| Complex PDF layouts | High | Keep a clear supported-document boundary and expose partial/failed extraction. |
| Arabic OCR variability | High | Validate with representative Arabic and mixed-language samples and disclose OCR quality. |
| Degraded scans | High | Treat as best-effort and propagate OCR uncertainty downstream. |
| Complex table reconstruction | High | Only present structured tables when sufficiently reliable; do not guarantee arbitrary reconstruction. |
| Chart/visual extraction pressure | High | Keep numerical chart understanding and arbitrary diagrams outside MVP. |
| Citation precision | High | Treat correct source mapping as a core acceptance area and suppress false precision. |
| Evidence calibration | High | Validate High/Medium/Low empirically; do not present as factual probability. |
| AI hallucination | High | Require document-only grounding, verification, insufficient-evidence behavior, and normal suppression of unsupported factual claims. |
| Extraction completeness expectations | High | Explicitly state that automatic metric extraction is useful but not exhaustive. |
| Verification latency | Medium/High | Preserve grounding quality as priority and benchmark responsiveness before SLA commitments. |
| Provider/model variation | Medium | Keep provider choice replaceable where practical and evaluate changes against representative samples. |
| Processing cost | Medium/High | Validate unit economics on real workloads before pricing commitments. |
| Prompt injection inside PDFs | High | Treat document content as untrusted evidence that cannot override application rules. |
| Existing VPS capacity | Medium | Benchmark against the approved preliminary workload and adjust technical design/hosting capacity if needed. |
| Scope creep into enterprise/team features | High | Keep collaboration, organization behavior, SSO, billing, and regional controls explicitly post-MVP/out of scope. |
| “Simple” AI requests expanding complexity | High | Apply scope-change control to any new AI extraction, reasoning, visual, or verification behavior. |

---

## 29. Scope Change Control

A capability must not silently enter implementation unless it is:

- listed as **MVP Included** in this scope; or
- explicitly required to satisfy another approved MVP scope item.

Any significant capability addition, removal, or material behavior change must be recorded as a scope change and evaluated for impact on:

- timeline;
- implementation complexity;
- operating cost;
- architecture;
- privacy/security;
- evaluation and QA;
- user experience;
- deployment;
- downstream requirements/design documents.

Examples that require explicit scope review include:

- raising document limits materially;
- adding another document format;
- adding multi-document behavior;
- adding chart reasoning;
- adding collaboration;
- adding a new export type as a committed product feature;
- changing the document-only grounding policy;
- weakening citation/highlight requirements;
- changing the original-PDF source-of-truth policy;
- introducing enterprise or regional hosting commitments.

Apparently small AI requests may materially increase evaluation and reliability complexity; they are not exempt from scope control.

---

## 30. Open Scope Decisions

**No unresolved scope-level decisions remain.**

The following matters are intentionally deferred but do **not** block Stage 03 because they do not change the approved product boundary:

| Item | Status | Resolution Stage |
|---|---|---|
| Exact performance SLAs | Not an MVP scope decision; current values are validation targets | After implementation benchmarking |
| Numeric extraction/grounding acceptance thresholds | Benchmark-derived, not scope-defining | SRS / evaluation planning |
| High/Medium/Low Evidence Support thresholds | Empirical calibration required | SRS / Technical Design / validation |
| Exact OCR, embedding, LLM, reranking, verification providers/models | Implementation choice | Wayfinder / Technical Design |
| Long-term pricing | Commercial decision after unit-economics/value validation | Post-MVP/product validation |
| Future large-document limits | Post-MVP decision | Future discovery |
| Future team/organization behavior | Post-MVP decision | Future discovery |

> **No scope-level blockers remain for proceeding to Stage 03 — Product Requirements Document.**

---

## 31. Scope Acceptance Checklist

- [x] MVP boundary is explicit.
- [x] Post-MVP features are separated from MVP commitments.
- [x] Explicit exclusions are documented.
- [x] Supported document formats are defined.
- [x] Native, scanned, and mixed PDF behavior is defined.
- [x] OCR scope and limitations are defined.
- [x] Arabic, English, and mixed-language scope is explicit.
- [x] Initial 20-page and ~25 MB document limits are preserved.
- [x] Original uploaded PDF remains the source of truth.
- [x] Optional OCR-searchable derivatives cannot replace the canonical source.
- [x] Statistics/KPI extraction scope is defined.
- [x] Extracted and derived metrics are distinguishable.
- [x] Table boundaries are explicit.
- [x] Chart/visual-content boundaries are explicit.
- [x] Single-document chat behavior is bounded.
- [x] Document-only grounding is preserved.
- [x] Insufficient-evidence behavior is defined.
- [x] Citation guarantees and conditional precision are defined.
- [x] Exact highlighting is conditional on reliable coordinates.
- [x] Evidence Support semantics are defined and separated from OCR/model confidence.
- [x] High/Medium/Low user-facing labels are preserved.
- [x] Security/privacy scope is stated.
- [x] Existing-VPS hosting constraint is preserved.
- [x] No selectable region, multi-region deployment, or configurable data residency is included.
- [x] Accepted MVP limitations are documented.
- [x] Product and portfolio deliverables are defined.
- [x] Scope change control is defined.
- [x] No database schema, API design, service architecture, exact provider/model, detailed algorithm, or implementation backlog has been prematurely defined.

---

## 32. Recommended Next Stage

# Stage 03 — Product Requirements Document (PRD)

After this scope is explicitly approved, Stage 03 should transform each approved scope item into detailed product requirements, including:

- user-facing behavior;
- user stories/use cases;
- functional requirements;
- acceptance criteria;
- states and transitions;
- edge cases;
- interaction behavior;
- error behavior;
- validation behavior;
- permissions/access behavior;
- responsive/RTL behavior where relevant.

The PRD must elaborate the approved scope without expanding it.

No work should proceed to Stage 03 as an approved baseline until Stage 02 is explicitly accepted.
