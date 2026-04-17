# Spec Packet 0003: dialect-loader-v1

**Phase**: A
**Depends on**: Packet 0002 (`normalize_identifier`), ADR 0003 (dictionary governance), Packet 0001 (`dictionaries/ar-v1.md`)
**Estimated size**: medium (one focused Codex session)
**Owner**: Codex

## Goal

Parse `dictionaries/ar-v1.md` at runtime and expose an immutable `Dialect` object that the transpiler consults for every `NAME` token. The loader applies `normalize_identifier` to every Arabic key so that user source code and the shipped dictionary meet at the same canonical form.

This is the second of the three foundation pieces (normalize → dialect → pretokenize). After this packet, the lookup table that every other Phase A feature relies on is available as a single function call: `load_dialect()`.

## Non-goals

- Does NOT integrate with Python's tokenizer (Packet 0004).
- Does NOT implement the `# apython: strict` pragma (later).
- Does NOT support dialects other than `ar-v1`. The API is designed to extend to `ar-v2`, `ur-v1`, etc., but this packet ships only ar-v1. A second dialect is a future packet.
- Does NOT handle soft keywords, compound keywords (`yield from`), or f-string internals. Those are transpiler concerns.
- Does NOT enforce that Python targets are valid Python identifiers beyond a sanity regex. We trust the dictionary curator.
- Does NOT cache across processes. A single in-process `functools.lru_cache` on `load_dialect(name)` is fine.

## Files

### Files to create

- `arabicpython/dialect.py`
- `tests/test_dialect.py`
- `tests/fixtures/dialect_malformed.md` — a small fixture file used by the malformed-dictionary tests (see Tests §9).

### Files to read (do not modify)

- `dictionaries/ar-v1.md` — the shipped dialect.
- `arabicpython/normalize.py` — call `normalize_identifier` on every Arabic key.
- `decisions/0003-keyword-dictionary.md` — governance.
- `decisions/0004-normalization-policy.md` — normalization contract.

## Public interface

```python
from dataclasses import dataclass
from typing import Mapping


class DialectError(ValueError):
    """Raised when a dictionary file cannot be parsed or is internally inconsistent."""


@dataclass(frozen=True)
class Dialect:
    """Immutable snapshot of an apython dialect.

    All Arabic keys in `names` and `attributes` are stored in their NORMALIZED
    form (per ADR 0004). Callers look up by passing a user-written Arabic token
    through `normalize_identifier` first, then indexing these maps.

    `reverse_names` and `reverse_attributes` map Python symbol back to the
    canonical (non-normalized) Arabic form from the dictionary, for use in
    error messages and translated tracebacks.

    `categories` tags each normalized Arabic key with its dictionary section
    ("keyword" | "literal" | "type" | "function" | "exception" | "method") so
    the transpiler can apply category-specific rules (e.g., soft keywords are
    not substituted if they appear as ordinary identifiers in scope).

    Attributes:
        name: dialect identifier, e.g., "ar-v1".
        names: maps Arabic (normalized) → Python, for NAME tokens NOT preceded by `.`.
        attributes: maps Arabic (normalized) → Python, for NAME tokens preceded by `.`.
        reverse_names: Python → Arabic canonical, for reverse lookup.
        reverse_attributes: Python → Arabic canonical, for reverse lookup.
        categories: Arabic normalized → category string.
    """
    name: str
    names: Mapping[str, str]
    attributes: Mapping[str, str]
    reverse_names: Mapping[str, str]
    reverse_attributes: Mapping[str, str]
    categories: Mapping[str, str]


def load_dialect(name: str = "ar-v1", *, path: "Path | None" = None) -> Dialect:
    """Parse a dialect dictionary and return an immutable Dialect.

    If `path` is None, looks up `dictionaries/<name>.md` relative to the
    installed `arabicpython` package's project root (use
    `importlib.resources` or `Path(__file__).parent.parent`).

    Call sites should not pass `path`; it exists for tests and fixtures.

    Caches on `(name, path)` via `functools.lru_cache`.

    Raises:
        DialectError: if the file is missing, malformed, or internally inconsistent.
        FileNotFoundError: if the path does not exist.
    """
```

