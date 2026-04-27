# Handoff Brief — B-012 (Django) + B-013 (SQLAlchemy) Alias Packets

**To**: Collaborating Claude Code agent  
**Project**: lughat-althuban / arabicpython — Arabic Python dialect  
**Repo**: https://github.com/GalaxyRuler/lughat-althuban  
**Date**: 2026-04-27  
**Packet IDs**: B-012, B-013  

---

## What this project is

`arabicpython` is a Python dialect that lets Arabic speakers write Python using Arabic
keywords and identifiers. A `.apy` file is translated to Python at import/run time. An
Arabic programmer writes:

```python
استورد فلاسك
تطبيق = فلاسك.قارورة(__name__)

@تطبيق.مسار('/')
دالة رئيسية():
    ارجع 'مرحبا'
```

…and it runs as valid Python. Your job is to add Arabic aliases for **Django** and
**SQLAlchemy** so the same programmer can build a full Django/SQLAlchemy app in Arabic.

---

## Codebase layout (repo root)

```
arabicpython/
  aliases/
    _finder.py          ← AliasFinder: loads all *.toml files on import
    _proxy.py           ← ModuleProxy: wraps real module, normalizes attr lookup
    numpy.toml          ← reference implementation — read this first
    pandas.toml         ← reference implementation — read this too
    flask.toml          ← reference: shows how SDK aliases are done
    ...                 ← one .toml per aliased library
  normalize.py          ← normalize_identifier() — CRITICAL, read this
  dialect.py            ← ar-v1/v2 dictionary loader
dictionaries/
  ar-v1.md              ← locked base dictionary (187 entries)
  ar-v2.md              ← current active dictionary (188+ entries)
tests/
  aliases/
    test_numpy.py       ← reference test file — mirror this structure
    test_pandas.py      ← reference test file
    test_stdlib_B016_B017_cross_consistency.py  ← cross-batch collision tests
specs/
  B-040-dictionary-v1.1-async-match.md  ← example spec for reference
ROADMAP-PHASE-B.md      ← status of all packets
```

---

## The alias TOML format

Every library gets one file: `arabicpython/aliases/<name>.toml`

```toml
# arabicpython/aliases/django.toml
[meta]
arabic_name   = "دجانغو"        # the Arabic import name (import دجانغو)
python_module = "django"          # the real Python module
dict_version  = "ar-v1"
schema_version = 1
maintainer    = "—"

[entries]
"نموذج"        = "Model"           # Arabic key = Python attribute
"حقل_نصي"     = "CharField"
"هجره"         = "migrations"
```

**Rules for `[entries]` keys:**
- Keys are Arabic strings that users type as attributes: `دجانغو.نموذج`
- Values are Python attribute names on the real module
- For submodule access, use dotted paths: `"نموذج" = "db.models.Model"`
- Keys **must** already be in normalized form (see Normalization below)
- The loader validates this at startup and silently skips the whole file if
  any key fails — you will get zero entries with no error message, so verify

---

## Normalization — THE most common failure mode

`arabicpython/normalize.py` applies these transforms to every key at load time:

1. NFKC normalization
2. Strip harakat (tashkeel) and tatweel
3. **أ / إ / آ → ا** (hamza on alef folds to bare alef — anywhere in the word)
4. **final ى → ي** (alef maqsura → yeh)
5. **final ة → ه** (ta marbuta → heh)

**What this means for your TOML keys:**

| You write | Normalizes to | Problem? |
|---|---|---|
| `"مصفوفة"` | `"مصفوفه"` | YES — store as `"مصفوفه"` |
| `"مدى"` | `"مدي"` | YES — store as `"مدي"` |
| `"إطار"` | `"اطار"` | YES — store as `"اطار"` |
| `"أساسي"` | `"اساسي"` | YES — store as `"اساسي"` |
| `"نموذج"` | `"نموذج"` | OK |
| `"هجره"` | `"هجره"` | OK (ه is already the normalized form) |

**Verify every key before you write it:**

