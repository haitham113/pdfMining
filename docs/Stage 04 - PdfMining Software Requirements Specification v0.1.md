# PdfMining — Software Requirements Specification (SRS)

## 1. Document Control

| Field | Value |
|---|---|
| Product | PdfMining |
| Document | Software Requirements Specification |
| Version | v0.1 |
| Status | Draft for approval |
| Primary Source | Stage 03 — PdfMining Product Requirements Document v0.1 |
| Supporting Sources | Stages 00–02 where additional approved context is required |
| Scope Baseline | Approved PdfMining MVP |
| Next Stage After Approval | Stage 05 — Wayfinder / Architecture Decisions |

This SRS translates the approved PRD into implementation-neutral, testable system requirements. The PRD remains the authoritative behavioral specification. Later approved decisions override earlier provisional ones.

### 1.1 Normative Language and Requirement IDs

- **shall** — mandatory MVP requirement.
- **should** — expected/recommended requirement whose final acceptance may depend on validation, consistent with PRD priority.
- **may** — explicitly optional capability.
- Requirement IDs are stable within this document. PRD-derived requirements preserve one-to-one traceability wherever practical; additional cross-cutting SRS requirements use separate ranges.

## 2. Purpose

This SRS defines what the PdfMining software system must satisfy technically so that implementation, architecture decisions, test planning, and acceptance can preserve the approved product behavior. It specifies functional behavior, logical interfaces, data/provenance obligations, security and privacy boundaries, reliability and recovery, performance expectations, observability, localization, AI behavior, and verification needs.

This SRS intentionally does **not** select final service boundaries, application architecture style, backend/frontend frameworks, database schema, API URLs, queue technology, object storage vendor, OCR engine, embedding model, LLM/provider, vector engine, RAG framework, chunking algorithm, verification/JEV implementation, deployment topology, or repository structure. Those are Stage 05/06 decisions.

## 3. Scope Summary

PdfMining is an evidence-first browser application for authenticated individual professionals working with information-heavy PDFs. The system accepts supported PDFs within configured limits, preserves the original PDF unchanged as the canonical evidence source, processes native/scanned/mixed content in Arabic and English, creates a normalized source-linked representation, extracts useful statistics and reliable tables, supports single-document grounded Q&A, evaluates claim/evidence support, navigates citations to the original PDF, exports structured statistics, retains private document history, and deletes document-specific data on confirmed deletion.

The MVP is intentionally bounded: no non-PDF ingestion, multi-document research, team collaboration, general chart-number reasoning, handwriting understanding, external web evidence, billing, public API, native apps, selectable hosting regions, or unsupported compliance claims.

## 4. Definitions and Terminology

| Term | Definition |
|---|---|
| Original PDF | The exact PDF file uploaded by the user, preserved unchanged. |
| Canonical document | The original uploaded PDF that remains the authoritative visual and citation source. |
| Native PDF | A PDF containing a usable text layer that can be extracted without OCR for the relevant content. |
| Scanned PDF | A PDF whose relevant page content is image-based and requires OCR to obtain machine-readable text. |
| Mixed PDF | A PDF containing a combination of usable native text and scanned/image-based content. |
| OCR | Optical character recognition used to obtain text and source locations from image-based document content. |
| Page | An ordered page of the canonical PDF. |
| Block | A logical extracted region containing text or document structure. |
| Span | A finer-grained text/source unit within a block, potentially carrying coordinates and provenance. |
| Bounding box / source region | A page-relative geometric region identifying the location of source content. |
| Normalized document representation | Internal implementation-neutral structure that preserves document content, structure, provenance, and source mapping without replacing the original PDF. |
| Chunk / retrieval unit | A source-linked unit prepared for semantic retrieval. |
| Embedding | A semantic vector representation associated with a retrieval unit. |
| Retrieval | Selection of document-scoped content relevant to a user question or analysis task. |
| RAG | Retrieval-grounded generation in which document evidence is retrieved and supplied to generation. |
| Citation | A claim-to-source reference containing page/source provenance and a recognizable source preview. |
| Evidence | Document source content used to support a claim or structured result. |
| Evidence Support | A categorical assessment of how strongly selected evidence supports a specific claim; it is not factual-truth probability. |
| Grounded answer | An answer whose document-derived factual claims are supported by evidence from the current uploaded document. |
| Insufficient Evidence | An explicit outcome indicating that the current document does not establish the requested factual answer or source quality is insufficient. |
| Searchable OCR derivative | Optional convenience PDF preserving page images with an OCR text layer; never canonical. |
| Statistic / KPI | A useful structured quantitative fact with context and provenance. |
| Processing warning | A retained indication that a capability or source region has a known limitation. |
| Partial processing | A usable document state in which one or more capabilities are incomplete, degraded, or failed while valid results remain available. |

## 5. System Context

```text
End User
   ↕
Browser / Web Client
   ↕
PdfMining logical application boundary
   ├─ authentication / authorization
   ├─ document ingestion and processing orchestration
   ├─ normalized document and provenance management
   ├─ statistics / table analysis
   ├─ retrieval-grounded chat and evidence verification
   ├─ citation / source-navigation services
   └─ export / history / deletion
      ↕        ↕        ↕        ↕
 Persistent   OCR      AI /      Vector
 storage    capability verification retrieval
```

The diagram is logical only. It does not imply service boundaries or deployment topology.

### 5.1 General System Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-SYS-001 | The system shall restrict the MVP evidence domain for document analysis and chat to one uploaded document at a time. | PRD-CHAT-001, PRD-GROUND-005 |
| SRS-SYS-002 | The system shall treat all uploaded document content, including prompt-like instructions, as untrusted data rather than executable system instructions. | PRD-GROUND-007, PRD-SEC-006 |
| SRS-SYS-003 | The system shall preserve successful capability outputs when an independent non-critical capability fails, provided those outputs remain valid and safely usable. | PRD-PROC-003, PRD-ERR-003, PRD-ERR-004, PRD-ERR-005 |
| SRS-SYS-004 | The system shall expose a user-visible distinction between operational failure, partial processing, and insufficient evidence. | PRD-PROC-004, PRD-PROC-005, PRD-ERR-006, PRD-GROUND-001 |
| SRS-SYS-005 | The system shall not introduce product behavior that requires multi-document analysis, organization collaboration, external web search, billing, a public API, or non-PDF ingestion in the MVP. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-SYS-006 | The system shall support the approved workflow through a browser-based desktop experience and a mobile-responsive web experience without requiring a native application. | PRD-UX-001 |

## 6. Actors and External Systems

| Actor / External System | Purpose | Information Exchanged | Trust Boundary |
|---|---|---|---|
| Authenticated end user | Uploads, inspects, queries, exports, revisits, and deletes owned documents. | Credentials/session, PDFs, passwords for protected PDFs, questions, user actions, exports. | Trusted identity after authentication; user-supplied files/questions remain untrusted input. |
| Browser/client application | Presents the web UI and original PDF viewer. | UI state, document metadata, rendered PDF, analysis results, chat, citations, warnings. | Client is outside server trust boundary; authorization cannot rely only on client state. |
| Original PDF file | Canonical evidence artifact. | Binary PDF content and metadata required for validation/rendering. | Untrusted uploaded content. |
| Persistent structured-data storage | Retains ownership, states, normalized data, provenance, results, conversations, and processing metadata. | Structured application data. | Protected infrastructure dependency. |
| Persistent file/object storage | Retains canonical PDFs and approved derivatives. | Original/derived binary artifacts. | Protected infrastructure dependency. |
| OCR capability | Recognizes scanned/image text and regions. | Page/region images; OCR text, coordinates, confidence. | May be external; content minimization/privacy controls apply. |
| AI generation capability | Produces overview and grounded answer text from supplied context. | Document evidence/context and generation result. | Potential external-provider boundary; must not redefine evidence policy. |
| Embedding capability | Generates semantic representations. | Source-linked retrieval text; vectors. | Potential external-provider boundary. |
| Vector retrieval capability | Retrieves relevant document-scoped units. | Embeddings/queries, candidate units, relevance metadata. | Must preserve user/document isolation. |
| Evidence-verification capability | Assesses claim/evidence support. | Claim and evidence set; structured support outcome. | Potential external-provider boundary; result semantics fixed by product requirements. |
| Spreadsheet export capability | Produces CSV/Excel files. | Structured statistics and provenance metadata. | Generated files contain untrusted source-derived text. |

## 7. Functional Requirements

### 7.1 Authentication and Access Control

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-AUTH-001 | The system shall require an authenticated individual account before a user can access private documents or document-derived data. | Must | 1. An unauthenticated visitor cannot open a user's document workspace or history.<br>2. After successful authentication, the user can access only content owned by that account. | PRD-AUTH-001 |
| SRS-AUTH-002 | The system shall allow a new individual user to create an account and then sign in to PdfMining. | Must | 1. A user can complete account creation using the product's supported account fields.<br>2. After account creation, the user can enter the authenticated product experience.<br>3. Invalid or incomplete registration input produces a clear corrective message without creating a usable account. | PRD-AUTH-002 |
| SRS-AUTH-003 | The system shall allow an existing user to sign in and sign out. | Must | 1. Valid credentials grant access to the user's private history.<br>2. Invalid credentials produce a clear authentication error without revealing protected content.<br>3. After logout, protected pages require authentication again. | PRD-AUTH-003 |
| SRS-AUTH-004 | When an authenticated session is no longer valid, the product shall require re-authentication and must not expose protected document content. | Must | 1. A protected action with an invalid session redirects or otherwise returns the user to an authentication flow.<br>2. Unsaved user input should be preserved where practical, but protected data is not shown until authentication succeeds. | PRD-AUTH-004 |
| SRS-AUTH-005 | The system shall enforce strict per-user access isolation for documents, history, conversations, statistics, citations, and other document-derived artifacts. | Must | 1. A user cannot access another user's document by navigation, identifier manipulation, history view, export, or citation link.<br>2. Access-denied attempts do not reveal the protected document's content or metadata. | PRD-AUTH-005 |

Additional system requirements:

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-AUTH-101 | The system shall perform authorization checks on every server-side operation that reads, modifies, exports, renders, retrieves, or deletes document-associated data. | PRD-AUTH-005, PRD-SEC-001 |
| SRS-AUTH-102 | The system shall bind each protected document and document-derived artifact to an owning user identity and shall use that ownership relationship for access-control decisions. | PRD-AUTH-005, PRD-SEC-001 |
| SRS-AUTH-103 | The system shall return an authorization-safe response for denied resource access without disclosing whether a protected resource exists for another user. | PRD-AUTH-005, PRD-SEC-001 |

### 7.2 Document Upload

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-UPLOAD-001 | The upload interface shall accept PDF files only. | Must | 1. A valid supported PDF can be selected for upload.<br>2. A non-PDF file is rejected before processing with a message that PDF is the supported format. | PRD-DOC-001 |
| SRS-UPLOAD-002 | The system shall validate the configured page limit and reject documents that exceed it; the initial MVP maximum is 20 pages. | Must | 1. A PDF of 20 pages or fewer passes the page-count boundary when other validations pass.<br>2. A PDF above the configured maximum is not processed and the user sees the current maximum. | PRD-DOC-002 |
| SRS-UPLOAD-003 | The system shall validate the configured file-size limit; the initial MVP target is approximately 25 MB and remains configuration-controlled. | Must | 1. A file over the active configured size is rejected before expensive processing.<br>2. The error communicates the active maximum allowed size rather than implying a universal 25 MB guarantee. | PRD-DOC-003 |
| SRS-UPLOAD-004 | For a password-protected PDF, the product shall allow the user to supply a password and process the document only when the password is valid. | Must | 1. A protected PDF prompts for a password rather than being silently rejected.<br>2. A valid password allows processing to continue.<br>3. An invalid or missing password produces a clear error and does not bypass protection. | PRD-DOC-004 |
| SRS-UPLOAD-005 | The user shall receive visible upload progress or an equivalent upload-in-progress state until the file is accepted or fails. | Must | 1. During upload, the UI visibly indicates that transfer is in progress.<br>2. Upload success transitions to a processing state; upload failure transitions to a retryable error state where appropriate. | PRD-DOC-005 |
| SRS-UPLOAD-006 | Uploading a PDF that is identical to a previously uploaded document shall not silently overwrite or alter the earlier document. | Must | 1. A duplicate upload either creates a separate document record or is explicitly identified before reuse.<br>2. The previous document and its analysis remain unchanged unless the user deletes it. | PRD-DOC-006 |
| SRS-UPLOAD-007 | The system shall reject empty, unreadable, corrupted, or otherwise unprocessable PDF inputs with a user-visible reason when identifiable. | Must | 1. A zero-page/empty PDF does not proceed to Ready.<br>2. A corrupted PDF that cannot be parsed ends in a visible failure state with retry/re-upload guidance. | PRD-DOC-007 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-UPLOAD-101 | The system shall validate that an uploaded object is a parseable PDF and shall not rely solely on filename extension for format validation. | PRD-DOC-001, PRD-DOC-007 |
| SRS-UPLOAD-102 | The system shall complete configured format, file-size, page-count, and protection checks before initiating avoidable expensive downstream analysis. | PRD-DOC-002, PRD-DOC-003, PRD-DOC-004 |
| SRS-UPLOAD-103 | The system shall persist the outcome of an accepted upload sufficiently to recover its document identity and processing status after a page refresh or application restart. | PRD-DOC-005, PRD-PROC-001, PRD-HIST-002 |
| SRS-UPLOAD-104 | The system shall treat user-supplied PDF passwords as secrets and shall not persist them beyond the duration required to open/process the protected document unless a later approved design explicitly requires protected storage. | PRD-DOC-004, PRD-SEC-004, PRD-SEC-008 |
| SRS-UPLOAD-105 | The system shall assign separate document identity to a duplicate upload unless the user is explicitly informed of and chooses an approved reuse behavior. | PRD-DOC-006 |

### 7.3 Original Document Preservation

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-DOC-101 | The system shall preserve the exact uploaded PDF bytes as the canonical document artifact for the lifetime of the retained document. | PRD-NATIVE-003, PRD-VIEW-001 |
| SRS-DOC-102 | The system shall distinguish the original PDF from all derived artifacts in persisted metadata and processing behavior. | PRD-NATIVE-003, PRD-OCR-008 |
| SRS-DOC-103 | The system shall resolve canonical citations and visual evidence inspection against the original PDF even when extraction, OCR, or searchable derivatives are used. | PRD-CITE-005, PRD-OCR-008, PRD-VIEW-001 |
| SRS-DOC-104 | The system shall not overwrite or silently substitute the original PDF with a normalized, rendered, OCR-searchable, or regenerated derivative. | PRD-NATIVE-003, PRD-OCR-008, PRD-VIEW-001 |

