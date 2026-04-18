# Spec Packet 0004: pretokenize-v1

**Phase**: A
**Depends on**: ADR 0005 (numerals/punctuation), ADR 0006 (bidi policy)
**Estimated size**: medium (one focused implementer session)
**Owner**: Gemini 3.1 Pro

## Goal

Implement `pretokenize`, a pure string-to-string function that performs character-level substitutions on `.apy` source so Python's tokenizer accepts it. This is the first transformation in the transpilation pipeline; without it, Arabic numerals and punctuation cause `tokenize.TokenizeError` before Packet 0005's identifier rewriter ever runs.

The function applies three orthogonal transformations during a single string-aware walk:

1. **Numeral folding** — Arabic-Indic and Eastern Arabic-Indic digits → ASCII (ADR 0005).
2. **Punctuation folding** — Arabic comma/semicolon/question-mark → ASCII (ADR 0005).
3. **Bidi rejection** — bidi control codepoints outside string literals raise `SyntaxError` (ADR 0006).

All three apply only outside string literals. String contents pass through unchanged.

## Non-goals

- Does NOT call Python's `tokenize` module. This is the *pre*-tokenize pass.
- Does NOT perform identifier substitution. Packet 0005 does that, after this runs.
- Does NOT handle f-string expression sections specially. The entire f-string is treated as a string literal — characters inside `{...}` pass through unchanged. **Known v1 limitation**: Arabic digits inside f-string expressions will fail in Packet 0005 because Python's tokenizer can't read them. Users must write ASCII digits inside f-string expressions in v1. Documented; resolved in a future packet.
- Does NOT validate that the resulting string is well-formed Python. That's downstream.
- Does NOT handle the `# apython: strict` pragma. CLI/transpiler concern.
- Does NOT detect mixed-script confusables (e.g., Latin `a` vs. Cyrillic `а`). Out of scope; ADR for v1.x.

## Files

### Files to create

- `arabicpython/pretokenize.py`
- `tests/test_pretokenize.py`

### Files to read (do not modify)

- `decisions/0005-numerals-punctuation.md` — authoritative spec for numerals/punctuation behavior.
- `decisions/0006-bidi-policy.md` — authoritative spec for bidi rejection behavior, including the exact error message format.
- `arabicpython/normalize.py` — example of pure-function module style used in this project.

## Public interface

```python
def pretokenize(source: str) -> str:
    """Pre-process Arabic Python source for Python's tokenizer.

    Performs three transformations during a single left-to-right walk:

    1. Outside string literals: replace U+0660-U+0669 (Arabic-Indic digits)
       and U+06F0-U+06F9 (Eastern Arabic-Indic digits) with the corresponding
       ASCII digits 0-9.
    2. Outside string literals: replace U+060C (،) with U+002C (,),
       U+061B (؛) with U+003B (;), U+061F (؟) with U+003F (?).
    3. Outside string literals: raise SyntaxError if any of U+202A-U+202E or
       U+2066-U+2069 (bidi control characters) is encountered. Inside string
       literals these pass through unchanged.

    Single-line and multi-line string literals (', ", ''', """) and string
    prefixes (r, b, u, f, and case-insensitive combinations) are recognized.
    String contents are preserved byte-for-byte.

    Comments (# ... newline) are NOT string literals: substitutions apply and
    bidi controls are rejected (per ADR 0006: comments are an attack vector,
    not a safe haven).

    A run of consecutive digit characters that mixes digit systems (e.g.,
    `١2` mixing Arabic-Indic and ASCII) raises SyntaxError. Pure-system runs
    are folded to ASCII; pure-ASCII runs pass through unchanged.

    Args:
        source: the .apy source text.

    Returns:
        Source text with the substitutions applied.

    Raises:
        SyntaxError: with the exact format from ADR 0006 for bidi controls,
            or a clear message naming the offending characters and line/column
            for mixed-digit literals.
    """
```

## Substitution table (verbatim from ADR 0005)

