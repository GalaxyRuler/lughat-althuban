# Spec Packet 0011: fstring-interior-3-11

**Phase**: A (post-wrap fix)
**Depends on**: Packet 0002 (normalize), Packet 0003 (dialect-loader), Packet 0004 (pretokenize), Packet 0005 (core-translate-v1) — all merged. ADR 0001 (architecture), ADR 0004 (normalization).
**Estimated size**: medium (1–2 sessions: mini-parser is subtle around format specs and nested braces)

## Goal

Close the Phase A gap discovered during Packet 0010 delivery: on Python 3.11, identifiers inside f-string expression regions (`f"...{expr}..."`) are not translated or normalized, because CPython 3.11 emits the entire f-string as a single `STRING` token and the Packet 0005 NAME-rewriter never sees the inner identifiers. On 3.12+ PEP 701 exposes `FSTRING_*` tokens and the current rewriter handles them naturally. This packet adds a 3.11-only sub-pass that parses f-string literals, rewrites identifiers inside `{...}` expressions through the same `normalize_identifier` + dialect-lookup logic used elsewhere, and substitutes the rewritten f-string back into the token stream. On 3.12+ the new code path is a no-op. Public API (`translate(source, *, dialect=None) -> str`) is unchanged.

The motivating regression is reproducible today by reverting `examples/05_data_structures.apy` to its spec-original form (`f"{الأسعار[فاكهة]}"`) and running the suite on 3.11: `NameError: name 'فاكهه' is not defined` because the outer `لكل فاكهة` is normalized (`ة → ه`) but the inner `فاكهة` inside the f-string is not.

## Non-goals

- **Does not change 3.12+ behavior.** The existing `FSTRING_MIDDLE` / inner `NAME` path already works; the new code must detect the 3.11 `STRING`-token case and leave other tokens alone. No version-gated rewrites on 3.12+.
- **Does not drop Python 3.11 support.** See "Alternatives considered" for why. `requires-python = ">=3.11"` in `pyproject.toml` stays. The CI matrix row for 3.11 stays.
- **Does not touch the CLI, import hook, REPL, or traceback layers.** They call `translate` and inherit the fix for free.
- **Does not alter ADR 0004 semantics.** Strict mode still skips the aggressive fold; strict-mode f-strings get `normalize_identifier(..., strict=True)` applied to inner NAMEs exactly as non-f-string NAMEs do today.
- **Does not attempt to preserve byte-for-byte layout of untouched f-strings.** Goal is semantic equivalence plus identifier rewrite; whitespace inside `{...}` may change by at most what `tokenize.untokenize` would already change for equivalent bare expressions elsewhere.
- **Does not translate literal text outside `{...}`.** Only the expression interior is touched. The string body between braces is opaque, same as ordinary string literals.
- **Does not handle bytes string literals (`b"..."`).** f-strings cannot be bytes in any Python version — nothing to do.
- **Does not reimplement an f-string parser for 3.12+.** On 3.12+ the stock tokenizer already gives us what we need; the new code is guarded behind `sys.version_info < (3, 12)`.
- **Does not add a dependency.** Stdlib only (`sys`, `tokenize`, `io`, plus the existing `arabicpython.normalize` / `arabicpython.dialect`).

## Files

### Files to create

- `arabicpython/_fstring_311.py` — the mini-parser + rewriter. Leading underscore signals "package-internal, not public API."
- `tests/test_fstring_311.py` — unit tests for the helper.

### Files to modify

- `arabicpython/translate.py` — in the NAME-rewrite loop, when the current token is `tokenize.STRING` and `sys.version_info < (3, 12)`, route its `.string` through `_fstring_311.rewrite_fstring_literal(...)` (which is a no-op for non-f-string literals) and emit a replacement `STRING` token. On 3.12+ the branch is short-circuited. Public signature of `translate` unchanged; imports add `sys` and `from arabicpython._fstring_311 import rewrite_fstring_literal`.
- `tests/test_translate.py` — add three new tests (see "Test requirements" below). Do not modify existing tests.
- `examples/05_data_structures.apy` — restore the original spec form:
  ```
  # القوائم والقواميس
  الفواكه = ["تفاح", "موز", "برتقال"]
  الأسعار = {"تفاح": 3, "موز": 2, "برتقال": 4}

  لكل فاكهة في الفواكه:
      اطبع(f"{فاكهة}: {الأسعار[فاكهة]} ريال")
  ```
  (This is the form originally specified in Packet 0010 § "Example file contents" → `05_data_structures.apy`, which was downgraded to positional `print()` args during the 0010 planner addendum as a workaround.)
