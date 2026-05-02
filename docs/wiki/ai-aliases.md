<div dir="rtl">

# مكتبات الذكاء الاصطناعي — AI Aliases

أسماء AI في لغة الثعبان مولدة من `lexicon/libraries.toml`. ملفات `arabicpython/aliases/openai.toml` وأخواتها ناتجة من المعجم ولا تعدل باليد.

## التثبيت

```bash
python -m pip install -e ".[ai]"
```

أو لتشغيل كل الاختبارات الاختيارية محليا:

```bash
python -m pip install -e ".[all]"
```

## جدول المكتبات

| الاسم العربي | Python | أمثلة من الأسماء العربية |
|--------------|--------|--------------------------|
| `ذكاء_مفتوح` | `openai` | `عميل`، `عميل_غير_متزامن`، `تضمين`، `خطا_api` |
| `كلود_عربي` | `anthropic` | `عميل`، `رساله`، `رسائل`، `خطا_مصادقه_ai` |
| `سلسلة_لغه` | `langchain_core` | `رساله_انسان`، `قالب_موجه`، `قابل_تشغيل` |
| `محولات` | `transformers` | `نموذج_تلقائي`، `مرمز_تلقائي`، `خط_انابيب` |
| `محولات_جمل` | `sentence_transformers` | `محول_جمل`، `تشابه_جيب_تمام`، `بحث_دلالي` |

## أمثلة

```python
استورد ذكاء_مفتوح

اطبع(ذكاء_مفتوح.عميل)
اطبع(ذكاء_مفتوح.خطا_api)
```

```python
استورد كلود_عربي

اطبع(كلود_عربي.عميل)
اطبع(كلود_عربي.رساله)
```

```python
استورد محولات

اطبع(محولات.مرمز_تلقائي)
اطبع(محولات.خط_انابيب)
```

```python
استورد محولات_جمل

اطبع(محولات_جمل.محول_جمل)
اطبع(محولات_جمل.تشابه_جيب_تمام)
```

## تحقق

```bash
python -m pytest tests/aliases/test_openai.py tests/aliases/test_anthropic.py
python -m pytest tests/aliases/test_langchain_core.py tests/aliases/test_transformers.py tests/aliases/test_sentence_transformers.py
```

</div>

---

# AI Aliases (English summary)

AI aliases are authored in `lexicon/libraries.toml` and generated into runtime TOMLs.

| Arabic import | Python module |
|---|---|
| `ذكاء_مفتوح` | `openai` |
| `كلود_عربي` | `anthropic` |
| `سلسلة_لغه` | `langchain_core` |
| `محولات` | `transformers` |
| `محولات_جمل` | `sentence_transformers` |

Install with `pip install -e ".[ai]"`, or `pip install -e ".[all]"` for the full optional test environment.
