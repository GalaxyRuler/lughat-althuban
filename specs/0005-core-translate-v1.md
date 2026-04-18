# Spec Packet 0005: core-translate-v1

**Phase**: A
**Depends on**: Packet 0001 (dictionary), Packet 0002 (normalize), Packet 0003 (dialect-loader), Packet 0004 (pretokenize); ADRs 0001 (architecture), 0004 (normalization).
**Estimated size**: medium-large (one focused implementer session)
**Owner**: Gemini 3.1 Pro

## Goal

Implement `translate`, the function that turns an `.apy` source string into a Python source string. This is the second and final transformation in the Phase A transpilation pipeline:

```
.apy text  →  pretokenize  →  tokenize  →  NAME-token rewrite  →  untokenize  →  Python text
```

`pretokenize` (Packet 0004) made the input lex-able by Python. `translate` adds the Arabic-keyword-to-Python-keyword rewrite on top, using the `Dialect` from Packet 0003. The output is a valid Python source string ready for `compile(src, path, "exec")`.

After this packet lands, the CLI runner (Packet 0006) and the import hook (later packet) are thin wrappers that call `translate` then `compile` then `exec`.

## Non-goals

- Does NOT call `compile` or `exec`. That's the runner's job.
- Does NOT rewrite identifiers inside f-string expression bodies on Python 3.11 (single `STRING` token; opaque). On 3.12+ where the tokenizer exposes `FSTRING_START`/`FSTRING_MIDDLE`/`FSTRING_END` and inner NAME tokens, identifiers inside `{...}` ARE translated. This version skew is documented; full f-string interior translation across all versions is a future packet.
- Does NOT alias library symbols (`os.path.join` stays English). Layer-3 work is Phase B per ADR 0007.
- Does NOT translate docstrings or comment text. Strings and comments pass through verbatim.
- Does NOT perform AST rewriting. NAME-token level only.
- Does NOT load the dialect from disk by default — call sites pass a `Dialect`, or omit and let `translate` call `load_dialect("ar-v1")`.
- Does NOT validate that the resulting Python compiles. Caller's job.
- Does NOT preserve perfect whitespace in all edge cases. `tokenize.untokenize` round-trips well enough for Phase A; line-number drift up to ±1 is acceptable per ADR 0001.

## Files

### Files to create

- `arabicpython/translate.py`
- `tests/test_translate.py`

### Files to read (do not modify)

- `arabicpython/pretokenize.py` — call this first to fold digits/punct.
- `arabicpython/dialect.py` — `Dialect` dataclass and `load_dialect`.
- `arabicpython/normalize.py` — `normalize_identifier` for keying lookups.
- `dictionaries/ar-v1.md` — for understanding test fixtures.
- `decisions/0001-architecture.md` — pipeline and constraints.
- `decisions/0004-normalization-policy.md` — why we normalize.

## Public interface

```python
def translate(source: str, *, dialect: "Dialect | None" = None) -> str:
    """Translate apython source to Python source.

    Pipeline:
      1. pretokenize(source) — fold Arabic digits/punctuation, reject bidi
         outside strings (raises SyntaxError on bidi or mixed-digit literals).
      2. tokenize.tokenize on the result, treated as UTF-8 bytes.
      3. Walk the token stream. For each NAME token:
         - If the previous non-whitespace, non-comment token is OP('.'),
           look up normalize_identifier(name) in dialect.attributes.
         - Otherwise, look up normalize_identifier(name) in dialect.names.
         - On hit, replace the token's string with the dictionary's Python
           symbol (e.g., 'إذا' → 'if', 'قراءة' → 'read').
         - On miss, replace with normalize_identifier(name) — collapses
           harakat/hamza variants per ADR 0004 so equivalent spellings refer
           to the same Python identifier.
         - ASCII-only NAME tokens that are unchanged by normalize_identifier
           pass through untouched.
      4. untokenize and return the result as a str.

    Args:
        source: the .apy source text.
        dialect: optional Dialect to use; defaults to load_dialect("ar-v1").

    Returns:
        Python source text suitable for compile(src, path, "exec").

    Raises:
        SyntaxError: propagated from pretokenize (bidi, mixed digits) or
            from tokenize (e.g., unclosed string literal).
        DialectError: propagated from load_dialect on first call when no
            explicit dialect is provided.
    """
```

## Algorithm details

### Step 1 — pretokenize

Call `arabicpython.pretokenize.pretokenize(source)`. Propagate any `SyntaxError`. Take the returned string forward as `intermediate`.

### Step 2 — tokenize