- `tests/test_examples.py` — `test_05_data_structures_runs` expected stdout changes back to the 3-line `"تفاح: 3 ريال\n..."` block originally specified in Packet 0010.

### Files to read (do not modify)

- `arabicpython/translate.py` — current rewrite loop (lines 62–108); this packet splices into it.
- `arabicpython/normalize.py` — `normalize_identifier` signature (the `strict` kwarg must be threaded through).
- `arabicpython/dialect.py` — `Dialect` dataclass; same `names` / `attributes` tables the outer loop uses.
- `arabicpython/pretokenize.py` — note that pretokenize preserves string interiors byte-for-byte, so the f-string text we see in the `STRING` token is exactly what the user wrote (modulo quoting). The inner expression region is therefore valid Python 3.11 f-string expression syntax.
- `specs/0010-examples-v1.delivery.md` → "Planner addendum" — the root-cause writeup that motivates this packet.
- `decisions/0004-normalization-policy.md` — strict-mode semantics.
- PEP 701 — https://peps.python.org/pep-0701/ (reference for why 3.12+ doesn't need this code).

## Public interfaces

`translate` is unchanged; only its internals grow. The new module exposes one package-internal function.

```python
# arabicpython/_fstring_311.py

def rewrite_fstring_literal(literal: str, dialect: "Dialect", *, strict: bool = False) -> str:
    """Rewrite identifiers inside an f-string literal's expression regions.

    Intended for use on Python 3.11 only, where the outer tokenizer emits
    the entire f-string as a single STRING token and the Packet 0005
    NAME-rewriter cannot see inner identifiers. Callers on Python 3.12+
    should not invoke this function — the stock tokenizer already exposes
    inner NAME tokens.

    Behavior:
      - If `literal` is not an f-string (prefix does not contain 'f'/'F'),
        returns `literal` unchanged.
      - Otherwise, parses the literal to locate expression regions
        delimited by `{...}`, honoring:
          * doubled braces `{{` and `}}` as literal escapes (not expressions),
          * nested `[...]`, `(...)`, `{...}` inside expressions (parens balance),
          * `!r`/`!s`/`!a` conversion markers (passed through verbatim),
          * `:...` format-spec tails (rewritten recursively, since format
            specs may themselves contain `{expr}` substitutions),
          * self-documenting `=` (e.g. `{x=}`) — the literal `x` before the
            `=` is part of the expression; the trailing `=` is not.
      - For each expression region, runs the same NAME-rewrite pass used
        by `translate`: tokenize the expression source, normalize each
        NAME, look up `dialect.attributes` (if preceded by OP '.')
        or `dialect.names`, substitute, untokenize.
      - Reassembles the f-string with rewritten expressions substituted
        in place; quote style (single/double, triple), prefix flags
        (`f`, `rf`, `Rf`, `fr`, etc.), and non-expression text are
        preserved byte-for-byte.

    Args:
        literal: the full source text of a STRING token, including
            prefix and quote delimiters (e.g., `f"hello {x}"` or
            `rf'''a {x!r:>10} b'''`).
        dialect: the `Dialect` used by the surrounding translate pass.
        strict: if True, inner NAMEs are normalized with
            `normalize_identifier(..., strict=True)` (NFKC only,
            matching ADR 0004 strict mode).

    Returns:
        The rewritten literal text (suitable for placing back into a
        `tokenize.TokenInfo` of type STRING).

    Raises:
        SyntaxError: if the literal is malformed as an f-string
            (unbalanced braces, unterminated expression, etc.).
            Message includes the offending fragment.

    Examples:
        >>> rewrite_fstring_literal('f"hello"', dialect)
        'f"hello"'
        >>> # assume dialect.names maps normalized 'اطبع' → 'print'
        >>> rewrite_fstring_literal('f"{اطبع}"', dialect)
        'f"{print}"'
        >>> # ta-marbuta normalization inside expression
        >>> rewrite_fstring_literal('f"{فاكهة}"', dialect)
        'f"{فاكهه}"'
        >>> # nested format spec with expression
        >>> rewrite_fstring_literal('f"{x:>{width}}"', dialect)
        'f"{x:>{width}}"'
        >>> # non-f-string untouched
        >>> rewrite_fstring_literal('"{not an expr}"', dialect)
        '"{not an expr}"'
    """
```

