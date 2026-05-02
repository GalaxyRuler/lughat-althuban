# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Phase D D-002 through D-005 delivery:
  - AI aliases for `anthropic`, `openai`, `langchain_core`, `transformers`,
    and `sentence_transformers`, all authored in `lexicon/libraries.toml`.
  - Reverse translator API and CLI command: `arabicpython.reverse` and
    `ثعبان ترجمة-عكسية`.
  - Canonical stdlib import names for D-004, including `نظام`→`os`,
    `نظام_بايثون`→`sys`, `مسار`→`pathlib`, `تعابير`→`re`,
    `ادوات_دوال`→`functools`, `تنميط`→`typing`, `خيوط`→`threading`,
    and `مسار_نظام`→`os.path`.
  - Traceback localization modes: `arabic`, `english`, and `mixed`.

### Changed

- Roadmap and contributor documentation now mark Phase C as complete and
  Phase D as the active roadmap.
- `lexicon/libraries.toml` is now the single authoring source for runtime alias
  TOMLs; generated alias files are marked as generated.
- `lexicon/messages.toml` now owns reusable tool messages and traceback message
  regex/templates; runtime imports generated Python data modules.
- `tools/validate_lexicon.py` now checks generated dictionaries, alias TOMLs,
  docs, messages, and traceback data for drift.
- Old non-conflicting import names such as `نظام_تشغيل`, `مسار_مكتبه`,
  `عشوائيات`, `اختبارات`, `صور`, `جانغو`, and `رسم_مخططات` are preserved as
  compatibility `arabic_aliases`.
- The full optional test environment is covered by `.[all]`; Windows dev
  installs include `pyreadline3` for readline-backed REPL history tests.

### Verification

- Full local suite after installing optional extras:
  `2926 passed, 23 skipped, 1 warning`.
- Remaining skips are Python-version-specific f-string tests or tutorial
  snippets explicitly marked non-runnable.

## [0.4.0] — 2026-05-01

### Added

- Canonical Arabic programming lexicon under `lexicon/`, with validators and
  generated runtime dictionary outputs.
- Arabic glossary, alias index, naming policy, exception policy,
  normalization/bidi guide, troubleshooting guide, educator guide, coverage
  matrix, and release checklist.
- CI checks for lexicon validation and generated-output freshness.

### Changed

- User-facing CLI, formatter, linter, pretokenizer, alias-proxy, kernel, LSP,
  and VS Code extension messages are Arabic-first.
- `ar-v2` dictionary copies are generated from one source and kept in sync.
- Tracebacks use the active `ar-v2` exception names and hide internal CLI
  runner frames.
- Jupyter alias completion loads the shipped alias names correctly.
- Documentation and examples now use shipped aliases such as `بانداس`,
  `نمباي`, and `فلاسك`, plus the `ar-v2` keyword `باسم`.

### Fixed

- Advanced examples `B57`, `B58`, and `B59` now compile under the default
  `ar-v2` dialect.
- Stale references to old repository names, unsupported aliases, and outdated
  exception spellings were removed from Arabic documentation.

### Changed

- FastAPI application GET route decorators use `احصل_مسار` for `FastAPI.get`,
  keeping the existing `طلبات.احصل` entry collision-free while preserving
  generic returned-object `.احصل` attributes for wrapped objects.
- Added `اسماء_بديله`, an Arabic alias module for the internal alias runtime
  helpers used by C-040, including `وكيل_صنف` and `حمل_خريطه`.
- Made alias registration lazy about target imports, so installing Arabic
  aliases no longer imports optional third-party libraries during app startup.
- C-040 keeps the full-stack `.apy` demo Arabic-first by adding optional aliases
  for FastAPI `TestClient` and `mongomock`, plus `ترويسات` for FastAPI request
  and client header objects.

## [0.3.0] — 2026-04-28

First public release on PyPI. Ships the complete Phase A + Phase B feature set.

### Phase A — Core dialect (0.1.x, shipped internally)

