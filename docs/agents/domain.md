# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Layout

This is a single-context repository.

- Read `CONTEXT.md` at the repo root before larger design, diagnosis, TDD, architecture, or product-shaping work.
- Read relevant ADR-style records from `decisions/` before changing language semantics, bidi handling, normalization, packaging, lexicon governance, or playground behavior.
- There is no `CONTEXT-MAP.md` and no `docs/adr/` directory in this repo.

## Use The Project Vocabulary

When output names a project concept, prefer the vocabulary in `CONTEXT.md` and the relevant ADRs. For Arabic terms, prefer the canonical terms in `lexicon/`.

If a needed concept is missing from `CONTEXT.md`, note the gap instead of inventing a conflicting term.

## Flag ADR Conflicts

If proposed work contradicts an existing decision in `decisions/`, surface the conflict explicitly and name the decision before changing the design.