### 7.4 Document Processing Lifecycle

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-PROC-001 | Each uploaded document shall expose a user-visible processing state that reflects its current progress. | Must | 1. The user can distinguish at least Uploaded/Queued, Extracting, OCR when applicable, Analyzing, Ready, Ready with warnings or partial results, and Failed.<br>2. The displayed state updates as the document advances or fails. | PRD-PROC-001 |
| SRS-PROC-002 | OCR processing shall be shown as a distinct state or progress phase when OCR is required. | Must | 1. A scanned page that requires OCR causes the user to see an OCR-related processing indication.<br>2. A purely native PDF is not falsely described as undergoing OCR. | PRD-PROC-002 |
| SRS-PROC-003 | The system shall preserve usable successful results when a non-critical processing capability fails. | Must | 1. If one non-critical capability fails, completed capabilities remain accessible.<br>2. The overall document is not labeled fully successful when a known non-critical failure affects output. | PRD-PROC-003 |
| SRS-PROC-004 | A document with usable results but known extraction, OCR, table, or analysis limitations shall be shown as Ready with warnings or an equivalent partial-success state. | Must | 1. Known limitations are visible from the document workspace.<br>2. Warnings identify the affected capability or region at a useful level without claiming unavailable precision. | PRD-PROC-004 |
| SRS-PROC-005 | A document that cannot produce a usable minimum result shall end in a Failed state with a clear user-visible explanation and available recovery action. | Must | 1. Failed documents do not expose fabricated analysis as valid results.<br>2. The user is told whether retry, password correction, or re-upload may resolve the issue. | PRD-PROC-005 |
| SRS-PROC-006 | After sufficient processing, PdfMining shall provide a concise automatic document overview. | Must | 1. A Ready document presents a concise overview derived from the document.<br>2. The overview remains document-grounded and does not silently add external facts.<br>3. If evidence quality is insufficient for a reliable overview, the product communicates the limitation instead of inventing content. | PRD-PROC-006 |
| SRS-PROC-007 | Processing warnings and failures shall remain inspectable after processing completes. | Must | 1. Reopening a document preserves its relevant warning/partial-processing indicators.<br>2. A warning is not cleared merely because the user navigates away and returns. | PRD-PROC-007 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-PROC-101 | The system shall persist the current document processing state and enough prior state information to prevent a retained document from presenting an impossible or stale user-visible state after restart. | PRD-PROC-001, PRD-PROC-007 |
| SRS-PROC-102 | The system shall permit only state transitions consistent with the approved lifecycle: Uploaded, Queued/waiting, Extracting, conditional OCR, Analyzing, Ready, Ready with Warnings/Partially Processed, Failed, retry processing where offered, and Deleted. | PRD-PROC-001 |
| SRS-PROC-103 | The system shall make retryable processing operations safe against duplicate user-visible results when the same document/capability is retried. | PRD-PROC-003, PRD-ERR-003, PRD-ERR-005 |
| SRS-PROC-104 | The system shall preserve valid completed intermediate results across a retry or recoverable downstream failure when those results remain compatible with the retry. | PRD-PROC-003, PRD-ERR-005 |
| SRS-PROC-105 | The system shall associate each processing warning or failure with the affected document and capability and shall retain that association while the document remains retained. | PRD-PROC-004, PRD-PROC-007, PRD-ERR-007 |

### 7.5 Native PDF Extraction

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-PARSE-001 | For native/text PDFs, PdfMining shall extract usable text and document structure while preserving page association. | Must | 1. Extracted text used in analysis can be associated with its original page.<br>2. Reading order and structure are retained sufficiently for approved statistics, chat, and citation behavior on representative native PDFs. | PRD-NATIVE-001 |
| SRS-PARSE-002 | Native extracted content shall retain source-coordinate relationships where reliable so citations can navigate to and highlight the original PDF. | Must | 1. Eligible native-text citations resolve to the correct page.<br>2. When reliable coordinates exist, the cited source region can be highlighted in the original PDF. | PRD-NATIVE-002 |
| SRS-PARSE-003 | The original uploaded PDF shall remain unchanged and canonical regardless of native extraction or normalized internal processing. | Must | 1. Opening the viewer shows the original uploaded PDF.<br>2. No generated or normalized derivative replaces the original as the citation authority. | PRD-NATIVE-003 |
| SRS-PARSE-004 | When unusual fonts, encodings, broken text layers, or complex layouts reduce native extraction quality, the product shall expose the resulting limitation where it affects user-visible outputs. | Must | 1. Known degraded extraction is reflected by a warning or reduced downstream support.<br>2. The product does not claim complete extraction when the native text layer is demonstrably unusable. | PRD-NATIVE-004 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-PARSE-101 | The system shall represent extracted native text with page identity and source regions at a granularity sufficient to support statement-level citation mapping where the source permits it. | PRD-NATIVE-001, PRD-NATIVE-002, PRD-CITE-001 |
| SRS-PARSE-102 | The system shall retain native extraction provenance so downstream artifacts can distinguish native text from OCR-derived text. | PRD-NATIVE-001, PRD-OCR-004 |
| SRS-PARSE-103 | The system shall preserve reading-order information or an equivalent order relation needed by downstream statistics, retrieval, and citation behavior on representative native PDFs. | PRD-NATIVE-001 |

### 7.6 Scanned PDF / OCR Processing

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-OCR-001 | The system shall detect pages or regions that require OCR and apply OCR selectively rather than treating every document as fully scanned. | Must | 1. Scanned pages receive OCR processing.<br>2. Native pages with usable text are processed without unnecessary whole-page OCR as the product behavior. | PRD-OCR-001 |
| SRS-OCR-002 | OCR shall support representative Arabic, English, and mixed Arabic/English scanned content within the MVP document boundary. | Must | 1. Representative Arabic and English scans can yield usable OCR text.<br>2. Mixed-language pages can be processed without being rejected solely for containing both supported languages. | PRD-OCR-002 |
| SRS-OCR-003 | OCR output used by the product shall retain page association, source coordinates, reading order, and OCR confidence where available. | Must | 1. OCR-derived citations can identify their source page.<br>2. Where coordinates are reliable, OCR-derived evidence can be highlighted.<br>3. Where OCR confidence is available, poor quality can influence user-visible warnings/support rather than being hidden. | PRD-OCR-003 |
| SRS-OCR-004 | Mixed native/scanned PDFs shall combine native extraction on usable native pages with OCR on scanned pages or required regions. | Must | 1. A mixed document can reach a usable Ready or partial-success state.<br>2. Evidence from both native and OCR-derived pages remains traceable to the same original PDF. | PRD-OCR-004 |
| SRS-OCR-005 | Poor OCR quality shall be disclosed and must reduce downstream confidence/support where it materially affects interpretation. | Must | 1. Low-quality OCR triggers a visible warning when it affects analysis.<br>2. The product does not present low-quality OCR-derived claims with unjustifiably strong wording or false location precision. | PRD-OCR-005 |
| SRS-OCR-006 | Partially successful OCR shall remain usable for regions/pages that were read reliably, while failed regions are identified as limited or unavailable. | Must | 1. Successful OCR content remains available after another page/region fails.<br>2. The product does not invent text for an unreadable region. | PRD-OCR-006 |
| SRS-OCR-007 | Common page rotations shall be handled so rotated scanned/native pages are usable where otherwise processable. | Must | 1. Representative commonly rotated pages can be processed without requiring the user to modify the source PDF.<br>2. If rotation or image quality still prevents reliable OCR, the limitation is disclosed. | PRD-OCR-007 |
| SRS-OCR-008 | A searchable OCR PDF derivative may be created as a convenience artifact, but it shall never replace the original PDF or become the citation authority. | Must | 1. Whether or not a searchable derivative exists, citations resolve against the original uploaded PDF.<br>2. Deleting the document also removes any document-specific searchable derivative. | PRD-OCR-008 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-OCR-101 | The system shall record, for OCR-derived content used downstream, the original page, OCR source region, recognized text, and provenance; OCR confidence shall also be retained when supplied by the OCR capability. | PRD-OCR-003 |
| SRS-OCR-102 | The system shall allow OCR to be invoked at page or region granularity so mixed documents can preserve usable native extraction where appropriate. | PRD-OCR-001, PRD-OCR-004 |
| SRS-OCR-103 | The system shall propagate materially poor OCR quality into warnings, support evaluation, or claim withholding rather than discarding the quality signal before downstream analysis. | PRD-OCR-005 |
| SRS-OCR-104 | The system shall keep successful OCR results from unaffected pages or regions when OCR fails elsewhere in the same document. | PRD-OCR-006, PRD-ERR-003 |

### 7.7 Normalized Document Representation

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-NORM-001 | The system shall maintain a normalized internal representation of each processable document without changing the canonical original PDF. | PRD-NATIVE-003, PRD-OCR-008 |
| SRS-NORM-002 | The normalized representation shall identify the document and its ordered pages. | PRD-NATIVE-001, PRD-OCR-003 |
| SRS-NORM-003 | The normalized representation shall be capable of representing text blocks and finer-grained spans with text content, page association, and reading order where available. | PRD-NATIVE-001, PRD-OCR-003 |
| SRS-NORM-004 | The normalized representation shall be capable of storing bounding regions or equivalent source coordinates for native and OCR-derived content when available. | PRD-NATIVE-002, PRD-OCR-003 |
| SRS-NORM-005 | The normalized representation shall identify whether extracted content originated from native parsing, OCR, or another approved extraction path. | PRD-OCR-004 |
| SRS-NORM-006 | The normalized representation shall be capable of representing extracted tables, figures/images, and structural metadata without requiring successful semantic interpretation of every visual. | PRD-TABLE-001, PRD-VIS-001 |
| SRS-NORM-007 | The normalized representation shall retain extraction or OCR confidence metadata when available and relevant to downstream quality decisions. | PRD-OCR-003, PRD-OCR-005 |
| SRS-NORM-008 | Every derived retrieval unit, statistic, citation, and evidence item shall be traceable through normalized source references to one or more original PDF pages/regions. | PRD-STAT-002, PRD-CITE-005 |
| SRS-NORM-009 | Source references used by retained derived artifacts shall remain stable for the lifetime of the retained document unless the artifact is explicitly reprocessed and versioned/replaced consistently. | PRD-HIST-003, PRD-PROC-007 |
| SRS-NORM-010 | The normalized representation shall support multiple source regions for one logical evidence item when evidence spans lines or non-contiguous regions. | PRD-HL-003, PRD-HL-004, PRD-CITE-003 |

### 7.8 Chunking and Retrieval Preparation

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-RAG-101 | The system shall transform eligible normalized content into retrievable units without losing document, page, and source-region provenance. | PRD-CHAT-004, PRD-CITE-005 |
| SRS-RAG-102 | Each retrieval unit shall retain sufficient source references to reconstruct citation evidence from the original PDF. | PRD-CITE-001, PRD-CITE-005 |
| SRS-RAG-103 | The system shall support reprocessing retrieval units when the configured chunking or retrieval-preparation strategy changes without altering the canonical original PDF. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-RAG-104 | Retrieval preparation shall preserve Arabic, English, and mixed-language text in a Unicode-safe representation. | PRD-LANG-001, PRD-LANG-002 |
| SRS-RAG-105 | Retrieval preparation shall not merge content from different users or different documents into a source unit that cannot be uniquely scoped back to its owner and document. | PRD-AUTH-005, PRD-CHAT-001 |
| SRS-RAG-106 | Transformations used for retrieval preparation shall preserve enough ordering and source mapping to support evidence reconstruction after retrieval. | PRD-CITE-002, PRD-HL-001 |

### 7.9 Embedding Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-EMB-001 | The system shall be capable of generating semantic vector representations for eligible retrieval units. | PRD-CHAT-004 |
| SRS-EMB-002 | Each persisted vector representation shall be associated with its retrieval unit, document identity, and owning user. | PRD-AUTH-005, PRD-CHAT-001 |
| SRS-EMB-003 | The embedding capability shall support the approved Arabic, English, and mixed-language retrieval scenarios to a quality level validated by the evaluation corpus. | PRD-LANG-001, PRD-LANG-002 |
| SRS-EMB-004 | The system shall support regeneration/replacement of embeddings when the configured embedding model or representation changes, without requiring replacement of the original PDF. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-EMB-005 | Embedding storage and retrieval shall enforce document and user isolation equivalent to other document-derived artifacts. | PRD-AUTH-005, PRD-SEC-001 |

### 7.10 Retrieval Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-RAG-111 | For a document question, the system shall retrieve candidate evidence only from the current document and owning user scope. | PRD-CHAT-001, PRD-CHAT-004 |
| SRS-RAG-112 | The retrieval capability shall return source provenance with each candidate result so later stages can construct citations. | PRD-CITE-001, PRD-CITE-005 |
| SRS-RAG-113 | The system shall support semantic retrieval over representative Arabic, English, and mixed-language document content. | PRD-LANG-001, PRD-LANG-002 |
| SRS-RAG-114 | When retrieval produces no evidence sufficient for the requested factual answer, the downstream answer path shall be able to return Insufficient Evidence rather than forcing generation. | PRD-GROUND-001, PRD-EVID-005 |
| SRS-RAG-115 | The retrieval interface shall preserve multiple potentially conflicting passages when they are relevant so conflict-handling logic can surface them rather than silently discard one side. | PRD-GROUND-003 |
| SRS-RAG-116 | The retrieval design shall permit later reranking or verification of candidates without changing the user-visible evidence contract. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-RAG-117 | Retrieval relevance signals shall not be presented to users as Evidence Support or factual-truth probability. | PRD-EVID-002, PRD-EVID-003 |

### 7.11 Statistics / KPI Extraction

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-STAT-001 | The system shall automatically surface useful quantitative facts and KPIs that have sufficient semantic context and document provenance. | Must | 1. Representative documents produce structured metrics when clear quantitative facts exist.<br>2. The product does not imply that every numeric value in the document has been discovered. | PRD-STAT-001 |
| SRS-STAT-002 | Each surfaced statistic shall include a metric or contextual label, value, unit when applicable, context, source page, and evidence/provenance link. | Must | 1. A user can identify what the value represents and where it came from.<br>2. A metric without a natural unit may omit the unit rather than invent one. | PRD-STAT-002 |
| SRS-STAT-003 | The system shall visibly distinguish directly extracted metrics from derived metrics. | Must | 1. Every displayed derived metric is labeled as derived.<br>2. Directly extracted values are not mislabeled as calculated. | PRD-STAT-003 |
| SRS-STAT-004 | The system shall show a derived metric only when its calculation is justified by document evidence and its source inputs remain traceable. | Must | 1. A derived metric provides access to the evidence supporting its inputs.<br>2. If required inputs are missing or ambiguous, the product withholds the derivation or marks it unavailable rather than guessing. | PRD-STAT-004 |
| SRS-STAT-005 | Repeated or duplicate metrics shall be handled without forcing unsafe deduplication when context differs. | Must | 1. Clearly repeated identical evidence is not needlessly multiplied where practical.<br>2. Values that appear similar but have different periods, populations, sections, or contexts remain distinguishable. | PRD-STAT-005 |
| SRS-STAT-006 | When conflicting values for the same apparent metric are surfaced within one document, the product shall preserve and expose the conflict rather than silently choose one. | Must | 1. Conflicting values can both be inspected with their separate provenance.<br>2. The UI does not imply a single authoritative value unless the document itself establishes one. | PRD-STAT-006 |
| SRS-STAT-007 | Ambiguous semantic classification shall remain visible instead of being presented as a certain normalized metric name. | Must | 1. An uncertain inferred label is qualified or falls back to source wording.<br>2. The source context remains available for user verification. | PRD-STAT-007 |
| SRS-STAT-008 | Statistics extraction shall support partial results and must not block the entire document when some metrics cannot be confidently structured. | Must | 1. Reliable extracted statistics remain usable even when other candidate metrics are omitted.<br>2. The product can show that extraction is partial or best-effort where relevant. | PRD-STAT-008 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-STAT-101 | Each persisted structured statistic shall retain a metric/source label, value, unit when applicable, context, page/source reference, extracted-versus-derived classification, and uncertainty/support metadata when available. | PRD-STAT-002, PRD-STAT-003 |
| SRS-STAT-102 | A derived statistic shall retain references to the source inputs and the derivation relationship necessary to explain why it was calculated. | PRD-STAT-004 |
| SRS-STAT-103 | The statistics pipeline shall preserve separate records when values differ by period, population, section, or other material context and shall not require unsafe normalization into one value. | PRD-STAT-005, PRD-STAT-006 |
| SRS-STAT-104 | The absence of a structured statistic shall not be interpreted by the system as proof that the original document contains no corresponding number or fact. | PRD-STAT-001, PRD-STAT-008 |

