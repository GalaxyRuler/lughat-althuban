# Dictionaries

This directory holds the canonical human-readable source of truth for every Arabic ↔ Python symbol mapping the dialect supports.

## Contents

| File | Contents | Status |
|---|---|---|
| `ar-v1.md` | Arabic keyword/builtin/exception table, v1 | locked (Phase A ship; ar-v1.0) |
| `exceptions-ar-v1.md` | Exception subclass hierarchy + interpreter-message translations | locked (Phase A ship) |
| `REVIEW-2026-04-19.md` | Planner-only sanity review of `ar-v1.md` | informational |

## Governance

Dictionary files are versioned separately from the package (see ADR 0003).

- **Frozen rule.** Per ADR 0008 § B.0, `ar-v1` is now permanently frozen for the lifetime of Phase A. Any change that would alter an existing entry's translation requires a new ADR superseding ADR 0008's freeze.
- **Allowed in-place under the freeze**: doc-hygiene corrections (typos, header status, count math), cosmetic rendering normalization, and *additions* for Python features not previously covered (e.g., a future `match` extension would be additive). See ADR 0003 for the additions carve-out.
- **Future versions** (`ar-v2`, etc.) are charter material for a superseding ADR. The Category D items in `REVIEW-2026-04-19.md` are the current best inputs to that charter.

## How the dictionary is loaded

`arabicpython.dialect.load_dialect("ar-v1")` parses `ar-v1.md` directly at load time — there is no generated Python sidecar. The loader walks the markdown tables, normalizes each canonical entry through `arabicpython.normalize.normalize_identifier`, and produces two frozen mappings:

- `dialect.names` (144 entries) — keywords, soft keywords, literals, types, built-in functions, exceptions
- `dialect.attributes` (29 entries) — methods on built-in types

Translation lookups consult these mappings; nothing is generated, regenerated, or built. Editing `ar-v1.md` and re-running the package picks up changes (subject to the frozen-rule constraints above).

## Format

Entries are rendered as markdown tables with four columns: Python symbol, Canonical Arabic, Alternates considered (informational only — not loaded), and Rationale. Multi-word translations use `_` (not space) because Python's tokenizer treats space as a token boundary. Method entries are rendered with a leading `.` for clarity but stored without it.

## Phase ownership

`ar-v1` was authored by the planner (Claude) in spec packet 0001 and has been live in every released package version. It is now frozen. Subsequent dictionary versions require a superseding ADR per the rules above.