```python
from arabicpython.normalize import normalize_identifier
word = "إطار_بيانات"
assert normalize_identifier(word) == word, f"Bad: {normalize_identifier(word)!r}"
```

Or batch-check a whole candidate list:

```python
candidates = ["نموذج", "هجره", "إطار"]  # your draft terms
for c in candidates:
    normed = normalize_identifier(c)
    if normed != c:
        print(f"FIX: {c!r} → {normed!r}")
    else:
        print(f"OK:  {c!r}")
```

---

## How to verify your TOML loads correctly

The AliasFinder silently swallows load errors, so always call the loader directly:

```python
from arabicpython.aliases._loader import load_mapping
from pathlib import Path

mapping = load_mapping(Path("arabicpython/aliases/django.toml"))
print(f"Loaded {len(mapping)} entries")
# If 0 entries → normalization error in one of your keys
```

Or load via the full finder to confirm the import name works:

```python
from arabicpython.aliases._finder import AliasFinder
from pathlib import Path

finder = AliasFinder(mappings_dir=Path("arabicpython/aliases"))
spec = finder.find_spec("دجانغو", None, None)
assert spec is not None, "TOML not found or failed to load"
proxy = spec.loader.create_module(spec)
print(f"Entries: {len(proxy._mapping)}")
print(f"Sample: {list(proxy._mapping.items())[:5]}")
```

---

## Collision checking — mandatory before finalising any key

There are **786 existing Arabic keys** across all alias modules plus **~196 dialect
keywords** (ar-v2). Your keys must not collide with any of them.

Run this script to check a candidate list:

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

candidates = [
    "نموذج", "هجره", "مسار_رابط",   # your draft terms here
]

for term in candidates:
    in_alias = all_alias_keys.get(term, [])
    in_dialect = term in d.names or term in d.attributes
    if in_alias or in_dialect:
        print(f"TAKEN: {term!r}  alias:{in_alias}  dialect:{in_dialect}")
    else:
        print(f"free:  {term!r}")
