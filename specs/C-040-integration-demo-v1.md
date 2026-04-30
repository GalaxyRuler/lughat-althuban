# C-040 — Phase C completion demo

Phase C's charter defines completion in §C.5 as a measurable full-stack outcome: an Arabic-speaking developer can install `lughat-althuban` and build a complete REST API with a database, background tasks, authentication, and Excel export while keeping Arabic method names on returned objects. This packet delivers that integration proof as one self-contained `.apy` program plus tests that run it end-to-end and inspect the required Arabic object methods.

## Acceptance

- The demo imports and composes `فاست_أبي` (FastAPI).
- The demo imports and composes `قاعده_وثائق` (pymongo) with a `mongomock` backend and no live server.
- The demo imports and composes `مهام_خلفيه` (celery) in eager mode.
- The demo imports and composes `جي_دبليو_تي` (PyJWT) for bearer-token authentication.
- The demo imports and composes `جداول_اكسل` (openpyxl) to return in-memory `.xlsx` bytes.

## Files Delivered

- `examples/C40_full_stack_demo.apy`
- `tests/test_c040_integration.py`
- `arabicpython/aliases/celery.toml`
- `arabicpython/aliases/fastapi.toml`
- `arabicpython/aliases/jwt.toml`
- `pyproject.toml`
- `tests/test_phase_a_compat.py`
- `specs/INDEX.md`
