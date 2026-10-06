# PdfMining — Product / Feature Brief

## 1. Document Control

| Field | Value |
|---|---|
| Product | PdfMining |
| Document | Product / Feature Brief |
| Version | v0.1 |
| Status | Draft for approval |
| Source | Stage 00 Product Discovery Decision Summary |

---

## 2. Executive Summary

PdfMining is an AI-powered document intelligence product for professionals who need to investigate complex PDFs, extract useful information, ask questions, and verify exactly where important claims came from.

The product addresses a key weakness of ordinary “chat with PDF” tools: answers may sound useful while provenance, citation quality, extraction completeness, or source relationships remain unclear. PdfMining instead combines document understanding, structured extraction, grounded AI interaction, evidence verification, and exact navigation back to the original document.

Its primary value proposition is **trust through verifiable evidence**. Users should be able to understand, extract, question, and verify information from Arabic, English, and mixed-language PDFs without losing the connection between an answer and its original supporting evidence.

---

## 3. Product Vision

PdfMining should become an evidence-first document intelligence platform that enables professionals to investigate complex documents as structured, searchable, conversational knowledge while preserving exact traceability to the original source.

Long term, the product should support broader professional document-analysis workflows, larger document sets, and collaborative business use without weakening the core principle that important outputs must remain verifiable against original evidence.

The defining product principle is:

> **Trustworthiness and traceability are more important than generative fluency.**

---

## 4. Problem Statement

Professionals working with information-heavy PDFs face several recurring problems:

- Important facts, statistics, KPIs, tables, and conclusions can be difficult and time-consuming to locate manually.
- Scanned documents may contain little or no usable text layer, making search and extraction difficult.
- Arabic, English, and mixed-language documents require reliable multilingual handling.
- Generic PDF-chat products may provide plausible answers without a clear or trustworthy relationship to the supporting source.
- A citation to a page is often insufficient when the user needs to know the exact supporting passage or region.
- Users may need to distinguish directly extracted values from values calculated or inferred from document evidence.
- Complex tables and degraded scans can make extraction incomplete or uncertain.
- AI-generated output can be misleading when uncertainty, insufficient evidence, or extraction limitations are hidden.

PdfMining exists to reduce the effort required to investigate PDFs while increasing the user’s ability to verify results.

---

## 5. Target Users

### 5.1 Primary MVP Users

The MVP targets **individual professionals working with information-heavy documents**, including analysts, consultants, researchers, engineers, managers, and other business professionals.

Typical documents include business reports, financial or operational reports, tenders and specifications, and research/report-style PDFs.

Their main pain points are:

- locating important information inside long or complex documents;
- extracting statistics, KPIs, and tables;
- working with scanned or multilingual PDFs;
- verifying whether an AI answer is actually supported;
- tracing claims back to exact source evidence.

PdfMining provides these users with structured extraction, grounded document Q&A, evidence-aware citations, and direct navigation to the supporting source.

### 5.2 Secondary / Future Users

Stage 00 did not define a separate secondary MVP audience.

The approved product trajectory is to evolve from private single-user accounts toward **business teams and organizations** after the MVP. Team collaboration and organization-level behavior are therefore future scope, not part of the initial target-user definition.

PdfMining is not positioned as a casual consumer PDF chatbot.

---

## 6. Primary Use Cases

The primary job to be done is:

> **Investigate complex PDFs and verify exactly where answers, facts, metrics, and conclusions came from.**

Primary user outcomes include:

- upload and process a supported PDF;
- inspect a concise overview of the document;
- locate and review extracted statistics and KPIs;
- inspect structured tables where reliable reconstruction is possible;
- distinguish extracted values from derived metrics;
- ask natural-language questions about the document;
- ask contextual follow-up questions;
- inspect statement-level supporting citations;
- review multiple supporting passages when a claim requires more than one source;
- navigate directly to the relevant page and source region;
- view highlighted supporting evidence in the original PDF;
- understand whether evidence support is High, Medium, or Low;
- compare conflicting values within the same document;
- identify repeated evidence;
- export structured statistics with provenance;
- analyze Arabic, English, and mixed-language PDFs, including scanned documents.

