# PdfMining — Product Requirements Document (PRD)

## 1. Document Control

| Field | Value |
|---|---|
| Product | PdfMining |
| Document | Product Requirements Document |
| Version | v0.1 |
| Status | Draft for approval |
| Primary Source | Stage 02 — PdfMining Project / Product Scope v0.1 |
| Supporting Sources | Stage 01 — Product / Feature Brief; Stage 00 — Product Discovery Decision Summary, where available |
| Scope Baseline | Approved PdfMining MVP |
| Next Stage After Approval | Stage 04 — Software Requirements Specification (SRS) |

This PRD elaborates the approved Stage 02 boundary. It does not authorize material scope expansion or removal.

---

## 2. Purpose

This PRD defines **what the PdfMining MVP must do from the user's perspective**. It translates the approved project/product scope into observable product behavior, user journeys, states, edge cases, errors, recovery behavior, AI-grounding behavior, citations, Evidence Support behavior, and acceptance criteria.

The later **Stage 04 — SRS** should derive precise functional and non-functional system requirements from this document. Later architecture and Technical Design stages may decide implementation mechanisms, but they must preserve the product behavior and scope boundaries defined here.

This PRD intentionally does **not** define database schemas, APIs, classes, services, queues, OCR/LLM providers, embedding models, RAG algorithms, verification algorithms, deployment topology, or source-code structure.

Stage 02 also establishes non-user-facing project deliverables such as deployment on the existing VPS, representative evaluation PDFs, documented validation results, a source repository, operating/deployment documentation, and honest portfolio/case-study material. Those remain binding Stage 02 project obligations, but they are not converted here into user-facing product features. Product-relevant validation obligations are reflected in the acceptance and performance sections below.

---

## 3. Product Summary

PdfMining is an evidence-first web application for **individual professionals working with information-heavy PDFs**. A user signs in, uploads a supported PDF, observes processing, reviews a concise document overview, explores structured statistics/KPIs and reliable table reconstructions, asks grounded questions, inspects statement-level evidence and Evidence Support, navigates to the original source page and exact highlighted region when coordinates are reliable, exports structured statistics, and can later return to or delete the document.

The MVP supports representative **native, scanned, and mixed native/scanned PDFs** in **Arabic, English, and mixed Arabic/English**. The original uploaded PDF remains unchanged and canonical. The primary differentiators are source traceability, document-only grounded AI, claim/evidence verification, visible Evidence Support, and exact source navigation when reliable.

The MVP is deliberately bounded. It does not promise universal PDF understanding, exhaustive metric discovery, perfect table reconstruction, chart-number interpretation, multi-document research, team collaboration, or unsupported compliance guarantees.

---

## 4. Goals

1. Enable an authenticated individual professional to complete the full PDF investigation workflow without leaving PdfMining.
2. Preserve the original uploaded PDF as the canonical evidence source throughout the document lifecycle.
3. Produce useful analysis for representative native, scanned, and mixed PDFs within the configured MVP boundary.
4. Treat Arabic and English as first-class document and interaction languages, including mixed-language documents.
5. Surface useful quantitative facts and KPIs with enough context and provenance to verify them.
6. Reconstruct tables only when sufficiently reliable and visibly withhold or qualify unreliable structured output.
7. Provide single-document conversational Q&A grounded only in the uploaded document.
8. Associate document-derived factual claims with inspectable source evidence and clear Evidence Support.
9. Let users navigate from evidence citations to the correct original PDF page and exact source region when reliable coordinates exist.
10. Degrade gracefully when OCR, extraction, table reconstruction, AI analysis, or another non-critical capability partially fails.
11. Preserve private document history until explicit user deletion and make deletion remove document-specific derived data.
12. Export structured statistics to CSV and Excel while retaining provenance and extracted-versus-derived distinctions.

---

## 5. Non-Goals

The following are explicitly **not** MVP goals:

- non-PDF ingestion such as DOCX, PPTX, spreadsheets, or standalone image uploads;
- multi-document chat, document collections, cross-document search, or cross-document analytics;
- team/organization accounts, shared workspaces, collaborative annotations, organization roles, enterprise SSO, or administration;
- large-document support beyond the configured MVP boundary;
- handwriting understanding;
- numerical interpretation of charts/graphs or arbitrary diagram understanding;
- guaranteed discovery of every statistic, KPI, number, or complete document extraction;
- perfect reconstruction of complex, merged, nested, highly visual, or multi-page tables;
- full BI/dashboard functionality;
- external web search or general model knowledge presented as document evidence;
- editing the original PDF or replacing it with a regenerated canonical PDF;
- password cracking or encryption bypass;
- selectable hosting regions, multi-region deployment, or configurable regional data residency;
- unsupported compliance/certification claims;
- billing/subscriptions;
- native mobile apps, browser extensions, desktop native apps, or a public API;
- chat transcript export, standalone citation export, or arbitrary full-table export.

---

## 6. User Types

### 6.1 Primary User — Individual Professional

**Description:** An authenticated individual working with information-heavy professional PDFs such as business reports, financial or operational reports, tenders/specifications, and research/report-style documents.

**Primary goals:**
- privately upload and retain PDFs;
- understand a document quickly through an overview;
- find useful statistics/KPIs and reliable structured tables;
- ask questions and follow-up questions;
- verify claims against source evidence;
- navigate directly to evidence in the original PDF;
- export structured statistics with provenance;
- return to prior work or delete it.

**Relevant workflows:** J1 through J9 in this PRD.

**Product-level permissions and boundaries:**
- may access only documents and derived data owned by the authenticated account;
- may upload, inspect, query, export statistics from, revisit, and delete owned documents;
- cannot access another user's documents or derived data;
- has no team, organization, shared-workspace, or collaborative-role behavior in the MVP.

### 6.2 Secondary Users

No separate secondary MVP audience is approved.

Business teams, organizations, administrators, and collaborative reviewers are post-MVP product directions and are not defined by this PRD.

---

## 7. Core User Journeys

### Journey J1 — Account Access

**Preconditions:** The user has access to the PdfMining web application.

**Trigger:** The user wants to access private PdfMining features.

**Main flow:**
1. The user creates an individual account or signs in to an existing account.
2. PdfMining authenticates the user.
3. The user enters the private document history/workspace.
4. Only documents and analysis owned by that account are visible.

**Alternate flow:** If an existing authenticated session is valid, the user proceeds directly to private content.

**Failure states:** Invalid credentials, invalid/expired session, unavailable authentication service, or unauthorized access attempt.

**Successful outcome:** The user has authenticated access to their own private PdfMining data only.

### Journey J2 — Upload and Process a Native PDF

**Preconditions:** The user is authenticated and has a native/text PDF within configured limits.

**Trigger:** The user selects a PDF for upload.

**Main flow:**
1. PdfMining validates file type, configured file size, and page count.
2. If validation passes, upload begins and progress/state is visible.
3. PdfMining processes native text and useful document structure while preserving the original PDF.
4. The user sees processing states through extraction and analysis.
5. PdfMining creates a concise overview and available analysis.
6. The document becomes Ready, or Ready with warnings if non-critical limitations exist.

**Alternate flow:** A password-protected PDF prompts for a password; a valid password allows processing.

**Failure states:** Non-PDF input, over-limit document, corrupted/unreadable PDF, invalid password, unusable native text layer, processing failure.

**Successful outcome:** The user can inspect the original PDF, overview, available statistics/tables, chat, and evidence with native source mapping where reliable.

### Journey J3 — Upload and Process a Scanned PDF

**Preconditions:** The user is authenticated and has a scanned or image-based PDF within configured limits.

**Trigger:** The user uploads the PDF.

**Main flow:**
1. PdfMining validates and uploads the PDF.
2. Scanned pages/regions requiring OCR are identified.
3. OCR is visibly performed for the required content.
4. OCR text, page association, reading order, source coordinates, and confidence are retained where available.
5. Analysis proceeds using reliable OCR output.
6. OCR quality limitations are surfaced.
7. The document becomes Ready or Ready with warnings/partial results.

**Alternate flow:** For a mixed native/scanned PDF, native pages use native extraction and scanned pages/regions use OCR selectively.

**Failure states:** Very poor scan quality, unreadable region, OCR failure, unsupported handwriting, malformed PDF, processing failure.

**Successful outcome:** Reliable OCR-derived content remains usable and traceable to the original scanned pages; unreadable content is not fabricated.

### Journey J4 — Explore Extracted Statistics

**Preconditions:** The document has reached a usable analysis state.

**Trigger:** The user opens the statistics/KPI area.

**Main flow:**
1. PdfMining shows automatically discovered useful quantitative facts/KPIs.
2. Each metric presents value, unit where applicable, context, source page, and provenance.
3. The UI distinguishes extracted values from derived metrics.
4. The user searches and filters the structured statistics.
5. The user opens source evidence for a metric.
6. Conflicting/repeated values remain distinguishable where context differs.

**Alternate flow:** A metric from a reliable reconstructed table appears through the same statistics/provenance model.

**Failure states:** No statistics found, ambiguous metric label, partial extraction, conflicting values, insufficient evidence for a derived metric.

**Successful outcome:** The user can investigate useful metrics without the product implying exhaustive numeric discovery.

### Journey J5 — Ask Questions About a Document

**Preconditions:** The document is sufficiently processed for grounded Q&A.

**Trigger:** The user asks a question in Arabic, English, or understandable mixed language.

**Main flow:**
1. The question is associated with one document.
2. PdfMining finds relevant document evidence.
3. The answer is generated from document evidence only.
4. Contextual follow-up questions may use conversation history to understand intent.
5. Document-derived factual claims receive citations where appropriate.
6. Evidence Support is shown for supported claim/evidence relationships.

**Alternate flow:** The answer synthesizes evidence from multiple pages or source passages in the same document.

**Failure states:** No relevant evidence, conflicting evidence, poor OCR/extraction, AI/verification failure, timeout, question requiring outside knowledge.

**Successful outcome:** The user receives a grounded answer or an explicit limitation/insufficient-evidence response.

### Journey J6 — Inspect Citations and Evidence Support

**Preconditions:** A displayed answer, statistic, or derived result has supporting evidence.

**Trigger:** The user inspects a citation or Evidence Support indicator.