- **Arabic keyword transpiler** — tokenize-layer translation of `ar-v1` Arabic keywords to Python equivalents; handles f-strings, nested scopes, type annotations.
- **Import hook** — `.apy` files importable via `import arabicpython` without a separate compilation step.
- **REPL** (`ثعبان`) — interactive Arabic Python shell with translated tracebacks.
- **Translated tracebacks** — `arabicpython.tracebacks` rewrites CPython error messages to Arabic; 100% coverage of 97 real CPython message templates (B-061).
- **Dictionary `ar-v1`** — 200+ keyword/built-in/exception/method entries with normalization; shipped as package data.
- **Dictionary `ar-v1.1`** — adds `async`/`await`/`match` keywords and a second spelling for `متزامن`.
- **CLI** — `ثعبان run FILE.apy`, `ثعبان repl`, `ثعبان check FILE`, `ثعبان راجع` (linter), `ثعبان نسّق` (formatter).
- **pytest plugin** — `pytest11` entry point; `.apy` test files collected and executed transparently.
- **Jupyter kernel** — `arabicpython_kernel` package; install with `python -m arabicpython_kernel.install`.

### Phase B — Standard library & third-party aliases (0.2.x → 0.3.0)

Arabic module names that transparently proxy real modules via `arabicpython.aliases`.

#### stdlib aliases

- **B-030** `مسارات` (os/pathlib/sys), `نظام` (os), `مسار` (pathlib.Path), `وسيطات` (sys)
- **B-031** `مجموعات` (collections), `تكرار` (itertools), `دوال_ترتيب_عالي` (functools)
- **B-032** `تاريخ_ووقت` (datetime), `تقويم` (calendar), `وقت` (time)
- **B-033** `ج_س_ن` (json), `ملفات_csv` (csv), `قاعده_بيانات` (sqlite3)
- **B-034** `تعابير_نمطيه` (re), `نصوص` (textwrap/string)
- **B-035** `رياضيات` (math), `احصاء` (statistics), `عشوائي` (random), `كسور` (fractions), `عشري` (decimal)
- **B-036** `سجلات` (logging)
- **B-037** `غير_متزامن` (asyncio)
- **B-038** `ضغط` (gzip/zipfile), `بريد` (email/smtplib), `تشفير` (hashlib/hmac/secrets), `ترميز` (base64/codecs), `خيوط` (threading/concurrent.futures), `مقابس` (socket), `http_خادم` (http.server), `بيانات_ثنائيه` (struct/io), `اختبارات` (unittest)

#### Third-party aliases

- **B-010** `فلاسك` (flask) — 54 entries
- **B-011** `فاست_أبي_سريعه` (fastapi) — 47 entries
- **B-012** `جانغو` (django) — 41 entries
- **B-013** `ألكيمي` (sqlalchemy) — 49 entries
- **B-014** `طلبات` (requests) — 36 entries
- **B-015** `اختبار_عربي` / pytest plugin aliases
- **B-016** `مصفوفات` (numpy) — 85 entries
- **B-017** `بيانات` (pandas) — 92 entries
- **B-018** `صور` (Pillow/PIL) — 38 entries
- **B-057** `سيبورن` (seaborn) — 38 entries
- **B-058** `سايباي` (scipy) — 17 entries
- **B-059** `أيو_هتب` (aiohttp) — 22 entries

#### Dictionary updates

- **B-040** `ar-v1.1` — `async`, `await`, `match`, `case`, `type` soft keywords; alternate `متزامن` spelling.

#### Tooling

- **B-055** Formatter (`ثعبان نسّق`) — deterministic `.apy` source formatter.
- **B-056** Linter (`ثعبان راجع`) — static analysis with codes W001–W004, E001, I001.

#### Documentation

- **B-060** Arabic wiki — 5 wiki pages: builtins, exceptions, stdlib-aliases, science-aliases, web-aliases.

### Package metadata

- Package renamed from `apython` → `lughat-althuban` for PyPI publication.
- Entry-point script: `ثعبان` (Arabic for "snake").
- Dictionary and alias TOML files shipped as package data (no source-tree dependency).
- Requires Python ≥ 3.11.

[0.3.0]: https://github.com/GalaxyRuler/lughat-althuban/releases/tag/v0.3.0

### Tooling & third-party aliases (B-053 through B-059)

Test suite: **2386 passing, 21 skipped**.

#### B-059 — aiohttp (`أيو_هتب`)

22 entries covering `ClientSession` (`جلسه_غير_متزامنه`), `ClientTimeout` (`مهله_عميل`),
`TCPConnector`, `BasicAuth`, `FormData`, `StreamReader`, web-server helpers
(`web.Application`, `web.run_app`, `web.Response`, `web.json_response`),
`WebSocketResponse`, and all client error/exception classes.
Demo: `examples/B59_aiohttp_demo.apy`.

