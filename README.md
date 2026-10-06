# PdfMining

**AI-powered PDF intelligence with grounded answers, structured extraction, and traceable citations.**

PdfMining is a document intelligence platform designed to help users extract, understand, and verify information from complex PDF documents.

It combines PDF/OCR processing, structured statistics extraction, retrieval-augmented generation (RAG), evidence verification, and exact source highlighting to provide answers that remain traceable to the original document.

> The goal is not simply to “chat with a PDF,” but to make every important answer inspectable and verifiable against its source.

---

## Key Features

### PDF Intelligence

- Native/text-based PDF processing
- Scanned PDF processing through OCR
- Mixed native/scanned document support
- Arabic and English document support
- Preservation of page, text, layout, and source-coordinate information
- Long-document processing

### Structured Data Extraction

Extract structured information such as:

- statistics
- percentages
- counts
- monetary values
- ratios
- KPIs
- contextual sentences
- tables where supported

Extracted data remains linked to its original document location.

### Grounded Document Chat

Ask questions about uploaded documents in Arabic or English.

PdfMining is designed around evidence-grounded answers:

```text
Question
   ↓
Document Retrieval
   ↓
Evidence Selection / Verification
   ↓
LLM Answer
   ↓
Claim ↔ Citation
   ↓
Exact Source Location
```

When sufficient supporting evidence cannot be found, the system should communicate that instead of fabricating an answer.

### Traceable Citations

PdfMining preserves the relationship between generated answers and the original PDF:

```text
Answer Claim
    ↓
Citation
    ↓
Source Span(s)
    ↓
Bounding Box(es)
    ↓
Original PDF Page
```

Users can navigate from a citation directly to the supporting passage and see it highlighted inside the original PDF.

### Evidence Support

PdfMining distinguishes between:

- semantic retrieval relevance;
- evidence supporting a generated claim;
- factual certainty.

A citation-support indicator represents how strongly the cited evidence supports a claim.

It is **not** presented as a probability that an AI-generated answer is factually true.

### Arabic + English

Arabic is treated as a first-class requirement rather than an optional localization feature.

The platform is intended to support:

- Arabic documents
- English documents
- mixed Arabic/English documents
- Arabic questions
- English questions
- RTL content
- OCR-generated Arabic text

---

## PDF Handling Philosophy

PdfMining always preserves the **original uploaded PDF unchanged as the canonical source of truth**.

The application does not regenerate every uploaded PDF into a normalized replacement.

Instead, it creates a normalized internal representation containing information such as:

```text
Document
 └── Page
      ├── Block
      │    └── Span
      │         ├── Text
      │         ├── Bounding Box
      │         ├── Source Type
      │         └── Confidence
      ├── Table
      ├── Image / Figure
      └── Structural Metadata
```

### Native PDFs

Text and citation coordinates are mapped directly to the original PDF.

### Scanned PDFs

PdfMining uses OCR to obtain:

- text
- reading order
- bounding boxes
- OCR confidence where available

OCR bounding boxes become the canonical coordinates for citations and highlighting.

A searchable PDF with an invisible OCR text layer may be generated as a convenience artifact, but it never replaces the original document or becomes the citation authority.

---

## AI Responsibilities

PdfMining deliberately separates different AI responsibilities.

### LLM

Used primarily for tasks requiring natural-language generation or semantic synthesis:

- document Q&A
- summaries
- semantic interpretation
- structured descriptions
- multilingual answer generation

### Embedding Model

Used for:

- semantic document retrieval
- vector representations
- initial RAG candidate search

### Structured Verification / Decision Model

The architecture is being designed to support specialized structured decision models such as JEV for tasks including:

- reranking
- evidence selection
- claim-support verification
- grounded / unsupported classification
- evidence-support scoring

### OCR

OCR is treated as a separate document-understanding capability and may use local or external models depending on the final architecture.

---

## High-Level Processing Flow