### 7.12 Table Extraction

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-TABLE-001 | The system shall reconstruct and display structured table content only when the reconstruction is sufficiently reliable. | Must | 1. Representative clear native tables can be displayed as structured content.<br>2. A table that cannot be reconstructed reliably is withheld or clearly marked partial. | PRD-TABLE-001 |
| SRS-TABLE-002 | Structured tables shall retain source page/provenance links back to the original PDF. | Must | 1. A displayed reconstructed table identifies its originating page or pages.<br>2. A user can navigate from a table or table-derived statistic to the relevant source evidence where mapping is available. | PRD-TABLE-002 |
| SRS-TABLE-003 | Scanned, image-based, merged-cell, nested, multi-page, and highly visual tables shall be treated as best-effort and may be withheld or simplified when relationships are ambiguous. | Must | 1. The product does not present an ambiguous table reconstruction as fully reliable.<br>2. A warning or omission communicates when structured output is limited. | PRD-TABLE-003 |
| SRS-TABLE-004 | Statistics extracted from reliable table content shall follow the same provenance and extracted-versus-derived rules as other statistics. | Must | 1. A table-origin statistic identifies its source evidence.<br>2. A calculation based on table values is labeled derived. | PRD-TABLE-004 |
| SRS-TABLE-005 | Failure to reconstruct a table shall not prevent the original table from remaining viewable in the canonical PDF. | Must | 1. The PDF viewer continues to show the original table.<br>2. No replacement structured table is treated as superior evidence to the original PDF. | PRD-TABLE-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-TABLE-101 | A structured table result shall retain its source page or pages and enough source-region provenance to support navigation to the original PDF. | PRD-TABLE-002 |
| SRS-TABLE-102 | The system shall represent table reconstruction quality or partiality sufficiently to withhold or qualify ambiguous structures rather than presenting them as reliable. | PRD-TABLE-001, PRD-TABLE-003 |
| SRS-TABLE-103 | When table-cell or row-level provenance is available and used for a statistic/citation, the system shall retain that association through the derived result. | PRD-TABLE-004, PRD-CITE-005 |

### 7.13 Chart and Visual Content

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-VIS-001 | Charts, graphs, images, and diagrams shall remain visible as part of the original PDF even when PdfMining does not semantically interpret them. | Must | 1. The viewer displays the original page containing the visual content.<br>2. Lack of visual interpretation does not remove or alter the source PDF. | PRD-VIS-001 |
| SRS-VIS-002 | The system shall not claim to extract or reason about numerical values encoded only in charts or graphs as an MVP capability. | Must | 1. A question that depends solely on an unextracted chart value produces an insufficient-evidence/unsupported-capability response.<br>2. The product does not present a chart region itself as verified numerical evidence. | PRD-VIS-002 |
| SRS-VIS-003 | Ordinary nearby native/OCR text such as captions may be used when it is reliably extracted, but the product shall distinguish textual evidence from unsupported visual interpretation. | Must | 1. A caption citation resolves to its textual source region when coordinates are reliable.<br>2. The presence of caption text does not cause the product to claim values that appear only graphically. | PRD-VIS-003 |

### 7.14 Chat and Conversation

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-CHAT-001 | The system shall allow an authenticated user to start and continue a conversation about one uploaded document at a time. | Must | 1. Questions in a document workspace use only that document as the evidence source.<br>2. The product does not offer multi-document selection for a single conversation. | PRD-CHAT-001 |
| SRS-CHAT-002 | The chat shall accept natural-language questions in Arabic and English, including understandable mixed-language questions. | Must | 1. Representative Arabic and English questions can be submitted.<br>2. A mixed Arabic/English question is not rejected solely because it mixes the two supported languages. | PRD-CHAT-002 |
| SRS-CHAT-003 | The system shall support contextual follow-up questions that use the conversation history to interpret user intent. | Must | 1. A follow-up such as 'What about the previous year?' can resolve prior conversational context when the referenced subject is clear.<br>2. Conversation history helps resolve intent but is not presented as document evidence. | PRD-CHAT-003 |
| SRS-CHAT-004 | Answers to document questions shall be grounded in evidence from the current uploaded document. | Must | 1. Document-derived factual claims are supported by document evidence where appropriate.<br>2. External general knowledge is not presented as evidence for a document claim. | PRD-CHAT-004 |
| SRS-CHAT-005 | The system shall support answers that combine evidence from multiple locations or pages in the same document when necessary. | Must | 1. A multi-source answer can cite more than one supporting passage.<br>2. Each cited passage remains individually navigable. | PRD-CHAT-005 |
| SRS-CHAT-006 | Document-associated conversation history shall persist until the document is deleted. | Must | 1. Reopening the document restores prior conversation history.<br>2. Deleting the document removes its conversation history from user access. | PRD-CHAT-006 |
| SRS-CHAT-007 | If answer generation fails for a transient reason, the user shall see a failure state and an available retry path without losing prior successful conversation history. | Must | 1. A failed answer is not displayed as a successful answer.<br>2. The user can retry the question or submit it again.<br>3. Earlier successful messages remain available. | PRD-CHAT-007 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-CHAT-101 | The system shall associate each conversation and message with one owning user and one document. | PRD-CHAT-001, PRD-CHAT-006 |
| SRS-CHAT-102 | Conversation history may be used to resolve conversational intent but shall not be treated as documentary evidence supporting a factual claim. | PRD-CHAT-003, PRD-CHAT-004 |
| SRS-CHAT-103 | The system shall persist successful messages and their answer/evidence associations for retained documents until document deletion. | PRD-CHAT-006, PRD-RET-001, PRD-RET-002 |
| SRS-CHAT-104 | A failed answer attempt shall have a distinguishable failed state and shall not overwrite a prior successful answer or conversation history. | PRD-CHAT-007, PRD-ERR-005 |

### 7.15 RAG / Grounded Answer Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-RAG-001 | When the document contains no relevant evidence for a requested factual answer, PdfMining shall explicitly state that the document does not establish the answer. | Must | 1. No unsupported factual answer is presented as if sourced from the document.<br>2. The response distinguishes 'not established by this document' from a processing error. | PRD-GROUND-001 |
| SRS-RAG-002 | When evidence is meaningful but incomplete or inferential, the answer shall use wording that reflects the uncertainty and must not overstate the claim. | Must | 1. Qualified evidence produces qualified language such as 'suggests', 'indicates', or an equivalent appropriate phrasing.<br>2. The support label and answer wording do not contradict each other. | PRD-GROUND-002 |
| SRS-RAG-003 | When relevant source passages conflict, the answer shall surface the conflict and cite the competing evidence rather than silently resolving it. | Must | 1. The user can inspect each conflicting source.<br>2. The answer does not assert a definitive resolution unless the document provides evidence for that resolution. | PRD-GROUND-003 |
| SRS-RAG-004 | When OCR or extraction quality prevents reliable interpretation, the answer shall communicate that limitation and reduce or withhold affected claims. | Must | 1. Known unreadable or unreliable regions are not used as strong evidence.<br>2. The user is told when source quality materially limits the answer. | PRD-GROUND-004 |
| SRS-RAG-005 | When a question requires knowledge outside the uploaded document, PdfMining shall not silently answer from general model knowledge as if it were document evidence. | Must | 1. The answer says the requested fact is outside what the document establishes, unless the question also has a document-grounded portion that can be answered separately.<br>2. No external-source citation is introduced into document chat. | PRD-GROUND-005 |
| SRS-RAG-006 | When the user asks for speculation, prediction, or an unsupported conclusion, PdfMining shall distinguish document-supported inference from unsupported speculation and decline to present unsupported factual certainty. | Must | 1. Any permitted inference is explicitly qualified and tied to evidence.<br>2. If the requested speculation cannot be grounded, the product states that the document is insufficient. | PRD-GROUND-006 |
| SRS-RAG-007 | Instructions embedded inside uploaded PDF content shall be treated as untrusted document data and must not override the product's grounding, privacy, access, or safety behavior. | Must | 1. A PDF passage instructing the system to ignore prior rules does not change user isolation or evidence policy.<br>2. Such text may be analyzed as document content when relevant, but not executed as product instructions. | PRD-GROUND-007 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-RAG-121 | Before presenting a grounded factual answer, the system shall obtain document evidence relevant to the claim or explicitly return an insufficiency/limitation outcome. | PRD-CHAT-004, PRD-GROUND-001 |
| SRS-RAG-122 | The generation context used for grounded factual answers shall be constrained to the current document evidence plus conversation context used only for intent resolution. | PRD-CHAT-001, PRD-CHAT-003, PRD-GROUND-005 |
| SRS-RAG-123 | The system shall prevent external general knowledge or external web content from being represented as document evidence in the MVP. | PRD-GROUND-005 |
| SRS-RAG-124 | The system shall preserve competing relevant evidence when the document conflicts and shall produce conflict-aware wording rather than an unsupported resolution. | PRD-GROUND-003 |
| SRS-RAG-125 | The system shall reduce, qualify, or withhold claims whose evidence depends on materially unreliable extraction or OCR. | PRD-GROUND-004 |
| SRS-RAG-126 | The system shall distinguish a document-supported inference from an unsupported prediction or speculation in generated output. | PRD-GROUND-006 |

### 7.16 Claim / Citation Association

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-CITE-101 | The system shall represent an answer as one or more claim units when needed to associate document-derived factual statements with supporting evidence. | PRD-CITE-001 |
| SRS-CITE-102 | A claim shall be able to reference one or more evidence items, and an evidence item shall retain its source page/region provenance. | PRD-CITE-003 |
| SRS-CITE-103 | The system shall not mark an unsupported claim as normally supported merely because semantically similar text was retrieved. | PRD-EVID-005 |
| SRS-CITE-104 | Citation previews shall be generated from or linked to the same source content represented by the cited provenance rather than unrelated context. | PRD-CITE-002 |
| SRS-CITE-105 | If exact coordinates are unavailable, citation data shall retain page-level provenance and source preview while explicitly indicating that exact region mapping is unavailable. | PRD-CITE-007, PRD-HL-005 |

### 7.17 Citation Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-CITE-001 | Document-derived factual claims shall use statement/claim-level citations where appropriate rather than relying only on a page-level bibliography. | Must | 1. A factual claim can be unambiguously associated with its supporting citation or citations.<br>2. A citation identifies the correct source page. | PRD-CITE-001 |
| SRS-CITE-002 | Each citation shall provide a page reference and a source-text preview sufficient for the user to recognize the supporting evidence. | Must | 1. The citation displays the source page.<br>2. The citation exposes a supporting excerpt or preview from the document. | PRD-CITE-002 |
| SRS-CITE-003 | The system shall support one or multiple citations for a claim, including citations across multiple pages, when one passage is insufficient. | Must | 1. The UI permits more than one evidence item for a claim.<br>2. Each evidence item can be opened independently. | PRD-CITE-003 |
| SRS-CITE-004 | The system should prioritize a minimal sufficient evidence set in citation presentation while allowing additional supporting evidence when useful. | Should | 1. The primary citation display does not overwhelm the user with redundant passages.<br>2. Additional support remains accessible when the answer depends on it or the user chooses to inspect it. | PRD-CITE-004 |
| SRS-CITE-005 | Citations shall resolve to the original uploaded PDF, including OCR-based citations for scanned content and provenance for statistics/table-derived values. | Must | 1. A native citation opens the original page.<br>2. An OCR citation opens the original scanned page rather than a replacement derivative.<br>3. A table-derived statistic can trace back to its source in the original PDF. | PRD-CITE-005 |
| SRS-CITE-006 | Citation numbering or identifiers, if shown, shall make claim-to-evidence association unambiguous; no specific numbering scheme is required. | Must | 1. A user can determine which evidence supports each cited claim even when multiple citations appear.<br>2. Identifiers do not imply evidence rank or factual probability unless explicitly explained. | PRD-CITE-006 |
| SRS-CITE-007 | When reliable exact source coordinates are unavailable, the citation shall fall back to the correct page and source preview without fabricating precise region mapping. | Must | 1. The user can still open the cited page.<br>2. The UI communicates that exact highlighting is unavailable rather than showing a guessed region. | PRD-CITE-007 |

### 7.18 Evidence-Support Evaluation

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-EVID-001 | For supported generated claims, PdfMining shall display Evidence Support using the categorical labels High, Medium, or Low where claim/evidence verification is available. | Must | 1. The UI uses the labels High, Medium, and Low rather than requiring percentages.<br>2. The label is associated with the specific claim/evidence relationship it describes. | PRD-EVID-001 |
| SRS-EVID-002 | Evidence Support shall mean how strongly the selected document evidence supports the specific generated claim. | Must | 1. Product copy or help text explains the evidence-claim relationship.<br>2. Evidence Support is not labeled as OCR confidence, retrieval relevance, or model confidence. | PRD-EVID-002 |
| SRS-EVID-003 | The system shall never represent Evidence Support as the probability that the answer or claim is factually true. | Must | 1. No label, tooltip, percentage, or explanatory text describes Evidence Support as factual-truth probability.<br>2. High does not imply guaranteed truth. | PRD-EVID-003 |
| SRS-EVID-004 | Medium and Low Evidence Support shall be accompanied by wording and presentation that does not overstate the supported claim. | Must | 1. Medium-support claims use qualified language when support is incomplete or inferential.<br>2. Low-support claims are visibly weak/ambiguous and are not phrased with stronger certainty than the evidence allows. | PRD-EVID-004 |
| SRS-EVID-005 | A claim with no sufficient evidence shall not be presented merely as Low; it must normally be removed or replaced by an explicit insufficient-evidence response. | Must | 1. Unsupported factual claims are not shown with a misleading Low badge as if some evidence supports them.<br>2. The user receives a clear insufficiency message when the answer cannot be established. | PRD-EVID-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-EVID-101 | The evidence-verification capability shall evaluate the support relationship between a specific claim and its selected document evidence, not the probability that the claim is true in the world. | PRD-EVID-002, PRD-EVID-003 |
| SRS-EVID-102 | The system shall keep retrieval similarity, OCR confidence, model confidence, and Evidence Support as logically distinct signals. | PRD-EVID-002 |
| SRS-EVID-103 | The system shall support a distinct Unsupported/Insufficient Evidence outcome separate from the user-facing High, Medium, and Low supported-claim labels. | PRD-EVID-005 |
| SRS-EVID-104 | Evidence Support thresholds or classification rules shall be configurable or replaceable for empirical calibration without redefining their user-facing semantics. | PRD-EVID-001, PRD-EVID-003 |
| SRS-EVID-105 | If evidence verification fails operationally, the system shall not fabricate an Evidence Support label and shall expose a degraded/failed verification state as appropriate. | PRD-ERR-005 |