The module may define private helpers (`_find_expression_spans`, `_rewrite_expression_source`, `_parse_prefix`) — none are exported.

## Algorithm details

### Step 0 — version guard in `translate.py`

In the main rewrite loop in `arabicpython/translate.py` (currently around lines 86–104), add a branch for `STRING` tokens:

```python
elif tok.type == tokenize.STRING and sys.version_info < (3, 12):
    new_literal = rewrite_fstring_literal(tok.string, dialect, strict=_strict_from_source(source))
    if new_literal == tok.string:
        new_tokens.append(tok)
    else:
        new_tokens.append(
            tokenize.TokenInfo(tokenize.STRING, new_literal, tok.start, tok.end, tok.line)
        )
```

Notes:
- `sys.version_info < (3, 12)` is the ONLY version check. On 3.12+ we keep today's behavior.
- `rewrite_fstring_literal` is defensive: if the literal is not an f-string, it returns `literal` unchanged, so the branch is cheap for non-f-string STRING tokens.
- Strict mode: Packet 0005 / ADR 0004 specify a `# apython: strict` magic comment or `--strict` CLI flag. Whether strict mode is currently wired into `translate()` is an open question (see "Open questions for the planner"). The implementer should thread whatever the outer loop uses for strict mode into `rewrite_fstring_literal` via the `strict` kwarg. If strict mode is not yet plumbed through `translate()` itself, default `strict=False` is correct and this packet does not need to add the plumbing.

### Step 1 — prefix parse

An f-string prefix is any case-insensitive permutation of `{f, r}` with `f` present. Valid: `f`, `F`, `rf`, `Rf`, `rF`, `RF`, `fr`, `fR`, `Fr`, `FR`. Not valid in 3.11: `b` / `u` combined with `f`. Extract the prefix (the run of ASCII letters before the first `'` or `"`) and the quote delimiter (single `'`, single `"`, `'''`, or `"""`).

- If the prefix does not contain `f` or `F` (case-insensitive): return `literal` unchanged.
- Otherwise, record whether the raw flag (`r`/`R`) is present (affects whether the expression is in a raw context — relevant mostly for how we preserve the rest, not for parsing `{...}` itself).

### Step 2 — locate expression spans

Walk the body between the opening and closing quotes. Maintain:
- `depth`: integer, initially 0, tracking `(`, `[`, `{` minus matching closers inside the current expression.
- `in_expr`: bool, initially False.
- `expr_start`: index into body where current expression's source begins.

Rules:
- When `in_expr is False`:
  - `{{` → emit as two literal `{` chars, advance 2.
  - `}}` → emit as two literal `}` chars, advance 2.
  - `{` → begin expression. `in_expr = True`, `expr_start = i + 1`, `depth = 0`, advance 1.
  - `}` (unpaired, not doubled) → SyntaxError: "single '}' in f-string literal".
  - any other char → emit verbatim.