```text
Original PDF
     │
     ▼
PDF Parsing / OCR
     │
     ▼
Normalized Document Representation
     │
     ├── Text / Structure
     ├── Tables
     ├── Coordinates
     └── Provenance
     │
     ▼
Retrieval Units / Chunks
     │
     ▼
Embeddings
     │
     ▼
Semantic Retrieval
     │
     ▼
Evidence Selection / Reranking
     │
     ▼
LLM Generation
     │
     ▼
Evidence Verification
     │
     ▼
Answer + Citations + Support Information
     │
     ▼
Original PDF Highlighting
```

---

## Planned MVP Experience

A typical user journey is expected to be:

1. Sign in.
2. Upload a PDF.
3. PdfMining processes the document.
4. Native text is extracted or OCR is performed when required.
5. Structured statistics and relevant document information become available.
6. The user explores or searches the extracted results.
7. The user asks questions about the document.
8. PdfMining returns evidence-grounded answers.
9. Citations are shown alongside relevant claims.
10. The user clicks a citation.
11. PdfMining navigates to the exact source passage in the original PDF.
12. The source is highlighted.
13. Structured results can be exported where supported.

---

## Planned Exports

The MVP is expected to support structured export to:

- CSV
- Excel

Exported statistics should preserve useful provenance such as page and source context where applicable.

---

## Architecture Status

PdfMining is currently in the **architecture decision stage**.

Product discovery and requirements definition have been completed before implementation begins.

```text
✅ Stage 00 — Product Discovery
✅ Stage 01 — Product / Feature Brief
✅ Stage 02 — Project / Product Scope
✅ Stage 03 — Product Requirements Document
✅ Stage 04 — Software Requirements Specification
🚧 Stage 05 — Wayfinder / Architecture Decisions
⬜ Stage 06 — Technical Design / Architecture Specification
⬜ Implementation
```

Major technology choices are intentionally being evaluated before being finalized.

Current preferences include:

- Vue / Nuxt for the frontend
- Node.js as the primary backend runtime
- Python only where its document/AI ecosystem provides a clear advantage
- PostgreSQL
- pgvector as the initial vector-storage candidate
- PDF.js or equivalent for document rendering
- Docker-based deployment
- Linux / Nginx
- provider-independent AI integrations where practical

These should not yet be interpreted as final architectural decisions.

---

## Design Principles

PdfMining follows several core principles:

1. **The original PDF is always the source of truth.**
2. **Extracted information must preserve source provenance.**
3. **AI answers should be grounded in document evidence.**
4. **Insufficient evidence is preferable to fabricated answers.**
5. **Retrieval similarity is not the same as evidence support.**
6. **Evidence support is not the same as factual certainty.**
7. **Arabic and English are first-class requirements.**
8. **Scanned documents should remain traceable through OCR coordinates.**
9. **AI providers should remain replaceable where practical.**
10. **MVP architecture should favor simplicity over unnecessary distributed-system complexity.**

---

## Project Goals

PdfMining is being developed both as a useful document-intelligence product and as a production-style demonstration of:

- RAG engineering
- document AI
- OCR
- multilingual AI
- embeddings and vector retrieval
- evidence verification
- citation provenance
- PDF coordinate mapping
- structured AI extraction
- full-stack AI system architecture

---

## Repository Structure

The repository is currently documentation-first while architecture decisions are being resolved.

```text
pdfmining/
├── AGENTS.md
├── docs/
│   ├── Stage 00 - ...
│   ├── Stage 01 - ...
│   ├── Stage 02 - ...
│   ├── Stage 03 - ...
│   ├── Stage 04 - ...
│   ├── agents/
│   └── ...
└── README.md
```

Application structure will be introduced after the architecture stage is approved.

---

## Development Status

**Status:** Planning / Architecture

Production implementation has intentionally not started yet.

The current focus is resolving architectural decisions through research, prototypes, benchmarks, and explicit decision records before creating the final technical design.

---

## License

License information will be added before public distribution.