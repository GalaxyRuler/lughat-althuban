# Dictionaries

This directory holds the canonical human-readable source of truth for every Arabic ↔ Python symbol mapping the dialect supports.

## Contents (planned)

| File | Contents | Status |
|---|---|---|
| `ar-v1.md` | Arabic keyword/builtin/exception table, v1 | not yet written |
| `ar-v1-alternates.md` | Candidate alternatives considered but rejected, with rationale | not yet written |

## Governance

Dictionary files are versioned separately from the package (see ADR 0003). A change to a dictionary file requires a new ADR if it alters an existing entry's translation. New entries for Python features not previously covered (e.g., `match` added in 3.10) do not require an ADR.

The machine-loadable form lives at `arabicpython/dialects/ar.py` and is generated from the markdown file by a build step. Do not edit the Python file directly; edit the markdown and regenerate.

## Format

Entries in `ar-v1.md` look like:

```
### if
- **Canonical**: إذا
- **Alternates considered**: لو, اذا
- **Rationale**: MSA-standard; matches Hedy; unambiguous in context.
```

## Phase ownership

Curating `ar-v1.md` is **planner work, not implementer work**. Claude writes it by hand in Packet 1.1 before any code is handed to Codex.
