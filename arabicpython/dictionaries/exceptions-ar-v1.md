# Arabic Exception Dictionary — exceptions-ar-v1

This document lists the translated exception type names and message templates used by the `arabicpython.tracebacks` module.

## Exception Type Names

### Base Hierarchy

| Python | Arabic |
|---|---|
| `BaseException` | `استثناء_اساسي` |
| `Exception` | `استثناء` |
| `GeneratorExit` | `خروج_مولد` |
| `KeyboardInterrupt` | `مقاطعه_لوحه_المفاتيح` |
| `SystemExit` | `خروج_نظام` |

### Arithmetic

| Python | Arabic |
|---|---|
| `ArithmeticError` | `خطا_حسابي` |
| `FloatingPointError` | `خطا_فاصله_عائمه` |
| `OverflowError` | `خطا_فيضان` |
| `ZeroDivisionError` | `خطا_القسمه_على_صفر` |

### Assertion / Attribute / Name

| Python | Arabic |
|---|---|
| `AssertionError` | `خطا_تاكيد` |
| `AttributeError` | `خطا_خاصيه` |
| `NameError` | `خطا_اسم` |
| `UnboundLocalError` | `خطا_متغير_غير_مرتبط` |

### Buffer / EOF

| Python | Arabic |
|---|---|
| `BufferError` | `خطا_مخزن_مؤقت` |
| `EOFError` | `خطا_نهايه_الملف` |

### Import

| Python | Arabic |
|---|---|
| `ImportError` | `خطا_استيراد` |
| `ModuleNotFoundError` | `خطا_الوحده_غير_موجوده` |

### Lookup

| Python | Arabic |
|---|---|
| `LookupError` | `خطا_بحث` |
| `IndexError` | `خطا_فهرس` |
| `KeyError` | `خطا_مفتاح` |

### Memory

| Python | Arabic |
|---|---|
| `MemoryError` | `خطا_ذاكره` |

### OS / IO Errors

| Python | Arabic |
|---|---|
| `OSError` | `خطا_نظام` |
| `EnvironmentError` | `خطا_بيئه` |
| `IOError` | `خطا_ادخال_اخراج` |
| `BlockingIOError` | `خطا_ادخال_اخراج_حاجب` |
| `ChildProcessError` | `خطا_عمليه_فرعيه` |
| `ConnectionError` | `خطا_اتصال` |
| `BrokenPipeError` | `خطا_انبوب_مكسور` |
| `ConnectionAbortedError` | `خطا_اتصال_ملغي` |
| `ConnectionRefusedError` | `خطا_اتصال_مرفوض` |
| `ConnectionResetError` | `خطا_اتصال_منقطع` |
| `FileExistsError` | `خطا_الملف_موجود` |
| `FileNotFoundError` | `خطا_الملف_غير_موجود` |
| `InterruptedError` | `خطا_مقاطعه` |
| `IsADirectoryError` | `خطا_هذا_مجلد` |
| `NotADirectoryError` | `خطا_ليس_مجلدا` |
| `PermissionError` | `خطا_صلاحيات` |
| `ProcessLookupError` | `خطا_بحث_عمليه` |
| `TimeoutError` | `خطا_انتهاء_مهله` |

### Reference

| Python | Arabic |
|---|---|
| `ReferenceError` | `خطا_مرجع` |

### Runtime

| Python | Arabic |
|---|---|
| `RuntimeError` | `خطا_تشغيل` |
| `NotImplementedError` | `خطا_غير_منفذ` |
| `RecursionError` | `خطا_عوديه` |
| `SystemError` | `خطا_نظام_داخلي` |

### Stop Iteration

| Python | Arabic |
|---|---|
| `StopIteration` | `ايقاف_التكرار` |
| `StopAsyncIteration` | `ايقاف_التكرار_المتزامن` |

### Syntax

| Python | Arabic |
|---|---|
| `SyntaxError` | `خطا_صياغه` |
| `IndentationError` | `خطا_ازاحه` |
| `TabError` | `خطا_تبويب` |

### Type

| Python | Arabic |
|---|---|
| `TypeError` | `خطا_نوع` |

### Unicode

| Python | Arabic |
|---|---|
| `UnicodeError` | `خطا_يونيكود` |
| `UnicodeDecodeError` | `خطا_فك_يونيكود` |
| `UnicodeEncodeError` | `خطا_ترميز_يونيكود` |
| `UnicodeTranslateError` | `خطا_ترجمه_يونيكود` |

