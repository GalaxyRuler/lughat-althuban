# Exception Name Cross-File Audit — ar-v1

**Date**: 2026-04-20  
**Author**: audit script (Claude Code)  
**Status**: research only — no files changed  
**Scope**: `dictionaries/ar-v1.md` (§5 Built-in exceptions) vs `dictionaries/exceptions-ar-v1.md` (§ Exception Type Names)  
**Governance note**: Any correction requires ar-v2 + ADR per ADR 0003 and ADR 0008 §B.0. This document is evidence for that future ADR.

---

## Summary

| Category | Count |
|---|---|
| Entries in ar-v1 | 40 |
| Entries in exceptions-ar-v1 | 38 |
| In both files, names **match** | 20 |
| In both files, names **mismatch** | 15 |
| Only in ar-v1 (missing from exceptions) | 5 |
| Only in exceptions (missing from ar-v1) | 3 |

**15 mismatches** — more than the 8 reported at audit-start. 7 additional discrepancies found: `Exception`, `EOFError`, `FileExistsError`, `FileNotFoundError`, `FloatingPointError`, `ModuleNotFoundError`, `TimeoutError`.

---

## Full Side-by-Side Comparison

Sorted alphabetically by Python name. Status codes:

- `✓ MATCH` — identical in both files (after visible-form comparison; normalizer may further fold these)
- `✗ MISMATCH` — both files have an entry, but the Arabic differs
- `ar-v1 only` — entry exists in ar-v1 but is absent from exceptions-ar-v1
- `exc only` — entry exists in exceptions-ar-v1 but is absent from ar-v1

| Python | ar-v1 canonical | exceptions Arabic | Status |
|---|---|---|---|
| `ArithmeticError` | `خطأ_حسابي` | `خطأ_حسابي` | ✓ MATCH |
| `AssertionError` | `خطأ_تأكيد` | `خطأ_تأكيد` | ✓ MATCH |
| `AttributeError` | `خطأ_صفة` | `خطأ_خاصية` | ✗ MISMATCH |
| `BaseException` | `استثناء_أساسي` | `استثناء_أساسي` | ✓ MATCH |
| `BlockingIOError` | *(absent)* | `خطأ_إدخال_إخراج_حاجب` | exc only |
| `ConnectionError` | `خطأ_اتصال` | *(absent)* | ar-v1 only |
| `EOFError` | `خطأ_نهاية_ملف` | `خطأ_نهاية_الملف` | ✗ MISMATCH |
| `Exception` | `استثناء_عام` | `استثناء` | ✗ MISMATCH |
| `FileExistsError` | `خطأ_ملف_موجود` | `خطأ_الملف_موجود` | ✗ MISMATCH |
| `FileNotFoundError` | `خطأ_ملف_مفقود` | `خطأ_الملف_غير_موجود` | ✗ MISMATCH |
| `FloatingPointError` | `خطأ_عشري` | `خطأ_فاصلة_عائمة` | ✗ MISMATCH |
| `GeneratorExit` | `خروج_مولد` | *(absent)* | ar-v1 only |
| `ImportError` | `خطأ_استيراد` | `خطأ_استيراد` | ✓ MATCH |
| `IndentationError` | `خطأ_إزاحة` | `خطأ_إزاحة` | ✓ MATCH |
| `IndexError` | `خطأ_فهرس` | `خطأ_فهرس` | ✓ MATCH |
| `IOError` | `خطأ_إدخال_إخراج` | *(absent)* | ar-v1 only |
| `IsADirectoryError` | *(absent)* | `خطأ_هذا_مجلد` | exc only |
| `KeyboardInterrupt` | `مقاطعة` | `مقاطعة_لوحة_المفاتيح` | ✗ MISMATCH |
| `KeyError` | `خطأ_مفتاح` | `خطأ_مفتاح` | ✓ MATCH |
| `LookupError` | `خطأ_بحث` | `خطأ_بحث` | ✓ MATCH |
| `MemoryError` | `خطأ_ذاكرة` | `خطأ_ذاكرة` | ✓ MATCH |
| `ModuleNotFoundError` | `خطأ_وحدة_مفقودة` | `خطأ_الوحدة_غير_موجودة` | ✗ MISMATCH |
| `NameError` | `خطأ_اسم` | `خطأ_اسم` | ✓ MATCH |
| `NotADirectoryError` | *(absent)* | `خطأ_ليس_مجلدا` | exc only |
| `NotImplementedError` | `خطأ_غير_منفذ` | `خطأ_غير_منفذ` | ✓ MATCH |
| `OSError` | `خطأ_نظام` | `خطأ_نظام` | ✓ MATCH |
| `OverflowError` | `خطأ_فائض` | `خطأ_فيضان` | ✗ MISMATCH |
| `PermissionError` | `خطأ_صلاحية` | `خطأ_صلاحيات` | ✗ MISMATCH |
| `RecursionError` | `خطأ_تكرار_ذاتي` | `خطأ_عودية` | ✗ MISMATCH |
| `RuntimeError` | `خطأ_تشغيل` | `خطأ_تشغيل` | ✓ MATCH |
| `StopIteration` | `انتهاء_التكرار` | `إيقاف_التكرار` | ✗ MISMATCH |
| `SyntaxError` | `خطأ_صياغة` | `خطأ_صياغة` | ✓ MATCH |
| `SystemError` | `خطأ_نظام_داخلي` | *(absent)* | ar-v1 only |
| `SystemExit` | `خروج_نظام` | `خروج_نظام` | ✓ MATCH |
| `TabError` | `خطأ_جدولة` | `خطأ_تبويب` | ✗ MISMATCH |
| `TimeoutError` | `خطأ_انتهاء_وقت` | `خطأ_انتهاء_مهلة` | ✗ MISMATCH |
| `TypeError` | `خطأ_نوع` | `خطأ_نوع` | ✓ MATCH |
| `UnicodeDecodeError` | `خطأ_فك_يونيكود` | `خطأ_فك_يونيكود` | ✓ MATCH |
| `UnicodeEncodeError` | `خطأ_ترميز_يونيكود` | `خطأ_ترميز_يونيكود` | ✓ MATCH |
| `UnicodeError` | `خطأ_يونيكود` | `خطأ_يونيكود` | ✓ MATCH |
| `ValueError` | `خطأ_قيمة` | `خطأ_قيمة` | ✓ MATCH |
| `Warning` | `تحذير` | *(absent)* | ar-v1 only |
| `ZeroDivisionError` | `خطأ_قسمة_صفر` | `خطأ_القسمة_على_صفر` | ✗ MISMATCH |