---

## 7. Core User Journey

The primary MVP journey is:

```text
User signs in
→ uploads a PDF
→ provides a password if the PDF is protected
→ PdfMining processes the document
→ processing state and any partial failures remain visible
→ user reviews the document overview and extracted information
→ user filters/searches statistics or inspects reconstructed tables
→ user asks a document question
→ PdfMining returns a document-grounded answer
→ factual claims include statement-level evidence where appropriate
→ user inspects Evidence Support and source passages
→ user navigates to the original PDF page and highlighted source region
→ user optionally exports structured statistics with provenance
```

For desktop use, the primary experience is a document-centered split-screen workspace with the PDF visible alongside analysis/chat. On mobile, the experience should use responsive switchable views rather than forcing the desktop layout.

A successful capability should remain usable when another processing capability fails.

---

## 8. MVP Feature Set

### 8.1 Account and Document Management

- **Authenticated single-user accounts** — provide private access to each user’s documents and analysis history.
- **Private document history** — allow users to return to previously processed documents until they delete them.
- **Secure per-user isolation** — prevent document data, extracted content, retrieval, chat, statistics, and citations from crossing user boundaries.
- **Complete document-specific deletion** — allow a user to delete a document and its associated derived artifacts, conversations, and evidence data.

### 8.2 PDF Processing

- **PDF-only upload support** — focus the MVP on a single document type.
- **Native, scanned, and mixed native/scanned PDFs** — support representative professional PDFs rather than text-only files.
- **Password-protected PDFs** — process them when the user provides the valid password; encryption bypass is not supported.
- **Common page-rotation handling** — reduce avoidable processing errors caused by common rotations.
- **Configurable document limits** — begin with an initial 20-page maximum and approximately 25 MB file-size target.
- **Structured internal representation** — represent extracted document structure in a normalized form while preserving the original PDF unchanged.
- **Partial-processing support** — keep successful capabilities usable when another processing step fails.
- **Visible processing states and failures** — communicate progress, errors, and known limitations instead of hiding them.

### 8.3 OCR and Multilingual Support

- **Arabic, English, and mixed-language content** — treat both supported languages as first-class MVP requirements.
- **OCR where required** — extract usable text and source coordinates from scanned pages rather than assuming OCR is needed for the entire document.
- **OCR quality/confidence disclosure** — make poor OCR quality visible so downstream uncertainty is understandable.
- **Mixed native/scanned page handling** — process OCR selectively where needed within the same PDF.
- **Explicit handwriting limitation** — handwriting understanding is not supported in the MVP.

### 8.4 Structured Statistics / KPI Extraction

- **Automatic statistics and KPI extraction** — surface useful quantitative facts without requiring the user to find every value manually.
- **Structured table extraction where reliable** — reconstruct tables only when the result is sufficiently trustworthy.
- **Derived metric calculations** — calculate useful metrics when justified by document evidence and label them explicitly as derived rather than extracted.
- **Statistics filtering and search** — help users locate relevant extracted metrics.
- **Concise automatic document overview** — provide a quick orientation to the document before deeper investigation.
- **Provenance preservation** — keep extracted or derived information connected to its supporting source.

### 8.5 Document Chat

- **Document-grounded Q&A** — answer questions using the uploaded document as the evidence source.
- **Conversation-aware follow-up questions** — use conversational context to interpret what the user means.
- **Document-only evidence policy** — do not silently fill evidence gaps with external model knowledge.
- **Insufficient-evidence behavior** — explain what can and cannot be established when the document does not provide enough support.
- **Arabic and English interaction** — support natural-language responses in the approved languages.

### 8.6 Citations and Evidence Support

