<div dir="rtl">

# قائمة فحص الإصدار

- حدّث `CHANGELOG.md` و`docs/ar/CHANGELOG.md`.
- شغّل مولد المعجم:

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

- اختبر التثبيت:

```bash
python -m pip install -e ".[dev]"
python -m pip install -e ".[kernel]"
python -m pip install -e ".[aliases]"
ثعبان --help
ثعبان --version
```

- راجع الأمثلة الاختيارية بحسب الاعتمادات المثبتة.

</div>
