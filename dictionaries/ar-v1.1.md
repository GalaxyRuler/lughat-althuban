# Arabic dialect dictionary — ar-v1.1
<!-- Generated from lexicon/core.toml. Do not edit by hand. -->

**Status**: compatibility
**Source of truth**: `lexicon/core.toml`

## Reading this file

- **Python**: the Python symbol this entry translates.
- **Canonical**: the visible Arabic spelling shown to learners.
- **Alternates**: defensible non-canonical spellings; not accepted as canonical.
- **Rationale**: why this Arabic term was chosen.

The runtime normalizer folds hamza variants, final ta marbuta, alef maksura,
harakat, and tatweel. This file keeps the natural visible form.

## 1. Control-flow keywords

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `and` | و | — | MSA conjunction "and". |
| `as` | كـ | باسم | Arabic prefix meaning "as"; natural in `import X as Y`. |
| `assert` | أكد | تحقق | MSA "affirm/assert". |
| `async` | غير_متزامن | لاتزامني | MSA "non-synchronous"; composed for clarity. |
| `async` | متزامن | — | v1.1 addition: shorter MSA term "concurrent/synchronous-with". Both غير_متزامن and متزامن are accepted; غير_متزامن remains the reverse-map canonical. |
| `await` | انتظر | — | MSA "wait". |
| `break` | اكسر | توقف، اقطع | MSA direct cognate; matches the "break out of loop" metaphor. |
| `class` | صنف | فئة، طبقة | Matches Hedy; MSA for "kind/category" is more established in CS translation than alternatives. |
| `continue` | استمر | تابع، واصل | MSA "continue". |
| `def` | دالة | عرف، تعريف | MSA mathematical standard for "function"; Hedy uses this. |
| `del` | احذف | امسح | MSA "delete". |
| `elif` | وإلا_إذا | وإذا | Composed from else + if; matches natural Arabic construction. |
| `else` | وإلا | والا | MSA "otherwise"; Hedy uses this. |
| `except` | استثناء | التقط | MSA noun form of "exception"; reads naturally in `try/except`. |
| `finally` | أخيرا | نهاية | MSA "at last / finally". |
| `for` | لكل | من_أجل | "For each" idiom in MSA; concise. |
| `from` | من | — | MSA preposition "from". |
| `global` | عام | عالمي | MSA "public/general"; avoid عالمي which means "global as in worldwide". |
| `if` | إذا | لو، إذا | MSA conditional "if". |
| `import` | استورد | اجلب، ادرج | MSA "import". |
| `in` | في | — | MSA preposition "in". |
| `is` | هو | يكون | MSA copula "is/he". |
| `lambda` | لامدا | دالة_مجهولة | Transliteration; standard in Arabic mathematics for lambda. |
| `nonlocal` | غير_محلي | — | Composed MSA. |
| `not` | ليس | لا | MSA negation; ليس reads as a formal "not". |
| `or` | أو | — | MSA disjunction "or". |
| `pass` | مرر | تجاوز | MSA "pass through". |
| `raise` | ارفع | اطلق | MSA "raise"; matches Python's metaphor. |
| `return` | ارجع | أرجع، اعد | MSA "return/go back"; without hamza variants for normalizer idempotency. |
| `try` | حاول | جرب | MSA "try/attempt". |
| `while` | طالما | بينما | MSA "as long as". |
| `with` | مع | — | MSA "with". |
| `yield` | سلم | انتج | MSA "hand over"; semantically closer to generator `yield` than "produce". |
| `match` | طابق | — | MSA "match/compare". |
| `case` | حالة | — | MSA "case". |
| `type` | نوع | — | MSA "type"; shared with built-in `type()`. |
| `_` | _ | — | Underscore is universal; no translation. |

## 2. Literal keywords

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `False` | خطأ | باطل، كاذب | Semantic literal "incorrect"; Hedy uses صحيح/خطأ pair. Shown in visible form `خطأ`; normalizer folds final hamza to give stored key `خطا` per ADR 0004. |
| `None` | لاشيء | عدم، فراغ | Literal "nothing"; closest to `None` semantically. |
| `True` | صحيح | حق | Semantic literal "correct"; Hedy uses. |

## 3. Built-in types

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `bool` | منطقي | — | MSA "logical/boolean". |
| `bytearray` | مصفوفة_بايتات | — | Composed: "array of bytes". |
| `bytes` | بايتات | ثنائيات | Transliteration; standard in Arabic technical writing. |
| `complex` | عدد_مركب | — | MSA "complex number" (mathematical). |
| `dict` | قاموس | — | MSA "dictionary". |
| `float` | عدد_عشري | عشري | MSA "decimal number". |
| `frozenset` | مجموعة_ثابتة | — | Composed: "frozen set". |
| `int` | عدد_صحيح | صحيح | MSA "integer"; avoids collision with True literal. |
| `list` | قائمة | — | MSA "list". |
| `object` | كائن | شيء | MSA "object"; established in Arabic OOP translation. |
| `range` | نطاق | مدى | MSA "range/span". |
| `set` | مجموعة | — | MSA "set" (mathematical usage). |
| `str` | نص | سلسلة، سلسلة_نصية | MSA "text"; simpler than "string" and widely used. |
| `tuple` | صف | ثنائية، طقم | MSA "row/series"; matches ordered-tuple concept. |
| `type` | نوع | — | See soft keywords. |

