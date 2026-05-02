# 0011 — Phase C charter

**Status**: accepted  
**Date**: 2026-04-28  
**Deciders**: project planner  

---

<div dir="rtl">

## النسخة العربية

### السياق

أنجزت المرحلة ب طبقة الأسماء العربية للمكتبات، وتشغيل الملفات العربية، والأدوات التعليمية، لكنها تركت ثلاث فجوات يجب أن تحسمها المرحلة ج:

1. **فجوة التثبيت**: لا يكفي أن ينسخ المستخدم المستودع ويثبته محليا. يجب أن يصبح التثبيت العادي ممكنا عبر PyPI.
2. **فجوة الصفات بعد النقطة**: أسماء الوحدات العربية وحدها لا تكفي؛ عندما يرجع البرنامج كائنا مثل `DataFrame` أو `Response` أو `Path` يجب أن تبقى الطرق والصفات عربية أيضا.
3. **فجوة التطبيق الحقيقي**: تغطية المرحلة ب نافعة للتجارب، لكنها لا تكفي لبناء تطبيق إنتاجي كامل. المرحلة ج تضيف مكتبات البيانات، الويب، التخزين، المهام الخلفية، الملفات المكتبية، المصادقة، الأتمتة، وواجهات سطر الأوامر.

كما أن دعم Excel وWord مهم عمليا في بيئات العمل العربية، لذلك أعطت المرحلة ج `openpyxl` و`python-docx` مكانا واضحا في الخطة.

### القرار

تفتح المرحلة ج ببوابة تثبيت ونشر واضحة:

```bash
pip install lughat-althuban
```

وتضيف بنية `ClassProxy` حتى تترجم أسماء الطرق والصفات على الكائنات، لا أسماء الوحدات فقط. كل مكتبة يمكن أن تحمل خرائط صفية في ملفات TOML، ثم يلتف وقت التشغيل حول الكائنات الراجعة ويترجم الوصول إلى الصفات العربية قبل تمريره إلى الكائن الأصلي.

القيود الأساسية:

- لا تترجم طرق dunder مثل `__len__` و`__iter__`.
- يجب أن تبقى فحوص `isinstance` صحيحة.
- الاسم العربي غير المعروف يعطي `AttributeError` واضحا مع تلميحات.
- الاسم الإنجليزي غير المعروف يمر بسياسة توافقية مع تحذير، كما في طبقة aliases.

### حزم المرحلة ج

| الحزمة | الهدف |
|--------|-------|
| C-001 | نشر PyPI، و`pyproject.toml`، وسير عمل الإصدار، و`CHANGELOG.md` |
| C-002 | بنية `ClassProxy` واختباراتها |
| C-010 إلى C-013 | حزم الأساس: `matplotlib`، و`scikit-learn`، و`pydantic`، و`httpx` |
| C-014 إلى C-019 | حزم التطبيق: `click`، و`rich`، و`redis`، و`celery`، و`pymongo`، و`asyncpg` |
| C-020 إلى C-023 | حزم البيانات والمكاتب: `openpyxl`، و`python-docx`، و`python-dotenv`، و`PyYAML` |
| C-024 إلى C-026 | الأتمتة والمصادقة: `playwright`، و`beautifulsoup4`، و`PyJWT` |
| C-030 | قاموس `ar-v2` الاختياري مع أربع مراجعات للكلمات |

كما توسع المرحلة ج تغطية `ClassProxy` لمكتبات المرحلة ب المهمة مثل `pandas` و`numpy` و`Flask` و`SQLAlchemy` و`requests`.

### قاموس ar-v2

لا تكسر المرحلة ج ملفات `ar-v1`. بدلا من ذلك تضيف `ar-v2` اختياريا، وتراجع أربع كلمات فقط:

| Python | ar-v1 | ar-v2 | السبب |
|--------|-------|-------|-------|
| `as` | `كـ` | `باسم` | أوضح في سياق الاستيراد |
| `pass` | `مرر` | `تجاوز` | أقرب لمعنى تخطي الكتلة |
| `while` | `طالما` | `بينما` | اختيار أوسع قبولا |
| `is` | `هو` | `يكون` | أقل التباسا من الضمير |

### معيار النجاح

تنجح المرحلة ج عندما يستطيع مطور عربي تثبيت الحزمة، ثم كتابة REST API كاملة بالعربية: خادم FastAPI، قاعدة بيانات، مهام خلفية، مصادقة JWT، وتصدير Excel، مع أسماء عربية للطرق على الكائنات الراجعة.