### 7.19 Source Navigation and Highlighting

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-VIEW-001 | The document workspace shall display the original uploaded PDF as the canonical visual source. | Must | 1. The viewed file is the original uploaded PDF.<br>2. Processing derivatives do not silently replace it. | PRD-VIEW-001 |
| SRS-VIEW-002 | The PDF viewer shall support direct page navigation, sequential scrolling, and zoom controls. | Must | 1. A user can move to a specified page.<br>2. A user can scroll through pages.<br>3. A user can zoom in and out while retaining access to the current document. | PRD-VIEW-002 |
| SRS-VIEW-003 | Citation activation shall navigate the viewer to the cited page and preserve enough context for the user to inspect the source. | Must | 1. Selecting a valid citation changes the viewer to the correct page.<br>2. If an exact highlight is available, it becomes visible after navigation. | PRD-VIEW-003 |
| SRS-VIEW-004 | The viewer and surrounding document workspace shall present Arabic/RTL text correctly where such text is rendered outside the PDF page image/content. | Must | 1. Arabic source previews and UI text use appropriate RTL direction where applicable.<br>2. PDF page rendering itself preserves the original page appearance. | PRD-VIEW-004 |
| SRS-VIEW-005 | The PDF viewer shall remain usable on mobile-responsive web through a view suited to smaller screens rather than requiring the desktop split-screen layout. | Must | 1. On a supported small viewport, the user can switch to and use the PDF viewer.<br>2. Essential page navigation and citation-driven navigation remain available. | PRD-VIEW-005 |

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-HL-001 | When reliable coordinates exist, citation navigation shall highlight the exact supporting source region in yellow on the original PDF. | Must | 1. Selecting an eligible citation shows a yellow highlight over the mapped evidence region.<br>2. The highlighted region is on the correct original page. | PRD-HL-001 |
| SRS-HL-002 | Native-text highlighting shall use reliable native source coordinates and OCR-derived highlighting must use reliable OCR coordinates. | Must | 1. Representative native citations highlight the mapped native source.<br>2. Representative scanned citations highlight the mapped OCR source on the original scanned page. | PRD-HL-002 |
| SRS-HL-003 | Multi-line evidence shall be highlightable as multiple contiguous or logically related regions when one bounding region would be misleading. | Must | 1. A citation spanning line breaks highlights all required lines without highlighting unrelated surrounding text.<br>2. The highlighted set still maps to the single cited evidence item. | PRD-HL-003 |
| SRS-HL-004 | The system should support multiple highlights associated with the same citation when evidence is composed of multiple non-contiguous source regions and one region would be misleading. | Should | 1. Each required mapped region is visually associated with the activated citation.<br>2. The UI does not imply one contiguous source span when the evidence is actually disjoint. | PRD-HL-004 |
| SRS-HL-005 | When exact coordinates are unavailable or unreliable, PdfMining shall omit the exact highlight and provide page-level navigation plus source preview with an explicit limitation. | Must | 1. No guessed yellow rectangle is shown.<br>2. The user can still inspect the correct page and textual evidence when available. | PRD-HL-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-VIEW-101 | The PDF rendering interface shall render the canonical original PDF and shall expose page navigation required by citation activation. | PRD-VIEW-001, PRD-VIEW-003 |
| SRS-VIEW-102 | The highlighting interface shall accept one or more page-relative source regions and render them over the corresponding original PDF page without modifying the PDF file. | PRD-HL-001, PRD-HL-003, PRD-HL-004 |
| SRS-VIEW-103 | The system shall maintain coordinate-system provenance sufficient to interpret native extraction coordinates and OCR-derived coordinates correctly on the original rendered page. | PRD-HL-002 |
| SRS-VIEW-104 | When source regions cannot be mapped reliably to the current rendered page geometry, the system shall omit exact highlighting and preserve page-level navigation/source preview instead. | PRD-HL-005, PRD-CITE-007 |
| SRS-VIEW-105 | Highlighting shall not alter the canonical PDF bytes or become a replacement evidence artifact. | PRD-VIEW-001, PRD-HL-001 |

### 7.20 Search / Sort / Filter

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-SEARCH-001 | The statistics interface shall provide search over displayed metric labels and relevant contextual text. | Must | 1. A search term narrows visible statistics to matching metric/context content.<br>2. Clearing the search restores the unfiltered result set. | PRD-SEARCH-001 |
| SRS-SEARCH-002 | The statistics interface shall provide basic filtering for structured-statistic attributes that are already available, including extracted-versus-derived type and Evidence Support when present. | Must | 1. A user can filter to directly extracted or derived metrics.<br>2. When Evidence Support exists for statistics, the user can filter by support label without changing the underlying data. | PRD-SEARCH-002 |
| SRS-SEARCH-003 | Statistics shall have a stable default ordering, but advanced user-configurable sorting is not an MVP requirement. | Must | 1. The same result set has a predictable default order within a document.<br>2. The product does not require arbitrary multi-column sorting to satisfy MVP acceptance. | PRD-SEARCH-003 |
| SRS-SEARCH-004 | The system shall use a predictable document-history ordering and shall not provide cross-document content search or advanced document filtering as an MVP requirement. | Must | 1. History presents documents in a predictable order.<br>2. The MVP does not expose a search that semantically searches across document contents. | PRD-SEARCH-004 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-SEARCH-101 | Statistics search and filtering shall operate on the retained structured-statistic fields and shall not alter the underlying result records. | PRD-SEARCH-001, PRD-SEARCH-002 |
| SRS-SEARCH-102 | The system shall provide deterministic default ordering for a stable statistics result set and a predictable default history ordering. | PRD-SEARCH-003, PRD-SEARCH-004 |
| SRS-SEARCH-103 | The MVP shall not require semantic search across the contents of multiple documents. | PRD-SEARCH-004 |

### 7.21 Export

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-EXPORT-001 | The system shall allow the user to export structured statistics from a document as CSV. | Must | 1. A Ready or partial document with structured statistics can produce a CSV file.<br>2. The export contains the currently available structured statistics rather than unrelated chat content. | PRD-EXPORT-001 |
| SRS-EXPORT-002 | The system shall allow the user to export structured statistics from a document as Excel. | Must | 1. A Ready or partial document with structured statistics can produce an Excel-compatible workbook.<br>2. The exported metrics correspond to the document's available structured statistics. | PRD-EXPORT-002 |
| SRS-EXPORT-003 | Each exported statistic shall include enough information to identify the source document, metric/value, context, page, provenance, and extracted-versus-derived status. | Must | 1. The export identifies the source document and page for each metric.<br>2. Derived metrics remain explicitly distinguishable from extracted values.<br>3. A provenance field or fields allow the user to trace the metric back to source evidence. | PRD-EXPORT-003 |
| SRS-EXPORT-004 | Export shall preserve relevant uncertainty/partial-result information rather than converting uncertain data into apparently certain data. | Must | 1. Where a statistic is marked partial, ambiguous, or has Evidence Support metadata, the export preserves an appropriate indicator when available.<br>2. Withheld/unsupported values are not invented solely to complete the export. | PRD-EXPORT-004 |
| SRS-EXPORT-005 | The MVP export feature shall not imply support for chat transcript export, standalone citation export, arbitrary full-table export, or regenerated canonical PDFs. | Must | 1. Only approved structured-statistics CSV/Excel export is required for MVP acceptance.<br>2. The UI does not advertise excluded export types as supported MVP capabilities. | PRD-EXPORT-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-EXPORT-101 | CSV and Excel exports shall encode Arabic, English, and mixed-language text without lossy character substitution. | PRD-LANG-001, PRD-EXPORT-003 |
| SRS-EXPORT-102 | Export generation shall include only the approved structured-statistics dataset and associated provenance/uncertainty fields, not chat transcripts or arbitrary full-table exports. | PRD-EXPORT-005 |
| SRS-EXPORT-103 | The export subsystem shall preserve page/source references and extracted-versus-derived classification for each exported statistic. | PRD-EXPORT-003 |
| SRS-EXPORT-104 | The export subsystem shall preserve partial/ambiguous/support indicators when present and shall not synthesize missing values to fill export cells. | PRD-EXPORT-004 |
| SRS-EXPORT-105 | The export subsystem shall neutralize spreadsheet-formula interpretation for untrusted textual fields where needed to prevent exported document content from being executed as a spreadsheet formula. | PRD-SEC-006 |

### 7.22 Document Deletion

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-DATA-101 | Uploaded documents and their document-specific analysis data shall persist in the user's private history until the user deletes the document. | Must | 1. A processed document remains available across later authenticated sessions.<br>2. The product does not silently expire document history under an unstated retention policy. | PRD-RET-001 |
| SRS-DATA-102 | Deleting a document shall logically remove the original PDF, optional searchable derivative, normalized/extracted artifacts, statistics, conversations, citations/evidence artifacts, and other document-specific derived data. | Must | 1. After deletion, the user cannot access any of the listed document-specific artifacts through the product.<br>2. The deleted document no longer appears in history. | PRD-RET-002 |
| SRS-DATA-103 | The deletion confirmation shall warn that document-specific analysis and conversation history will also be removed. | Must | 1. The confirmation names or otherwise clearly identifies the selected document.<br>2. The confirmation explains that the document and associated analysis cannot remain accessible after deletion. | PRD-RET-003 |
| SRS-DATA-104 | The system shall not introduce organization-level retention rules or shared-document lifecycle behavior. | Must | 1. No organization retention policy is required for MVP acceptance.<br>2. A user's document lifecycle is controlled by that user's upload and delete actions. | PRD-RET-004 |
| SRS-DATA-105 | Failed or abandoned processing shall not leave unnecessary temporary document artifacts retained as part of the user's long-term document data. | Must | 1. A failed processing attempt does not create extra user-visible document copies or derivatives that persist without purpose.<br>2. Cleanup of temporary artifacts does not remove successful results that the product intentionally retains for a partial document. | PRD-RET-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-DATA-201 | Confirmed document deletion shall make the original PDF and all document-specific derived artifacts inaccessible through normal product interfaces. | PRD-HIST-005, PRD-RET-002 |
| SRS-DATA-202 | Document deletion shall cover normalized content, OCR artifacts, searchable OCR derivatives, statistics, tables, retrieval units, embeddings, conversations, messages, claims, citations, evidence assessments, exports retained by the product, and processing artifacts associated only with that document. | PRD-RET-002 |
| SRS-DATA-203 | The deletion operation shall verify document ownership before deleting or revealing deletion-specific metadata. | PRD-AUTH-005, PRD-HIST-004 |
| SRS-DATA-204 | If deletion cannot complete, the system shall expose failure without falsely reporting successful deletion; any retry shall be safe to repeat. | PRD-HIST-004, PRD-HIST-005 |
| SRS-DATA-205 | Deletion shall remove or invalidate retrieval/vector entries so deleted content cannot be returned by subsequent retrieval operations. | PRD-RET-002 |

### 7.23 Document History and Management

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-DOC-001 | Authenticated users shall have a private history listing their uploaded documents. | Must | 1. A user can see previously uploaded documents that have not been deleted.<br>2. The list contains only documents owned by the authenticated account. | PRD-HIST-001 |
| SRS-DOC-002 | Each history item shall show enough metadata to identify the document and its current processing status. | Must | 1. At minimum, the original filename and current state are visible.<br>2. Upload time and page count are shown when available without implying unsupported metadata. | PRD-HIST-002 |
| SRS-DOC-003 | The system shall allow an authenticated user to reopen a previously processed document and recover its persisted overview, statistics, conversations, citations, and warnings that remain applicable. | Must | 1. Reopening a Ready document restores the document workspace and available analysis.<br>2. Conversation history remains associated with that document until deletion. | PRD-HIST-003 |
| SRS-DOC-004 | The system shall allow an authenticated user to delete a selected document through an explicit confirmation step. | Must | 1. The product clearly identifies the document to be deleted.<br>2. Deletion does not occur until the user confirms the destructive action. | PRD-HIST-004 |
| SRS-DOC-005 | After confirmed deletion, the document shall disappear from the user's history and its document-specific analysis must no longer be accessible. | Must | 1. The deleted document cannot be reopened from history, citation links, or saved product routes.<br>2. Subsequent access attempts do not reveal deleted content. | PRD-HIST-005 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-DOC-111 | The system shall persist document identity, original filename, owner, processing state, upload time, and page count when available for history/workspace reconstruction. | PRD-HIST-001, PRD-HIST-002 |
| SRS-DOC-112 | Reopening a retained document shall restore applicable persisted overview, structured results, conversation history, citations/evidence, and warnings without requiring re-upload. | PRD-HIST-003 |
| SRS-DOC-113 | A retained document in an in-progress state shall be reopenable so the user can inspect its current status. | PRD-HIST-002, PRD-PROC-001 |

### 7.24 Workspace and Responsive Interaction

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-UX-001 | On desktop, the primary document workspace shall allow the original PDF to be visible alongside analysis/chat. | Must | 1. A user can inspect the PDF and analysis/chat without leaving the document workspace.<br>2. Citation navigation updates the source side while the answer context remains available. | PRD-SPLIT-001 |
| SRS-UX-002 | On small screens, the product shall use switchable views rather than forcing the desktop side-by-side layout. | Must | 1. The user can switch between analysis/chat and PDF views.<br>2. Citation activation can take the user to the PDF view and cited page without losing the conversation state. | PRD-SPLIT-002 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-UX-201 | The desktop document workspace shall permit simultaneous visibility of the canonical PDF and analysis/chat content. | PRD-SPLIT-001, PRD-UX-001 |
| SRS-UX-202 | On small viewports, the system shall preserve document/chat state when switching between analysis and PDF views, including citation-driven transitions. | PRD-SPLIT-002, PRD-VIEW-005 |
| SRS-UX-203 | Critical evidence, warning, error, and support semantics shall be represented by text or equivalent non-color-only cues. | PRD-UX-003 |
| SRS-UX-204 | Keyboard-focusable interactive controls shall use standard browser interaction semantics where the chosen UI control model supports them. | PRD-UX-002 |

## 8. Data Requirements

The SRS defines logical information obligations, not a physical schema. The implementation may combine or split entities as long as the requirements and provenance relationships are preserved.

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-DATA-001 | The system shall maintain a logical User entity sufficient to identify an account and associate owned documents and protected operations with that account. | PRD-AUTH-001, PRD-AUTH-005 |
| SRS-DATA-002 | The system shall maintain a logical Document entity representing the canonical original PDF, ownership, lifecycle state, upload metadata, and processing metadata. | PRD-HIST-001, PRD-HIST-002, PRD-VIEW-001 |
| SRS-DATA-003 | The system shall represent document pages as individually addressable source units linked to the canonical document. | PRD-NATIVE-001, PRD-OCR-003 |
| SRS-DATA-004 | The system shall represent extracted blocks/spans or equivalent granular source units needed for reading order and citation mapping. | PRD-NATIVE-001, PRD-CITE-001 |
| SRS-DATA-005 | The system shall represent OCR results with text, page/region provenance, and available confidence metadata. | PRD-OCR-003 |
| SRS-DATA-006 | The system shall represent reconstructed tables and their source provenance when reliable structured output exists. | PRD-TABLE-001, PRD-TABLE-002 |
| SRS-DATA-007 | The system shall represent structured statistics with their labels, values, context, source provenance, and extracted-versus-derived status. | PRD-STAT-002, PRD-STAT-003 |
| SRS-DATA-008 | The system shall represent retrieval units and references to semantic-vector representations without requiring a particular physical vector schema. | PRD-CHAT-004 |
| SRS-DATA-009 | The system shall represent conversations, messages, answers, claims, citations, and evidence assessments in relationships that preserve document and user scope. | PRD-CHAT-006, PRD-CITE-001, PRD-EVID-001 |
| SRS-DATA-010 | The system shall represent processing jobs or equivalent processing-state records sufficiently to support retries, recovery, and observability. | PRD-PROC-001, PRD-PROC-007 |
| SRS-DATA-011 | The system shall represent exports or export-generation state when needed to provide in-progress, completion, and failure behavior. | PRD-PERF-007, PRD-ERR-008 |
| SRS-DATA-012 | Document-specific logical entities shall be deletable as a dependency graph rooted in the owned Document. | PRD-RET-002 |
| SRS-DATA-013 | Retained document-associated data shall persist until explicit document deletion except for temporary artifacts that are not required for retained product behavior. | PRD-RET-001, PRD-RET-005 |
| SRS-DATA-014 | Temporary processing artifacts shall be eligible for cleanup after failure or completion when they are no longer required for recovery or retained partial results. | PRD-RET-005 |

### 8.1 Logical Entities

