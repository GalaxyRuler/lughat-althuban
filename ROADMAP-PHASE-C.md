# Phase C Roadmap

**Status as of 2026-04-28:** Phase B complete. Phase C not yet started — all packets open for claim.

This file is the **single visible map** of what Phase C contains, what's open for contribution, and what depends on what. To pick up work, see [CONTRIBUTING.md](CONTRIBUTING.md). To understand *why* Phase C is structured this way, see [decisions/0011-phase-c-charter.md](decisions/0011-phase-c-charter.md).

---

## Goal of Phase C

> An Arabic-speaking developer can `pip install lughat-althuban`, then write a complete REST API — with a database, background tasks, authentication, and Excel report export — entirely in Arabic, with Arabic method names on every object.

That is the success criterion (ADR 0011 §C.5). Every Phase C packet either advances toward it or makes it durable.

---

## How to read this roadmap

Each packet has:

- **ID** — the canonical packet identifier. Used in branch names, commit messages, PR titles.
- **Title** — short name.
- **Depends on** — packets that must be `merged` before this one can start.
- **Size** — S (1 session), M (2–3 sessions), L (break this up if not already broken).
- **Status** — see legend at bottom.
- **Owner** — who's implementing. `—` means open for claim.
- **First-pickup?** — packets explicitly tagged as good entry points for new contributors.

To claim a packet: open a "Claim a packet" issue (template in `.github/ISSUE_TEMPLATE/`). The planner assigns it to you and updates this file.

---

## Foundation (must ship first; gates everything else)

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-001 | pypi-release-v1 — `pyproject.toml` + CI publish workflow + CHANGELOG + v0.3.0 tag | — | M | drafted | — | no (infrastructure) |
| C-002 | class-proxy-v1 — `ClassProxy` runtime: per-class `[classes]` TOML section + `__getattr__` proxy + edge-case test suite | C-001 | M | drafted | — | no (architectural) |

**⚠️ C-001 must merge before any library packet. C-002 must merge before any packet that needs ClassProxy (C-010–C-013, C-018, C-020, C-021, C-024, C-025).**

---

## Core library aliases

### Data science completion

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-010 | aliases-matplotlib-v1 — `رسوم_بيانيه`; Figure, Axes, pyplot surface; also adds pandas DataFrame + numpy ndarray ClassProxy sections | C-002 | L | drafted | — | no (large surface) |
| C-011 | aliases-scikit-learn-v1 — `تعلم_آلي`; estimators, pipelines, preprocessing, metrics; also adds Flask ClassProxy | C-002 | L | drafted | — | no (large surface) |

### Modern application foundation

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-012 | aliases-pydantic-v1 — `نماذج_بيانات`; BaseModel, Field, validators, model_config; also adds SQLAlchemy ClassProxy | C-002 | M | drafted | — | yes |
| C-013 | aliases-httpx-v1 — `طلبات_حديثه`; sync + async Client, Request, Response; also adds requests Session/Response ClassProxy | C-002 | M | drafted | — | **yes** |

### CLI and terminal

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-014 | aliases-click-v1 — `واجهه_سطر_اوامر`; @command, @option, @argument, @group, Context | C-001 | S | drafted | — | **yes** |
| C-015 | aliases-rich-v1 — `طباعه_جميله`; Console, Table, Progress, Panel, Markdown, Syntax, Spinner | C-001 | S | drafted | — | **yes** |

### Data persistence

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-016 | aliases-redis-v1 — `مخزن_سريع`; StrictRedis, connection pool, pub/sub, pipeline, Lua scripting | C-001 | M | drafted | — | yes |
| C-017 | aliases-celery-v1 — `مهام_خلفيه`; Celery app, @task, delay, apply_async, chord, group, chain, beat | C-001 | M | drafted | — | no (async complexity) |
| C-018 | aliases-pymongo-v1 — `قاعده_وثائق`; MongoClient, Database, Collection, CRUD, aggregation pipeline; ClassProxy on Collection/Cursor | C-002 | M | drafted | — | yes |
| C-019 | aliases-asyncpg-v1 — `قاعده_بوست`; Connection, Pool, fetch, fetchrow, fetchval, execute, transaction | C-001 | S | drafted | — | **yes** |

### Office / data exchange

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-020 | aliases-openpyxl-v1 — `جداول_اكسل`; Workbook, Worksheet, Cell, styles, charts; ClassProxy on Workbook/Worksheet/Cell | C-002 | M | drafted | — | **yes** |
| C-021 | aliases-python-docx-v1 — `مستندات_وورد`; Document, Paragraph, Table, Run, styles; ClassProxy on Document | C-002 | M | drafted | — | yes |