## 4. Built-in functions

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `abs` | مطلق | — | MSA "absolute". |
| `all` | كل | — | MSA "all". |
| `any` | أي | — | MSA "any"; normalizer folds hamza to give stored key `اي` per ADR 0004. |
| `ascii` | أيسكي | — | Transliteration. |
| `bin` | ثنائي | — | MSA "binary". |
| `breakpoint` | نقطة_توقف | — | Composed: "stopping point"; matches the debugger metaphor. |
| `callable` | قابل_للاستدعاء | — | MSA "callable". |
| `chr` | رمز | حرف | MSA "symbol"; `.ord` counterpart is قيمة_رمز. |
| `classmethod` | تابع_صنف | — | Composed: "method of class". |
| `compile` | ترجم | جمع | MSA "translate/compile". |
| `delattr` | احذف_صفة | — | Composed: "delete attribute". |
| `dir` | محتويات | — | MSA "contents"; reads naturally for object inspection. |
| `divmod` | قسمة_باقي | — | Composed: "division and remainder". |
| `enumerate` | رقم | عدد، عدد_متسلسل | MSA "number"; short and clear. |
| `eval` | قيم | — | MSA "evaluate". |
| `exec` | نفذ | — | MSA "execute". |
| `filter` | فلتر | صف | Transliteration; `صف` would collide with `tuple`. See collision audit. |
| `format` | نسق | — | MSA "format". |
| `getattr` | اجلب_صفة | — | Composed: "fetch attribute". |
| `globals` | متغيرات_عامة | عامات | Composed for clarity. |
| `hasattr` | يملك_صفة | — | Composed: "owns attribute". |
| `hash` | بصمة | تجزئة | MSA "fingerprint/signature"; semantic. |
| `help` | مساعدة | ساعد | MSA "help". |
| `hex` | ست_عشري | — | MSA "hexadecimal". |
| `id` | معرف | — | MSA "identifier". |
| `input` | ادخل | اقرا | MSA "enter"; reads as an imperative. |
| `isinstance` | من_نوع | — | Composed: "is of type". |
| `issubclass` | صنف_فرعي | — | MSA "subclass". |
| `iter` | كرر | — | MSA "iterate". |
| `len` | طول | — | MSA "length". |
| `locals` | متغيرات_محلية | محلات | Composed for clarity. |
| `map` | طبق | — | MSA "apply"; closer to functional map than alternatives. |
| `max` | الأكبر | أكبر | MSA "maximum". |
| `min` | الأصغر | أصغر | MSA "minimum". |
| `next` | التالي | — | MSA "next". |
| `oct` | ثماني | — | MSA "octal". |
| `open` | افتح | — | MSA "open". |
| `ord` | قيمة_رمز | — | Composed: "value of symbol"; pairs with chr. |
| `pow` | أس | — | MSA "power/exponent" (short mathematical form). |
| `print` | اطبع | — | MSA "print"; Hedy uses. |
| `property` | خاصية | — | MSA "property/attribute". |
| `repr` | تمثيل | — | MSA "representation". |
| `reversed` | معكوس | — | MSA "reversed". |
| `round` | قرب | دور | MSA "approximate". |
| `setattr` | عين_صفة | — | Composed: "set attribute". |
| `slice` | شريحة | — | MSA "slice". |
| `sorted` | مرتب | — | MSA "sorted". |
| `staticmethod` | تابع_ثابت | — | Composed: "static method". |
| `sum` | مجموع | — | MSA "sum". |
| `super` | الأصل | الأب | MSA "origin/parent"; matches OOP inheritance metaphor. |
| `vars` | متغيرات | — | MSA "variables". |
| `zip` | ازدوج | دمج | MSA "pair up". |