**Main flow:**
1. The user can see which claim the citation supports.
2. The citation shows the page and a source-text preview.
3. One or multiple evidence passages are available as required.
4. Evidence Support is shown as High, Medium, or Low where verification is available.
5. Explanatory UI makes clear that Evidence Support measures evidence-to-claim support, not factual-truth probability.

**Alternate flow:** Medium/Low support is shown with qualified answer wording.

**Failure states:** Unsupported claim, missing reliable coordinates, degraded OCR/source mapping, verification failure.

**Successful outcome:** The user can understand both the evidence and the strength of its support for the specific claim.

### Journey J7 — Navigate to Exact Source

**Preconditions:** A citation identifies a valid source page; exact coordinates may or may not be reliable.

**Trigger:** The user activates the citation.

**Main flow:**
1. The original PDF viewer navigates to the cited page.
2. If reliable coordinates exist, the exact source region is highlighted in yellow.
3. Multi-line or multi-region evidence highlights the mapped regions required for the citation.
4. The user can inspect surrounding source context.

**Alternate flow:** If exact coordinates are unreliable, PdfMining navigates to the correct page and presents the source preview without a fabricated exact highlight.

**Failure states:** Source mapping unavailable or document has become inaccessible/deleted.

**Successful outcome:** The user reaches the correct original evidence with the highest reliable location precision available.

### Journey J8 — Export Structured Results

**Preconditions:** The document has one or more structured statistics.

**Trigger:** The user chooses CSV or Excel export.

**Main flow:**
1. The user selects an approved export format.
2. PdfMining generates structured statistics including document identification, metric/value/context, page, provenance, and extracted-versus-derived status.
3. Relevant uncertainty/partial-result information is preserved when available.
4. The export completes and becomes available to the user.

**Alternate flow:** Statistics sourced from reliable table content may be included when they meet structured-statistic criteria.

**Failure states:** Export generation failure or temporary unavailability.

**Successful outcome:** The user receives a traceable CSV/Excel statistics export without unsupported export types being implied.

### Journey J9 — Return to or Delete a Previous Document

**Preconditions:** The user previously uploaded a document and has not deleted it.

**Trigger:** The user returns to document history or chooses to delete a document.

**Main flow — Return:**
1. The user opens private document history.
2. The user selects a prior document.
3. PdfMining restores the original PDF and persisted document-associated analysis, conversations, citations, and warnings.

**Main flow — Delete:**
1. The user chooses delete for a selected document.
2. PdfMining warns that the original PDF and document-specific analysis/conversation data will be removed.
3. The user confirms.
4. The document disappears from history and is no longer accessible.

**Alternate flow:** A document still processing can be reopened to inspect its current state.

**Failure states:** Unauthorized access, deletion failure, already-deleted document, invalid session.

**Successful outcome:** The user can reliably resume prior private work or permanently remove the selected document from product access.

---

## 8. Functional Requirements

All priorities are product priorities: **Must** is required for MVP acceptance; **Should** is expected unless validation shows a justified reason to defer without breaking the approved scope. Deferred and out-of-scope capabilities are not labeled Could.


### 8.1 Authentication and User Access

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-AUTH-001** | PdfMining must require an authenticated individual account before a user can access private documents or document-derived data. | The MVP is a private, single-user account experience. | **Must** | 1. An unauthenticated visitor cannot open a user's document workspace or history.<br>2. After successful authentication, the user can access only content owned by that account. |
| **PRD-AUTH-002** | A new individual user must be able to create an account and then sign in to PdfMining. | A usable MVP requires a path from first visit to authenticated use. | **Must** | 1. A user can complete account creation using the product's supported account fields.<br>2. After account creation, the user can enter the authenticated product experience.<br>3. Invalid or incomplete registration input produces a clear corrective message without creating a usable account. |
| **PRD-AUTH-003** | An existing user must be able to sign in and sign out. | Users need explicit control over access to confidential document data. | **Must** | 1. Valid credentials grant access to the user's private history.<br>2. Invalid credentials produce a clear authentication error without revealing protected content.<br>3. After logout, protected pages require authentication again. |
| **PRD-AUTH-004** | When an authenticated session is no longer valid, the product must require re-authentication and must not expose protected document content. | Expired or invalid sessions are a normal user-visible state. | **Must** | 1. A protected action with an invalid session redirects or otherwise returns the user to an authentication flow.<br>2. Unsaved user input should be preserved where practical, but protected data is not shown until authentication succeeds. |
| **PRD-AUTH-005** | PdfMining must enforce strict per-user access isolation for documents, history, conversations, statistics, citations, and other document-derived artifacts. | Per-user isolation is an explicit MVP contract. | **Must** | 1. A user cannot access another user's document by navigation, identifier manipulation, history view, export, or citation link.<br>2. Access-denied attempts do not reveal the protected document's content or metadata. |


### 8.2 Document Upload

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-DOC-001** | The upload experience must accept PDF files only. | PDF is the sole MVP input format. | **Must** | 1. A valid supported PDF can be selected for upload.<br>2. A non-PDF file is rejected before processing with a message that PDF is the supported format. |
| **PRD-DOC-002** | The product must validate the configured page limit and reject documents that exceed it; the initial MVP maximum is 20 pages. | Large-document support beyond the configured boundary is deferred. | **Must** | 1. A PDF of 20 pages or fewer passes the page-count boundary when other validations pass.<br>2. A PDF above the configured maximum is not processed and the user sees the current maximum. |
| **PRD-DOC-003** | The product must validate the configured file-size limit; the initial MVP target is approximately 25 MB and remains configuration-controlled. | The scope defines an initial size boundary without fixing a permanent public limit. | **Must** | 1. A file over the active configured size is rejected before expensive processing.<br>2. The error communicates the active maximum allowed size rather than implying a universal 25 MB guarantee. |
| **PRD-DOC-004** | For a password-protected PDF, the product must allow the user to supply a password and process the document only when the password is valid. | Password-protected PDFs are conditionally supported; bypass is excluded. | **Must** | 1. A protected PDF prompts for a password rather than being silently rejected.<br>2. A valid password allows processing to continue.<br>3. An invalid or missing password produces a clear error and does not bypass protection. |
| **PRD-DOC-005** | The user must receive visible upload progress or an equivalent upload-in-progress state until the file is accepted or fails. | Users must be able to distinguish upload from later document processing. | **Must** | 1. During upload, the UI visibly indicates that transfer is in progress.<br>2. Upload success transitions to a processing state; upload failure transitions to a retryable error state where appropriate. |
| **PRD-DOC-006** | Uploading a PDF that is identical to a previously uploaded document must not silently overwrite or alter the earlier document. | Private history must remain predictable even when users upload duplicates. | **Must** | 1. A duplicate upload either creates a separate document record or is explicitly identified before reuse.<br>2. The previous document and its analysis remain unchanged unless the user deletes it. |
| **PRD-DOC-007** | The product must reject empty, unreadable, corrupted, or otherwise unprocessable PDF inputs with a user-visible reason when identifiable. | Unsupported or malformed content must not be presented as successfully processed. | **Must** | 1. A zero-page/empty PDF does not proceed to Ready.<br>2. A corrupted PDF that cannot be parsed ends in a visible failure state with retry/re-upload guidance. |


### 8.3 Document Processing States

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-PROC-001** | Each uploaded document must expose a user-visible processing state that reflects its current progress. | Processing can take tens of seconds or minutes and must not be opaque. | **Must** | 1. The user can distinguish at least Uploaded/Queued, Extracting, OCR when applicable, Analyzing, Ready, Ready with warnings or partial results, and Failed.<br>2. The displayed state updates as the document advances or fails. |
| **PRD-PROC-002** | OCR processing must be shown as a distinct state or progress phase when OCR is required. | Scanned and mixed documents have materially different processing behavior. | **Must** | 1. A scanned page that requires OCR causes the user to see an OCR-related processing indication.<br>2. A purely native PDF is not falsely described as undergoing OCR. |
| **PRD-PROC-003** | The product must preserve usable successful results when a non-critical processing capability fails. | Graceful degradation is an explicit reliability requirement. | **Must** | 1. If one non-critical capability fails, completed capabilities remain accessible.<br>2. The overall document is not labeled fully successful when a known non-critical failure affects output. |
| **PRD-PROC-004** | A document with usable results but known extraction, OCR, table, or analysis limitations must be shown as Ready with warnings or an equivalent partial-success state. | Users must be able to distinguish complete-looking output from known limitations. | **Must** | 1. Known limitations are visible from the document workspace.<br>2. Warnings identify the affected capability or region at a useful level without claiming unavailable precision. |
| **PRD-PROC-005** | A document that cannot produce a usable minimum result must end in a Failed state with a clear user-visible explanation and available recovery action. | Failure must be explicit rather than hidden. | **Must** | 1. Failed documents do not expose fabricated analysis as valid results.<br>2. The user is told whether retry, password correction, or re-upload may resolve the issue. |
| **PRD-PROC-006** | After sufficient processing, PdfMining must provide a concise automatic document overview. | A concise overview is an approved MVP deliverable and first analysis experience. | **Must** | 1. A Ready document presents a concise overview derived from the document.<br>2. The overview remains document-grounded and does not silently add external facts.<br>3. If evidence quality is insufficient for a reliable overview, the product communicates the limitation instead of inventing content. |
| **PRD-PROC-007** | Processing warnings and failures must remain inspectable after processing completes. | Users returning later need the same visibility into quality limitations. | **Must** | 1. Reopening a document preserves its relevant warning/partial-processing indicators.<br>2. A warning is not cleared merely because the user navigates away and returns. |


### 8.4 Native PDF Processing

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-NATIVE-001** | For native/text PDFs, PdfMining must extract usable text and document structure while preserving page association. | Native text is the primary source for analysis where available. | **Must** | 1. Extracted text used in analysis can be associated with its original page.<br>2. Reading order and structure are retained sufficiently for approved statistics, chat, and citation behavior on representative native PDFs. |
| **PRD-NATIVE-002** | Native extracted content must retain source-coordinate relationships where reliable so citations can navigate to and highlight the original PDF. | Exact source navigation is a core differentiator. | **Must** | 1. Eligible native-text citations resolve to the correct page.<br>2. When reliable coordinates exist, the cited source region can be highlighted in the original PDF. |
| **PRD-NATIVE-003** | The original uploaded PDF must remain unchanged and canonical regardless of native extraction or normalized internal processing. | The approved evidence model depends on the original file as source of truth. | **Must** | 1. Opening the viewer shows the original uploaded PDF.<br>2. No generated or normalized derivative replaces the original as the citation authority. |
| **PRD-NATIVE-004** | When unusual fonts, encodings, broken text layers, or complex layouts reduce native extraction quality, the product must expose the resulting limitation where it affects user-visible outputs. | Native PDFs are not guaranteed to extract perfectly. | **Must** | 1. Known degraded extraction is reflected by a warning or reduced downstream support.<br>2. The product does not claim complete extraction when the native text layer is demonstrably unusable. |