### Configuration

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-022 | aliases-python-dotenv-v1 — `متغيرات_بيئه`; load_dotenv, dotenv_values, get_key, set_key, find_dotenv | C-001 | S | drafted | — | **yes** |
| C-023 | aliases-pyyaml-v1 — `ضبط_yaml`; safe_load, safe_dump, full_load, Loader, Dumper | C-001 | S | drafted | — | **yes** |

### Automation and scraping

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-024 | aliases-playwright-v1 — `متصفح_آلي`; async API: Browser, Page, Locator, expect; ClassProxy on Page/Locator | C-002 | M | drafted | — | yes |
| C-025 | aliases-beautifulsoup4-v1 — `تحليل_ويب`; BeautifulSoup, Tag, find, find_all, CSS selectors, NavigableString; ClassProxy on BeautifulSoup/Tag | C-002 | M | drafted | — | yes |

### Authentication

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-026 | aliases-pyjwt-v1 — `رموز_مصادقه`; encode, decode, get_unverified_header, PyJWTError, algorithms | C-001 | S | drafted | — | **yes** |

---

## Dictionary

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-030 | dictionary-v2 — `ar-v2.md` opt-in: 4 revised keywords (`باسم` for `as`, `تجاوز` for `pass`, `بينما` for `while`, `يكون` for `is`); backward-compatible via ADR 0010 versioning | C-001 | S | delivered | — | **yes** (Arabic linguists) |

---

## Pickup advice

- **Fastest wins (single session, minimal dependency):** C-014 (click), C-015 (rich), C-019 (asyncpg), C-022 (dotenv), C-023 (PyYAML), C-026 (PyJWT) — all depend only on C-001.
- **Best for data science contributors:** C-010 (matplotlib + pandas/numpy ClassProxy).
- **Best for ML contributors:** C-011 (scikit-learn).
- **Best for Arabic linguists:** C-030 (ar-v2 dictionary revision).
- **Infrastructure contributors:** C-001 (PyPI release pipeline) — critical path for everything else.
- **Architecture contributors:** C-002 (ClassProxy) — requires Python data model expertise; claim only if you understand `__getattr__`, `__class__`, dunder forwarding, and pickling.

---

## Dependency graph

```
C-001 (PyPI)
  ├── C-002 (ClassProxy)
  │     ├── C-010 (matplotlib + pandas/numpy proxy)
  │     ├── C-011 (scikit-learn + flask proxy)
  │     ├── C-012 (pydantic + sqlalchemy proxy)
  │     ├── C-013 (httpx + requests proxy)
  │     ├── C-018 (pymongo)
  │     ├── C-020 (openpyxl)
  │     ├── C-021 (python-docx)
  │     ├── C-024 (playwright)
  │     └── C-025 (beautifulsoup4)
  ├── C-014 (click)
  ├── C-015 (rich)
  ├── C-016 (redis)
  ├── C-017 (celery)
  ├── C-019 (asyncpg)
  ├── C-022 (dotenv)
  ├── C-023 (PyYAML)
  ├── C-026 (PyJWT)
  └── C-030 (ar-v2 dictionary)
```

---

## Status legend

| Status | Meaning |
|---|---|
| `drafted` | Spec is fully written (or scoped). Open for claim. |
| `in-progress` | Claimed by an owner; implementation underway. |
| `delivered` | PR open with delivery note. Awaiting review. |
| `reviewing` | Planner is reviewing. |
| `merged` | Shipped on `main`. |
| `blocked` | Waiting on another packet, an ADR, or an external decision. |

---

## What Phase C explicitly defers (Phase D)

- `tensorflow` / `pytorch` / HuggingFace `transformers` — each needs its own charter
- `boto3` (AWS) — requires a scoped-subset strategy
- `openai` / `anthropic` SDK — rapidly evolving APIs
- `opencv` — C-extension ClassProxy interactions need validation
- `tkinter` — stdlib GUI; lower priority than web-app story
- WebAssembly / browser playground
- CPython fork for native Arabic error messages (ADR 0007 Layer 4)
- Arabic-script language variants (Urdu, Persian, Kurdish)
- Reverse translation (English `.py` → Arabic `.apy`)

---

*This file is updated whenever a packet's status changes. The source of truth is `specs/INDEX.md`; this file is the curated, contributor-friendly view.*