### Value

| Python | Arabic |
|---|---|
| `ValueError` | `خطا_قيمه` |

### Warning Hierarchy

| Python | Arabic |
|---|---|
| `Warning` | `تحذير` |
| `BytesWarning` | `تحذير_بايت` |
| `DeprecationWarning` | `تحذير_اهمال` |
| `EncodingWarning` | `تحذير_ترميز` |
| `FutureWarning` | `تحذير_مستقبلي` |
| `ImportWarning` | `تحذير_استيراد` |
| `PendingDeprecationWarning` | `تحذير_اهمال_قادم` |
| `ResourceWarning` | `تحذير_موارد` |
| `RuntimeWarning` | `تحذير_تشغيل` |
| `SyntaxWarning` | `تحذير_صياغه` |
| `UnicodeWarning` | `تحذير_يونيكود` |
| `UserWarning` | `تحذير_مستخدم` |

### Exception Groups (Python 3.11+)

| Python | Arabic |
|---|---|
| `BaseExceptionGroup` | `مجموعه_استثنائات_اساسيه` |
| `ExceptionGroup` | `مجموعه_استثنائات` |

---

## Message Templates

### Division Errors

| Pattern | Arabic template |
|---|---|
| `^division by zero$` | `القسمة على صفر` |
| `^integer division or modulo by zero$` | `قسمة صحيحة أو باقي على صفر` |
| `^float division by zero$` | `قسمة عشرية على صفر` |

### Name / Variable Errors

| Pattern | Arabic template |
|---|---|
| `^name '(?P<name>[^']+)' is not defined$` | `الاسم '{name}' غير معرّف` |
| `^name '...' is not defined. Did you mean: '...'?$` | `الاسم '{name}' غير معرّف. هل تقصد: '{sugg}'؟` |
| `^free variable '...' referenced before assignment in enclosing scope$` | `المتغير الحر '{name}' مستخدم قبل تعريفه في النطاق المحيط` |
| `^local variable '...' referenced before assignment$` | `المتغير المحلي '{name}' مستخدم قبل تعريفه` |
| `^cannot access local variable '...' where it is not associated with a value$` | `لا يمكن الوصول إلى المتغير المحلي '{name}' لأنه غير مرتبط بقيمة` |

### Attribute Errors

| Pattern | Arabic template |
|---|---|
| `^'...' object has no attribute '...'$` | `الكائن من نوع '{type}' لا يملك الخاصية '{attr}'` |
| `^'...' object has no attribute '...'. Did you mean: '...'?$` | `الكائن من نوع '{type}' لا يملك الخاصية '{attr}'. هل تقصد: '{sugg}'؟` |

### Type Errors

| Pattern | Arabic template |
|---|---|
| `^'...' object is not subscriptable$` | `الكائن من نوع '{type}' لا يقبل الفهرسة` |
| `^'...' object is not callable$` | `الكائن من نوع '{type}' غير قابل للاستدعاء` |
| `^'...' object is not iterable$` | `الكائن من نوع '{type}' غير قابل للتكرار` |
| `^'...' object cannot be interpreted as an integer$` | `الكائن من نوع '{type}' لا يمكن تفسيره كعدد صحيح` |
| `^'...' object is not an iterator$` | `الكائن من نوع '{type}' ليس مكرراً` |
| `^argument of type '...' is not iterable$` | `الوسيط من نوع '{type}' غير قابل للتكرار` |
| `^list indices must be integers or slices, not <type>$` | `فهارس القائمة يجب أن تكون أعداداً صحيحة أو شرائح، لا '{type}'` |
| `^tuple indices must be integers or slices, not <type>$` | `فهارس الصف يجب أن تكون أعداداً صحيحة أو شرائح، لا '{type}'` |
| `^string indices must be integers$` | `فهارس النص يجب أن تكون أعداداً صحيحة` |
| `^object of type '...' has no len()$` | `الكائن من نوع '{type}' لا يملك دالة len()` |
| `^unhashable type: '...'$` | `النوع '{type}' غير قابل للتجزئة` |
| `^a bytes-like object is required, not '...'$` | `مطلوب كائن من نوع bytes، لا '{type}'` |
| `^<func>() takes N positional arguments but M were given$` | `{func}() تأخذ {n} وسيط موضعي{plural} لكن تم تمرير {got}` |
| `^sequence item N: expected str instance, X found$` | `عنصر المتسلسلة {n}: متوقع نص، وجد {got}` |

