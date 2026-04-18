# Spec Packet 0007: import-hook-v1

**Phase**: A
**Depends on**: Packet 0005 (translate); Packet 0006 (cli); ADR 0001 (architecture), ADR 0002 (file extension), ADR 0007 (scope).
**Estimated size**: medium (one focused implementer session)
**Owner**: Gemini 3.1 Pro

## Goal

Implement a `sys.meta_path` import hook so `.apy` files participate in Python's normal `import` machinery. After this packet lands, an `.apy` file can `import` another `.apy` file (or a `.py` file), `.py` files can `import` `.apy` files (after the hook is installed), and `.apy` packages with `__init__.apy` work like any other package.

The CLI runner from Packet 0006 installs the hook automatically so `apython hello.apy` programs can import their own modules without ceremony.

## Non-goals

- **No bytecode caching.** `.apyc` is reserved per `.gitignore` but not produced. Each import re-translates the source. Performance optimization is a separate Phase A or B packet.
- **No namespace packages.** A directory without `__init__.py` or `__init__.apy` is not a package. PEP 420 namespace packages are out of scope for v1.
- **No source maps for tracebacks.** Same constraint as Packet 0006 — tracebacks point at the translated Python line/col, not the original `.apy` line/col. Translated tracebacks are a separate packet.
- **No `-m` flag in the CLI.** Packet 0006 already excluded this. The hook makes it *implementable* in a future packet, but wiring `-m apkg` through `runpy` is out of scope here.
- **No bidirectional import** (i.e. translating English module names to Arabic at the import-name layer). `استورد طلبات` is Phase B library aliasing, not Phase A. Phase A users write `import requests`.
- **No file watching / hot reload.** Stock `importlib.reload` works (and is tested), but the hook does not auto-reload on disk changes.
- **No support for `.zip`/`.egg`/zipimport sources.** Only filesystem `.apy` files. Zip support is additive if ever needed.

## Files

### Files to create

- `arabicpython/import_hook.py`
- `tests/test_import_hook.py`
- `tests/fixtures/apkg/__init__.apy` — fixture package (also referenced in tests)
- `tests/fixtures/apkg/sub.apy` — fixture submodule
- `tests/fixtures/mixed/__init__.py` — mixed package fixture (Python `__init__`)
- `tests/fixtures/mixed/leaf.apy` — Arabic submodule of a Python package
- `tests/fixtures/standalone.apy` — top-level fixture module

(Test fixtures live under `tests/fixtures/` so test files have a stable place to point `sys.path` at. The fixtures directory does not contain its own `__init__.py` — only the named subpackages do.)

### Files to modify

- `arabicpython/cli.py` — add a call to `install()` at the start of `main()` (and add `tests/fixtures/` to nothing — the CLI does not change its sys.path; only fixture tests do). One small edit; see "CLI integration" below.

### Files to read (do not modify)

- `arabicpython/translate.py` — call `translate(source)` from `exec_module`.
- `arabicpython/cli.py` — current shape, to know where to insert `install()`.
- `decisions/0001-architecture.md` — pipeline & meta_path commitment.
- `decisions/0002-file-extension.md` — `.apy` is the canonical extension.
- `decisions/0007-scope.md` — Phase A scope.
- Python `importlib.abc` docs.

## Public interface

```python
# arabicpython/import_hook.py

import importlib.abc
import importlib.machinery
from typing import Sequence


class ApyFinder(importlib.abc.MetaPathFinder):
    """Locate `.apy` modules and packages on sys.path / parent __path__."""

    def find_spec(
        self,
        fullname: str,
        path: "Sequence[str] | None",
        target: "object | None" = None,
    ) -> "importlib.machinery.ModuleSpec | None":
        ...


class ApyLoader(importlib.abc.Loader):
    """Translate, compile, and exec a `.apy` module."""

    def __init__(self, fullname: str, path: str, *, is_package: bool = False) -> None:
        ...

    def create_module(self, spec):
        return None  # use default module creation

    def exec_module(self, module) -> None:
        ...

    def get_source(self, fullname: str) -> str:
        """Return the original .apy source (used by linecache / tracebacks)."""
        ...


def install() -> None:
    """Idempotent: insert ApyFinder at the FRONT of sys.meta_path if not already there.

    The finder only matches `.apy` files, so inserting at position 0 cannot
    shadow stdlib `.py` modules — there is no `os.apy` in the stdlib.
    """


def uninstall() -> None:
    """Idempotent: remove any ApyFinder instances from sys.meta_path.

    Provided primarily for tests. Production code should not need to uninstall.
    """
```

