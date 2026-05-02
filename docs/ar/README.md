<div dir="rtl">

# لغة الثعبان (lughat-althuban)

لغة الثعبان هي لهجة برمجة مبنية بالكامل باللغة العربية، تتيح للمطورين كتابة شفرات برمجية باستخدام كلمات مفتاحية ودوال مدمجة ووحدات قياسية ومكتبات شهيرة عربية بحتة. يعتمد المشروع على محرك Python القياسي (CPython)، مما يضمن توافقاً كاملاً مع بيئة Python مع توفير تجربة برمجة أصيلة للناطقين بالعربية.

**الحالة (2026-05-02)**: 2926 اختباراً ناجحاً في بيئة `.[all]` — المراحل أ/ب/ج مكتملة — عمل المرحلة د D-002 إلى D-005 مشحون.

---

## نظرة سريعة

```python
# تحليل_بيانات.apy — برنامج تحليل بيانات كامل بالعربية
استورد بانداس باسم بد        # pandas
استورد نمباي باسم نم        # numpy
استورد سيبورن باسم رسم       # seaborn

بيانات = بد.قراءة_جيسون("data.json")
متوسط  = نم.متوسط(بيانات["الدرجات"])
اطبع(f"متوسط الدرجات: {متوسط:.1f}")

رسم.ضبط_موضوع("whitegrid")
رسم.خط_بياني(data=بيانات, x="الطالب", y="الدرجات")
```

---

## الحالة الراهنة

| البند | القيمة |
|-------|--------|
| الاختبارات | 2926 نجاحاً، 23 تخطياً مقصوداً خاصاً بإصدار Python أو مقتطفات غير قابلة للتشغيل |
| مصدر الحقيقة | `lexicon/core.toml`، `lexicon/libraries.toml`، `lexicon/messages.toml` |
| وحدات stdlib | 31 وحدة مولدة من `lexicon/libraries.toml` |
| مكتبات علمية | numpy، pandas، matplotlib، seaborn، scipy، scikit-learn |
| مكتبات ويب | flask، requests، aiohttp، fastapi، django، httpx |
| ذكاء اصطناعي | openai، anthropic، langchain-core، transformers، sentence-transformers |
| أدوات | مترجم عكسي + أثر بثلاثة أوضاع + منسّق + مدقّق + نواة Jupyter + VS Code |

---

## طرق التشغيل

```bash
ثعبان ملف.apy              # تشغيل ملف
ثعبان -c 'اطبع("مرحبا")'   # سطر مباشر
ثعبان                       # البيئة التفاعلية
ثعبان ترجمة-عكسية ملف.py    # تحويل Python إلى .apy
ثعبان نسّق ملف.apy          # تنسيق تلقائي
ثعبان راجع ملف.apy          # فحص الجودة
```

---

## فهرس الوحدات

### المكتبة القياسية (31 وحدة)

| الاسم العربي | الوحدة الأصلية | الاسم العربي | الوحدة الأصلية |
| --- | --- | --- | --- |
| نظام | os | رياضيات | math |
| مسار | pathlib | احصاء | statistics |
| نظام_بايثون | sys | عشوائي | random |
| مجموعات | collections | تسجيل | logging |
| ادوات_تكرار | itertools | اتزامن | asyncio |
| ادوات_دوال | functools | تشفير | hashlib |
| تاريخ_وقت | datetime | ادخال_اخراج | io |
| وقت_نظام | time | مدير_سياق | contextlib |
| روزنامه | calendar | قاعدة_بيانات | sqlite3 |
| جيسون | json | تعابير | re |
| ملف_csv | csv | تنميط | typing |
| خيوط | threading | مسار_نظام | os.path |
| نصوص | string | تنسيق_نص | textwrap |
| عملية_فرعية | subprocess | ادوات_ملفات | shutil |
| محلل_وسائط | argparse | اسرار | secrets |
| معرف_فريد | uuid | — | — |

### العلوم والبيانات

| الاسم العربي | الوحدة | الاسم العربي | الوحدة |
| --- | --- | --- | --- |
| نمباي | numpy | سيبورن | seaborn |
| بانداس | pandas | سايباي | scipy |
| رسوم_بيانيه | matplotlib | تعلم_آلي | scikit-learn |

### الذكاء الاصطناعي

| الاسم العربي | الوحدة |
| --- | --- |
| ذكاء_مفتوح | openai |
| كلود_عربي | anthropic |
| سلسلة_لغه | langchain_core |
| محولات | transformers |
| محولات_جمل | sentence_transformers |

### الويب والشبكات

| الاسم العربي | الوحدة |
| --- | --- |
| فلاسك | flask |
| طلبات | requests |
| أيو_هتب | aiohttp |
| فاست_أبي | fastapi |
| دجانغو | django |
| طلبات_حديثه | httpx |

---

## روابط هامة

- [دليل البدء الشامل](getting-started.md)
- [المعجم العربي الموحد](lexicon.md)
- ملاحق مشتقة: [مسرد المصطلحات الأساسي](glossary.md)، [مرجع المكتبة القياسية](stdlib-reference.md)، [فهرس أسماء المكتبات](aliases-index.md)
- [سياسة التسمية العربية](naming-policy.md)
- [سياسة أسماء المكتبات](alias-policy.md)
- [سياسة الاستثناءات](exception-policy.md)
- [التطبيع وسلامة اتجاه النص](normalization-and-bidi.md)
- [استكشاف الأخطاء](troubleshooting.md)
- [الحدود المعروفة](known-limitations.md)
- [دليل المعلم](educator-guide.md)
- [قائمة فحص الإصدار](release-checklist.md)
- [مصفوفة التغطية](coverage-matrix.md)
- [ويكي المشروع](../wiki/index.md)
- [دليل المساهمة](../../CONTRIBUTING.md)
- [سجل التغييرات](CHANGELOG.md)
- [ميثاق المرحلة د](../../decisions/0012-phase-d-charter.md)
- [خارطة الطريق الحالية](../../ROADMAP-PHASE-D.md)
- [خارطة المرحلة ج التاريخية](../../ROADMAP-PHASE-C.md)

</div>
