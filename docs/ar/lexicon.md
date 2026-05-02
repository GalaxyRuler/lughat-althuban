# المعجم العربي الموحد

هذا الملف هو المرجع العلني الواحد للمصطلحات البرمجية العربية في لغة الثعبان.
يولد من `lexicon/core.toml` و`lexicon/libraries.toml`، وتبقى الصفحات المتخصصة مثل `glossary.md` و`aliases-index.md` و`stdlib-reference.md` واجهات مشتقة للتصفح السريع وليست مصادر مستقلة.

## المصطلحات الأساسية

| الرمز في Python | العربية المعتمدة | النوع | بدائل موثقة |
|---|---|---|---|
| `and` | و | كلمة تحكم | — |
| `as` | باسم | كلمة تحكم | كـ |
| `assert` | أكد | كلمة تحكم | تحقق |
| `async` | غير_متزامن | كلمة تحكم | لاتزامني |
| `await` | انتظر | كلمة تحكم | — |
| `break` | اكسر | كلمة تحكم | توقف، اقطع |
| `class` | صنف | كلمة تحكم | فئة، طبقة |
| `continue` | استمر | كلمة تحكم | تابع، واصل |
| `def` | دالة | كلمة تحكم | عرف، تعريف |
| `del` | احذف | كلمة تحكم | امسح |
| `elif` | وإلا_إذا | كلمة تحكم | وإذا |
| `else` | وإلا | كلمة تحكم | والا |
| `except` | استثناء | كلمة تحكم | التقط |
| `finally` | أخيرا | كلمة تحكم | نهاية |
| `for` | لكل | كلمة تحكم | من_أجل |
| `from` | من | كلمة تحكم | — |
| `global` | عام | كلمة تحكم | عالمي |
| `if` | إذا | كلمة تحكم | لو، إذا |
| `import` | استورد | كلمة تحكم | اجلب، ادرج |
| `in` | في | كلمة تحكم | — |
| `is` | يكون | كلمة تحكم | هو |
| `lambda` | لامدا | كلمة تحكم | دالة_مجهولة |
| `nonlocal` | غير_محلي | كلمة تحكم | — |
| `not` | ليس | كلمة تحكم | لا |
| `or` | أو | كلمة تحكم | — |
| `pass` | مرر | كلمة تحكم | تجاوز |
| `raise` | ارفع | كلمة تحكم | اطلق |
| `return` | ارجع | كلمة تحكم | أرجع، اعد |
| `try` | حاول | كلمة تحكم | جرب |
| `while` | طالما | كلمة تحكم | بينما |
| `with` | مع | كلمة تحكم | — |
| `yield` | سلم | كلمة تحكم | انتج |
| `match` | طابق | كلمة تحكم | — |
| `case` | حالة | كلمة تحكم | — |
| `type` | نوع | كلمة تحكم | — |
| `_` | _ | كلمة تحكم | — |
| `False` | خطأ | قيمة حرفية | باطل، كاذب |
| `None` | لاشيء | قيمة حرفية | عدم، فراغ |
| `True` | صحيح | قيمة حرفية | حق |
| `bool` | منطقي | نوع مدمج | — |
| `bytearray` | مصفوفة_بايتات | نوع مدمج | — |
| `bytes` | بايتات | نوع مدمج | ثنائيات |
| `complex` | عدد_مركب | نوع مدمج | — |
| `dict` | قاموس | نوع مدمج | — |
| `float` | عدد_عشري | نوع مدمج | عشري |
| `frozenset` | مجموعة_ثابتة | نوع مدمج | — |
| `int` | عدد_صحيح | نوع مدمج | صحيح |
| `list` | قائمة | نوع مدمج | — |
| `object` | كائن | نوع مدمج | شيء |
| `range` | نطاق | نوع مدمج | مدى |
| `set` | مجموعة | نوع مدمج | — |
| `str` | نص | نوع مدمج | سلسلة، سلسلة_نصية |
| `tuple` | صف | نوع مدمج | ثنائية، طقم |
| `type` | نوع | نوع مدمج | — |
| `abs` | مطلق | دالة مدمجة | — |
| `all` | كل | دالة مدمجة | — |
| `any` | أي | دالة مدمجة | — |
| `ascii` | أيسكي | دالة مدمجة | — |
| `bin` | ثنائي | دالة مدمجة | — |
| `breakpoint` | نقطة_توقف | دالة مدمجة | — |
| `callable` | قابل_للاستدعاء | دالة مدمجة | — |
| `chr` | رمز | دالة مدمجة | حرف |
| `classmethod` | تابع_صنف | دالة مدمجة | — |
| `compile` | ترجم | دالة مدمجة | جمع |
| `delattr` | احذف_صفة | دالة مدمجة | — |
| `dir` | محتويات | دالة مدمجة | — |
| `divmod` | قسمة_باقي | دالة مدمجة | — |
| `enumerate` | رقم | دالة مدمجة | عدد، عدد_متسلسل |
| `eval` | قيم | دالة مدمجة | — |
| `exec` | نفذ | دالة مدمجة | — |
| `filter` | فلتر | دالة مدمجة | صف |
| `format` | نسق | دالة مدمجة | — |
| `getattr` | اجلب_صفة | دالة مدمجة | — |
| `globals` | متغيرات_عامة | دالة مدمجة | عامات |
| `hasattr` | يملك_صفة | دالة مدمجة | — |
| `hash` | بصمة | دالة مدمجة | تجزئة |
| `help` | مساعدة | دالة مدمجة | ساعد |
| `hex` | ست_عشري | دالة مدمجة | — |
| `id` | معرف | دالة مدمجة | — |
| `input` | ادخل | دالة مدمجة | اقرا |
| `isinstance` | من_نوع | دالة مدمجة | — |
| `issubclass` | صنف_فرعي | دالة مدمجة | — |
| `iter` | كرر | دالة مدمجة | — |
| `len` | طول | دالة مدمجة | — |
| `locals` | متغيرات_محلية | دالة مدمجة | محلات |
| `map` | طبق | دالة مدمجة | — |
| `max` | الأكبر | دالة مدمجة | أكبر |
| `min` | الأصغر | دالة مدمجة | أصغر |
| `next` | التالي | دالة مدمجة | — |
| `oct` | ثماني | دالة مدمجة | — |
| `open` | افتح | دالة مدمجة | — |
| `ord` | قيمة_رمز | دالة مدمجة | — |
| `pow` | أس | دالة مدمجة | — |
| `print` | اطبع | دالة مدمجة | — |
| `property` | خاصية | دالة مدمجة | — |
| `repr` | تمثيل | دالة مدمجة | — |
| `reversed` | معكوس | دالة مدمجة | — |
| `round` | قرب | دالة مدمجة | دور |
| `setattr` | عين_صفة | دالة مدمجة | — |
| `slice` | شريحة | دالة مدمجة | — |
| `sorted` | مرتب | دالة مدمجة | — |
| `staticmethod` | تابع_ثابت | دالة مدمجة | — |
| `sum` | مجموع | دالة مدمجة | — |
| `super` | الأصل | دالة مدمجة | الأب |
| `vars` | متغيرات | دالة مدمجة | — |
| `zip` | ازدوج | دالة مدمجة | دمج |
| `ArithmeticError` | خطأ_حسابي | استثناء | — |
| `AssertionError` | خطأ_تأكيد | استثناء | — |
| `AttributeError` | خطأ_صفة | استثناء | — |
| `BaseException` | استثناء_أساسي | استثناء | — |
| `BlockingIOError` | خطأ_إدخال_إخراج_حاجب | استثناء | — |
| `ConnectionError` | خطأ_اتصال | استثناء | — |
| `EOFError` | خطأ_نهاية_ملف | استثناء | — |
| `Exception` | استثناء_عام | استثناء | استثناء |
| `FileExistsError` | خطأ_ملف_موجود | استثناء | — |
| `FileNotFoundError` | خطأ_ملف_مفقود | استثناء | — |
| `FloatingPointError` | خطأ_عشري | استثناء | — |
| `GeneratorExit` | خروج_مولد | استثناء | — |
| `ImportError` | خطأ_استيراد | استثناء | — |
| `IndentationError` | خطأ_إزاحة | استثناء | — |
| `IndexError` | خطأ_فهرس | استثناء | — |
| `IOError` | خطأ_إدخال_إخراج | استثناء | — |
| `IsADirectoryError` | خطأ_هذا_مجلد | استثناء | — |
| `KeyboardInterrupt` | مقاطعة | استثناء | — |
| `KeyError` | خطأ_مفتاح | استثناء | — |
| `LookupError` | خطأ_بحث | استثناء | — |
| `MemoryError` | خطأ_ذاكرة | استثناء | — |
| `ModuleNotFoundError` | خطأ_وحدة_مفقودة | استثناء | — |
| `NameError` | خطأ_اسم | استثناء | — |
| `NotADirectoryError` | خطأ_ليس_مجلدا | استثناء | — |
| `NotImplementedError` | خطأ_غير_منفذ | استثناء | — |
| `OSError` | خطأ_نظام | استثناء | — |
| `OverflowError` | خطأ_فائض | استثناء | — |
| `PermissionError` | خطأ_صلاحية | استثناء | — |
| `RecursionError` | خطأ_عودية | استثناء | خطأ_تكرار_ذاتي |
| `RuntimeError` | خطأ_تشغيل | استثناء | — |
| `StopIteration` | انتهاء_التكرار | استثناء | — |
| `SyntaxError` | خطأ_صياغة | استثناء | — |
| `SystemError` | خطأ_نظام_داخلي | استثناء | — |
| `SystemExit` | خروج_نظام | استثناء | — |
| `TabError` | خطأ_جدولة | استثناء | — |
| `TimeoutError` | خطأ_انتهاء_وقت | استثناء | — |
| `TypeError` | خطأ_نوع | استثناء | — |
| `UnicodeDecodeError` | خطأ_فك_يونيكود | استثناء | — |
| `UnicodeEncodeError` | خطأ_ترميز_يونيكود | استثناء | — |
| `UnicodeError` | خطأ_يونيكود | استثناء | — |
| `ValueError` | خطأ_قيمة | استثناء | — |
| `Warning` | تحذير | استثناء | — |
| `ZeroDivisionError` | خطأ_قسمة_صفر | استثناء | — |
| `.count` | عد | صفة/طريقة شائعة | — |
| `.decode` | فك_رمز | صفة/طريقة شائعة | — |
| `.encode` | رمز_بايتات | صفة/طريقة شائعة | رمز |
| `.endswith` | ينتهي_بـ | صفة/طريقة شائعة | — |
| `.find` | ابحث | صفة/طريقة شائعة | — |
| `.format` | نسق | صفة/طريقة شائعة | — |
| `.join` | اجمع | صفة/طريقة شائعة | — |
| `.lower` | صغير | صفة/طريقة شائعة | — |
| `.replace` | استبدل | صفة/طريقة شائعة | — |
| `.split` | قسم | صفة/طريقة شائعة | — |
| `.startswith` | يبدأ_بـ | صفة/طريقة شائعة | — |
| `.capitalize` | كبر_الأول | صفة/طريقة شائعة | — |
| `.center` | توسط | صفة/طريقة شائعة | — |
| `.ljust` | ضبط_يسار | صفة/طريقة شائعة | — |
| `.rjust` | ضبط_يمين | صفة/طريقة شائعة | — |
| `.strip` | جرد | صفة/طريقة شائعة | نظف |
| `.swapcase` | عكس_الحالة | صفة/طريقة شائعة | — |
| `.title` | عنوان | صفة/طريقة شائعة | — |
| `.upper` | كبير | صفة/طريقة شائعة | — |
| `.zfill` | مل_بأصفار | صفة/طريقة شائعة | — |
| `.append` | اضف | صفة/طريقة شائعة | الحق |
| `.extend` | مدد | صفة/طريقة شائعة | — |
| `.index` | موقع | صفة/طريقة شائعة | — |
| `.insert` | ادرج | صفة/طريقة شائعة | — |
| `.pop` | انتزع | صفة/طريقة شائعة | — |
| `.remove` | ازل | صفة/طريقة شائعة | — |
| `.reverse` | اعكس | صفة/طريقة شائعة | — |
| `.sort` | رتب | صفة/طريقة شائعة | — |
| `.get` | اجلب | صفة/طريقة شائعة | — |
| `.items` | عناصر | صفة/طريقة شائعة | — |
| `.keys` | مفاتيح | صفة/طريقة شائعة | — |
| `.popitem` | انتزع_زوج | صفة/طريقة شائعة | — |
| `.setdefault` | عين_افتراضي | صفة/طريقة شائعة | — |
| `.update` | حدث | صفة/طريقة شائعة | — |
| `.values` | قيم_القاموس | صفة/طريقة شائعة | قيم |
| `.add` | ضم | صفة/طريقة شائعة | — |
| `.difference` | فرق | صفة/طريقة شائعة | — |
| `.discard` | أسقط | صفة/طريقة شائعة | — |
| `.intersection` | تقاطع | صفة/طريقة شائعة | — |
| `.union` | اتحاد | صفة/طريقة شائعة | — |
| `.clear` | امسح | صفة/طريقة شائعة | — |
| `.copy` | انسخ | صفة/طريقة شائعة | — |
| `.fit` | لائم | صفة/طريقة شائعة | — |
| `.predict` | تنبا | صفة/طريقة شائعة | — |
| `.transform` | حول_بيانات | صفة/طريقة شائعة | — |
| `.fit_transform` | لائم_وحول | صفة/طريقة شائعة | — |
| `.score` | قيم_نموذج | صفة/طريقة شائعة | — |
| `.predict_proba` | احتمالات_التنبا | صفة/طريقة شائعة | — |