### 8.5 Scanned PDF / OCR Processing

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-OCR-001** | PdfMining must detect pages or regions that require OCR and apply OCR selectively rather than treating every document as fully scanned. | Selective OCR is part of the approved mixed-document behavior. | **Must** | 1. Scanned pages receive OCR processing.<br>2. Native pages with usable text are processed without unnecessary whole-page OCR as the product behavior. |
| **PRD-OCR-002** | OCR must support representative Arabic, English, and mixed Arabic/English scanned content within the MVP document boundary. | Arabic and English are first-class MVP languages. | **Must** | 1. Representative Arabic and English scans can yield usable OCR text.<br>2. Mixed-language pages can be processed without being rejected solely for containing both supported languages. |
| **PRD-OCR-003** | OCR output used by the product must retain page association, source coordinates, reading order, and OCR confidence where available. | These attributes enable traceability, highlighting, and visible quality disclosure. | **Must** | 1. OCR-derived citations can identify their source page.<br>2. Where coordinates are reliable, OCR-derived evidence can be highlighted.<br>3. Where OCR confidence is available, poor quality can influence user-visible warnings/support rather than being hidden. |
| **PRD-OCR-004** | Mixed native/scanned PDFs must combine native extraction on usable native pages with OCR on scanned pages or required regions. | Mixed PDFs are an explicit supported scenario. | **Must** | 1. A mixed document can reach a usable Ready or partial-success state.<br>2. Evidence from both native and OCR-derived pages remains traceable to the same original PDF. |
| **PRD-OCR-005** | Poor OCR quality must be disclosed and must reduce downstream confidence/support where it materially affects interpretation. | OCR uncertainty must propagate rather than disappear. | **Must** | 1. Low-quality OCR triggers a visible warning when it affects analysis.<br>2. The product does not present low-quality OCR-derived claims with unjustifiably strong wording or false location precision. |
| **PRD-OCR-006** | Partially successful OCR must remain usable for regions/pages that were read reliably, while failed regions are identified as limited or unavailable. | Graceful partial processing is required. | **Must** | 1. Successful OCR content remains available after another page/region fails.<br>2. The product does not invent text for an unreadable region. |
| **PRD-OCR-007** | Common page rotations must be handled so rotated scanned/native pages are usable where otherwise processable. | Common rotations are explicitly in scope. | **Must** | 1. Representative commonly rotated pages can be processed without requiring the user to modify the source PDF.<br>2. If rotation or image quality still prevents reliable OCR, the limitation is disclosed. |
| **PRD-OCR-008** | A searchable OCR PDF derivative may be created as a convenience artifact, but it must never replace the original PDF or become the citation authority. | The approved derivative policy preserves source truth. | **Must** | 1. Whether or not a searchable derivative exists, citations resolve against the original uploaded PDF.<br>2. Deleting the document also removes any document-specific searchable derivative. |


### 8.6 Document History and Management

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-HIST-001** | Authenticated users must have a private history listing their uploaded documents. | Returning to prior work is an approved MVP workflow. | **Must** | 1. A user can see previously uploaded documents that have not been deleted.<br>2. The list contains only documents owned by the authenticated account. |
| **PRD-HIST-002** | Each history item must show enough metadata to identify the document and its current processing status. | Users need to distinguish documents and incomplete processing. | **Must** | 1. At minimum, the original filename and current state are visible.<br>2. Upload time and page count are shown when available without implying unsupported metadata. |
| **PRD-HIST-003** | A user must be able to reopen a previously processed document and recover its persisted overview, statistics, conversations, citations, and warnings that remain applicable. | Document-associated analysis persists until deletion. | **Must** | 1. Reopening a Ready document restores the document workspace and available analysis.<br>2. Conversation history remains associated with that document until deletion. |
| **PRD-HIST-004** | A user must be able to delete a selected document through an explicit confirmation step. | Deletion is destructive and removes document-specific data. | **Must** | 1. The product clearly identifies the document to be deleted.<br>2. Deletion does not occur until the user confirms the destructive action. |
| **PRD-HIST-005** | After confirmed deletion, the document must disappear from the user's history and its document-specific analysis must no longer be accessible. | Deletion must have complete user-visible semantics. | **Must** | 1. The deleted document cannot be reopened from history, citation links, or saved product routes.<br>2. Subsequent access attempts do not reveal deleted content. |


### 8.7 Statistics and KPI Extraction

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-STAT-001** | PdfMining must automatically surface useful quantitative facts and KPIs that have sufficient semantic context and document provenance. | Structured quantitative investigation is a core MVP capability. | **Must** | 1. Representative documents produce structured metrics when clear quantitative facts exist.<br>2. The product does not imply that every numeric value in the document has been discovered. |
| **PRD-STAT-002** | Each surfaced statistic must include a metric or contextual label, value, unit when applicable, context, source page, and evidence/provenance link. | Metrics must remain understandable and traceable. | **Must** | 1. A user can identify what the value represents and where it came from.<br>2. A metric without a natural unit may omit the unit rather than invent one. |
| **PRD-STAT-003** | The product must visibly distinguish directly extracted metrics from derived metrics. | Users must know whether a value appears in the document or was calculated. | **Must** | 1. Every displayed derived metric is labeled as derived.<br>2. Directly extracted values are not mislabeled as calculated. |
| **PRD-STAT-004** | A derived metric may be shown only when its calculation is justified by document evidence and its source inputs remain traceable. | Derived calculations are approved conditionally. | **Must** | 1. A derived metric provides access to the evidence supporting its inputs.<br>2. If required inputs are missing or ambiguous, the product withholds the derivation or marks it unavailable rather than guessing. |
| **PRD-STAT-005** | Repeated or duplicate metrics must be handled without forcing unsafe deduplication when context differs. | The scope accepts imperfect deduplication and contextual ambiguity. | **Must** | 1. Clearly repeated identical evidence is not needlessly multiplied where practical.<br>2. Values that appear similar but have different periods, populations, sections, or contexts remain distinguishable. |
| **PRD-STAT-006** | When conflicting values for the same apparent metric are surfaced within one document, the product must preserve and expose the conflict rather than silently choose one. | Intra-document conflicts are an approved investigation scenario. | **Must** | 1. Conflicting values can both be inspected with their separate provenance.<br>2. The UI does not imply a single authoritative value unless the document itself establishes one. |
| **PRD-STAT-007** | Ambiguous semantic classification must remain visible instead of being presented as a certain normalized metric name. | Metric naming can be limited by source clarity. | **Must** | 1. An uncertain inferred label is qualified or falls back to source wording.<br>2. The source context remains available for user verification. |
| **PRD-STAT-008** | Statistics extraction must support partial results and must not block the entire document when some metrics cannot be confidently structured. | Useful coverage is required; exhaustive extraction is not. | **Must** | 1. Reliable extracted statistics remain usable even when other candidate metrics are omitted.<br>2. The product can show that extraction is partial or best-effort where relevant. |


### 8.8 Table Handling

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-TABLE-001** | PdfMining must reconstruct and display structured table content only when the reconstruction is sufficiently reliable. | The MVP prefers no structured table to a confidently wrong one. | **Must** | 1. Representative clear native tables can be displayed as structured content.<br>2. A table that cannot be reconstructed reliably is withheld or clearly marked partial. |
| **PRD-TABLE-002** | Structured tables must retain source page/provenance links back to the original PDF. | Table-derived facts must remain verifiable. | **Must** | 1. A displayed reconstructed table identifies its originating page or pages.<br>2. A user can navigate from a table or table-derived statistic to the relevant source evidence where mapping is available. |
| **PRD-TABLE-003** | Scanned, image-based, merged-cell, nested, multi-page, and highly visual tables must be treated as best-effort and may be withheld or simplified when relationships are ambiguous. | Complex table reconstruction is explicitly limited. | **Must** | 1. The product does not present an ambiguous table reconstruction as fully reliable.<br>2. A warning or omission communicates when structured output is limited. |
| **PRD-TABLE-004** | Statistics extracted from reliable table content must follow the same provenance and extracted-versus-derived rules as other statistics. | Table-derived metrics are within the statistics scope, not a separate evidence model. | **Must** | 1. A table-origin statistic identifies its source evidence.<br>2. A calculation based on table values is labeled derived. |
| **PRD-TABLE-005** | Failure to reconstruct a table must not prevent the original table from remaining viewable in the canonical PDF. | The original document remains the source of truth regardless of structured extraction success. | **Must** | 1. The PDF viewer continues to show the original table.<br>2. No replacement structured table is treated as superior evidence to the original PDF. |


### 8.9 Chart and Visual Content

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-VIS-001** | Charts, graphs, images, and diagrams must remain visible as part of the original PDF even when PdfMining does not semantically interpret them. | Visual content is preserved but general multimodal understanding is not approved. | **Must** | 1. The viewer displays the original page containing the visual content.<br>2. Lack of visual interpretation does not remove or alter the source PDF. |
| **PRD-VIS-002** | PdfMining must not claim to extract or reason about numerical values encoded only in charts or graphs as an MVP capability. | Chart numerical interpretation is explicitly out of scope. | **Must** | 1. A question that depends solely on an unextracted chart value produces an insufficient-evidence/unsupported-capability response.<br>2. The product does not present a chart region itself as verified numerical evidence. |
| **PRD-VIS-003** | Ordinary nearby native/OCR text such as captions may be used when it is reliably extracted, but the product must distinguish textual evidence from unsupported visual interpretation. | Text near visuals can be in scope without implying chart intelligence. | **Must** | 1. A caption citation resolves to its textual source region when coordinates are reliable.<br>2. The presence of caption text does not cause the product to claim values that appear only graphically. |