| Codepoint range | → ASCII | Scope |
|---|---|---|
| U+0660-U+0669 (٠–٩) | U+0030-U+0039 (0-9) | outside string literals |
| U+06F0-U+06F9 (۰–۹) | U+0030-U+0039 (0-9) | outside string literals |
| U+060C (،) | U+002C (,) | outside string literals |
| U+061B (؛) | U+003B (;) | outside string literals |
| U+061F (؟) | U+003F (?) | outside string literals |

## Bidi rejection set (verbatim from ADR 0006)

U+202A, U+202B, U+202C, U+202D, U+202E, U+2066, U+2067, U+2068, U+2069.

**Error format** (must match ADR 0006 exactly):
```
SyntaxError: bidi control character U+202E (RIGHT-TO-LEFT OVERRIDE) is not allowed outside string literals at line L, column C. See https://trojansource.codes for why.
```
The codepoint (`U+202E`), the Unicode name (use `unicodedata.name`), and the 1-indexed line / 0-indexed column are mandatory. The trailing URL is mandatory.

## State machine

Implement a single-pass walker. States:

- `DEFAULT` — outside strings/comments. Apply substitutions. Reject bidi.
- `COMMENT` — between `#` and the next newline. Apply digit and punctuation substitutions (per tests 33–35; comments are NOT strings). Reject bidi. Mixed-digit detection is not required inside comments.
- `STRING_SQ` — inside `'...'`. Pass through. Allow bidi.
- `STRING_DQ` — inside `"..."`. Pass through. Allow bidi.
- `STRING_TSQ` — inside `'''...'''`. Pass through. Allow bidi.
- `STRING_TDQ` — inside `"""..."""`. Pass through. Allow bidi.

### Transitions

- `DEFAULT` + `#` → `COMMENT`
- `COMMENT` + `\n` → `DEFAULT`
- `DEFAULT` + `'''` → `STRING_TSQ` (check triple before single)
- `DEFAULT` + `"""` → `STRING_TDQ`
- `DEFAULT` + `'` (not part of triple) → `STRING_SQ`
- `DEFAULT` + `"` (not part of triple) → `STRING_DQ`
- `STRING_SQ` + unescaped `'` → `DEFAULT`
- `STRING_DQ` + unescaped `"` → `DEFAULT`
- `STRING_TSQ` + `'''` → `DEFAULT`
- `STRING_TDQ` + `"""` → `DEFAULT`

### Escape handling

- Inside `STRING_SQ`/`STRING_DQ` (single-line), a backslash escapes the next character. `'\''` is a valid string containing one apostrophe.
- Inside `STRING_TSQ`/`STRING_TDQ`, escapes work but unescaped `'` or `"` doesn't end the triple-quoted string — only the matching triple closes it.
- Raw-string prefixes (`r`, `R`, `rb`, `br`, etc.) DO NOT change escape semantics for our purposes — backslash still escapes the next char in single-line strings for the purposes of finding the closing quote. (Python's runtime handling of raw strings is different, but that doesn't affect where the string ends.)

### String prefix recognition

A string prefix is one or more of `r`, `R`, `b`, `B`, `u`, `U`, `f`, `F` (any case-insensitive combination, max 2 letters in practice) **immediately** before a `'` or `"`. The prefix itself is just letters in `DEFAULT` — they're not Arabic, not digits, not punctuation, so they pass through unchanged. The state transition into a string is triggered by the quote character. **No special prefix logic is required.**

### Digit-run handling

When `DEFAULT` encounters a digit (ASCII, Arabic-Indic, or Eastern Arabic-Indic), look ahead to the end of the consecutive digit run (only digits — `.`, `e`, sign chars do NOT extend the run for this check). Categorize:

- Pure ASCII → emit unchanged.
- Pure Arabic-Indic → translate each digit to ASCII; emit.
- Pure Eastern Arabic-Indic → translate each digit to ASCII; emit.
- Mixed (more than one system in the run) → raise `SyntaxError` with message:
  ```
  SyntaxError: mixed digit systems in numeric literal at line L, column C — found ASCII and Arabic-Indic digits in '<run>'. Use one system per literal.
  ```
  (Or whichever two/three systems were detected; list them.)

