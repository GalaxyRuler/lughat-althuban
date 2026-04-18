# Delivery Note: Packet 0005 core-translate-v1

**PR**: 6
**Branch**: packet/0005-core-translate-v1
**Implementation commit**: ebe4fe82bb610d75b7698c76b56e1690dc979cb4
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices
- Created `arabicpython/translate.py` implementing the second and final transformation step.
- Implemented an `O(n)` token walker using `tokenize.tokenize` and `tokenize.untokenize` which modifies only valid `NAME` tokens according to the current dialect.
- Ensured proper preservation of attribute semantics (e.g. replacing `.` followed by `NAME` correctly by looking into `dialect.attributes` vs `dialect.names`).
- Added robust error handling: propagating `SyntaxError` from `pretokenize` and catching `tokenize.TokenError` to translate it to `SyntaxError`.
- Created `tests/test_translate.py` with all 59 tests matching the spec perfectly, using the exact Arabic mapping values from the dictionaries (`ar-v1.md`).

## Deviations from the spec — anything you did differently and why; "None" if verbatim
None. The code perfectly conforms to the spec algorithm.

## Implementation notes worth remembering — non-obvious decisions
- To handle `untokenize` bytes conversion uniformly on Python versions that return `bytes`, `result_bytes.decode("utf-8")` was used and any resulting BOM (`\ufeff`) stripped.
- Tracked the last *significant* token to accurately deduce if a `NAME` token is an attribute to safely resolve method/attribute lookups vs global names.

## Validation — what you ran and the result
- `python -m pytest -v`: All 197 tests passed.
- `python -m ruff check .`: Clean.
- `python -m black --check .`: Clean.

## Open questions for the planner — anything ambiguous in the spec
None. The specs were comprehensive.

## Known limitations
- Harakat inside identifiers require Python 3.12+ (CPython 3.11 tokenizer limitation, not an apython bug).