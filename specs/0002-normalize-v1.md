# Spec Packet 0002: normalize-v1

**Phase**: A
**Depends on**: ADR 0004 (identifier normalization policy)
**Estimated size**: small (one Codex session)
**Owner**: Codex

## Goal

Implement `normalize_identifier`, the pure function that maps an arbitrary Arabic (or mixed-script) string to its canonical form for dictionary lookup and identifier equality. This function is called in three places across the codebase (dialect loading, every `NAME` token during transpilation, reverse traceback translation), so it must be correct, fast, and dependency-free.

Every other piece of Phase A depends on this being right. If the normalizer has a bug, every lookup silently degrades.

## Non-goals

- Does NOT integrate with Python's tokenizer. That is Packet 0004.
- Does NOT parse the `# apython: strict` file-level pragma. It accepts a `strict` boolean parameter; pragma parsing is handled by the CLI/transpiler layer in a later packet.
- Does NOT load or touch `dictionaries/ar-v1.md`. That is Packet 0003. (One test in this packet reads the markdown file to cross-check idempotency, but the normalizer itself has no knowledge of the dialect.)
- Does NOT handle security concerns like mixed-script confusables or bidi controls. Those are handled elsewhere (pretokenize pass, Packet 0004+).
- Does NOT modify characters outside the Arabic script. ASCII, CJK, Latin-Extended, etc. pass through unchanged (after NFKC).

## Files

### Files to create

- `arabicpython/normalize.py`
- `tests/test_normalize.py`

### Files to read (do not modify)

- `decisions/0004-normalization-policy.md` — the binding spec for behavior.
- `dictionaries/ar-v1.md` — used by one cross-check test.

## Public interface

```python
def normalize_identifier(s: str, *, strict: bool = False) -> str:
    """Normalize an Arabic (or mixed-script) identifier to canonical form.

    The non-strict default applies the full Arabic-aware normalization from
    ADR 0004:
      1. Unicode NFKC (matches Python tokenizer behavior for identifiers).
      2. Strip tatweel U+0640 wherever it appears.
      3. Strip harakat in ranges U+064B-U+065F and U+0670 (superscript alef).
      4. Fold hamza variants: U+0623 (أ), U+0625 (إ), U+0622 (آ) → U+0627 (ا).
         Applied at all positions in the string.
      5. Fold alef maksura U+0649 (ى) → U+064A (ي) ONLY if it is the last
         character of the input string.
      6. Fold ta marbuta U+0629 (ة) → U+0647 (ه) ONLY if it is the last
         character of the input string.

    Strict mode applies only step 1.

    The function is pure: no I/O, no global state, no randomness.
    Idempotent: normalize_identifier(normalize_identifier(x)) == normalize_identifier(x)
    for all x and for both strict values.

    Args:
        s: the input string. May be empty, ASCII-only, Arabic-only, or mixed.
        strict: if True, apply only NFKC.

    Returns:
        The normalized string.

    Examples:
        >>> normalize_identifier("")
        ''
        >>> normalize_identifier("hello_world")
        'hello_world'
        >>> normalize_identifier("مَرحَبا")
        'مرحبا'
        >>> normalize_identifier("مـرحـبا")   # tatweel stripped
        'مرحبا'
        >>> normalize_identifier("أحمد")      # hamza folded
        'احمد'
        >>> normalize_identifier("مشى")       # alef maksura → ya at word-end
        'مشي'
        >>> normalize_identifier("شجرة")      # ta marbuta → ha at word-end
        'شجره'
        >>> normalize_identifier("مَرحَبا", strict=True)
        'مَرحَبا'
    """
```

## Implementation constraints

- **Dependencies**: stdlib only. Use `unicodedata.normalize` for NFKC. Do not add third-party deps.
- **Python version**: 3.11+ (matches project pyproject.toml).
- **Purity**: no module-level mutable state, no globals that change after import, no I/O.
- **Performance**: should run in well under 1 ms for typical identifier lengths (< 50 chars). No required benchmark, but avoid obviously wasteful patterns like repeated full-string scans when one pass suffices.
- **Style**: pass `ruff check .` and `black --check .` at project defaults (line length 100).

## Implementation hints

