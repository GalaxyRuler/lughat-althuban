# 0007 — Scope: learning dialect first, production replacement second

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

Ramsey Nasser's critique of Arabic programming languages, articulated most fully in his Deconstruct 2019 talk and his Ajam Media interview, identifies three layers where English embeds itself into any programming language:

1. **Keywords** (`if`, `def`, `class`) — tractable, the layer zhpy addresses.
2. **Local identifiers** — solved by Unicode-aware languages like Python 3 via PEP 3131.
3. **External identifiers** — library names, method names, error messages, documentation. The hard problem.

Nasser's conclusion, based on building Qalb: layer 3 is not just hard, it is **impossible for an individual or small team** to solve because it requires rewriting the ecosystem that surrounds the language, not just the language itself. A production Arabic programming language is a multi-year initiative requiring funding, community, and a captive audience.

At the same time, Hedy's deployment across 47 languages including Arabic demonstrates that **layer 1 alone is genuinely valuable for education**, even when layers 2 and 3 remain English. Children learning to program benefit enormously from native-language keywords; whether their adult selves later work in English-language libraries is irrelevant to the learning moment.

These two positions are both correct. The question is which one we build.

## Decision

**Build both, in strict sequence: Phase A (learning dialect) first, Phase B (production replacement) second.** The two phases share an architecture (ADR 0001) so that Phase B is additive, not a rebuild. Phase A must ship and be usable by real learners before Phase B work begins.

### Phase A — Learning Dialect

**Goal**: A learner can write, run, debug, and import complete small programs in Arabic on any platform that runs CPython 3.11+.

**Scope included:**
- `.apy` file extension and its tokenize-based transpiler.
- Arabic keyword dictionary v1 (`dictionaries/ar-v1.md`).
- Identifier normalization (ADR 0004).
- Arabic digits and punctuation in source (ADR 0005).
- Bidi rejection (ADR 0006).
- `apython` CLI runner.
- `sys.meta_path` import hook so `.apy` files import each other.
- Interactive REPL with Arabic prompts and TAB completion.
- Translated tracebacks for the ~50 most common exception message templates.
- Example programs, tutorial documentation, pytest suite covering the above.
- pip-installable from the private repo (`pip install git+https://github.com/GalaxyRuler/apython.git`).

**Scope explicitly excluded from Phase A:**
- Library aliasing (learner writes `import requests`, not `استورد طلبات`).
- Stdlib symbol aliasing (`print` is translated; `os.path.join` is not).
- Translated docstrings for stdlib.
- CPython patches of any kind.
- LSP server.
- IDE/editor extension beyond a minimal syntax-highlight grammar.
- F-string interior translation.
- `async`/`await`/`match`/`case` keyword coverage (v1 dictionary; revisit for v1.1).
- Reverse translation (Python → Arabic).
- Distribution bundle (Anaconda-style installer).

**Ship criteria:**
- All tests green on Linux, Windows, macOS across Python 3.11/3.12/3.13.
- Three end-to-end example programs run from a fresh install.
- At least one real learner (not the implementers) has used it for a non-trivial task and provided feedback.
- Tutorial documentation covers: install, hello world, variables, control flow, functions, classes, imports, error reading.

### Phase B — Production Replacement

**Goal**: An Arabic-speaking developer or organization can adopt `apython` as the primary language for production software.

**Scope (in priority order):**
1. Layer 3 aliasing — module proxies, bidirectional name registry, auto-transliteration fallback. Proves the "third-party libraries in Arabic" model.
2. Hand-curated Arabic SDKs for the top 10 libraries: `requests`, `flask`, `fastapi`, `numpy`, `pandas`, `sqlalchemy`, `pytest`, `click`, `pydantic`, `httpx`.
3. Complete stdlib alias layer (~200 modules, ~30,000 symbols).
4. CPython fork with gettext-based Arabic error messages.
5. Tooling parity: `apip`, `apytest`, `apdb`, LSP server, VS Code extension.
6. Translated official Python documentation mirror for Arabic.
7. Distribution bundle: CPython + stdlib-ar + top-50 curated SDKs + tools, single installer.
8. Community: Q&A site, books, university-curriculum partnerships, conference presence.

**Phase B start gates:**
- Phase A ship criteria met.
- At least one committed buyer or sponsor (government education ministry, university, company, or foundation) willing to fund multi-year work.
- Absent a buyer: Phase A remains the project's deliverable; Phase B becomes dormant research.

## Consequences

**Positive:**
- Clear staging prevents scope creep. Every Phase A packet has a bright-line test for "is this Phase A work or Phase B work?" — if it's the latter, it's deferred.
- Architecture built to Phase B standards from day one means no rework.
- Shipping Phase A first produces a real artifact that attracts real feedback, which informs Phase B priorities.
- Honest framing in documentation: we tell users what they're getting. The README makes clear that production use is Phase B, not Phase A.

**Negative:**
- Temptation exists to start Phase B library aliasing "just for one package" as part of Phase A. We resist this. The packet template enforces the discipline.
- Some potential users will evaluate Phase A and walk away because production features aren't there. That's fine; they're not the target audience for Phase A.

**Neutral:**
- The repo is private until Phase A ships. After shipping, we make it public with Phase B as a documented roadmap.

## Alternatives considered

**Build Phase A only, ever.** Rejected. The user explicitly wants a production replacement. Phase A alone is a teaching tool, not an infrastructure play.

**Build Phase B only, skip the teaching tool.** Rejected. Phase B is years of work; skipping Phase A means no users and no feedback for the first two years. Phase A is how we find out what matters in Phase B.

**Build both simultaneously.** Rejected. Two halves of a project compete for attention; neither ships.

**Build Phase A with a small slice of Phase B (e.g., one library aliased) to prove the model.** Accepted as Phase A's final packet (Packet 4.1–4.3 in the plan). We ship one demo of the Phase B model so that we have evidence Phase B is tractable, but the package does not yet depend on it.

## References

- Ramsey Nasser, *A Personal Computer for Children of All Cultures*, Deconstruct 2019: https://www.deconstructconf.com/2019/ramsey-nasser-a-personal-computer-for-children-of-all-cultures
- Ramsey Nasser on Qalb, Ajam Media: https://ajammc.com/2020/06/17/code-ramsey-nasser/
- Hedy project: https://hedy.org/
- Hedy in Arabic case study: https://cs.ou.nl/oursi/OUrsi081-Swidan-Hedy-in-Arabic.pdf