## Parsing rules

The dictionary is a Markdown file with six data sections. Section titles (H2) identify categories:

| H2 heading starts with | Category tag | Target map |
|---|---|---|
| `## 1. Control-flow keywords` | `keyword` | `names` |
| `### Soft keywords` (sub-section of §1) | `keyword` | `names` |
| `## 2. Literal keywords` | `literal` | `names` |
| `## 3. Built-in types` | `type` | `names` |
| `## 4. Built-in functions` | `function` | `names` |
| `## 5. Built-in exceptions` | `exception` | `names` |
| `## 6. Common methods on built-in types` | `method` | `attributes` |

Sections outside that set (`## Reading this file`, `## Collision audit`, `## Counts`, `## Known omissions`, `## References`) are ignored for data extraction. The loader must still handle their presence without crashing.

A data row is a Markdown table line matching all of:

- Starts with `|` and ends with `|`.
- Has exactly 4 cells after splitting on `|` and stripping the leading/trailing empty cells.
- Cell 1 is a Python symbol wrapped in backticks: `` `if` ``, `` `.append` ``, etc.
- Cell 2 is a non-empty Arabic canonical.
- Cell 3 is either `—` (em dash) or a comma-separated list of alternates (ignored by the loader).
- Cell 4 is free-form rationale (ignored by the loader).

Header rows (`| Python | Canonical | Alternates | Rationale |`) and separator rows (`|---|---|---|---|`) are skipped by shape (all cells are `Python`/`Canonical`/etc. strings, or all cells are dashes).

### Canonicals and reverse mapping

- **Forward key**: apply `normalize_identifier(arabic_canonical)`. Store in `names` or `attributes` depending on category.
- **Forward value**: the Python symbol, with the leading `.` stripped if present (methods are stored as plain identifiers).
- **Reverse key**: the Python symbol (same stripping).
- **Reverse value**: the ORIGINAL Arabic canonical from the file, NOT the normalized form. This is the display form for error messages.

### Validation

Raise `DialectError` (with a clear message and the offending source line number) if any of:

1. A data row has fewer or more than 4 cells after stripping.
2. The Python cell is not wrapped in backticks.
3. The Python cell after unwrapping is empty.
4. The Arabic canonical cell is empty.
5. After normalization, an Arabic key appears twice in the SAME map (`names` or `attributes`). Cross-map collisions are allowed (a method `عد` and a function `عد` can coexist — they disambiguate by `.` context).
6. Two Python symbols in the SAME map map from DIFFERENT normalized Arabic keys. (One Arabic form must have exactly one Python target within a map.)
7. Total entries below 150 (a sanity floor — protects against silent parse failure).
8. A data row is encountered before any recognized H2/H3 heading (category must always be known).

Do NOT raise on:
- Trailing whitespace on lines.
- Empty lines between rows.
- Unknown H2 sections (ignore their rows entirely — their content is not interpreted).

## Implementation constraints

- **Dependencies**: stdlib only (`pathlib`, `re`, `functools`, `dataclasses`, `importlib.resources` acceptable).
- **Python version**: 3.11+.
- **Purity**: `load_dialect` performs I/O; everything else must be pure. The returned `Dialect` is frozen; the `Mapping` values should be `types.MappingProxyType` wrapping `dict` (read-only views).
- **Performance**: parsing the 174-entry ar-v1 file must complete well under 10 ms. Do not use a full Markdown parser; a 50–80 line line-by-line scanner is appropriate.
- **Style**: pass `ruff check .` and `black --check .` at project defaults.
- **No dependencies on tokenize, ast, or compile**. This module is pure data loading.

## Implementation hints