## Implementation constraints

- **Dependencies**: stdlib only (`unicodedata` for character names in error messages).
- **Python version**: 3.11+.
- **Purity**: no I/O, no global state, no side effects.
- **Performance**: O(n) single pass over the input. Should handle a 10,000-line file in well under 100 ms.
- **Style**: pass `ruff check .` and `black --check .` at project defaults (line length 100).

## Implementation hints

- A single `for i, ch in enumerate(source)` loop with explicit `state` and look-ahead via `source[i:i+3]` is cleaner than using a buffer + `str.translate()`. The string-aware nature defeats simple `str.translate()`.
- Build the output as a `list[str]` and `"".join` at the end — much faster than string concatenation in a loop.
- Track `line` (1-indexed) and `col` (0-indexed) by incrementing on each character: `\n` resets col to 0 and increments line; everything else increments col.
- Triple-quote detection: when in `DEFAULT` and you see `'` or `"`, check `source[i:i+3]` against `'''` / `"""` first; only if no match, treat as single-line opener.
- Digit-system categorization: define three frozensets (`_ASCII_DIGITS`, `_ARABIC_INDIC_DIGITS`, `_EASTERN_ARABIC_INDIC_DIGITS`) and check membership.
- Translation tables: precompute three `str.maketrans` dicts (one per source system → ASCII), or one combined dict that maps all 20 source codepoints to their ASCII equivalents (used only in `DEFAULT` chunks, after digit-run validation).
- For bidi rejection: precompute a frozenset of the 9 codepoints. On encountering one in `DEFAULT` or `COMMENT`, raise immediately with the formatted message.
- For the bidi error message, use `unicodedata.name(ch)` to get the canonical Unicode name (e.g., "RIGHT-TO-LEFT OVERRIDE").

## Test requirements

All tests live in `tests/test_pretokenize.py`. Use exact test names below. Pytest only — no other framework.

### Basic passthrough (5)

1. `test_empty_string`: `pretokenize("")` returns `""`.
2. `test_pure_ascii_passthrough`: `pretokenize("x = 1\nprint(x)\n")` returns the same string.
3. `test_arabic_identifier_passthrough`: `pretokenize("اسم = 1\n")` returns the same string (no digits/punct/bidi to fold).
4. `test_keyword_chars_passthrough`: `pretokenize("def foo():\n    pass\n")` unchanged.
5. `test_only_whitespace_passthrough`: `pretokenize("   \n\t\n  ")` unchanged.

### Arabic-Indic digit folding (5)

6. `test_single_arabic_indic_digit`: `pretokenize("x = ٥")` returns `"x = 5"`.
7. `test_multi_digit_arabic_indic`: `pretokenize("x = ١٢٣")` returns `"x = 123"`.
8. `test_arabic_indic_in_expression`: `pretokenize("y = ٢ + ٣")` returns `"y = 2 + 3"`.
9. `test_arabic_indic_zero`: `pretokenize("x = ٠")` returns `"x = 0"`.
10. `test_arabic_indic_all_digits`: `pretokenize("x = ٠١٢٣٤٥٦٧٨٩")` returns `"x = 0123456789"`.

### Eastern Arabic-Indic digit folding (3)

11. `test_eastern_indic_digit`: `pretokenize("x = ۵")` returns `"x = 5"`.
12. `test_eastern_indic_multi`: `pretokenize("x = ۱۲۳")` returns `"x = 123"`.
13. `test_eastern_indic_all`: `pretokenize("x = ۰۱۲۳۴۵۶۷۸۹")` returns `"x = 0123456789"`.

### Arabic punctuation folding (4)

14. `test_arabic_comma`: `pretokenize("foo(a، b)")` returns `"foo(a, b)"`.
15. `test_arabic_semicolon`: `pretokenize("a = 1؛ b = 2")` returns `"a = 1; b = 2"`.
16. `test_arabic_question_mark`: `pretokenize("x ؟ y")` returns `"x ? y"`.
17. `test_multiple_arabic_commas`: `pretokenize("foo(a، b، c، d)")` returns `"foo(a, b, c, d)"`.