Use `tokenize.tokenize(io.BytesIO(intermediate.encode("utf-8")).readline)`. Catch `tokenize.TokenizeError` and re-raise as `SyntaxError` with a message that includes the original error text. (The downstream CPython error path expects `SyntaxError`, not `TokenizeError`.)

### Step 3 — NAME rewrite

Implement as a loop that builds a list of new tokens, tracking the last *significant* token for the attribute-context check:

- Significant = anything that is not `NL`, `NEWLINE`, `INDENT`, `DEDENT`, `COMMENT`, `ENCODING`, or `ENDMARKER`.
- A NAME is "in attribute position" iff the last significant token was `OP` with `string == "."`.

For each `NAME` token `tok`:
- `key = normalize_identifier(tok.string)`
- If attribute position and `key in dialect.attributes`: `new_string = dialect.attributes[key]`
- Elif (not attribute position) and `key in dialect.names`: `new_string = dialect.names[key]`
- Else: `new_string = key`  (so equivalent spellings collapse to the same Python identifier)
- If `new_string == tok.string`: append the original token unchanged.
- Else: append a new `TokenInfo(NAME, new_string, tok.start, tok.end, tok.line)`.

For all other tokens: append unchanged.

### Step 4 — untokenize

Use `tokenize.untokenize(tokens)`. The result is `bytes` in some Python versions and `str` in others — the spec returns `str`. Decode if necessary using UTF-8.

Strip a leading UTF-8 BOM if present (untokenize sometimes emits one because we passed the encoding token through).

### F-string handling (version-dependent)

- On Python 3.12+: the tokenizer emits `FSTRING_START`, `FSTRING_MIDDLE`, `FSTRING_END`, and regular `NAME`/`OP` tokens inside `{...}` expressions. The NAME-rewrite logic catches identifiers inside f-string expressions naturally — no special code needed. Verify with the version-specific test below.
- On Python 3.11: f-strings are a single `STRING` token. NAMEs inside them are invisible to us. Documented as a known v1 limitation.

No version-gating in the implementation — the same code path runs on all versions; behavior just differs because the underlying tokenizer differs.

### Encoding and BOM

`tokenize.tokenize` requires a binary readline that yields a `coding:` line first or defaults to UTF-8. Encode the pretokenized string to UTF-8 bytes; do not prepend a coding cookie.

## Implementation constraints

- **Dependencies**: stdlib only (`io`, `tokenize`).
- **Python version**: 3.11+ (matches the rest of the package).
- **Purity**: no I/O, no global state, no caching beyond what `load_dialect` already memoizes.
- **Performance**: O(n) in tokens. A 1,000-line file should translate in well under 50 ms.
- **Style**: pass `ruff check .` and `black --check .` at project defaults (line length 100).
- **Imports**: `from arabicpython.pretokenize import pretokenize`, `from arabicpython.normalize import normalize_identifier`, `from arabicpython.dialect import Dialect, load_dialect`. No relative-import gymnastics.

## Test requirements

All tests in `tests/test_translate.py`. Use exact test names below. Pytest only.

Use the default `ar-v1` dialect throughout unless a test name says `_custom_dialect_`. Tests should call `translate(src)` (letting the default load) except where noted.

### Identity on pure ASCII Python (5)

1. `test_empty_string`: `translate("")` returns `""` (or `"\n"` — assert via `compile`-able; document whichever the implementation produces).
2. `test_pure_ascii_passthrough`: `translate("x = 1\nprint(x)\n")` is byte-equal to the input (no Arabic, nothing to change).
3. `test_ascii_function_def`: `translate("def foo(x):\n    return x + 1\n")` is byte-equal to input.
4. `test_ascii_class_def`: `translate("class C:\n    def m(self):\n        pass\n")` is byte-equal.
5. `test_ascii_with_comment`: `translate("# hello\nx = 1\n")` is byte-equal.

### Single keyword translation (10)

For each, assert the translated source compiles and contains the expected ASCII keyword. Use the dictionary mapping verbatim; if a name in the test below isn't in `ar-v1.md`, fix the test, not the dictionary.

6. `test_translate_if`: `إذا x: pass` → contains `if`.
7. `test_translate_else`: `إذا x: pass\nوإلا: pass` (or whatever maps to `else`) → contains `else`.
8. `test_translate_while`: source with the Arabic for `while` translates → contains `while`.
9. `test_translate_for`: source with the Arabic for `for` translates → contains `for`.
10. `test_translate_def`: source with the Arabic for `def` → contains `def`.
11. `test_translate_class`: → contains `class`.
12. `test_translate_return`: → contains `return`.
13. `test_translate_pass`: → contains `pass`.
14. `test_translate_True_literal`: source with the Arabic for `True` → contains `True`.
15. `test_translate_None_literal`: source with the Arabic for `None` → contains `None`.