### 8.10 Document Chat

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-CHAT-001** | A user must be able to start and continue a conversation about one uploaded document at a time. | Single-document Q&A is the approved MVP boundary. | **Must** | 1. Questions in a document workspace use only that document as the evidence source.<br>2. The product does not offer multi-document selection for a single conversation. |
| **PRD-CHAT-002** | The chat must accept natural-language questions in Arabic and English, including understandable mixed-language questions. | Arabic and English interaction are first-class MVP capabilities. | **Must** | 1. Representative Arabic and English questions can be submitted.<br>2. A mixed Arabic/English question is not rejected solely because it mixes the two supported languages. |
| **PRD-CHAT-003** | The product must support contextual follow-up questions that use the conversation history to interpret user intent. | Follow-up interaction is explicitly included. | **Must** | 1. A follow-up such as 'What about the previous year?' can resolve prior conversational context when the referenced subject is clear.<br>2. Conversation history helps resolve intent but is not presented as document evidence. |
| **PRD-CHAT-004** | Answers to document questions must be grounded in evidence from the current uploaded document. | Document-only grounding is a core safety and trust contract. | **Must** | 1. Document-derived factual claims are supported by document evidence where appropriate.<br>2. External general knowledge is not presented as evidence for a document claim. |
| **PRD-CHAT-005** | An answer may combine evidence from multiple locations or pages in the same document when necessary. | Some document questions require synthesis across sections. | **Must** | 1. A multi-source answer can cite more than one supporting passage.<br>2. Each cited passage remains individually navigable. |
| **PRD-CHAT-006** | Document-associated conversation history must persist until the document is deleted. | Users are expected to return to prior analysis. | **Must** | 1. Reopening the document restores prior conversation history.<br>2. Deleting the document removes its conversation history from user access. |
| **PRD-CHAT-007** | If answer generation fails for a transient reason, the user must see a failure state and an available retry path without losing prior successful conversation history. | AI/provider failures must be recoverable without hiding the problem. | **Must** | 1. A failed answer is not displayed as a successful answer.<br>2. The user can retry the question or submit it again.<br>3. Earlier successful messages remain available. |


### 8.11 Grounding and Insufficient Evidence Behavior

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-GROUND-001** | When the document contains no relevant evidence for a requested factual answer, PdfMining must explicitly state that the document does not establish the answer. | The product must prefer limitation over unsupported generation. | **Must** | 1. No unsupported factual answer is presented as if sourced from the document.<br>2. The response distinguishes 'not established by this document' from a processing error. |
| **PRD-GROUND-002** | When evidence is meaningful but incomplete or inferential, the answer must use wording that reflects the uncertainty and must not overstate the claim. | Medium or Low Evidence Support requires calibrated language. | **Must** | 1. Qualified evidence produces qualified language such as 'suggests', 'indicates', or an equivalent appropriate phrasing.<br>2. The support label and answer wording do not contradict each other. |
| **PRD-GROUND-003** | When relevant source passages conflict, the answer must surface the conflict and cite the competing evidence rather than silently resolving it. | Conflicting evidence is a legitimate document state. | **Must** | 1. The user can inspect each conflicting source.<br>2. The answer does not assert a definitive resolution unless the document provides evidence for that resolution. |
| **PRD-GROUND-004** | When OCR or extraction quality prevents reliable interpretation, the answer must communicate that limitation and reduce or withhold affected claims. | Poor source quality must propagate into downstream behavior. | **Must** | 1. Known unreadable or unreliable regions are not used as strong evidence.<br>2. The user is told when source quality materially limits the answer. |
| **PRD-GROUND-005** | When a question requires knowledge outside the uploaded document, PdfMining must not silently answer from general model knowledge as if it were document evidence. | External knowledge and web search are outside the MVP evidence contract. | **Must** | 1. The answer says the requested fact is outside what the document establishes, unless the question also has a document-grounded portion that can be answered separately.<br>2. No external-source citation is introduced into document chat. |
| **PRD-GROUND-006** | When the user asks for speculation, prediction, or an unsupported conclusion, PdfMining must distinguish document-supported inference from unsupported speculation and decline to present unsupported factual certainty. | The product must not transform speculation into evidence-backed fact. | **Must** | 1. Any permitted inference is explicitly qualified and tied to evidence.<br>2. If the requested speculation cannot be grounded, the product states that the document is insufficient. |
| **PRD-GROUND-007** | Instructions embedded inside uploaded PDF content must be treated as untrusted document data and must not override the product's grounding, privacy, access, or safety behavior. | Prompt-like document text is a known scope risk. | **Must** | 1. A PDF passage instructing the system to ignore prior rules does not change user isolation or evidence policy.<br>2. Such text may be analyzed as document content when relevant, but not executed as product instructions. |


### 8.12 Citations

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-CITE-001** | Document-derived factual claims must use statement/claim-level citations where appropriate rather than relying only on a page-level bibliography. | Fine-grained traceability is an approved MVP differentiator. | **Must** | 1. A factual claim can be unambiguously associated with its supporting citation or citations.<br>2. A citation identifies the correct source page. |
| **PRD-CITE-002** | Each citation must provide a page reference and a source-text preview sufficient for the user to recognize the supporting evidence. | Users need to inspect evidence without guessing what a citation refers to. | **Must** | 1. The citation displays the source page.<br>2. The citation exposes a supporting excerpt or preview from the document. |
| **PRD-CITE-003** | A claim may have one or multiple citations, including citations across multiple pages, when one passage is insufficient. | Evidence may be distributed through a document. | **Must** | 1. The UI permits more than one evidence item for a claim.<br>2. Each evidence item can be opened independently. |
| **PRD-CITE-004** | Citation presentation must prioritize a minimal sufficient evidence set while allowing additional supporting evidence when useful. | The scope explicitly favors sufficient evidence without unnecessary clutter. | **Should** | 1. The primary citation display does not overwhelm the user with redundant passages.<br>2. Additional support remains accessible when the answer depends on it or the user chooses to inspect it. |
| **PRD-CITE-005** | Citations must resolve to the original uploaded PDF, including OCR-based citations for scanned content and provenance for statistics/table-derived values. | The original PDF is the canonical evidence source. | **Must** | 1. A native citation opens the original page.<br>2. An OCR citation opens the original scanned page rather than a replacement derivative.<br>3. A table-derived statistic can trace back to its source in the original PDF. |
| **PRD-CITE-006** | Citation numbering or identifiers, if shown, must make claim-to-evidence association unambiguous; no specific numbering scheme is required. | The scope leaves numbering presentation to the PRD while requiring clarity. | **Must** | 1. A user can determine which evidence supports each cited claim even when multiple citations appear.<br>2. Identifiers do not imply evidence rank or factual probability unless explicitly explained. |
| **PRD-CITE-007** | When reliable exact source coordinates are unavailable, the citation must fall back to the correct page and source preview without fabricating precise region mapping. | False citation precision is an explicit quality failure. | **Must** | 1. The user can still open the cited page.<br>2. The UI communicates that exact highlighting is unavailable rather than showing a guessed region. |


### 8.13 Evidence Support

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-EVID-001** | For supported generated claims, PdfMining must display Evidence Support using the categorical labels High, Medium, or Low where claim/evidence verification is available. | High/Medium/Low is the approved MVP user-facing representation. | **Must** | 1. The UI uses the labels High, Medium, and Low rather than requiring percentages.<br>2. The label is associated with the specific claim/evidence relationship it describes. |
| **PRD-EVID-002** | Evidence Support must mean how strongly the selected document evidence supports the specific generated claim. | The indicator must not be confused with other confidence concepts. | **Must** | 1. Product copy or help text explains the evidence-claim relationship.<br>2. Evidence Support is not labeled as OCR confidence, retrieval relevance, or model confidence. |
| **PRD-EVID-003** | The product must never represent Evidence Support as the probability that the answer or claim is factually true. | The approved scope explicitly prohibits this interpretation. | **Must** | 1. No label, tooltip, percentage, or explanatory text describes Evidence Support as factual-truth probability.<br>2. High does not imply guaranteed truth. |
| **PRD-EVID-004** | Medium and Low Evidence Support must be accompanied by wording and presentation that does not overstate the supported claim. | Support strength and answer wording must be consistent. | **Must** | 1. Medium-support claims use qualified language when support is incomplete or inferential.<br>2. Low-support claims are visibly weak/ambiguous and are not phrased with stronger certainty than the evidence allows. |
| **PRD-EVID-005** | A claim with no sufficient evidence must not be presented merely as Low; it must normally be removed or replaced by an explicit insufficient-evidence response. | Unsupported is distinct from low support. | **Must** | 1. Unsupported factual claims are not shown with a misleading Low badge as if some evidence supports them.<br>2. The user receives a clear insufficiency message when the answer cannot be established. |


### 8.14 PDF Viewer

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-VIEW-001** | The document workspace must display the original uploaded PDF as the canonical visual source. | Users need direct access to the evidence source. | **Must** | 1. The viewed file is the original uploaded PDF.<br>2. Processing derivatives do not silently replace it. |
| **PRD-VIEW-002** | The PDF viewer must support direct page navigation, sequential scrolling, and zoom controls. | These are necessary to inspect cited evidence and the surrounding document. | **Must** | 1. A user can move to a specified page.<br>2. A user can scroll through pages.<br>3. A user can zoom in and out while retaining access to the current document. |
| **PRD-VIEW-003** | Citation activation must navigate the viewer to the cited page and preserve enough context for the user to inspect the source. | Citation-to-source navigation is central to the evidence-first experience. | **Must** | 1. Selecting a valid citation changes the viewer to the correct page.<br>2. If an exact highlight is available, it becomes visible after navigation. |
| **PRD-VIEW-004** | The viewer and surrounding document workspace must present Arabic/RTL text correctly where such text is rendered outside the PDF page image/content. | Arabic is a first-class experience. | **Must** | 1. Arabic source previews and UI text use appropriate RTL direction where applicable.<br>2. PDF page rendering itself preserves the original page appearance. |
| **PRD-VIEW-005** | The PDF viewer must remain usable on mobile-responsive web through a view suited to smaller screens rather than requiring the desktop split-screen layout. | Mobile-responsive web is included while native apps are excluded. | **Must** | 1. On a supported small viewport, the user can switch to and use the PDF viewer.<br>2. Essential page navigation and citation-driven navigation remain available. |


