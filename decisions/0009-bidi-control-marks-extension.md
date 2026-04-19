# 0009 — Bidi control marks extension

**Status**: accepted
**Date**: 2026-04-19
**Deciders**: project planner
**Supersedes**: ADR 0006 (reject-list portion only; rationale and in-string/in-comment policy carry forward unchanged)

## Context

ADR 0006 rejected nine bidi formatting characters outside string literals — the embeddings/overrides U+202A–U+202E (LRE, RLE, PDF, LRO, RLO) and the isolates U+2066–U+2069 (LRI, RLI, FSI, PDI). On a re-read of UAX #9 (Unicode Bidirectional Algorithm, v17.0.0) that reject list is materially incomplete. UAX #9 §7's implementation guidance for source-code tokenizers calls out three additional zero-width directional marks that affect bidi rendering and are exactly the kind of invisible characters Trojan-Source-class attacks exploit:

| Codepoint | Name | Abbr. | What it does |
|---|---|---|---|
| U+200E | LEFT-TO-RIGHT MARK | LRM | Implicit directional mark; gives surrounding text an L type for the purposes of the bidi algorithm |
| U+200F | RIGHT-TO-LEFT MARK | RLM | Implicit directional mark; gives surrounding text an R type |
| U+061C | ARABIC LETTER MARK | ALM | Implicit directional mark; gives surrounding text an R type, specifically encoded for Arabic context (added in Unicode 6.3) |

Unlike LRE/RLE/LRO/RLO/LRI/RLI/FSI, these three are not "initiators" — they don't push a stack frame and they aren't paired with a closer. That non-initiator nature is exactly why they're easy to overlook when surveying the bidi attack surface. They still affect the resolved bidi level of adjacent characters, and they are still zero-width and invisible.

For an Arabic-keyword dialect, ALM is the most concerning of the three. An attacker can embed ALM inside an Arabic identifier where it is invisible to a code reviewer but parsed as part of the name. Two visually-identical `طلبات` tokens — one bare, one with an embedded ALM — normalize to different identifiers and resolve to different objects. This is the same attack class the original ADR 0006 was designed to prevent; ADR 0006 just stopped one character short.

PEP 672 and UTS #36 (Unicode Security Considerations) both discuss invisible characters in identifiers as a distinct attack class from formatting initiators. UAX #9's own §7 puts the three marks first in its lexer detection list.

## Decision

**Extend the bidi-rejection set in `pretokenize.py` from 9 codepoints to 12.** The new set is:

| Codepoint | Name |
|---|---|
| U+061C | ARABIC LETTER MARK (ALM) — *new in this ADR* |
| U+200E | LEFT-TO-RIGHT MARK (LRM) — *new in this ADR* |
| U+200F | RIGHT-TO-LEFT MARK (RLM) — *new in this ADR* |
| U+202A | LEFT-TO-RIGHT EMBEDDING (LRE) |
| U+202B | RIGHT-TO-LEFT EMBEDDING (RLE) |
| U+202C | POP DIRECTIONAL FORMATTING (PDF) |
| U+202D | LEFT-TO-RIGHT OVERRIDE (LRO) |
| U+202E | RIGHT-TO-LEFT OVERRIDE (RLO) |
| U+2066 | LEFT-TO-RIGHT ISOLATE (LRI) |
| U+2067 | RIGHT-TO-LEFT ISOLATE (RLI) |
| U+2068 | FIRST STRONG ISOLATE (FSI) |
| U+2069 | POP DIRECTIONAL ISOLATE (PDI) |

Everything else from ADR 0006 carries forward unchanged:

- **Inside string literals**: all 12 pass through unchanged. Strings are data; users can embed any Unicode they need.
- **Inside comments**: all 12 are rejected. Comments are read by humans during review, and bidi-in-comments is a primary Trojan Source mechanism.
- **Error message format**: same `SyntaxError: bidi control character U+XXXX (NAME) is not allowed outside string literals at line L, column C. See https://trojansource.codes for why.`
- **Rationale, alternatives, security posture**: unchanged.

## Consequences

