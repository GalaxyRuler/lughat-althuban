<div dir="rtl">

# قائمة فحص الإصدار

- حدّث `CHANGELOG.md` و`docs/ar/CHANGELOG.md`.
- ثبّت بيئة التحقق الكاملة قبل العد النهائي للاختبارات:

```bash
python -m pip install -e ".[all]"
```

- شغّل مولد المعجم. أي تغيير في `lexicon/` يجب أن يمر عبر المولد، لا عبر تعديل الملفات الناتجة:

```bash
python tools/generate_lexicon_outputs.py
python tools/generate_lexicon_outputs.py --check
```

- شغّل التحقق:

```bash
python tools/validate_lexicon.py
ruff check .
black --check .
python -m pytest
```

- اختبر أوامر الواجهة الأساسية وإضافات المرحلة د:

```bash
ثعبان --help
ثعبان --version
ثعبان ترجمة-عكسية --help
ثعبان --tracebacks=arabic -c "1 / 0"
ثعبان --tracebacks=mixed -c "1 / 0"
```

- راجع أن ملفات `arabicpython/aliases/*.toml`، و`docs/ar/lexicon.md`، و`docs/ar/aliases-index.md` تحمل ترويسة التوليد ولا تحتوي تعديلات يدوية.
- راجع الأمثلة الاختيارية بحسب الاعتمادات المثبتة. للتحقق من حزمة AI المنشورة فقط:

```bash
python -m pip install -e ".[ai]"
python -m pytest tests/aliases/test_anthropic.py tests/aliases/test_openai.py tests/aliases/test_transformers.py
```

- في بيئة Python 3.13 مع `.[all]` كان خط الأساس بعد إضافة أمثلة الملعب المرئية: `2960 passed, 23 skipped`. التخطي المتبقي خاص بإصدار Python أو مقتطفات تعليمية غير قابلة للتشغيل، لا بمكتبات اختيارية ناقصة.

</div>
