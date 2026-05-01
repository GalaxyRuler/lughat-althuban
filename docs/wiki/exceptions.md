<div dir="rtl">

# الاستثناءات — Exceptions Reference

هذه القائمة الكاملة للاستثناءات القياسية في لغة الثعبان. جميع الأسماء تتبع نمط `خطأ_وصف` (خطأ + وصف المشكلة بالعربية).

> **ملاحظة:** عند رفع استثناء أو التقاطه، استخدم الاسم العربي كما هو موضح هنا. المترجم يستبدله بالاسم الإنجليزي قبل تنفيذ الكود.

---

## هرمية الاستثناءات

```
استثناء_أساسي          ← BaseException
├── خروج_نظام         ← SystemExit
├── مقاطعه            ← KeyboardInterrupt
├── خروج_مولد         ← GeneratorExit
└── استثناء_عام       ← Exception
    ├── خطأ_حسابي     ← ArithmeticError
    │   ├── خطأ_عشري  ← FloatingPointError
    │   ├── خطأ_فائض  ← OverflowError
    │   └── خطأ_قسمة_صفر ← ZeroDivisionError
    ├── خطأ_صفه       ← AttributeError
    ├── خطأ_استيراد   ← ImportError
    │   └── خطأ_وحده_مفقوده ← ModuleNotFoundError
    ├── خطأ_بحث       ← LookupError
    │   ├── خطأ_فهرس  ← IndexError
    │   └── خطأ_مفتاح ← KeyError
    ├── خطأ_ذاكره     ← MemoryError
    ├── خطأ_اسم       ← NameError
    │   └── خطأ_متغير_غير_معرف ← UnboundLocalError
    ├── خطأ_نظام      ← OSError  (= IOError)
    │   ├── خطأ_ملف_موجود ← FileExistsError
    │   ├── خطأ_ملف_مفقود ← FileNotFoundError
    │   ├── خطأ_انقطاع ← BrokenPipeError
    │   ├── خطأ_صلاحيه ← PermissionError
    │   ├── خطأ_انتهاء_وقت ← TimeoutError
    │   └── خطأ_اتصال ← ConnectionError
    ├── خطأ_تشغيل     ← RuntimeError
    │   ├── خطأ_عودية ← RecursionError
    │   └── خطأ_غير_منفذ ← NotImplementedError
    ├── خطأ_صياغه     ← SyntaxError
    │   ├── خطأ_ازاحه ← IndentationError
    │   └── خطأ_جدولة ← TabError
    ├── خطأ_نوع       ← TypeError
    ├── خطأ_يونيكود   ← UnicodeError
    │   ├── خطأ_فك_يونيكود ← UnicodeDecodeError
    │   ├── خطأ_ترميز_يونيكود ← UnicodeEncodeError
    │   └── خطأ_ترجمه_يونيكود ← UnicodeTranslateError
    ├── خطأ_قيمة      ← ValueError
    ├── خطأ_نهايه_ملف ← EOFError
    ├── خطأ_نظام_داخلي ← SystemError
    ├── انتهاء_التكرار ← StopIteration
    ├── انتهاء_التكرار_غير_المتزامن ← StopAsyncIteration
    └── تحذير         ← Warning
        ├── تحذير_إهمال ← DeprecationWarning
        ├── تحذير_وقت_تشغيل ← RuntimeWarning
        ├── تحذير_مستخدم ← UserWarning
        └── تحذير_بناء_جمله ← SyntaxWarning
```

---

## الجدول الكامل