```

---

## Known collisions you will hit — resolved here so you don't waste time

The following obvious Arabic choices for Django/SQLAlchemy are **already taken**.
Use the suggested alternatives:

| Concept | Obvious Arabic | Why taken | Use instead |
|---|---|---|---|
| `path()` URL | `مسار` | pathlib module | `مسار_رابط` |
| `filter()` queryset | `فلتر` | `filter` builtin (ar-v2) | `رشح` |
| `.get()` queryset | `اجلب` | dict `.get` method (ar-v2) | `اجلب_كائن` |
| `all()` queryset | `كل` | `all` builtin (ar-v2) | `استرجع_الكل` |
| `delete()` | `احذف` | `del` keyword + Flask/requests | `احذف_كائن` |
| `update()` queryset | `حدث` | asyncio + dict `.update` | `حدث_كائنات` |
| Django `Session` / SQLAlchemy `Session` | `جلسه` | Flask + requests | `جلسه_قاعده` |
| Django `request` object | `طلب` | Flask + requests | `طلب_ويب` |
| Django `redirect()` | `حول` | Flask | `اعد_توجيه` |
| Django `render()` | `صيغ` | Flask `render_template` | `اعرض_قالب` |
| Django `HttpResponse` | `استجابه` | requests `Response` | `استجابه_http` |
| SQLAlchemy `select()` | `اختر` | random `choice` | `اختر_من` |
| SQLAlchemy `Filter` | `مرشح` | logging `Filter` | `مرشح_استعلام` |

---

## B-012 scope — Django core

**Arabic import name**: `دجانغو`  
**Python module**: `django`  
**Target**: `arabicpython/aliases/django.toml`

Cover these surfaces (suggested groupings for the TOML comments):

### URL routing (`django.urls`)
`path`, `re_path`, `include`, `reverse`, `reverse_lazy`

### HTTP objects (`django.http`)
`HttpResponse`, `HttpResponseRedirect`, `HttpResponseNotFound`,
`JsonResponse`, `FileResponse`, `Http404`, `StreamingHttpResponse`

### Shortcuts (`django.shortcuts`)
`render`, `redirect`, `get_object_or_404`, `get_list_or_404`

### Views — function-based (`django.views`)
`View`, `TemplateView`

### Views — generic class-based (`django.views.generic`)
`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`,
`FormView`, `TemplateView`, `RedirectView`

### Models (`django.db.models`)
`Model`, `Manager`, `QuerySet`,
`CharField`, `TextField`, `IntegerField`, `FloatField`, `BooleanField`,
`DateField`, `DateTimeField`, `TimeField`,
`EmailField`, `URLField`, `SlugField`, `UUIDField`, `FileField`, `ImageField`,
`ForeignKey`, `OneToOneField`, `ManyToManyField`,
`CASCADE`, `PROTECT`, `SET_NULL`, `DO_NOTHING`,
`Q`, `F`, `Value`, `ExpressionWrapper`,
`Count`, `Sum`, `Avg`, `Max`, `Min`

### Forms (`django.forms`)
`Form`, `ModelForm`,
`CharField` (forms version — use a suffix like `حقل_نصي_نموذج`),
`IntegerField`, `EmailField`, `ChoiceField`, `MultipleChoiceField`,
`BooleanField`, `DateField`, `FileField`

### Settings / apps (`django.conf`, `django.apps`)
`settings`, `AppConfig`

### Exceptions (`django.core.exceptions`)
`ObjectDoesNotExist`, `MultipleObjectsReturned`,
`ValidationError`, `PermissionDenied`, `ImproperlyConfigured`

### Signals (`django.db.models.signals`)
`pre_save`, `post_save`, `pre_delete`, `post_delete`

### Middleware / WSGI
`WSGIHandler`, `get_wsgi_application`

---

## B-013 scope — SQLAlchemy

**Arabic import name**: `قاعده_علائقيه`  
**Python module**: `sqlalchemy`  
**Target**: `arabicpython/aliases/sqlalchemy.toml`

### Engine & connection (`sqlalchemy`)
`create_engine`, `text`, `URL`, `make_url`, `inspect`

### Session (`sqlalchemy.orm`)
`Session`, `sessionmaker`, `scoped_session`

### ORM base & mapping (`sqlalchemy.orm`)
`DeclarativeBase`, `MappedColumn`, `mapped_column`, `relationship`,
`backref`, `Mapped`, `registry`

### Column types (`sqlalchemy`)
`Column`, `Integer`, `String`, `Float`, `Boolean`,
`Date`, `DateTime`, `Time`, `Text`,
`ForeignKey`, `PrimaryKeyConstraint`, `UniqueConstraint`, `Index`

### Query API (`sqlalchemy`)
`select`, `insert`, `update`, `delete`,
`and_`, `or_`, `not_`, `func`, `case`, `cast`, `literal`, `label`

### ORM query helpers (`sqlalchemy.orm`)
`Query`, `joinedload`, `subqueryload`, `selectinload`,
`contains_eager`, `defer`, `undefer`

### Result objects
`Row`, `Result`, `ScalarResult`, `CursorResult`

### Exceptions (`sqlalchemy.exc`)
`SQLAlchemyError`, `IntegrityError`, `OperationalError`,
`NoResultFound`, `MultipleResultsFound`

---

## Test file structure

Create two test files mirroring the pattern in `tests/aliases/test_numpy.py`:

```
tests/aliases/test_django.py
tests/aliases/test_sqlalchemy.py
tests/aliases/test_stdlib_B012_B013_cross_consistency.py
```

### Fixture pattern (copy from test_numpy.py)

```python
import pytest
import django   # real library
from pathlib import Path

ALIASES_DIR = Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

@pytest.fixture(scope="module")
def دجانغو():
    from arabicpython.aliases._finder import AliasFinder
    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("دجانغو", None, None)
    assert spec is not None, "AliasFinder did not find 'دجانغو'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy
```

### Test class pattern

```python
class TestDjangoModels:
    def test_model_alias(self, دجانغو):
        from django.db import models
        assert دجانغو.نموذج is models.Model

    def test_charfield_alias(self, دجانغو):
        from django.db.models import CharField
        assert دجانغو.حقل_نصي is CharField