- **Statement/claim-level citations** — connect document-derived factual claims to their supporting evidence.
- **Multiple citations where required** — support claims whose evidence spans multiple passages or pages.
- **Minimal sufficient evidence set** — show the smallest set of sources needed to support the claim while allowing additional supporting evidence where useful.
- **Evidence verification** — assess whether the selected evidence actually supports the generated claim.
- **High / Medium / Low Evidence Support** — communicate support strength without implying misleading probability or generic model confidence.
- **Unsupported-claim control** — normally remove unsupported factual claims before they are shown.
- **Uncertain wording for Medium support** — ensure the language of the answer reflects inference or uncertainty where appropriate.

### 8.7 PDF Viewer and Source Navigation

- **Original-PDF viewing** — display the original uploaded document as the canonical visual source.
- **Exact page navigation** — take the user directly to the page containing the cited evidence.
- **Source-region navigation** — locate the specific supporting region or span when reliable coordinates exist.
- **Yellow evidence highlighting** — visually highlight cited evidence inside the viewer.
- **Coordinate honesty** — do not present an exact-location citation when reliable source coordinates cannot be established.

### 8.8 Export

- **CSV export** — export structured statistics in a reusable format.
- **Excel export** — provide spreadsheet-compatible structured output.
- **Provenance in exports** — preserve enough source information for exported statistics to remain traceable to document evidence.

### 8.9 User Experience

- **Document-centered desktop workspace** — keep the PDF visible alongside chat and analysis, with statistics available through appropriate panels or tabs.
- **Responsive mobile behavior** — use switchable views suitable for smaller screens.
- **Meaningful processing states** — communicate states such as Uploaded, Extracting, OCR if required, Analyzing, and Ready.
- **Graceful degradation** — preserve usable results when another capability fails.
- **Visible errors and limitations** — clearly disclose partial failures, poor OCR, unsupported content, and known extraction limitations.

---

## 9. PDF Handling Principle

The **original uploaded PDF always remains unchanged and is the source of truth**.

PdfMining does not normalize every upload by regenerating it into a replacement PDF. Instead, it creates a normalized internal document representation containing the structure required for analysis, which may include pages, text blocks and spans, reading order, bounding boxes, tables, images, OCR output, source coordinates, and extraction confidence.

For **native/text-based PDFs**, PdfMining uses the original PDF and maps extracted information and citations back to original page coordinates.

For **scanned PDFs**, PdfMining preserves the original file, performs OCR where needed, retains OCR text, reading order, coordinates, and confidence, and uses OCR coordinates for citation overlays.

PdfMining may optionally generate a searchable PDF derivative with an invisible OCR text layer as a convenience artifact. Such a derivative must never replace the original PDF or become the canonical citation source.

The viewer therefore presents the original PDF and renders citation/highlight overlays using stored source coordinates.

---

## 10. AI Product Behavior

PdfMining’s AI behavior should follow these product rules:

- Answers must be grounded in evidence from the uploaded document.
- External model knowledge must not silently fill missing evidence.
- Conversation history may clarify user intent but is not evidence.
- Document-derived factual claims should be traceable to supporting evidence where appropriate.
- Unsupported factual claims should normally be removed before presentation.
- When sufficient evidence does not exist, PdfMining should state what can and cannot be established.
- Evidence Support must represent how strongly selected evidence supports a specific generated claim.
- Evidence Support must not be presented as vector similarity, generic model confidence, or probability that a claim is universally true.
- OCR confidence and Evidence Support are separate concepts and must not be conflated.
- Arabic and English interaction should be supported as first-class product behavior.
- Document content must be treated as untrusted data; prompt-like instructions inside a PDF must not override application behavior or isolation rules.
- AI-related limitations and uncertainty should be communicated rather than concealed.

---

## 11. Citation and Evidence Experience

A document-derived claim should resolve conceptually through:

**Document → Page → Source Region / Span → Source Text → Coordinates**

From the user’s perspective:

- factual claims can carry statement-level citations;
- selecting a citation reveals the supporting source passage;
- the user can navigate directly to the relevant page;
- when reliable coordinates exist, the exact source region is highlighted in yellow;
- a claim may cite one passage, several passages, or evidence across multiple pages;
- the interface should prioritize the minimal sufficient supporting evidence while allowing additional evidence to be inspected where useful;
- each claim may display **High**, **Medium**, or **Low Evidence Support**;
- Low or uncertain support must not be presented with stronger language than the evidence justifies;
- unsupported factual claims should normally be withheld rather than displayed as confident answers;
- when exact coordinate mapping is unreliable, PdfMining must disclose the limitation rather than simulate precise highlighting.

The purpose of this experience is not merely to show citations, but to let the user evaluate whether the answer is actually supported.

---

## 12. Product Differentiators

PdfMining differs from a generic PDF chatbot through the following product characteristics:

1. **Evidence-first trust model** — verification and traceability take priority over fluent but unsupported answers.
2. **Statement-level source traceability** — important claims connect to specific supporting evidence rather than only a document or page.
3. **Exact original-source navigation** — users can move from a claim to the original PDF page and highlighted source region when coordinates are reliable.
4. **Evidence Support classification** — users see whether selected evidence strongly, moderately, or weakly supports a claim without misleading probability-style confidence.
5. **First-class Arabic, English, and mixed-language support** — multilingual professional documents are part of the core MVP rather than an afterthought.
6. **Native, scanned, and mixed-PDF handling** — OCR and source-coordinate preservation support investigation beyond text-native documents.
7. **Structured extraction with provenance** — statistics, KPIs, tables, and derived metrics remain connected to original evidence and can be exported with provenance.

---

## 13. MVP Boundaries

### 13.1 In Scope for MVP

The MVP includes:

- authenticated private single-user accounts;
- secure document history and complete document-specific deletion;
- PDF-only uploads;
- initial configurable limits of 20 pages and approximately 25 MB;
- native, scanned, and mixed native/scanned PDFs;
- password-protected PDFs when the user supplies the password;
- common page-rotation handling;
- Arabic, English, and mixed-language documents;
- OCR with quality/confidence disclosure;
- normalized internal document representation;
- structured table extraction where reliable;
- automatic statistics/KPI extraction;
- explicitly labeled derived metrics;
- concise automatic document overview;
- grounded document chat and contextual follow-up questions;
- statement-level citations and multiple citations where needed;
- exact source highlighting when coordinates are reliable;
- citation/evidence verification;
- High / Medium / Low Evidence Support;
- statistics filtering/search;
- CSV/Excel export with provenance;
- partial-processing behavior, visible errors, and explicit limitations.

### 13.2 Post-MVP / Future Scope

Approved future directions or candidates include:

- business teams and organizations;
- team collaboration;
- document collections/workspaces;
- multi-document chat;
- very large-document support;
- support for additional document formats;
- configurable regional data residency;
- broader scale and higher concurrency;
- future behavior for organization-level document and access management.

These items remain subject to later discovery and scope decisions.

### 13.3 Explicitly Out of Scope

The MVP does not include:

- handwriting understanding;
- numerical interpretation of charts or graphs;
- arbitrary multimodal diagram understanding;
- full BI/dashboard functionality;
- external web or general-knowledge answers as evidence;
- enterprise compliance certification claims such as HIPAA or government certification;
- editable canonical evidence;
- password or encryption bypass;
- guaranteed extraction completeness;
- perfect reconstruction of arbitrarily complex tables.

---

## 14. Key Product Principles

Future requirements and designs should preserve the following principles:

- **The original uploaded PDF is the canonical source of truth.**
- **Trustworthiness and traceability take priority over generative fluency.**
- **Document-derived factual claims should remain verifiable against source evidence.**
- **Insufficient evidence should be acknowledged rather than silently filled with model knowledge.**
- **Evidence Support and OCR confidence are different concepts.**
- **Exact highlighting should be shown only when source coordinates are reliable.**
- **Arabic and English are first-class product languages.**
- **Extracted and derived metrics must be distinguishable.**
- **Partial processing should degrade gracefully rather than invalidate all successful results.**
- **Known limitations and uncertainty should remain visible to the user.**
- **Document content is untrusted data and must not control application behavior.**
- **Private user data and derived artifacts must remain isolated by user.**
- **Provider choices should remain replaceable where possible; product behavior should not depend on a single provider being permanent.**

