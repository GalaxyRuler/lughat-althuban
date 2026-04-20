# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Nothing yet. Phase B is chartered (ADR 0008) but not started; first packet
B-001 (alias-runtime + `requests`) is gated on funding-unlock conditions
documented in the charter.

## [0.1.1] — 2026-04-20 — Dictionary rendering + coverage pass

Post-release doc and dictionary improvements. No code changes.

### Changed — dictionaries

- **ar-v1.md rendering convention**: all canonical entries now shown in natural
  visible (pre-normalizer) form. The ADR 0004 normalizer folds on lookup so
  runtime behaviour is unchanged; this is documentation-only. 45 entries
  corrected — primarily `خطا_*` → `خطأ_*` exception names, `اي` → `أي`,
  `الاكبر` → `الأكبر`, `يبدا_بـ` → `يبدأ_بـ`, and similar hamza restorations.

### Added — dictionaries (Category C, no ADR required per ADR 0003)

- `breakpoint` → `نقطة_توقف` (built-in function)
- 7 string methods: `.title عنوان`, `.capitalize كبر_الأول`,
  `.swapcase عكس_الحالة`, `.zfill مل_بأصفار`, `.center توسط`,
  `.ljust ضبط_يسار`, `.rjust ضبط_يمين`
- 5 set methods: `.add ضم`, `.discard أسقط`, `.union اتحاد`,
  `.intersection تقاطع`, `.difference فرق`
  (`.remove` / `.clear` / `.copy` already worked via existing mappings)
- 1 dict method: `.popitem → انتزع_زوج`
  (`.pop` was already covered via the shared `انتزع → pop` mapping)
- `aiter` / `anext` documented as deferred to Phase B in Known omissions

**Updated counts**: 173 → 187 entries (names 144→145, attributes 29→42).

### Added — tests

- 15 new tests in `test_dialect.py` covering all v1.1 additions.
- Count assertions updated to ≥ 187 total / ≥ 42 attributes.
- **Test suite: 351 passing, 21 intentionally skipped.**

## [0.1.0] — 2026-04-19 — Phase A complete

First feature-complete release of the Arabic-keyword Python dialect. Source-to-source preprocessor on top of CPython 3.11+; no fork.

### Added — language pipeline

- **Pretokenize layer** (`arabicpython/pretokenize.py`): Arabic-Indic + Eastern-Arabic digit folding, Arabic punctuation aliasing (`،`/`؛`/`؟`), 12-codepoint bidi-control rejection per UAX #9.
- **Identifier normalization** (`arabicpython/normalize.py`): hamza folding, ta-marbuta→ha, harakat stripping, tatweel removal. Idempotent; `قيمه` and `قيمة` resolve to the same name.
- **Dialect loader** (`arabicpython/dialect.py`): parses `dictionaries/ar-v1.md` directly at load time into frozen name/attribute mappings. 173 entries at Phase A ship (expanded to 187 in v0.1.1).
- **Translate layer** (`arabicpython/translate.py`): tokenize → name-rewrite → untokenize. Includes a Python-3.11-specific f-string-interior rewriter (Packet 0011) that's bypassed on 3.12+ where PEP 701 changed f-string tokenization.
- **`.apy` import hook** (`arabicpython/importer.py`): `sys.meta_path` finder so `.apy` files import each other and `.py` modules transparently in both directions.
- **Interactive REPL** (`arabicpython/repl.py`): multi-line Arabic input with continuation prompts; readline-aware where available.
- **Arabic tracebacks** (`arabicpython/excepthook.py`): 38 exception types and ~30 common interpreter messages translated; unmapped messages pass through.
- **CLI** (`arabicpython/cli.py`): four entry surfaces (file, `-c`, stdin, REPL) mirroring `python`. UTF-8 stdout/stderr forced on Windows.

### Added — content

- **Dictionaries**: `ar-v1.md` (canonical word list, locked at v1.0) and `exceptions-ar-v1.md` (exception subclass hierarchy + interpreter-message translations).
- **Examples**: 7 progressive `.apy` programs covering hello, arithmetic, control flow, functions, data structures, classes, and cross-module imports.
- **Tutorial**: `docs/getting-started-ar.md` covering the eight ADR-0007 ship topics.

### Added — design (ADRs)

- **0001** Architecture: source-to-source preprocessor.
- **0002** File extension: `.apy`.
- **0003** Keyword dictionary governance.
- **0004** Identifier normalization policy.
- **0005** Arabic numerals and punctuation in source.
- **0006** Bidi control character policy *(superseded by 0009 — reject-list portion only)*.
- **0007** Scope: learning dialect first, production replacement second.
- **0008** Phase B charter (freeze ar-v1, module-proxy meta-path finder, B-001 first packet, funding-gate unlocks, 24-month sunset default).
- **0009** Bidi control marks extension (12 codepoints per UAX #9 §7).

### Added — process

- 11 spec packets (0001–0011) tracked in `specs/INDEX.md`, each with paired delivery notes.
- CI matrix: ubuntu / macos / windows × Python 3.11 / 3.12 / 3.13.
- Test suite: 336 passing, 21 intentionally skipped (3.11-specific paths on 3.12+; readline-unavailable on Windows).

### Known limitations (deferred fixups)

- `from . import x` inside `__init__.apy` does not translate; workaround `import pkg.sub as sub`.
- Cross-language attribute access from `.py` to `.apy` requires the ADR-0004-normalized form (e.g., `module.قيمه`, not `module.قيمة`).
- No end-to-end async/await program coverage; keywords translate but real async programs are not exercised by the suite.

## Phase 0 — Design decisions

Initial scaffolding period (pre-Phase A):

- Project scaffolding: README, LICENSE (Apache-2.0), `pyproject.toml`, CI workflow.
- ADRs 0001–0007 establishing architecture, file extension, dictionary governance, normalization policy, numerals/punctuation, bidi policy, and scope.
- Spec packet template for planner→implementer handoff.