- When `in_expr is True`:
  - track parens: `(`, `[`, `{` increment `depth`; `)`, `]` decrement `depth`.
  - A `}` at `depth == 0` ends the expression at `i`; the expression text is `body[expr_start:i]` (before any conversion or format-spec tail handling — see Step 3).
  - A `}` at `depth > 0` decrements `depth` (closing a nested dict/set/format-spec sub-brace).
  - A `!` at `depth == 0` followed by `r`, `s`, or `a` begins the conversion marker; the expression text ends just before the `!`. Resume scanning after the marker character for a possible `:` format spec.
  - A `:` at `depth == 0` begins the format spec; the expression text ends just before the `:`. The format spec runs from after the `:` to the matching `}` at depth 0, but may itself contain `{...}` nested-expression regions which must be parsed recursively.
  - An `=` at `depth == 0` that is NOT followed by `=` is the self-documenting marker (e.g., `{x=}`). The expression text ends just before the `=`. The `=` is emitted verbatim, and scanning continues for an optional `!` conversion or `:` format spec.
  - Backslashes inside `{...}` are forbidden on Python 3.11 (the interpreter raises `SyntaxError`). This packet need not re-validate — if the user wrote an invalid f-string, CPython will reject it when the translated output is compiled. But if parsing encounters `\` inside `{...}` that makes span-finding ambiguous, raise `SyntaxError` with a clear message.

At the end of body: if `in_expr is True`, raise `SyntaxError` ("expected '}' before end of f-string").

Output of this step: a list of `(literal_prefix_start, expr_start, expr_end, conversion_marker, format_spec_start, format_spec_end, expr_region_end)` tuples identifying each expression region's sub-ranges.

### Step 3 — rewrite each expression's source

For each expression span, take `body[expr_start:expr_end]`. This is a Python *expression* source (on 3.11, syntactically restricted: no backslashes, no same-quote strings, etc.). Rewrite it using a helper that mirrors the outer `translate.py` NAME loop:

```python
def _rewrite_expression_source(expr_src: str, dialect: Dialect, *, strict: bool) -> str:
    # Wrap in a dummy assignment so tokenize can see a complete statement.
    wrapped = "_ = (" + expr_src + ")\n"
    tokens = list(tokenize.tokenize(io.BytesIO(wrapped.encode("utf-8")).readline))
    # walk tokens, same logic as translate.py:
    #   - NAME + last_significant OP('.') → dialect.attributes lookup
    #   - NAME otherwise → dialect.names lookup
    #   - fallback → normalize_identifier(name, strict=strict)
    # untokenize, strip the "_ = (" prefix and ")\n" suffix.
    # return just the rewritten expression text.
