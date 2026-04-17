# 0001 — Architecture: source-to-source preprocessor

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

To let users write Python in Arabic we need some mechanism that turns Arabic source into something CPython can execute. The space of approaches spans from "thin textual substitution" to "fork CPython and ship a custom interpreter." Each point on that spectrum has different costs, reversibility properties, and maintenance burdens.

The primary constraint is that Phase A must ship in months, not years, and must track upstream CPython releases with near-zero friction. Phase B may relax this later for error-message localization, but not now.

A secondary constraint is that the architecture must not foreclose Phase B. Specifically: whatever we pick must coexist with (a) a name-aliasing layer for third-party libraries, (b) a translated-traceback layer, and (c) an eventual CPython fork for localized error messages. Anything that conflicts with any of those three is disqualified.

The reference implementation we study is zhpy (Chinese Python by Fred Lin). zhpy's Python 3 rewrite is ~80 lines of core logic using the stdlib `tokenize` module. That is the tightest-possible envelope for this kind of dialect.

## Decision

`apython` is a **source-to-source preprocessor built on `tokenize`**, executed against stock CPython 3.11+. The pipeline is:

```
.apy UTF-8 text
    ↓
pretokenize text pass (outside strings only):
  - reject bidi control codepoints (see ADR 0006)
  - transliterate Arabic digits → ASCII (see ADR 0005)
  - alias Arabic punctuation (see ADR 0005)
    ↓
tokenize.generate_tokens
    ↓
NAME-token rewrite:
  - normalize identifier (see ADR 0004)
  - if normalized name in dialect dictionary → replace
  - else → emit normalized form
    ↓
tokenize.untokenize → Python source string
    ↓
compile(src, original_path, "exec")
    ↓
runpy / exec
```

Two execution surfaces are exposed:
1. `apython file.apy` CLI runner.
2. A `sys.meta_path` import hook that recognizes `.apy` files so Arabic modules can import each other.

Both share the same pipeline. No AST rewriting. No CPython fork in Phase A.

## Consequences

**Positive:**
- Tracks every CPython release automatically. No patch-maintenance cost.
- Core logic is small (target: <150 LOC for `core.py` + `pretokenize.py` + `normalize.py` combined).
- String literals and comments are protected by construction — `tokenize` correctly lexes them before we see any tokens.
- Produces standard Python source as an intermediate form; useful for debugging, reversibility, and pedagogy.
- PEP 3131 means Arabic identifiers pass through natively. No name mangling needed (unlike zhpy2's `zh_ord`/`zh_chr` hack for Python 2).

**Negative:**
- F-string bodies are tokenized as `STRING` tokens in older Python versions; this may limit keyword translation inside f-string expressions. Flagged in Phase A testing, likely a known limitation.
- Error messages from CPython remain English in Phase A. A wrapper layer translates them for display (see future ADR when Phase 3 is specced), but internal introspection (e.g., `sys.exc_info()`) still surfaces English. This is the Nasser "external identifier" problem deferred to Phase B.
- `tokenize.untokenize` does not perfectly round-trip whitespace in all edge cases; line numbers may drift by ±1 in rare inputs. Acceptable risk for Phase A; revisit if it causes learner confusion.

**Neutral:**
- Commits us to stdlib-only for the core. No `pyparsing`, `parso`, `lark`, or similar.

## Alternatives considered

**AST rewriting (via `ast.NodeTransformer`).** Rejected. By the time Python builds an AST, `if` is already an `If` node — there is nothing to rename. AST is the correct layer for adding *new* syntax (decorators, custom statements) but not for translating keywords. We may use AST rewriting in Phase B for library aliasing hooks; it is not wrong, just wrong for this job.

**`pyparsing` or `lark` grammar (zhpy2 pattern).** Rejected. zhpy2 uses `pyparsing` with ~1,200 LOC; zhpy3 replaces it with `tokenize` at ~80 LOC. No feature advantage for the new code, substantially more surface area, external dependency, slower.

**CPython fork in Phase A.** Rejected as premature. Forking means every CPython release requires a rebase. Worthwhile later for localized error messages (Phase B, Layer 7); disastrous now when every byte of effort should ship the learning dialect.

**Runtime monkey-patching of `builtins`.** Rejected. Would rename functions like `print`→`اطبع` at runtime, leaving the source-file level unchanged. Destroys the "write Arabic code" goal and breaks introspection.

**Transpile to `.py` files on disk, check those in.** Rejected. The user's source of truth is `.apy`. Disk-persisted transpilation creates drift and confuses version control.

## Implementation notes

- The `pretokenize` pass is necessary because Python's tokenizer rejects Arabic digits and punctuation *before* yielding tokens; we cannot fix those at the token layer. It is a separate concern from the token-level keyword rewrite.
- The pass must track string-literal state (single, double, triple, raw, byte, f-string) to avoid transforming text inside strings. This state machine is small but must be thoroughly tested.
- `tokenize.untokenize` preserves line numbers well enough for tracebacks pointing to the original `.apy` file path via `compile(src, original_path, "exec")`.

## References

- zhpy3 source: https://github.com/gasolin/zhpy/tree/master/zhpy3
- PEP 3131 (non-ASCII identifiers): https://peps.python.org/pep-3131/
- Python `tokenize` module: https://docs.python.org/3/library/tokenize.html