(For 6–15, look up the actual Arabic spelling in `dictionaries/ar-v1.md` — do not invent.)

### Built-in function translation (5)

16. `test_translate_print`: source containing the Arabic for `print` translates so that the output contains `print` and is compile-able.
17. `test_translate_len`: same pattern for `len`.
18. `test_translate_range`: same for `range`.
19. `test_translate_input`: same for `input`.
20. `test_translate_isinstance`: same for `isinstance`.

### Built-in type translation (3)

21. `test_translate_list`: Arabic for `list` → `list` in output.
22. `test_translate_dict`: Arabic for `dict` → `dict` in output.
23. `test_translate_str`: Arabic for `str` → `str` in output.

### Exception translation (3)

24. `test_translate_exception_keyword`: source using the Arabic for `except` (the keyword) translates to `except` and compiles.
25. `test_translate_exception_class`: source using the Arabic for `Exception` (the class — `استثناء_عام` per the dictionary) translates to `Exception`.
26. `test_translate_value_error`: source using the Arabic for `ValueError` translates to `ValueError`.

### Method/attribute translation (5)

27. `test_translate_str_method`: `s.قراءة()` (or whichever Arabic maps to a `str` method like `.upper`) translates to `s.upper()`. Use a method actually present in `dialect.attributes`.
28. `test_translate_list_method`: `lst.<arabic for append>(x)` translates correctly.
29. `test_translate_dict_method`: `d.<arabic for get>(k)` translates correctly.
30. `test_translate_chained_attributes`: `a.b.<arabic method>()` — only the method gets translated; intermediate attribute names that aren't in `dialect.attributes` pass through normalized.
31. `test_attribute_does_not_match_name`: an Arabic name that exists in `dialect.names` but NOT in `dialect.attributes` is NOT translated when it appears after a `.`. E.g., the Arabic for `print` should not become `.print` if used as `obj.<that_word>`.

### Normalization in translation (3)

32. `test_translate_with_harakat`: source uses `إذا` with a fatha embedded (`إِذا`); still translates to `if`.
33. `test_translate_hamza_variant`: source uses `اذا` (alef without hamza); still translates to `if` (since normalize folds hamza variants).
34. `test_unknown_identifier_normalized`: a user variable `كَلب` (with fatha) becomes `كلب` in the output even though it's not in the dictionary. Two assignments using equivalent spellings produce the same Python identifier.

### Pretokenize integration (3)

35. `test_translate_with_arabic_digits`: `x = ٥` → `x = 5` (pretokenize folds, translate passes through unchanged).
36. `test_translate_with_arabic_punct`: `foo(a، b)` → `foo(a, b)`.
37. `test_translate_combined_keyword_and_digit`: `إذا x > ٥: pass` → `if x > 5: pass` (or however the formatting comes out — assert it compiles and contains both `if` and `5`).

### Unknown identifiers preserved (3)

38. `test_unknown_arabic_name_preserved`: `كلب = 1` → `كلب = 1` (no translation; not in dictionary; normalize is identity for this exact spelling). Compiles as valid Python (PEP 3131).
39. `test_user_function_def`: `def دالتي(): pass` → `def دالتي(): pass`. Compiles.
40. `test_unknown_attribute_preserved`: `obj.صفتي` → `obj.صفتي` (not in `dialect.attributes`, passes through).

### String preservation (3)

41. `test_arabic_keyword_inside_string_not_translated`: `x = "إذا"` → `x = "إذا"`. The string body is opaque.
42. `test_arabic_method_inside_string_not_translated`: `x = "obj.قراءة()"` passes through unchanged.
43. `test_triple_string_preserved`: `'''multi\nline\nإذا'''` passes through unchanged.

### Comment preservation (2)

44. `test_arabic_keyword_in_comment_not_translated`: `# إذا x: pass\nx = 1` → comment text untouched, `x = 1` compiles.
45. `test_inline_comment_with_arabic_keyword`: `x = 1  # إذا` → comment untouched.

### Combined real-world programs (5)

For each, assert that `compile(translate(src), "<test>", "exec")` succeeds and that the translated output contains expected Python keywords in the right places. (Do NOT assert exact whitespace — tokenize/untokenize may shift it.)

