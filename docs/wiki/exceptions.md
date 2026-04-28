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
    ├── خطا_حسابي     ← ArithmeticError
    │   ├── خطا_عشري  ← FloatingPointError
    │   ├── خطا_فائض  ← OverflowError
    │   └── خطا_قسمه_صفر ← ZeroDivisionError
    ├── خطا_صفه       ← AttributeError
    ├── خطا_استيراد   ← ImportError
    │   └── خطا_وحده_مفقوده ← ModuleNotFoundError
    ├── خطا_بحث       ← LookupError
    │   ├── خطا_فهرس  ← IndexError
    │   └── خطا_مفتاح ← KeyError
    ├── خطا_ذاكره     ← MemoryError
    ├── خطا_اسم       ← NameError
    │   └── خطا_متغير_غير_معرف ← UnboundLocalError
    ├── خطا_نظام      ← OSError  (= IOError)
    │   ├── خطا_ملف_موجود ← FileExistsError
    │   ├── خطا_ملف_مفقود ← FileNotFoundError
    │   ├── خطا_انقطاع ← BrokenPipeError
    │   ├── خطا_صلاحيه ← PermissionError
    │   ├── خطا_انتهاء_وقت ← TimeoutError
    │   └── خطا_اتصال ← ConnectionError
    ├── خطا_تشغيل     ← RuntimeError
    │   ├── خطا_تكرار_ذاتي ← RecursionError
    │   └── خطا_غير_منفذ ← NotImplementedError
    ├── خطا_صياغه     ← SyntaxError
    │   ├── خطا_ازاحه ← IndentationError
    │   └── خطا_جدوله ← TabError
    ├── خطا_نوع       ← TypeError
    ├── خطا_يونيكود   ← UnicodeError
    │   ├── خطا_فك_يونيكود ← UnicodeDecodeError
    │   ├── خطا_ترميز_يونيكود ← UnicodeEncodeError
    │   └── خطا_ترجمه_يونيكود ← UnicodeTranslateError
    ├── خطا_قيمه      ← ValueError
    ├── خطا_نهايه_ملف ← EOFError
    ├── خطا_نظام_داخلي ← SystemError
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
| `ArithmeticError` | `خطا_حسابي` | أساس أخطاء الحساب |
| `AssertionError` | `خطا_تاكيد` | فشل جملة `تحقق` |
| `AttributeError` | `خطا_صفه` | وصف خاصية غير موجودة |
| `BlockingIOError` | `خطا_ادخال_اخراج_محجوب` | عملية I/O محجوبة |
| `BrokenPipeError` | `خطا_انبوب_مكسور` | الكتابة على أنبوب مغلق |
| `BufferError` | `خطا_مخزن` | خطأ في المخزن المؤقت |
| `ChildProcessError` | `خطا_عمليه_فرعيه` | فشل عملية فرعية |
| `ConnectionAbortedError` | `خطا_اتصال_منقطع` | اتصال مُقطع |
| `ConnectionError` | `خطا_اتصال` | أساس أخطاء الاتصال |
| `ConnectionRefusedError` | `خطا_اتصال_مرفوض` | اتصال مرفوض |
| `ConnectionResetError` | `خطا_اتصال_مُعاد_ضبطه` | اتصال مُعاد ضبطه |
| `EOFError` | `خطا_نهايه_ملف` | قراءة ما بعد نهاية الملف |
| `EnvironmentError` | `خطا_بيئه` | مرادف OSError |
| `FileExistsError` | `خطا_ملف_موجود` | إنشاء ملف موجود مسبقاً |
| `FileNotFoundError` | `خطا_ملف_مفقود` | الملف غير موجود |
| `FloatingPointError` | `خطا_عشري` | خطأ في الأعداد العشرية |
| `GeneratorExit` | `خروج_مولد` | إغلاق المولد |
| `IOError` | `خطا_نظام` | مرادف OSError |
| `ImportError` | `خطا_استيراد` | فشل الاستيراد |
| `IndentationError` | `خطا_ازاحه` | خطأ في المسافة البادئة |
| `IndexError` | `خطا_فهرس` | الفهرس خارج النطاق |
| `InterruptedError` | `خطا_مقاطعه` | استدعاء نظام مُقاطَع |
| `IsADirectoryError` | `خطا_هذا_مجلد` | طُلب ملف لكنه مجلد |
| `KeyError` | `خطا_مفتاح` | المفتاح غير موجود في القاموس |
| `KeyboardInterrupt` | `مقاطعه` | Ctrl+C |
| `LookupError` | `خطا_بحث` | أساس أخطاء البحث |
| `MemoryError` | `خطا_ذاكره` | نفاد الذاكرة |
| `ModuleNotFoundError` | `خطا_وحده_مفقوده` | الوحدة غير موجودة |
| `NameError` | `خطا_اسم` | اسم غير معرَّف |
| `NotADirectoryError` | `خطا_ليس_مجلدا` | مجلد مطلوب لكن المسار ملف |
| `NotImplementedError` | `خطا_غير_منفذ` | دالة مجردة غير مُنفَّذة |
| `OSError` | `خطا_نظام` | خطأ نظام التشغيل |
| `OverflowError` | `خطا_فائض` | الرقم أكبر مما يمكن تمثيله |
| `PermissionError` | `خطا_صلاحيه` | صلاحيات غير كافية |
| `ProcessLookupError` | `خطا_بحث_عمليه` | العملية غير موجودة |
| `RecursionError` | `خطا_تكرار_ذاتي` | تجاوز حد العودية |
| `ReferenceError` | `خطا_مرجع` | مرجع ضعيف إلى كائن محذوف |
| `RuntimeError` | `خطا_تشغيل` | خطأ عام أثناء التشغيل |
| `StopAsyncIteration` | `انتهاء_التكرار_غير_المتزامن` | توقف المكرر غير المتزامن |
| `StopIteration` | `انتهاء_التكرار` | توقف المكرر |
| `SyntaxError` | `خطا_صياغه` | خطأ في بناء الجملة |
| `SystemError` | `خطا_نظام_داخلي` | خطأ داخلي في مفسر Python |
| `SystemExit` | `خروج_نظام` | خروج مطلوب |
| `TabError` | `خطا_جدوله` | خلط بين المسافات والجداول |
| `TimeoutError` | `خطا_انتهاء_وقت` | انتهاء وقت العملية |
| `TypeError` | `خطا_نوع` | نوع بيانات خاطئ |
| `UnboundLocalError` | `خطا_متغير_غير_معرف` | متغير محلي غير مُسنَد |
| `UnicodeDecodeError` | `خطا_فك_يونيكود` | فشل فك ترميز Unicode |
| `UnicodeEncodeError` | `خطا_ترميز_يونيكود` | فشل ترميز Unicode |
| `UnicodeError` | `خطا_يونيكود` | أساس أخطاء Unicode |
| `UnicodeTranslateError` | `خطا_ترجمه_يونيكود` | فشل ترجمة Unicode |
| `ValueError` | `خطا_قيمه` | قيمة غير صالحة لهذا النوع |
| `Warning` | `تحذير` | أساس التحذيرات |
| `ZeroDivisionError` | `خطا_قسمه_صفر` | قسمة على صفر |

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
    استثناء خطا_قسمه_صفر:
        اطبع("خطأ: القسمة على صفر غير مسموحة!")
        ارجع لا_شيء

