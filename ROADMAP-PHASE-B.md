# Phase B Roadmap

**Status as of 2026-04-27:** Phase A complete. Phase B well underway — B-030 through B-039 merged (26 stdlib modules aliased), Flask (`فلاسك`), requests (`طلبات`), Django (`دجانغو`), and SQLAlchemy (`قاعده_علائقيه`) SDK aliases shipped. B-016/B-017 (numpy/pandas) also merged. Remaining SDK packets open for contributors.

This file is the **single visible map** of what Phase B contains, what's open for contribution, and what depends on what. To pick up work, see [CONTRIBUTING.md](CONTRIBUTING.md). To understand *why* Phase B is structured this way, see [decisions/0008-phase-b-charter.md](decisions/0008-phase-b-charter.md).

---

## Goal of Phase B

> An Arabic-speaking developer can write a working Flask hello-world entirely in Arabic.

That is the success criterion (ADR 0008.B.4). Every Phase B packet either advances toward it or makes it durable.

---

## How to read this roadmap

Each packet has:

- **ID** — the canonical packet identifier. Used in branch names, commit messages, PR titles.
- **Title** — short name.
- **Depends on** — packets that must be `merged` before this one can start.
- **Size** — S (1 session), M (2–3 sessions), L (break this up if not already broken).
- **Status** — see legend at bottom.
- **Owner** — who's implementing. `—` means open for claim. `?` means a stub awaiting a contributor *and* full specification.
- **First-pickup?** — packets explicitly tagged as good entry points for new contributors.

To claim a packet: open a "Claim a packet" issue (template in `.github/ISSUE_TEMPLATE/`). The planner assigns it to you and updates this file.

---

## Foundation (must ship first; gates everything else)

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-001](specs/B-001-alias-runtime-v1.md) | alias-runtime-v1 — proxy meta-path finder + `requests` mapping | — | L | merged | — | no (architectural) |
| [B-002](specs/B-002-phase-a-compat-suite.md) | phase-a-compat-suite — pin Phase A examples in CI permanently | — | S | merged | — | **yes** |

**Why these two first:** B-001 commits to the proxy class's exact public API and TOML schema. Every SDK and stdlib alias packet in Phase B inherits from it. B-002 is the safety net that makes the rest of Phase B safe to land — without it, any later packet could silently break a Phase A example.

---

## SDK aliases — top 10 libraries

One packet per library. All depend on B-001 (which already covers `requests` itself, so there is no separate B-009).

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-010](specs/B-010-aliases-flask-v1.md) | aliases-flask-v1 — ~60 entries; the success-criterion packet | B-001 | M | merged | — | **yes** |
| B-011 | aliases-fastapi-v1 | B-001 | M | stub | ? | yes |
| B-012 | aliases-django-core-v1 — urls, views, models, forms | B-001 | L | merged | — | no (large surface) |
| B-013 | aliases-sqlalchemy-v1 | B-001 | M | merged | — | no (semantic depth) |
| B-014 | aliases-requests-extras-v1 — session/auth surface omitted from B-001 | B-001 | S | stub | ? | **yes** |
| B-015 | aliases-pytest-v1 | B-001 | M | stub | ? | yes |
| B-016 | aliases-numpy-core-v1 | B-001 | L | merged | — | no (large surface) |
| B-017 | aliases-pandas-core-v1 | B-001, B-016 | L | merged | — | no (large surface) |
| B-018 | aliases-pillow-v1 | B-001 | S | stub | ? | **yes** |

**Pickup advice:** B-014 (`requests` extras) and B-018 (`pillow`) are the smallest. B-016, B-017 are real research projects — claim only if you use the library professionally.

---

## Stdlib alias batches

Each batch is a coherent group of stdlib modules that ship together. All depend on B-001.

| ID | Title | Modules covered | Depends on | Size | Status | Owner |
|---|---|---|---|---|---|---|
| [B-030](specs/B-030-stdlib-os-pathlib-sys.md) | stdlib-os-pathlib-sys | `os`, `pathlib`, `sys` | B-001 | M | merged | — |
| B-031 | stdlib-collections-itertools-functools | `collections`, `itertools`, `functools` | B-001 | M | merged | — |
| B-032 | stdlib-datetime-time-calendar | `datetime`, `time`, `calendar` | B-001 | M | merged | — |
| B-033 | stdlib-json-csv-sqlite3 | `json`, `csv`, `sqlite3` | B-001 | M | merged | — |
| B-034 | stdlib-re-string-textwrap | `re`, `string`, `textwrap` | B-001 | M | merged | — |
| B-035 | stdlib-math-statistics-random | `math`, `statistics`, `random` | B-001 | M | merged | — |
| B-036 | stdlib-logging | `logging` | B-001 | S | merged | — |
| B-037 | stdlib-asyncio-core | `asyncio` core surface | B-001 | M | merged | — |
| B-038 | stdlib-hashlib-io-contextlib | `hashlib`, `io`, `contextlib` | B-001 | M | merged | — |
| B-039 | stdlib-subprocess-shutil-argparse-secrets-uuid | `subprocess`, `shutil`, `argparse`, `secrets`, `uuid` | B-001 | M | merged | — |

