import sys

from arabicpython import cli
from arabicpython.tracebacks import format_exception, translate_exception_message


def test_name_error_message_pattern():
    assert translate_exception_message("name 'x' is not defined") == "الاسم 'x' غير معرّف"


def test_zero_division_message_pattern():
    assert translate_exception_message("division by zero") == "القسمة على صفر"


def test_index_error_message_pattern():
    assert translate_exception_message("list index out of range") == "فهرس القائمة خارج النطاق"


def test_format_exception_english_mode():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_exception(*sys.exc_info(), mode="english")
    assert "Traceback" in output
    assert "ZeroDivisionError: division by zero" in output


def test_format_exception_mixed_mode():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_exception(*sys.exc_info(), mode="mixed")
    assert "خطأ_قسمة_صفر: division by zero" in output


def test_cli_tracebacks_english_flag(tmp_path, capsys):
    path = tmp_path / "err.apy"
    path.write_text("1 / 0\n", encoding="utf-8")
    assert cli.main(["--tracebacks", "english", str(path)]) == 1
    _, err = capsys.readouterr()
    assert "Traceback" in err
    assert "ZeroDivisionError: division by zero" in err


def test_cli_tracebacks_env(tmp_path, capsys, monkeypatch):
    path = tmp_path / "err.apy"
    path.write_text("1 / 0\n", encoding="utf-8")
    monkeypatch.setenv("PYTHONTRACEBACK", "mixed")
    assert cli.main([str(path)]) == 1
    _, err = capsys.readouterr()
    assert "خطأ_قسمة_صفر: division by zero" in err