هذا المعيار يقيس شيئا إنتاجيا حقيقيا، ولا يمكن تحقيقه دون `ClassProxy`.

### ما يؤجل إلى المرحلة د

تؤجل المرحلة ج الأسطح الكبيرة أو المختلفة جذريا: `tensorflow`، و`pytorch`، و`transformers`، و`boto3`، و`openai`، و`anthropic`، و`opencv`، و`tkinter`، وتفرعات CPython، واللهجات العربية الأخرى، والترجمة العكسية، وملعب WebAssembly.

### نموذج المساهمة

تعتمد المرحلة ج على أمناء للمكتبات، ومراجعة عربية أصلية لكل اسم جديد، ومراجعة مصطلحية عبر Siwar KSAA عندما يكون ذلك مناسبا، وقالب issue لاقتراح alias ناقص دون الحاجة إلى كتابة spec كامل.

</div>

---

## Context

Phase B shipped everything it promised: the module-proxy alias runtime (B-001), 21 stdlib alias batches, 10 SDK aliases (Flask, FastAPI, Django, SQLAlchemy, pytest, numpy, pandas, Pillow, seaborn, scipy, aiohttp, plus extras), a full tooling layer (formatter, linter, LSP, VS Code extension, Jupyter kernel, pip wrapper, pytest runner), an Arabic tutorial and cookbook (B-060), and 100 % error-message translation coverage (B-061). The test suite stands at 2,570 passing tests.

Three forces shape what Phase C must solve:

1. **The installation gap.** The project has no PyPI release. Every potential user must clone the repository, run `pip install -e .`, and trust the setup. This is not a real deployment story. Until `pip install lughat-althuban` works, the audience is contributors, not users.

2. **The class-proxy gap.** Phase B's alias runtime covers module-level names only. Once a developer receives an object — a `DataFrame`, a `Response`, a `Path` — they fall back to English for every method call. A language that is Arabic only up to the first dot operator is incomplete. Phase C must solve instance-level (class) proxying.

3. **The production-application gap.** Phase B's library coverage — numpy, pandas, Flask, FastAPI — is enough for data science notebooks and toy web services. It is not enough to build a complete production application. A real app needs: ML pipelines (scikit-learn), modern HTTP clients (httpx), task queues (celery), caching (redis), document databases (pymongo), CLI tooling (click), Excel I/O (openpyxl), terminal UI (rich), environment configuration (python-dotenv), JWT authentication (PyJWT), browser automation (playwright), and web scraping (beautifulsoup4). Phase C adds these.

A secondary observation: the Arab business world runs heavily on Excel and Microsoft Office workflows. Covering `openpyxl` and `python-docx` is a practical, visible win in that market that is disproportionately impactful relative to engineering effort.

---

## Decision

### C.0 PyPI publication is the Phase C gate-zero

Before any library alias packet in Phase C is merged, the project must be installable from PyPI:

```bash
pip install lughat-althuban
```

This requires:
- A proper `pyproject.toml` (replacing or supplementing the existing `setup.py` / `setup.cfg` if present) with canonical metadata: name, version, description, classifiers, `python_requires >= 3.11`, entry points for `ثعبان` CLI.
- A CI publish workflow (GitHub Actions: `publish.yml`) that runs on version tags, builds the wheel and sdist, and uploads to PyPI via trusted publishing (OIDC, no stored API token).
- A versioning policy: `MAJOR.MINOR.PATCH` where MAJOR increments on dictionary-version changes, MINOR on new library packets or feature additions, PATCH on bug fixes. Phase C opens at `0.3.0` (Phase A = 0.1.x, Phase B = 0.2.x).
- A `CHANGELOG.md` at the repo root, updated on every release.

Packet: **C-001**.

### C.1 Class-proxy architecture: per-class attribute maps in TOML

Phase B's proxy covers `module.attribute` access. Phase C extends the same proxy system to cover `instance.method` access, using the same per-library TOML files. The extension works as follows:

Each library TOML may now contain a `[classes]` section alongside `[entries]`:

```toml
[classes.DataFrame]
"تجميع"       = "groupby"
"دمج"         = "merge"
"تصفيه"       = "query"
"احصائيات"    = "describe"
"قيم_مفقوده"  = "isnull"
"امل_فراغات"  = "fillna"
"احذف_فراغات" = "dropna"
"رتب"         = "sort_values"
"اعد_تسميه"   = "rename"
"احفظ_csv"    = "to_csv"
"احفظ_excel"  = "to_excel"
"احفظ_json"   = "to_json"
```