```

Subtleties:
- Wrapping the expression in `_ = (...)` makes it a complete tokenizable statement and sidesteps issues with bare expressions that start with operators (rare in f-strings but possible). After untokenize, the prefix/suffix are stripped by string-slicing on the known wrapper.
- If the inner tokenize raises `TokenError`, propagate as `SyntaxError` with message naming the offending f-string fragment.
- The attribute-context tracking inside the expression is local to that expression — the outer f-string's surrounding tokens are irrelevant (an expression starts with a fresh `last_significant = None`).

If the format spec is non-empty and itself contains `{...}` regions, recursively apply Step 2/3 to the format-spec body. (Format-spec NAMEs *outside* nested `{}` — e.g., the `>` / `10` in `{x:>10}` — are not identifiers in the dialect's sense and pass through unchanged.)

### Step 4 — reassemble

Walk the body from left to right; for each expression span, substitute the rewritten expression text (plus unchanged conversion marker, `=`, and format spec with its own inner substitutions) in place of the original expression text. Literal text outside expressions is copied verbatim. Prepend the prefix and leading quote; append the trailing quote. Return the reassembled literal.

### Step 5 — untokenize interaction

`tokenize.untokenize` in Python 3.11 tolerates `TokenInfo(STRING, "<arbitrary string>", ...)` — it emits the string verbatim. Verify with a round-trip test. If untokenize emits a BOM, the existing `translate` BOM-strip handles it.

## Implementation constraints

- **Python version**: package still requires `>=3.11`; new code runs on 3.11–3.13 (no-op on 3.12+).
- **Dependencies allowed**: stdlib only (`io`, `sys`, `tokenize`), plus internal imports of `arabicpython.normalize`, `arabicpython.dialect`.
- **Forbidden**: regex-based f-string parsing (too error-prone around nested braces and format specs); mutating `arabicpython.translate.translate`'s public signature; adding new public symbols to `arabicpython/__init__.py`; silent fallback that leaves malformed f-strings un-rewritten (must raise `SyntaxError`).
- **Style**: `ruff check .` clean; `black --check .` clean; line length 100.
- **Performance budget**: the common case (no f-strings) adds one `isinstance`/prefix check per STRING token; target overhead <5% on the Packet 0005 `test_program_*` tests on 3.11. F-string-heavy files translate in O(body length) total.
- **Purity**: no I/O, no global mutable state, no caching.
- **Imports in `translate.py`**: add `import sys` and `from arabicpython._fstring_311 import rewrite_fstring_literal`. Keep the existing imports.

## Test requirements

### `tests/test_fstring_311.py` (new)

Use `pytest.mark.skipif(sys.version_info >= (3, 12), ...)` on every test in this file — these tests exercise the 3.11 code path specifically. (The 3.12+ behavior is already covered by Packet 0005 test 52 `test_fstring_arabic_expr_312_plus_translates`.)

Load the default `ar-v1` dialect once (module-level fixture).

1. `test_non_fstring_passes_through`:
   - Input: `rewrite_fstring_literal('"hello"', dialect)`
   - Expected: returns `'"hello"'` unchanged. Same for `"'x'"`, `'r"raw"'`, `'"""triple"""'`.

2. `test_fstring_no_expressions_passes_through`:
   - Input: `rewrite_fstring_literal('f"no expressions here"', dialect)`
   - Expected: returns `'f"no expressions here"'` unchanged.

3. `test_fstring_simple_keyword_rewrite`:
   - Input: `rewrite_fstring_literal('f"{اطبع}"', dialect)` (the Arabic for `print` as an inner expression).
   - Expected: contains `'{print}'`.

4. `test_fstring_normalizes_ta_marbuta`:
   - Input: `rewrite_fstring_literal('f"{فاكهة}"', dialect)`
   - Expected: contains `'فاكهه'` (ta-marbuta folded to ha per ADR 0004).

5. `test_fstring_subscript_with_arabic_names`:
   - Input: `rewrite_fstring_literal('f"{الأسعار[فاكهة]}"', dialect)`
   - Expected: both `الأسعار` and `فاكهة` are normalized inside, producing `f"{الاسعار[فاكهه]}"` (or whatever the normalizer maps the outer identifier to — assert equal to calling `normalize_identifier` on each name independently).

6. `test_fstring_doubled_braces_are_literal`:
   - Input: `rewrite_fstring_literal('f"{{اطبع}}"', dialect)` — doubled braces mean literal `{اطبع}`, no expression.
   - Expected: returns input unchanged.

7. `test_fstring_mixed_literal_and_expr`:
   - Input: `rewrite_fstring_literal('f"before {فاكهة} after"', dialect)`
   - Expected: `'before '` and `' after'` are byte-preserved; `فاكهة` is normalized to `فاكهه`.

8. `test_fstring_conversion_marker_preserved`:
   - Input: `rewrite_fstring_literal('f"{اطبع!r}"', dialect)`
   - Expected: contains `'{print!r}'` (conversion `!r` untouched).

9. `test_fstring_format_spec_preserved`:
   - Input: `rewrite_fstring_literal('f"{x:>10}"', dialect)`
   - Expected: `':>10'` passes through; `x` normalized (identity for ASCII).

10. `test_fstring_nested_format_spec_with_expression`:
    - Input: `rewrite_fstring_literal('f"{x:>{عرض}}"', dialect)` (Arabic identifier as the dynamic width).
    - Expected: inner `عرض` is normalized through the nested-brace recursion.

11. `test_fstring_self_documenting_equals`:
    - Input: `rewrite_fstring_literal('f"{فاكهة=}"', dialect)` (3.8+ `x=` form).
    - Expected: expression normalized to `فاكهه`; literal `=` preserved.

12. `test_fstring_nested_expression_with_dict`:
    - Input: `rewrite_fstring_literal('f"{{\'a\': 1}[\'a\']}"', dialect)` — inner braces are a dict literal inside an expression (depth > 0 braces).
    - Expected: parses correctly (doesn't treat inner `{` as a new expression); returns something semantically equivalent when compiled.

13. `test_fstring_triple_quoted`:
    - Input: `rewrite_fstring_literal("f'''line1\\n{فاكهة}\\nline2'''", dialect)`
    - Expected: triple-quoted form preserved; `فاكهة` normalized.

14. `test_fstring_raw_prefix_rf`:
    - Input: `rewrite_fstring_literal('rf"{فاكهة}"', dialect)`
    - Expected: prefix `rf` preserved exactly (order and case); inner expression rewritten.

15. `test_fstring_attribute_access_inside`:
    - Input: `rewrite_fstring_literal('f"{obj.قراءة}"', dialect)` — Arabic method name (check dictionary for actual mapping; use one that appears in `dialect.attributes`).
    - Expected: attribute-position lookup against `dialect.attributes`, not `dialect.names` (mirrors outer rewriter's behavior).

16. `test_fstring_unbalanced_raises`:
    - Input: `rewrite_fstring_literal('f"{x"', dialect)` (missing `}`).
    - Expected: raises `SyntaxError` with message containing `"f-string"`.

17. `test_fstring_single_closing_brace_raises`:
    - Input: `rewrite_fstring_literal('f"oops }"', dialect)`.
    - Expected: raises `SyntaxError` with message containing `"single"` or `"unmatched"`.

18. `test_fstring_strict_mode_skips_fold`:
    - Input: `rewrite_fstring_literal('f"{فاكهة}"', dialect, strict=True)`.
    - Expected: `فاكهة` is NOT folded to `فاكهه` (only NFKC applied). The rewritten literal contains the original form.

19. `test_non_fstring_with_braces_untouched`:
    - Input: `rewrite_fstring_literal('"{اطبع}"', dialect)` — regular string, not f-string.
    - Expected: returns input unchanged.

20. `test_byte_preservation_outside_expressions`:
    - Input: `rewrite_fstring_literal('f"  spaces\\ttab {x}"', dialect)`.
    - Expected: the literal prefix `'  spaces\\ttab '` is byte-identical in the output (including the escape sequence source).

### `tests/test_translate.py` additions

21. `test_translate_fstring_arabic_expr_on_311` (renamed / new; no skipif):
    - Input: `translate('x = 1\nاطبع(f"{x}")\n')` on any Python version.
    - Expected: compiles; contains `print`.

22. `test_translate_fstring_arabic_identifier_normalized_on_311`:
    - Input: `translate('فاكهة = 1\nاطبع(f"{فاكهة}")\n')`.
    - Expected on Python 3.11: the outer `فاكهة` and the inner f-string `فاكهة` are both normalized to `فاكهه`, so the translated Python is executable (`exec`-ing it in a fresh namespace prints `1`).
    - Expected on Python 3.12+: same behavior (already worked; this test now guards against regression on both versions).

23. `test_translate_fstring_subscript_regression_packet_0010`:
    - Input: the exact program from `examples/05_data_structures.apy` after this packet restores the f-string form.
    - Expected: `translate` + `compile` + `exec` produces the 3-line `"تفاح: 3 ريال\n..."` stdout on 3.11, 3.12, and 3.13. This is the direct regression test for the Packet 0010 bug.

### `tests/test_examples.py` modification

- `test_05_data_structures_runs` — update expected stdout to the 3-line form originally specified in Packet 0010:
  ```
  تفاح: 3 ريال
  موز: 2 ريال
  برتقال: 4 ريال
  ```
  No other test in that file changes.

### Edge cases that must be covered

Already listed inline under `test_fstring_311.py`. Also:

- **Empty expression**: `f"{}"` is a SyntaxError even in stock Python — the packet's parser should either raise or let the downstream `compile` call catch it. Document which; a test asserting either behavior is sufficient.
- **Adjacent string concatenation**: `f"{x}" "tail"` — each STRING token is handled independently; this "just works" because the outer loop walks tokens one at a time.
- **Comment-like content inside string**: the `#` inside a string is not a comment (already handled by the tokenizer); no action needed.
- **Escape sequences in literal portion of raw f-strings**: `rf"\n{x}"` — the `\n` is a literal backslash-n (raw), NOT a newline. Preserve the two characters byte-identically.

