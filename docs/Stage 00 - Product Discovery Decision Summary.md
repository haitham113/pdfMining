# PdfMining — Product Discovery Decision Summary

## 1. Product Vision

PdfMining is an **AI-powered document intelligence platform for professional PDF investigation**.

Its purpose is not merely to let users “chat with a PDF,” but to help them:

- understand complex documents;
- extract structured facts, statistics, KPIs, and tables;
- ask natural-language questions;
- receive document-grounded answers;
- verify exactly where each important claim came from;
- navigate directly to highlighted supporting evidence inside the original PDF.

The central product principle is:

> **Trustworthiness and traceability are more important than generative fluency.**

---

## 2. Target Users

### MVP primary audience

Individual professionals working with information-heavy documents, including:

- analysts;
- consultants;
- researchers;
- engineers;
- managers;
- business professionals.

### Product trajectory

Start with private single-user accounts, with future evolution toward business teams and organizations.

PdfMining is **not positioned as a casual consumer PDF chatbot**.

---

## 3. Primary Use Cases

The main job-to-be-done is:

> **Investigate complex PDFs and verify exactly where answers, facts, metrics, and conclusions came from.**

Core use cases include:

- asking questions about a PDF;
- locating supporting evidence;
- extracting statistics and KPIs;
- extracting structured tables;
- reviewing document summaries;
- comparing conflicting values within a document;
- identifying repeated evidence;
- exporting structured statistics with provenance;
- analyzing Arabic, English, and mixed-language PDFs.

The initial product remains horizontal rather than industry-specific, but testing should emphasize business reports, financial/operational reports, tenders/specifications, and research/report-style documents.

---

## 4. Core Value Proposition

PdfMining provides:

**Document understanding + structured extraction + grounded AI reasoning + evidence verification + exact source navigation.**

The product should answer not only:

> “What does this document say?”

but also:

> “Where exactly does it say that, and how strongly does the cited evidence support the claim?”

---

## 5. Product Differentiators

Key differentiators are:

- Arabic and English as first-class languages;
- mixed Arabic/English documents;
- native, scanned, and mixed PDFs;
- OCR;
- structured table extraction;
- automatic statistics/KPI extraction;
- derived-vs-extracted metric distinction;
- document-grounded RAG;
- statement/claim-level citations;
- citation verification;
- Evidence Support classification;
- exact source navigation;
- PDF highlight overlays;
- explicit uncertainty and limitation disclosure;
- provenance-preserving CSV/Excel exports.

The defining differentiator is the **evidence-first trust model**, rather than generic LLM chat.

---

## 6. MVP Definition

The MVP includes:

- authenticated single-user accounts;
- private document history;
- PDF-only uploads;
- configurable document limits;
- initial limit: **20 pages**;
- initial file-size target: approximately **25 MB**, configurable;
- native/text PDFs;
- scanned PDFs;
- mixed native/scanned PDFs;
- password-protected PDFs when the user provides the password;
- common page-rotation handling;
- Arabic, English, and mixed-language content;
- OCR with quality/confidence disclosure;
- structured internal document representation;
- table extraction where reconstruction is sufficiently reliable;
- automatic statistics/KPI extraction;
- derived metric calculations with explicit labeling;
- concise automatic document overview;
- grounded document chat;
- follow-up questions using conversation context;
- statement-level citations;
- multiple citations where jointly required;
- exact source highlighting where coordinates are reliable;
- citation/evidence verification;
- user-visible **High / Medium / Low Evidence Support**;
- statistics filtering/search;
- CSV/Excel export with provenance;
- partial-processing support;
- visible errors and known limitations;
- secure document history;
- complete document-specific deletion.

### MVP product priority

1. Grounding and citation correctness
2. Extraction accuracy
3. Useful coverage
4. UX responsiveness
5. Operating-cost optimization

---

## 7. Explicitly Out of Scope

For MVP:

- multi-document chat;
- document collections/workspaces;
- organizations and team collaboration;
- very large-document support;
- non-PDF document formats;
- handwriting understanding;
- numerical interpretation of charts/graphs;
- arbitrary multimodal diagram understanding;
- full BI/dashboard functionality;
- external web/general-knowledge answers;
- enterprise compliance certifications;
- configurable regional data residency;
- editable canonical evidence;
- password/encryption bypass;
- guaranteed extraction completeness;
- perfect reconstruction of arbitrarily complex tables.