### 8.15 Exact Source Highlighting

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-HL-001** | When reliable coordinates exist, citation navigation must highlight the exact supporting source region in yellow on the original PDF. | Yellow exact highlighting is an approved MVP behavior. | **Must** | 1. Selecting an eligible citation shows a yellow highlight over the mapped evidence region.<br>2. The highlighted region is on the correct original page. |
| **PRD-HL-002** | Native-text highlighting must use reliable native source coordinates and OCR-derived highlighting must use reliable OCR coordinates. | The source-coordinate model differs by content type while preserving one canonical PDF. | **Must** | 1. Representative native citations highlight the mapped native source.<br>2. Representative scanned citations highlight the mapped OCR source on the original scanned page. |
| **PRD-HL-003** | Multi-line evidence must be highlightable as multiple contiguous or logically related regions when one bounding region would be misleading. | Evidence can span multiple rendered lines. | **Must** | 1. A citation spanning line breaks highlights all required lines without highlighting unrelated surrounding text.<br>2. The highlighted set still maps to the single cited evidence item. |
| **PRD-HL-004** | Evidence composed of multiple non-contiguous source regions may use multiple highlights associated with the same citation when necessary. | Some claims require evidence fragments from one or more regions. | **Should** | 1. Each required mapped region is visually associated with the activated citation.<br>2. The UI does not imply one contiguous source span when the evidence is actually disjoint. |
| **PRD-HL-005** | When exact coordinates are unavailable or unreliable, PdfMining must omit the exact highlight and provide page-level navigation plus source preview with an explicit limitation. | The product must never fabricate coordinate certainty. | **Must** | 1. No guessed yellow rectangle is shown.<br>2. The user can still inspect the correct page and textual evidence when available. |


### 8.16 Split View

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-SPLIT-001** | On desktop, the primary document workspace must allow the original PDF to be visible alongside analysis/chat. | The approved usability scope calls for a document-centered split-screen experience. | **Must** | 1. A user can inspect the PDF and analysis/chat without leaving the document workspace.<br>2. Citation navigation updates the source side while the answer context remains available. |
| **PRD-SPLIT-002** | On small screens, the product must use switchable views rather than forcing the desktop side-by-side layout. | Responsive mobile web is included; native apps are not. | **Must** | 1. The user can switch between analysis/chat and PDF views.<br>2. Citation activation can take the user to the PDF view and cited page without losing the conversation state. |


### 8.17 Search, Sort and Filtering

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-SEARCH-001** | The statistics view must provide search over displayed metric labels and relevant contextual text. | Search within extracted statistics is explicitly included. | **Must** | 1. A search term narrows visible statistics to matching metric/context content.<br>2. Clearing the search restores the unfiltered result set. |
| **PRD-SEARCH-002** | The statistics view must provide basic filtering for structured-statistic attributes that are already available, including extracted-versus-derived type and Evidence Support when present. | Filtering is approved; advanced analytics is not. | **Must** | 1. A user can filter to directly extracted or derived metrics.<br>2. When Evidence Support exists for statistics, the user can filter by support label without changing the underlying data. |
| **PRD-SEARCH-003** | Statistics must have a stable default ordering, but advanced user-configurable sorting is not an MVP requirement. | Stage 02 permits default ordering but excludes advanced sorting as a commitment. | **Must** | 1. The same result set has a predictable default order within a document.<br>2. The product does not require arbitrary multi-column sorting to satisfy MVP acceptance. |
| **PRD-SEARCH-004** | Document history may use a default recency ordering; cross-document content search and advanced document filtering are not part of the MVP. | Cross-document analytics and collection search are deferred. | **Must** | 1. History presents documents in a predictable order.<br>2. The MVP does not expose a search that semantically searches across document contents. |


### 8.18 Export

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-EXPORT-001** | The user must be able to export structured statistics from a document as CSV. | CSV statistics export is an approved MVP deliverable. | **Must** | 1. A Ready or partial document with structured statistics can produce a CSV file.<br>2. The export contains the currently available structured statistics rather than unrelated chat content. |
| **PRD-EXPORT-002** | The user must be able to export structured statistics from a document as Excel. | Excel statistics export is an approved MVP deliverable. | **Must** | 1. A Ready or partial document with structured statistics can produce an Excel-compatible workbook.<br>2. The exported metrics correspond to the document's available structured statistics. |
| **PRD-EXPORT-003** | Each exported statistic must include enough information to identify the source document, metric/value, context, page, provenance, and extracted-versus-derived status. | Exported data must remain traceable outside the application. | **Must** | 1. The export identifies the source document and page for each metric.<br>2. Derived metrics remain explicitly distinguishable from extracted values.<br>3. A provenance field or fields allow the user to trace the metric back to source evidence. |
| **PRD-EXPORT-004** | Export must preserve relevant uncertainty/partial-result information rather than converting uncertain data into apparently certain data. | Export cannot strip away important evidence limitations. | **Must** | 1. Where a statistic is marked partial, ambiguous, or has Evidence Support metadata, the export preserves an appropriate indicator when available.<br>2. Withheld/unsupported values are not invented solely to complete the export. |
| **PRD-EXPORT-005** | The MVP export feature must not imply support for chat transcript export, standalone citation export, arbitrary full-table export, or regenerated canonical PDFs. | Those export types are deferred or out of scope. | **Must** | 1. Only approved structured-statistics CSV/Excel export is required for MVP acceptance.<br>2. The UI does not advertise excluded export types as supported MVP capabilities. |


### 8.19 Arabic and English Experience

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-LANG-001** | Arabic and English documents must both be supported as first-class MVP scenarios for native extraction, OCR where needed, statistics, citations, and document chat. | Bilingual document handling is a core MVP boundary. | **Must** | 1. Representative Arabic and English documents can complete the supported workflow.<br>2. Arabic is not presented as an experimental or optional feature relative to English. |
| **PRD-LANG-002** | Mixed Arabic/English documents must be supported without requiring the user to choose a single document language. | Mixed-language documents are explicitly included. | **Must** | 1. A document containing both Arabic and English can be processed.<br>2. Evidence from both supported languages can be cited when relevant. |
| **PRD-LANG-003** | Arabic and English questions must be accepted, and answers should default to the language of the user's question when practical. | Interaction should be natural across the two supported languages. | **Must** | 1. An Arabic question can receive an Arabic answer when the answer is supported.<br>2. An English question can receive an English answer when the answer is supported. |
| **PRD-LANG-004** | Understandable mixed-language questions may be answered in the dominant or user-requested supported language without claiming a separate code-switching accuracy guarantee. | Mixed-language questions are conditionally supported at scope level. | **Should** | 1. A mixed Arabic/English question is processed when its intent is understandable.<br>2. If the intent is ambiguous, the product asks for clarification or states the ambiguity rather than inventing intent. |
| **PRD-LANG-005** | Arabic UI/content areas such as chat, source previews, metric context, and warnings must use appropriate RTL presentation where applicable, while preserving original PDF page appearance. | RTL-aware behavior is required. | **Must** | 1. Arabic textual UI content is readable in RTL direction.<br>2. Mixed-language strings remain legible and source navigation remains correct. |
| **PRD-LANG-006** | PdfMining must not promise automatic translation between Arabic and English as an MVP feature. | Translation was not approved as a product capability. | **Must** | 1. The product does not advertise translation as part of the MVP.<br>2. Answering in a supported interaction language does not alter the canonical source text or citation. |


### 8.20 Errors, Warnings and Recovery

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-ERR-001** | Invalid, corrupted, or unreadable PDFs must produce a clear upload/processing error and must not enter a misleading Ready state. | Malformed PDFs are only best-effort supported. | **Must** | 1. The user sees that the document could not be processed.<br>2. Where appropriate, the user can re-upload a corrected copy. |
| **PRD-ERR-002** | Password-protected or encrypted PDFs that cannot be opened with the supplied password must request correction or fail visibly; PdfMining must not attempt protection bypass. | Encryption bypass is explicitly out of scope. | **Must** | 1. An incorrect password does not unlock or process protected content.<br>2. The user can submit a corrected password when the document format is otherwise supported. |
| **PRD-ERR-003** | An OCR failure must identify OCR as the affected capability and preserve usable non-OCR results when possible. | Partial success should survive non-critical failure. | **Must** | 1. Native pages remain usable when OCR on another page fails.<br>2. The document carries a visible partial-processing/OCR warning. |
| **PRD-ERR-004** | A structured extraction or table reconstruction failure must not invalidate the original PDF viewer or successful chat/evidence features that remain supportable. | Capabilities should degrade independently where practical. | **Must** | 1. The original PDF remains accessible.<br>2. The affected extraction result is withheld or marked unavailable rather than fabricated. |
| **PRD-ERR-005** | An AI generation or verification provider failure must produce a visible answer failure and a retry path while preserving already completed document processing. | Provider failures should not erase successful work. | **Must** | 1. The failed answer is not presented as complete.<br>2. Previously extracted statistics, PDF access, and prior successful chat messages remain available. |
| **PRD-ERR-006** | A timeout during processing or answer generation must be distinguishable from a semantic insufficient-evidence response. | Operational failure and evidence insufficiency have different meanings. | **Must** | 1. The user is told that processing/answer generation did not complete.<br>2. The UI does not mislabel a timeout as 'the document has no evidence'. |
| **PRD-ERR-007** | Partial results must be explicitly labeled and must identify the affected capability or limitation at a useful level. | Hidden partial failure is prohibited. | **Must** | 1. The user can distinguish full-ready output from partial-ready output.<br>2. Known missing OCR/table/statistics capability is not silently omitted without a relevant warning when it materially affects results. |
| **PRD-ERR-008** | Export failure must leave the document and its analysis intact and offer a retry or re-initiation path. | Export is downstream of analysis and should fail independently. | **Must** | 1. A failed export does not delete or alter document results.<br>2. The user receives a visible failure message and can attempt export again. |
| **PRD-ERR-009** | Error and warning messages must avoid exposing sensitive document content, passwords, or unnecessary provider/internal details. | User-visible recovery must preserve confidentiality. | **Must** | 1. A password is never echoed in an error message.<br>2. Errors explain the actionable user-facing problem without exposing protected internal data. |


**Scope note for 8.2:** Drag-and-drop is not required by the approved Stage 02 baseline. A design may support it later without changing the PDF-only validation contract, but MVP acceptance does not depend on it.

