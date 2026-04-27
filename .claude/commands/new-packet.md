# arabicpython — New Alias Packet Guide

You are implementing a new alias packet for the **arabicpython / lughat-althuban** project.
Read this entire guide before writing a single line. It contains everything you need —
the architecture, the rules, the failure modes, and the quality gate.

---

## What this project is

`arabicpython` lets Arabic speakers write Python using Arabic keywords and identifiers.
A `.apy` file is translated to Python at import/run time. An Arabic programmer writes:

```python
استورد فلاسك
تطبيق = فلاسك.قارورة(__name__)

@تطبيق.مسار('/')
دالة رئيسية():
    ارجع 'مرحبا'
```

…and it runs as valid Python. An **alias packet** is a `.toml` file that maps Arabic
attribute names onto a real Python library, so `import نمباي` works like `import numpy`.

---

## Repo layout (relevant paths)

```
arabicpython/
  aliases/
    _finder.py       ← AliasFinder: loads all *.toml files on import
    _proxy.py        ← ModuleProxy: wraps real module, does dict lookup on attr access
    numpy.toml       ← reference implementation — read this first
    pandas.toml      ← reference implementation — read this too
    flask.toml       ← shows how SDK submodule paths work
  normalize.py       ← normalize_identifier() — CRITICAL, read this
  dialect.py         ← ar-v1/v2 dictionary loader
dictionaries/
  ar-v2.md           ← current active dictionary (~196 dialect keywords)
tests/aliases/
  test_numpy.py      ← reference test file — mirror this structure exactly
  test_pandas.py     ← reference test file
  test_stdlib_B016_B017_cross_consistency.py  ← cross-batch collision test pattern
ROADMAP-PHASE-B.md  ← flip your packet from stub → merged when done
specs/              ← handoff briefs for each packet (read yours before starting)
```

---

## Step 1 — Read the reference files

In this order:

1. `arabicpython/aliases/numpy.toml` — canonical TOML format
2. `tests/aliases/test_numpy.py` — canonical test structure
3. `arabicpython/normalize.py` — understand the normalization pipeline
4. `arabicpython/aliases/flask.toml` — how dotted submodule paths work
5. The spec for your specific packet in `specs/`

---

## Step 2 — The TOML format

Every library gets one file: `arabicpython/aliases/<name>.toml`

```toml
[meta]
arabic_name    = "نمباي"          # the Arabic import name
python_module  = "numpy"          # the real Python module
dict_version   = "ar-v1"
schema_version = 1
maintainer     = "—"

[entries]
"مصفوفه"     = "array"            # Arabic key = Python attribute
"مصفوفه_صفر" = "zeros"
"متوسط"      = "mean"
```

Rules:
- Keys are what users type as attributes: `نمباي.مصفوفه`
- Values are Python attribute names on the real module
- For submodule attributes use dotted paths: `"نموذج" = "db.models.Model"`
- Keys **must** be in normalized form (see Step 3)
- The loader silently returns 0 entries on any key error — verify after writing

---

## Step 3 — Normalization (most common failure mode)

`normalize_identifier()` applies these transforms to every identifier at runtime:

1. NFKC normalization
2. Strip harakat (tashkeel) and tatweel
3. **أ / إ / آ → ا** (hamza on alef → bare alef, anywhere in word)
4. **final ى → ي** (alef maqsura → yeh)
5. **final ة → ه** (ta marbuta → heh)

Your TOML keys must **already be in the normalized form** — otherwise the loader
silently drops the whole file with zero entries and no error message.

| You might write | Normalizes to | Store as |
|---|---|---|
| `"مصفوفة"` | `"مصفوفه"` | `"مصفوفه"` ✓ |
| `"مدى"` | `"مدي"` | `"مدي"` ✓ |
| `"إطار"` | `"اطار"` | `"اطار"` ✓ |
| `"أساسي"` | `"اساسي"` | `"اساسي"` ✓ |
| `"نموذج"` | `"نموذج"` | `"نموذج"` ✓ |

**Verify every key before writing the TOML:**

```python
from arabicpython.normalize import normalize_identifier

candidates = ["إطار_بيانات", "مصفوفة", "مدى", "أساسي"]
for c in candidates:
    normed = normalize_identifier(c)
    if normed != c:
        print(f"FIX: {c!r} → {normed!r}")
    else:
        print(f"OK:  {c!r}")
```

---

## Step 4 — Verify the TOML loads

The AliasFinder silently swallows load errors. Always verify directly:

```python
from arabicpython.aliases._loader import load_mapping
from pathlib import Path

mapping = load_mapping(Path("arabicpython/aliases/yourmodule.toml"))
print(f"Loaded {len(mapping)} entries")
# 0 entries = normalization error in one of your keys
```

Or via the full finder:

```python
from arabicpython.aliases._finder import AliasFinder
from pathlib import Path

finder = AliasFinder(mappings_dir=Path("arabicpython/aliases"))
spec = finder.find_spec("عربي_اسم_الاستيراد", None, None)
assert spec is not None, "TOML not found or failed to load"
proxy = spec.loader.create_module(spec)
print(f"Entries: {len(proxy._mapping)}")
print(list(proxy._mapping.items())[:5])
```