These can be considered post-MVP where justified.

---

## 8. Key UX Decisions

The primary desktop experience should use a **document-centered split-screen workspace**.

The PDF remains visible alongside chat/analysis, with statistics available through appropriate panels/tabs.

Citation interaction should:

1. navigate to the relevant page;
2. locate the exact source region;
3. visually highlight the evidence.

Mobile should use responsive, switchable views rather than forcing desktop split-screen behavior.

Processing should expose meaningful states such as:

**Uploaded → Extracting → OCR if required → Analyzing → Ready**

Partial failures must remain visible.

A successfully processed capability should remain usable even when another capability fails.

Known limitations must always be explicitly communicated to the user.

---

## 9. AI Behavior Decisions

### LLM

Used for:

- answering;
- summaries;
- semantic synthesis;
- metric interpretation;
- Arabic/English natural-language responses.

### Embeddings

Used primarily for semantic retrieval.

### JEV / verification logic

Used for structured decisions including:

- relevance scoring;
- reranking;
- evidence selection;
- claim-support verification;
- citation-support scoring;
- grounded/unsupported classification;
- High / Medium / Low support classification.

JEV complements rather than replaces the LLM.

### Grounding policy

MVP answers are **document-only grounded**.

External model knowledge must not silently fill missing evidence.

When evidence is insufficient, PdfMining should explain what can and cannot be established.

Conversation history may determine what the user means, but it does not itself constitute evidence.

Document content must be treated as **untrusted data**, including any prompt-like instructions contained inside PDFs.

---

## 10. Citation and Evidence Decisions

Every document-derived factual claim should be traceable to evidence.

Citations operate primarily at **statement/claim level**, not merely answer or paragraph level.

A citation conceptually resolves to:

**Document → Page → Source Region / Span → Source Text → Coordinates**

A claim may have:

- one supporting source;
- multiple supporting passages;
- evidence across multiple pages.

The displayed evidence set should be the **minimal sufficient supporting set**, with additional supporting evidence accessible where useful.

### Evidence Support

Evidence Support represents:

> **How strongly the selected source evidence supports a specific generated claim.**

It does **not** mean:

- vector similarity;
- general model confidence;
- probability that the claim is universally true.

Internally, more granular scoring may exist.

For MVP, users see:

- **High**
- **Medium**
- **Low**

rather than potentially misleading percentages.

Unsupported factual claims should normally be removed before the answer is shown.

Medium-support claims may be shown only when their wording reflects the uncertainty or inference.

---

## 11. Document / OCR Decisions

### Canonical-source invariant

The **original uploaded PDF is always preserved unchanged as the source of truth**.

PdfMining normalizes the **internal document representation**, not the visible/canonical PDF.

The internal representation may contain:

- pages;
- text blocks and spans;
- reading order;
- bounding boxes;
- tables;
- images;
- OCR output;
- source coordinates;
- extraction confidence.

### Native PDFs

Use the original PDF and map extracted content back to its original coordinates.

### Scanned PDFs

PdfMining should:

1. preserve the original PDF;
2. OCR the pages;
3. retain OCR text, coordinates, reading order, and confidence;
4. use OCR coordinates for citation overlays.

An optional searchable PDF with an invisible text layer may exist as a convenience derivative.

It must **never become the canonical source**.

### Highlighting

The viewer displays the original PDF and renders overlays using stored coordinates.

If reliable source coordinates cannot be established, PdfMining must not pretend that an exact-location citation exists.

### Other document rules

- Mixed scanned/native documents are supported.
- OCR should be determined where needed rather than assumed for the whole document.
- Common rotations should be handled automatically.
- Handwriting is unsupported in MVP and must be explicitly disclosed.
- Poor OCR quality should propagate appropriate uncertainty downstream.

OCR confidence and Evidence Support are separate concepts.

---

## 12. Security and Privacy Decisions

Documents remain stored until explicitly deleted by the user.

Deleting a document should remove document-specific:

- original PDF;
- OCR/searchable derivatives;
- normalized representations;
- extracted artifacts;
- chunks;
- embeddings;
- statistics;
- associated conversations;
- evidence/citation artifacts.

