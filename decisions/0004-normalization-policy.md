# 0004 — Identifier normalization policy

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

Arabic orthography has several sources of legitimate variation that English identifiers don't face:

1. **Harakat (short-vowel diacritics)**: `كَتَبَ` and `كتب` are the same word semantically. Python's NFKC preserves the distinction.
2. **Tatweel (U+0640, kashida)**: a stretching glyph inserted for calligraphy. `مـرحـبا` and `مرحبا` are the same word.
3. **Hamza variants**: `أ` (U+0623), `إ` (U+0625), `آ` (U+0622), `ا` (U+0627) are orthographically distinct but frequently conflated by writers. Native speakers routinely misspell hamza placement.
4. **Alef maksura vs ya**: `ى` (U+0649) vs `ي` (U+064A). Commonly confused at word endings.
5. **Ta marbuta vs ha**: `ة` (U+0629) vs `ه` (U+0647). Commonly confused at word endings.

Python's tokenizer applies NFKC to identifiers (per PEP 3131). NFKC handles compatibility composition (presentation forms FExx → base letters) and precomposed/decomposed equivalence, but does **not** fold any of the five variations above. Under stock Python, `مرحبا` and `مَرحبا` are different identifiers.

For a learning dialect, treating them as different is hostile — a learner who typed harakat once by accident would then be unable to reference their variable. For production code, deliberate distinction may be wanted in rare cases (e.g., Quranic or scholarly text processing).

## Decision

**Apply an Arabic-aware normalization pass to every `NAME` token before dictionary lookup or identifier emission.** The normalization, in order:

1. NFKC (matches stock Python).
2. Strip tatweel U+0640.
3. Strip harakat in ranges U+064B–U+065F and U+0670 (superscript alef).
4. Fold hamza variants: أ إ آ → ا.
5. Fold alef maksura: ى → ي (only at word-final position).
6. Fold ta marbuta: ة → ه (only at word-final position).

**This normalization is the default.** A file can opt out via a magic comment on the first two lines:

```python
# apython: strict
```

Or via CLI flag `apython --strict file.apy`. In strict mode, only step 1 (NFKC) is applied, matching stock Python identifier behavior.

The normalization is applied **symmetrically** to both the source token and the dictionary keys. This means dictionary entries are stored in already-normalized form; there is no way for a dictionary entry to rely on e.g. a harakat.

## Consequences

**Positive:**
- Learners who typo hamza placement still get working code.
- Identifier matching becomes intuitive: if it looks the same, it is the same.
- Strict mode is available for users who need the distinction.

**Negative:**
- Folding `ة`→`ه` at word-final position is controversial. The two letters are phonetically distinct (ta vs ha) in careful pronunciation and can distinguish words (`مرأة` vs `مره` are both real words). We accept the risk because confusions are more common than deliberate distinctions among learners.
- The normalizer is ~100 LOC of careful Unicode handling. Small but must be thoroughly tested.
- The "word-final" conditions in steps 5 and 6 require looking at token context (is this letter at the end of a token?). This is a per-token operation, not a per-character one; the normalizer API must reflect this.

**Neutral:**
- This normalization is more aggressive than typical Arabic NLP normalizers, which often leave ة and ه distinct. We document this explicitly in user docs.

## Alternatives considered

**NFKC only (Python default).** Rejected. Fails the learner-friendly goal that motivates Phase A.

**Aggressive normalization by default, no opt-out.** Rejected. Forecloses legitimate use cases (Quranic text, scholarly editions) we want to support in Phase B.

**Strip harakat and tatweel only, no hamza/maksura/ta-marbuta folding.** Rejected as insufficient. The hamza-misplacement issue is specifically what trips up learners most often.

**Make normalization configurable per-identifier (e.g., a pragma that says "treat the next identifier strictly").** Rejected as too fine-grained. File-level strict mode covers the use case.

## Implementation notes

- The normalizer is `arabicpython/normalize.py`, public function `normalize_identifier(s: str, *, strict: bool = False) -> str`.
- The same function is used at three places:
  1. When building the dialect dictionary at load time (every key is normalized once).
  2. When tokenizing source (every `NAME` token is normalized before lookup).
  3. When reverse-translating tracebacks back to Arabic (Phase 3), to ensure round-trip equivalence.
- Tests must cover the full truth table of folding combinations, especially position-dependent folds.
- Unicode ranges to know: harakat `\u064B-\u065F`, tatweel `\u0640`, hamza variants `\u0622\u0623\u0625`, alef `\u0627`, alef maksura `\u0649`, ya `\u064A`, ta marbuta `\u0629`, ha `\u0647`, superscript alef `\u0670`.

## References

- PEP 3131, section on normalization: https://peps.python.org/pep-3131/
- Unicode Standard Annex #15 (normalization forms): https://www.unicode.org/reports/tr15/
- QCRI Arabic Normalizer (common NLP patterns): https://alt.qcri.org/tools/arabic-normalizer/
