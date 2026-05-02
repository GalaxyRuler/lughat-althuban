<div dir="rtl">

# مصفوفة التغطية

| السطح | الدليل الحالي | الاختبار |
|---|---|---|
| القاموس الأساسي | `lexicon/core.toml` | `tests/test_lexicon.py` |
| نسخ القواميس | `arabicpython/dictionaries/` و`dictionaries/` | `tools/validate_lexicon.py` |
| الأسماء العربية للمكتبات | `lexicon/libraries.toml` | `tools/validate_lexicon.py` و`tests/test_aliases_toml_invariants.py` |
| ملفات aliases المولدة | `arabicpython/aliases/*.toml` | `python tools/generate_lexicon_outputs.py --check` |
| رسائل الأدوات | `lexicon/messages.toml` و`arabicpython/_generated_messages.py` | `tools/validate_lexicon.py` |
| الأثر العربي | `lexicon/core.toml` و`lexicon/messages.toml` و`arabicpython/tracebacks.py` | `tests/test_tracebacks.py` و`tests/test_tracebacks_arabic.py` |
| المترجم العكسي | `arabicpython/reverse.py` | `tests/test_reverse.py` |
| أسماء AI | `lexicon/libraries.toml`، مجموعة `ai` الاختيارية | `tests/aliases/test_anthropic.py` وما يقابلها |
| أسماء stdlib المعتمدة | `lexicon/libraries.toml` | `tests/aliases/test_phase_d_stdlib.py` |
| CLI | `arabicpython/cli.py` | `tests/test_cli.py` |
| المنسق | `arabicpython/formatter.py` | `tests/test_formatter.py` |
| المدقق | `arabicpython/linter.py` | `tests/test_linter.py` |
| نواة Jupyter | `arabicpython_kernel/` | `tests/test_jupyter_kernel.py` |
| VS Code | `editors/vscode/` | `tests/test_vscode_extension.py` |
| الأمثلة | `examples/` | `tests/test_examples.py` |

آخر تحقق كامل في بيئة `pip install -e ".[all]"`: `2926 passed, 23 skipped, 1 warning`.
التخطيات المتبقية مرتبطة بمسارات Python 3.11 أو مقتطفات تعليمية موسومة بأنها غير قابلة للتشغيل، وليست مكتبات ناقصة.

</div>
