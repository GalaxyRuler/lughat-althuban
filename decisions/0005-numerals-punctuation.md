# 0005 — Arabic numerals and punctuation in source

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

Python's tokenizer accepts ASCII digits `0-9` and ASCII punctuation only. Arabic writers commonly use:

- **Arabic-Indic digits** `٠١٢٣٤٥٦٧٨٩` (U+0660–U+0669), used in most Arabic-script contexts.
- **Eastern Arabic-Indic digits** `۰۱۲۳۴۵۶۷۸۹` (U+06F0–U+06F9), used in Persian, Urdu, Pashto.
- **Arabic comma** `،` (U+060C).
- **Arabic semicolon** `؛` (U+061B).
- **Arabic question mark** `؟` (U+061F).

A learner writing `x = ٥` or `نتائج = [١، ٢، ٣]` is writing natural Arabic. Python rejects both. The choice is whether to accept them as syntax.

Note: Python's `int()` and related numeric-coercion functions already accept Arabic-Indic digits at *runtime* (any Unicode codepoint with `Decimal` numeric property). The restriction is at the tokenizer level for *literals*.

## Decision

**Accept Arabic-Indic and Eastern Arabic-Indic digits as numeric literals, and accept Arabic comma/semicolon/question mark as syntactic punctuation.** Translation happens at the pretokenize stage, before Python's tokenizer sees the source.

Specifically:

| Input | Translated to | Scope |
|---|---|---|
| U+0660–U+0669 (٠–٩) | U+0030–U+0039 (0–9) | outside string literals |
| U+06F0–U+06F9 (۰–۹) | U+0030–U+0039 (0–9) | outside string literals |
| U+060C (،) | U+002C (,) | outside string literals |
| U+061B (؛) | U+003B (;) | outside string literals |
| U+061F (؟) | U+003F (?) | outside string literals |

Inside string literals, these characters are preserved unchanged. A program can still write `"٢١"` as string data and it remains `"٢١"`; only digit literals in expressions are transliterated.

Arabic parentheses and brackets do not exist as separate codepoints — `(`, `)`, `[`, `]`, `{`, `}` are the same codepoints in both scripts. However, bidi rendering may visually flip them when adjacent to Arabic text. That is a rendering issue, not a syntax issue; addressed in editor tooling rather than here.

## Consequences

**Positive:**
- Natural Arabic writing patterns work as expected.
- Zero cost for users who prefer ASCII digits; the transformation is idempotent.
- Covers Persian and Urdu users of the same script at no extra cost.

**Negative:**
- `?` has no Python syntactic meaning, so accepting `؟` is symbolic-only. Left in for consistency with comma and semicolon, and to leave room for future walrus-like operators or type-annotation syntax. Can be removed if problematic.
- Mixing Arabic-Indic and ASCII digits in the same literal is ambiguous: `x = ١2` could mean "12". We reject such mixed literals at the pretokenize stage with a clear `SyntaxError`.

**Neutral:**
- The pretokenize stage now has three responsibilities (digits, punctuation, bidi rejection per ADR 0006). Keeping them in one module is correct; they share the string-literal state machine.

## Alternatives considered

**Only Arabic-Indic, not Eastern Arabic-Indic.** Rejected. Excludes Persian/Urdu learners for no technical benefit. Both fold to the same ASCII targets.

**Accept Arabic punctuation everywhere, including inside strings.** Rejected. String contents should be preserved as-written. A learner storing `"١٢٣"` as part of a display string must get those characters back exactly.

**Treat Arabic digits as a feature flag (opt-in).** Rejected. The whole point of the dialect is that Arabic input works; gating digits behind a flag contradicts that.

**Reject mixed-digit literals silently by using the first digit's system.** Rejected. Silent ambiguity is worse than a loud error.

## Implementation notes

- `pretokenize.py` performs these substitutions during its string-aware walk.
- The substitution is a simple `str.translate()` call with a precomputed translation table, applied only to runs of non-string-literal text.
- Test fixtures must include: Arabic digit in expression, Arabic digit inside f-string format spec (is the format spec "inside" or "outside" a string? — it's inside), Arabic digit inside triple-quoted string, Arabic comma in function argument list, Arabic comma inside string.
- The `#%` stdlib `%` formatter and `.format()` do not need special handling; they operate on runtime strings, which are preserved.

## References

- Unicode chart for Arabic-Indic Digits: https://unicode.org/charts/PDF/U0600.pdf
- Unicode chart for Extended Arabic-Indic Digits: https://unicode.org/charts/PDF/U06F0.pdf
