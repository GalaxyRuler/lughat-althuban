# Phase D Roadmap

**Status as of 2026-05-02:** Phase D is active. Phase C is complete and historical; see [`ROADMAP-PHASE-C.md`](ROADMAP-PHASE-C.md) for its shipped packet map. Phase D is governed by [`decisions/0012-phase-d-charter.md`](decisions/0012-phase-d-charter.md).

Theme: **AI & Reach** — make لغة الثعبان easier to discover, try, share, and use for modern AI-oriented Python work.

---

## Current phase gate

Phase D is complete when Tier 1 is shipped:

- D-001 web playground is publicly accessible and runs the built-in examples.
- D-002 AI SDK aliases are present and tested.
- D-003 reverse translator converts Python source into readable `.apy`.
- D-004 standard-library alias coverage is reconciled with the shipped lexicon.
- D-005 traceback localization reaches the Phase D CLI and message-policy bar.

Tier 2 work is useful during Phase D, but can ship after the Tier 1 gate.

---

## Tier 1 — Must Ship

| ID | Title | Status | Notes |
|---|---|---|---|
| D-001 | Web playground | shipped | `docs/playground.html` and `.github/workflows/pages.yml` are present. |
| D-002 | AI SDK Arabic aliases | shipped | `anthropic`, `openai`, `langchain-core`, `transformers`, and `sentence-transformers` are authored in `lexicon/libraries.toml`. |
| D-003 | Reverse translator: Python to لغة الثعبان | shipped CLI/API | Uses generated dialect reverse maps; playground reverse-translation UI remains a follow-up. |
| D-004 | Standard-library alias coverage reconciliation | shipped | Canonical D charter names live in `lexicon/libraries.toml` with compatible old names preserved where safe. |
| D-005 | Full traceback localization policy | shipped | CLI supports `--tracebacks=arabic|english|mixed` with generated exception/message data. |

---

## Tier 2 — Should Ship

| ID | Title | Status | Notes |
|---|---|---|---|
| D-006 | Integrated web tutorial | drafted | Tutorial page or playground tab with progressive lessons. |
| D-007 | Mobile-optimized playground / PWA | drafted | Offline manifest, service worker, and touch-friendly layout. |
| D-008 | Arabic Jupyter kernel improvements | drafted | Arabic display metadata, completion polish, and notebook UX. |
| D-009 | Arabic `pip` wrapper improvements | drafted | Clarify installation and package-management flows for learners. |
| D-010 | Example gallery page | shipped | `docs/gallery.html` links runnable examples into `playground.html?example=<id>` and lists local stdlib/AI examples. |
| D-011 | `[ai]` optional-dependency extra | shipped | `.[ai]` installs AI SDK alias dependencies for local examples and CI coverage. |

---

## Tier 3 — Future Vision

| ID | Title | Status |
|---|---|---|
| D-012 | Multi-dialect Arabic support | deferred |
| D-013 | Arabic AI pair programmer in the playground | deferred |
| D-014 | School curriculum pack | deferred |
| D-015 | Arabic package index | deferred |
| D-016 | Static type checking in Arabic | deferred |
| D-017 | Community and governance | deferred |

---

## Pickup advice

Start with D-002 or D-003 only after checking `lexicon/` and the alias invariant tests. Start with D-004 by auditing the shipped stdlib alias TOMLs first; do not rename shipped aliases without a compatibility plan. Start with D-005 by comparing ADR 0012 against `arabicpython/tracebacks.py`, `arabicpython/cli.py`, and `tests/test_tracebacks.py`.

For any new Arabic term, update `lexicon/` first, then regenerate derived docs and dictionaries.

---

## Reference files

- [`decisions/0012-phase-d-charter.md`](decisions/0012-phase-d-charter.md) — accepted Phase D charter.
- [`lexicon/README.md`](lexicon/README.md) — canonical naming and normalization governance.
- [`specs/INDEX.md`](specs/INDEX.md) — packet ledger and historical maps.
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — contributor workflow.
