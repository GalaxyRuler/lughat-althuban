# Delivery Note: Packet 0002 normalize-v1

**PR**: #3 (merged)
**Branch**: `packet/0002-normalize-v1` (deleted post-merge)
**Implementation commit**: `73fa2bf`
**Implementer**: Codex
**Reviewer**: Claude

## What shipped

- `arabicpython/normalize.py` — `normalize_identifier(s, *, strict=False) -> str`, ~40 LOC, stdlib-only (`unicodedata`).
- `tests/test_normalize.py` — all 43 spec-required tests, grouped as drafted (basic, NFKC, tatweel, harakat, hamza, alef maksura, ta marbuta, strict, idempotency, combined, dictionary cross-check, non-Arabic).

## Deviations from the spec

None. Public interface, pipeline order, test names and cases all match the packet verbatim.

## Implementation notes worth remembering

- Harakat set computed as `frozenset(chr(cp) for cp in range(0x064B, 0x0660)) | {U+0670}` — single module-level constant, no regex.
- Hamza fold uses `str.translate` with a precomputed translation table.
- Alef-maksura and ta-marbuta checks are `if`/`if` with early `return` in each branch, relying on mutual exclusivity of the two target characters.
- `test_dictionary_entries_idempotent` parses `dictionaries/ar-v1.md` with a plain `splitlines`/`split("|")` helper (no markdown dep). Minimum entry count asserted ≥ 150.

## Validation

- Local: `python -m ruff check .`, `python -m black --check .`, `python -m pytest` (44 passed incl. placeholder).
- CI: 9/9 matrix cells green (Linux/Windows/macOS × Python 3.11/3.12/3.13).

## Process note

Codex correctly did not write this delivery note in the PR because the planner handoff restricted edits to the two code paths. The handoff was over-restrictive relative to the spec's workflow step 7; written here on main post-merge instead. Future handoffs will name the delivery-note path explicitly in the allowed-edits list.

## Open questions for the planner

None.
