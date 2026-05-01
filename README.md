<div dir="rtl">

# لغة الثعبان — بايثون بالعربية الكاملة

[![الاختبارات](https://img.shields.io/badge/اختبارات-2510_نجاح-brightgreen)](tests/)
[![بايثون](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)
[![الرخصة](https://img.shields.io/badge/رخصة-Apache--2.0-orange)](LICENSE)

لهجة برمجية تكتب فيها **الكلمات المفتاحية والدوال المدمجة والاستثناءات والمكتبات** بالعربية الكاملة. ملفات `.apy` تُترجم إلى بايثون القياسي في وقت التحميل وتُنفَّذ بواسطة CPython — دون تشعيب للمترجم ودون تعديل على اللغة الأصلية.

**الحالة (2026-05-01)**: المرحلة أ مكتملة. المرحلة ب مكتملة إلى حدٍّ بعيد — أكثر من **2700 اختبار ناجح** على Python 3.11–3.13 في Ubuntu وmacOS وWindows. 40+ وحدة عربية مُشحونة. منظومة أدوات متكاملة (منسّق + مدقّق + نواة Jupyter + امتداد VS Code).

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
اطبع("✓ تم حفظ التقرير")
```

```bash
$ ثعبان تحليل_مبيعات.apy
متوسط الإيرادات: 48750.32
✓ تم حفظ التقرير
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
pip install -e ".[dev]"
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
| [دليل البدء الموسَّع](docs/tutorial-ar.md) | الموازي العربي للدليل الإنجليزي مع مسرد المصطلحات (B-060) |
| [كتاب الوصفات العربي](docs/cookbook-ar.md) | عشر وصفات قصيرة قائمة بذاتها مع مسرد مصطلحات (B-061) |
| [نظرة عامة على المشروع](docs/ar/README.md) | المعمارية، هيكل المشروع، خارطة الطريق |
| [الأمثلة التعليمية](examples/README-ar.md) | شرح الأمثلة السبعة التصاعدية |
| [سجل التغييرات](docs/ar/CHANGELOG.md) | ما الذي تغيّر في كل إصدار |
| [قاموس الكلمات المفتاحية](dictionaries/ar-v1.md) | المرجع الكامل لكل الكلمات المفتاحية والدوال |

## المرحلة (ب): مفتوحة للمساهمات

اكتملت المرحلة (أ). المرحلة (ب) تضيف أسماء عربية لمكتبات بايثون الشهيرة (فلاسك، نمباي، وغيرها)، وتغطي المكتبة القياسية، وتحدّث القاموس بكلمات `async` و`match`. يوجد ٢٨ حزمة تنفيذية، ست منها مكتوبة بالكامل والباقي بانتظار من يكتب مواصفاتها.

- **خارطة الطريق:** [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md)
- **دليل المساهمة:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **حزمة جيدة للبدء:** [`specs/B-002-phase-a-compat-suite.md`](specs/B-002-phase-a-compat-suite.md)

</div>

---

## طرق التشغيل

```bash
ثعبان ملف.apy [مُعامِلات...]     # تشغيل ملف
ثعبان -c 'اطبع("مرحبا")'         # تنفيذ سطر مباشرةً
ثعبان - < ملف.apy                # قراءة من المدخل القياسي
ثعبان                             # البيئة التفاعلية REPL
ثعبان نسّق ملف.apy               # تنسيق الملف تلقائياً
ثعبان راجع ملف.apy               # فحص الجودة وإظهار التحذيرات
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

38 نوع استثناء قياسي و~30 رسالة مترجمة. الأنواع غير المعروفة تمر كما هي.

---

## الوحدات العربية — استيراد المكتبات بأسماء عربية

### المكتبة القياسية (21 وحدة)

| الاسم العربي | وحدة Python | الاسم العربي | وحدة Python |
|---|---|---|---|
| `نظام_تشغيل` | `os` | `رياضيات` | `math` |
| `مسار_مكتبه` | `pathlib` | `احصاء` | `statistics` |
| `نظام` | `sys` | `عشوائيات` | `random` |
| `مجموعات` | `collections` | `تسجيل` | `logging` |
| `ادوات_تكرار` | `itertools` | `اتزامن` | `asyncio` |
| `ادوات_داليه` | `functools` | `هاشلب` | `hashlib` |
| `مكتبة_تاريخ` | `datetime` | `مجاري` | `io` |
| `وقت_نظام` | `time` | `مدير_سياق` | `contextlib` |
| `روزنامه` | `calendar` | `قاعدة_بيانات` | `sqlite3` |
| `جيسون` | `json` | `تعابير_نمطيه` | `re` |
| `ملفات_csv` | `csv` | | |

### علوم وبيانات (6 حزم)

| الاسم العربي | حزمة Python |
|---|---|
| `نمباي` | `numpy` |
| `بانداس` | `pandas` |
| `رسوم_بيانيه` | `matplotlib` |
| `سيبورن` | `seaborn` |
| `سايباي` | `scipy` |
| `تعلم_آلي` | `scikit-learn` |

### ويب وشبكات (4 حزم)

| الاسم العربي | حزمة Python |
|---|---|
| `فلاسك` | `flask` |
| `طلبات` | `requests` |
| `أيو_هتب` | `aiohttp` |
| `فاست_أبي` | `fastapi` |

## طبقة الأدوات

| الأداة | الأمر | الوصف |
|---|---|---|
| **المنسِّق** | `ثعبان نسّق ملف.apy` | تنسيق تلقائي: المسافات البادئة، والتباعد، وأسلوب التعليقات |
| **المدقِّق** | `ثعبان راجع ملف.apy` | تشخيصات: W001–W004، E001، I001 |
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
from arabicpython.formatter import format_source, format_file
from arabicpython.linter import lint_source, Diagnostic
```

---

## هيكل المشروع

```
lughat-althuban/
├── arabicpython/              حزمة المحوِّل
│   ├── aliases/               تعيينات TOML (40+ وحدة)
│   ├── formatter.py           المنسِّق التلقائي
│   └── linter.py              محرك التدقيق والتشخيص
├── arabicpython_kernel/       حزمة نواة Jupyter
├── editors/vscode/            امتداد VS Code
├── tools/                     مولد القواعد النحوية وأدوات التطوير
├── decisions/                 سجلات قرارات المعمارية (ADRs)
├── dictionaries/              مرجع الكلمات المفتاحية ar-v1
├── specs/                     حزم المواصفات للتنفيذ
├── tests/                     مجموعة pytest (أكثر من 2700 نجاح)
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
| 0 | قرارات التصميم (8 سجلات ADR) | ✅ مكتملة |
| أ | اللهجة الأساسية: التجهيز المسبق، التطبيع، الترجمة، CLI، REPL، خطاف الاستيراد، رسائل الخطأ | ✅ مكتملة |
| ب | النظام البيئي: 40+ وحدة عربية، منسِّق، مدقِّق، نواة Jupyter، VS Code، دليل تعليمي | 🟡 **مكتملة إلى حدٍّ بعيد — المساهمون مرحب بهم** |
| ج | متقدم: خادم LSP، ملعب ويب، تكامل مدير الحزم | 📋 مخطط لها |

انظر [`ROADMAP-PHASE-B.md`](ROADMAP-PHASE-B.md) و[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## الوثائق

| الوثيقة | الوصف |
|---------|--------|
| [دليل البدء الشامل](docs/ar/getting-started.md) | من "مرحبا بالعالم" إلى الاستيراد — خطوة بخطوة |
| [دليل البدء الموسَّع](docs/tutorial-ar.md) | شرح تفصيلي كامل مع أمثلة وتسلسل هندسي (B-060) |
| [كتاب الوصفات](docs/cookbook-ar.md) | عشر وصفات قائمة بذاتها قابلة للتشغيل المباشر |
| [مسرد المصطلحات](docs/tutorial-ar-glossary.md) | 35+ مصطلح حاسوبي بتعريفات عربية فصيحة |
| [نظرة عامة على المشروع](docs/ar/README.md) | المعمارية، هيكل المشروع، خارطة الطريق |
| [مرجع المكتبة القياسية](docs/ar/stdlib-reference.md) | جميع الوحدات القياسية العربية مع أمثلة |
| [ويكي المشروع](docs/wiki/index.md) | دليل شامل: الكلمات المفتاحية، المكتبات، الأدوات، الأسئلة الشائعة |
| [دليل المساهمة](CONTRIBUTING.md) | كيفية إضافة وحدات ومساهمات الكود |
| [سجل التغييرات](CHANGELOG.md) | ما الذي تغيّر في كل إصدار |
| [خارطة الطريق](ROADMAP-PHASE-B.md) | الحزم القادمة وحالتها |

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

**Status (2026-04-28)**: Phase A complete. Phase B substantially complete — **2,510 tests passing** across Python 3.11–3.13 on Ubuntu / macOS / Windows.

**License**: Apache-2.0.

---

## Install

```bash
git clone https://github.com/GalaxyRuler/lughat-althuban
cd lughat-althuban
pip install -e .          # installs the ثعبان console script
pip install -e ".[dev]"   # all optional library aliases
```

---

## Run

```bash
ثعبان script.apy          # run a file
ثعبان -c 'اطبع("مرحبا")'  # inline snippet
ثعبان                      # interactive REPL
ثعبان نسّق script.apy      # auto-format
ثعبان راجع script.apy      # lint
```

---

## Key facts

- 38 Arabic exception names · ~30 translated interpreter messages
- 21 stdlib alias modules · 6 science/data · 4 web · 1 ML (40+ total)
- Formatter · Linter · Jupyter kernel · VS Code extension · pytest plugin — all ship in this repo
- Normalization: `أ/إ/آ → ا`, final `ة → ه`, final `ى → ي`

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Arabic commit messages are preferred. Every unit of work is a self-contained spec packet in `specs/`.

## Acknowledgements

zhpy (2014) · قلب by Ramsey Nasser · Hedy · Siwar/KSAA Arabic lexicon API.