#### B-058 — scipy (`سايباي`)

17 entries mapping scipy's major submodule namespaces: `احصاء_متقدم` (stats),
`تحسين` (optimize), `تكامل` (integrate), `جبر_خطي` (linalg), `استيفاء`
(interpolate), `تحويل_فوريه` (fft), `معالجه_اشارات` (signal), `مصفوفات_مبعثره`
(sparse), `هندسه_فضائيه` (spatial), `دالات_خاصه` (special), `ثوابت` (constants).
Demo: `examples/B58_scipy_demo.apy`.

#### B-057 — seaborn (`سيبورن`)

38 entries: full coverage of relational (`خط_بياني`, `مخطط_نقاط`), distribution
(`توزيع_بيانات`, `كثافه_احتماليه`, `توزيع_تراكمي`), categorical (`مخطط_شريطي`,
`مخطط_صندوقي`, `مخطط_كمان`, `مخطط_سرب`), matrix (`خريطه_حراره`), multi-plot grids,
theming (`ضبط_موضوع`, `احضر_لوحه`), and dataset helpers (`حمل_بيانات`).
Demo: `examples/B57_seaborn_demo.apy`.

#### B-056 — Linter (`ثعبان راجع`)

`arabicpython/linter.py` — static analysis for `.apy` files.
Codes: W001 (line length), W002 (trailing whitespace), W003 (tab indent),
W004 (mixed Arabic/Latin identifier), E001 (ar-v1 keyword in ar-v2 file),
I001 (no module intro). CLI: `ثعبان راجع [--select CODES] [--no-info] FILE…`.
23 tests. Demo: `examples/B56_linter_demo.apy`.

#### B-055 — Formatter (`ثعبان نسّق`)

`arabicpython/formatter.py` — deterministic source formatter for `.apy` files.
Fixes: tab→space indentation, trailing whitespace, blank-line collapse (≤2),
comment spacing (`#comment` → `# comment`), comma spacing.
CLI: `ثعبان نسّق [--check] FILE…`. Idempotent. 22 tests.
Demo: `examples/B55_formatter_demo.apy`.

#### B-054 — Jupyter Kernel

`arabicpython_kernel/` package — `ArabicPythonKernel` extends `IPythonKernel`.
Translates Arabic Python in `do_execute` before execution; Arabic tab-completion
for keywords and alias module names; `__main__.py` installer
(`python -m arabicpython_kernel install`). Optional dep group: `pip install lughat-althuban[kernel]`.
17 structural tests (no live Jupyter required). Language: `apy`, extension: `.apy`.

#### B-053 — VSCode Extension

`editors/vscode/` — full VSCode language extension for `.apy` files.
Ships: `package.json` (language contribution, grammar, LSP config),
`extension.js` (LanguageClient wrapping `ثعبان خادم`, status-bar item),
`language-config.json` (brackets, Arabic wordPattern, indentation rules),
`syntaxes/apy.tmLanguage.json` (TextMate grammar — 12 repository rules,
500+ Arabic keywords/builtins). Generator: `tools/generate_vscode_grammar.py`.
51 structural tests.

### Phase B — stdlib aliases (B-030 through B-038)

All modules import via Arabic names and expose curated Arabic attribute aliases.
Every batch ships with a TOML mapping, test file, cross-consistency test (no
Arabic key collisions with earlier batches), demo `.apy` file, and snapshot.
CI matrix established for Ubuntu, macOS, and Windows on Python 3.11, 3.12, and 3.13.

#### B-038 — hashlib (`هاشلب`), io (`مجاري`), contextlib (`مدير_سياق`)

- **هاشلب**: 17 entries — `شا256`, `مد5`, `بليك_ب/ص`, `خوارزميات_مضمونه`, `مشتق_مفتاح`, `هاش_ملف`, SHA-3 family.
- **مجاري**: 16 entries — `تيار_نص` (StringIO), `تيار_بايت` (BytesIO), Buffered*/TextIOWrapper, IOBase hierarchy, `ابحث_بدايه/حاليه/نهايه` (SEEK_*).
- **مدير_سياق**: 11 entries — `مدير_سياق_داله` (contextmanager), `اكتم` (suppress), `سياق_فارغ` (nullcontext), ExitStack, redirect_stdout/stderr.

#### B-037 — asyncio (`اتزامن`)