## Reference materials

- `decisions/0001-architecture.md` — confirms tokenize-based rewrite is the only transformation layer; this packet stays within that envelope.
- `decisions/0004-normalization-policy.md` — strict mode semantics. Inner-expression NAMEs must honor the same `strict` flag as outer NAMEs.
- `specs/0005-core-translate-v1.md` § "F-string handling (version-dependent)" — the original non-goal that this packet relaxes. Also § "CPython 3.11 tokenizer gaps".
- `specs/0010-examples-v1.delivery.md` § "Planner addendum" → item 2 — root-cause writeup of the bug this packet fixes.
- PEP 701 — https://peps.python.org/pep-0701/ — why 3.12+ doesn't need this code. Useful context for reviewers but not code.
- Python `tokenize` docs — https://docs.python.org/3/library/tokenize.html — `TokenInfo`, `untokenize` round-trip caveats.
- CPython 3.11 `Lib/tokenize.py` f-string handling — for reference on exactly how 3.11 emits STRING tokens for f-strings.
- Prior art: nothing in zhpy (Chinese Python); zhpy predates f-strings entirely. This is genuinely new territory for the dialect pattern.

## Planner decisions (resolved before handoff)

1. **Strict mode is NOT plumbed through `translate()` today.** Verified by planner: `translate(source, *, dialect=None)` has no `strict` parameter, and `arabicpython/translate.py` line 88 calls `normalize_identifier(tok.string)` with no kwarg. Therefore `strict=False` is the correct default for `rewrite_fstring_literal` and this packet MUST NOT add strict-mode plumbing to `translate()`. The `strict` kwarg on `rewrite_fstring_literal` is forward-looking — kept in the signature so a future strict-mode packet can wire it through without re-shaping this API. Test 18 (`test_fstring_strict_mode_skips_fold`) exercises the function directly and is sufficient coverage.