### Mixed-digit literal rejection (3)

18. `test_mixed_arabic_and_ascii_raises`: `pretokenize("x = ١2")` raises `SyntaxError` whose `str(e)` contains `"mixed digit"` and the literal `"١2"` (or both system names).
19. `test_mixed_arabic_and_eastern_raises`: `pretokenize("x = ١۲")` raises `SyntaxError` containing `"mixed digit"`.
20. `test_mixed_in_middle_of_expression_raises`: `pretokenize("y = 5 + ١2 - 3")` raises `SyntaxError` mentioning the mixed run.

### String preservation (8)

21. `test_arabic_digit_inside_single_quoted`: `pretokenize("x = '٥'")` returns `"x = '٥'"` (digit preserved inside string).
22. `test_arabic_digit_inside_double_quoted`: `pretokenize('x = "٥"')` returns `'x = "٥"'`.
23. `test_arabic_digit_inside_triple_single`: `pretokenize("x = '''٥'''")` returns `"x = '''٥'''"`.
24. `test_arabic_digit_inside_triple_double`: `pretokenize('x = """٥"""')` returns `'x = """٥"""'`.
25. `test_arabic_punct_inside_string`: `pretokenize("x = 'a، b'")` returns `"x = 'a، b'"` (Arabic comma preserved).
26. `test_arabic_digit_outside_then_inside`: `pretokenize("x = ٥; y = '٥'")` returns `"x = 5; y = '٥'"`.
27. `test_escaped_quote_in_string`: `pretokenize("x = 'a\\'b'")` returns the same string — the escaped quote does not end the string, so the digit-folding state stays inside the string.
28. `test_string_after_string`: `pretokenize("x = 'a' + 'b'")` returns the same; the closing `'` correctly returns to DEFAULT and the next `'` correctly opens a new string.

### String prefixes (4)

29. `test_raw_string_prefix`: `pretokenize("x = r'٥'")` returns the same — `r` prefix doesn't change pretokenize behavior, content preserved.
30. `test_byte_string_prefix`: `pretokenize("x = b'٥'")` returns the same.
31. `test_f_string_prefix_content_preserved`: `pretokenize("x = f'٥'")` returns the same — entire f-string is opaque to pretokenize.
32. `test_uppercase_prefix`: `pretokenize("x = R'٥'")` returns the same.

### Comments (3)

33. `test_arabic_digit_in_comment_folded`: `pretokenize("# value is ٥\nx = 1")` returns `"# value is 5\nx = 1"` (comments are NOT strings; substitution applies).
34. `test_arabic_punct_in_comment_folded`: `pretokenize("# a، b\nx = 1")` returns `"# a, b\nx = 1"`.
35. `test_comment_ends_at_newline`: `pretokenize("# ٥\n٥ = 1")` returns `"# 5\n5 = 1"` — the second `٥` is in DEFAULT (after the comment ended), so it folds.

### Bidi rejection — 9 codepoints, outside strings (9)

36. `test_bidi_lre_rejected`: source with `U+202A` outside any string raises `SyntaxError` whose `str(e)` contains `"U+202A"`, `"LEFT-TO-RIGHT EMBEDDING"`, and `"trojansource.codes"`.
37. `test_bidi_rle_rejected`: same for `U+202B` ("RIGHT-TO-LEFT EMBEDDING").
38. `test_bidi_pdf_rejected`: same for `U+202C` ("POP DIRECTIONAL FORMATTING").
39. `test_bidi_lro_rejected`: same for `U+202D` ("LEFT-TO-RIGHT OVERRIDE").
40. `test_bidi_rlo_rejected`: same for `U+202E` ("RIGHT-TO-LEFT OVERRIDE").
41. `test_bidi_lri_rejected`: same for `U+2066` ("LEFT-TO-RIGHT ISOLATE").
42. `test_bidi_rli_rejected`: same for `U+2067` ("RIGHT-TO-LEFT ISOLATE").
43. `test_bidi_fsi_rejected`: same for `U+2068` ("FIRST STRONG ISOLATE").
44. `test_bidi_pdi_rejected`: same for `U+2069` ("POP DIRECTIONAL ISOLATE").