46. `test_program_factorial`: a recursive factorial in Arabic; translates and compiles; running it (via `exec` in a fresh namespace and calling the translated function name) returns the right number for n=5.
47. `test_program_fizzbuzz`: small fizzbuzz; translates, compiles, executes; check stdout via `capsys`.
48. `test_program_class_with_method`: small class with one method; translates, compiles, instantiates, calls method, asserts return value.
49. `test_program_try_except`: try/except block in Arabic catches `ValueError`; translates, compiles, executes, asserts the except branch ran.
50. `test_program_for_loop_with_range`: for loop summing `range(n)` in Arabic; translates, compiles, executes, asserts result.

### F-string handling (2)

51. `test_fstring_text_preserved`: `f"hello {x}"` (ASCII only) translates byte-equal.
52. `test_fstring_arabic_expr_312_plus_translates`: `f"{اطبع}"` — on Python 3.12+, NAME tokens inside f-string `{...}` are exposed by the tokenizer, so this should translate to `f"{print}"`. Use `pytest.mark.skipif(sys.version_info < (3, 12), reason="...")`. On 3.11 the equivalent test would XFAIL because the f-string is opaque; do NOT add a 3.11 test for this — just document the limitation in the delivery note.

### Whitespace and structure preservation (3)

53. `test_indentation_preserved`: a 4-space-indented function body retains its indentation in the output (within `tokenize.untokenize`'s reasonable round-trip).
54. `test_blank_lines_preserved`: source with a blank line between two statements still has a separation in output (does not merge to one line).
55. `test_line_count_within_one`: for a 20-line source, the translated output has line count within ±1 of the input. (Per ADR 0001's tolerance.)

### Error propagation (2)

56. `test_bidi_error_propagates`: source with a bidi control outside strings raises `SyntaxError` when passed to `translate` (forwarded from pretokenize, error message intact).
57. `test_unclosed_string_raises_syntax_error`: source with `x = "unclosed` raises `SyntaxError` (re-raised from `tokenize.TokenizeError`).

### Custom dialect parameter (2)

58. `test_custom_dialect_used`: pass an explicit `Dialect` (e.g., one loaded from a small fixture file) and verify its mappings are honored, not `ar-v1`.
59. `test_default_dialect_is_ar_v1`: when no `dialect` is passed, the default `ar-v1` is used (assert by translating something only `ar-v1` would handle).

## Reference materials

- `decisions/0001-architecture.md` — pipeline and rationale.
- `decisions/0004-normalization-policy.md` — what `normalize_identifier` collapses and why.
- Python `tokenize` module: https://docs.python.org/3/library/tokenize.html
- Python `tokenize.untokenize` round-trip caveats: https://docs.python.org/3/library/tokenize.html#tokenize.untokenize
- PEP 3131 (Unicode identifiers): https://peps.python.org/pep-3131/
- PEP 701 (formalized f-string tokenization in 3.12): https://peps.python.org/pep-0701/

## Open questions for the planner

None expected. If you hit a real ambiguity — for example, an Arabic spelling in a test that doesn't appear in `ar-v1.md` — stop and write the question in the delivery note rather than guessing or modifying the dictionary.

## Acceptance checklist

- [ ] `arabicpython/translate.py` created with the exact public interface above.
- [ ] `tests/test_translate.py` created with all 59 tests.
- [ ] `pytest tests/test_translate.py` passes on Python 3.11, 3.12, 3.13. (Test 52 skips on 3.11.)
- [ ] Existing test suites (`test_normalize.py`, `test_dialect.py`, `test_pretokenize.py`) still pass.
- [ ] `ruff check .` clean; `black --check .` clean.
- [ ] No new dependencies in `pyproject.toml`.
- [ ] CI green across all 9 matrix cells.
- [ ] `specs/0005-core-translate-v1.delivery.md` written covering shipped behavior, deviations (if any), implementation notes, open questions.

## Workflow for the implementer

1. Create branch `packet/0005-core-translate-v1` from `main`.
2. Implement `arabicpython/translate.py` and `tests/test_translate.py`.
3. Run `pytest` (full suite, not just the new file) until green.
4. Run `ruff check .` and `black --check .` until clean. **Do not push without running both — Packet 0004 burned an entire CI cycle on a missed ruff violation.**
5. Commit. Suggested message: `Packet 0005: implement translate per ADR 0001`.
6. Push.
7. Write `specs/0005-core-translate-v1.delivery.md`.
8. Open a PR titled `Packet 0005: core-translate-v1` linking back to this spec.
9. Wait for CI green, then planner review.

## Allowed edit scope

- `arabicpython/translate.py` (new)
- `tests/test_translate.py` (new)
- `specs/0005-core-translate-v1.delivery.md` (new)

Do NOT modify: any other module, any ADR, the dictionary, `pyproject.toml`, the CI workflow, or existing tests. If you believe the spec has a bug, flag it in the delivery note rather than silently deviating.