2. **Add a `# TODO(phase-b-drop-311)` comment on the version-guard branch in `translate.py`.** Planner decision: yes. Cheap insurance against the dead code being forgotten when the version-support ADR eventually lands. Suggested wording: `# TODO(phase-b-drop-311): delete this branch and rewrite_fstring_literal when 3.11 support is dropped.`

## Acceptance checklist

- [ ] `arabicpython/_fstring_311.py` created with `rewrite_fstring_literal` and its private helpers.
- [ ] `arabicpython/translate.py` modified to route STRING tokens through the rewriter on Python < 3.12. Public signature unchanged.
- [ ] `tests/test_fstring_311.py` created with tests 1–20.
- [ ] `tests/test_translate.py` — tests 21–23 added; existing tests unchanged.
- [ ] `examples/05_data_structures.apy` restored to the Packet 0010 spec form (f-string with subscript).
- [ ] `tests/test_examples.py` — `test_05_data_structures_runs` expected stdout updated.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11, 3.12, 3.13 across Linux/macOS/Windows (CI proves this).
- [ ] Delivery note `0011-fstring-interior-3-11.delivery.md` written.

## Workflow for the implementer

1. Create branch `packet/0011-fstring-interior-3-11` from `main`.
2. Implement `arabicpython/_fstring_311.py` first; drive it with `tests/test_fstring_311.py` until all 20 tests pass on Python 3.11.
3. Wire into `arabicpython/translate.py`. Add the three `tests/test_translate.py` tests.
4. Restore `examples/05_data_structures.apy` and update `tests/test_examples.py`.
5. Run the full suite on 3.11 locally. Then run on 3.12 and 3.13 if available. **Validate on 3.11 specifically before declaring done — the bug and fix are 3.11-only, and the Packet 0010 delivery note flagged "local-only on 3.13" as a prior failure mode.**
6. Run `ruff check .` and `black --check .` until clean.
7. Commit. Suggested message: `Packet 0011: rewrite identifiers inside f-strings on Python 3.11`.
8. Push; open PR titled `Packet 0011: fstring-interior-3-11` linking back to this spec.
9. Write `specs/0011-fstring-interior-3-11.delivery.md`.
10. Wait for 9-of-9 CI green; then planner review.

