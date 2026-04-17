# 0006 — Bidi control character policy

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

Unicode defines a set of "bidirectional formatting" control characters that override the normal bidi algorithm's behavior. The relevant ones:

| Codepoint | Name | Effect |
|---|---|---|
| U+202A | LRE — Left-to-Right Embedding | Begin LTR segment |
| U+202B | RLE — Right-to-Left Embedding | Begin RTL segment |
| U+202C | PDF — Pop Directional Formatting | End an LRE/RLE/LRO/RLO |
| U+202D | LRO — Left-to-Right Override | Force LTR regardless of content |
| U+202E | RLO — Right-to-Left Override | Force RTL regardless of content |
| U+2066 | LRI — Left-to-Right Isolate | LTR isolated segment |
| U+2067 | RLI — Right-to-Left Isolate | RTL isolated segment |
| U+2068 | FSI — First Strong Isolate | Auto-detected isolate |
| U+2069 | PDI — Pop Directional Isolate | End an LRI/RLI/FSI |

These are zero-width, invisible characters. They exist to let authors force bidi rendering in edge cases where the default algorithm produces wrong output.

**The problem**: in 2021, the Trojan Source vulnerability (CVE-2021-42574) demonstrated that these characters enable a serious class of attacks against source code. An attacker can embed bidi controls that make source *display* one way in an editor while *executing* a different logical program. This affects every language whose compiler/interpreter ignores bidi controls but whose editors honor them — which is Python, C, C++, Go, Java, Rust, JavaScript, and essentially every mainstream language.

For a language that explicitly mixes RTL (Arabic) and LTR (English-origin symbols, operators, digits) in every line, the risk is elevated. A `.apy` file is a far more plausible target for bidi-based source obfuscation than a `.py` file, because the user already expects mixed directional text.

PEP 672 (Unicode Security Considerations) discusses these issues for Python broadly. CPython 3.12+ issues warnings in some scenarios but does not reject bidi controls.

## Decision

**Reject bidi control codepoints U+202A–U+202E and U+2066–U+2069 outside string literals.** When detected during the pretokenize pass, raise a `SyntaxError` with a message indicating the codepoint, its name, and the line/column of the offense.

Inside string literals, bidi controls are preserved unchanged. This matches Python's behavior and allows legitimate uses (displaying mixed-script text that requires manual bidi hints). Users who need to embed such characters in program data can do so; they cannot do so in code.

## Consequences

**Positive:**
- Eliminates the entire Trojan Source attack surface from the dialect's source files.
- Establishes a security-first default. Given that the dialect's user base includes learners, attack-resistant-by-default is the right posture.
- Forces the project to treat bidi as a first-class concern rather than an afterthought.

**Negative:**
- There are legitimate uses of bidi controls in code layout for RTL authors — specifically, isolating a single-line English identifier inside a mostly-Arabic line to force cleaner rendering. We are rejecting these uses. Mitigation: editor tooling in Phase B should apply bidi isolation *visually* without requiring source-level codepoints.
- The error must be extremely clear. A learner won't know what U+202E is. The error message includes the character name and a link to documentation.

**Neutral:**
- This is more restrictive than Python's default. A `.apy` file that is a valid Python file might still be rejected. That's acceptable — `.apy` is a superset of some Python semantics but a subset of some Python permissions.

## Alternatives considered

**Follow Python's default (allow, maybe warn).** Rejected. Python's default is wrong for any security-sensitive language and especially wrong for a mixed-directionality one. We are explicitly *not* Python here.

**Warn but don't reject.** Rejected. Warnings in code are routinely ignored. The only safe default is hard rejection.

**Reject only the RTL-override characters (U+202D, U+202E) while allowing isolates (U+2066–U+2069).** Rejected as too clever. Isolates can also be misused for obfuscation. The full set is safer.

**Allow in comments.** Rejected. Comments are parsed by humans, and bidi in comments is how Trojan Source attacks hide in review. Comments are *especially* risky, not less.

## Implementation notes

- The rejection happens in `pretokenize.py` as part of its string-aware walk.
- The error message format: `SyntaxError: bidi control character U+202E (RIGHT-TO-LEFT OVERRIDE) is not allowed outside string literals at line L, column C. See https://trojansource.codes for why.`
- Test fixtures must include: each of the 9 codepoints outside strings (should raise), each inside a single-line string (should pass through), each inside a triple-quoted string (should pass through), bidi in a docstring (should pass through).
- The check must also cover bidi controls embedded between an identifier and an operator — a common Trojan Source pattern.

## References

- Trojan Source paper: https://trojansource.codes/trojan-source.pdf
- CVE-2021-42574: https://nvd.nist.gov/vuln/detail/CVE-2021-42574
- PEP 672 (Unicode Security Considerations for Python): https://peps.python.org/pep-0672/
- Unicode Technical Report #36 (Security Considerations): https://www.unicode.org/reports/tr36/
- Unicode Bidirectional Algorithm (UAX #9): https://www.unicode.org/reports/tr9/
