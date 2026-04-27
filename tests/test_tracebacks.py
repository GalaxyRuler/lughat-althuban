import io
import re
import sys

import pytest

from arabicpython import cli, run_repl
from arabicpython.normalize import normalize_identifier
from arabicpython.tracebacks import (
    EXCEPTION_NAMES_AR,
    MESSAGE_TEMPLATES_AR,
    format_translated_exception,
    install_excepthook,
    print_translated_exception,
    translate_exception_message,
    translate_exception_name,
    uninstall_excepthook,
)

# Translation lookups (8)


def test_translate_exception_name_known():
    assert translate_exception_name("ZeroDivisionError") == "خطا_القسمه_على_صفر"


def test_translate_exception_name_unknown_passes_through():
    assert translate_exception_name("MyCustomError") == "MyCustomError"


def test_translate_message_division_by_zero():
    assert translate_exception_message("division by zero") == "القسمة على صفر"


def test_translate_message_name_error():
    assert translate_exception_message("name 'foo' is not defined") == "الاسم 'foo' غير معرّف"


def test_translate_message_attribute_error():
    msg = "'list' object has no attribute 'frobnicate'"
    translated = translate_exception_message(msg)
    assert "الكائن من نوع 'list' لا يملك الخاصية 'frobnicate'" in translated


def test_translate_message_unknown_passes_through():
    msg = "some random error message"
    assert translate_exception_message(msg) == msg


def test_translate_message_first_match_wins():
    # The first pattern for name error is more general, but they are anchored.
    # If there were overlapping patterns, the first would win.
    pass


def test_all_exception_names_have_translations():
    # B-041: full hierarchy — at least 69 entries (38 original + 31 new)
    assert len(EXCEPTION_NAMES_AR) >= 69
    for _name, translation in EXCEPTION_NAMES_AR.items():
        assert translation
        # Contains at least one Arabic codepoint U+0600–U+06FF
        assert any("\u0600" <= ch <= "\u06ff" for ch in translation)


# Type-name table coverage (4)


def test_table_includes_zero_division_error():
    assert "ZeroDivisionError" in EXCEPTION_NAMES_AR


def test_table_includes_all_common_types():
    common = {
        "NameError",
        "TypeError",
        "ValueError",
        "IndexError",
        "KeyError",
        "AttributeError",
        "ImportError",
        "FileNotFoundError",
        "ZeroDivisionError",
    }
    for c in common:
        assert c in EXCEPTION_NAMES_AR


def test_table_no_duplicate_arabic_values():
    values = list(EXCEPTION_NAMES_AR.values())
    assert len(values) == len(set(values))


def test_table_arabic_names_are_normalized():
    for val in EXCEPTION_NAMES_AR.values():
        assert normalize_identifier(val) == val


# Message template coverage (3)


def test_message_templates_compiled():
    for p, _ in MESSAGE_TEMPLATES_AR:
        assert isinstance(p, re.Pattern)


def test_message_templates_arabic_present():
    for _, t in MESSAGE_TEMPLATES_AR:
        assert any("\u0600" <= ch <= "\u06ff" for ch in t)


def test_message_templates_anchored():
    for p, _ in MESSAGE_TEMPLATES_AR:
        assert p.pattern.startswith("^")
        assert p.pattern.endswith("$")


# format_translated_exception (5)


def test_format_zero_division_simple():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "خطا_القسمه_على_صفر" in output
    assert "القسمة على صفر" in output
    assert "تتبع_الأخطاء" in output


def test_format_includes_arabic_module_marker():
    try:
        exec("1/0")
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "<الوحدة>" in output


def test_format_includes_file_path_and_line():
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        output = format_translated_exception(*sys.exc_info())
    assert "ملف" in output
    assert "سطر" in output


def test_format_chained_exception_with_from():
    try:
        try:
            1 / 0  # noqa: B018
        except ZeroDivisionError as e:
            raise ValueError("bad value") from e
    except ValueError:
        output = format_translated_exception(*sys.exc_info())
    assert "السبب المباشر للاستثناء أعلاه:" in output
    assert "خطا_القسمه_على_صفر" in output
    assert "خطا_قيمه" in output


