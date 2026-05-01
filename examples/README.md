<div dir="rtl">

# فهرس الأمثلة

كل ملف `.apy` هنا قابل للترجمة مباشرة بالقاموس النشط `ar-v2`، ما عدا مثال المدقّق `B56_linter_demo.apy` الذي يتعمد إدخال الصيغة القديمة `كـ` لعرض التشخيص `E001`.

## الأساسيات

| الملف | يوضح | الأمر |
|---|---|---|
| `01_hello.apy` | الطباعة والنصوص | `ثعبان examples/01_hello.apy` |
| `02_arithmetic.apy` | الحساب والمتغيرات | `ثعبان examples/02_arithmetic.apy` |
| `03_control_flow.apy` | `إذا`، `لكل`، `مدى` | `ثعبان examples/03_control_flow.apy` |
| `04_functions.apy` | `دالة` و`ارجع` | `ثعبان examples/04_functions.apy` |
| `05_data_structures.apy` | القوائم والقواميس | `ثعبان examples/05_data_structures.apy` |
| `06_classes.apy` | الأصناف والطرق | `ثعبان examples/06_classes.apy` |
| `07_imports.apy` | استيراد ملفات `.apy` | `ثعبان examples/07_imports.apy` |
| `helper.apy` | وحدة مساعدة يستوردها `07_imports.apy` | لا يشغّل وحده |

## المكتبة القياسية والأدوات

| الملف | يوضح | المتطلبات |
|---|---|---|
| `B30_filesystem_walk.apy` | الملفات والمسارات | مدمج |
| `B31_functional_data.apy` | أدوات الدوال والتكرار | مدمج |
| `B32_datetime_math.apy` | التاريخ والوقت | مدمج |
| `B33_data_storage.apy` | JSON وCSV وSQLite | مدمج |
| `B34_text_processing.apy` | التعابير النمطية | مدمج |
| `B35_numerics.apy` | الرياضيات والإحصاء | مدمج |
| `B37_async_demo.apy` | `غير_متزامن` و`انتظر` | مدمج |
| `B40_match_demo.apy` | `طابق` و`حالة` | Python 3.11+ |
| `B55_formatter_demo.apy` | المنسق | الحزمة نفسها |
| `B56_linter_demo.apy` | المدقق وتشخيص الصيغ القديمة | الحزمة نفسها |

## مكتبات اختيارية

ثبّت المجموعة الواسعة بالأمر:

```bash
python -m pip install -e ".[aliases]"
```

| الملف | المكتبة | ملاحظة |
|---|---|---|
| `B57_seaborn_demo.apy` | `seaborn`, `matplotlib` | يرسم ثم يغلق المخطط |
| `B58_scipy_demo.apy` | `scipy`, `numpy` | حوسبة علمية محلية |
| `B59_aiohttp_demo.apy` | `aiohttp` | يستخدم الشبكة للوصول إلى httpbin |
| `C10_matplotlib_demo.apy` | `matplotlib` | رسم بياني |
| `C11_sklearn_demo.apy` | `scikit-learn` | تعلم آلي صغير |
| `C12_pydantic_demo.apy` | `pydantic` | نماذج تحقق |
| `C13_httpx_demo.apy` | `httpx` | طلبات HTTP |
| `C20_openpyxl_demo.apy` | `openpyxl` | ملفات Excel |
| `C21_docx_demo.apy` | `python-docx` | مستندات Word |

## اختبار سريع

```bash
python -m pytest tests/test_examples.py
```

</div>
