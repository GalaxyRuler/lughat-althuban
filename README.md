<div dir="rtl">

# لغة الثعبان — بايثون بالعربية الكاملة

[![الاختبارات](https://img.shields.io/badge/اختبارات-2960_نجاح-brightgreen)](tests/)
[![CI](https://github.com/GalaxyRuler/lughat-althuban/actions/workflows/ci.yml/badge.svg)](https://github.com/GalaxyRuler/lughat-althuban/actions/workflows/ci.yml)
[![بايثون](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![الرخصة](https://img.shields.io/badge/رخصة-Apache--2.0-orange)](LICENSE)

لهجة برمجية تكتب فيها **الكلمات المفتاحية والدوال المدمجة والاستثناءات والمكتبات** بالعربية الكاملة. ملفات `.apy` تُترجم إلى بايثون القياسي في وقت التحميل وتُنفَّذ بواسطة CPython — دون تشعيب للمترجم ودون تعديل على اللغة الأصلية.

**الحالة (2026-05-03)**: المراحل أ/ب/ج مكتملة، وعمل المرحلة د D-002 إلى D-005 مشحون: معجم واحد في `lexicon/`، أسماء AI عربية، مترجم عكسي Python→لغة الثعبان، أسماء stdlib المعتمدة، أثر أخطاء عربي بثلاثة أوضاع، وملعب مرئي يتضمن لعبة منصة بواجهة Pygame عربية. آخر تشغيل كامل: **2960 اختباراً ناجحاً** على Python 3.13 مع 23 تخطياً مقصوداً.

---

## مثال متكامل — تحليل بيانات بالعربية الكاملة

```python
# تحليل_مبيعات.apy
استورد بانداس باسم بد        # pandas
استورد نمباي باسم نم        # numpy
استورد سيبورن باسم رسم       # seaborn
استورد رياضيات

بيانات = بد.قراءة_جيسون("مبيعات.json")
متوسط  = نم.متوسط(بيانات["الإيرادات"])
اطبع(f"متوسط الإيرادات: {رياضيات.تقريب(متوسط, 2)}")

رسم.ضبط_موضوع("darkgrid")
مخطط = رسم.خط_بياني(بيانات=بيانات, x="الشهر", y="الإيرادات")
مخطط.figure.savefig("تقرير_المبيعات.png")
اطبع("تم حفظ التقرير")
```

```bash
$ ثعبان تحليل_مبيعات.apy
متوسط الإيرادات: 48750.32
تم حفظ التقرير
```

---

## التثبيت

يتطلب Python 3.11 أو أحدث:

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .
```

للتطوير مع جميع المكتبات المدعومة:

```bash
pip install -e ".[all]"
```

يُثبَّت الأمر `ثعبان` تلقائياً. `ثعبان --help` و`ثعبان --version` يعملان كما هو متوقع.

## رسائل الخطأ بالعربية

```bash
$ ثعبان -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطأ_قسمة_صفر: القسمة على صفر
```

## الوثائق بالعربية

| الوثيقة | الوصف |
|---------|--------|
| [دليل البدء الشامل](docs/ar/getting-started.md) | من "مرحبا بالعالم" إلى الاستيراد — خطوة بخطوة |
| [المعجم العربي الموحد](docs/ar/lexicon.md) | الكلمات المفتاحية والدوال والاستثناءات وأسماء المكتبات في مرجع واحد |
| [كتاب الوصفات العربي](docs/ar/cookbook.md) | وصفات عملية قابلة للتشغيل |
| [نظرة عامة على المشروع](docs/ar/README.md) | المعمارية، هيكل المشروع، خارطة الطريق |
| [الأمثلة التعليمية](examples/README.md) | فهرس الأمثلة الأساسية والمتقدمة |
| [معرض GitHub Pages للأمثلة](docs/gallery.html) | أمثلة قابلة للفتح في الملعب، بما فيها الألعاب المرئية وعروض stdlib وAI |
| [سجل التغييرات](CHANGELOG.md) | ما الذي تغيّر في كل إصدار |
| [قاموس وقت التشغيل](dictionaries/ar-v2.md) | الأثر المولّد من المعجم الموحد للقاموس الافتراضي |

## حالة المشروع

اكتملت المراحل أ وب وج. المرحلة د نشطة الآن تحت عنوان **AI & Reach**، وحزم D-002 إلى D-005 مشحونة في هذا الفرع: أسماء AI، مترجم عكسي، أسماء stdlib المعتمدة، وأثر أخطاء عربي كامل. المساهمات الجديدة يجب أن تبدأ من [المعجم العربي الموحد](lexicon/README.md) عند إضافة مصطلح أو اسم مكتبة، ثم تضيف الاختبارات والوثائق المناسبة.

- **خارطة الطريق الحالية:** [`ROADMAP-PHASE-D.md`](ROADMAP-PHASE-D.md)
- **خارطة المرحلة ج التاريخية:** [`ROADMAP-PHASE-C.md`](ROADMAP-PHASE-C.md)
- **ميثاق المرحلة د:** [`decisions/0012-phase-d-charter.md`](decisions/0012-phase-d-charter.md)
- **دليل المساهمة:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **قائمة المواصفات:** [`specs/INDEX.md`](specs/INDEX.md)

</div>

---

## طرق التشغيل

```bash
ثعبان ملف.apy [مُعامِلات...]     # تشغيل ملف
ثعبان -c 'اطبع("مرحبا")'         # تنفيذ سطر مباشرةً
ثعبان - < ملف.apy                # قراءة من المدخل القياسي
ثعبان                             # البيئة التفاعلية REPL
ثعبان ترجمة-عكسية ملف.py          # تحويل Python إلى .apy
ثعبان نسّق ملف.apy               # تنسيق الملف تلقائياً
ثعبان راجع ملف.apy               # فحص الجودة وإظهار التحذيرات
ثعبان --tracebacks=mixed ملف.apy  # أثر عربي مع رسالة Python الأصلية
```

رموز الخروج: `0` نجاح، `1` خطأ في التشغيل أو الترجمة، `2` خطأ في الاستخدام.

---

## استيراد وحدات `.apy`

```python
# رئيسي.apy
استورد مساعد
مساعد.مرحبا("عالم")
```

```python
# مساعد.apy
دالة مرحبا(اسم):
    اطبع(f"مرحبا يا {اسم}")
```

الحزم المختلطة `.py` / `.apy` تعمل — ملفات Python التي تستورد وحدات `.apy` ترى الأسماء المترجمة والمُطبَّعة.

---

## رسائل الخطأ بالعربية

```bash
$ ثعبان -c '1 / 0'
تتبع_الأخطاء (المكدس الأحدث آخرا):
  ملف "<string>", سطر 1, في <الوحدة>
خطأ_قسمة_صفر: القسمة على صفر
```

أسماء الاستثناءات تأتي من `lexicon/core.toml`، وقوالب رسائل الأثر من `lexicon/messages.toml`. الوضع الافتراضي `arabic` يترجم الاسم والرسالة، و`english` يعرض أثر Python الأصلي، و`mixed` يعرض اسم الاستثناء بالعربية مع الرسالة الإنجليزية الأصلية.

---

## الوحدات العربية — استيراد المكتبات بأسماء عربية

### المكتبة القياسية (31 وحدة)

| الاسم العربي | وحدة Python | الاسم العربي | وحدة Python |
|---|---|---|---|
| `نظام` | `os` | `رياضيات` | `math` |
| `مسار` | `pathlib` | `احصاء` | `statistics` |
| `نظام_بايثون` | `sys` | `عشوائي` | `random` |
| `مجموعات` | `collections` | `تسجيل` | `logging` |
| `ادوات_تكرار` | `itertools` | `اتزامن` | `asyncio` |
| `ادوات_دوال` | `functools` | `تشفير` | `hashlib` |
| `تاريخ_وقت` | `datetime` | `ادخال_اخراج` | `io` |
| `وقت_نظام` | `time` | `مدير_سياق` | `contextlib` |
| `روزنامه` | `calendar` | `قاعدة_بيانات` | `sqlite3` |
| `جيسون` | `json` | `تعابير` | `re` |
| `ملف_csv` | `csv` | `تنميط` | `typing` |
| `خيوط` | `threading` | `مسار_نظام` | `os.path` |
| `نصوص` | `string` | `تنسيق_نص` | `textwrap` |
| `عملية_فرعية` | `subprocess` | `ادوات_ملفات` | `shutil` |
| `محلل_وسائط` | `argparse` | `اسرار` | `secrets` |
| `معرف_فريد` | `uuid` | — | — |

### علوم وبيانات (6 حزم)

| الاسم العربي | حزمة Python |
|---|---|
| `نمباي` | `numpy` |
| `بانداس` | `pandas` |
| `رسوم_بيانيه` | `matplotlib` |
| `سيبورن` | `seaborn` |
| `سايباي` | `scipy` |
| `تعلم_آلي` | `scikit-learn` |

### الذكاء الاصطناعي (5 حزم)

| الاسم العربي | حزمة Python |
|---|---|
| `ذكاء_مفتوح` | `openai` |
| `كلود_عربي` | `anthropic` |
| `سلسلة_لغه` | `langchain_core` |
| `محولات` | `transformers` |
| `محولات_جمل` | `sentence_transformers` |

ثبّتها مع:

```bash
pip install -e ".[ai]"
```

### وسائط وألعاب

| الاسم العربي | حزمة Python |
|---|---|
| `بيلو` | `PIL.Image` / Pillow |
| `لعبه` أو `لعبة` | `pygame` / pygame-ce |

ثبّتها مع مجموعة الأسماء الاختيارية:

```bash
pip install -e ".[aliases]"
```

### ويب وشبكات (6 حزم)

| الاسم العربي | حزمة Python |
|---|---|
| `فلاسك` | `flask` |
| `طلبات` | `requests` |
| `أيو_هتب` | `aiohttp` |
| `فاست_أبي` | `fastapi` |
| `دجانغو` | `django` |
| `طلبات_حديثه` | `httpx` |

## طبقة الأدوات

| الأداة | الأمر | الوصف |
|---|---|---|
| **المنسِّق** | `ثعبان نسّق ملف.apy` | تنسيق تلقائي: المسافات البادئة، والتباعد، وأسلوب التعليقات |
| **المدقِّق** | `ثعبان راجع ملف.apy` | تشخيصات: W001–W004، E001، I001 |
| **المترجم العكسي** | `ثعبان ترجمة-عكسية ملف.py` | تحويل Python إلى لغة الثعبان اعتماداً على `Dialect.reverse_names` |
| **نواة Jupyter** | `pip install -e ".[kernel]"` | تشغيل دفاتر `.apy` في Jupyter |
| **امتداد VS Code** | `editors/vscode/` | إبراز صياغي لملفات `.apy` |
| **إضافة pytest** | مُدمجة تلقائياً | اكتشاف وتشغيل ملفات اختبار `.apy` |

---

## واجهة برمجة Python

```python
from arabicpython import (
    install,                       # تثبيت خطاف استيراد .apy
    uninstall,
    run_repl,                      # تشغيل البيئة التفاعلية REPL
    install_excepthook,            # توجيه الاستثناءات غير الملتقطة للمترجم
    uninstall_excepthook,
    format_translated_exception,   # تنسيق مجموعة (نوع، قيمة، تتبع) بالعربية
)
from arabicpython.reverse import reverse_translate
from arabicpython.formatter import format_source, format_file
from arabicpython.linter import lint_source, Diagnostic
```

---

## هيكل المشروع

```
lughat-althuban/
├── arabicpython/              حزمة المحوِّل
│   ├── aliases/               تعيينات TOML مولدة من lexicon/libraries.toml
│   ├── reverse.py             مترجم Python → لغة الثعبان
│   ├── formatter.py           المنسِّق التلقائي
│   └── linter.py              محرك التدقيق والتشخيص
├── arabicpython_kernel/       حزمة نواة Jupyter
├── editors/vscode/            امتداد VS Code
├── tools/                     مولد القواعد النحوية وأدوات التطوير
├── decisions/                 سجلات قرارات المعمارية (ADRs)
├── lexicon/                   مصدر الحقيقة للمصطلحات والكلمات والرسائل
├── dictionaries/              مخرجات القواميس المولدة
├── specs/                     حزم المواصفات للتنفيذ
├── tests/                     مجموعة pytest (2960 نجاحاً في بيئة all)
├── examples/                  برامج .apy قابلة للتشغيل
├── docs/
│   ├── ar/                    الوثائق العربية
│   └── wiki/                  ويكي المرجع الشامل
└── apps/                      تطبيقات عرض متكاملة
```

---

## المعمارية

المصدر يمر عبر `pretokenize` (الأرقام العربية ← ASCII، ترميز علامات الترقيم، رفض محارف bidi) ← `tokenize` الخاصة ببايثون ← معيد كتابة NAME يستشير القاموس العربي↔Python القانوني ← `untokenize` ← `compile` ← `exec`. لا إعادة كتابة لشجرة AST، ولا تشعيب لـ CPython. نفس الأنبوب يدعم كل نقاط الدخول (CLI، REPL، خطاف الاستيراد).

قرارات رئيسية: [`decisions/0001-architecture.md`](decisions/0001-architecture.md) | [`decisions/0004-normalization-policy.md`](decisions/0004-normalization-policy.md)

**قواعد التطبيع**: `أ/إ/آ → ا`، `ة → ه` (في النهاية)، `ى → ي` (في النهاية). جميع مفاتيح TOML يجب أن تجتاز `normalize_identifier()`.

---

## نموذج التطوير

- **المخطط (Claude)**: يكتب سجلات القرارات، يُنسِّق القواميس، يُؤلِّف حزم المواصفات، يراجع التغييرات.
- **المنفِّذ**: يقرأ الحزم في `specs/NNNN-*.md`، يكتب الكود، يُشغِّل الاختبارات.

كل وحدة عمل هي حزمة مواصفات مكتفية بنفسها. انظر [`specs/0000-template.md`](specs/0000-template.md) و[`specs/INDEX.md`](specs/INDEX.md).

---

## القيود المعروفة

- **`from . import x` في `__init__.apy` داخل حزمة** — الحل البديل: `import pkg.sub as sub`.
- **الوصول إلى السمات من `.py` إلى `.apy`** يجب أن يستخدم شكل المعرِّف المُطبَّع وفق ADR-0004 (مثل `module.قيمه` لا `module.قيمة`).

---

## خارطة الطريق

| المرحلة | المحتوى | الحالة |
|---|---|---|
| 0 | قرارات التصميم (8 سجلات ADR) | مكتملة |
| أ | اللهجة الأساسية: التجهيز المسبق، التطبيع، الترجمة، CLI، REPL، خطاف الاستيراد، رسائل الخطأ | مكتملة |
| ب | النظام البيئي: 40+ وحدة عربية، منسِّق، مدقِّق، نواة Jupyter، VS Code، دليل تعليمي | مكتملة |
| ج | معجم موحد، نشر PyPI، مكتبات تطبيقية، وتكاملات متقدمة | مكتملة |
| د | AI & Reach: ملعب ويب، AI aliases، ترجمة عكسية، stdlib canonical، أثر بثلاثة أوضاع | نشطة؛ D-002 إلى D-005 مشحونة |

انظر [`ROADMAP-PHASE-D.md`](ROADMAP-PHASE-D.md) و[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## الوثائق

| الوثيقة | الوصف |
|---------|--------|
| [دليل البدء الشامل](docs/ar/getting-started.md) | من "مرحبا بالعالم" إلى الاستيراد — خطوة بخطوة |
| [المعجم العربي الموحد](docs/ar/lexicon.md) | الكلمات المفتاحية والدوال والاستثناءات وأسماء المكتبات في مرجع واحد |
| [كتاب الوصفات](docs/ar/cookbook.md) | وصفات قائمة بذاتها قابلة للتشغيل المباشر |
| [مسرد المصطلحات](docs/ar/glossary.md) | مصطلحات مولدة من المعجم الموحد |
| [نظرة عامة على المشروع](docs/ar/README.md) | المعمارية، هيكل المشروع، خارطة الطريق |
| [ويكي المشروع](docs/wiki/index.md) | دليل شامل: الكلمات المفتاحية، المكتبات، الأدوات، الأسئلة الشائعة |
| [دليل المساهمة](CONTRIBUTING.md) | كيفية إضافة وحدات ومساهمات الكود |
| [سجل التغييرات](CHANGELOG.md) | ما الذي تغيّر في كل إصدار |
| [ميثاق المرحلة د](decisions/0012-phase-d-charter.md) | خطة D-001 إلى D-017 وحالة D-002 إلى D-005 |
| [خارطة الطريق](ROADMAP-PHASE-D.md) | حالة المرحلة الحالية وما بقي للصقل |

---

## الإقرارات والشكر

- **zhpy** (gasolin، 2014) — لهجة بايثون الصينية القائمة على التجزئة المعجمية التي يعتمد هذا المشروع معمارياً عليها.
- **قلب لـ Ramsey Nasser** — النقد الذي يأخذه هذا المشروع بجدية.
- **Hedy** — دليل على نجاح التعليم متعدد اللغات والمتدرج في النحو على نطاق واسع.
- **السوار / مجمع اللغة العربية (KSAA)** — واجهة برمجية للمعجم العربي تُستخدم في أبحاث المصطلحات.

</div>

---

# لغة الثعبان — Arabic Python (English summary)

> **The primary documentation above is in Arabic — the language this project is built for.**
> Below is a concise English reference for contributors and readers not yet fluent in Arabic.

A Python dialect where **keywords, built-ins, exceptions, and popular libraries** are all written in Arabic. `.apy` files are translated to standard Python at import time and executed by CPython — no interpreter fork, no language modification.

**Status (2026-05-03)**: Phases A-C complete; Phase D D-002 through D-005 are shipped, with visual playground examples and an Arabic Pygame alias. Full local verification with optional extras: **2960 passed, 23 intentionally skipped** on Python 3.13.

**License**: Apache-2.0.

---

## Install

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .          # installs the ثعبان console script
pip install -e ".[all]"   # dev, kernel, aliases, and AI optional targets
```

---

## Run

```bash
ثعبان script.apy          # run a file
ثعبان -c 'اطبع("مرحبا")'  # inline snippet
ثعبان                      # interactive REPL
ثعبان ترجمة-عكسية file.py # reverse-translate Python to .apy
ثعبان نسّق script.apy      # auto-format
ثعبان راجع script.apy      # lint
```

---

## Key facts

- generated lexicon source of truth for core words, aliases, messages, and docs
- Arabic traceback modes: `arabic`, `english`, `mixed`
- 31 stdlib alias modules · AI aliases for OpenAI, Anthropic, LangChain Core, Transformers, and Sentence Transformers · media/game aliases for Pillow and Pygame
- 38 Arabic exception names · translated common interpreter messages
- Formatter · Linter · Jupyter kernel · VS Code extension · pytest plugin — all ship in this repo
- Normalization: `أ/إ/آ → ا`, final `ة → ه`, final `ى → ي`

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Arabic commit messages are preferred. Larger work should include a spec packet or a clear issue, and any new Arabic term should start in `lexicon/`.

## Acknowledgements

zhpy (2014) · قلب by Ramsey Nasser · Hedy · Siwar/KSAA Arabic lexicon API.