## Allowed edit scope

- `arabicpython/_fstring_311.py` (new)
- `arabicpython/translate.py` (modify — add routing branch and imports only; do not restructure the existing loop)
- `tests/test_fstring_311.py` (new)
- `tests/test_translate.py` (add tests 21–23 only)
- `examples/05_data_structures.apy` (restore original form)
- `tests/test_examples.py` (update `test_05_data_structures_runs` expected stdout only)
- `specs/0011-fstring-interior-3-11.delivery.md` (new)

Do NOT modify: any ADR, the dictionary, `pyproject.toml`, the CI workflow, `arabicpython/pretokenize.py`, `arabicpython/normalize.py`, `arabicpython/dialect.py`, `arabicpython/cli.py`, `arabicpython/import_hook.py`, `arabicpython/repl.py`, `arabicpython/tracebacks.py`, or any other test file. If you believe the spec has a bug, flag it in the delivery note rather than silently deviating.

## Alternatives considered (for planner + future readers)

### Alternative A — drop Python 3.11 support

Change `requires-python = ">=3.12"` in `pyproject.toml`; remove the `"3.11"` row from the CI matrix; update the README line "Requires Python 3.11+" to "Requires Python 3.12+"; delete the `pytest.mark.skipif(sys.version_info < (3, 12), ...)` guards on the two harakat tests in `tests/test_translate.py`; delete the `ERRORTOKEN` scan in `translate.py` (3.12+ always raises `TokenError`); close the f-string bug by construction.

**Implications:**
- ~40 LOC of 3.11-specific code and test guards disappear across `translate.py`, `test_translate.py`.
- Users on distros that ship 3.11 as default (Ubuntu 22.04 LTS, RHEL 9, Debian 12) would need a newer Python. Ubuntu 22.04 LTS is supported through April 2027; dropping support for its default Python during Phase A is a meaningful user-facing cost for an education-oriented project.
- A new ADR would be warranted (e.g., `decisions/0008-python-version-support.md`) explaining why we dropped the LTS-distro default and at what Phase B cadence we add/remove versions.
- All three Phase A "CPython 3.11 tokenizer gaps" documented in Packet 0005 become non-issues.

**Recommendation: do not drop 3.11 at this time.** The Phase A charter was "track upstream CPython releases with near-zero friction" and that includes the most widely deployed LTS-distro default. The in-pipeline fix in this packet is contained (~200 LOC of new code in a single internal module) and well-bounded by tests. The version-drop decision is better made once Phase B is chartered and user-base data exists.

If the planner overrides this recommendation, the deliverable becomes a small packet + ADR rather than the in-pipeline fix; the existing sections of this spec ("Files to create/modify", "Test requirements") would be replaced with a much shorter delete-and-document list. Flag the decision before the implementer starts.

### Alternative B — AST-based rewrite of f-strings on 3.11

Parse the whole source with `ast.parse` on 3.11 to get `JoinedStr` / `FormattedValue` nodes, rewrite, and `ast.unparse`. Rejected: `ast.unparse` does not preserve source formatting, loses comments, and would require running the translator twice (once on tokens for everything else, once on AST for f-strings) with reconciliation between the two. The text-level mini-parser proposed here stays consistent with the rest of the pipeline, which is tokenize-based by ADR 0001.

### Alternative C — regex-based f-string parsing

Rejected under "Forbidden" above. Format specs with nested `{...}` and self-documenting `=` cannot be parsed reliably with regex without a depth-tracking state machine, and once you have a state machine you don't need the regex.