- Define the harakat character set once as a module-level `frozenset`. Do not use regex for simple character membership tests — `str.translate()` or a generator expression is cleaner and faster.
- The fold-hamza step can be a single `str.translate()` with a precomputed translation table.
- The "word-final" condition for alef maksura and ta marbuta is just "is this the last character of the string after prior steps." Check `s[-1]` after stripping.
- Codepoint cheat sheet (verify against `unicodedata.name` when writing tests):

  | Codepoint | Name | Symbol |
  |---|---|---|
  | U+0622 | ARABIC LETTER ALEF WITH MADDA ABOVE | آ |
  | U+0623 | ARABIC LETTER ALEF WITH HAMZA ABOVE | أ |
  | U+0625 | ARABIC LETTER ALEF WITH HAMZA BELOW | إ |
  | U+0627 | ARABIC LETTER ALEF | ا |
  | U+0629 | ARABIC LETTER TEH MARBUTA | ة |
  | U+0640 | ARABIC TATWEEL | ـ |
  | U+0647 | ARABIC LETTER HEH | ه |
  | U+0649 | ARABIC LETTER ALEF MAKSURA | ى |
  | U+064A | ARABIC LETTER YEH | ي |
  | U+064B–U+065F | various fathatan/dammatan/kasratan/sukun/hamza-above/etc. | (harakat block) |
  | U+0670 | ARABIC LETTER SUPERSCRIPT ALEF | ٰ |

## Test requirements

All tests live in `tests/test_normalize.py`. Each test has a clear name, concrete inputs, and a specific expected output.

### Basic cases

1. `test_empty_string`: `normalize_identifier("")` → `""`.
2. `test_ascii_passthrough`: `normalize_identifier("hello_world")` → `"hello_world"`.
3. `test_ascii_numbers_passthrough`: `normalize_identifier("var123")` → `"var123"`.
4. `test_plain_arabic_passthrough`: `normalize_identifier("كتاب")` → `"كتاب"` (no changes needed).

### NFKC

5. `test_nfkc_presentation_form`: given an Arabic presentation form character (e.g., `"ﻣ"` U+FEE3, initial form of meem), normalize_identifier produces the base form `"م"` U+0645.
6. `test_nfkc_applied_in_strict`: same input as #5 passes NFKC in strict mode.

### Tatweel

7. `test_tatweel_stripped`: `normalize_identifier("مـرحـبا")` → `"مرحبا"`.
8. `test_tatweel_at_edges`: `normalize_identifier("ـمرحباـ")` → `"مرحبا"`.
9. `test_only_tatweel`: `normalize_identifier("ـــ")` → `""`.

### Harakat

10. `test_fatha_stripped`: `normalize_identifier("مَرحبا")` → `"مرحبا"` (U+064E).
11. `test_kasra_stripped`: identifier with U+0650 → stripped.
12. `test_damma_stripped`: identifier with U+064F → stripped.
13. `test_sukun_stripped`: identifier with U+0652 → stripped.
14. `test_shadda_stripped`: identifier with U+0651 → stripped.
15. `test_tanwin_stripped`: fathatan U+064B, dammatan U+064C, kasratan U+064D all stripped.
16. `test_superscript_alef_stripped`: U+0670 stripped.
17. `test_all_harakat_combined`: a string with every harakat codepoint → all stripped.

### Hamza folding

18. `test_hamza_above_folded`: `normalize_identifier("أ")` → `"ا"`.
19. `test_hamza_below_folded`: `normalize_identifier("إ")` → `"ا"`.
20. `test_madda_folded`: `normalize_identifier("آ")` → `"ا"`.
21. `test_hamza_at_start`: `normalize_identifier("أحمد")` → `"احمد"`.
22. `test_hamza_at_middle`: `normalize_identifier("سأل")` → `"سال"`.
23. `test_hamza_at_end`: `normalize_identifier("بدأ")` → `"بدا"`.
24. `test_multiple_hamzas`: `normalize_identifier("أكدأ")` → `"اكدا"`.

### Alef maksura

25. `test_alef_maksura_final_folded`: `normalize_identifier("مشى")` → `"مشي"`.
26. `test_alef_maksura_not_final_preserved`: `normalize_identifier("ىa")` → `"ىa"` (not at end).
27. `test_alef_maksura_only`: `normalize_identifier("ى")` → `"ي"`.

### Ta marbuta

28. `test_ta_marbuta_final_folded`: `normalize_identifier("شجرة")` → `"شجره"`.
29. `test_ta_marbuta_not_final_preserved`: `normalize_identifier("ةa")` → `"ةa"` (not at end).
30. `test_ta_marbuta_only`: `normalize_identifier("ة")` → `"ه"`.

