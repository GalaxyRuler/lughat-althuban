import importlib
import sys

import pytest

from arabicpython.cli import main
from arabicpython.dialect import load_dialect
from arabicpython.import_hook import install
from arabicpython.linter import lint_source
from arabicpython.normalize import normalize_identifier
from arabicpython.translate import translate

AR_V2_PROGRAM = """# apython: dict=ar-v2
عدد = 0
بينما عدد < 2:
    عدد += 1

حاول:
    ارفع خطا_قيمة("تمام")
استثناء خطا_قيمة باسم مشكلة:
    رسالة = مشكلة.args[0]

شيء = لاشيء
إذا شيء يكون لاشيء:
    تجاوز

اطبع(رسالة)
اطبع(عدد)
"""


AR_V1_PROGRAM = """عدد = 0
طالما عدد < 2:
    عدد += 1

حاول:
    ارفع خطا_قيمة("تمام")
استثناء خطا_قيمة كـ مشكلة:
    رسالة = مشكلة.args[0]

شيء = لاشيء
إذا شيء هو لاشيء:
    مرر

اطبع(رسالة)
اطبع(عدد)
"""


def test_ar_v2_file_using_all_four_new_keywords_executes(tmp_path, capsys):
    path = tmp_path / "v2_program.apy"
    path.write_text(AR_V2_PROGRAM, encoding="utf-8")

    assert main([str(path)]) == 0
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "تمام\n2\n"


def test_ar_v2_file_using_old_spelling_raises_clear_error():
    source = "# apython: dict=ar-v2\nطالما صحيح:\n    تجاوز\n"

    with pytest.raises(SyntaxError) as exc:
        translate(source)

    assert "الكلمة 'طالما' غير معرّفة في ar-v2؛ استخدم 'بينما'" in str(exc.value)


def test_ar_v1_file_still_works_without_opt_in(tmp_path, capsys):
    path = tmp_path / "v1_program.apy"
    path.write_text(AR_V1_PROGRAM, encoding="utf-8")

    assert main([str(path)]) == 0
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "تمام\n2\n"


def test_load_dialect_ar_v2_returns_revised_mapping_only():
    ar_v1 = load_dialect("ar-v1")
    ar_v2 = load_dialect("ar-v2")

    assert ar_v2.names[normalize_identifier("باسم")] == "as"
    assert ar_v2.names[normalize_identifier("تجاوز")] == "pass"
    assert ar_v2.names[normalize_identifier("بينما")] == "while"
    assert ar_v2.names[normalize_identifier("يكون")] == "is"

    for old in ("كـ", "مرر", "طالما", "هو"):
        assert normalize_identifier(old) not in ar_v2.names

    changed = {"as", "pass", "while", "is"}
    for python_symbol, ar_v1_canonical in ar_v1.reverse_names.items():
        if python_symbol not in changed:
            assert ar_v2.reverse_names[python_symbol] == ar_v1_canonical

    assert dict(ar_v1.attributes) == dict(ar_v2.attributes)
    assert len(ar_v1.names) == len(ar_v2.names)


def test_import_hook_honors_ar_v2_file_directive(tmp_path):
    module_path = tmp_path / "uses_ar_v2.apy"
    module_path.write_text(
        "# apython: dict=ar-v2\n" "عدد = 0\n" "بينما عدد < 1:\n" "    عدد += 1\n" "نتيجة = عدد\n",
        encoding="utf-8",
    )

    old_meta_path = sys.meta_path[:]
    old_path = sys.path[:]
    try:
        sys.path.insert(0, str(tmp_path))
        install()
        module = importlib.import_module("uses_ar_v2")
        assert getattr(module, normalize_identifier("نتيجة")) == 1
    finally:
        sys.meta_path[:] = old_meta_path
        sys.path[:] = old_path
        sys.modules.pop("uses_ar_v2", None)
        importlib.invalidate_caches()


def test_linter_e001_flags_all_changed_keywords_in_ar_v2_files():
    source = "# apython: dict=ar-v2\nكـ\nمرر\nطالما صحيح:\n    تجاوز\nهو = 1\n"

    messages = [diag.message for diag in lint_source(source) if diag.code == "E001"]
    assert messages == [
        "الكلمة 'كـ' غير معرّفة في ar-v2؛ استخدم 'باسم'",
        "الكلمة 'مرر' غير معرّفة في ar-v2؛ استخدم 'تجاوز'",
        "الكلمة 'طالما' غير معرّفة في ar-v2؛ استخدم 'بينما'",
        "الكلمة 'هو' غير معرّفة في ar-v2؛ استخدم 'يكون'",
    ]