---

## 15. Success Criteria

### 15.1 Product Success

The MVP is successful at the product level when:

- a user can complete the end-to-end workflow from upload through extraction, Q&A, evidence inspection, source navigation, and optional export;
- representative Arabic, English, and mixed-language PDFs can be investigated effectively;
- scanned and native PDFs can participate in the same core user workflow;
- extracted statistics/KPIs and reliable tables are useful enough to reduce manual document investigation;
- users can distinguish extracted values from derived metrics;
- citations are understandable and let users trace important claims back to source evidence;
- exports preserve usable provenance;
- limitations and partial failures are understandable rather than hidden.

### 15.2 Quality Success

The MVP is successful at the quality level when:

- grounding and citation correctness remain the highest product priority;
- source navigation reliably reaches the correct page and exact region when coordinates are available;
- the product does not pretend exact coordinate certainty when mapping is unreliable;
- OCR quality is disclosed and poor OCR appropriately reduces downstream certainty;
- unsupported questions are handled by explaining insufficient evidence;
- unsupported factual claims are normally filtered before presentation;
- High / Medium / Low Evidence Support can be calibrated through later empirical validation rather than arbitrary thresholds;
- partial failures do not unnecessarily block successful capabilities.

The following Stage 00 performance values remain **validation targets, not public SLAs**:

- typical native PDF processing for a document within the initial limit: roughly 30–60 seconds;
- OCR-heavy PDF processing: target roughly 2–3 minutes;
- typical chat question: approximately 5–10 seconds;
- preliminary engineering validation scenario: approximately 10 simultaneously active users.

Grounding quality should not be silently sacrificed merely to meet latency targets.

### 15.3 Portfolio Success

Because PdfMining is also intended to serve as a flagship AxioStack AI portfolio project, it should be able to demonstrate credibly that it can:

- process representative native, scanned, Arabic, English, and mixed-language PDFs;
- extract structured information with visible provenance;
- answer questions using document evidence;
- verify claim/evidence relationships;
- navigate users from generated claims to exact original evidence when reliable coordinates exist;
- communicate uncertainty, OCR limitations, unsupported questions, and partial failures clearly;
- show an evidence-first workflow that is visibly more trustworthy than a generic PDF-chat demonstration.

Portfolio demonstrations should present real product limitations honestly rather than implying unsupported completeness or accuracy guarantees.

---

## 16. Assumptions and Constraints

### 16.1 Confirmed MVP Constraints

- The MVP supports PDFs only.
- The initial configurable limit is 20 pages.
- The initial file-size target is approximately 25 MB.
- Large-document support is post-MVP.
- The product supports Arabic, English, and mixed-language content.
- Handwriting is not supported.
- Chart/graph numerical interpretation and arbitrary diagram understanding are not included.
- MVP accounts are private and single-user.
- Answers are document-only grounded.
- External AI providers may be used.
- Only the minimum necessary document content should be sent to external providers.
- Provider configurations should preferably avoid model training on submitted data and minimize or disable retention where available.
- Documents remain stored until explicitly deleted by the user.
- Document-specific deletion should remove the original PDF and associated document-derived artifacts and conversations.
- Data should be encrypted in transit and at rest.
- Operational logs should minimize document content and exclude secrets such as PDF passwords.
- Strict per-user isolation applies to original files and derived data.
- The MVP will be hosted on the project's existing VPS.
- The MVP will not offer hosting-region selection, multi-region deployment, or configurable data residency.
- The physical hosting location is an infrastructure fact to disclose where relevant, not a user-selectable product feature.
- The MVP does not claim regulated-industry or enterprise compliance certification.

### 16.2 Working Assumptions Requiring Validation

- The approved initial document limits are sufficient to demonstrate the core value proposition.
- Representative professional PDFs within those limits can be processed within the provisional performance targets.
- Table reconstruction will be useful when the product limits output to sufficiently reliable cases.
- High / Medium / Low Evidence Support can be meaningfully calibrated through empirical validation.
- The combination of OCR, retrieval, generation, and verification can be operated at a cost acceptable for the intended product direction.