## 5. Built-in exceptions

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `ArithmeticError` | خطأ_حسابي | — | Composed. |
| `AssertionError` | خطأ_تأكيد | — | Composed. |
| `AttributeError` | خطأ_صفة | — | Composed. |
| `BaseException` | استثناء_أساسي | — | Composed. |
| `ConnectionError` | خطأ_اتصال | — | Composed. |
| `EOFError` | خطأ_نهاية_ملف | — | Composed. |
| `Exception` | استثناء_عام | استثناء | "general exception"; `استثناء` alone collides with the `except` keyword (same name in MSA). Parallels `BaseException` → `استثناء_أساسي`. |
| `FileExistsError` | خطأ_ملف_موجود | — | Composed. |
| `FileNotFoundError` | خطأ_ملف_مفقود | — | Composed. |
| `FloatingPointError` | خطأ_عشري | — | Composed. |
| `GeneratorExit` | خروج_مولد | — | Composed. |
| `ImportError` | خطأ_استيراد | — | Composed. |
| `IndentationError` | خطأ_إزاحة | — | Composed. |
| `IndexError` | خطأ_فهرس | — | Composed. |
| `IOError` | خطأ_إدخال_إخراج | — | Composed. |
| `KeyboardInterrupt` | مقاطعة | — | MSA "interruption"; simplest form. |
| `KeyError` | خطأ_مفتاح | — | Composed. |
| `LookupError` | خطأ_بحث | — | Composed. |
| `MemoryError` | خطأ_ذاكرة | — | Composed. |
| `ModuleNotFoundError` | خطأ_وحدة_مفقودة | — | Composed. |
| `NameError` | خطأ_اسم | — | Composed. |
| `NotImplementedError` | خطأ_غير_منفذ | — | Composed. |
| `OSError` | خطأ_نظام | — | Composed. |
| `OverflowError` | خطأ_فائض | — | Composed. |
| `PermissionError` | خطأ_صلاحية | — | Composed. |
| `RecursionError` | خطأ_تكرار_ذاتي | — | Composed. |
| `RuntimeError` | خطأ_تشغيل | — | Composed. |
| `StopIteration` | انتهاء_التكرار | — | Composed. |
| `SyntaxError` | خطأ_صياغة | — | Composed. |
| `SystemError` | خطأ_نظام_داخلي | — | Composed. |
| `SystemExit` | خروج_نظام | — | Composed. |
| `TabError` | خطأ_جدولة | — | Composed. |
| `TimeoutError` | خطأ_انتهاء_وقت | — | Composed. |
| `TypeError` | خطأ_نوع | — | Composed. |
| `UnicodeDecodeError` | خطأ_فك_يونيكود | — | Composed. |
| `UnicodeEncodeError` | خطأ_ترميز_يونيكود | — | Composed. |
| `UnicodeError` | خطأ_يونيكود | — | Composed. |
| `ValueError` | خطأ_قيمة | — | Composed. |
| `Warning` | تحذير | — | MSA "warning". |
| `ZeroDivisionError` | خطأ_قسمة_صفر | — | Composed. |

## 6. Common methods on built-in types

| Python | Canonical | Alternates | Rationale |
|---|---|---|---|
| `.count` | عد | — | MSA "count". |
| `.decode` | فك_رمز | — | Composed: "decode". |
| `.encode` | رمز_بايتات | رمز | Composed; `رمز` alone would collide with `chr`. See collision audit. |
| `.endswith` | ينتهي_بـ | — | Composed: "ends with". |
| `.find` | ابحث | — | MSA "find/search". |
| `.format` | نسق | — | Same as built-in `format`. |
| `.join` | اجمع | — | MSA "join/collect". |
| `.lower` | صغير | — | MSA "small/lowercase". |
| `.replace` | استبدل | — | MSA "replace". |
| `.split` | قسم | — | MSA "split/divide". |
| `.startswith` | يبدأ_بـ | — | Composed: "starts with". |
| `.capitalize` | كبر_الأول | — | Composed: "capitalize the first (letter)". |
| `.center` | توسط | — | MSA "be in the center"; pads to center the string. |
| `.ljust` | ضبط_يسار | — | Composed: "left-align". |
| `.rjust` | ضبط_يمين | — | Composed: "right-align". |
| `.strip` | جرد | نظف | MSA "strip". |
| `.swapcase` | عكس_الحالة | — | Composed: "reverse/swap case". |
| `.title` | عنوان | — | MSA "title/heading"; title-cases every word. |
| `.upper` | كبير | — | MSA "big/uppercase". |
| `.zfill` | مل_بأصفار | — | Composed: "fill with zeros". |
| `.append` | اضف | الحق | MSA "add". |
| `.extend` | مدد | — | MSA "extend". |
| `.index` | موقع | — | MSA "position". |
| `.insert` | ادرج | — | MSA "insert". |
| `.pop` | انتزع | — | MSA "extract". |
| `.remove` | ازل | — | MSA "remove". |
| `.reverse` | اعكس | — | MSA "reverse" (imperative). |
| `.sort` | رتب | — | MSA "arrange/sort". |
| `.get` | اجلب | — | MSA "fetch". |
| `.items` | عناصر | — | MSA "items/elements". |
| `.keys` | مفاتيح | — | MSA "keys". |
| `.popitem` | انتزع_زوج | — | Composed: "extract a pair" (dict items are key-value pairs). |
| `.setdefault` | عين_افتراضي | — | Composed. |
| `.update` | حدث | — | MSA "update". |
| `.values` | قيم_القاموس | قيم | Composed; `قيم` alone would collide with `eval`. See collision audit. |
| `.add` | ضم | — | MSA "include/incorporate"; distinct from `اضف` (list `.append`) to avoid attribute collision. |
| `.difference` | فرق | — | MSA mathematical "difference" (A minus B). |
| `.discard` | أسقط | — | MSA "drop/set aside"; like `.remove` but no error if element absent. |
| `.intersection` | تقاطع | — | MSA mathematical "intersection". |
| `.union` | اتحاد | — | MSA mathematical "union". |
| `.clear` | امسح | — | MSA "clear/erase". |
| `.copy` | انسخ | — | MSA "copy". |