## أسماء المكتبات والوحدات

الأسماء التالية هي الأسماء العربية المعتمدة للاستيراد عبر نظام الأسماء المستعارة.

### الذكاء الاصطناعي

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| ذكاء_مفتوح | `openai` | `arabicpython/aliases/openai.toml` |
| سلسلة_لغه | `langchain_core` | `arabicpython/aliases/langchain_core.toml` |
| كلود_عربي | `anthropic` | `arabicpython/aliases/anthropic.toml` |
| محولات | `transformers` | `arabicpython/aliases/transformers.toml` |
| محولات_جمل | `sentence_transformers` | `arabicpython/aliases/sentence_transformers.toml` |

### البيانات والعلوم

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| بانداس | `pandas` | `arabicpython/aliases/pandas.toml` |
| تعلم_آلي | `sklearn` | `arabicpython/aliases/sklearn.toml` |
| جداول_اكسل | `openpyxl` | `arabicpython/aliases/openpyxl.toml` |
| رسوم_بيانيه | `matplotlib` | `arabicpython/aliases/matplotlib.toml` |
| سايباي | `scipy` | `arabicpython/aliases/scipy.toml` |
| سيبورن | `seaborn` | `arabicpython/aliases/seaborn.toml` |
| نمباي | `numpy` | `arabicpython/aliases/numpy.toml` |