### Strict mode

31. `test_strict_mode_preserves_harakat`: `normalize_identifier("مَرحَبا", strict=True)` → `"مَرحَبا"`.
32. `test_strict_mode_preserves_tatweel`: `normalize_identifier("مـرحبا", strict=True)` → `"مـرحبا"`.
33. `test_strict_mode_preserves_hamza_variants`: `normalize_identifier("أحمد", strict=True)` → `"أحمد"`.
34. `test_strict_mode_still_applies_nfkc`: same as test #5 but with `strict=True`, still produces base form.

### Idempotency

35. `test_idempotent_non_strict`: for each of the following inputs, assert `normalize_identifier(normalize_identifier(x)) == normalize_identifier(x)`:
    - `""`
    - `"hello_world"`
    - `"مَرحَبا"`
    - `"مـرحـبا"`
    - `"أحمد"`
    - `"شجرة"`
    - `"مشى"`
    - `"خطا_قيمة"` (from the dictionary)
36. `test_idempotent_strict`: same set of inputs under `strict=True`, same idempotency invariant.

### Combined transformations

37. `test_tatweel_and_harakat_together`: `normalize_identifier("مَـرحَـبا")` → `"مرحبا"`.
38. `test_hamza_and_harakat_together`: `normalize_identifier("أَحمد")` → `"احمد"`.
39. `test_all_at_once`: a synthetic string containing NFKC-normalizable form, tatweel, harakat, hamza variant, and final ta marbuta → fully normalized result.

### Cross-check with the v1 dictionary

40. `test_dictionary_entries_idempotent`:
    - Parse `dictionaries/ar-v1.md`, extracting every Arabic canonical entry from every table (keywords, types, functions, exceptions, methods).
    - For each entry `e`, assert `normalize_identifier(e) == normalize_identifier(normalize_identifier(e))`.
    - No entries should cause any exception.
    - This test uses a simple markdown parser (split on `|`, find rows that look like data rows, extract the second column). A 20-line helper in the test file is fine; do not add a dependency.
    - Minimum count assertion: the parser must find at least 150 entries to catch parse failures.

### Characters that do NOT belong to the Arabic range

41. `test_latin_preserved`: `normalize_identifier("variableName")` → `"variableName"`.
42. `test_mixed_script_identifier`: `normalize_identifier("myمتغير")` → `"myمتغير"` (no changes; hamza/harakat absent, not word-final for ta marbuta/alef maksura).
43. `test_digits_passthrough`: `normalize_identifier("var_123")` → `"var_123"`.

## Reference materials

- `decisions/0004-normalization-policy.md` (project root) — authoritative spec.
- Python `unicodedata` module: https://docs.python.org/3/library/unicodedata.html
- Unicode Arabic block chart: https://www.unicode.org/charts/PDF/U0600.pdf
- PEP 3131 normalization: https://peps.python.org/pep-3131/

## Open questions for the planner

None — spec is complete. If an edge case arises that is not covered above, stop and write a question in the delivery note; do not guess.

## Acceptance checklist

- [ ] `arabicpython/normalize.py` created with the specified public interface.
- [ ] `tests/test_normalize.py` created with all 43 tests listed above.
- [ ] `pytest tests/test_normalize.py` passes on Python 3.11, 3.12, 3.13.
- [ ] `ruff check .` passes with no warnings.
- [ ] `black --check .` passes with no required changes.
- [ ] No new dependencies added to `pyproject.toml`.
- [ ] CI run on the PR is green across Linux/Windows/macOS × Python 3.11/3.12/3.13.
- [ ] Delivery note `specs/0002-normalize-v1.delivery.md` written covering: what shipped, any deviations from the spec, any edge cases encountered, open questions for the planner.

## Workflow for Codex

1. Create branch `packet/0002-normalize-v1` from `main`.
2. Implement the two files.
3. Run `pytest tests/test_normalize.py` locally until green.
4. Run `ruff check .` and `black --check .` until clean.
5. Commit. Suggested message: `Packet 0002: implement normalize_identifier per ADR 0004`.
6. Push to `origin packet/0002-normalize-v1`.
7. Write delivery note.
8. Open a PR titled `Packet 0002: normalize-v1` with body linking to this spec.
9. Wait for CI to finish and planner review.
