# Domain Docs

This repository uses a single-context layout: a root `CONTEXT.md` for domain terms and `docs/adr/` for architecture decisions.

## Before exploring

Read `CONTEXT.md` if it exists. Read ADRs in `docs/adr/` that relate to the work. For scope and requirements, read the existing stage documents in order, from Stage 00 through Stage 04, and check each document's control table before treating a draft as approved.

If `CONTEXT.md` or `docs/adr/` does not exist, proceed without flagging its absence. Create domain docs when terms or decisions are resolved.

## Layout

    /
    ├── CONTEXT.md
    └── docs/
        └── adr/
            └── 0001-example-decision.md

Use terms defined in `CONTEXT.md` in issues, proposals, and tests. If a term is missing, reconsider it or record the gap for domain modeling. Surface any conflict with an existing ADR explicitly.