### المستندات

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| مستندات_وورد | `docx` | `arabicpython/aliases/docx.toml` |

### الوسائط

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| بيلو | `PIL.Image` | `arabicpython/aliases/pillow.toml` |

### المكتبة القياسية

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| اتزامن | `asyncio` | `arabicpython/aliases/asyncio.toml` |
| احصاء | `statistics` | `arabicpython/aliases/statistics.toml` |
| ادخال_اخراج | `io` | `arabicpython/aliases/io.toml` |
| ادوات_تكرار | `itertools` | `arabicpython/aliases/itertools.toml` |
| ادوات_دوال | `functools` | `arabicpython/aliases/functools.toml` |
| ادوات_ملفات | `shutil` | `arabicpython/aliases/shutil.toml` |
| اسرار | `secrets` | `arabicpython/aliases/secrets.toml` |
| تاريخ_وقت | `datetime` | `arabicpython/aliases/datetime.toml` |
| تسجيل | `logging` | `arabicpython/aliases/logging.toml` |
| تشفير | `hashlib` | `arabicpython/aliases/hashlib.toml` |
| تعابير | `re` | `arabicpython/aliases/re.toml` |
| تنسيق_نص | `textwrap` | `arabicpython/aliases/textwrap.toml` |
| تنميط | `typing` | `arabicpython/aliases/typing.toml` |
| جيسون | `json` | `arabicpython/aliases/json.toml` |
| خيوط | `threading` | `arabicpython/aliases/threading.toml` |
| روزنامه | `calendar` | `arabicpython/aliases/calendar.toml` |
| رياضيات | `math` | `arabicpython/aliases/math.toml` |
| عشوائي | `random` | `arabicpython/aliases/random.toml` |
| عملية_فرعية | `subprocess` | `arabicpython/aliases/subprocess.toml` |
| قاعدة_بيانات | `sqlite3` | `arabicpython/aliases/sqlite3.toml` |
| مجموعات | `collections` | `arabicpython/aliases/collections.toml` |
| محلل_وسائط | `argparse` | `arabicpython/aliases/argparse.toml` |
| مدير_سياق | `contextlib` | `arabicpython/aliases/contextlib.toml` |
| مسار | `pathlib` | `arabicpython/aliases/pathlib.toml` |
| مسار_نظام | `os.path` | `arabicpython/aliases/os_path.toml` |
| معرف_فريد | `uuid` | `arabicpython/aliases/uuid.toml` |
| ملف_csv | `csv` | `arabicpython/aliases/csv.toml` |
| نصوص | `string` | `arabicpython/aliases/string.toml` |
| نظام | `os` | `arabicpython/aliases/os.toml` |
| نظام_بايثون | `sys` | `arabicpython/aliases/sys.toml` |
| وقت_نظام | `time` | `arabicpython/aliases/time.toml` |