### Call Signature Errors

| Pattern | Arabic template |
|---|---|
| `^unsupported operand type(s) for <op>: '...' and '...'$` | `أنواع المعاملات غير مدعومة لـ {op}: '{a}' و '{b}'` |
| `^can only concatenate <a> (not "<b>") to <a>$` | `يمكن فقط ضم {a} (لا {b}) إلى {a}` |
| `^<func>() missing N required positional argument(s): ...` | `{func}() ينقصها {n} وسيط إجباري{plural}: {rest}` |
| `^<func>() got an unexpected keyword argument '...'$` | `{func}() استلمت وسيطا مفتاحيا غير متوقع '{name}'` |
| `^expected N positional arguments, got M$` | `كان متوقعا {n} {arg_kind} لكن تم تمرير {got}` |

### Index / Key Errors

| Pattern | Arabic template |
|---|---|
| `^list index out of range$` | `فهرس القائمة خارج النطاق` |
| `^tuple index out of range$` | `فهرس الصف خارج النطاق` |
| `^string index out of range$` | `فهرس النص خارج النطاق` |
| `^pop from empty list$` | `إخراج من قائمة فارغة` |
| `^pop from an empty (set|deque|dict)$` | `إخراج من {1} فارغ` |
| `^dictionary changed size during iteration$` | `تغير حجم القاموس أثناء التكرار` |

### Value Errors

| Pattern | Arabic template |
|---|---|
| `^too many values to unpack (expected N)$` | `قيم كثيرة جداً للتفريغ (متوقع {n})` |
| `^not enough values to unpack (expected N, got M)$` | `قيم غير كافية للتفريغ (متوقع {n}، حصلنا على {got})` |
| `^invalid literal for int() with base N: '...'$` | `قيمة غير صالحة للدالة int() بالأساس {base}: '{val}'` |
| `^could not convert string to float: '...'$` | `تعذر تحويل النص إلى عدد عشري: '{val}'` |
| `^math domain error$` | `خطأ في نطاق الرياضيات` |

### Overflow / Arithmetic

| Pattern | Arabic template |
|---|---|
| `^math range error$` | `خطأ في مجال الرياضيات` |
| `^int too large to convert to float$` | `العدد الصحيح كبير جداً للتحويل إلى عشري` |

### Recursion / Runtime

| Pattern | Arabic template |
|---|---|
| `^maximum recursion depth exceeded...` | `تم تجاوز عمق العودية الأقصى{rest}` |
| `^generator already executing$` | `المولّد قيد التنفيذ بالفعل` |
| `^coroutine already executing$` | `الكوروتين قيد التنفيذ بالفعل` |
| `^coroutine raised StopIteration$` | `الكوروتين أطلق ايقاف_التكرار` |

### Import Errors

| Pattern | Arabic template |
|---|---|
| `^No module named '...'$` | `لا توجد وحدة باسم '{name}'` |
| `^cannot import name '...' from '...'...` | `لا يمكن استيراد الاسم '{name}' من '{module}'{rest}` |

### Syntax / Indentation

| Pattern | Arabic template |
|---|---|
| `^expected an indented block...` | `متوقع كتلة مزاحة{rest}` |
| `^inconsistent use of tabs and spaces in indentation$` | `استخدام غير متسق للجداول والمسافات في الإزاحة` |
| `^unindent does not match any outer indentation level$` | `الإزاحة لا تطابق أي مستوى خارجي` |

### OS Errors

| Pattern | Arabic template |
|---|---|
| `^[Errno N] <msg>: '<path>'$` | `[رقم الخطأ {errno}] {msg}: '{path}'` |
| `^[Errno N] <msg>$` | `[رقم الخطأ {errno}] {msg}` |
| `^[WinError N] <msg>$` | `[خطأ ويندوز {errno}] {msg}` |
| `^Connection refused$` | `رُفض الاتصال` |
| `^Connection reset by peer$` | `أعاد الطرف الآخر ضبط الاتصال` |
| `^Broken pipe$` | `الأنبوب معطوب` |

---

## Frame Line Strings

| English | Arabic |
|---|---|
| `Traceback (most recent call last):` | `تتبع_الأخطاء (المكدس الأحدث آخرا):` |
| `  File "{path}", line {N}, in {scope}` | `  ملف "{path}", سطر {N}, في {scope}` |
| `  File "{path}", line {N}` | `  ملف "{path}", سطر {N}` |
| `<module>` | `<الوحدة>` |
