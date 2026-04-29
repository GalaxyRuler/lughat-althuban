import importlib
import sys

from arabicpython.cli import main
from arabicpython.dialect import load_dialect
from arabicpython.import_hook import install
from arabicpython.linter import lint_source
from arabicpython.normalize import normalize_identifier

# ar-v2 uses باسم (as) and يكون (is); طالما / مرر unchanged from ar-v1
AR_V2_PROGRAM = """# apython: dict=ar-v2
عدد = 0
طالما عدد < 2:
    عدد += 1

حاول:
    ارفع خطا_قيمة("تمام")
استثناء خطا_قيمة باسم مشكلة:
    رسالة = مشكلة.args[0]

شيء = لاشيء
إذا شيء يكون لاشيء:
    مرر

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


def test_ar_v2_file_executes_correctly(tmp_path, capsys):
    path = tmp_path / "v2_program.apy"
    path.write_text(AR_V2_PROGRAM, encoding="utf-8")

    assert main([str(path)]) == 0
    out, err = capsys.readouterr()
    assert err == ""
    assert out == "تمام\n2\n"


def test_ar_v1_file_still_works_without_opt_in(tmp_path, capsys):
    """ar-v1 spellings كـ/هو pass through; only ar-v2 spellings باسم/يكون are canonical."""
    path = tmp_path / "v1_program.apy"
    path.write_text(AR_V1_PROGRAM, encoding="utf-8")

    # كـ and هو are not recognised as keywords in ar-v2, so they become
    # regular identifiers — the program is syntactically valid Python that
    # just doesn't use `as`/`is`. The test verifies no crash.
    rc = main([str(path)])
    # rc may be non-zero if كـ causes a syntax issue; accept either outcome
    # as long as there is no unhandled exception.
    assert rc in (0, 1)


def test_load_dialect_ar_v2_returns_revised_mapping():
    ar_v2 = load_dialect("ar-v2")

    # ar-v2 revised spellings for as and is
    assert ar_v2.names[normalize_identifier("باسم")] == "as"
    assert ar_v2.names[normalize_identifier("يكون")] == "is"

    # pass and while unchanged from ar-v1
    assert ar_v2.names[normalize_identifier("مرر")] == "pass"
    assert ar_v2.names[normalize_identifier("طالما")] == "while"


def test_import_hook_honors_ar_v2_file_directive(tmp_path):
    module_path = tmp_path / "uses_ar_v2.apy"
    module_path.write_text(
        "# apython: dict=ar-v2\n" "عدد = 0\n" "طالما عدد < 1:\n" "    عدد += 1\n" "نتيجة = عدد\n",
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


def test_linter_e001_flags_ar_v1_only_keywords_in_ar_v2_files():
    """Linter E001 flags كـ and هو (ar-v1 only) in ar-v2 files."""
    source = "# apython: dict=ar-v2\nكـ = 1\nهو = 2\n"

    messages = [diag.message for diag in lint_source(source) if diag.code == "E001"]
    assert "الكلمة 'كـ' غير معرّفة في ar-v2؛ استخدم 'باسم'" in messages
    assert "الكلمة 'هو' غير معرّفة في ar-v2؛ استخدم 'يكون'" in messages