### الاختبار

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| بايتست | `pytest` | `arabicpython/aliases/pytest.toml` |
| مونجو_وهمي | `mongomock` | `arabicpython/aliases/mongomock.toml` |

### حزم أخرى

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| ألكيمي | `sqlalchemy` | `arabicpython/aliases/sqlalchemy.toml` |
| اسماء_بديله | `arabicpython.aliases` | `arabicpython/aliases/alias_runtime.toml` |
| جي_دبليو_تي | `jwt` | `arabicpython/aliases/jwt.toml` |
| دوت_إنف | `dotenv` | `arabicpython/aliases/dotenv.toml` |
| ريتش | `rich` | `arabicpython/aliases/rich.toml` |
| قاعده_بوست | `asyncpg` | `arabicpython/aliases/asyncpg.toml` |
| قاعده_وثائق | `pymongo` | `arabicpython/aliases/pymongo.toml` |
| كليك | `click` | `arabicpython/aliases/click.toml` |
| مخزن_سريع | `redis` | `arabicpython/aliases/redis.toml` |
| مهام_خلفيه | `celery` | `arabicpython/aliases/celery.toml` |
| نماذج_بيانات | `pydantic` | `arabicpython/aliases/pydantic.toml` |
| يامل | `yaml` | `arabicpython/aliases/yaml.toml` |

### الويب

| العربية | وحدة Python | ملف الخريطة |
|---|---|---|
| أيو_هتب | `aiohttp` | `arabicpython/aliases/aiohttp.toml` |
| تحليل_ويب | `bs4` | `arabicpython/aliases/bs4.toml` |
| دجانغو | `django` | `arabicpython/aliases/django.toml` |
| طلبات | `requests` | `arabicpython/aliases/requests.toml` |
| طلبات_حديثه | `httpx` | `arabicpython/aliases/httpx.toml` |
| عميل_اختبار_فاست | `fastapi.testclient` | `arabicpython/aliases/fastapi_testclient.toml` |
| فاست_أبي | `fastapi` | `arabicpython/aliases/fastapi.toml` |
| فلاسك | `flask` | `arabicpython/aliases/flask.toml` |
| متصفح_الي | `playwright.async_api` | `arabicpython/aliases/playwright.toml` |

## صفحات مشتقة

- [مسرد المصطلحات الأساسي](glossary.md)
- [فهرس أسماء المكتبات](aliases-index.md)
- [مرجع المكتبة القياسية](stdlib-reference.md)
