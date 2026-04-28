# B-061 Delivery Note — Error-Message Coverage Audit

**Status:** delivered  
**Date:** 2026-04-28  
**Implementer:** Claude  

---

## Summary

Audited `MESSAGE_TEMPLATES_AR` in `arabicpython/tracebacks.py` against 97 real
CPython error messages spanning all major exception types. Found 37 gaps (38.1%
untranslated). Added templates for all gaps. Final coverage: **97/97 (100%)**.

---

## Audit methodology

1. Wrote `tools/b061_audit.py` — a test harness that runs 97 representative
   CPython error-message strings through `translate_exception_message()` and
   reports hits vs misses.
2. Ran the audit, collected 37 misses.
3. Added regex + Arabic template pairs to `MESSAGE_TEMPLATES_AR`, keeping
   the broad KeyError catch-all last.
4. Re-ran audit: 0 misses.
5. Ran `python -m black` + `python -m ruff check` — clean.
6. Ran `pytest tests/test_tracebacks.py` — 95/95 pass.
7. Ran full suite — 1765 pass, 354 skip (all skips expected).

---

## Templates added (37)

### ZeroDivisionError (2)
| Pattern | Arabic |
|---------|--------|
| `float modulo` | باقي قسمة عشرية على صفر |
| `complex division by zero` | قسمة عدد مركب على صفر |

### AttributeError — module variants (2)
| Pattern | Arabic |
|---------|--------|
| `module 'X' has no attribute 'Y'` | الوحدة 'X' لا تملك الخاصية 'Y' |
| `module 'X' has no attribute 'Y'. Did you mean: 'Z'?` | الوحدة 'X' لا تملك الخاصية 'Y'. هل تقصد: 'Z'؟ |

### TypeError — new variants (9)
| Pattern | Arabic |
|---------|--------|
| `func() got multiple values for argument 'x'` | func() استلمت قيماً متعددة للوسيط 'x' |
| `bad operand type for unary OP: 'type'` | نوع معامل خاطئ للعملية الأحادية OP: 'type' |
| `'type' object does not support item assignment` | الكائن من نوع 'type' لا يدعم تعيين العناصر |
| `'type' object doesn't support item assignment/deletion` | الكائن من نوع 'type' لا يدعم … العناصر |
| `can't multiply sequence by non-int of type 'type'` | لا يمكن ضرب المتسلسلة بنوع غير صحيح 'type' |
| `expected str, bytes or os.PathLike object, not type` | متوقع نص أو بايتات أو مسار، ليس 'type' |
| `descriptor 'X' for 'Y' objects doesn't apply to a 'Z' object` | الواصف 'X' لكائنات 'Y' لا ينطبق على كائن 'Z' |

### ValueError — new variants (6)
| Pattern | Arabic |
|---------|--------|
| `substring not found` | النص الفرعي غير موجود |
| `list.remove(x): x not found` | list.remove(x): العنصر غير موجود في القائمة |
| `I/O operation on closed file.` | عملية إدخال/إخراج على ملف مغلق |
| `Circular reference detected` | تم اكتشاف مرجع دائري |
| `empty separator` | الفاصل فارغ |
| `dictionary update sequence element #N has length M; 2 is required` | عنصر تسلسل تحديث القاموس رقم N له طول M؛ المطلوب 2 |

### IndexError — new variants (3)
| Pattern | Arabic |
|---------|--------|
| `pop index out of range` | فهرس الإخراج خارج النطاق |
| `bytearray index out of range` | فهرس مصفوفة البايت خارج النطاق |
| `range object index out of range` | فهرس كائن النطاق خارج النطاق |

### ImportError — new variants (2)
| Pattern | Arabic |
|---------|--------|
| `attempted relative import with no known parent package` | محاولة استيراد نسبي دون وجود حزمة أصلية معروفة |
| `cannot import name 'X' from partially initialized module 'Y'` | لا يمكن استيراد الاسم 'X' من الوحدة المُهيَّأة جزئياً 'Y' (على الأرجح بسبب استيراد دائري) |

### OverflowError (1)
| Pattern | Arabic |
|---------|--------|
| `(34, 'Result too large')` | خطأ عملية: Result too large |

### RuntimeError (3)
| Pattern | Arabic |
|---------|--------|
| `dictionary changed size during iteration` | تغيّر حجم القاموس أثناء التكرار |
| `Set changed size during iteration` | تغيّر حجم المجموعة أثناء التكرار |
| `asynchronous generator raised StopIteration` | المولّد غير المتزامن أطلق ايقاف_التكرار |

### SyntaxError — new variants (9)
| Pattern | Arabic |
|---------|--------|
| `invalid syntax` | صياغة غير صالحة |
| `invalid syntax. Perhaps you forgot a comma?` | صياغة غير صالحة. ربما نسيت فاصلة؟ |
| `unterminated string literal (detected at line N)` | نص حرفي غير منتهٍ (اكتُشف في السطر N) |
| `EOL while scanning string literal` | نهاية السطر أثناء فحص نص حرفي |
| `unexpected EOF while parsing` | نهاية ملف غير متوقعة أثناء التحليل |
| `unexpected character after line continuation character` | حرف غير متوقع بعد حرف استمرار السطر |
| `invalid character 'X' (U+XXXX)` | حرف غير صالح 'X' (U+XXXX) |
| `Missing parentheses in call to 'print'. Did you mean print(...)?` | أقواس مفقودة في استدعاء 'print'. هل تقصد print(...)؟ |
| `f-string expression part cannot include a backslash` | جزء تعبير النص المنسق لا يمكن أن يحتوي على شرطة مائلة عكسية |

### Connection errors (2)
| Pattern | Arabic |
|---------|--------|
| `Connection timed out` | انتهت مهلة الاتصال |
| `timed out` | انتهت المهلة |

---

## Files changed

- `arabicpython/tracebacks.py` — 37 new `(re.Pattern, str)` entries in `MESSAGE_TEMPLATES_AR`
- `tools/b061_audit.py` — new audit harness (97 test cases)
- `specs/B-061-errormsg.delivery.md` — this file

---

## Coverage report

| Exception type | Probed | Covered | Gap |
|---|---|---|---|
| ZeroDivisionError | 5 | 5 | 0 |
| NameError / UnboundLocalError | 5 | 5 | 0 |
| AttributeError | 6 | 6 | 0 |
| TypeError | 22 | 22 | 0 |
| ValueError | 11 | 11 | 0 |
| IndexError | 6 | 6 | 0 |
| KeyError | 1 | 1 | 0 |
| ImportError | 4 | 4 | 0 |
| OverflowError | 3 | 3 | 0 |
| RecursionError | 2 | 2 | 0 |
| RuntimeError | 5 | 5 | 0 |
| SyntaxError / IndentationError | 12 | 12 | 0 |
| StopIteration | 1 | 1 | 0 |
| OSError / FileNotFoundError | 3 | 3 | 0 |
| Connection errors | 5 | 5 | 0 |
| Unicode errors | 4 | 4 | 0 |
| **Total** | **97** | **97** | **0** |

**Coverage: 100%**