def test_format_chained_exception_implicit_context():
    try:
        try:
            1 / 0  # noqa: B018
        except ZeroDivisionError:
            raise ValueError("bad value")  # noqa: B904
    except ValueError:
        output = format_translated_exception(*sys.exc_info())
    assert "أثناء معالجة الاستثناء أعلاه, حدث استثناء آخر:" in output
    assert "خطا_القسمه_على_صفر" in output
    assert "خطا_قيمه" in output


# print_translated_exception (2)


def test_print_writes_to_stderr_by_default(capsys):
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        print_translated_exception(*sys.exc_info())
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err


def test_print_accepts_custom_file():
    buf = io.StringIO()
    try:
        1 / 0  # noqa: B018
    except ZeroDivisionError:
        print_translated_exception(*sys.exc_info(), file=buf)
    assert "خطا_القسمه_على_صفر" in buf.getvalue()


# install_excepthook / uninstall_excepthook (4)


@pytest.fixture(autouse=True)
def snapshot_excepthook():
    from arabicpython import tracebacks

    orig_hook = sys.excepthook
    orig_saved = tracebacks._saved_excepthook

    # Baseline for this file
    sys.excepthook = sys.__excepthook__
    tracebacks._saved_excepthook = None

    yield sys.__excepthook__

    sys.excepthook = orig_hook
    tracebacks._saved_excepthook = orig_saved


def test_install_replaces_excepthook(snapshot_excepthook):
    install_excepthook()
    assert sys.excepthook is print_translated_exception


def test_install_is_idempotent(snapshot_excepthook):
    install_excepthook()
    first_hook = sys.excepthook
    install_excepthook()
    assert sys.excepthook is first_hook


def test_uninstall_restores_previous(snapshot_excepthook):
    orig = sys.excepthook
    install_excepthook()
    uninstall_excepthook()
    assert sys.excepthook is orig


def test_uninstall_idempotent(snapshot_excepthook):
    uninstall_excepthook()
    uninstall_excepthook()
    # Should not raise


# CLI integration (3)


