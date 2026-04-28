# Audit Fixes — Make Example Files Fully Arabic (Implementation Prompt)

**Depends on:** C-001 ✅  
**Note:** Do NOT add [attributes] sections — those require C-002.

---

## Task

Make all example .apy files fully Arabic and add missing [entries] to alias TOMLs.

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/dictionaries/ar-v1.md (keyword reference),
            arabicpython/aliases/flask.toml (TOML format reference),
            examples/ directory (all .apy files)

---

## PART 1: Fix example .apy files

Replace every English identifier that already has an Arabic alias.

examples/B01_http.apy:
  headers.get(...)  →  headers.اجلب(...)

examples/B31_functional_data.apy:
  .append  →  .اضف

examples/B33_data_storage.apy:
  io.StringIO  →  مجاري.تيار_نص
  False        →  خطأ
  list(...)    →  قائمة(...)
  len(...)     →  طول(...)

examples/B35_numerics.apy:
  round(...)              →  قرب(...)
  list(...), range(...), sorted(...)  →  قائمة, نطاق, مرتب

examples/B36_logging_demo.apy:
  io.StringIO        →  مجاري.تيار_نص
  .strip().split()   →  .جرد().قسم()

examples/B37_async_demo.apy:
  return       →  ارجع
  range(...)   →  نطاق(...)
  .get         →  .اجلب
  .append      →  .اضف
  sorted(...)  →  مرتب(...)
  len(...)     →  طول(...)

examples/B38_utilities_demo.apy:
  .strip().split()   →  .جرد().قسم()
  ZeroDivisionError  →  خطأ_قسمة_صفر

examples/B40_async_demo.apy:
  asyncio.sleep      →  اتزامن.تريث
  asyncio.gather     →  اتزامن.اجمع_مهام
  asyncio.run        →  اتزامن.شغل
  range(...)         →  نطاق(...)

examples/B57_seaborn_demo.apy:
  ImportError  →  خطأ_استيراد

examples/B59_aiohttp_demo.apy:
  str(...)        →  نص(...)
  dict(...)       →  قاموس(...)
  Exception       →  استثناء_عام
  asyncio.run     →  اتزامن.شغل
  .get            →  .اجلب

examples/اختبار_نموذجي.apy:
  pytest.raises    →  بايتست.يثير
  pytest.fixture   →  بايتست.مثبت
  max(...)         →  الأكبر(...)
  min(...)         →  الأصغر(...)
  sum(...)         →  مجموع(...)
  .upper()         →  .كبير()
  ZeroDivisionError / TypeError in except clauses  →  خطأ_قسمة_صفر / خطأ_نوع

---

## PART 2: Add missing [entries] to alias TOML files

asyncio.toml — add:
  "تريث"         = "sleep"
  "اجمع_مهام"    = "gather"
  "شغل"          = "run"

numpy.toml — add:
  "قرب"          = "round"
  "جيب"          = "sin"
  "جيب_تمام"     = "cos"
  "ظل"           = "tan"
  "باي"          = "pi"

---

## PART 3: Add missing entries to ar-v1.md dictionary

Built-in functions — add:
  aiter  →  مكرر_غير_متزامن
  anext  →  التالي_غير_متزامن

Built-in exceptions — add:
  ExceptionGroup       →  مجموعة_استثناءات
  BaseExceptionGroup   →  مجموعة_استثناءات_اساسيه
  UnboundLocalError    →  خطأ_متغير_محلي

String methods (section 6) — add:
  .rstrip  →  جرد_يمين
  .lstrip  →  جرد_يسار

---

## Constraints

- Run full test suite after: pytest tests/ -x
- Do not add [attributes] sections (C-002 work)
- Do not change List C items: "GET", "POST", protocol strings, proper nouns
- Each .apy file must still execute correctly after changes