These assumptions should be tested rather than converted prematurely into guarantees.

---

## 17. Product Risks

| Risk | Product Impact | Mitigation Direction |
|---|---|---|
| OCR accuracy | Arabic, degraded scans, unusual layouts, or mixed-language pages may produce incorrect or incomplete text. | Expose OCR quality/confidence, propagate uncertainty, and avoid overstating downstream accuracy. |
| Complex table reconstruction | Merged cells, visual layouts, and scanned tables may be reconstructed incorrectly. | Return structured tables only when reconstruction is sufficiently reliable and disclose limitations. |
| Citation correctness | A correct answer with an incorrect page or highlight would undermine the core differentiator. | Treat citation/source mapping as a primary quality criterion and suppress false precision. |
| Evidence calibration | High / Medium / Low labels could mislead users if poorly calibrated. | Validate labels empirically and define them as evidence support rather than generic confidence. |
| Extraction completeness | Automatic KPI/statistic detection may miss relevant values. | Avoid completeness guarantees and make extraction limitations visible. |
| Verification latency | Evidence verification can increase response time. | Preserve grounding quality as the priority and validate acceptable responsiveness. |
| Model/provider variation | OCR, retrieval, generation, or verification changes may alter results between processing versions. | Keep product behavior provider-independent where practical and make quality changes measurable. |
| Processing cost | OCR plus extraction, retrieval, answering, and verification may cost more than ordinary PDF chat. | Validate cost against actual representative workloads before commercial commitments. |
| Prompt injection inside documents | Malicious or instruction-like PDF content could attempt to manipulate model behavior. | Treat document contents as untrusted evidence and preserve application rules and user isolation. |
| Poor coordinate mapping | Exact highlighting may be unavailable or inaccurate for some documents. | Show exact-location citations only when coordinates are reliable; otherwise disclose the limitation. |

---

## 18. Open Questions

No unresolved product-level questions remain from Stage 01.

The previously provisional items have been resolved as follows:

- **Performance SLAs** — current processing/chat timings remain non-binding validation targets. Formal SLAs will be considered only after benchmarking the implemented MVP.
- **Accuracy thresholds** — quality dimensions and evaluation methods will be defined, but numeric acceptance thresholds will be set only after benchmarking representative Arabic, English, native, scanned, and mixed PDFs.
- **Evidence Support calibration** — High / Medium / Low remain the MVP user-facing labels; their internal thresholds will be empirically calibrated using representative claim/evidence evaluation data.
- **Provider/model selection** — PdfMining remains provider-independent at the product level. Concrete OCR, embedding, LLM, reranking, and verification technologies will be selected during Technical Design / implementation evaluation based on measured quality, cost, latency, privacy, and maintainability.
- **Long-term pricing** — final pricing is deferred until MVP unit economics and user-value validation are available. Any earlier pricing model is provisional.
- **Hosting** — the MVP will run on the project's existing VPS. No hosting-region selection, multi-region deployment, or configurable data residency is included in MVP.
- **Future large-document limits** — large-document support remains post-MVP, and future page/file-size limits will be defined only after benchmarking the MVP on the actual hosting environment.
- **Future team/organization behavior** — team and organization capabilities remain post-MVP and will receive separate product discovery before their detailed behavior is defined.

> **No product-level blockers remain for proceeding to the Project/Product Scope stage.**

---

## 19. Recommended Next Stage

The recommended next stage is:

**Stage 02 — Project / Product Scope**

Stage 02 should convert the approved product direction into precise project boundaries. It should establish:

- exact MVP scope boundaries;
- required deliverables;
- explicit exclusions;
- project constraints;
- dependencies;
- validation assumptions;
- the release boundary for the first MVP.

Stage 02 should preserve the decisions in this brief without prematurely defining database schemas, API endpoints, infrastructure topology, detailed service boundaries, implementation libraries, or other Technical Design decisions.