When `ModuleProxy` returns an instance of a class named in `[classes]`, it wraps the instance in a `ClassProxy` that intercepts `__getattr__` and translates Arabic method/attribute names through the class map before forwarding to the real instance.

Important constraints:
- `ClassProxy` does **not** intercept dunder methods (starts and ends with `__`); they are always forwarded unmodified to avoid breaking Python's data model.
- `ClassProxy.__class__` returns the underlying class so `isinstance` checks continue to work.
- Unmapped Arabic attribute names raise `AttributeError` with a hint: `"الخاصية 'X' غير موجودة. الخصائص المتاحة: [...]"`.
- Unmapped English attribute names pass through with a `DeprecationWarning` (same policy as Phase B module-level fallback).

This architecture is validated by the `ClassProxy` unit tests in `C-002` before any library uses it.

Packet: **C-002** (ClassProxy runtime).

### C.2 Phase C library packets

Sixteen library alias packets ship in Phase C. They are ordered by dependency and impact:

#### Foundation tier (blocks other packets)

| ID | Library | Arabic import name | Depends on |
|----|---------|-------------------|------------|
| C-010 | `matplotlib` | `رسوم_بيانيه` | C-002 (ClassProxy for Figure/Axes) |
| C-011 | `scikit-learn` | `تعلم_آلي` | C-002 (ClassProxy for estimators) |
| C-012 | `pydantic` | `نماذج_بيانات` | C-001 (release gate) |
| C-013 | `httpx` | `طلبات_حديثه` | C-001 |

#### Application tier

| ID | Library | Arabic import name | Key surface |
|----|---------|-------------------|-------------|
| C-014 | `click` | `واجهه_سطر_اوامر` | `@click.command`, decorators, argument/option helpers |
| C-015 | `rich` | `طباعه_جميله` | Console, Table, Progress, Markdown, Syntax, Panel |
| C-016 | `redis-py` | `مخزن_سريع` | StrictRedis, connection pool, pub/sub, pipeline |
| C-017 | `celery` | `مهام_خلفيه` | Celery app, `@task`, `delay`, `apply_async`, beat scheduler |
| C-018 | `pymongo` | `قاعده_وثائق` | MongoClient, Database, Collection, CRUD + aggregation |
| C-019 | `asyncpg` | `قاعده_بوست` | Connection, Pool, `fetch`, `fetchrow`, `execute` |

#### Data / office tier

| ID | Library | Arabic import name | Key surface |
|----|---------|-------------------|-------------|
| C-020 | `openpyxl` | `جداول_اكسل` | Workbook, Worksheet, Cell, load_workbook, styles |
| C-021 | `python-docx` | `مستندات_وورد` | Document, Paragraph, Table, Run, styles |
| C-022 | `python-dotenv` | `متغيرات_بيئه` | `load_dotenv`, `dotenv_values`, `get_key`, `set_key` |
| C-023 | `PyYAML` | `ضبط_yaml` | `safe_load`, `safe_dump`, `full_load` |

#### Automation / scraping tier

| ID | Library | Arabic import name | Key surface |
|----|---------|-------------------|-------------|
| C-024 | `playwright` | `متصفح_آلي` | Page, Browser, Locator, async API |
| C-025 | `beautifulsoup4` | `تحليل_ويب` | BeautifulSoup, Tag, find/find_all, CSS selectors |

#### Auth tier

| ID | Library | Arabic import name | Key surface |
|----|---------|-------------------|-------------|
| C-026 | `PyJWT` | `رموز_مصادقه` | `encode`, `decode`, `get_unverified_header`, algorithms |

### C.3 Class-proxy coverage for existing Phase B libraries

Phase B's pandas, numpy, Flask, and FastAPI aliases are module-level only. Phase C adds `[classes]` sections to their existing TOMLs, prioritised by usage frequency:

| Library | Classes to proxy | Priority |
|---------|-----------------|----------|
| `pandas` | `DataFrame`, `Series`, `GroupBy`, `DataFrameGroupBy` | C-010 (alongside matplotlib) |
| `numpy` | `ndarray` | C-010 |
| `flask` | `Flask` app instance methods (already partially covered via ClassFactory in B-010; extend) | C-011 |
| `sqlalchemy` | `Session`, `Query`, `Engine`, `Connection` | C-012 |
| `requests` | `Session`, `Response` | C-013 |

These are **sub-packets** of the corresponding C-01x anchor packets, not standalone IDs.

### C.4 ar-v2 dictionary

Phase A froze `ar-v1.md`. Community feedback over the Phase B period revealed a handful of word choices that feel unnatural to native Arabic speakers:

- `كـ` (as) — the dagger-alef suffix reads as a prefix, causing confusion in `استورد X كـ Y`
- `مرر` (pass) — some prefer `تجاوز`
- `طالما` (while) — some prefer `بينما` (which was the alternate)
- `هو` (is) — identity test reads awkwardly in some contexts

Phase C ships **`ar-v2.md`** as an opt-in dictionary. Files declare `# apython: dict=ar-v2` in their header to use it. `ar-v1` files are unaffected. The versioning mechanism (ADR 0010) already supports this. `ar-v2` changes:

| Python | ar-v1 | ar-v2 | Rationale |
|--------|-------|-------|-----------|
| `as` | `كـ` | `باسم` | "by the name of" reads naturally in import context |
| `pass` | `مرر` | `تجاوز` | More natural for "skip this block" |
| `while` | `طالما` | `بينما` | Preferred by the majority of beta testers |
| `is` | `هو` | `يكون` | Less ambiguous with pronoun use |

All other `ar-v1` entries carry forward unchanged into `ar-v2`.

Packet: **C-030**.

### C.5 Phase C success criterion

Phase C is shippable (v0.3.0) when:

> **An Arabic-speaking developer can `pip install lughat-althuban`, then write a complete REST API — with a database, background tasks, authentication, and Excel report export — entirely in Arabic, with Arabic method names on every object.**

Concretely: a single `.apy` program that uses `فاست_أبي` (FastAPI), `قاعده_وثائق` (pymongo), `مهام_خلفيه` (celery), `رموز_مصادقه` (PyJWT), and `جداول_اكسل` (openpyxl), with Arabic method names on all returned objects (e.g., `نتيجه.تجميع(...)`, `مستخدم.احفظ()`).

This is measurable, production-relevant, and specifically requires ClassProxy (C-002) to work.

### C.6 Explicit deferrals to Phase D

The following are **not** in Phase C scope:

- **`tensorflow` / `pytorch` / `transformers`** — the surface area of each is larger than all of Phase B's library packets combined. Each needs its own charter. Phase D.
- **`boto3` (AWS SDK)** — 400+ services; requires a scoped-subset strategy that has not been decided. Phase D.
- **`openai` / `anthropic` SDK** — rapidly evolving APIs; better to alias a stable revision. Phase D (or a rolling packet once APIs stabilize).
- **`opencv`** — large C-extension surface; ClassProxy interactions with numpy arrays need validation first. Phase D.
- **`tkinter`** — stdlib GUI; deprioritized in favor of web-app story. Phase D.
- **CPython fork for native Arabic error messages** (ADR 0007 Layer 4) — requires a dedicated team and a CPython release cycle. Phase D or separate project.
- **Arabic-script language variants** (Urdu, Persian, Kurdish) — different dictionaries, potentially different normalizers. Phase D.
- **Reverse translation** (English `.py` → Arabic `.apy` for reading existing code) — useful, complex, out of scope. Phase D.
- **WebAssembly / browser playground** — high impact but orthogonal to the library coverage story. Phase D.

### C.7 Contributor model

Phase B used a "claim a packet" model with no active contributor community. Phase C formalizes this:

- **Library stewards**: each C-01x packet designates a steward responsible for keeping the TOML current as the upstream library evolves. Stewards are credited in the TOML `[meta]` section.
- **Community review**: all new TOML entries require review from at least one Arabic native speaker before merge.
- **Siwar KSAA cross-check**: the Arabic canonical names in all Phase C TOMLs are cross-checked against the KSAA Siwar lexicographic database before the packet is marked `reviewing`.
- **Issue template**: "Propose a missing alias" — allows users to suggest Arabic names for unmapped English attributes without writing a full spec.

---

## Packet list summary

| ID | Title | Size | Depends on |
|----|-------|------|------------|
| C-001 | pypi-release-v1 — `pyproject.toml` + CI publish + CHANGELOG | M | — |
| C-002 | class-proxy-v1 — `ClassProxy` runtime + unit tests | M | C-001 |
| C-010 | aliases-matplotlib-v1 + pandas/numpy ClassProxy | L | C-002 |
| C-011 | aliases-scikit-learn-v1 + flask ClassProxy | L | C-002 |
| C-012 | aliases-pydantic-v1 + sqlalchemy ClassProxy | M | C-002 |
| C-013 | aliases-httpx-v1 + requests ClassProxy | M | C-002 |
| C-014 | aliases-click-v1 | S | C-001 |
| C-015 | aliases-rich-v1 | S | C-001 |
| C-016 | aliases-redis-v1 | M | C-001 |
| C-017 | aliases-celery-v1 | M | C-001 |
| C-018 | aliases-pymongo-v1 | M | C-002 |
| C-019 | aliases-asyncpg-v1 | S | C-001 |
| C-020 | aliases-openpyxl-v1 | M | C-002 |
| C-021 | aliases-python-docx-v1 | M | C-002 |
| C-022 | aliases-python-dotenv-v1 | S | C-001 |
| C-023 | aliases-pyyaml-v1 | S | C-001 |
| C-024 | aliases-playwright-v1 | M | C-002 |
| C-025 | aliases-beautifulsoup4-v1 | M | C-002 |
| C-026 | aliases-pyjwt-v1 | S | C-001 |
| C-030 | dictionary-v2 — ar-v2 opt-in with 4 revised keywords | S | C-001 |