46 entries: `شغل` (run), `تريث` (sleep — uses `تريث` not `نمه` to avoid collision with `وقت_نظام`), `اجمع_مهام` (gather), `انتظر`/`انتظر_من_اجل`, Task/Future/TaskGroup, Lock/Queue/Semaphore/Barrier, `مهله` (timeout), coroutine checks, event-loop helpers.

Note: `حلقه_احداث` maps to `AbstractEventLoop` (not `EventLoop` which is Python 3.13-only).

#### B-036 — logging (`تسجيل`)

41 entries: level constants (`مستوى_تصحيح`/`مستوى_خطا`/…), logger functions, `احضر_مسجل` (getLogger), Handler/Formatter (`منسق_سجل`)/Filter class aliases, StreamHandler/FileHandler/NullHandler.

#### B-035 — math (`رياضيات`), statistics (`احصاء`), random (`عشوائيات`)

- **رياضيات**: 41 entries — `باي`, `جذر`, `مصنوعيه` (factorial), `قاسم_مشترك` (gcd), trig functions (جيب/جيب_تمام/ظل), `توليفه`/`تباديل_عدد` (comb/perm).
- **احصاء**: 21 entries — `وسط` (mean), `وسيط` (median), `منوال` (mode), `انحراف` (stdev), `توزيع_طبيعي` (NormalDist).
- **عشوائيات**: 21 entries — `عشوائي` (random), `عدد_عشوائي` (randint), `اختر` (choice), `خلط` (shuffle), `ابذر` (seed). Uses `بايتات_عشوائيه_عدد` for `randbytes` (avoids collision with `os.urandom`).

#### B-034 — re (`تعابير_نمطيه`), string (`نصوص`), textwrap (`تنسيق_نص`)

- **تعابير_نمطيه**: 33 entries — `رجم` (compile), `طابق` (match), `ابحث` (search), `عوض` (sub — uses `عوض` not `استبدل` to avoid dialect `.replace` collision), `خطأ_نمط` maps to `re.error` (not `PatternError` which is Python 3.13-only), Pattern/Match unbound methods.
- **نصوص**: 14 entries — Template/Formatter class aliases, `بديل_امن` (safe_substitute).
- **تنسيق_نص**: 8 entries — `التف` (wrap), `امل` (fill), `اختصر` (shorten), TextWrapper class.

#### B-033 — json (`جيسون`), csv (`ملفات_csv`), sqlite3 (`قاعدة_بيانات`)

- **جيسون**: 10 entries — `نص` (dumps), `من_نص` (loads), `حفظ`/`تحميل` (dump/load), JSONEncoder/Decoder unbound `رمز`/`فكك`.
- **ملفات_csv**: 17 entries — `قارئ`/`كاتب` (reader/writer), DictReader/DictWriter with `اكتب_سطر`/`اكتب_راس`, QUOTE_* constants.
- **قاعدة_بيانات**: 23 entries — `اتصل` (connect), Connection/Cursor/Row, `نفذ`/`نفذ_عديد`/`ثبت`/`تراجع`/`اغلق`, `اجلب_واحد`/`اجلب_الكل`.

#### B-032 — datetime (`مكتبة_تاريخ`), time (`وقت_نظام`), calendar (`روزنامه`)

#### B-031 — collections (`مجموعات`), itertools (`ادوات_تكرار`), functools (`ادوات_داليه`)

#### B-030 — os (`نظام_تشغيل`), pathlib (`مسار_مكتبه`), sys (`نظام`)

### SDK aliases

- **فلاسك** (flask): ~60 entries covering Flask app, routes, request/response, blueprints, error handlers.
- **طلبات** (requests): core HTTP surface — `اجلب`/`ارسل`/`رفع`/`حذف`, Session, Response aliases.

## [0.1.1] — 2026-04-20 — Dictionary rendering + coverage pass

Post-release doc and dictionary improvements. No code changes.

### Changed — dictionaries

- **ar-v1.md rendering convention**: all canonical entries now shown in natural
  visible (pre-normalizer) form. The ADR 0004 normalizer folds on lookup so
  runtime behaviour is unchanged; this is documentation-only. 45 entries
  corrected — primarily `خطأ_*` → `خطأ_*` exception names, `اي` → `أي`,
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
- **Tutorial**: Arabic getting-started documentation covering the eight ADR-0007 ship topics.

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