- Use a small state machine: walk lines, track `current_category`, classify each line as (heading | separator | data-row | other), act accordingly.
- Table cell split: `[c.strip() for c in line.strip().strip("|").split("|")]`. This yields 4 cells for a well-formed row.
- Use a regex like `^`(?P<sym>[^`]+)`$` on the first cell to unwrap backticks; reject rows that don't match.
- A method row's first cell is `` `.append` ``, `` `.encode` ``, etc. Detect the leading dot when classifying and strip it before storing.
- `types.MappingProxyType(dict_)` gives you a read-only view without copying. Use it for each of the 5 mapping attributes on `Dialect`.
- `@functools.lru_cache(maxsize=8)` on `load_dialect`. Note that `Path` is hashable, so `(name, path)` works as a cache key.

## Test requirements

All tests live in `tests/test_dialect.py`. Group by concern. You may use pytest fixtures.

### Load and shape

1. `test_load_ar_v1_succeeds`: `load_dialect("ar-v1")` returns a `Dialect` without raising.
2. `test_dialect_is_frozen`: attempting to assign to `d.name` raises (`FrozenInstanceError`).
3. `test_mappings_are_read_only`: attempting `d.names["new"] = "x"` raises `TypeError` (MappingProxyType).
4. `test_name_attribute`: `d.name == "ar-v1"`.

### Entry counts

5. `test_total_entry_count`: `len(d.names) + len(d.attributes) >= 150`. (Avoid hard-coding 174 in case the dictionary grows.)
6. `test_attributes_nonempty`: `len(d.attributes) >= 25` (methods section has 29).
7. `test_names_nonempty`: `len(d.names) >= 120`.

### Forward lookup (names map)

8. `test_keyword_if`: the normalized form of `"إذا"` is in `d.names` and maps to `"if"`.
9. `test_keyword_def`: lookup of `"دالة"` (normalized) returns `"def"`.
10. `test_keyword_class`: lookup of `"صنف"` returns `"class"`.
11. `test_literal_true`: lookup of `"صحيح"` returns `"True"`.
12. `test_type_str`: lookup of `"نص"` returns `"str"`.
13. `test_function_print`: lookup of `"اطبع"` returns `"print"`.
14. `test_exception_value_error`: lookup of `"خطا_قيمة"` returns `"ValueError"`.
15. `test_filter_resolved`: lookup of `"فلتر"` (normalized) returns `"filter"` — confirms the collision-audit resolution landed.

### Forward lookup (attributes map)

16. `test_method_append`: `d.attributes[normalize_identifier("اضف")]` returns `"append"` (note: no leading dot in stored value).
17. `test_method_keys`: lookup of `"مفاتيح"` returns `"keys"`.
18. `test_method_encode_resolved`: lookup of `normalize_identifier("رمز_بايتات")` returns `"encode"` — confirms collision resolution.
19. `test_method_values_resolved`: lookup of `normalize_identifier("قيم_القاموس")` returns `"values"`.

### Normalization is applied

20. `test_lookup_with_harakat`: `d.names[normalize_identifier("إِذَا")]` returns `"if"` — harakat-laden user input normalizes to the same key.
21. `test_lookup_with_tatweel`: `d.names[normalize_identifier("إـذا")]` returns `"if"`.
22. `test_lookup_via_folded_hamza`: `d.names[normalize_identifier("اذا")]` returns `"if"` — folded form equals canonical form under normalization.

### Reverse lookup

23. `test_reverse_name_keyword`: `d.reverse_names["if"]` equals the **canonical** dictionary form `"إذا"` (with hamza), not the normalized form.
24. `test_reverse_attribute_method`: `d.reverse_attributes["append"]` equals `"اضف"`.
25. `test_reverse_preserves_hamza`: `d.reverse_names["print"]` contains no dot and no normalization artifacts — it is whatever the dictionary cell literally contained.

### Categories

26. `test_category_keyword`: `d.categories[normalize_identifier("إذا")] == "keyword"`.
27. `test_category_type`: `d.categories[normalize_identifier("نص")] == "type"`.
28. `test_category_function`: `d.categories[normalize_identifier("اطبع")] == "function"`.
29. `test_category_exception`: `d.categories[normalize_identifier("خطا_قيمة")] == "exception"`.
30. `test_category_method`: `d.categories[normalize_identifier("اضف")] == "method"`.
31. `test_category_literal`: `d.categories[normalize_identifier("صحيح")] == "literal"`.

### Cross-map coexistence (collision context)

32. `test_cross_map_allowed`: construct a scenario that asserts the SAME normalized Arabic token may appear in both `d.names` and `d.attributes` without error. If no such case naturally exists in ar-v1 today, this test uses a malformed fixture with an intentional cross-map entry to verify the loader does NOT raise. (If uncomfortable making this a property of ar-v1, use a fixture — see §9.)

### Cache

33. `test_load_is_cached`: `load_dialect("ar-v1") is load_dialect("ar-v1")`.
34. `test_load_with_path_cached`: `load_dialect("fixture", path=P) is load_dialect("fixture", path=P)`.

### Malformed dictionary errors (use `tests/fixtures/dialect_malformed.md`)

For these tests, write a small fixture dictionary with exactly ONE defect per test case, loaded via `load_dialect("malformed", path=...)`. Use either one fixture file per case or switch the content via `tmp_path` fixtures — implementer's choice.

35. `test_missing_backticks_raises`: Python cell lacks backticks → `DialectError`, message mentions line number.
36. `test_empty_canonical_raises`: Arabic cell is empty → `DialectError`.
37. `test_duplicate_normalized_key_raises`: two rows map different Python symbols from the same normalized Arabic key → `DialectError` naming both Python symbols.
38. `test_row_before_section_raises`: a data-shaped row appears before any recognized H2 heading → `DialectError`.
39. `test_insufficient_entries_raises`: a valid-format fixture with only 10 rows → `DialectError` mentioning the 150 floor.
40. `test_missing_file_raises`: non-existent path → `FileNotFoundError` (not `DialectError`).

### Cross-check: every dictionary Python target is a valid Python identifier

41. `test_all_python_targets_are_identifiers`: for every value in `d.names.values()` and `d.attributes.values()`, assert `value.isidentifier()` and `not keyword.iskeyword(value)` OR (`keyword.iskeyword(value)` AND the category is `"keyword"`). This catches accidental leading dots, dashes, or typos in Python targets.

## Reference materials

- `decisions/0003-keyword-dictionary.md` — governance rules.
- `decisions/0004-normalization-policy.md` — what normalization does.
- `dictionaries/ar-v1.md` — the file being parsed.
- Python `keyword` module: https://docs.python.org/3/library/keyword.html
- `types.MappingProxyType`: https://docs.python.org/3/library/types.html#types.MappingProxyType

## Open questions for the planner

None. If an edge case arises, stop and write a question in the delivery note; do not guess.

## Acceptance checklist

- [ ] `arabicpython/dialect.py` created with the exact public interface above.
- [ ] `tests/test_dialect.py` created with all 41 tests.
- [ ] `tests/fixtures/dialect_malformed.md` (or per-test fixtures) created as needed.
- [ ] `pytest` passes on Python 3.11, 3.12, 3.13.
- [ ] `ruff check .` clean; `black --check .` clean.
- [ ] No new dependencies in `pyproject.toml`.
- [ ] CI green across all 9 matrix cells.
- [ ] `specs/0003-dialect-loader-v1.delivery.md` written covering shipped behavior, deviations (if any), and any open questions.

## Workflow for Codex

1. Create branch `packet/0003-dialect-loader-v1` from `main`.
2. Implement `arabicpython/dialect.py` and its tests and fixtures.
3. Run `pytest` locally until green.
4. Run `ruff check .` and `black --check .` until clean.
5. Commit. Suggested message: `Packet 0003: implement dialect loader per ADR 0003/0004`.
6. Push `packet/0003-dialect-loader-v1`.
7. Write `specs/0003-dialect-loader-v1.delivery.md` (this delivery note IS in scope — unlike Packet 0002, no path restriction).
8. Open a PR titled `Packet 0003: dialect-loader-v1` linking to this spec.
9. Wait for CI and planner review.

## Allowed edit scope

- `arabicpython/dialect.py` (new)
- `tests/test_dialect.py` (new)
- `tests/fixtures/dialect_malformed.md` and/or other fixture files under `tests/fixtures/` (new)
- `specs/0003-dialect-loader-v1.delivery.md` (new)

Do NOT modify: the normalize module, the dictionary, any ADR, pyproject.toml, CI workflow, or existing tests.
