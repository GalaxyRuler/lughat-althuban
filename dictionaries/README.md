# Dictionaries

This directory holds the canonical human-readable source of truth for every Arabic ↔ Python symbol mapping the dialect supports.

## Contents

| File | Contents | Status |
|---|---|---|
| `ar-v1.md` | Arabic keyword/builtin/exception table, v1 | locked (Phase A ship; ar-v1.0) |
| `exceptions-ar-v1.md` | Exception subclass hierarchy + interpreter-message translations | locked (Phase A ship) |

## Governance

Dictionary files are versioned separately from the package (see ADR 0003).

- **Frozen rule.** `ar-v1` is permanently frozen. Any change that would alter an existing entry's translation requires a new ADR.
- **Allowed in-place under the freeze**: doc-hygiene corrections (typos, header status, count math), cosmetic rendering normalization, and *additions* for Python features not previously covered (e.g., a future `match` extension would be additive). See ADR 0003 for the additions carve-out.
- **Future versions** (`ar-v2`, etc.) require a new ADR.

## How the dictionary is loaded

`arabicpython.dialect.load_dialect("ar-v1")` parses `ar-v1.md` directly at load time — there is no generated Python sidecar. The loader walks the markdown tables, normalizes each canonical entry through `arabicpython.normalize.normalize_identifier`, and produces two frozen mappings:

- `dialect.names` (144 entries) — keywords, soft keywords, literals, types, built-in functions, exceptions
- `dialect.attributes` (29 entries) — methods on built-in types

Translation lookups consult these mappings; nothing is generated, regenerated, or built. Editing `ar-v1.md` and re-running the package picks up changes (subject to the frozen-rule constraints above).

## Format

Entries are rendered as markdown tables with four columns: Python symbol, Canonical Arabic, Alternates considered (informational only — not loaded), and Rationale. Multi-word translations use `_` (not space) because Python's tokenizer treats space as a token boundary. Method entries are rendered with a leading `.` for clarity but stored without it.