**Scope note for 8.16:** Pane resizing and collapse behavior were not approved as standalone MVP capabilities. They may be design refinements later, but the required product behavior is desktop side-by-side visibility plus mobile switchable views.

**Scope note for 8.17:** General table sorting/filtering and advanced document-history search are not MVP commitments. The approved search/filter capability is centered on extracted statistics/KPIs.


## 9. Data Retention and Deletion — Product Behavior

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-RET-001** | Uploaded documents and their document-specific analysis data must persist in the user's private history until the user deletes the document. | Persistence-until-deletion is the approved MVP retention model. | **Must** | 1. A processed document remains available across later authenticated sessions.<br>2. The product does not silently expire document history under an unstated retention policy. |
| **PRD-RET-002** | Deleting a document must logically remove the original PDF, optional searchable derivative, normalized/extracted artifacts, statistics, conversations, citations/evidence artifacts, and other document-specific derived data. | Document deletion must be comprehensive from the user's perspective. | **Must** | 1. After deletion, the user cannot access any of the listed document-specific artifacts through the product.<br>2. The deleted document no longer appears in history. |
| **PRD-RET-003** | The deletion confirmation must warn that document-specific analysis and conversation history will also be removed. | Users must understand the consequence of deletion. | **Must** | 1. The confirmation names or otherwise clearly identifies the selected document.<br>2. The confirmation explains that the document and associated analysis cannot remain accessible after deletion. |
| **PRD-RET-004** | The MVP must not introduce organization-level retention rules or shared-document lifecycle behavior. | Those capabilities are outside the single-user MVP. | **Must** | 1. No organization retention policy is required for MVP acceptance.<br>2. A user's document lifecycle is controlled by that user's upload and delete actions. |
| **PRD-RET-005** | Failed or abandoned processing must not leave unnecessary temporary document artifacts retained as part of the user's long-term document data. | Stage 02 requires cleanup of unnecessary temporary artifacts after failed processing. | **Must** | 1. A failed processing attempt does not create extra user-visible document copies or derivatives that persist without purpose.<br>2. Cleanup of temporary artifacts does not remove successful results that the product intentionally retains for a partial document. |


## 10. Security and Privacy — Product Requirements

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-SEC-001** | A user's documents and document-derived data must be inaccessible to other users. | Strict user isolation is a fundamental privacy requirement. | **Must** | 1. Cross-account access to PDFs, OCR text, statistics, conversations, citations, exports, or derived artifacts is denied.<br>2. Unauthorized attempts do not disclose protected content. |
| **PRD-SEC-002** | Document data must be protected in transit and at rest as a product security requirement. | Encryption in transit and at rest are explicitly approved scope requirements. | **Must** | 1. Production use does not transmit protected document content over an unencrypted application channel.<br>2. Stored original and derived document data are covered by the product's at-rest protection design, to be specified technically in the SRS/design stages. |
| **PRD-SEC-003** | Where external AI/OCR processing is used, PdfMining must minimize transmitted document content to what is needed for the processing task and provide understandable privacy disclosure where relevant. | External processing is allowed but bounded by minimization and transparency. | **Must** | 1. The product/privacy information does not imply all processing is local if external providers are used.<br>2. The product does not send unrelated document content merely for convenience when a smaller relevant portion suffices. |
| **PRD-SEC-004** | Product and operational error behavior must not expose PDF passwords or unnecessarily include sensitive document content. | Secrets and confidential content require special handling. | **Must** | 1. User-visible errors never display the submitted PDF password.<br>2. Normal product diagnostics presented to users avoid dumping document content. |
| **PRD-SEC-005** | PdfMining must make no unsupported compliance, certification, regulated-industry, regional-residency, or multi-region claims. | The MVP has explicitly limited compliance and hosting commitments. | **Must** | 1. Marketing/product UI does not claim SOC 2, ISO 27001, HIPAA, government certification, configurable data residency, or multi-region deployment unless separately established.<br>2. No hosting-region selector is offered in the MVP. |
| **PRD-SEC-006** | Uploaded PDF content must be treated as untrusted data and cannot change account permissions, system rules, evidence policy, or product behavior merely by containing instructions. | Document prompt injection is an explicit product risk. | **Must** | 1. Embedded instructions cannot grant access to another user's content.<br>2. Embedded instructions cannot cause external knowledge to be presented as document evidence. |
| **PRD-SEC-007** | Where external AI/OCR providers are used and provider controls are available, the product should use configurations that prevent submitted content from being used for model training and minimize or disable provider retention. | Stage 02 requires privacy-conscious external-provider configuration where available. | **Should** | 1. Provider configuration is reviewed for available training-use controls before production use.<br>2. Available retention-minimization settings are enabled where compatible with the approved product behavior.<br>3. Product disclosure does not claim stronger provider privacy behavior than is actually configured. |
| **PRD-SEC-008** | Operational logging associated with document processing must minimize document content and exclude secrets such as user-supplied PDF passwords. | Confidential document content and secrets should not be unnecessarily replicated into logs. | **Must** | 1. PDF passwords are not recorded in operational logs.<br>2. Normal logs avoid storing full document text/source excerpts unless a separately approved diagnostic process explicitly requires and protects them. |


## 11. Performance Expectations

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-PERF-001** | Upload interactions must remain responsive enough to show immediate acknowledgment and ongoing upload status; no public upload-time SLA is established. | The user must know the application is working without inventing an unapproved SLA. | **Must** | 1. Starting an upload produces visible acknowledgment.<br>2. The user can distinguish an active upload from an unresponsive page. |
| **PRD-PERF-002** | For representative native PDFs within the initial limit, the product should be validated against an initial end-to-end processing target of roughly 30–60 seconds. | Stage 02 defines this as a validation target, not a public SLA. | **Should** | 1. Representative benchmark results are recorded against the target.<br>2. Product messaging does not convert the target into a guaranteed completion time. |
| **PRD-PERF-003** | For representative OCR-heavy PDFs within the initial limit, the product should be validated against an initial processing target of roughly 2–3 minutes. | OCR-heavy documents have a separate approved validation target. | **Should** | 1. Representative OCR-heavy benchmark results are recorded.<br>2. Grounding/citation correctness is not intentionally weakened solely to hit the target. |
| **PRD-PERF-004** | Typical document-chat questions should be validated against an initial response target of approximately 5–10 seconds. | Stage 02 provides a provisional chat target. | **Should** | 1. Representative questions are benchmarked.<br>2. Slow responses show an in-progress state rather than appearing lost.<br>3. The target is not advertised as a guaranteed SLA. |
| **PRD-PERF-005** | The MVP should be validated against an engineering scenario of approximately 10 simultaneously active users on the approved hosting environment. | The scope includes a preliminary concurrency validation scenario. | **Should** | 1. A documented validation run evaluates the representative workload.<br>2. Failure to meet the scenario triggers technical remediation/hosting review rather than silently changing product evidence quality. |
| **PRD-PERF-006** | The PDF viewer, page navigation, citation navigation, and statistics interactions must remain usable while background or downstream processing continues when the required underlying content is already available. | Successful capabilities should remain usable during long-running or partial work. | **Must** | 1. Opening an available PDF does not require unrelated failed/unfinished analysis to finish.<br>2. Navigation controls provide visible response to user action. |
| **PRD-PERF-007** | CSV/Excel export must provide visible in-progress and success/failure feedback; no public export-time SLA is established. | Exports may vary in size and must not appear silently stalled. | **Must** | 1. Starting export produces visible acknowledgment.<br>2. Completion provides the file; failure provides a retryable error without altering analysis. |
| **PRD-PERF-008** | The MVP must not present the validation targets in this PRD as public uptime, recovery-time, or guaranteed latency SLAs. | Stage 02 explicitly establishes validation targets rather than operational SLAs. | **Must** | 1. Product/marketing copy does not promise the 30–60 second, 2–3 minute, or 5–10 second targets as guaranteed completion times.<br>2. No uptime or recovery-time SLA is claimed unless separately approved and validated. |


## 12. Accessibility and Responsive Behavior

| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-UX-001** | The MVP must provide a document-centered desktop web experience and a mobile-responsive web experience. | Web is the only approved delivery surface; responsive mobile web is included. | **Must** | 1. Desktop supports the side-by-side document workspace.<br>2. Small viewports use switchable views rather than forcing the desktop layout. |
| **PRD-UX-002** | Primary interactive controls for upload, navigation, chat submission, citation activation, filters, export, and deletion should be operable using standard keyboard interaction where the browser control model supports it. | Basic keyboard usability improves access without making an unapproved compliance claim. | **Should** | 1. Interactive controls can receive focus in a logical sequence.<br>2. Focused buttons/links can be activated using standard keyboard actions. |
| **PRD-UX-003** | Citation, warning, error, and Evidence Support states must use readable text labels and must not rely solely on color. | Critical trust states must remain understandable to more users. | **Must** | 1. High/Medium/Low appears as text, not color alone.<br>2. Warnings/errors include text that communicates meaning. |
| **PRD-UX-004** | Arabic/RTL presentation must remain usable across supported viewport sizes, including chat, source previews, statistics context, and warning text. | Arabic is first-class on desktop and mobile web. | **Must** | 1. RTL content does not obscure essential controls or citation associations.<br>2. Switching between PDF and analysis on mobile preserves reading direction and context. |
| **PRD-UX-005** | The MVP must not claim formal WCAG or other accessibility conformance unless separately defined and validated. | No formal accessibility certification target was approved. | **Must** | 1. Public/product copy does not claim a conformance level that has not been tested and approved.<br>2. Basic usability requirements in this PRD are not represented as certification. |


**Browser-support note:** The MVP is a web application for desktop browsers and mobile-responsive web. A precise supported-browser/version matrix is a later SRS/QA decision and is not fixed by this PRD.



---

## 13. Product States

### 13.1 Document State Model

The user-visible document lifecycle is:

```text
Uploaded
  ↓
Queued / waiting to process
  ↓
Extracting
  ↓
OCR (only when required)
  ↓
Analyzing
  ↓
Ready
  ├─→ Ready with Warnings / Partially Processed
  └─→ Failed (if a usable minimum result cannot be produced)
```

Permitted user-visible transitions include:

