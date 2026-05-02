<div dir="rtl">

# سياسة الاستثناءات والأثر

أسماء الاستثناءات ورسائل الأثر جزء من طبقة المعجم، وليست جداول يدوية داخل وقت التشغيل.

- أسماء فئات الاستثناءات تأتي من `lexicon/core.toml`.
- قوالب رسائل CPython وأنماطها تأتي من `lexicon/messages.toml`.
- الملفان `arabicpython/_generated_traceback_data.py` و`arabicpython/_generated_messages.py` ناتجان مولدان؛ لا تعدلهما باليد.

## القواعد

- استخدم `خطأ_...` للاستثناءات التي تنتهي بـ `Error`.
- استخدم `تحذير_...` لفئات `Warning`.
- لا تعرض إطار تشغيل داخلي من `arabicpython/cli.py` في أثر برنامج المستخدم.
- اترك أسماء Python التقنية داخل الرسالة عندما تكون جزءا من خطأ CPython، مثل `list` أو `bytes`.
- أضف قالب رسالة فقط عندما يكون النص شائعا ومفهوما بالعربية.

## أوضاع الأثر

يدعم سطر الأوامر ثلاثة أوضاع:

| الوضع | السلوك |
|-------|--------|
| `arabic` | أسماء الاستثناءات والرسائل بالعربية قدر الإمكان |
| `english` | أثر CPython الأصلي دون ترجمة |
| `mixed` | إطار وأسماء استثناءات عربية، مع رسالة CPython الأصلية |

يمكن اختيار الوضع عبر:

```bash
ثعبان --tracebacks=arabic ملف.apy
ثعبان --tracebacks=english ملف.apy
ثعبان --tracebacks=mixed ملف.apy
```

أو عبر المتغير:

```bash
PYTHONTRACEBACK=mixed ثعبان ملف.apy
```

## تحقق سريع

```bash
ثعبان -c "1 / 0"
ثعبان --tracebacks=mixed -c "1 / 0"
python -m pytest tests/test_tracebacks.py tests/test_tracebacks_arabic.py
```

</div>