**Positive:**
- Closes a real gap in the dialect's bidi defenses, particularly the ALM-in-Arabic-identifier attack which is dialect-specific and not addressed by ADR 0006 as written.
- Brings the reject-list into alignment with UAX #9 §7's source-code tokenizer guidance and with PEP 672/UTS #36 invisible-character recommendations.
- Mechanical change: three characters added to one frozenset; existing test pattern extends straightforwardly with three new rejection tests.

**Negative:**
- Marginally more restrictive than ADR 0006. Any pre-existing `.apy` file that contained LRM, RLM, or ALM outside a string literal will now be rejected. Search of the current repo finds zero such files; risk is theoretical for now and worth taking even if a real file surfaces later (the file is wrong; reject-and-fix is the right outcome).
- Three additional codepoints to remember in error-message documentation. Mitigation: the error message names the specific character via `unicodedata.name`, so users get the name without consulting a table.

**Neutral:**
- The reject-list could in principle grow further (e.g., U+180E MONGOLIAN VOWEL SEPARATOR was once a default-ignorable that affected layout; later reclassified). Drawing the line at "characters with Bidi_Class formatting effect per UAX #9" is the principled boundary; we don't preemptively add characters with merely *aesthetic* invisibility (zero-width joiners, variation selectors, etc.) because rejecting those would break legitimate Arabic text shaping.

## Alternatives considered

**Leave ADR 0006 as is.** Rejected. The gap is real, the fix is three characters, and the dialect's user base is exactly the audience most exposed to ALM-style attacks (people writing Arabic identifiers).

**Add only ALM (the dialect-specific one), defer LRM/RLM.** Rejected as inconsistent. UAX #9 treats all three as the same category of invisible directional mark; rejecting one and not the others would be a defensible position only if LRM/RLM had legitimate non-string uses in `.apy` source. They don't — the language has no LTR-vs-RTL display question to settle outside string data, because the source itself is processed in logical order by the tokenizer regardless of how it's rendered.

**Reject all default-ignorable characters wholesale.** Rejected as too broad. Default-ignorables include zero-width joiner (U+200D) and zero-width non-joiner (U+200C), which are required for correct rendering of certain Arabic letter combinations. A blanket ban would break the very text the dialect is meant to support.

**Allow these three in identifiers, normalize them away.** Rejected. Normalization-based defense (silently stripping invisibles) trains users to write code where what they see and what runs are different things. Hard rejection with a clear error is the safer pedagogical default and matches ADR 0006's existing posture.

**Defer to a future "ADR 0010 — full Unicode security policy" consolidating UAX #9, UTS #36, UTS #39, and UTS #55.** Rejected as letting-the-perfect-be-the-enemy. Such an ADR is worth writing eventually (the Phase B charter implicitly assumes it), but a three-codepoint extension that closes a real gap shouldn't wait on a much larger consolidation effort.

## Implementation notes

- The change touches one frozenset in `arabicpython/pretokenize.py` and adds five tests in `tests/test_pretokenize.py` (three rejection tests for ALM/LRM/RLM, one in-string pass-through test for ALM, and the existing test count comment is updated from `(9)` to `(12)`).
- ADR 0006's "Status" line is updated to `superseded by 0009` per the convention in `decisions/README.md`. The body of 0006 is preserved verbatim; readers needing the rationale go there.
- No spec packet is required — this is a planner-direct mechanical change of the kind ADR 0006's "Implementation notes" already anticipated ("the rejection happens in `pretokenize.py` as part of its string-aware walk").

## References

- UAX #9: Unicode Bidirectional Algorithm — https://www.unicode.org/reports/tr9/ (v17.0.0; §7 source-code tokenizer guidance is the direct basis for this ADR)
- ADR 0006 — Bidi control character policy (the ADR this one extends)
- PEP 672 — Unicode Security Considerations for Python: https://peps.python.org/pep-0672/
- UTS #36 — Unicode Security Considerations: https://www.unicode.org/reports/tr36/
- UTS #55 — Unicode Source Code Handling: https://www.unicode.org/reports/tr55/
- Trojan Source paper: https://trojansource.codes/trojan-source.pdf
- CVE-2021-42574: https://nvd.nist.gov/vuln/detail/CVE-2021-42574