---

## Dictionary and traceback expansion

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-040](specs/B-040-dictionary-v1.1-async-match.md) | dictionary-v1.1 — `async`, `await`, `match`, `case` keyword translations | — | S | merged | — | **yes** (small, high-impact) |
| B-041 | traceback-coverage-v2 — full Python exception hierarchy + ~120 message templates | — | M | stub | ? | yes |

---

## Tooling — sponsor-conditional (per ADR 0008.B.5)

These ship as **stubs only** until a sponsor commits. Each will need its own ADR before full specification.

| ID | Title | Depends on | Size | Status | Notes |
|---|---|---|---|---|---|
| B-050 | tooling-pip-wrapper | B-001 | M | sponsor-stub | Arabic-named CLI for `pip install` |
| B-051 | tooling-pytest-wrapper | B-015 | S | sponsor-stub | Arabic test runner |
| B-052 | lsp-server-v1 | — | L | sponsor-stub | Language server for IDE completion |
| B-053 | vscode-extension-v1 | B-052 | M | sponsor-stub | Syntax highlight, completion, error squiggles |
| B-054 | jupyter-kernel-v1 | — | L | sponsor-stub | `.apy` cells in Jupyter notebooks |

---

## Documentation translation

Open to non-code contributors. See [CONTRIBUTING.md §3c](CONTRIBUTING.md#3c--documentation-translation).

| ID | Title | Depends on | Size | Status | Owner | First-pickup? |
|---|---|---|---|---|---|---|
| [B-060](specs/B-060-tutorial-translation.md) | tutorial-translation — Python tutorial chapters 1–10 in Arabic, with `.apy` examples | — | L (split into 10 sub-packets) | drafted | — | **yes** (any chapter) |
| B-061 | error-message-coverage — translate ~120 most common interpreter messages | — | M | stub | ? | **yes** |

---

## Dialects — post-v2 (per ADR 0008.B.5)

Stubs only. These are not committed to or foreclosed — they exist as placeholders so dialect contributors can see they're welcome.

| ID | Title | Depends on | Size | Status | Notes |
|---|---|---|---|---|---|
| B-070 | dialect-egyptian | dictionary-v1 frozen | M | future | Colloquial Egyptian keyword set |
| B-071 | dialect-levantine | dictionary-v1 frozen | M | future | Levantine keyword set |
| B-072 | dialect-maghrebi | dictionary-v1 frozen | M | future | Maghrebi keyword set |

---

## Status legend

| Status | Meaning |
|---|---|
| `drafted` | Spec is fully written. Open for claim. |
| `in-progress` | Claimed by an owner; implementation underway. |
| `delivered` | PR open with delivery note. Awaiting review. |
| `reviewing` | Planner is reviewing. |
| `merged` | Shipped on `main`. |
| `blocked` | Waiting on another packet, an ADR, or an external decision. |
| `stub` | Placeholder spec only. Needs full specification before implementation can start. See `specs/B-HANDOFF-FOR-GEMINI.md`. |
| `sponsor-stub` | Stub deferred until a sponsor commits, per ADR 0008.B.5. |
| `future` | Architecturally welcome but no commitment to ship. |

---

## Where to start (decision tree)

- **I write Python and use Flask** → claim B-010.
- **I write Python and use one of the other top-10 libraries** → claim that library's packet (B-011 to B-018).
- **I want a small, high-impact code packet** → claim B-002, B-040, or B-014 (`requests` extras).
- **I want a small, high-impact non-code packet** → claim a single chapter of B-060 (e.g., "tutorial chapter 3 — control flow"), or B-061.
- **I'm an Arabic linguist with no Python background** → review the translation tables in B-010 or B-030 before they're implemented. Comment on the spec packet's PR.
- **I want to design infrastructure** → talk to the planner about B-001 (architectural; not for first-time contributors but possible if you have meta-path finder experience).
- **None of the above fits** → open a "Propose new packet" issue.

---

*This file is updated whenever a packet's status changes. The source of truth is `specs/INDEX.md`; this file is the curated, contributor-friendly view.*