| Logical Entity | Purpose | Critical Information | Relationships | Retention Considerations |
|---|---|---|---|---|
| User | Authenticated account identity and ownership root. | Account identity; authentication/authorization references. | Owns documents. | Account lifecycle is outside document deletion unless separately approved. |
| Document | Canonical PDF and lifecycle root. | Owner, original-file identity, filename, state, upload metadata, page count, processing metadata. | Owns pages and document-specific artifacts. | Retained until user deletion. |
| DocumentPage | Addressable original page. | Document reference, page number, rendering/source metadata. | Belongs to Document; source for blocks/spans/OCR/tables. | Deleted with Document. |
| ExtractedBlock / ExtractedSpan | Normalized source text/structure. | Text, reading order, page, coordinates, provenance, confidence where available. | Belongs to page; source for chunks/citations/statistics. | Deleted with Document. |
| OCRResult | OCR-derived source content. | Recognized text, page/region, reading order, confidence, OCR provenance. | Linked to page/source region. | Deleted with Document. |
| Table | Reliable/partial structured table representation. | Structure, quality/partiality, source pages/regions. | Linked to source regions and statistics. | Deleted with Document. |
| Statistic | Structured quantitative result. | Label, value, unit, context, type, provenance, uncertainty/support. | Linked to source evidence and optional derivation inputs. | Deleted with Document. |
| RetrievalChunk | Retrievable source-linked unit. | Text/content reference, document/user scope, source provenance. | Linked to source spans/regions and embedding reference. | Deleted/rebuilt with Document. |
| EmbeddingReference | Reference to semantic representation. | Retrieval-unit identity, model/version metadata as needed, vector reference. | Belongs to retrieval unit/document/user. | Deleted/rebuilt with Document. |
| Conversation / Message | Document chat history. | Document/user scope, message role/content/state, timestamps as needed. | Belongs to Document/User. | Deleted with Document. |
| Answer / Claim | Generated answer and claim units. | Answer state/text; claim text/identity. | Linked to message, citations, evidence assessments. | Deleted with Document. |
| Citation | Claim-to-source association. | Document, page, source region(s), preview, evidence reference, mapping reliability. | Supports claim/statistic and viewer navigation. | Deleted with Document. |
| EvidenceAssessment | Support evaluation for claim/evidence. | Claim, evidence set, support outcome, evaluation metadata as needed. | Linked to Claim and Citation/Evidence. | Deleted with Document. |
| Export | Generated export or generation state. | Document, format, status, generated artifact reference as needed. | Derived from statistics. | Temporary or deleted with Document if retained. |
| ProcessingJob | Logical processing/retry state. | Document, phase, attempt, outcome, warning/error references. | Operates on Document and derived artifacts. | Retained only as required for recovery/audit. |

## 9. Data Provenance Requirements

Canonical provenance chain:

```text
Statistic / Retrieval Unit / Claim / Citation / Evidence Assessment
                     ↓
               Source Span(s) / Region(s)
                     ↓
                    Page
                     ↓
             Original uploaded PDF
```

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-DATA-301 | Every persisted statistic shall be traceable to one or more source spans/regions and pages in the original PDF, directly or through a retained derivation relationship. | PRD-STAT-002, PRD-STAT-004 |
| SRS-DATA-302 | Every retained retrieval unit shall be traceable to normalized source content and the original document/page. | PRD-CITE-005 |
| SRS-DATA-303 | Every citation shall identify the originating document and page and shall reference the supporting source span/region or page-level fallback. | PRD-CITE-002, PRD-CITE-005, PRD-CITE-007 |
| SRS-DATA-304 | Every OCR-derived source item used downstream shall preserve OCR provenance distinct from native extraction provenance. | PRD-OCR-003, PRD-OCR-004 |
| SRS-DATA-305 | Every derived metric shall preserve source-input provenance and an explicit derived classification. | PRD-STAT-003, PRD-STAT-004 |
| SRS-DATA-306 | Every claim-level Evidence Support assessment shall be traceable to the evaluated claim and evidence set. | PRD-EVID-001, PRD-EVID-002 |
| SRS-DATA-307 | Provenance references shall survive persistence and reopening of a document so restored citations continue to resolve correctly while the document remains retained. | PRD-HIST-003, PRD-CITE-005 |

## 10. External Interface Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-EXT-001 | The browser/client interface shall support authenticated account access, document upload, processing-state display, document history, analysis, chat, citation activation, export, and deletion. | PRD-AUTH-001, PRD-DOC-005, PRD-HIST-001 |
| SRS-EXT-002 | The PDF rendering interface shall render the canonical original PDF and support page navigation, scrolling, zoom, and overlay highlighting. | PRD-VIEW-001, PRD-VIEW-002, PRD-HL-001 |
| SRS-EXT-003 | The OCR interface shall accept page or region content and return recognized text with source-location information and confidence when available. | PRD-OCR-001, PRD-OCR-003 |
| SRS-EXT-004 | The generative AI interface shall support document-grounded overview and Q&A generation from supplied evidence/context without requiring external web access. | PRD-PROC-006, PRD-CHAT-004, PRD-GROUND-005 |
| SRS-EXT-005 | The embedding interface shall accept eligible text units and return semantic representations suitable for document-scoped retrieval. | PRD-CHAT-004 |
| SRS-EXT-006 | The vector retrieval interface shall support document/user-scoped retrieval and return source-linked candidate items. | PRD-AUTH-005, PRD-CHAT-001, PRD-CITE-005 |
| SRS-EXT-007 | The evidence-verification interface shall support structured evaluation of a claim against one or more evidence items and return enough information to derive the approved support outcome. | PRD-EVID-001, PRD-EVID-002 |
| SRS-EXT-008 | The persistent file-storage interface shall preserve the original PDF as immutable canonical content until deletion and shall distinguish derived artifacts. | PRD-NATIVE-003, PRD-RET-002 |
| SRS-EXT-009 | The persistent structured-data interface shall support atomic or otherwise consistency-preserving updates required for ownership, processing state, provenance, and deletion semantics. | PRD-AUTH-005, PRD-PROC-001, PRD-RET-002 |
| SRS-EXT-010 | The export interface shall generate standards-compatible CSV and Excel outputs containing the approved structured-statistics fields. | PRD-EXPORT-001, PRD-EXPORT-002, PRD-EXPORT-003 |
| SRS-EXT-011 | External processing interfaces shall expose failure/time-out outcomes distinctly enough for the application to separate operational failure from semantic insufficient evidence. | PRD-ERR-005, PRD-ERR-006 |

### 10.1 User Interface Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-UX-101 | The system shall provide a document-centered desktop web experience and a mobile-responsive web experience. | Must | 1. Desktop supports the side-by-side document workspace.<br>2. Small viewports use switchable views rather than forcing the desktop layout. | PRD-UX-001 |
| SRS-UX-102 | The system should make primary interactive controls for upload, navigation, chat submission, citation activation, filters, export, and deletion operable using standard keyboard interaction where the browser control model supports it. | Should | 1. Interactive controls can receive focus in a logical sequence.<br>2. Focused buttons/links can be activated using standard keyboard actions. | PRD-UX-002 |
| SRS-UX-103 | Citation, warning, error, and Evidence Support states shall use readable text labels and must not rely solely on color. | Must | 1. High/Medium/Low appears as text, not color alone.<br>2. Warnings/errors include text that communicates meaning. | PRD-UX-003 |
| SRS-UX-104 | Arabic/RTL presentation shall remain usable across supported viewport sizes, including chat, source previews, statistics context, and warning text. | Must | 1. RTL content does not obscure essential controls or citation associations.<br>2. Switching between PDF and analysis on mobile preserves reading direction and context. | PRD-UX-004 |
| SRS-UX-105 | The system shall not claim formal WCAG or other accessibility conformance unless separately defined and validated. | Must | 1. Public/product copy does not claim a conformance level that has not been tested and approved.<br>2. Basic usability requirements in this PRD are not represented as certification. | PRD-UX-005 |

The exact visual design, component library, browser-version matrix, and frontend framework remain later decisions. The interface must nevertheless preserve the functional and localization requirements above.

### 10.2 PDF Rendering Interface

The PDF interface must satisfy SRS-EXT-002 and SRS-VIEW-* / SRS-HL-* requirements.

### 10.3 AI Generation Interface

The AI generation interface must satisfy SRS-EXT-004 and the SRS-RAG-* grounding requirements.

### 10.4 Embedding Interface

The embedding interface must satisfy SRS-EXT-005 and SRS-EMB-*.

### 10.5 Verification / Decision Interface

The verification interface must satisfy SRS-EXT-007 and SRS-EVID-* without defining a final JEV or other implementation.

### 10.6 OCR Interface

The OCR interface must satisfy SRS-EXT-003 and SRS-OCR-*.

### 10.7 Object / File Storage Interface

The file-storage interface must satisfy SRS-EXT-008, SRS-DOC-101 through SRS-DOC-104, and document deletion requirements.

## 11. Security Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-SEC-001 | A user's documents and document-derived data shall be inaccessible to other users. | Must | 1. Cross-account access to PDFs, OCR text, statistics, conversations, citations, exports, or derived artifacts is denied.<br>2. Unauthorized attempts do not disclose protected content. | PRD-SEC-001 |
| SRS-SEC-002 | Document data shall be protected in transit and at rest as a product security requirement. | Must | 1. Production use does not transmit protected document content over an unencrypted application channel.<br>2. Stored original and derived document data are covered by the product's at-rest protection design, to be specified technically in the SRS/design stages. | PRD-SEC-002 |
| SRS-SEC-003 | Where external AI/OCR processing is used, PdfMining shall minimize transmitted document content to what is needed for the processing task and provide understandable privacy disclosure where relevant. | Must | 1. The product/privacy information does not imply all processing is local if external providers are used.<br>2. The product does not send unrelated document content merely for convenience when a smaller relevant portion suffices. | PRD-SEC-003 |
| SRS-SEC-004 | Product and operational error behavior shall not expose PDF passwords or unnecessarily include sensitive document content. | Must | 1. User-visible errors never display the submitted PDF password.<br>2. Normal product diagnostics presented to users avoid dumping document content. | PRD-SEC-004 |
| SRS-SEC-005 | The system shall make no unsupported compliance, certification, regulated-industry, regional-residency, or multi-region claims. | Must | 1. Marketing/product UI does not claim SOC 2, ISO 27001, HIPAA, government certification, configurable data residency, or multi-region deployment unless separately established.<br>2. No hosting-region selector is offered in the MVP. | PRD-SEC-005 |
| SRS-SEC-006 | Uploaded PDF content shall be treated as untrusted data and cannot change account permissions, system rules, evidence policy, or product behavior merely by containing instructions. | Must | 1. Embedded instructions cannot grant access to another user's content.<br>2. Embedded instructions cannot cause external knowledge to be presented as document evidence. | PRD-SEC-006 |
| SRS-SEC-007 | Where external AI/OCR providers are used and provider controls are available, the system should use configurations that prevent submitted content from being used for model training and minimize or disable provider retention. | Should | 1. Provider configuration is reviewed for available training-use controls before production use.<br>2. Available retention-minimization settings are enabled where compatible with the approved product behavior.<br>3. Product disclosure does not claim stronger provider privacy behavior than is actually configured. | PRD-SEC-007 |
| SRS-SEC-008 | Operational logging associated with document processing shall minimize document content and exclude secrets such as user-supplied PDF passwords. | Must | 1. PDF passwords are not recorded in operational logs.<br>2. Normal logs avoid storing full document text/source excerpts unless a separately approved diagnostic process explicitly requires and protects them. | PRD-SEC-008 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-SEC-101 | All production transport of authentication data, original PDFs, derived document data, and user questions/answers shall use encrypted transport appropriate to the deployment environment. | PRD-SEC-002 |
| SRS-SEC-102 | Persisted original and derived document data shall be protected at rest using the storage-security controls selected in Technical Design. | PRD-SEC-002 |
| SRS-SEC-103 | Secrets, credentials, API keys, and user-supplied PDF passwords shall not be committed to source code or exposed in client-delivered configuration. | PRD-SEC-004, PRD-SEC-008 |
| SRS-SEC-104 | Runtime components shall receive only the permissions and document scope required for their assigned processing function. | PRD-SEC-001, PRD-SEC-003 |
| SRS-SEC-105 | Uploaded PDFs shall be treated as hostile/untrusted input and processed using controls that prevent document content from being executed as application instructions or gaining system privileges. | PRD-GROUND-007, PRD-SEC-006 |
| SRS-SEC-106 | Operational logs shall exclude PDF passwords and shall minimize raw document text, questions, answers, and source excerpts. | PRD-SEC-004, PRD-SEC-008, PRD-OBS-002 |
| SRS-SEC-107 | External processing requests shall include only the content reasonably necessary for the requested OCR, generation, embedding, or verification operation. | PRD-SEC-003 |
| SRS-SEC-108 | Where an external provider offers retention/training controls, production configuration should disable training use and minimize retention when compatible with required functionality. | PRD-SEC-007 |
| SRS-SEC-109 | Authorization failures shall be logged with non-sensitive identifiers sufficient for security investigation without logging protected document contents. | PRD-SEC-001, PRD-SEC-008 |
| SRS-SEC-110 | Deletion authorization shall be checked before destructive processing begins and before document-specific metadata is disclosed. | PRD-HIST-004, PRD-SEC-001 |

## 12. Privacy Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-PRIV-001 | The system shall treat original PDFs, extracted content, conversations, citations, statistics, and exports as confidential user data. | PRD-SEC-001 |
| SRS-PRIV-002 | If external providers receive document content, product/privacy disclosure shall accurately state that external processing occurs and shall not imply local-only processing. | PRD-SEC-003 |
| SRS-PRIV-003 | The system shall retain document-specific user data until user deletion under the MVP model, except for temporary artifacts eligible for earlier cleanup. | PRD-RET-001, PRD-RET-005 |
| SRS-PRIV-004 | The system shall not create organization-level retention or shared-document lifecycle rules in the MVP. | PRD-RET-004 |
| SRS-PRIV-005 | Analytics/observability payloads shall minimize personally identifiable or sensitive document content and shall not require full questions, answers, or source excerpts for approved MVP events. | PRD-OBS-001, PRD-OBS-002 |
| SRS-PRIV-006 | The system shall not claim provider privacy, regional residency, certification, or compliance properties stronger than those actually configured and validated. | PRD-SEC-005, PRD-SEC-007 |

## 13. Performance Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-PERF-001 | Upload interactions shall remain responsive enough to show immediate acknowledgment and ongoing upload status; no public upload-time SLA is established. | Must | 1. Starting an upload produces visible acknowledgment.<br>2. The user can distinguish an active upload from an unresponsive page. | PRD-PERF-001 |
| SRS-PERF-002 | The system should be validated on representative native PDFs within the initial limit against an end-to-end processing target of roughly 30–60 seconds. | Should | 1. Representative benchmark results are recorded against the target.<br>2. Product messaging does not convert the target into a guaranteed completion time. | PRD-PERF-002 |
| SRS-PERF-003 | The system should be validated on representative OCR-heavy PDFs within the initial limit against a processing target of roughly 2–3 minutes. | Should | 1. Representative OCR-heavy benchmark results are recorded.<br>2. Grounding/citation correctness is not intentionally weakened solely to hit the target. | PRD-PERF-003 |
| SRS-PERF-004 | The system should be validated on typical document-chat questions against an initial response target of approximately 5–10 seconds. | Should | 1. Representative questions are benchmarked.<br>2. Slow responses show an in-progress state rather than appearing lost.<br>3. The target is not advertised as a guaranteed SLA. | PRD-PERF-004 |
| SRS-PERF-005 | The system should be validated against an engineering scenario of approximately 10 simultaneously active users on the approved hosting environment. | Should | 1. A documented validation run evaluates the representative workload.<br>2. Failure to meet the scenario triggers technical remediation/hosting review rather than silently changing product evidence quality. | PRD-PERF-005 |
| SRS-PERF-006 | The PDF viewer, page navigation, citation navigation, and statistics interactions shall remain usable while background or downstream processing continues when the required underlying content is already available. | Must | 1. Opening an available PDF does not require unrelated failed/unfinished analysis to finish.<br>2. Navigation controls provide visible response to user action. | PRD-PERF-006 |
| SRS-PERF-007 | CSV/Excel export shall provide visible in-progress and success/failure feedback; no public export-time SLA is established. | Must | 1. Starting export produces visible acknowledgment.<br>2. Completion provides the file; failure provides a retryable error without altering analysis. | PRD-PERF-007 |
| SRS-PERF-008 | The system shall not present the validation targets in this PRD as public uptime, recovery-time, or guaranteed latency SLAs. | Must | 1. Product/marketing copy does not promise the 30–60 second, 2–3 minute, or 5–10 second targets as guaranteed completion times.<br>2. No uptime or recovery-time SLA is claimed unless separately approved and validated. | PRD-PERF-008 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-PERF-101 | Interactive actions shall provide prompt visible acknowledgment even when completion is asynchronous, including upload, question submission, citation navigation, and export initiation. | PRD-PERF-001, PRD-PERF-004, PRD-PERF-007 |
| SRS-PERF-102 | Background document processing shall not unnecessarily block access to the original PDF or already-completed valid outputs. | PRD-PERF-006, PRD-PROC-003 |
| SRS-PERF-103 | Performance validation shall record representative native-document, OCR-heavy-document, chat, and concurrency measurements against the PRD targets without converting them into contractual SLAs. | PRD-PERF-002, PRD-PERF-003, PRD-PERF-004, PRD-PERF-005, PRD-PERF-008 |
| SRS-PERF-104 | Performance optimizations shall not intentionally weaken grounding, citation correctness, source traceability, or Evidence Support semantics solely to meet provisional timing targets. | PRD-PERF-003, PRD-PERF-005 |

