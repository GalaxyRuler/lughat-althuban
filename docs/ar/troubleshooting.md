<div dir="rtl">

# استكشاف الأخطاء

## لا يظهر الأمر `ثعبان`

تحقق من تثبيت الحزمة في البيئة نفسها:

```bash
python -m pip install -e .
ثعبان --version
```

على Windows قد تحتاج إلى فتح طرفية جديدة بعد التثبيت.

## تظهر رسائل ترميز في أوامر pip على Windows

بعض الطرفيات القديمة تستخدم `cp1252` ولا تطبع الوصف العربي للحزمة. استخدم:

```powershell
$env:PYTHONUTF8="1"
$env:PYTHONIOENCODING="utf-8"
python -m pip show lughat-althuban
```

## لا يعمل اسم مكتبة عربي

راجع [فهرس الأسماء العربية للمكتبات](aliases-index.md). إذا لم يظهر الاسم هناك فهو غير مشحون، حتى لو ظهر في وثيقة قديمة.

مصدر الحقيقة للأسماء هو `lexicon/libraries.toml`. لا تعدّل ملفات `arabicpython/aliases/*.toml` مباشرة؛ شغّل المولد بعد تعديل المعجم:

```bash
python tools/generate_lexicon_outputs.py
python tools/validate_lexicon.py
```

بعض الأسماء القديمة محفوظة كأسماء استيراد توافقية عندما لا يوجد تعارض، مثل `نظام_تشغيل` لـ`os` و`صور` لـ`PIL.Image`. الاسم المعتمد يظهر أولا في الفهرس.

## مكتبة اختيارية مفقودة

ثبّت الحزمة المناسبة داخل البيئة نفسها. أثناء التطوير، أسرع خيار لتشغيل الاختبارات الاختيارية كلها:

```bash
python -m pip install -e ".[all]"
```

ولحزمة AI فقط:

```bash
python -m pip install -e ".[ai]"
```

تغطي `.[ai]` الأسماء العربية لـ`openai`، و`anthropic`، و`langchain_core`، و`transformers`، و`sentence_transformers`.

## يفشل ملف يستخدم `كـ`

القاموس النشط `ar-v2` يستخدم `باسم`. عدّل:

```python
استورد بانداس باسم بد
```

## أريد أثر الأخطاء بالإنجليزية أو المختلط

الافتراضي هو `arabic`. استخدم أحد الأوضاع الثلاثة:

```bash
ثعبان --tracebacks=arabic ملف.apy
ثعبان --tracebacks=english ملف.apy
ثعبان --tracebacks=mixed ملف.apy
```

أو:

```bash
PYTHONTRACEBACK=mixed ثعبان ملف.apy
```

## كيف أعكس ملف Python إلى لغة الثعبان؟

استخدم المترجم العكسي:

```bash
ثعبان ترجمة-عكسية script.py --stdout
ثعبان ترجمة-عكسية script.py --level=3
```

</div>