```

### Cross-consistency test

`test_stdlib_B012_B013_cross_consistency.py` must parametrize against ALL earlier
module Arabic names (see the existing `test_stdlib_B016_B017_cross_consistency.py`
for the exact pattern — copy it and add "دجانغو" and "قاعده_علائقيه" to `NEW_MODULES`
and add all B-016/B-017 modules to `EARLIER_MODULES`).

---

## Important behavioural notes

### Proxy attribute lookup is exact (no normalization on access)

The proxy does NOT normalize attribute names when you write `دجانغو.نموذج`. It does a
direct dictionary lookup. So if your TOML key is `"نموذج"` and the user types
`دجانغو.نموذج` (exact same string), it works. If the user types `دجانغو.نَموذج`
(with haraka), the CLI normalizes identifiers before lookup — but only in source code
translation, not at the interactive attribute-access level.

**Implication for tests**: use the exact normalized form in your test assertions:

```python
assert دجانغو.نموذج is django.db.models.Model   # OK
assert دجانغو.نَموذج is django.db.models.Model  # WRONG — will AttributeError
```

### Dotted module paths in entry values

If the Python attribute lives on a submodule, use a dotted path as the value:

```toml
"نموذج"      = "db.models.Model"         # django.db.models.Model
"حقل_نصي"   = "db.models.CharField"
"رشح"        = "db.models.Q"             # for Q-object filtering
```

The proxy resolves these by walking `getattr` on the wrapped module.

### Django requires setup before importing models

In test files, add a `conftest.py` or module-level setup:

```python
import django
from django.conf import settings

def pytest_configure():
    if not settings.configured:
        settings.configure(
            DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3",
                                   "NAME": ":memory:"}},
            INSTALLED_APPS=["django.contrib.contenttypes", "django.contrib.auth"],
        )
```

---

## Quality bar before submitting a PR

**Run this before every commit — CI will fail if you skip it:**

```bash
python -m black .
python -m ruff check .
```

Black is a non-negotiable CI gate. Ruff enforces no unused imports and no ambiguous
variable names (e.g. don't use `l`, `O`, or `I` as variable names — ruff E741).
Fix any violations before pushing; the CI pipeline rejects unformatted code in all
9 matrix cells (3 OS × 3 Python versions).

Then verify the tests:

1. `python -m pytest tests/aliases/test_django.py tests/aliases/test_sqlalchemy.py tests/aliases/test_stdlib_B012_B013_cross_consistency.py -q` — all green
2. `python -m pytest tests/ -q --ignore=tests/aliases/test_django.py --ignore=tests/aliases/test_sqlalchemy.py --ignore=tests/aliases/test_stdlib_B012_B013_cross_consistency.py` — nothing broken in the existing suite
3. Every TOML key round-trips: `normalize_identifier(key) == key` for every key
4. Zero cross-batch collisions: the cross-consistency test covers this

---

## Reference files to read before starting

In order:

1. `arabicpython/aliases/numpy.toml` — canonical TOML format
2. `tests/aliases/test_numpy.py` — canonical test structure
3. `tests/aliases/test_stdlib_B016_B017_cross_consistency.py` — cross-batch collision test
4. `arabicpython/normalize.py` — understand the normalization pipeline
5. `arabicpython/aliases/flask.toml` — how an SDK alias handles submodule paths
6. `ROADMAP-PHASE-B.md` — context on where this fits

---

## When you're done

Update `ROADMAP-PHASE-B.md`: flip B-012 and B-013 from `stub` to `merged`.

Commit message format (match the existing style):

```
B-012/B-013: aliases — django (N entries) and sqlalchemy (M entries)
```

Open a PR against `main`. The existing CI runs `pytest tests/` — your new tests
will be picked up automatically.

---

## Questions / coordination

This project is coordinated by the repo owner. If you hit a collision that isn't
covered above, or you're unsure about an Arabic term choice, open a draft PR with
a comment explaining the options. Do not guess on Arabic term choices where two
reasonable options exist — document the choice and the rationale rejected.