Performance targets in this SRS are engineering validation targets carried from the PRD, not public SLAs.

## 14. Scalability Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-SCALE-001 | The MVP shall support validation of approximately 10 simultaneously active users on the approved existing VPS environment using a representative workload. | PRD-PERF-005 |
| SRS-SCALE-002 | The system shall support documents up to the configured page limit, initially 20 pages, without assuming support for larger documents. | PRD-DOC-002 |
| SRS-SCALE-003 | The system shall support documents up to the configured file-size limit, initially targeting approximately 25 MB, without hard-coding that value as a permanent product constant. | PRD-DOC-003 |
| SRS-SCALE-004 | Exact limits for documents per user, total stored volume, concurrent processing jobs, and concurrent chat requests beyond the validated MVP workload remain unresolved technical capacity decisions and shall not be invented in this SRS. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-SCALE-005 | Capacity limitations shall fail or queue safely without cross-user data leakage or corruption of the canonical original PDF. | PRD-SEC-001, PRD-PROC-001 |

## 15. Reliability Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-REL-001 | Retryable processing operations shall be idempotent or otherwise protected from creating duplicate retained outputs for the same logical operation. | PRD-PROC-003, PRD-ERR-003, PRD-ERR-005 |
| SRS-REL-002 | A process/service interruption shall not corrupt or overwrite the canonical original PDF. | PRD-NATIVE-003 |
| SRS-REL-003 | After interruption, the system shall recover persisted document state sufficiently to resume, retry, or fail visibly without presenting an impossible Ready state. | PRD-PROC-001, PRD-PROC-005 |
| SRS-REL-004 | Successful intermediate outputs shall be preserved when downstream processing fails and those outputs remain valid. | PRD-PROC-003 |
| SRS-REL-005 | Failure in OCR, statistics extraction, table reconstruction, AI generation, verification, or export shall be isolated from unrelated already-usable capabilities where practical. | PRD-ERR-003, PRD-ERR-004, PRD-ERR-005, PRD-ERR-008 |
| SRS-REL-006 | The system shall prevent stale or duplicate processing completion from silently replacing newer valid processing state. | PRD-PROC-001 |
| SRS-REL-007 | A user-visible Ready state shall only be set when the system has a usable minimum result and no known material limitation requiring a warning/partial state. | PRD-PROC-004, PRD-PROC-005 |
| SRS-REL-008 | Partial-success states shall retain the identity of failed/limited capabilities so later inspection and retry can target the affected area. | PRD-PROC-004, PRD-ERR-007 |

## 16. Availability and Recovery Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-AVAIL-001 | The MVP shall not claim a public uptime or recovery-time SLA unless separately approved and validated. | PRD-PERF-008 |
| SRS-AVAIL-002 | Persistent document state shall survive application/process restart so retained documents do not depend on in-memory state alone. | PRD-HIST-003, PRD-PROC-007 |
| SRS-AVAIL-003 | During a downstream service outage, the system shall present an operational failure/in-progress state rather than an unsupported semantic answer. | PRD-ERR-005, PRD-ERR-006 |
| SRS-AVAIL-004 | Recovery behavior shall preserve user isolation and the canonical-source invariant. | PRD-SEC-001, PRD-NATIVE-003 |

## 17. Observability Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-OBS-001 | For MVP validation, the system should make key document lifecycle outcomes observable at event level without making analytics a user-facing feature. | Should | 1. At minimum, document uploaded, processing completed, processing completed with warnings/partial results, processing failed, and document deleted can be counted or reviewed.<br>2. Event observation does not require storing full document text or PDF passwords in analytics data. | PRD-OBS-001 |
| SRS-OBS-002 | For MVP validation, the system should make key evidence-workflow outcomes observable at event level while minimizing document content in analytics payloads. | Should | 1. At minimum, question asked, answer returned, insufficient-evidence returned, citation activated, and export completed/failed can be observed.<br>2. The observable event does not need to contain the user's full question, answer, or source excerpt. | PRD-OBS-002 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-OBS-101 | The system shall make upload validation failures and upload completion observable with document/job correlation identifiers that do not contain document content. | PRD-OBS-001 |
| SRS-OBS-102 | The system shall record or expose processing phase durations and terminal outcomes sufficient to evaluate native and OCR-heavy processing targets. | PRD-PERF-002, PRD-PERF-003, PRD-OBS-001 |
| SRS-OBS-103 | The system shall make OCR failures, extraction warnings, and partial-processing outcomes observable at document/capability level. | PRD-ERR-003, PRD-ERR-007, PRD-OBS-001 |
| SRS-OBS-104 | The system shall make AI generation, evidence-verification, embedding, and retrieval failures observable without requiring full sensitive payload logging. | PRD-ERR-005, PRD-OBS-002 |
| SRS-OBS-105 | The system shall make citation activation and citation-generation/mapping failures observable for validation of evidence navigation. | PRD-OBS-002, PRD-CITE-007 |
| SRS-OBS-106 | The system shall make export completion/failure and retry attempts observable. | PRD-OBS-002, PRD-ERR-008 |
| SRS-OBS-107 | Processing and downstream events shall be correlatable to the relevant user-safe document/job identifiers and processing attempt. | PRD-OBS-001 |
| SRS-OBS-108 | Observability data shall distinguish insufficient-evidence outcomes from AI/provider/time-out failures. | PRD-ERR-006, PRD-OBS-002 |

## 18. Auditability Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-AUDIT-001 | The system shall retain enough processing metadata to explain which major processing capabilities completed, warned, or failed for a retained document. | PRD-PROC-007 |
| SRS-AUDIT-002 | For a retained generated answer, the system shall retain or reconstruct the claim-to-evidence associations needed to inspect displayed citations and Evidence Support. | PRD-CITE-001, PRD-EVID-001 |
| SRS-AUDIT-003 | The system shall retain enough deletion outcome metadata to determine whether a confirmed deletion completed or failed without retaining deleted document contents solely for audit. | PRD-HIST-005, PRD-RET-002 |
| SRS-AUDIT-004 | Major user actions relevant to document lifecycle—upload, deletion, question submission, citation activation, and export—should be auditable through minimal-content events. | PRD-OBS-001, PRD-OBS-002 |
| SRS-AUDIT-005 | Audit/observability records shall not become an alternate store of full deleted document content. | PRD-RET-002, PRD-SEC-008 |

## 19. Localization / Language Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-LANG-001 | Arabic and English documents shall both be supported as first-class MVP scenarios for native extraction, OCR where needed, statistics, citations, and document chat. | Must | 1. Representative Arabic and English documents can complete the supported workflow.<br>2. Arabic is not presented as an experimental or optional feature relative to English. | PRD-LANG-001 |
| SRS-LANG-002 | Mixed Arabic/English documents shall be supported without requiring the user to choose a single document language. | Must | 1. A document containing both Arabic and English can be processed.<br>2. Evidence from both supported languages can be cited when relevant. | PRD-LANG-002 |
| SRS-LANG-003 | Arabic and English questions shall be accepted, and answers shall default to the language of the user's question when practical. | Must | 1. An Arabic question can receive an Arabic answer when the answer is supported.<br>2. An English question can receive an English answer when the answer is supported. | PRD-LANG-003 |
| SRS-LANG-004 | The system should process understandable mixed-language questions and answer in the dominant or user-requested supported language when practical, without claiming a separate code-switching accuracy guarantee. | Should | 1. A mixed Arabic/English question is processed when its intent is understandable.<br>2. If the intent is ambiguous, the product asks for clarification or states the ambiguity rather than inventing intent. | PRD-LANG-004 |
| SRS-LANG-005 | Arabic UI/content areas such as chat, source previews, metric context, and warnings shall use appropriate RTL presentation where applicable, while preserving original PDF page appearance. | Must | 1. Arabic textual UI content is readable in RTL direction.<br>2. Mixed-language strings remain legible and source navigation remains correct. | PRD-LANG-005 |
| SRS-LANG-006 | The system shall not promise automatic translation between Arabic and English as an MVP feature. | Must | 1. The product does not advertise translation as part of the MVP.<br>2. Answering in a supported interaction language does not alter the canonical source text or citation. | PRD-LANG-006 |

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-LANG-101 | All persisted and transmitted textual data shall use a Unicode-safe encoding capable of losslessly representing Arabic, English, and mixed text. | PRD-LANG-001, PRD-LANG-002 |
| SRS-LANG-102 | The UI shall support RTL presentation for Arabic chat content, source previews, metric context, warnings, and other textual areas outside the original PDF. | PRD-LANG-005, PRD-VIEW-004 |
| SRS-LANG-103 | The system shall preserve the original PDF page appearance and shall not rewrite source text merely to enforce UI directionality. | PRD-LANG-005, PRD-VIEW-004 |
| SRS-LANG-104 | Numeric text and punctuation in Arabic/mixed content shall be preserved as extracted rather than normalized into a different numeral system without an explicit approved transformation. | PRD-LANG-001 |
| SRS-LANG-105 | Citation source mapping and highlighting shall remain correct for RTL and mixed-direction source text when reliable coordinates exist. | PRD-LANG-001, PRD-HL-001 |
| SRS-LANG-106 | The system shall not automatically translate source documents or citations as an MVP feature. | PRD-LANG-006 |

## 20. File and Document Limits

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-SYS-101 | The page-count limit shall be configuration-controlled; its initial MVP value shall be 20 pages. | PRD-DOC-002 |
| SRS-SYS-102 | The file-size limit shall be configuration-controlled; the initial MVP target shall be approximately 25 MB and the active value shall be communicated on rejection. | PRD-DOC-003 |
| SRS-SYS-103 | Only PDF input shall be accepted by the MVP document-ingestion path. | PRD-DOC-001 |
| SRS-SYS-104 | Password-protected PDFs shall require a valid user-supplied password; the system shall not attempt password cracking or protection bypass. | PRD-DOC-004, PRD-ERR-002 |
| SRS-SYS-105 | Zero-page, corrupted, unreadable, or otherwise unprocessable PDFs shall not reach a misleading Ready state. | PRD-DOC-007, PRD-ERR-001 |

The active page and file-size limits are configuration-controlled. The initial page maximum is 20 pages. The initial size target is approximately 25 MB, but the active configured value is the value the system must enforce and communicate. Password-protected PDFs require a valid user-supplied password; protection bypass is out of scope.

## 21. Error Handling Requirements

| SRS ID | Requirement | Priority | Verification conditions carried from PRD | Source |
|---|---|---|---|---|
| SRS-ERR-001 | Invalid, corrupted, or unreadable PDFs shall produce a clear upload/processing error and must not enter a misleading Ready state. | Must | 1. The user sees that the document could not be processed.<br>2. Where appropriate, the user can re-upload a corrected copy. | PRD-ERR-001 |
| SRS-ERR-002 | Password-protected or encrypted PDFs that cannot be opened with the supplied password shall request correction or fail visibly; PdfMining must not attempt protection bypass. | Must | 1. An incorrect password does not unlock or process protected content.<br>2. The user can submit a corrected password when the document format is otherwise supported. | PRD-ERR-002 |
| SRS-ERR-003 | An OCR failure shall identify OCR as the affected capability and preserve usable non-OCR results when possible. | Must | 1. Native pages remain usable when OCR on another page fails.<br>2. The document carries a visible partial-processing/OCR warning. | PRD-ERR-003 |
| SRS-ERR-004 | A structured extraction or table reconstruction failure shall not invalidate the original PDF viewer or successful chat/evidence features that remain supportable. | Must | 1. The original PDF remains accessible.<br>2. The affected extraction result is withheld or marked unavailable rather than fabricated. | PRD-ERR-004 |
| SRS-ERR-005 | An AI generation or verification provider failure shall produce a visible answer failure and a retry path while preserving already completed document processing. | Must | 1. The failed answer is not presented as complete.<br>2. Previously extracted statistics, PDF access, and prior successful chat messages remain available. | PRD-ERR-005 |
| SRS-ERR-006 | A timeout during processing or answer generation shall be distinguishable from a semantic insufficient-evidence response. | Must | 1. The user is told that processing/answer generation did not complete.<br>2. The UI does not mislabel a timeout as 'the document has no evidence'. | PRD-ERR-006 |
| SRS-ERR-007 | Partial results shall be explicitly labeled and must identify the affected capability or limitation at a useful level. | Must | 1. The user can distinguish full-ready output from partial-ready output.<br>2. Known missing OCR/table/statistics capability is not silently omitted without a relevant warning when it materially affects results. | PRD-ERR-007 |
| SRS-ERR-008 | Export failure shall leave the document and its analysis intact and offer a retry or re-initiation path. | Must | 1. A failed export does not delete or alter document results.<br>2. The user receives a visible failure message and can attempt export again. | PRD-ERR-008 |
| SRS-ERR-009 | Error and warning messages shall avoid exposing sensitive document content, passwords, or unnecessary provider/internal details. | Must | 1. A password is never echoed in an error message.<br>2. Errors explain the actionable user-facing problem without exposing protected internal data. | PRD-ERR-009 |

| Error Class | Retryability / Recovery | Required User-Visible Behavior | Preservation Rule |
|---|---|---|---|
| Validation / unsupported format / over limit | Normally non-retryable until input/configuration changes. | State the actionable validation reason and active limit where relevant. | Do not start normal downstream analysis. |
| Corrupted/unreadable PDF | Re-upload/correct source; retry only if failure may be transient. | Fail visibly; never Ready. | Preserve no misleading derived output. |
| Password/encryption issue | Retry with corrected password. | Request/correct password; never bypass protection. | Do not expose or log password. |
| Parsing failure | Retry may be offered if transient; otherwise partial/fail. | Identify extraction limitation. | Preserve independent usable outputs. |
| OCR failure | Retryable where appropriate. | Identify OCR as affected capability; partial warning when other content is usable. | Preserve native/successful OCR results. |
| Table/statistics extraction failure | Retryable where appropriate. | Withhold/mark affected output; keep canonical PDF usable. | Preserve other analysis. |
| AI / verification provider failure | Retryable for transient failures. | Show failed answer/verification state, not insufficient evidence. | Preserve document processing and prior chat. |
| Embedding / retrieval failure | Retryable for transient failures. | Show operational failure when Q&A cannot proceed. | Do not fabricate an answer. |
| Export failure | Retryable. | Show export failure and allow re-initiation. | Document/results remain unchanged. |
| Storage failure | Depends on operation; retry after recovery where safe. | Do not report success when persistence did not complete. | Protect canonical source and consistent state. |
| Authorization failure | Not retryable without valid identity/ownership. | Deny access without protected metadata disclosure. | No protected data returned. |

## 22. Accepted MVP Limitations

