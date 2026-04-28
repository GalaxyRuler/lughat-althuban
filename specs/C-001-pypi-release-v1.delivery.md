# C-001 Delivery Note — pypi-release-v1

**Packet:** C-001  
**Status:** delivered  
**Delivered:** 2026-04-28  
**Owner:** Claude  

---

## What was done

### 1. Package renamed: `apython` → `lughat-althuban`

`pyproject.toml` updated:
- `name = "lughat-althuban"`
- `version = "0.3.0"`
- Full classifier list (Development Status :: 4 - Beta, Python 3.11–3.13, etc.)
- `[project.urls]` — Homepage, Documentation, Repository, Changelog, Bug Tracker
- `[project.optional-dependencies]` — `dev`, `kernel`, `all` extras
- `[tool.setuptools.package-data]` — TOML alias files, dictionary `.md` files, kernel `.json` files

### 2. Version bump

`arabicpython/__init__.py`: `__version__ = "0.3.0"`

### 3. Dictionary files moved inside the package

`arabicpython/dictionaries/` now contains `ar-v1.md`, `ar-v1.1.md`, `ar-v2.md`,
`exceptions-ar-v1.md`, and `__init__.py`. `dialect.py` path fixed:
`Path(__file__).parent / "dictionaries"` (works in both editable and installed mode).

### 4. GitHub Actions publish workflow

`.github/workflows/publish.yml` — triggered on `v*` tags:
- `build` job: `python -m build` → uploads `dist/` artifact
- `publish` job: `pypa/gh-action-pypi-publish@release/v1` with OIDC trusted publishing (no stored API token)

### 5. CHANGELOG.md

`## [0.3.0] — 2026-04-28` section written covering all Phase A + B features.

---

## Manual steps required (maintainer)

Before pushing the `v0.3.0` tag, the repository owner must configure PyPI trusted publishing:

1. Create the project on [pypi.org](https://pypi.org) (first release only — name `lughat-althuban`).
2. Go to **Manage project → Publishing → Add a new publisher**.
3. Fill in:
   - **Owner:** `GalaxyRuler`
   - **Repository:** `lughat-althuban`
   - **Workflow:** `publish.yml`
   - **Environment:** `pypi`
4. On GitHub, create the `pypi` **Environment** (repo Settings → Environments → New environment → `pypi`).
5. Push the tag: `git tag v0.3.0 && git push origin v0.3.0`

The workflow triggers automatically and publishes `lughat-althuban==0.3.0` to PyPI.

---

## Verification checklist

- [x] `python -m build` produces `dist/lughat_althuban-0.3.0-py3-none-any.whl` and `.tar.gz`
- [x] `pip install dist/lughat_althuban-0.3.0-py3-none-any.whl` installs without error
- [x] `from arabicpython import __version__; assert __version__ == "0.3.0"`
- [x] `import arabicpython.aliases.مصفوفات` resolves (package data included in wheel)
- [x] `ثعبان --help` works after install
- [x] `publish.yml` references `pypa/gh-action-pypi-publish@release/v1` (OIDC, no token)
