# Phase C Roadmap

**Status as of 2026-05-01:** Phase C is complete and historical. PyPI metadata, ClassProxy support, application-library aliases, `ar-v2`, the integration demo, and the canonical lexicon are shipped. The active phase is Phase D; see [`ROADMAP-PHASE-D.md`](ROADMAP-PHASE-D.md) and [`decisions/0012-phase-d-charter.md`](decisions/0012-phase-d-charter.md).

This file is the historical contributor-friendly map of what Phase C contained and what depended on what. To pick up current work, see [CONTRIBUTING.md](CONTRIBUTING.md) and the Phase D roadmap. To understand *why* Phase C was structured this way, see [decisions/0011-phase-c-charter.md](decisions/0011-phase-c-charter.md).

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
| C-001 | pypi-release-v1 — `pyproject.toml` + CI publish workflow + CHANGELOG + v0.3.0 tag | — | M | merged | — | no (infrastructure) |
| C-002 | class-proxy-v1 — `ClassProxy` runtime: per-class `[classes]` TOML section + `__getattr__` proxy + edge-case test suite | C-001 | M | merged | — | no (architectural) |

**⚠️ C-001 must merge before any library packet. C-002 must merge before any packet that needs ClassProxy (C-010–C-013, C-018, C-020, C-021, C-024, C-025).**

---

## Core library aliases

### Data science completion

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-010 | aliases-matplotlib-v1 — `رسوم_بيانيه`; Figure, Axes, pyplot surface; also adds pandas DataFrame + numpy ndarray ClassProxy sections | C-002 | L | merged | — | no (large surface) |
| C-011 | aliases-scikit-learn-v1 — `تعلم_آلي`; estimators, pipelines, preprocessing, metrics; also adds Flask ClassProxy | C-002 | L | merged | — | no (large surface) |

### Modern application foundation

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-012 | aliases-pydantic-v1 — `نماذج_بيانات`; BaseModel, Field, validators, model_config; also adds SQLAlchemy ClassProxy | C-002 | M | merged | — | yes |
| C-013 | aliases-httpx-v1 — `طلبات_حديثه`; sync + async Client, Request, Response; also adds requests Session/Response ClassProxy | C-002 | M | merged | — | **yes** |

### CLI and terminal

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-014 | aliases-click-v1 — `كليك`; @command, @option, @argument, @group, Context | C-001 | S | merged | — | **yes** |
| C-015 | aliases-rich-v1 — `ريتش`; Console, Table, Progress, Panel, Markdown, Syntax, Spinner | C-001 | S | merged | — | **yes** |

### Data persistence

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-016 | aliases-redis-v1 — `مخزن_سريع`; StrictRedis, connection pool, pub/sub, pipeline, Lua scripting | C-001 | M | merged | — | yes |
| C-017 | aliases-celery-v1 — `مهام_خلفيه`; Celery app, @task, delay, apply_async, chord, group, chain, beat | C-001 | M | merged | — | no (async complexity) |
| C-018 | aliases-pymongo-v1 — `قاعده_وثائق`; MongoClient, Database, Collection, CRUD, aggregation pipeline; ClassProxy on Collection/Cursor | C-002 | M | merged | — | yes |
| C-019 | aliases-asyncpg-v1 — `قاعده_بوست`; Connection, Pool, fetch, fetchrow, fetchval, execute, transaction | C-001 | S | merged | — | **yes** |

### Office / data exchange

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-020 | aliases-openpyxl-v1 — `جداول_اكسل`; Workbook, Worksheet, Cell, styles, charts; ClassProxy on Workbook/Worksheet/Cell | C-002 | M | merged | — | **yes** |
| C-021 | aliases-python-docx-v1 — `مستندات_وورد`; Document, Paragraph, Table, Run, styles; ClassProxy on Document | C-002 | M | merged | — | yes |

### Configuration

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-022 | aliases-python-dotenv-v1 — `دوت_إنف`; load_dotenv, dotenv_values, get_key, set_key, find_dotenv | C-001 | S | merged | — | **yes** |
| C-023 | aliases-pyyaml-v1 — `يامل`; safe_load, safe_dump, full_load, Loader, Dumper | C-001 | S | merged | — | **yes** |

### Automation and scraping

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-024 | aliases-playwright-v1 — `متصفح_الي`; async API: Browser, Page, Locator, expect; ClassProxy on Page/Locator | C-002 | M | merged | — | yes |
| C-025 | aliases-beautifulsoup4-v1 — `تحليل_ويب`; BeautifulSoup, Tag, find, find_all, CSS selectors, NavigableString; ClassProxy on BeautifulSoup/Tag | C-002 | M | merged | — | yes |

### Authentication

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-026 | aliases-pyjwt-v1 — `جي_دبليو_تي`; encode, decode, get_unverified_header, PyJWTError, algorithms | C-001 | S | merged | — | **yes** |

---

## Dictionary

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| C-030 | dictionary-v2 — `ar-v2.md`: revised keywords (`باسم`, `مرر`, `طالما`, `يكون`) with backward-compatible dictionary versioning | C-001 | S | merged | — | **yes** (Arabic linguists) |

---

## Pickup advice

Phase C packets have shipped. New contributors should start with [`ROADMAP-PHASE-D.md`](ROADMAP-PHASE-D.md), issues labeled documentation, examples, alias coverage, or lexicon review. Larger new surfaces should get a fresh packet under `specs/packets/`.

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

## What Phase C explicitly deferred into Phase D

The items below are now tracked by [`ROADMAP-PHASE-D.md`](ROADMAP-PHASE-D.md) and [`decisions/0012-phase-d-charter.md`](decisions/0012-phase-d-charter.md).

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