| Limitation | Required System Behavior | Warning / Fallback |
|---|---|---|
| OCR on degraded scans may be inaccurate or incomplete. | Use reliable partial OCR; qualify/withhold affected analysis. | Warn when material. |
| Arabic OCR quality varies by font, scan quality, layout, and content. | Apply the same evidence-first behavior and propagate uncertainty. | Warn when material. |
| Mixed-language pages may be harder to extract. | Preserve usable content and traceability. | Warn when material. |
| Unusual fonts or broken native text layers may reduce extraction quality. | Use best-effort extraction and reduced downstream confidence/support. | Warn when affected. |
| Extremely complex layouts may disrupt reading order or source mapping. | Use best available mapping and suppress false precision. | Warn when material. |
| Handwriting understanding is unsupported. | Do not invent handwriting OCR/meaning; affected content may be unavailable. | Warn when encountered. |
| Very low-resolution scans may not produce useful OCR. | Allow partial/failure behavior rather than fabricated text. | Warn. |
| Chart/graph numerical values are not interpreted as an MVP capability. | Keep visuals viewable; return insufficient/unsupported capability for chart-only values. | Warn/explain when asked. |
| Arbitrary diagrams are not semantically understood. | Keep diagram viewable; do not claim general diagram reasoning. | Explain when relevant. |
| Complex, merged, nested, multi-page, or highly visual tables may fail reconstruction. | Simplify, mark partial, or withhold when unreliable. | Warn. |
| Table extraction may be withheld. | Keep original table visible in canonical PDF. | Warn when structured result unavailable. |
| Statistics/KPI extraction may miss relevant metrics. | Never imply an absent structured metric proves the PDF lacks it. | General disclosure / contextual no-results state. |
| Metric labels may be ambiguous. | Qualify inferred labels or preserve source wording/context. | Warn/qualify where ambiguous. |
| Repeated metrics/evidence may not be perfectly deduplicated. | Preserve context instead of unsafe merging. | Contextual handling. |
| Derived metrics may be unavailable. | Withhold when inputs/evidence are insufficient. | Explain when requested/displayed. |
| Exact source highlighting may be unavailable. | Navigate to correct page and source preview; omit fabricated region. | Explicit limitation. |
| OCR confidence and Evidence Support are different. | Keep signals distinct. | Help/tooltip/explanatory copy. |
| Evidence Support is not factual-truth probability. | Use High/Medium/Low only for claim/evidence support. | Help/tooltip/explanatory copy. |
| High/Medium/Low thresholds require empirical calibration. | Treat thresholds as evaluation/calibration output, not universal probabilities. | Internal validation; user copy avoids probability. |
| AI responses may be limited or withheld. | Return explicit insufficient-evidence behavior. | Per-answer disclosure. |
| Processing/chat timings are validation targets, not SLAs. | Show progress and avoid guarantees. | Product/marketing language. |
| A non-critical capability may fail while others remain usable. | Use Ready with Warnings/Partial and preserve successful capabilities. | Visible warning. |

## 23. Configurability Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-CONFIG-001 | The active maximum PDF page count shall be configurable without requiring product-scope changes. | PRD-DOC-002 |
| SRS-CONFIG-002 | The active maximum upload size shall be configurable without treating approximately 25 MB as a permanent hard-coded public limit. | PRD-DOC-003 |
| SRS-CONFIG-003 | AI generation, embedding, OCR, and evidence-verification implementations shall be replaceable/configurable at the architecture level without changing approved product semantics. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-CONFIG-004 | Evidence Support calibration thresholds or equivalent classification policy shall be configurable to support empirical validation. | PRD-EVID-001, PRD-EVID-003 |
| SRS-CONFIG-005 | Operational timeouts and retry policies should be configurable within safe bounds without changing the distinction between operational failure and insufficient evidence. | PRD-ERR-006 |
| SRS-CONFIG-006 | Feature flags may be used for incomplete or risky internal capabilities, but disabling a Must requirement in the accepted MVP shall require an explicit scope/acceptance decision. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-CONFIG-007 | Retention of temporary processing artifacts shall be configurable or policy-driven separately from the user-facing retain-until-deletion document lifecycle. | PRD-RET-001, PRD-RET-005 |

## 24. Constraints

| Constraint Type | Constraint |
|---|---|
| Product | Single-document, PDF-only, individual-account MVP; no cross-document analysis, teams, external web evidence, or excluded export types. |
| Canonical source | Original uploaded PDF must remain unchanged and authoritative. |
| Document limits | Initial maximum 20 pages; file-size limit configuration-controlled with initial target around 25 MB. |
| Language | Arabic and English, including mixed Arabic/English, are first-class supported scenarios. |
| Hosting | MVP must be deployable on the user's existing VPS; no selectable regions or multi-region deployment. |
| Privacy | Strict per-user isolation; content minimization for external processing; no unnecessary sensitive logging. |
| Evidence | Grounded document-only answers; unsupported claims withheld; Evidence Support is not truth probability. |
| Visual understanding | No MVP commitment to chart-number extraction, arbitrary diagram reasoning, or handwriting understanding. |
| Architecture | This SRS must remain implementation-neutral; provider/framework/topology selections are deferred. |
| Performance | PRD times are validation targets, not SLAs. |
| Project deliverables | Representative evaluation PDFs, documented validation results, source repository, operating/deployment documentation, and honest portfolio/case-study material remain Stage 02 obligations. |

## 25. Assumptions

| ID | Assumption | Impact if False |
|---|---|---|
| A1 | The initial 20-page and ~25 MB limits are sufficient to demonstrate the product's core value. | The MVP document boundary may need a recorded scope change. |
| A2 | Representative professional native PDFs within the limits can be processed usefully. | Extraction scope or acceptance criteria may need revision before release acceptance. |
| A3 | Representative scanned PDFs are sufficiently legible for OCR to produce useful text and coordinates. | Scanned-document usefulness and citation precision will fall. |
| A4 | Arabic, English, and mixed-language OCR/analysis can reach useful quality on representative samples. | A core MVP differentiator would be weakened and require remediation. |
| A5 | Table reconstruction is useful when unreliable structures are withheld. | Table acceptance may need to narrow further. |
| A6 | High/Medium/Low Evidence Support can be empirically calibrated to be meaningful. | The indicator may require redesign before being positioned as a differentiator. |
| A7 | OCR, retrieval, generation, and verification can operate at acceptable cost for the intended direction. | Provider choices, processing policy, or future commercial model may need change. |
| A8 | Users have legal/organizational permission to upload documents they process. | Use may create legal/privacy risk outside intended assumptions. |
| A9 | Users have network access to the web app and permitted external processing dependencies. | Offline use will not work; offline behavior is not in scope. |
| A10 | External processing is permissible for a user's document under disclosed provider/privacy configuration where used. | Some documents may be unsuitable until alternative privacy/deployment behavior exists. |
| A11 | The existing VPS can support the initial validation workload after benchmarking. | Hosting capacity or technical design may require revision without changing the product boundary. |
| A12 | Reliable source coordinates can be produced for a meaningful portion of representative native/OCR content. | Exact highlighting would be available less often, weakening a core differentiator. |

## 26. Dependencies

| Dependency | Why Required | SRS Boundary |
|---|---|---|
| Existing VPS hosting environment | MVP must be deployable and validated on the already-owned environment. | Exact topology/capacity tuning remains Stage 05/06. |
| Persistent structured-data storage | Required for ownership, history, provenance, states, conversations, and deletion semantics. | Technology unresolved. |
| Persistent file/object storage | Required for canonical PDFs and optional derivatives. | Technology unresolved. |
| PDF parsing capability | Required for native extraction and source mapping. | Library/stack unresolved. |
| PDF rendering capability | Required for canonical viewing, navigation, and highlighting. | Library/stack unresolved. |
| OCR capability supporting Arabic and English | Required for scanned/mixed PDFs. | Engine/provider unresolved. |
| AI generation capability | Required for overview and grounded Q&A. | Model/provider unresolved. |
| Embedding capability | Required for semantic retrieval. | Model/provider unresolved. |
| Vector retrieval capability | Required for document-scoped evidence retrieval. | Engine/index strategy unresolved. |
| Evidence-verification / structured decision capability | Required for claim/evidence assessment and Evidence Support. | JEV/other implementation unresolved. |
| Spreadsheet export capability | Required for CSV/Excel statistics export. | Library unresolved. |
| Representative native/scanned/mixed PDFs | Required for system and AI validation. | Evaluation corpus design must be completed. |
| Representative Arabic/English/mixed PDFs | Required for bilingual validation. | Evaluation corpus design must be completed. |
| Claim/evidence evaluation data | Required for support calibration. | Thresholds remain empirical. |
| External-provider privacy controls where used | Needed for minimization, retention, and training-use configuration. | Depends on selected provider capabilities. |

## 27. Verification Strategy

| Category | Verification Method | Representative Verification Focus |
|---|---|---|
| Authentication / isolation | Functional, integration, security testing | Cross-account identifier manipulation; invalid session; logout; denied export/citation/document access. |
| Upload / limits / protected PDFs | Functional and negative testing | Valid/invalid format; 20/21 pages; active size limit; corrupt/zero-page; valid/invalid password. |
| Native extraction / source mapping | Document corpus evaluation + manual visual verification | Page mapping, reading order, native coordinates, degraded text-layer warnings. |
| OCR / mixed documents | Corpus evaluation + integration testing | Arabic/English/mixed OCR; page/region selective OCR; rotations; partial OCR; confidence propagation. |
| Normalized representation / provenance | Integration/data integrity testing | Trace derived results through source spans/pages to original PDF. |
| Statistics / derived metrics | Corpus evaluation + functional testing | Context, units, provenance, conflicts, ambiguity, extracted-vs-derived, partial results. |
| Tables / visuals | Corpus evaluation + manual visual verification | Reliable table reconstruction; withholding complex tables; chart-only number refusal. |
| Retrieval / grounded chat | AI evaluation + integration testing | Document scope, relevant evidence, no external evidence, conflict handling, insufficient evidence. |
| Citations / highlighting | Functional + manual visual verification | Claim association, page correctness, preview correspondence, native/OCR regions, multi-region/fallback. |
| Evidence Support | AI evaluation + calibration testing | High/Medium/Low semantics, Unsupported separation, wording consistency, no truth-probability framing. |
| Export | Functional/integration testing | CSV/Excel, Unicode Arabic, provenance, partial indicators, failure recovery, formula-injection safety. |
| Deletion / retention | Integration/security testing | Ownership check; deletion graph; vector invalidation; inaccessible routes; temp cleanup. |
| Security / privacy | Security review + penetration/negative testing | Transport/storage protection, untrusted PDF behavior, secrets/logging, external-provider configuration. |
| Performance / scale | Performance testing | Native 30–60 s target, OCR-heavy 2–3 min target, chat ~5–10 s target, ~10 active-user scenario. |
| Reliability / recovery | Fault-injection/integration testing | Worker/service interruption, retries, state recovery, duplicate prevention, partial-success preservation. |
| Localization / responsive UX | Functional/manual testing | Arabic RTL, mixed text, small viewports, keyboard controls, citation navigation on mobile. |
| Observability / auditability | Integration inspection | Event outcomes, correlation, no sensitive payload requirements. |

## 28. AI Evaluation Requirements

| SRS ID | Requirement | PRD source(s) |
|---|---|---|
| SRS-AIEVAL-001 | The project shall maintain a representative evaluation corpus containing native, scanned, and mixed native/scanned PDFs within the approved document limits. | Stage 03 scope / SRS cross-cutting derivation |
| SRS-AIEVAL-002 | The evaluation corpus shall include representative Arabic, English, and mixed Arabic/English content. | PRD-LANG-001, PRD-LANG-002 |
| SRS-AIEVAL-003 | Retrieval quality shall be evaluated using document questions with known relevant evidence and source locations. | PRD-CHAT-004, PRD-CITE-001 |
| SRS-AIEVAL-004 | Grounded-answer evaluation shall measure whether factual claims are supported by the current document and whether unsupported answers are withheld. | PRD-GROUND-001, PRD-GROUND-005 |
| SRS-AIEVAL-005 | Citation evaluation shall verify source-page correctness, source-preview correspondence, and exact-region correctness when highlighting is expected. | PRD-CITE-002, PRD-HL-001 |
| SRS-AIEVAL-006 | Evidence Support evaluation shall assess whether High, Medium, and Low classifications meaningfully reflect claim/evidence support and shall treat Unsupported as a separate outcome. | PRD-EVID-001, PRD-EVID-005 |
| SRS-AIEVAL-007 | Evidence Support evaluation shall explicitly confirm that user-facing classifications are not calibrated or described as factual-truth probabilities. | PRD-EVID-003 |
| SRS-AIEVAL-008 | The OCR-to-answer pipeline shall be evaluated end-to-end on representative scanned and mixed documents, including the effect of OCR quality on claims and highlighting. | PRD-OCR-005, PRD-GROUND-004 |
| SRS-AIEVAL-009 | Statistics extraction shall be evaluated for useful discovery, provenance correctness, extracted-versus-derived classification, ambiguity handling, and non-exhaustive disclosure. | PRD-STAT-001, PRD-STAT-003, PRD-STAT-007 |
| SRS-AIEVAL-010 | Table extraction shall be evaluated on clear and difficult representative tables to confirm that unreliable structures are withheld or qualified rather than confidently misrepresented. | PRD-TABLE-001, PRD-TABLE-003 |
| SRS-AIEVAL-011 | Performance evaluation shall record native processing, OCR-heavy processing, chat response, and approximately 10-active-user scenarios against the PRD validation targets. | PRD-PERF-002, PRD-PERF-003, PRD-PERF-004, PRD-PERF-005 |
| SRS-AIEVAL-012 | Exact metric definitions and numeric acceptance thresholds not fixed by the PRD shall be selected during Wayfinder/Technical Design and documented before release validation. | Stage 03 scope / SRS cross-cutting derivation |

Exact metrics, dataset sizes, acceptance thresholds, and scoring procedures not already fixed by the PRD remain Stage 05/06 evaluation-design decisions. The evaluation plan must be defined before release acceptance.

## 29. Requirements Traceability Matrix

Every mandatory and recommended PRD requirement has a direct SRS mapping below. Additional cross-cutting requirements in this SRS may map to the same PRD behaviors but are omitted from this matrix for readability.