| Python | العربية | الوصف |
|--------|---------|--------|
| `BaseException` | `استثناء_أساسي` | جذر هرمية الاستثناءات |
| `Exception` | `استثناء_عام` | الاستثناء العام القابل للالتقاط |
| `ArithmeticError` | `خطأ_حسابي` | أساس أخطاء الحساب |
| `AssertionError` | `خطأ_تاكيد` | فشل جملة `تحقق` |
| `AttributeError` | `خطأ_صفه` | وصف خاصية غير موجودة |
| `BlockingIOError` | `خطأ_ادخال_اخراج_محجوب` | عملية I/O محجوبة |
| `BrokenPipeError` | `خطأ_انبوب_مكسور` | الكتابة على أنبوب مغلق |
| `BufferError` | `خطأ_مخزن` | خطأ في المخزن المؤقت |
| `ChildProcessError` | `خطأ_عمليه_فرعيه` | فشل عملية فرعية |
| `ConnectionAbortedError` | `خطأ_اتصال_منقطع` | اتصال مُقطع |
| `ConnectionError` | `خطأ_اتصال` | أساس أخطاء الاتصال |
| `ConnectionRefusedError` | `خطأ_اتصال_مرفوض` | اتصال مرفوض |
| `ConnectionResetError` | `خطأ_اتصال_مُعاد_ضبطه` | اتصال مُعاد ضبطه |
| `EOFError` | `خطأ_نهايه_ملف` | قراءة ما بعد نهاية الملف |
| `EnvironmentError` | `خطأ_بيئه` | مرادف OSError |
| `FileExistsError` | `خطأ_ملف_موجود` | إنشاء ملف موجود مسبقاً |
| `FileNotFoundError` | `خطأ_ملف_مفقود` | الملف غير موجود |
| `FloatingPointError` | `خطأ_عشري` | خطأ في الأعداد العشرية |
| `GeneratorExit` | `خروج_مولد` | إغلاق المولد |
| `IOError` | `خطأ_نظام` | مرادف OSError |
| `ImportError` | `خطأ_استيراد` | فشل الاستيراد |
| `IndentationError` | `خطأ_ازاحه` | خطأ في المسافة البادئة |
| `IndexError` | `خطأ_فهرس` | الفهرس خارج النطاق |
| `InterruptedError` | `خطأ_مقاطعه` | استدعاء نظام مُقاطَع |
| `IsADirectoryError` | `خطأ_هذا_مجلد` | طُلب ملف لكنه مجلد |
| `KeyError` | `خطأ_مفتاح` | المفتاح غير موجود في القاموس |
| `KeyboardInterrupt` | `مقاطعه` | Ctrl+C |
| `LookupError` | `خطأ_بحث` | أساس أخطاء البحث |
| `MemoryError` | `خطأ_ذاكره` | نفاد الذاكرة |
| `ModuleNotFoundError` | `خطأ_وحده_مفقوده` | الوحدة غير موجودة |
| `NameError` | `خطأ_اسم` | اسم غير معرَّف |
| `NotADirectoryError` | `خطأ_ليس_مجلدا` | مجلد مطلوب لكن المسار ملف |
| `NotImplementedError` | `خطأ_غير_منفذ` | دالة مجردة غير مُنفَّذة |
| `OSError` | `خطأ_نظام` | خطأ نظام التشغيل |
| `OverflowError` | `خطأ_فائض` | الرقم أكبر مما يمكن تمثيله |
| `PermissionError` | `خطأ_صلاحيه` | صلاحيات غير كافية |
| `ProcessLookupError` | `خطأ_بحث_عمليه` | العملية غير موجودة |
| `RecursionError` | `خطأ_عودية` | تجاوز حد العودية |
| `ReferenceError` | `خطأ_مرجع` | مرجع ضعيف إلى كائن محذوف |
| `RuntimeError` | `خطأ_تشغيل` | خطأ عام أثناء التشغيل |
| `StopAsyncIteration` | `انتهاء_التكرار_غير_المتزامن` | توقف المكرر غير المتزامن |
| `StopIteration` | `انتهاء_التكرار` | توقف المكرر |
| `SyntaxError` | `خطأ_صياغه` | خطأ في بناء الجملة |
| `SystemError` | `خطأ_نظام_داخلي` | خطأ داخلي في مفسر Python |
| `SystemExit` | `خروج_نظام` | خروج مطلوب |
| `TabError` | `خطأ_جدولة` | خلط بين المسافات والجداول |
| `TimeoutError` | `خطأ_انتهاء_وقت` | انتهاء وقت العملية |
| `TypeError` | `خطأ_نوع` | نوع بيانات خاطئ |
| `UnboundLocalError` | `خطأ_متغير_غير_معرف` | متغير محلي غير مُسنَد |
| `UnicodeDecodeError` | `خطأ_فك_يونيكود` | فشل فك ترميز Unicode |
| `UnicodeEncodeError` | `خطأ_ترميز_يونيكود` | فشل ترميز Unicode |
| `UnicodeError` | `خطأ_يونيكود` | أساس أخطاء Unicode |
| `UnicodeTranslateError` | `خطأ_ترجمه_يونيكود` | فشل ترجمة Unicode |
| `ValueError` | `خطأ_قيمة` | قيمة غير صالحة لهذا النوع |
| `Warning` | `تحذير` | أساس التحذيرات |
| `ZeroDivisionError` | `خطأ_قسمة_صفر` | قسمة على صفر |