---

## Step 5 — Collision checking (mandatory)

Your keys must not collide with the ~786 existing alias keys or the ~196 dialect
keywords in ar-v2. Run this before finalising any key:

```python
import sys, pathlib, tomllib
sys.stdout.reconfigure(encoding='utf-8')
from arabicpython.dialect import load_dialect

ALIASES_DIR = pathlib.Path("arabicpython/aliases")
d = load_dialect("ar-v2")

all_alias_keys = {}
for toml in sorted(ALIASES_DIR.glob("*.toml")):
    data = tomllib.loads(toml.read_text(encoding="utf-8"))
    for k in data.get("entries", {}):
        all_alias_keys.setdefault(k, []).append(toml.stem)

candidates = ["نموذج", "مسار", "رشح"]   # ← your draft terms
for term in candidates:
    in_alias = all_alias_keys.get(term, [])
    in_dialect = term in d.names or term in d.attributes
    if in_alias or in_dialect:
        print(f"TAKEN: {term!r}  alias:{in_alias}  dialect:{in_dialect}")
    else:
        print(f"free:  {term!r}")
```

---

## Step 6 — Test file structure

Create three files following the pattern in `tests/aliases/test_numpy.py`:

```
tests/aliases/test_<yourmodule>.py
tests/aliases/test_<yourmodule2>.py          (if doing two packets)
tests/aliases/test_stdlib_B0XX_cross_consistency.py
```

### Fixture pattern

```python
import pytest
ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

@pytest.fixture(scope="module")
def عربي_اسم():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("عربي_اسم", None, None)
    assert spec is not None, "AliasFinder did not find 'عربي_اسم'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy
```

### Test class pattern

```python
class TestModuleCore:
    def test_some_alias(self, عربي_اسم):
        import realmodule
        assert عربي_اسم.عربي_مفتاح is realmodule.PythonAttr
```

**Critical**: Use the exact normalized form in test assertions. The proxy does NOT
normalize on attribute access — `proxy.نَموذج` (with haraka) will AttributeError,
even if your TOML key is `"نموذج"`.

### Cross-consistency test

Copy `tests/aliases/test_stdlib_B016_B017_cross_consistency.py`, update:
- `NEW_MODULES` = your new Arabic module names
- `EARLIER_MODULES` = all previous batch module names (add to the existing list)

---

## Step 7 — Quality gate (run before EVERY commit)

**This is mandatory. CI rejects any unformatted or lint-failing code across all 9
matrix cells (macOS/Ubuntu/Windows × Python 3.11/3.12/3.13).**

```bash
python -m black .
python -m ruff check .
```

Fix all violations before committing. Common ruff traps:
- `F401` — unused import (remove it)
- `E741` — ambiguous variable name (`l`, `O`, `I`) — rename to something descriptive

Then run the full test suite:

```bash
python -m pytest tests/ -q
```

---

## Step 8 — Commit and PR

Commit message format (match the existing style):

```
B-0XX/B-0YY: aliases — modulename (N entries) and othermodule (M entries)
```

Flip your packet(s) in `ROADMAP-PHASE-B.md` from `stub` → `merged`.

Open a PR against `main`. CI runs automatically. If CI fails on your PR:
- Black failure → run `python -m black .` and push
- Ruff failure → fix the flagged lines and push
- Test failure → read the traceback; 99% of the time it's a normalization issue

---

## Behavioural notes

### Proxy lookup is exact

`proxy.مفتاح` does a direct dict lookup — no normalization at access time. Your test
assertions must use the exact same string as the TOML key.

### Dotted submodule paths

```toml
"نموذج"    = "db.models.Model"        # resolves django.db.models.Model
"حقل_نصي" = "db.models.CharField"
```

The proxy walks `getattr` on the wrapped module for each dot segment.

### AliasFinder is silent on failure

If your TOML has a bad key (un-normalized, typo, duplicate), the entire file loads
with 0 entries and no exception is raised. Always check `len(proxy._mapping) > 0`.

---

## Reference: key common collisions

These obvious Arabic words are already taken across earlier packets or the dialect:

| Concept | Obvious term | Taken by | Use instead |
|---|---|---|---|
| `path` | `مسار` | pathlib | `مسار_رابط` |
| `filter` | `فلتر` / `رشح` | builtin ar-v2 | `رشح_نتائج` or suffix |
| `session` | `جلسه` | Flask / requests | `جلسه_قاعده` |
| `request` | `طلب` | Flask / requests | `طلب_ويب` |
| `all()` | `كل` | builtin ar-v2 | `استرجع_الكل` |
| `select` | `اختر` | random | `اختر_من` |
| `delete` | `احذف` | Flask + del keyword | `احذف_كائن` |
| `update` | `حدث` | asyncio + dict | `حدث_كائنات` |

When in doubt, run the collision checker in Step 5.