| PRD Requirement | Direct SRS Requirement | Priority |
|---|---|---|
| PRD-AUTH-001 | SRS-AUTH-001 | Must |
| PRD-AUTH-002 | SRS-AUTH-002 | Must |
| PRD-AUTH-003 | SRS-AUTH-003 | Must |
| PRD-AUTH-004 | SRS-AUTH-004 | Must |
| PRD-AUTH-005 | SRS-AUTH-005 | Must |
| PRD-CHAT-001 | SRS-CHAT-001 | Must |
| PRD-CHAT-002 | SRS-CHAT-002 | Must |
| PRD-CHAT-003 | SRS-CHAT-003 | Must |
| PRD-CHAT-004 | SRS-CHAT-004 | Must |
| PRD-CHAT-005 | SRS-CHAT-005 | Must |
| PRD-CHAT-006 | SRS-CHAT-006 | Must |
| PRD-CHAT-007 | SRS-CHAT-007 | Must |
| PRD-CITE-001 | SRS-CITE-001 | Must |
| PRD-CITE-002 | SRS-CITE-002 | Must |
| PRD-CITE-003 | SRS-CITE-003 | Must |
| PRD-CITE-004 | SRS-CITE-004 | Should |
| PRD-CITE-005 | SRS-CITE-005 | Must |
| PRD-CITE-006 | SRS-CITE-006 | Must |
| PRD-CITE-007 | SRS-CITE-007 | Must |
| PRD-DOC-001 | SRS-UPLOAD-001 | Must |
| PRD-DOC-002 | SRS-UPLOAD-002 | Must |
| PRD-DOC-003 | SRS-UPLOAD-003 | Must |
| PRD-DOC-004 | SRS-UPLOAD-004 | Must |
| PRD-DOC-005 | SRS-UPLOAD-005 | Must |
| PRD-DOC-006 | SRS-UPLOAD-006 | Must |
| PRD-DOC-007 | SRS-UPLOAD-007 | Must |
| PRD-ERR-001 | SRS-ERR-001 | Must |
| PRD-ERR-002 | SRS-ERR-002 | Must |
| PRD-ERR-003 | SRS-ERR-003 | Must |
| PRD-ERR-004 | SRS-ERR-004 | Must |
| PRD-ERR-005 | SRS-ERR-005 | Must |
| PRD-ERR-006 | SRS-ERR-006 | Must |
| PRD-ERR-007 | SRS-ERR-007 | Must |
| PRD-ERR-008 | SRS-ERR-008 | Must |
| PRD-ERR-009 | SRS-ERR-009 | Must |
| PRD-EVID-001 | SRS-EVID-001 | Must |
| PRD-EVID-002 | SRS-EVID-002 | Must |
| PRD-EVID-003 | SRS-EVID-003 | Must |
| PRD-EVID-004 | SRS-EVID-004 | Must |
| PRD-EVID-005 | SRS-EVID-005 | Must |
| PRD-EXPORT-001 | SRS-EXPORT-001 | Must |
| PRD-EXPORT-002 | SRS-EXPORT-002 | Must |
| PRD-EXPORT-003 | SRS-EXPORT-003 | Must |
| PRD-EXPORT-004 | SRS-EXPORT-004 | Must |
| PRD-EXPORT-005 | SRS-EXPORT-005 | Must |
| PRD-GROUND-001 | SRS-RAG-001 | Must |
| PRD-GROUND-002 | SRS-RAG-002 | Must |
| PRD-GROUND-003 | SRS-RAG-003 | Must |
| PRD-GROUND-004 | SRS-RAG-004 | Must |
| PRD-GROUND-005 | SRS-RAG-005 | Must |
| PRD-GROUND-006 | SRS-RAG-006 | Must |
| PRD-GROUND-007 | SRS-RAG-007 | Must |
| PRD-HIST-001 | SRS-DOC-001 | Must |
| PRD-HIST-002 | SRS-DOC-002 | Must |
| PRD-HIST-003 | SRS-DOC-003 | Must |
| PRD-HIST-004 | SRS-DOC-004 | Must |
| PRD-HIST-005 | SRS-DOC-005 | Must |
| PRD-HL-001 | SRS-HL-001 | Must |
| PRD-HL-002 | SRS-HL-002 | Must |
| PRD-HL-003 | SRS-HL-003 | Must |
| PRD-HL-004 | SRS-HL-004 | Should |
| PRD-HL-005 | SRS-HL-005 | Must |
| PRD-LANG-001 | SRS-LANG-001 | Must |
| PRD-LANG-002 | SRS-LANG-002 | Must |
| PRD-LANG-003 | SRS-LANG-003 | Must |
| PRD-LANG-004 | SRS-LANG-004 | Should |
| PRD-LANG-005 | SRS-LANG-005 | Must |
| PRD-LANG-006 | SRS-LANG-006 | Must |
| PRD-NATIVE-001 | SRS-PARSE-001 | Must |
| PRD-NATIVE-002 | SRS-PARSE-002 | Must |
| PRD-NATIVE-003 | SRS-PARSE-003 | Must |
| PRD-NATIVE-004 | SRS-PARSE-004 | Must |
| PRD-OBS-001 | SRS-OBS-001 | Should |
| PRD-OBS-002 | SRS-OBS-002 | Should |
| PRD-OCR-001 | SRS-OCR-001 | Must |
| PRD-OCR-002 | SRS-OCR-002 | Must |
| PRD-OCR-003 | SRS-OCR-003 | Must |
| PRD-OCR-004 | SRS-OCR-004 | Must |
| PRD-OCR-005 | SRS-OCR-005 | Must |
| PRD-OCR-006 | SRS-OCR-006 | Must |
| PRD-OCR-007 | SRS-OCR-007 | Must |
| PRD-OCR-008 | SRS-OCR-008 | Must |
| PRD-PERF-001 | SRS-PERF-001 | Must |
| PRD-PERF-002 | SRS-PERF-002 | Should |
| PRD-PERF-003 | SRS-PERF-003 | Should |
| PRD-PERF-004 | SRS-PERF-004 | Should |
| PRD-PERF-005 | SRS-PERF-005 | Should |
| PRD-PERF-006 | SRS-PERF-006 | Must |
| PRD-PERF-007 | SRS-PERF-007 | Must |
| PRD-PERF-008 | SRS-PERF-008 | Must |
| PRD-PROC-001 | SRS-PROC-001 | Must |
| PRD-PROC-002 | SRS-PROC-002 | Must |
| PRD-PROC-003 | SRS-PROC-003 | Must |
| PRD-PROC-004 | SRS-PROC-004 | Must |
| PRD-PROC-005 | SRS-PROC-005 | Must |
| PRD-PROC-006 | SRS-PROC-006 | Must |
| PRD-PROC-007 | SRS-PROC-007 | Must |
| PRD-RET-001 | SRS-DATA-101 | Must |
| PRD-RET-002 | SRS-DATA-102 | Must |
| PRD-RET-003 | SRS-DATA-103 | Must |
| PRD-RET-004 | SRS-DATA-104 | Must |
| PRD-RET-005 | SRS-DATA-105 | Must |
| PRD-SEARCH-001 | SRS-SEARCH-001 | Must |
| PRD-SEARCH-002 | SRS-SEARCH-002 | Must |
| PRD-SEARCH-003 | SRS-SEARCH-003 | Must |
| PRD-SEARCH-004 | SRS-SEARCH-004 | Must |
| PRD-SEC-001 | SRS-SEC-001 | Must |
| PRD-SEC-002 | SRS-SEC-002 | Must |
| PRD-SEC-003 | SRS-SEC-003 | Must |
| PRD-SEC-004 | SRS-SEC-004 | Must |
| PRD-SEC-005 | SRS-SEC-005 | Must |
| PRD-SEC-006 | SRS-SEC-006 | Must |
| PRD-SEC-007 | SRS-SEC-007 | Should |
| PRD-SEC-008 | SRS-SEC-008 | Must |
| PRD-SPLIT-001 | SRS-UX-001 | Must |
| PRD-SPLIT-002 | SRS-UX-002 | Must |
| PRD-STAT-001 | SRS-STAT-001 | Must |
| PRD-STAT-002 | SRS-STAT-002 | Must |
| PRD-STAT-003 | SRS-STAT-003 | Must |
| PRD-STAT-004 | SRS-STAT-004 | Must |
| PRD-STAT-005 | SRS-STAT-005 | Must |
| PRD-STAT-006 | SRS-STAT-006 | Must |
| PRD-STAT-007 | SRS-STAT-007 | Must |
| PRD-STAT-008 | SRS-STAT-008 | Must |
| PRD-TABLE-001 | SRS-TABLE-001 | Must |
| PRD-TABLE-002 | SRS-TABLE-002 | Must |
| PRD-TABLE-003 | SRS-TABLE-003 | Must |
| PRD-TABLE-004 | SRS-TABLE-004 | Must |
| PRD-TABLE-005 | SRS-TABLE-005 | Must |
| PRD-UX-001 | SRS-UX-101 | Must |
| PRD-UX-002 | SRS-UX-102 | Should |
| PRD-UX-003 | SRS-UX-103 | Must |
| PRD-UX-004 | SRS-UX-104 | Must |
| PRD-UX-005 | SRS-UX-105 | Must |
| PRD-VIEW-001 | SRS-VIEW-001 | Must |
| PRD-VIEW-002 | SRS-VIEW-002 | Must |
| PRD-VIEW-003 | SRS-VIEW-003 | Must |
| PRD-VIEW-004 | SRS-VIEW-004 | Must |
| PRD-VIEW-005 | SRS-VIEW-005 | Must |
| PRD-VIS-001 | SRS-VIS-001 | Must |
| PRD-VIS-002 | SRS-VIS-002 | Must |
| PRD-VIS-003 | SRS-VIS-003 | Must |

**Traceability result:** all 142 PRD requirement IDs have at least one direct SRS requirement mapping. No PRD requirement is blocked from translation.

## 30. Unresolved Technical Decisions

| ID | Decision | Why It Matters | Dependencies | Recommended Investigation |
|---|---|---|---|---|
| TD-001 | Application architecture style | Determines modularity, deployment complexity, scaling, and fault boundaries. | All functional/NFR requirements | Architecture decision |
| TD-002 | Frontend framework and supported browser/version matrix | Affects PDF viewer integration, RTL/responsive behavior, maintainability, and QA scope. | SRS-VIEW-*, SRS-UX-*, SRS-LANG-* | Prototype + architecture decision |
| TD-003 | Backend framework/runtime composition | Affects processing orchestration, auth, APIs, maintainability, and VPS resource use. | Most server-side requirements | Architecture decision |
| TD-004 | Need for a separate Python/AI-processing service | Affects library availability, process isolation, operational complexity, and resource usage. | PDF/OCR/AI/table pipelines | Prototype + benchmark |
| TD-005 | Native PDF parsing/extraction stack | Affects reading order, coordinates, source mapping, and Arabic/native quality. | SRS-PARSE-*, SRS-NORM-* | Benchmark |
| TD-006 | OCR engine/provider | Affects Arabic/English quality, coordinates, confidence, privacy, speed, and cost. | SRS-OCR-*, SRS-PRIV-* | Benchmark + security review |
| TD-007 | Table extraction/reconstruction approach | Affects reliable structured table coverage and provenance. | SRS-TABLE-* | Benchmark |
| TD-008 | Embedding model/provider | Affects multilingual retrieval quality, cost, privacy, and reprocessing. | SRS-EMB-* | Benchmark |
| TD-009 | Vector storage/retrieval engine and indexing approach | Affects retrieval latency, isolation, persistence, and VPS footprint. | SRS-RAG-111..117 | Architecture decision + benchmark |
| TD-010 | LLM/provider for overview and Q&A | Affects grounding quality, multilingual behavior, latency, cost, and privacy. | SRS-RAG-*, SRS-CHAT-* | Benchmark + security review |
| TD-011 | Evidence-verification implementation / JEV integration | Affects claim/evidence classification quality and explainability. | SRS-EVID-* | Research + prototype + benchmark |
| TD-012 | Chunking strategy | Affects retrieval quality, citation fidelity, and reprocessing. | SRS-RAG-101..106 | Prototype + benchmark |
| TD-013 | Retrieval and reranking strategy | Affects evidence recall/precision, conflict handling, and latency. | SRS-RAG-111..117 | Prototype + benchmark |
| TD-014 | Claim decomposition and citation-association strategy | Affects statement-level traceability and minimal evidence sets. | SRS-CITE-* | Prototype + evaluation |
| TD-015 | Evidence Support threshold calibration | Affects High/Medium/Low meaningfulness and wording policy. | SRS-EVID-104, SRS-AIEVAL-006 | Benchmark / evaluation design |
| TD-016 | Background processing, queueing, retry, and idempotency mechanism | Affects lifecycle reliability, recovery, and concurrency. | SRS-PROC-*, SRS-REL-* | Architecture decision |
| TD-017 | Original/derived file-storage implementation | Affects canonical preservation, deletion, at-rest protection, and VPS operations. | SRS-DOC-101..104, SRS-DATA-* | Architecture decision + security review |
| TD-018 | Structured database/persistence technology and logical-to-physical model | Affects ownership, provenance, state consistency, and deletion. | SRS-DATA-* | Architecture decision |
| TD-019 | Authentication/session implementation | Affects session behavior, security, and user isolation. | SRS-AUTH-*, SRS-SEC-* | Security review + architecture decision |
| TD-020 | PDF viewer/highlighting library and coordinate transforms | Affects rendering fidelity, exact highlights, mobile behavior, and RTL-adjacent UI. | SRS-VIEW-*, SRS-HL-* | Prototype |
| TD-021 | Deployment topology on existing VPS | Affects resource isolation, operations, performance, and recovery. | SRS-PERF-*, SRS-SCALE-*, SRS-AVAIL-* | Architecture decision + benchmark |
| TD-022 | Observability/logging/metrics stack | Affects validation, incident diagnosis, privacy-safe telemetry, and VPS footprint. | SRS-OBS-*, SRS-AUDIT-* | Architecture decision |
| TD-023 | External-provider privacy routing and retention/training configuration | Affects confidentiality disclosures and provider risk. | SRS-SEC-107..108, SRS-PRIV-* | Security/privacy review |
| TD-024 | CSV/Excel generation and spreadsheet-safety implementation | Affects Unicode fidelity, interoperability, and formula-injection handling. | SRS-EXPORT-* | Prototype + security review |

These are architecture/technical decisions, not unresolved product requirements. They are intended inputs to Stage 05.

## 31. SRS Acceptance Checklist

| Check | Status |
|---|---|
| Every PRD requirement maps to at least one SRS requirement | Yes — 142/142 direct mappings. |
| Every mandatory requirement is testable | Yes — normative requirements plus carried PRD verification conditions and category-level verification strategy. |
| Original PDFs remain canonical | Yes. |
| Normalized-document requirements preserve source provenance | Yes. |
| Native/scanned handling is explicit | Yes. |
| OCR requirements are explicit | Yes. |
| Arabic/English/mixed-language requirements are explicit | Yes. |
| Statistics requirements remain bounded/non-exhaustive | Yes. |
| Table/chart limitations are preserved | Yes. |
| RAG grounding is explicit | Yes. |
| Insufficient-evidence behavior is explicit | Yes. |
| Citations are traceable | Yes. |
| Evidence Support is distinct from factual-truth probability | Yes. |
| Deletion covers document-specific derived artifacts and retrieval/vector data | Yes. |
| Security/privacy requirements exist | Yes. |
| Observability requirements exist | Yes. |
| AI evaluation requirements exist | Yes. |
| Accepted MVP limitations remain visible | Yes. |
| Architecture choices remain unresolved where appropriate | Yes — Section 30. |
| No product-level blocker remains | Yes. |

## 32. Readiness for Stage 05

### Architecture Decisions Ready for Wayfinder

All 24 technical decisions in Section 30 are ready for explicit research, prototype, benchmark, trade-off, security/privacy, or architecture decision work. The SRS defines the behavioral and technical constraints those decisions must satisfy.

### Decisions Still Blocked

**None at product level.** The approved PRD states that no product-level blocker remains for Stage 04, and this SRS introduces no new product ambiguity. Numeric AI/evaluation thresholds that require empirical calibration are technical/evaluation decisions rather than product blockers.

### Readiness Assessment

PdfMining is **ready for Stage 05 — Wayfinder / Architecture Decisions**, subject to explicit approval of this Stage 04 SRS.

## 33. Recommended Next Stage

# Stage 05 — Wayfinder / Architecture Decisions

After Stage 04 approval, Stage 05 should use the approved Stage 00 Discovery Summary, Stage 01 Product Feature Brief, Stage 02 Product Scope, Stage 03 PRD, and this Stage 04 SRS. It should resolve major technical uncertainty through explicit decision tickets using research, prototypes, benchmarks, trade-off analysis, security/privacy review, and AI engineering evaluation.

Stage 05 should **not** immediately begin implementation. Its output should provide the decision foundation for **Stage 06 — Technical Design / Architecture Specification**.

---

## Stage 04 Status Summary

- **Completion status:** Complete — draft for explicit approval.
- **Total SRS requirements:** 364
- **Unresolved product-level decisions:** 0
- **Unresolved architecture/technical decisions:** 24
- **Ready for Stage 05:** Yes, after explicit Stage 04 approval.
- **Do not proceed to Stage 05 until Stage 04 is explicitly approved.**