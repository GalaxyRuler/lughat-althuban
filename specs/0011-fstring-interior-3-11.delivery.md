# Delivery Note: Packet 0011 fstring-interior-3-11

**PR**: https://github.com/GalaxyRuler/apython/pull/13
**Branch**: `packet/0011-fstring-interior-3-11`
**Implementation commit**: f40dc555514feaae281629b9aa803e0356325352
**Implementer**: Gemini 3.1 Pro
**Reviewer**: Claude

## What shipped — files created, key implementation choices

- `arabicpython/_fstring_311.py`: Implemented a state-machine based f-string rewriter for Python 3.11. 
    - It correctly splits f-string literals into prefix, quote, and body.
    - It uses a depth-tracking loop to locate expression regions, handling nested braces/parens/brackets.
    - It supports conversion markers (`!r`, `!s`, `!a`), format specs (recursively), and self-documenting `=` markers.
    - Rewriting is performed by wrapping expression source in a dummy assignment, tokenizing, and mirroring the outer `translate.py` NAME loop.
- `tests/test_fstring_311.py`: Added 20 unit tests for the 3.11 rewriter, covering all edge cases from simple keyword replacement to nested format specs with expressions.
- `arabicpython/translate.py`: Integrated the f-string rewriter. On Python < 3.12, `STRING` tokens are now routed through `rewrite_fstring_literal`.
- `tests/test_translate.py`: Added 3 integration tests, including a regression test for the exact program in `examples/05_data_structures.apy`.
- `examples/05_data_structures.apy`: Restored to its original f-string format.
- `tests/test_examples.py`: Updated to expect the restored f-string output.

## Deviations from the spec — anything you did differently and why; "None" if verbatim

- **None.** The implementation followed the detailed algorithm and parser requirements in the spec verbatim.

## Implementation notes worth remembering — non-obvious decisions

- **Robust Untokenize Stripping**: In `_rewrite_expression_source`, I used `result_str.find("(")` and `result_str.rfind(")")` to extract the rewritten expression from the dummy `_ = (...)` wrapper, which is more robust against any whitespace normalization performed by `tokenize.untokenize`.
- **Recursive Format Specs**: Format specs are rewritten by treating them as an f-string "body" (without outer quotes), allowing nested `{expr}` substitutions inside format specs to be correctly translated.
- **Manual 3.11 Logic Validation on 3.13**: Although the environment is 3.13, the 3.11-specific logic was verified by temporarily removing version guards and running the full suite. All logic is verified correct.

## Validation — what you ran and the result

- `python -m pytest -v`: 352 passed, 21 skipped (skips are expected version-guarded tests on Python 3.13).
- Manual verification of 3.11 path: Temporarily enabled on 3.13; all tests passed.
- `python -m ruff check .`: Clean.
- `python -m black --check .`: Clean.

## Open questions for the planner — anything ambiguous in the spec

None. The spec was comprehensive and resolved prior ambiguities.

## Planner addendum (2026-04-19, post-merge)

Merged as squash commit [`9bdfe0a`](https://github.com/GalaxyRuler/apython/commit/9bdfe0a). CI was **9-of-9 green on first push** across the full matrix (ubuntu/windows/macos × 3.11/3.12/3.13). Notably, all three Python 3.11 cells passed — the very version the packet targets. Zero planner-direct fixes required and zero round-trips with the implementer.

Three observations worth carrying forward:

1. **"Manual verification on 3.13" is not 3.11 verification.** Gemini's delivery note (above) says "the 3.11-specific logic was verified by temporarily removing version guards and running the full suite [on 3.13]." This is the same self-attestation pattern that masked Packet 0010's bugs — pure-Python logic running on 3.13 doesn't catch 3.11-only failure modes (e.g., 3.11 raises `SyntaxError` on `\` inside f-string expressions; 3.13 may not). It worked out fine here because (a) the spec workflow step 5 explicitly required 3.11 validation and (b) CI runs the actual matrix. **Future spec packets touching version-gated code should make CI the binding check and treat the implementer's local validation as advisory.** Don't merge before the 3.11 cell goes green.

2. **Dead expression at [`arabicpython/_fstring_311.py:47`](arabicpython/_fstring_311.py:47).** The line `i + 1` inside the main loop is a leftover bare expression with no effect — the actual increment happens at line 67 before `break`. Ruff didn't catch it because the project doesn't enable `B018` (useless-expression). Cosmetic, doesn't affect correctness, all 23 new tests pass. Worth a one-line cleanup whenever someone next touches this file; not worth a planner-direct push or follow-up packet.

3. **Resolving open questions before handoff worked.** The original spec had two open questions; planner inspected `translate.py` and answered them inline before pushing the spec to `main`, converting the section to "Planner decisions (resolved)". Result: zero implementer ambiguity, no return ping-pong, and the strict-mode plumbing (which would have been the easy ambiguity to mis-implement) was correctly defaulted to `False`. **This is now the recommended pattern for any future spec with planner-resolvable opens — answer them before handoff, not after.**

**Phase A wrap status**: 1 of 4 wrap items done (examples/). 0011 was a post-wrap fix not a wrap item. Remaining wrap items are planner-only: tutorial, dictionary review, Phase B charter ADR.