### Bidi inside strings is allowed (3)

45. `test_bidi_in_single_quoted_passes`: `pretokenize("x = '\u202E'")` returns the same source unchanged.
46. `test_bidi_in_triple_quoted_passes`: `pretokenize("x = '''\u202E'''")` unchanged.
47. `test_bidi_in_docstring_passes`: a triple-quoted string at module top with embedded U+202E passes through unchanged.

### Bidi in comments is REJECTED (1)

48. `test_bidi_in_comment_rejected`: `pretokenize("# \u202E hidden")` raises `SyntaxError` mentioning `U+202E` and the column. (Per ADR 0006: comments are an attack vector, not a safe haven.)

### Line/column accuracy in error messages (2)

49. `test_bidi_error_line_column`: `pretokenize("x = 1\ny = \u202E")` raises `SyntaxError` whose message contains `"line 2"` and `"column 4"` (zero-indexed col where U+202E sits).
50. `test_mixed_digit_error_line_column`: `pretokenize("a = 1\nb = ١2")` raises `SyntaxError` mentioning `"line 2"`.

### Idempotency on ASCII (1)

51. `test_idempotent_on_ascii_python`: a small valid ASCII Python program runs through `pretokenize` and the output is byte-equal to the input. Use this fixture:
    ```python
    src = '''def foo(x, y):
        if x > y:
            return x
        return y
    '''
    ```

### Combined transformation (2)

52. `test_full_arabic_function`: input
    ```python
    """def اضافة(a، b):
        return a + b

    print(اضافة(٢، ٣))
    """
    ```
    expected output:
    ```python
    """def اضافة(a, b):
        return a + b

    print(اضافة(2, 3))
    """
    ```

53. `test_string_with_arabic_inside_arabic_function`: input
    ```python
    'تحية = "مرحبا، يا عالم"\n'
    ```
    expected output:
    ```python
    'تحية = "مرحبا، يا عالم"\n'
    ```
    (The Arabic comma inside the string must NOT be folded.)

## Reference materials

- `decisions/0005-numerals-punctuation.md` — authoritative.
- `decisions/0006-bidi-policy.md` — authoritative, includes exact error format.
- Python `unicodedata.name` docs: https://docs.python.org/3/library/unicodedata.html
- Python tokenize behavior reference: https://docs.python.org/3/library/tokenize.html
- Trojan Source paper: https://trojansource.codes/trojan-source.pdf

## Open questions for the planner

None. If a real ambiguity arises, stop and write a question in the delivery note rather than guessing.

## Acceptance checklist

- [ ] `arabicpython/pretokenize.py` created with the exact public interface above.
- [ ] `tests/test_pretokenize.py` created with all 53 tests.
- [ ] `pytest tests/test_pretokenize.py` passes on Python 3.11, 3.12, 3.13.
- [ ] `ruff check .` clean; `black --check .` clean.
- [ ] No new dependencies in `pyproject.toml`.
- [ ] CI green across all 9 matrix cells.
- [ ] `specs/0004-pretokenize-v1.delivery.md` written covering shipped behavior, deviations (if any), implementation notes, and open questions.

## Workflow for the implementer

1. Create branch `packet/0004-pretokenize-v1` from `main`.
2. Implement the two files.
3. Run `pytest tests/test_pretokenize.py` locally until green.
4. Run `ruff check .` and `black --check .` until clean.
5. Commit. Suggested message: `Packet 0004: implement pretokenize per ADR 0005/0006`.
6. Push.
7. Write `specs/0004-pretokenize-v1.delivery.md`.
8. Open a PR titled `Packet 0004: pretokenize-v1` linking back to this spec.
9. Wait for CI and planner review.

## Allowed edit scope

- `arabicpython/pretokenize.py` (new)
- `tests/test_pretokenize.py` (new)
- `specs/0004-pretokenize-v1.delivery.md` (new)

Do NOT modify: any other module, any ADR, the dictionary, `pyproject.toml`, the CI workflow, or existing tests.
