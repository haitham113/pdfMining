# Repository Guidelines

## Project Structure & Source of Truth

This repository currently contains planning documents only. `docs/Stage 00` records product discovery; Stages 01–02 define the feature brief and MVP scope; Stage 03 is the product requirements document (PRD); Stage 04 is the software requirements specification (SRS). Read them in stage order when changing scope or requirements. The PRD defines user-visible behavior, while the SRS expresses testable, implementation-neutral system requirements. Check each document's control table before treating a draft as approved. There are no source, test, or asset directories yet; their layout remains a later architecture decision.

## Build, Test, and Development Commands

No build system, runtime, package manager, formatter, or test command is configured. For document review, run `rg --files docs` to list deliverables and `rg -n 'PRD-|SRS-' docs` to inspect requirement references. Open the affected Markdown files and review their tables, links, and headings after edits. Add project-specific build and test commands here when implementation begins.

## Writing Style & Naming Conventions

Use Markdown headings, short paragraphs, and tables where requirements need IDs, priority, verification conditions, or source links. Keep stage filenames in the existing `Stage NN - PdfMining ... v0.1.md` pattern; avoid renaming published references casually. Preserve stable `PRD-...` and `SRS-...` IDs and traceability when revising requirements. In the SRS, use **shall** for mandatory behavior, **should** for expected behavior, and **may** for optional behavior.

## Verification Guidelines

There is no automated test suite or coverage threshold. For each requirement change, verify its acceptance or verification condition is observable, its PRD-to-SRS mapping remains accurate, and related scope, limitations, and terminology agree across stages. Review representative native, scanned, and mixed Arabic/English PDF cases when proposing later evaluation plans.

## Commits & Pull Requests

The current directory has no usable Git history, so no established commit-message convention can be inferred. Use concise, imperative subjects that name the changed stage, such as `Clarify Stage 04 citation requirements`. In a pull request, summarize the decision, list affected requirement IDs and source documents, explain traceability or scope changes, and record how the Markdown was reviewed. Include screenshots only when a rendered layout change needs visual review.

## Agent skills

### Issue tracker

Issues and specs are tracked in GitHub Issues for `haitham113/pdfMining`. See `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage labels. See `docs/agents/triage-labels.md`.

### Domain docs

Use a single-context layout with a root `CONTEXT.md` and `docs/adr/`. See `docs/agents/domain.md`.