- **Uploaded → Queued/Extracting:** upload and validation succeeded.
- **Extracting → OCR:** one or more pages/regions require OCR.
- **Extracting/OCR → Analyzing:** sufficient source content exists for downstream analysis.
- **Analyzing → Ready:** approved outputs completed without known material limitation.
- **Analyzing → Ready with Warnings / Partially Processed:** useful outputs exist but one or more capabilities are limited or failed.
- **Any processing state → Failed:** the product cannot produce a usable minimum result.
- **Ready/Partial → processing-related retry state:** a user retries a failed capability where the product offers retry.
- **Any retained state → Deleted:** after explicit deletion confirmation; Deleted is terminal from the user's perspective.

A warning/partial state must identify the affected capability rather than using a generic success indicator.

### 13.2 Conversation State Model

```text
No conversation
  ↓
Question submitted / Awaiting answer
  ├─→ Answered
  ├─→ Insufficient Evidence
  └─→ Failed
```

- **Answered:** a grounded response is shown with evidence where appropriate.
- **Insufficient Evidence:** the document does not establish the requested answer, or source quality makes a reliable answer unavailable.
- **Failed:** answer generation/verification did not complete for operational reasons.
- A failed message may be retried without deleting prior successful conversation history.

### 13.3 Export State Model

```text
Idle
  ↓
Generating
  ├─→ Completed
  └─→ Failed
```

- **Completed:** the approved CSV or Excel export is available.
- **Failed:** the user receives an error and can retry; document analysis remains unchanged.

---

## 14. Edge Cases

| ID | Scenario | Expected Product Behavior |
|---|---|---|
| EC-001 | Empty or zero-page PDF | Reject or fail visibly; do not produce a Ready document. |
| EC-002 | One-page PDF | Process normally if otherwise supported; all evidence remains page-traceable. |
| EC-003 | PDF exactly at configured 20-page maximum | Accept when other validations pass. |
| EC-004 | PDF exceeds configured page maximum | Reject before normal analysis and state the active page limit. |
| EC-005 | File above configured size limit | Reject and communicate the active configured limit. |
| EC-006 | Password-protected PDF with valid password | Continue normal processing after successful unlock. |
| EC-007 | Password-protected PDF with invalid/no password | Request correction or fail visibly; never bypass protection. |
| EC-008 | Mixed native/scanned pages | Use native extraction where usable and OCR selectively where required. |
| EC-009 | Arabic and English on the same page | Process as a supported mixed-language scenario; preserve traceability for both languages. |
| EC-010 | Commonly rotated page | Handle rotation automatically where otherwise processable. |
| EC-011 | Broken native text layer | Use best-effort extraction; warn when limitations affect results; do not claim completeness. |
| EC-012 | Very low-resolution scan | Best-effort OCR; surface poor quality and withhold unreliable claims/highlights. |
| EC-013 | Handwritten content | Treat handwriting understanding as unsupported; do not invent OCR/meaning for it. |
| EC-014 | Duplicate/repeated statistic with same source/context | Avoid unnecessary duplication where practical without claiming perfect deduplication. |
| EC-015 | Similar statistic with different period/population/context | Keep entries distinguishable; do not collapse them as duplicates. |
| EC-016 | Contradictory values for an apparent metric | Preserve both with provenance and expose the conflict. |
| EC-017 | Metric has value but ambiguous semantic label | Qualify the inferred label or preserve source wording; keep context visible. |
| EC-018 | Derived metric has ambiguous/missing inputs | Withhold the derived value or state it cannot be reliably calculated. |
| EC-019 | PDF contains no extractable statistics | Show an empty/no-results statistics state that does not claim the PDF contains no numbers. |
| EC-020 | Clear native table | Reconstruct when sufficiently reliable and retain source provenance. |
| EC-021 | Merged/nested/complex table | Best-effort only; simplify, mark partial, or withhold if relationships are unreliable. |
| EC-022 | Multi-page table | Best-effort; do not imply correct cross-page joining when uncertain. |
| EC-023 | Scanned table | OCR/reconstruct only when sufficiently reliable; otherwise withhold structured output and keep original viewable. |
| EC-024 | Value visible only in a chart | Do not extract/answer it as verified numerical evidence under MVP chart capabilities. |
| EC-025 | Citation spans multiple lines | Highlight all reliable mapped lines without including unrelated text. |
| EC-026 | Claim needs evidence from multiple regions/pages | Attach multiple citations/highlights as required. |
| EC-027 | Citation page is known but exact coordinates are unreliable | Navigate to the correct page and show source preview; omit exact yellow highlight. |
| EC-028 | OCR cannot read one region/page | Preserve usable OCR/native results elsewhere and expose the affected limitation. |
| EC-029 | User asks an unrelated/general-knowledge question | State that the uploaded document does not establish the answer; do not use outside knowledge as document evidence. |
| EC-030 | User asks for speculation/prediction | Only provide a clearly qualified document-supported inference; otherwise state insufficient evidence. |
| EC-031 | Relevant sources conflict | Surface the conflict and cite competing evidence instead of silently choosing. |
| EC-032 | Document contains prompt-like instructions | Treat them as untrusted document content; they do not override product rules or permissions. |
| EC-033 | AI answer generation fails after extraction succeeded | Preserve PDF/analysis and prior chat; show answer failure and retry path. |
| EC-034 | Export fails | Preserve all analysis; show failure and allow re-initiation. |
| EC-035 | User deletes document while viewing it | After confirmation, terminate access to that document and remove it from history. |
| EC-036 | User attempts to open another user's document URL/identifier | Deny access without revealing protected content or metadata. |
| EC-037 | Mobile viewport opens a citation | Switch/focus the PDF view at the cited page; preserve chat state. |
| EC-038 | No relevant evidence exists | Return explicit insufficient-evidence behavior, not a low-support fabricated answer. |

---

## 15. Acceptance Criteria by Feature

| Feature Area | Acceptance Condition | Priority |
|---|---|---|
| Authentication | An authenticated individual can access their own private workspace, and cross-user access is denied. | Must |
| Upload | Supported PDFs within active limits can be uploaded; unsupported formats and over-limit files are rejected clearly. | Must |
| Password-protected PDFs | A valid user-supplied password permits processing; invalid/missing passwords do not bypass protection. | Must |
| Processing states | Users can distinguish upload, extraction, conditional OCR, analysis, Ready, partial/warning, and Failed states. | Must |
| Original source | The original uploaded PDF remains unchanged and is always the canonical viewer/citation source. | Must |
| Native extraction | Representative native PDFs yield useful text/structure with page association and reliable coordinates where available. | Must |
| OCR | Representative scanned and mixed PDFs yield useful Arabic/English OCR with visible quality limitations. | Must |
| Mixed PDFs | Native pages and scanned pages can be processed appropriately in the same document. | Must |
| Overview | A usable processed document presents a concise, document-grounded overview or an explicit limitation. | Must |
| Statistics | Useful quantitative facts/KPIs are surfaced with context and provenance without claiming exhaustive discovery. | Must |
| Extracted vs derived | Derived metrics are explicitly labeled and traceable to evidence inputs. | Must |
| Conflicting statistics | Conflicting values can coexist with separate provenance and are not silently reconciled. | Must |
| Tables | Clear tables may be reconstructed; unreliable complex tables are partial/withheld rather than confidently wrong. | Must |
| Charts/visuals | Original visuals remain viewable, but chart numerical interpretation is not presented as an MVP capability. | Must |
| Document chat | Questions operate on one document only and may use contextual follow-ups. | Must |
| Grounding | Document-derived factual answers rely on uploaded-document evidence only. | Must |
| Insufficient evidence | Missing/weak/unreadable evidence produces explicit limitation behavior rather than fabricated certainty. | Must |
| Citations | Document-derived claims can be associated with page-referenced source previews and one/multiple evidence passages. | Must |
| Evidence Support | High/Medium/Low reflects claim/evidence support and is never represented as factual-truth probability. | Must |
| PDF viewer | The user can view the original PDF, navigate pages, scroll, zoom, and follow citations. | Must |
| Exact highlighting | Reliable source regions are highlighted yellow; unreliable coordinates never produce simulated precision. | Must |
| Desktop workspace | The original PDF is visible alongside analysis/chat in the primary desktop experience. | Must |
| Mobile web | Smaller screens use switchable PDF and analysis/chat views while preserving citation navigation. | Must |
| Statistics search/filter | Users can search and filter structured statistics; advanced cross-document/BI behavior is absent. | Must |
| CSV export | Structured statistics export with provenance and type distinction succeeds on representative documents. | Must |
| Excel export | Structured statistics export with provenance and type distinction succeeds on representative documents. | Must |
| Document history | Users can return to retained private documents and persisted analysis. | Must |
| Deletion | Confirmed deletion removes the document from product access and removes associated document-specific data. | Must |
| Arabic | Representative Arabic native/scanned documents and Arabic questions complete the supported workflow. | Must |
| English | Representative English native/scanned documents and English questions complete the supported workflow. | Must |
| Mixed language | Representative mixed Arabic/English documents remain processable and source-traceable. | Must |
| Error recovery | Non-critical failures preserve successful capabilities and expose actionable failure/warning states. | Must |
| Privacy/security | User isolation, protected transmission/storage, content minimization, and no unsupported compliance claims are preserved. | Must |
| Performance validation | Representative native/OCR/chat/concurrency scenarios are measured against Stage 02 validation targets without converting them into public SLAs. | Should |
| Accessibility/responsiveness | Critical state meaning is not color-only; keyboard/basic responsive behavior is usable without claiming unvalidated conformance. | Must/Should |

---

## 16. Analytics / Product Observability Requirements

The approved scope does not create a user-facing analytics/dashboard feature. However, Stage 02 requires validation of processing, evidence, and performance behavior. The following event-level observability requirements support that validation without prescribing analytics infrastructure.


| ID | Requirement | Rationale | Priority | Acceptance Criteria |
|---|---|---|---|---|
| **PRD-OBS-001** | For MVP validation, the product should make key document lifecycle outcomes observable at event level without making analytics a user-facing feature. | Stage 02 requires documented validation results and visible processing outcomes. | **Should** | 1. At minimum, document uploaded, processing completed, processing completed with warnings/partial results, processing failed, and document deleted can be counted or reviewed.<br>2. Event observation does not require storing full document text or PDF passwords in analytics data. |
| **PRD-OBS-002** | For MVP validation, the product should make key evidence-workflow outcomes observable at event level while minimizing document content in analytics payloads. | Citation use, insufficient-evidence behavior, and export are core differentiators that need validation. | **Should** | 1. At minimum, question asked, answer returned, insufficient-evidence returned, citation activated, and export completed/failed can be observed.<br>2. The observable event does not need to contain the user's full question, answer, or source excerpt. |