---

## التحذيرات

| Python | العربية |
|--------|---------|
| `DeprecationWarning` | `تحذير_إهمال` |
| `FutureWarning` | `تحذير_مستقبلي` |
| `PendingDeprecationWarning` | `تحذير_إهمال_قادم` |
| `ResourceWarning` | `تحذير_موارد` |
| `RuntimeWarning` | `تحذير_وقت_تشغيل` |
| `SyntaxWarning` | `تحذير_بناء_جمله` |
| `UnicodeWarning` | `تحذير_يونيكود` |
| `UserWarning` | `تحذير_مستخدم` |

---

## أمثلة

### رفع والتقاط الاستثناءات

```python
دالة قسم(أ, ب):
    حاول:
        ارجع أ / ب
    استثناء خطأ_قسمة_صفر:
        اطبع("خطأ: القسمة على صفر غير مسموحة!")
        ارجع لا_شيء

اطبع(قسم(10, 2))   # 5.0
اطبع(قسم(10, 0))   # خطأ: القسمة على صفر...
```

### رفع استثناء مخصص

```python
صنف خطأ_كلمة_مرور(استثناء_عام):
    دالة __init__(ذات, رسالة="كلمة المرور ضعيفة"):
        الأصل().__init__(رسالة)

دالة تحقق_كلمه_مرور(كلمه):
    اذا طول(كلمه) < 8:
        ارفع خطأ_كلمة_مرور(f"كلمة المرور '{كلمه}' قصيرة جداً")

حاول:
    تحقق_كلمه_مرور("123")
استثناء خطأ_كلمة_مرور باسم خ:
    اطبع(f"فشل التحقق: {خ}")
```

### معالجة الملفات

```python
حاول:
    مع افتح("بيانات.txt", encoding="utf-8") باسم ملف:
        محتوى = ملف.read()
استثناء خطأ_ملف_مفقود:
    اطبع("الملف غير موجود!")
استثناء خطأ_صلاحيه:
    اطبع("لا تملك صلاحية القراءة!")
اخيرا:
    اطبع("انتهت محاولة فتح الملف.")
```

### التحقق من المدخلات

```python
دالة اقرا_عدد():
    طالما صحيح:
        حاول:
            نص_مدخل = ادخل("أدخل رقماً: ")
            ارجع عدد_صحيح(نص_مدخل)
        استثناء خطأ_قيمة:
            اطبع("إدخال غير صالح، أدخل رقماً صحيحاً.")

رقم = اقرا_عدد()
اطبع(f"أدخلت: {رقم}")
```

</div>

---

# Exceptions Reference (English summary)

All standard Python exceptions are available under Arabic names following the pattern `خطأ_description`. The full hierarchy and table are in the Arabic section above.

Common exceptions quick lookup:

| Python | Arabic |
|--------|--------|
| `Exception` | `استثناء_عام` |
| `ValueError` | `خطأ_قيمة` |
| `TypeError` | `خطأ_نوع` |
| `KeyError` | `خطأ_مفتاح` |
| `IndexError` | `خطأ_فهرس` |
| `AttributeError` | `خطأ_صفه` |
| `ImportError` | `خطأ_استيراد` |
| `FileNotFoundError` | `خطأ_ملف_مفقود` |
| `PermissionError` | `خطأ_صلاحيه` |
| `ZeroDivisionError` | `خطأ_قسمة_صفر` |
| `RuntimeError` | `خطأ_تشغيل` |
| `SyntaxError` | `خطأ_صياغه` |
| `StopIteration` | `انتهاء_التكرار` |
| `KeyboardInterrupt` | `مقاطعه` |
| `SystemExit` | `خروج_نظام` |