**Total: 20 packets.** Estimated size breakdown: 3 L, 9 M, 8 S.

---

## Consequences

**Positive:**
- PyPI publication (C-001) removes the single largest barrier to adoption with one packet.
- ClassProxy (C-002) makes the Arabic surface genuinely complete — no more English method names after the first dot.
- The 16 library packets cover the full stack for a production REST API, covering the gap that Phase B intentionally left open.
- `ar-v2` gives the community a path to refine word choices without breaking existing Phase A/B code.
- Formalizing library stewards distributes maintenance load and builds the contributor community Phase D will need.

**Negative:**
- ClassProxy adds a new layer of indirection that may introduce edge-case bugs (dunder method forwarding, pickling, multiprocessing, `copy.deepcopy`). Mitigation: C-002 ships with a dedicated edge-case test suite before any library uses it.
- 20 packets is more than Phase B's 18 (post-cleanup). At solo pace this is a full quarter of sustained work. Mitigation: S-packets (click, rich, dotenv, yaml, pyjwt, asyncpg) can each be completed in a single session; they pad the count without padding the effort.
- `ar-v2` creates a second dictionary to maintain in parallel. Mitigation: `ar-v2` makes exactly 4 changes; the governance overhead is small.

**Neutral:**
- The ClassProxy approach means Phase C is still pure-Python: no CPython patches, no compiled extensions, no fork. The project remains installable from a pure wheel.
- Phase C's success criterion requires 6 libraries working together (FastAPI + pymongo + celery + PyJWT + openpyxl + ClassProxy). This is a higher integration bar than Phase B's single Flask hello-world. It is also a more compelling demo.

---

## Alternatives considered

**Ship ClassProxy in Phase B (retroactively).** Rejected. Phase B already had a well-defined scope and 2,570 passing tests. Retrofitting ClassProxy mid-phase would have required re-testing every existing alias TOML for class-level interactions. The clean break is better architecture.

**Auto-generate class proxy maps from `inspect.getmembers`.** Rejected. Auto-generation produces transliterations (`groupby → جروب_باي`), not translations. Curation is the point. Auto-generation is an acceptable fallback for unmapped names (and is already the Phase B policy via `DeprecationWarning`), not a replacement for curated maps.

**Defer PyPI publication to Phase D.** Rejected. PyPI is the single highest-leverage action in Phase C — it multiplies the impact of every other packet by making the project discoverable and installable. Deferring it makes every other Phase C packet less valuable.

**Use Pydantic models as the ClassProxy mechanism (wrap objects in Pydantic models with Arabic field names).** Rejected. Pydantic is a data validation library, not a proxy layer. It would require defining a Pydantic schema for every class in every library — far more maintenance burden than a TOML `[classes]` section — and it would break `isinstance` checks.

**ar-v2 as a full replacement for ar-v1 (no opt-in).** Rejected. ADR 0003 and ADR 0010 guarantee that existing files keep working with their declared dictionary. A forced replacement would break thousands of lines of Phase A/B user code and violate the compatibility promise of ADR 0008 §B.3.

---

## References

- ADR 0008 — Phase B charter (compatibility promise in B.3 that Phase C inherits)
- ADR 0010 — Dictionary versioning (mechanism that makes ar-v2 opt-in safe)
- ADR 0003 — Keyword dictionary governance (ar-v2 follows the same addition/change rules)
- ADR 0001 — Architecture (ClassProxy must not violate the tokenize-only translation pipeline)
- Python data model — dunder method resolution, `__getattr__` vs `__getattribute__`
- PEP 562 — `__getattr__` on modules (referenced in Phase B; ClassProxy is the instance-level analogue)
- KSAA Siwar lexicographic database — https://siwar.ksaa.gov.sa