External AI providers may be used, but only the minimum necessary document content should be transmitted.

Providers/configurations should preferably:

- not use submitted data for model training;
- minimize or disable retention where available.

Ordinary confidential professional/business documents are supported.

PdfMining should not make MVP claims of HIPAA, government, or other regulated-industry certification.

Stored data should be encrypted:

- in transit;
- at rest.

Operational logs should minimize document content and exclude secrets such as PDF passwords.

Strict per-user isolation applies across:

- files;
- OCR/extracted text;
- embeddings;
- retrieval;
- chat;
- statistics;
- citations.

Failed processing should clean unnecessary temporary artifacts.

Initial deployment uses one disclosed hosting region rather than promising selectable residency.

Users should receive understandable privacy/process disclosures.

---

## 13. Performance Assumptions

These are **initial validation targets**, not public SLAs.

### Document limits

Initially:

- maximum pages: **20**
- maximum file size: approximately **25 MB**

Both should be configuration-controlled.

Therefore, “large-document support” is **post-MVP**, not an initial product claim.

### Processing targets

For a typical ≤20-page document:

- native PDF: roughly **30–60 seconds**
- OCR-heavy PDF: target roughly **2–3 minutes**

These must be benchmarked before becoming promises.

### Chat

Typical question target:

**approximately 5–10 seconds**

Grounding quality should not be silently sacrificed merely to achieve latency.

### Concurrency

A preliminary validation target is approximately:

**10 simultaneously active users**

This is an engineering validation scenario, not a commercial SLA.

---

## 14. Open Risks

Important risks include:

### OCR accuracy

Arabic, degraded scans, unusual layouts, and mixed-language pages may produce poor extraction.

### Table reconstruction

Complex tables, merged cells, visual layouts, and scanned tables may be difficult to reconstruct reliably.

### Citation correctness

Accurate textual answers with inaccurate highlight coordinates would undermine the product's main differentiator.

### Evidence calibration

High/Medium/Low must eventually be validated empirically rather than assigned using arbitrary thresholds.

### Extraction completeness

Automatic KPI/statistic detection cannot guarantee finding every relevant value.

### Verification latency

Evidence verification may meaningfully increase answer response time.

### Model/provider variation

Changes to OCR, embeddings, LLMs, or verification models can change results across processing versions.

### Cost

OCR + retrieval + answer generation + verification may make each document/query more expensive than ordinary PDF-chat products.

### Prompt injection

Malicious or instruction-like document content must never override application rules or isolation boundaries.

---

## 15. Remaining Unresolved Decisions

No unresolved decision currently blocks progression to Stage 01.

Some values intentionally remain **provisional and evidence-driven**, including:

- exact performance SLAs;
- benchmark-derived accuracy thresholds;
- High/Medium/Low Evidence Support thresholds;
- exact provider choices;
- long-term pricing;
- hosting region;
- future large-document limits;
- post-MVP team/organization behavior.

These should not be prematurely finalized until measurement or later product stages justify them.

One important future distinction must be preserved:

> **Product requirements define desired behavior; later Technical Design determines how that behavior is implemented.**

---

## 16. Recommended Input for Stage 01 — Product/Feature Brief

The Product/Feature Brief should inherit these core principles:

### Product statement

PdfMining is an evidence-first AI document intelligence platform for professionals that transforms PDFs into searchable, structured, conversational knowledge while preserving exact traceability to the original document.

### Primary problem

Existing PDF-chat tools can answer questions but often provide weak provenance, opaque confidence, unreliable citation relationships, limited structured extraction, and insufficient handling of scanned/multilingual professional documents.

### Primary value proposition

Users can understand, extract, question, and verify information from PDFs without losing connection to the original evidence.

### Core product pillar

**Trust through verifiable evidence.**

### MVP focus

Prove that PdfMining can reliably:

1. process representative Arabic/English PDFs;
2. extract useful structured information;
3. answer questions using document evidence;
4. verify claim/evidence relationships;
5. navigate users to the exact original source;
6. communicate uncertainty and limitations instead of hiding them.

The Stage 01 Product/Feature Brief should remain product-focused and should **not prematurely decide architecture, database schemas, APIs, infrastructure topology, or implementation libraries**.
