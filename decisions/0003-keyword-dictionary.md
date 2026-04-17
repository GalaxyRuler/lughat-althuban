# 0003 — Keyword dictionary governance

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

The dialect maps Arabic words to Python keywords, built-ins, and exception names. For most Python symbols, multiple Arabic translations are equally defensible. Examples:

| English | Candidates |
|---|---|
| `if` / `else` | إذا / وإلا — لو / وإلا — اذا / والا |
| `def` | دالة — عرف — تابع |
| `class` | صنف — فئة |
| `return` | ارجع — أرجع — اعد |
| `True` / `False` / `None` | صحيح / خطأ / لاشيء — حق / باطل / عدم |
| `for` | لكل — من_أجل |
| `while` | طالما — بينما |
| `print` | اطبع — قل (Qalb) |
| `import` | استورد — ادرج — جلب |

No convention is canonical across existing Arabic programming projects (Qalb, Kalimat, Phoenix, Hedy). If we defer the choice we get either:
- Fragmentation (every user picks their own), which splits the ecosystem before it exists, OR
- Paralysis (we never ship).

The governance question is therefore: how do we choose, how do we lock in, and how do we evolve the dictionary over time without fragmenting users.

## Decision

1. **The dictionary is versioned data, separate from code.** It lives at `dictionaries/ar-v1.md` as the human-readable source of truth, and at `arabicpython/dialects/ar.py` as the machine-loadable form. The two are kept in sync by a generation script (implementation detail, part of Packet 1.1).

2. **One canonical Arabic word per Python symbol in v1.** No built-in aliases. A learner who writes `اذا` instead of `إذا` gets a `NameError` or a normalization-mediated match (see ADR 0004), not a silent acceptance of both forms. This is a deliberate choice for dictionary clarity; normalization handles orthographic variation separately.

3. **Selection criteria, in priority order:**
   1. **Hedy's Arabic translation**, where one exists and is unambiguous. Hedy is the only production-quality precedent with a real Arabic learner user base; inheriting its choices maximizes continuity for learners who graduate from Hedy to `apython`.
   2. **Modern Standard Arabic** over regional dialects. Pedagogically neutral; defers dialect choice to a future post-v1 extension if desired.
   3. **Shortest defensible translation** when multiple MSA options are equal. `اطبع` (5 chars) over `أطبع على الشاشة` (15 chars).
   4. **Avoid homographs** with common identifiers a learner would write. `من` means "from" but is also a common word; prefer `من_مكتبة` if collision is likely. Actual collision risk is assessed per symbol during Packet 1.1.

4. **Governance: dictionary changes require an ADR.** The dictionary is treated like language grammar — small shifts have ecosystem-wide consequences. Proposed changes go through a numbered ADR that supersedes this one or a subsequent dictionary ADR. Additions (new symbols for Python features we did not originally cover, like `match`/`case`) do not require an ADR; removals and renames do.

5. **Versioning: a dictionary has a version independent of the package.** The package is `apython` v0.1.0; the dictionary it loads is `ar-v1.0`. A file can declare the dictionary version it expects via a magic comment: `# apython: dict=ar-v1`. If missing, the current dictionary is used. This lets us evolve the dictionary post-v1 without breaking existing code.

## Consequences

**Positive:**
- Learners see consistent translations across files, tutorials, error messages, and documentation.
- The dictionary is small enough (~200 entries) for one person to curate and one reviewer to audit.
- Versioning lets us fix mistakes in v2 without abandoning v1 users.

**Negative:**
- Community contributors may disagree with specific choices. Mitigation: the ADR process gives them a formal way to propose changes, and alternates are documented in `dictionaries/ar-v1.md` for transparency.
- One-canonical-per-symbol may feel rigid to bilingual developers who'd rather mix. Normalization (ADR 0004) absorbs orthographic variation; this decision draws the line at semantic variation.

**Neutral:**
- Post-v1 we may introduce a `strict=false` dictionary loader that accepts documented alternates. This is a Phase B concern, not a Phase A concern.

## Alternatives considered

**Accept multiple synonyms from day one.** Rejected. Learning materials would have to pick one anyway; having multiple on the language side just pushes the choice downstream. Also makes tooling (autocomplete, error messages suggesting "did you mean") noisier.

**Defer the choice to per-project config files.** Rejected. Would fragment the ecosystem. An `apython` file should be readable by any `apython` reader without configuration.

**Auto-generate translations via LLM.** Rejected for v1. LLM translations are non-deterministic and sometimes wrong on connotation. May be useful as a proposal tool for community contributors, but the canonical dictionary must be human-curated.

**Fork Hedy's translations wholesale.** Rejected as insufficient. Hedy covers fewer keywords than Python; we need translations for symbols Hedy doesn't use (e.g., `yield`, `async`, `nonlocal`, `global`). Hedy is a starting point, not a finished table.

## Implementation notes

- Packet 1.1 (my work, not Codex's) produces `dictionaries/ar-v1.md` with every entry, its selected translation, alternates considered, and rationale for the choice.
- Packet 1.2 (Codex's work) reads `ar-v1.md` into `arabicpython/dialects/ar.py` and validates: no duplicate keys, no duplicate values, every Python keyword covered.
- The dictionary must include exception class names (`ValueError` → `خطأ_قيمة`), common built-in methods on str/list/dict (`.append` → `.أضف`), and a small set of module-level `sys`/`os` functions that appear in beginner programs.

## References

- Hedy's Arabic translation: https://hedy.org/ (crowdsourced via Weblate)
- Qalb keyword list: https://nas.sr/%D9%82%D9%84%D8%A8/
- Kalimat: https://github.com/baronleonardo/kalimat
