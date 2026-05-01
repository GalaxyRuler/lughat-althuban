# Spec packet index

| ID | Title | Phase | Owner | Status |
|---|---|---|---|---|
| 0000 | Template (do not implement) | — | — | reference |
| 0001 | dictionary-v1 | A | Claude | merged |
| 0002 | normalize-v1 | A | Codex | merged |
| 0003 | dialect-loader-v1 | A | Gemini 3.1 Pro | merged |
| 0004 | pretokenize-v1 | A | Gemini 3.1 Pro | merged |
| 0005 | core-translate-v1 | A | Gemini 3.1 Pro | merged |
| 0006 | cli-v1 | A | Gemini 3.1 Pro | merged |
| 0007 | import-hook-v1 | A | Gemini 3.1 Flash | merged |
| 0008 | repl-v1 | A | Gemini 3.1 Flash | merged |
| 0009 | translated-tracebacks-v1 | A | Gemini 3.1 Pro | merged |
| 0010 | examples-v1 | A (wrap) | Gemini 3.1 Pro | merged |
| 0011 | fstring-interior-3-11 | A (post-wrap fix) | Gemini 3.1 Pro | merged |
| 0012 | arabic-docs-translation-v1 | A (doc wrap) | Gemini | merged |
| 0013 | search-engine-v1 | A (showcase) | Gemini Pro | merged |
| 0014 | prayer-times-v1 | A (showcase) | Gemini Pro | merged |
| B-001 | alias-runtime-v1 | B (foundation) | — | merged |
| B-002 | phase-a-compat-suite | B (foundation) | — | merged |
| B-010 | aliases-flask-v1 | B (SDK) | — | merged |
| B-011 | aliases-fastapi-v1 | B (SDK) | — | merged |
| B-012 | aliases-django-core-v1 | B (SDK) | — | merged |
| B-013 | aliases-sqlalchemy-v1 | B (SDK) | — | merged |
| B-014 | aliases-requests-extras-v1 | B (SDK) | — | merged |
| B-015 | aliases-pytest-v1 | B (SDK) | — | merged |
| B-016 | aliases-numpy-core-v1 | B (SDK) | — | merged |
| B-017 | aliases-pandas-core-v1 | B (SDK) | — | merged |
| B-018 | aliases-pillow-v1 | B (SDK) | — | merged |
| B-030 | stdlib-os-pathlib-sys | B (stdlib) | — | merged |
| B-031 | stdlib-collections-itertools-functools | B (stdlib) | — | merged |
| B-032 | stdlib-datetime-time-calendar | B (stdlib) | — | merged |
| B-033 | stdlib-json-csv-sqlite3 | B (stdlib) | — | merged |
| B-034 | stdlib-re-string-textwrap | B (stdlib) | — | merged |
| B-035 | stdlib-math-statistics-random-decimal-fractions | B (stdlib) | — | merged |
| B-036 | stdlib-logging | B (stdlib) | — | merged |
| B-037 | stdlib-asyncio-core | B (stdlib) | — | merged |
| B-038 | stdlib-leftovers | B (stdlib) | — | merged |
| B-040 | dictionary-v1.1-async-match | B (dictionary) | — | merged |
| B-041 | traceback-arabic-frames-v1.1 | B (dictionary) | — | merged |
| B-050 | vscode-extension-syntax-v1 | B (tooling) | — | merged |
| B-051 | formatter-arabic-aware-v1 | B (tooling) | — | merged |
| B-052 | lsp-server-v1 | B (tooling) | — | merged |
| B-053 | linter-arabicpython-v1 | B (tooling) | — | merged |
| B-054 | repl-readline-arabic-v1 | B (tooling) | — | merged |
| B-060 | tutorial-translation | B (docs) | — | merged |
| B-061 | error-message-coverage | B (audit) | Claude | merged |
| C-001 | pypi-release-v1 | C (foundation) | Claude | merged |
| C-002 | class-proxy-v1 | C (foundation) | Claude | merged |
| C-010 | aliases-matplotlib-v1 | C (data science) | — | merged |
| C-011 | aliases-scikit-learn-v1 | C (data science) | — | merged |
| C-012 | aliases-pydantic-v1 | C (app foundation) | — | merged |
| C-013 | aliases-httpx-v1 | C (app foundation) | — | merged |
| C-014 | aliases-click-v1 | C (CLI) | Claude | merged |
| C-015 | aliases-rich-v1 | C (CLI) | — | merged |
| C-016 | aliases-redis-v1 | C (persistence) | — | merged |
| C-017 | aliases-celery-v1 | C (persistence) | — | merged |
| C-018 | aliases-pymongo-v1 | C (persistence) | — | merged |
| C-019 | aliases-asyncpg-v1 | C (persistence) | — | merged |
| C-020 | aliases-openpyxl-v1 | C (office) | — | merged |
| C-021 | aliases-python-docx-v1 | C (office) | — | merged |
| C-022 | aliases-python-dotenv-v1 | C (config) | — | merged |
| C-023 | aliases-pyyaml-v1 | C (config) | — | merged |
| C-024 | aliases-playwright-v1 | C (automation) | — | merged |
| C-025 | aliases-beautifulsoup4-v1 | C (automation) | — | merged |
| C-026 | aliases-pyjwt-v1 | C (auth) | — | merged |
| C-030 | dictionary-v2 | C (dictionary) | — | merged |
| C-040 | integration-demo-v1 | C (validation) | — | merged |

## Legend

- **Status**: `drafted` → `in-progress` → `delivered` → `reviewing` → `merged` | `blocked`
- **Historical statuses**: old packet files may still describe `stub` or `deferred` work from planning time; this index records the current repository state.
- **Owner**: the implementer assigned to the packet. Phase A used `Codex` for the early packets and switched to `Gemini 3.1 Pro` / `Gemini 3.1 Flash` partway through. `Claude` is the owner for planner-only work (dictionary curation, decision docs, spec authoring). Phase B and C packets are unclaimed at draft time; contributors claim via the `propose-claim` GitHub issue template.

## Phase B map

Phase B is complete in the current repository. The historical roadmap remains at [`ROADMAP-PHASE-B.md`](../ROADMAP-PHASE-B.md), and active contribution guidance is in [`CONTRIBUTING.md`](../CONTRIBUTING.md).

## Phase C map

Phase C is complete in the current repository. Its historical 20-packet roadmap is [`ROADMAP-PHASE-C.md`](../ROADMAP-PHASE-C.md), and the charter is [`decisions/0011-phase-c-charter.md`](../decisions/0011-phase-c-charter.md).

## Phase D map

Phase D is active. The current contributor roadmap is [`ROADMAP-PHASE-D.md`](../ROADMAP-PHASE-D.md), and the charter is [`decisions/0012-phase-d-charter.md`](../decisions/0012-phase-d-charter.md).