The package re-exports `install` and `uninstall` from `arabicpython/__init__.py`:

```python
# add to arabicpython/__init__.py
from arabicpython.import_hook import install, uninstall  # noqa: E402
```

(Implementer: place the import at the bottom of `__init__.py`, after `__version__`. The `noqa: E402` is acceptable here.)

## Behavior

### Module discovery (`find_spec`)

For a top-level import like `import standalone`:

1. `find_spec("standalone", path=None, target=None)` is called.
2. `path is None` means search `sys.path`.
3. For each entry `p` in `sys.path`:
   - If `os.path.isfile(os.path.join(p, "standalone.apy"))` → return a spec for a module loader.
   - Else if `os.path.isdir(os.path.join(p, "standalone"))` and `os.path.isfile(os.path.join(p, "standalone", "__init__.apy"))` → return a spec for a package loader (`is_package=True`, `submodule_search_locations=[that_dir]`).
4. If neither matches in any `sys.path` entry → return `None` (let other finders try).

For a submodule import like `import apkg.sub`:

1. After `apkg` is loaded, `find_spec("apkg.sub", path=apkg.__path__, target=...)` is called.
2. Search behaves the same but uses `path` instead of `sys.path`. The leaf name is `"sub"` (the part after the last dot).

The finder must NOT raise `ImportError` for misses — it must return `None` so the rest of `sys.meta_path` can try. Only return a non-None `ModuleSpec` for actual hits.

### Module loading (`exec_module`)

```python
def exec_module(self, module):
    with open(self.path, encoding="utf-8") as f:
        source = f.read()
    translated = translate(source)
    code = compile(translated, self.path, "exec")
    exec(code, module.__dict__)
```

Module attributes set by Python's import machinery (we do not need to set them manually if `ModuleSpec` is constructed correctly):
- `__name__` — the dotted module name.
- `__file__` — the absolute path of the `.apy` file.
- `__loader__` — the `ApyLoader` instance.
- `__spec__` — the `ModuleSpec`.
- `__package__` — the parent package name (or the module's own name if it's a package).
- `__path__` — for packages only, the list of directories to search for submodules (`[dir_containing_init_apy]`).

Use `importlib.util.spec_from_file_location(name, path, loader=loader, submodule_search_locations=[...] if is_package else None)` to construct the spec. This handles all the attribute wiring correctly.

### Source retrieval (`get_source`)

`get_source(fullname)` returns the **original** `.apy` source (UTF-8 text). This makes the `linecache` module work for tracebacks: when a runtime error occurs in an imported `.apy` module, Python asks the loader for the source to display the offending line. It will get the original Arabic text, which is what the user wrote — accepting the line-number drift documented in ADR 0001.

If the file cannot be read (permission, disappeared) `get_source` may raise `ImportError`.

### Error handling

- `SyntaxError` from `translate` (bidi, mixed digits) → propagate. The path attribute on the SyntaxError comes from the `compile` call, so set the SyntaxError's `filename` to `self.path` if it's not already populated.
- `SyntaxError` from `compile` → propagate (already has the correct path because we passed `self.path` to `compile`).
- `UnicodeDecodeError` from reading the file as UTF-8 → wrap in `ImportError(f"can't decode {path}: {e}")`.
- `FileNotFoundError` during `exec_module` (file vanished between `find_spec` and `exec_module`) → wrap in `ImportError`.
- Any exception during `exec` of the translated code → propagate (it's the user's code).

### Search order vs. existing finders

- Insert `ApyFinder` at **position 0** in `sys.meta_path`. By construction it only returns specs for `.apy` files, so it cannot shadow stdlib `.py` modules.
- If both `foo.apy` and `foo.py` exist on `sys.path`, **`foo.apy` wins** (because our finder runs first and returns a hit). This is a deliberate choice: a learner who creates `mymodule.apy` expects it to be the one that loads, not a stale `mymodule.py` left behind from a copy.
- Test `test_apy_wins_over_py_when_both_present` verifies this.

### CLI integration

In `arabicpython/cli.py`, add **one line** at the top of `main()`, before any argument parsing or file reading:

```python
def main(argv=None) -> int:
    from arabicpython.import_hook import install
    install()
    # ... existing code ...
```

Place the import inside the function (lazy) so importing `arabicpython.cli` for its `main` symbol does not have an import-time side effect on other test code; the side effect happens only when the CLI actually runs.

This single change makes `apython hello.apy` work when `hello.apy` does `import other_module` and `other_module.apy` is in the same directory. (Note: `apython` does NOT prepend the script's directory to `sys.path`. Stock `python` does this and we will mirror it in a follow-up packet, but it is **out of scope here**. For now, tests that need cross-file imports manage `sys.path` explicitly via fixtures.)

## Implementation constraints

- **Dependencies**: stdlib only (`importlib.abc`, `importlib.machinery`, `importlib.util`, `os`, `sys`).
- **Python version**: 3.11+.
- **Idempotency**: `install()` called twice must NOT add two finders. Check `sys.meta_path` for any instance of `ApyFinder` before inserting.
- **Test isolation**: every test that touches `sys.meta_path`, `sys.modules`, or `sys.path` must clean up after itself. Use a pytest fixture (`autouse=True` per-test or per-module) that snapshots and restores those three lists. See "Test fixtures" below.
- **No global mutable state in the finder/loader** beyond what `sys.meta_path` already mandates.
- **Style**: pass `ruff check .` and `black --check .` at project defaults (line length 100).

## Test requirements

All tests in `tests/test_import_hook.py`. Use exact test names below. Pytest only.

### Test fixtures

Create a single autouse fixture at the top of the test file:

```python
import sys
import importlib

import pytest


@pytest.fixture(autouse=True)
def restore_import_state():
    """Snapshot sys.meta_path, sys.modules, sys.path before each test; restore after."""
    saved_meta_path = sys.meta_path[:]
    saved_modules = dict(sys.modules)
    saved_path = sys.path[:]
    try:
        yield
    finally:
        sys.meta_path[:] = saved_meta_path
        # Remove anything added during the test
        for name in list(sys.modules):
            if name not in saved_modules:
                del sys.modules[name]
        sys.path[:] = saved_path
        importlib.invalidate_caches()
```

A second helper fixture for "fixtures dir on sys.path":

```python
@pytest.fixture
def fixtures_on_path():
    import pathlib
    fdir = str(pathlib.Path(__file__).parent / "fixtures")
    sys.path.insert(0, fdir)
    yield fdir
```

### Install / uninstall (4)

1. `test_install_adds_finder_to_meta_path`: call `install()`, assert an `ApyFinder` instance is in `sys.meta_path`.
2. `test_install_is_idempotent`: call `install()` twice, assert exactly one `ApyFinder` instance in `sys.meta_path`.
3. `test_uninstall_removes_finder`: call `install()` then `uninstall()`, assert no `ApyFinder` instances remain.
4. `test_uninstall_is_idempotent`: call `uninstall()` without prior install — does not raise.

### Basic imports — module discovery (5)

5. `test_import_standalone_apy(fixtures_on_path)`: `install()`, then `import standalone`. Assert the module loaded and a known symbol from `standalone.apy` is accessible (e.g., a function or constant defined in the fixture).
6. `test_import_apy_from_apy(fixtures_on_path)`: a fixture `.apy` file imports another `.apy` file and uses a value from it. (Implementer: extend `standalone.apy` or add a second fixture so this test has something to import.)
7. `test_import_apy_from_py(fixtures_on_path)`: a Python `.py` file (defined inline in the test or as a fixture) imports an `.apy` module. Verify it works after `install()`.
8. `test_no_install_means_no_apy_imports(fixtures_on_path)`: WITHOUT calling `install()`, `import standalone` raises `ModuleNotFoundError`. Confirms the hook is opt-in.
9. `test_finder_returns_none_for_missing_module(fixtures_on_path)`: `install()`, then attempt `import nonexistent_module_xyz` — raises `ModuleNotFoundError` (not some weird internal error). Confirms the finder cooperates with the rest of `sys.meta_path` instead of monopolizing import.

### Packages (4)

10. `test_import_apy_package(fixtures_on_path)`: `install()`, then `import apkg`. Assert `apkg.__path__` is set and a symbol defined in `apkg/__init__.apy` is accessible as an attribute.
11. `test_import_apy_submodule(fixtures_on_path)`: `install()`, then `import apkg.sub`. Assert both `apkg` and `apkg.sub` are in `sys.modules`.
12. `test_from_apkg_import_sub(fixtures_on_path)`: `install()`, then `from apkg import sub` — works and `sub` is the submodule.
13. `test_mixed_package_apy_submodule(fixtures_on_path)`: `install()`, then `import mixed.leaf`. The parent package has `__init__.py` (Python), the leaf has `.apy`. Both load and `mixed.leaf` is accessible.

### Module attributes (4)

14. `test_imported_module_has_correct_name(fixtures_on_path)`: after `import standalone`, `standalone.__name__ == "standalone"`.
15. `test_imported_module_has_absolute_file(fixtures_on_path)`: `standalone.__file__` ends with `standalone.apy` and is an absolute path.
16. `test_imported_package_has_path(fixtures_on_path)`: `apkg.__path__` is a list containing the directory holding `__init__.apy`.
17. `test_imported_module_loader_is_apy_loader(fixtures_on_path)`: `standalone.__loader__` is an `ApyLoader` instance.

### Relative imports (2)

18. `test_relative_import_in_apy_package(fixtures_on_path)`: `apkg/__init__.apy` does `from . import sub` (or similar relative import); `import apkg` succeeds and `apkg.sub` is bound. (Implementer: design the fixture content to exercise this.)
19. `test_relative_import_dotted(fixtures_on_path)`: a deeper fixture demonstrates `from .sibling import name` working across two `.apy` siblings in the same package. Skip if it requires creating more than one extra fixture file beyond what's already specified — in that case implement test 18 only and document the skip in the delivery note.

### Caching and reload (3)

20. `test_import_uses_sys_modules_cache(fixtures_on_path)`: import `standalone` twice; the second call returns the same object (Python's normal import behavior). Verify by `id()`.
21. `test_importlib_reload_re_executes(fixtures_on_path)`: after `import standalone`, modify the source file's contents (write a different value to a constant), then `importlib.reload(standalone)`, assert the new value is observed. (Restore the file in a `try/finally` to keep the fixture pristine.)
22. `test_no_pycache_for_apy(fixtures_on_path, tmp_path)`: copy the standalone fixture into `tmp_path`, add `tmp_path` to `sys.path`, import it, assert no `__pycache__` directory was created in `tmp_path`. Confirms we don't accidentally generate bytecode caches.

### Error handling (5)

23. `test_apy_with_bidi_raises_syntax_error(tmp_path)`: write an `.apy` file containing U+202E in `tmp_path`, add to sys.path, attempt to import it — `SyntaxError` (not `ImportError`) is raised, message mentions `bidi control`, and `e.filename` is the file path.
24. `test_apy_with_translated_python_syntax_error(tmp_path)`: write an `.apy` file whose translated Python is invalid (e.g. `إذا صحيح:` with no body) — import raises `SyntaxError` with `filename` set to the file path.
25. `test_apy_runtime_error_in_module_import(tmp_path)`: write an `.apy` file that raises `ZeroDivisionError` at module top level; import raises `ZeroDivisionError` (not wrapped). The traceback shows the `.apy` filename.
26. `test_unreadable_apy_raises_import_error(tmp_path, monkeypatch)`: simulate a file-vanished-between-find-and-exec scenario by monkeypatching `open` to raise `FileNotFoundError` during `exec_module`; assert `ImportError` is raised. (Or skip via `@pytest.mark.skipif(sys.platform == "win32", ...)` if the monkeypatch interferes with Windows file handling — document in delivery note.)
27. `test_non_utf8_apy_raises_import_error(tmp_path)`: write a file with invalid UTF-8 bytes named `bad.apy`, add to sys.path, attempt import → `ImportError` mentioning encoding/decoding.

### Search order and edge cases (3)

28. `test_apy_wins_over_py_when_both_present(tmp_path)`: create both `foo.apy` and `foo.py` in `tmp_path` with distinguishing markers; `install()` then `import foo`; assert the `.apy` version loaded (check the marker).
29. `test_apy_does_not_shadow_stdlib(tmp_path)`: confirm `import os` still loads stdlib `os` after `install()`. (Trivial but proves the position-0 insertion is safe by construction.)
30. `test_get_source_returns_original_apy(fixtures_on_path)`: after `import standalone`, `standalone.__loader__.get_source("standalone")` returns the original Arabic source text (containing at least one Arabic character from the fixture).

### CLI integration (1)

31. `test_cli_installs_hook(tmp_path, capsys)`: write a tiny `main.apy` that does `import helper` (also in `tmp_path`), and `helper.apy` defines a function the main calls. Use `monkeypatch` to add `tmp_path` to `sys.path` (since the CLI doesn't auto-prepend the script dir in v1). Call `cli.main([str(main_apy)])`, assert exit 0 and expected output. This test confirms `install()` runs before exec.

(31 tests total. Implementer: if test 19 is skipped per the spec's permission, that's 30 — note in the delivery checklist.)

## Reference materials

- `decisions/0001-architecture.md`
- `decisions/0002-file-extension.md`
- `decisions/0007-scope.md`
- Python `importlib` docs: https://docs.python.org/3/library/importlib.html
- `importlib.abc.MetaPathFinder`: https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder
- `importlib.abc.Loader`: https://docs.python.org/3/library/importlib.html#importlib.abc.Loader
- `importlib.util.spec_from_file_location`: https://docs.python.org/3/library/importlib.html#importlib.util.spec_from_file_location
- zhpy3's import hook for inspiration (different API, same idea): https://github.com/gasolin/zhpy/tree/master/zhpy3

## Open questions for the planner

None expected. If you hit a real ambiguity — e.g., `importlib.util.spec_from_file_location` doesn't behave the way the spec assumes on some Python version, or the relative-import test 18 needs a different fixture shape than what's described — flag it in the delivery note with a concrete diagnosis rather than guessing.

## Acceptance checklist

- [ ] `arabicpython/import_hook.py` created with `ApyFinder`, `ApyLoader`, `install()`, `uninstall()`.
- [ ] `arabicpython/__init__.py` re-exports `install`, `uninstall`.
- [ ] `arabicpython/cli.py` calls `install()` at the start of `main()` (one new line plus a lazy import).
- [ ] `tests/test_import_hook.py` created with all 30 (or 31) tests.
- [ ] Fixture files under `tests/fixtures/` created as listed.
- [ ] `pytest` (full suite, including pre-existing 226 tests) passes on Python 3.11, 3.12, 3.13.
- [ ] `ruff check .` clean; `black --check .` clean.
- [ ] No new dependencies in `pyproject.toml`.
- [ ] CI green across all 9 matrix cells.
- [ ] After installing locally (`pip install -e .`), a two-file `.apy` example where one imports the other runs via `apython main.apy` (with the imported file's directory on `PYTHONPATH`).
- [ ] `specs/0007-import-hook-v1.delivery.md` written covering shipped behavior, deviations, implementation notes, open questions.

## Workflow for the implementer

1. Create branch `packet/0007-import-hook-v1` from `main`.
2. Implement `arabicpython/import_hook.py`. Get tests 1–4 (install/uninstall) passing first; they exercise no fixtures.
3. Create the fixture files. Make their content boring and obvious — each fixture exists to be checked by ONE specific test.
4. Implement `find_spec` and `exec_module`. Get tests 5–17 passing.
5. Add the `cli.py` change and the `__init__.py` re-export.
6. Add the relative-import fixtures and tests 18–19. If 19 needs more fixtures than the spec describes, skip it and note in delivery.
7. Add caching, reload, and error tests.
8. Run `pytest` (full suite) until green.
9. Run `ruff check .` and `black --check .` until clean. **Do not push without running both.**
10. Optionally `pip install -e .` and try a real two-file Arabic program to gut-check.
11. Commit. Suggested message: `Packet 0007: implement .apy import hook`.
12. Push.
13. Write `specs/0007-import-hook-v1.delivery.md`.
14. Open a PR titled `Packet 0007: import-hook-v1` linking back to this spec.
15. Wait for CI green, then planner review.

## Allowed edit scope

- `arabicpython/import_hook.py` (new)
- `arabicpython/__init__.py` (one re-export line at the bottom)
- `arabicpython/cli.py` (lazy import + one `install()` call at top of `main()`)
- `tests/test_import_hook.py` (new)
- `tests/fixtures/**/*.apy` and `tests/fixtures/mixed/__init__.py` (new)
- `specs/0007-import-hook-v1.delivery.md` (new)

Do NOT modify: any other module, any ADR, the dictionary, `pyproject.toml`, the CI workflow, or other existing tests. If you believe the spec has a bug, flag it in the delivery note rather than silently deviating.
