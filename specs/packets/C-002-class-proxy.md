# C-002 — ClassProxy (Implementation Prompt)

**Blocks:** C-010, C-011, C-012, C-013, C-018, C-020, C-021, C-024, C-025  
**Depends on:** C-001 ✅  
**Size:** M  

---

## Task

Implement C-002 — ClassProxy runtime for lughat-althuban

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: specs/C-001-pypi-release-v1.delivery.md, arabicpython/aliases/_loader.py,
            arabicpython/aliases/_proxy.py, arabicpython/aliases/flask.toml

Goal: Arabic attribute names must work on *instances* of library objects, not just
on modules. After C-002, this must work:

    from فلاسك import طلب
    if طلب.طريقه == "GET":   # request.method

## Architecture

1. Extend AliasMapping dataclass (_loader.py) with a new field:
       attributes: dict[str, str]   # Arabic attr → Python attr
   Parse it from an [attributes] TOML section (same format as [entries]).
   The section is optional — loaders must not fail if absent.

2. Add ClassProxy class (arabicpython/aliases/_proxy.py):
   - Wraps any object instance
   - __getattr__(arabic_name):
       a. Look up arabic_name in the mapping's `attributes` dict
       b. If found: return getattr(wrapped_obj, python_name)
       c. If not found: return getattr(wrapped_obj, arabic_name) — fall through
          so normal Python names still work
   - __setattr__, __delattr__: forward to wrapped object
   - Do NOT intercept dunders (__len__, __iter__, etc.) — Python bypasses
     __getattr__ for dunders anyway; ClassProxy must not break isinstance,
     pickling, comparison, or iteration
   - isinstance(proxy, OriginalClass) must return True — implement via
     __class__ property returning type(wrapped_obj)

3. ModuleProxy integration (_proxy.py): when a module-level name resolves
   to a class that appears in proxy_classes (already tracked in AliasMapping),
   wrap the returned instance in ClassProxy automatically.
   The call site: فلاسك.طلب  →  ClassProxy(flask.request, mapping)

4. Add [attributes] sections to flask.toml and requests.toml as the
   canonical test cases. At minimum implement:

   flask.toml [attributes]:
   "طريقه"            = "method"
   "وسيطات_الطلب"     = "args"
   "نموذج"            = "form"
   "بيانات_json"      = "json"
   "ترويسات"          = "headers"
   "كوكيز"            = "cookies"
   "ملفات"            = "files"
   "رابط"             = "url"
   "مسار"             = "path"
   "اجلب_json"        = "get_json"
   "رمز_الحاله"       = "status_code"
   "بيانات"           = "data"

   requests.toml [attributes]:
   "رمز_الحاله"       = "status_code"
   "نص"               = "text"
   "بيانات_json"      = "json"
   "محتوي"            = "content"
   "ترويسات"          = "headers"
   "رابط"             = "url"
   "ناجح"             = "ok"
   "ارفع_للحاله"      = "raise_for_status"

5. Tests (tests/test_class_proxy.py):
   - ClassProxy forwards Arabic attribute access to the real object
   - isinstance(proxy, OriginalClass) is True
   - Dunders work (len, iter, repr) without wrapping
   - Unknown Arabic attrs fall through to real attr (no AttributeError for valid attrs)
   - [attributes] section in TOML is parsed correctly
   - Flask request.method accessible as طلب.طريقه in an integration test
     using Flask test_request_context

## Constraints

- Zero new dependencies
- Python 3.11+ only
- Do not break any existing tests (2570+ currently passing)
- The [attributes] TOML section must be optional so all existing TOMLs
  remain valid without modification