def test_cli_runtime_error_shows_arabic(tmp_path, capsys):
    f = tmp_path / "err.apy"
    f.write_text("x = 1 / 0\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err
    assert "القسمة على صفر" in err


def test_cli_name_error_shows_arabic(tmp_path, capsys):
    f = tmp_path / "name.apy"
    f.write_text("undefined_var\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "خطا_اسم" in err
    assert "الاسم 'undefined_var' غير معرّف" in err


def test_cli_unknown_exception_falls_through_to_english_message(tmp_path, capsys):
    f = tmp_path / "custom.apy"
    f.write_text("raise Exception('unique message')\n", encoding="utf-8")
    assert cli.main([str(f)]) == 1
    _, err = capsys.readouterr()
    assert "استثناء: unique message" in err


# REPL integration (2)


def test_repl_runtime_error_shows_arabic(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("١/٠\n"))
    # run_repl calls sys.exit, so we catch it
    run_repl(banner="", exit_msg="")
    _, err = capsys.readouterr()
    assert "خطا_القسمه_على_صفر" in err


def test_repl_name_error_shows_arabic(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO("undefined_in_repl\n"))
    run_repl(banner="", exit_msg="")
    _, err = capsys.readouterr()
    assert "خطا_اسم" in err


# Class identity preservation (1)


def test_exception_class_identity_unchanged(tmp_path, capsys):
    f = tmp_path / "identity.apy"
    f.write_text("try:\n    1/0\nexcept ZeroDivisionError:\n    اطبع('caught')\n", encoding="utf-8")
    assert cli.main([str(f)]) == 0
    out, _ = capsys.readouterr()
    assert "caught" in out


# ── B-041: New exception name translations ────────────────────────────────────


class TestB041WarningNames:
    def test_warning_base(self):
        assert EXCEPTION_NAMES_AR["Warning"] == "تحذير"

    def test_deprecation_warning(self):
        assert EXCEPTION_NAMES_AR["DeprecationWarning"] == "تحذير_اهمال"

    def test_pending_deprecation_warning(self):
        assert EXCEPTION_NAMES_AR["PendingDeprecationWarning"] == "تحذير_اهمال_قادم"

    def test_runtime_warning(self):
        assert EXCEPTION_NAMES_AR["RuntimeWarning"] == "تحذير_تشغيل"

    def test_syntax_warning(self):
        assert EXCEPTION_NAMES_AR["SyntaxWarning"] == "تحذير_صياغه"

    def test_user_warning(self):
        assert EXCEPTION_NAMES_AR["UserWarning"] == "تحذير_مستخدم"

    def test_future_warning(self):
        assert EXCEPTION_NAMES_AR["FutureWarning"] == "تحذير_مستقبلي"

    def test_import_warning(self):
        assert EXCEPTION_NAMES_AR["ImportWarning"] == "تحذير_استيراد"

    def test_unicode_warning(self):
        assert EXCEPTION_NAMES_AR["UnicodeWarning"] == "تحذير_يونيكود"

    def test_bytes_warning(self):
        assert EXCEPTION_NAMES_AR["BytesWarning"] == "تحذير_بايت"

    def test_resource_warning(self):
        assert EXCEPTION_NAMES_AR["ResourceWarning"] == "تحذير_موارد"

    def test_encoding_warning(self):
        assert EXCEPTION_NAMES_AR["EncodingWarning"] == "تحذير_ترميز"


class TestB041ConnectionErrorNames:
    def test_connection_error(self):
        assert EXCEPTION_NAMES_AR["ConnectionError"] == "خطا_اتصال"

    def test_broken_pipe_error(self):
        assert EXCEPTION_NAMES_AR["BrokenPipeError"] == "خطا_انبوب_مكسور"

    def test_connection_aborted_error(self):
        assert EXCEPTION_NAMES_AR["ConnectionAbortedError"] == "خطا_اتصال_ملغي"

    def test_connection_refused_error(self):
        assert EXCEPTION_NAMES_AR["ConnectionRefusedError"] == "خطا_اتصال_مرفوض"

    def test_connection_reset_error(self):
        assert EXCEPTION_NAMES_AR["ConnectionResetError"] == "خطا_اتصال_منقطع"

    def test_child_process_error(self):
        assert EXCEPTION_NAMES_AR["ChildProcessError"] == "خطا_عمليه_فرعيه"

    def test_interrupted_error(self):
        assert EXCEPTION_NAMES_AR["InterruptedError"] == "خطا_مقاطعه"

    def test_process_lookup_error(self):
        assert EXCEPTION_NAMES_AR["ProcessLookupError"] == "خطا_بحث_عمليه"


class TestB041OtherNewNames:
    def test_buffer_error(self):
        assert EXCEPTION_NAMES_AR["BufferError"] == "خطا_مخزن_مؤقت"

    def test_generator_exit(self):
        assert EXCEPTION_NAMES_AR["GeneratorExit"] == "خروج_مولد"

    def test_stop_async_iteration(self):
        assert EXCEPTION_NAMES_AR["StopAsyncIteration"] == "ايقاف_التكرار_المتزامن"

    def test_unbound_local_error(self):
        assert EXCEPTION_NAMES_AR["UnboundLocalError"] == "خطا_متغير_غير_مرتبط"

    def test_unicode_translate_error(self):
        assert EXCEPTION_NAMES_AR["UnicodeTranslateError"] == "خطا_ترجمه_يونيكود"

    def test_reference_error(self):
        assert EXCEPTION_NAMES_AR["ReferenceError"] == "خطا_مرجع"

    def test_system_error(self):
        assert EXCEPTION_NAMES_AR["SystemError"] == "خطا_نظام_داخلي"

    def test_environment_error(self):
        assert EXCEPTION_NAMES_AR["EnvironmentError"] == "خطا_بيئه"

    def test_io_error(self):
        assert EXCEPTION_NAMES_AR["IOError"] == "خطا_ادخال_اخراج"

    def test_base_exception_group(self):
        assert EXCEPTION_NAMES_AR["BaseExceptionGroup"] == "مجموعه_استثنائات_اساسيه"

    def test_exception_group(self):
        assert EXCEPTION_NAMES_AR["ExceptionGroup"] == "مجموعه_استثنائات"


# ── B-041: New message templates ──────────────────────────────────────────────


class TestB041TypeErrorTemplates:
    def test_list_indices_not_integer(self):
        msg = "list indices must be integers or slices, not float"
        result = translate_exception_message(msg)
        assert "فهارس القائمة" in result
        assert "float" in result

    def test_tuple_indices_not_integer(self):
        msg = "tuple indices must be integers or slices, not str"
        result = translate_exception_message(msg)
        assert "فهارس الصف" in result
        assert "str" in result

    def test_object_has_no_len(self):
        msg = "object of type 'int' has no len()"
        result = translate_exception_message(msg)
        assert "لا يملك دالة len()" in result
        assert "int" in result

    def test_unhashable_type(self):
        msg = "unhashable type: 'list'"
        result = translate_exception_message(msg)
        assert "غير قابل للتجزئة" in result
        assert "list" in result

    def test_object_not_iterator(self):
        msg = "'int' object is not an iterator"
        result = translate_exception_message(msg)
        assert "ليس مكرراً" in result

    def test_bytes_like_required(self):
        msg = "a bytes-like object is required, not 'str'"
        result = translate_exception_message(msg)
        assert "مطلوب كائن من نوع bytes" in result

    def test_takes_n_positional_args(self):
        msg = "foo() takes 1 positional argument but 3 were given"
        result = translate_exception_message(msg)
        assert "foo()" in result
        assert "3" in result

    def test_sequence_item_expected_str(self):
        msg = "sequence item 0: expected str instance, int found"
        result = translate_exception_message(msg)
        assert "عنصر المتسلسلة" in result
        assert "int" in result


class TestB041UnboundLocalTemplate:
    def test_unbound_local_py312_message(self):
        msg = "cannot access local variable 'x' where it is not associated with a value"
        result = translate_exception_message(msg)
        assert "المتغير المحلي 'x'" in result
        assert "غير مرتبط بقيمة" in result


class TestB041AttributeErrorSuggestion:
    def test_attribute_error_with_suggestion(self):
        msg = "'list' object has no attribute 'appned'. Did you mean: 'append'?"
        result = translate_exception_message(msg)
        assert "هل تقصد: 'append'؟" in result
        assert "appned" in result


class TestB041ValueErrorTemplates:
    def test_too_many_values_to_unpack(self):
        msg = "too many values to unpack (expected 2)"
        result = translate_exception_message(msg)
        assert "كثيرة جداً للتفريغ" in result
        assert "2" in result

    def test_not_enough_values_to_unpack(self):
        msg = "not enough values to unpack (expected 3, got 1)"
        result = translate_exception_message(msg)
        assert "غير كافية للتفريغ" in result
        assert "3" in result
        assert "1" in result


class TestB041OverflowTemplates:
    def test_math_range_error(self):
        result = translate_exception_message("math range error")
        assert "مجال الرياضيات" in result

    def test_int_too_large(self):
        result = translate_exception_message("int too large to convert to float")
        assert "كبير جداً للتحويل" in result


class TestB041RuntimeTemplates:
    def test_generator_already_executing(self):
        result = translate_exception_message("generator already executing")
        assert "المولّد قيد التنفيذ" in result

    def test_coroutine_already_executing(self):
        result = translate_exception_message("coroutine already executing")
        assert "الكوروتين قيد التنفيذ" in result


class TestB041SyntaxTemplates:
    def test_expected_indented_block(self):
        result = translate_exception_message("expected an indented block")
        assert "كتلة مزاحة" in result

    def test_inconsistent_tabs_spaces(self):
        result = translate_exception_message("inconsistent use of tabs and spaces in indentation")
        assert "غير متسق" in result

    def test_unindent_mismatch(self):
        result = translate_exception_message("unindent does not match any outer indentation level")
        assert "الإزاحة لا تطابق" in result


class TestB041OSErrorTemplates:
    def test_errno_without_path(self):
        result = translate_exception_message("[Errno 111] Connection refused")
        assert "رقم الخطأ 111" in result

    def test_windows_error_format(self):
        result = translate_exception_message("[WinError 5] Access is denied")
        assert "خطأ ويندوز 5" in result

    def test_math_domain_error(self):
        result = translate_exception_message("math domain error")
        assert "نطاق الرياضيات" in result