---

## Mismatches — Detail

### Previously known (8)

| Python | ar-v1 | exceptions | Nature of divergence |
|---|---|---|---|
| `AttributeError` | `خطأ_صفة` | `خطأ_خاصية` | Different root word: صفة (attribute/adjective) vs خاصية (property) |
| `KeyboardInterrupt` | `مقاطعة` | `مقاطعة_لوحة_المفاتيح` | ar-v1 is bare noun; exceptions adds full compound "keyboard interruption" |
| `OverflowError` | `خطأ_فائض` | `خطأ_فيضان` | Same root (ف و ض), different noun form: فائض (surplus/overflow adj) vs فيضان (flood/overflow noun) |
| `PermissionError` | `خطأ_صلاحية` | `خطأ_صلاحيات` | Singular vs plural of صلاحية (permission) |
| `RecursionError` | `خطأ_تكرار_ذاتي` | `خطأ_عودية` | Different concept: تكرار_ذاتي (self-repetition) vs عودية (recursion, the CS term) |
| `StopIteration` | `انتهاء_التكرار` | `إيقاف_التكرار` | انتهاء (ending/expiry) vs إيقاف (stopping/halting); hamza variant also differs |
| `TabError` | `خطأ_جدولة` | `خطأ_تبويب` | جدولة (scheduling/tabulation) vs تبويب (tabbing, the typographic act) |
| `ZeroDivisionError` | `خطأ_قسمة_صفر` | `خطأ_القسمة_على_صفر` | ar-v1 elides article and preposition; exceptions has full definite-article form with على |

### Newly identified (7)