اطبع(قسم(10, 2))   # 5.0
اطبع(قسم(10, 0))   # خطأ: القسمة على صفر...
```

### رفع استثناء مخصص

```python
صنف خطا_كلمه_مرور(استثناء_عام):
    دالة __init__(ذات, رسالة="كلمة المرور ضعيفة"):
        الأصل().__init__(رسالة)

دالة تحقق_كلمه_مرور(كلمه):
    اذا طول(كلمه) < 8:
        ارفع خطا_كلمه_مرور(f"كلمة المرور '{كلمه}' قصيرة جداً")

حاول:
    تحقق_كلمه_مرور("123")
استثناء خطا_كلمه_مرور كـ خ:
    اطبع(f"فشل التحقق: {خ}")
```

### معالجة الملفات

```python
حاول:
    مع افتح("بيانات.txt", encoding="utf-8") كـ ملف:
        محتوى = ملف.read()
استثناء خطا_ملف_مفقود:
    اطبع("الملف غير موجود!")
استثناء خطا_صلاحيه:
    اطبع("لا تملك صلاحية القراءة!")
اخيرا:
    اطبع("انتهت محاولة فتح الملف.")
```

### التحقق من المدخلات

```python
دالة اقرا_عدد():
    بينما صحيح:
        حاول:
            نص_مدخل = ادخل("أدخل رقماً: ")
            ارجع عدد_صحيح(نص_مدخل)
        استثناء خطا_قيمه:
            اطبع("إدخال غير صالح، أدخل رقماً صحيحاً.")

رقم = اقرا_عدد()
اطبع(f"أدخلت: {رقم}")
```

</div>

---

# Exceptions Reference (English summary)

All standard Python exceptions are available under Arabic names following the pattern `خطا_description`. The full hierarchy and table are in the Arabic section above.

Common exceptions quick lookup:

| Python | Arabic |
|--------|--------|
| `Exception` | `استثناء_عام` |
| `ValueError` | `خطا_قيمه` |
| `TypeError` | `خطا_نوع` |
| `KeyError` | `خطا_مفتاح` |
| `IndexError` | `خطا_فهرس` |
| `AttributeError` | `خطا_صفه` |
| `ImportError` | `خطا_استيراد` |
| `FileNotFoundError` | `خطا_ملف_مفقود` |
| `PermissionError` | `خطا_صلاحيه` |
| `ZeroDivisionError` | `خطا_قسمه_صفر` |
| `RuntimeError` | `خطا_تشغيل` |
| `SyntaxError` | `خطا_صياغه` |
| `StopIteration` | `انتهاء_التكرار` |
| `KeyboardInterrupt` | `مقاطعه` |
| `SystemExit` | `خروج_نظام` |