Suggested event vocabulary for later SRS/implementation planning, consistent with the requirements above:

- document uploaded;
- document processing completed;
- document processing completed with warnings/partial results;
- document processing failed;
- document deleted;
- question asked;
- answer returned;
- insufficient-evidence returned;
- citation activated;
- export completed;
- export failed.

These events must not be interpreted as approval for storing full document content, questions, answers, source excerpts, or secrets in analytics payloads.

---

## 17. Known MVP Limitations

| Limitation | Expected User-Visible Behavior | Warning/Disclosure Needed |
|---|---|---|
| OCR may be inaccurate/incomplete on degraded scans | Partial or reduced-quality OCR results; affected analysis may be withheld or qualified. | Yes, when material |
| Arabic OCR quality varies by font, scan quality, layout, and content | Same evidence-first treatment as other OCR limitations; do not overstate certainty. | Yes, when material |
| Mixed-language pages may be harder to extract | Preserve usable content; disclose material quality limitations. | Yes, when material |
| Unusual fonts/broken text layers may reduce native extraction quality | Best-effort extraction; affected downstream output may be partial. | Yes |
| Extremely complex layouts may disrupt reading order/source mapping | Use best available mapping and suppress false precision. | Yes |
| Handwriting is unsupported | Do not claim handwriting understanding; affected content may be unavailable. | Yes when encountered |
| Very low-resolution scans may not produce useful OCR | OCR may fail or produce partial results. | Yes |
| Chart/graph numerical values are not interpreted | Visual remains viewable; chart-only values are not verified numerical evidence. | Yes when user asks for such interpretation |
| Arbitrary diagrams are not semantically understood | Original diagram remains viewable; no general diagram reasoning claim. | Yes when relevant |
| Complex/merged/nested/multi-page/highly visual tables may fail reconstruction | Structured table may be simplified, partial, or withheld. | Yes |
| Table extraction may be withheld | Original table remains viewable in PDF. | Yes when structured result is unavailable |
| Statistics/KPI extraction may miss relevant metrics | Do not imply an absent metric proves the PDF lacks it. | General product disclosure |
| Metric labels may be ambiguous | Qualify inferred label or preserve source wording/context. | Yes where ambiguous |
| Repeated metrics/evidence may not be perfectly deduplicated | Preserve context to avoid unsafe merging. | Usually contextual, not necessarily global warning |
| Derived metrics may be unavailable | Withhold calculation when inputs/evidence are insufficient. | Yes where requested |
| Exact source highlighting may be unavailable | Navigate to correct page/source preview without fabricated exact region. | Yes |
| OCR confidence and Evidence Support are different | Do not conflate the two indicators. | Product help/tooltip |
| Evidence Support is not factual-truth probability | Use High/Medium/Low only for claim/evidence support relationship. | Product help/tooltip |
| High/Medium/Low thresholds require empirical calibration | Treat labels as validated product indicators, not universal probability guarantees. | Internal validation; user copy must avoid probability claims |
| AI responses may be limited or withheld | Return explicit insufficient-evidence behavior. | Yes in affected answer |
| Processing/chat timings are validation targets, not SLAs | Show progress; do not promise guaranteed times. | Product/marketing language |
| A non-critical capability may fail while others remain usable | Ready-with-warnings/partial state; successful capabilities remain accessible. | Yes |

---

## 18. Dependencies

| Dependency | Product Impact | PRD Boundary |
|---|---|---|
| Existing VPS hosting environment | MVP behavior must be deployable and usable on the already-owned environment. | Exact deployment architecture remains later. |
| Persistent document/data storage capability | Required for private history, retained original PDFs, analysis, and deletion semantics. | Storage technology is not specified here. |
| PDF parsing/rendering capability | Required to show original PDFs and map evidence. | Exact library is not specified. |
| OCR capability supporting Arabic and English | Required for scanned/mixed documents. | Exact OCR provider/model is not specified. |
| AI language-model capability | Required for overview, Q&A, and semantic synthesis. | Exact model/provider is not specified. |
| Retrieval/evidence-selection capability | Required for document-grounded answers. | Retrieval/chunking/embedding algorithms are not specified. |
| Evidence-verification capability | Required for claim/evidence checking and Evidence Support. | Exact verification implementation is not specified. |
| Representative Arabic/English/mixed PDFs | Required to validate bilingual extraction, OCR, grounding, and citations. | Evaluation set design occurs later. |
| Representative native/scanned/mixed PDFs | Required to validate the complete processing boundary. | Must represent realistic professional layouts. |
| Claim/evidence evaluation data | Required to calibrate High/Medium/Low Evidence Support. | Numeric thresholds remain empirical, not product-scope choices. |
| External provider privacy/configuration options where used | Needed to minimize transmission, retention, and training use where possible. | Provider selection remains replaceable. |
| Spreadsheet export capability | Required for CSV/Excel statistics export. | Exact export implementation is not specified. |

---

## 19. Assumptions

| ID | Assumption | Product Impact if False |
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

---

## 20. Open Product Decisions

> **No product-level blockers remain for proceeding to Stage 04 — Software Requirements Specification.**

The following Stage 02 matters remain intentionally deferred but are **not open PRD product decisions** and do not prevent complete product definition:

- exact public performance SLAs — to be considered only after implementation benchmarking;
- numeric extraction/grounding acceptance thresholds — to be defined through SRS/evaluation planning;
- High/Medium/Low Evidence Support thresholds — to be empirically calibrated;
- exact OCR, embedding, LLM, reranking, and verification providers/models — later technical decisions;
- long-term pricing — post-MVP commercial decision;
- future large-document limits — future discovery;
- future team/organization behavior — future discovery.

No additional product-level ambiguity was introduced by this PRD.

---

## 21. Requirements Traceability

| Stage 02 Scope Area | PRD Requirement Group |
|---|---|
| User Accounts and Access | PRD-AUTH-* |
| Document Upload and Limits | PRD-DOC-* |
| Processing States / Partial Processing / Overview | PRD-PROC-* |
| Native PDF Extraction | PRD-NATIVE-* |
| Scanned PDF / OCR | PRD-OCR-* |
| Document History and Management | PRD-HIST-* |
| Statistics / KPI Extraction | PRD-STAT-* |
| Tables / Structured Content | PRD-TABLE-* |
| Chart / Visual Boundaries | PRD-VIS-* |
| Single-Document Chat / Q&A | PRD-CHAT-* |
| Grounding / Insufficient Evidence | PRD-GROUND-* |
| Citations | PRD-CITE-* |
| Evidence Support / Verification | PRD-EVID-* |
| Original PDF Viewer | PRD-VIEW-* |
| Exact Source Highlighting | PRD-HL-* |
| Desktop Split / Mobile Switching | PRD-SPLIT-* |
| Statistics Search / Filter / Default Ordering | PRD-SEARCH-* |
| CSV / Excel Statistics Export | PRD-EXPORT-* |
| Arabic / English / Mixed-Language Experience | PRD-LANG-* |
| Errors / Warnings / Recovery | PRD-ERR-* |
| Retention and Deletion | PRD-RET-* |
| Security and Privacy | PRD-SEC-* |
| Performance Validation | PRD-PERF-* |
| Responsive / Basic Accessibility Behavior | PRD-UX-* |
| Product Observability for MVP Validation | PRD-OBS-* |
| Stage 02 Product/Portfolio Project Deliverables | Remain Stage 02 project obligations; product-facing portions are reflected across PRD groups, while repository/documentation/case-study artifacts remain outside the user-facing PRD |

This mapping is intentionally lightweight. Full bidirectional traceability belongs in the SRS/evaluation stages.

---

## 22. PRD Completion Checklist

- [x] All approved MVP scope areas are represented.
- [x] Explicit Stage 02 exclusions remain excluded.
- [x] Every major product feature has testable acceptance criteria.
- [x] Error behavior is defined.
- [x] Partial-processing behavior is defined.
- [x] Insufficient-evidence behavior is defined.
- [x] Native PDFs are covered.
- [x] Scanned PDFs and OCR are covered.
- [x] Mixed native/scanned PDFs are covered.
- [x] Arabic and English are first-class.
- [x] Mixed Arabic/English documents are covered.
- [x] The original PDF remains canonical.
- [x] Optional OCR-searchable derivatives cannot replace the canonical source.
- [x] Statistics extraction is useful but explicitly non-exhaustive.
- [x] Extracted and derived metrics are distinguishable.
- [x] Table guarantees remain conditional on reconstruction reliability.
- [x] Chart/graph numerical interpretation remains out of scope.
- [x] Single-document chat and document-only grounding are preserved.
- [x] Conversation history is not treated as evidence.
- [x] Citation behavior is explicit and statement/claim-oriented.
- [x] Multiple supporting passages/pages are supported where required.
- [x] Exact highlighting is conditional on reliable coordinates.
- [x] Yellow source highlighting is defined for reliable mappings.
- [x] Evidence Support semantics are separate from OCR/model/retrieval confidence.
- [x] Evidence Support is explicitly not factual-truth probability.
- [x] Unsupported claims are not downgraded to merely Low support.
- [x] Known limitations remain visible.
- [x] Security/privacy and complete document-specific deletion are preserved.
- [x] Existing-VPS/no-region-selection scope is preserved without specifying deployment architecture.
- [x] Performance values remain validation targets, not public SLAs.
- [x] Responsive desktop/mobile-web behavior is covered.
- [x] No database, API, provider/model, detailed RAG, verification algorithm, or deployment architecture was introduced.

---

## 23. Recommended Next Stage

# Stage 04 — Software Requirements Specification (SRS)

After this PRD is explicitly approved, Stage 04 should transform the approved product behavior into precise system requirements covering:

- functional requirements;
- non-functional requirements;
- system interfaces;
- data requirements;
- security requirements;
- performance requirements;
- reliability requirements;
- constraints;
- requirements traceability.

The SRS should define what the system must satisfy technically **without yet choosing the final architecture**.

**Do not proceed to Stage 04 until Stage 03 is explicitly approved.**