| Python | ar-v1 | exceptions | Nature of divergence |
|---|---|---|---|
| `Exception` | `استثناء_عام` | `استثناء` | ar-v1 adds عام (general) to avoid collision with the `except` keyword; exceptions uses the bare noun. ar-v1 rationale is documented inline: bare `استثناء` collides with the `except` keyword translation. |
| `EOFError` | `خطأ_نهاية_ملف` | `خطأ_نهاية_الملف` | Presence vs absence of the definite article ال on ملف (file). |
| `FileExistsError` | `خطأ_ملف_موجود` | `خطأ_الملف_موجود` | Same: ال article on ملف. |
| `FileNotFoundError` | `خطأ_ملف_مفقود` | `خطأ_الملف_غير_موجود` | Completely different phrasing: مفقود (missing) vs غير_موجود (not found/not present). Also ال article. |
| `FloatingPointError` | `خطأ_عشري` | `خطأ_فاصلة_عائمة` | ar-v1 uses a shorthand (decimal/floating); exceptions uses a full technical compound (floating-point separator). |
| `ModuleNotFoundError` | `خطأ_وحدة_مفقودة` | `خطأ_الوحدة_غير_موجودة` | Same pattern as FileNotFoundError: مفقودة (missing) vs غير_موجودة (not found), plus ال article. |
| `TimeoutError` | `خطأ_انتهاء_وقت` | `خطأ_انتهاء_مهلة` | وقت (time, general) vs مهلة (deadline/time-limit); both are defensible but semantically distinct. |

---

## Coverage gaps

### In ar-v1 but absent from exceptions-ar-v1 (5)

These exception types are translatable by user code but will show an untranslated Python name in tracebacks:

| Python | ar-v1 canonical | Priority note |
|---|---|---|
| `ConnectionError` | `خطأ_اتصال` | Parent of several networking errors; high user visibility |
| `GeneratorExit` | `خروج_مولد` | Raised internally; low user visibility |
| `IOError` | `خطأ_إدخال_إخراج` | Alias for OSError in Python 3; lower priority |
| `SystemError` | `خطأ_نظام_داخلي` | Interpreter-internal; low user visibility |
| `Warning` | `تحذير` | Base class only; low traceback frequency |

### In exceptions-ar-v1 but absent from ar-v1 (3)

These appear in traceback output but cannot be typed in source code (no keyword/name entry):

| Python | exceptions Arabic | Priority note |
|---|---|---|
| `BlockingIOError` | `خطأ_إدخال_إخراج_حاجب` | OSError subclass; moderate frequency in async code |
| `IsADirectoryError` | `خطأ_هذا_مجلد` | OSError subclass; common in file-handling code |
| `NotADirectoryError` | `خطأ_ليس_مجلدا` | OSError subclass; common in file-handling code |

---

## Observations for ar-v2 authors

1. **The `Exception` / `except` keyword collision** is ar-v1's most structurally important divergence. ar-v1 deliberately chose `استثناء_عام` to avoid shadowing the `except` keyword translation (`استثناء`). The exceptions file uses bare `استثناء`. Whichever is authoritative for tracebacks must be consistent with the keyword table — this is not a simple rename.

2. **Definite-article pattern** (`ملف` vs `الملف`, `وحدة` vs `الوحدة`): the exceptions file systematically adds ال to noun phrases in compound error names. ar-v1 systematically omits it. Both are grammatically valid; ar-v2 should pick one rule and apply it uniformly across all compound names.

3. **Short vs descriptive** (`خطأ_عشري` vs `خطأ_فاصلة_عائمة`, `مقاطعة` vs `مقاطعة_لوحة_المفاتيح`): ar-v1 favors terse forms; exceptions favors fuller descriptive forms. This is a style decision that ar-v2 should resolve with an explicit rule.

4. **Root-word disagreements** (`صفة` vs `خاصية`, `تكرار_ذاتي` vs `عودية`, `فائض` vs `فيضان`): these are semantic/lexical choices that may require community input, as both sides have pedagogical merit.

5. **Missing entries**: ar-v2 should extend both files to cover the same set of exceptions. The 3 OSError subclasses in exceptions but absent from ar-v1 (`BlockingIOError`, `IsADirectoryError`, `NotADirectoryError`) are worth adding to the canonical dictionary given their frequency.

---

## File metadata at time of audit

| File | Declared status | Exception entry count |
|---|---|---|
| `dictionaries/ar-v1.md` | locked (ar-v1.0), 2026-04-19 | 40 |
| `dictionaries/exceptions-ar-v1.md` | no version/lock declaration | 38 |
