# tests/aliases/test_pytest.py
# B-015: Arabic aliases for pytest — اختبارات

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def اختبارات():
    """Return a ModuleProxy wrapping `pytest`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("اختبارات", None, None)
    assert spec is not None, "AliasFinder did not find 'اختبارات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core helpers ──────────────────────────────────────────────────────────────


class TestCoreHelpers:
    def test_fixture_alias(self, اختبارات):
        assert اختبارات.مثبت is pytest.fixture

    def test_raises_alias(self, اختبارات):
        assert اختبارات.يثير is pytest.raises

    def test_warns_alias(self, اختبارات):
        assert اختبارات.يحذر is pytest.warns

    def test_approx_alias(self, اختبارات):
        assert اختبارات.تقريبا is pytest.approx

    def test_fail_alias(self, اختبارات):
        assert اختبارات.افشل is pytest.fail

    def test_skip_alias(self, اختبارات):
        assert اختبارات.تخطي is pytest.skip

    def test_xfail_alias(self, اختبارات):
        assert اختبارات.فشل_متوقع is pytest.xfail

    def test_param_alias(self, اختبارات):
        assert اختبارات.معامل is pytest.param

    def test_importorskip_alias(self, اختبارات):
        assert اختبارات.استورد_او_تخطي is pytest.importorskip

    def test_deprecated_call_alias(self, اختبارات):
        assert اختبارات.استدعاء_مهمل is pytest.deprecated_call


# ── Marks ─────────────────────────────────────────────────────────────────────


class TestMarks:
    def test_mark_alias(self, اختبارات):
        assert اختبارات.علامه is pytest.mark

    def test_mark_parametrize_accessible(self, اختبارات):
        """Sub-marks are accessed via the MarkGenerator returned by العلامه."""
        assert hasattr(اختبارات.علامه, "parametrize")

    def test_mark_skip_accessible(self, اختبارات):
        assert hasattr(اختبارات.علامه, "skip")

    def test_mark_skipif_accessible(self, اختبارات):
        assert hasattr(اختبارات.علامه, "skipif")

    def test_mark_xfail_accessible(self, اختبارات):
        assert hasattr(اختبارات.علامه, "xfail")


# ── Runner ────────────────────────────────────────────────────────────────────


class TestRunner:
    def test_main_alias(self, اختبارات):
        assert اختبارات.شغل_الاختبارات is pytest.main

    def test_exit_alias(self, اختبارات):
        assert اختبارات.اخرج_pytest is pytest.exit


# ── Types ─────────────────────────────────────────────────────────────────────


class TestTypes:
    def test_exception_info_alias(self, اختبارات):
        assert اختبارات.معلومات_الخطا is pytest.ExceptionInfo

    def test_monkeypatch_alias(self, اختبارات):
        assert اختبارات.ترقيع_القرد is pytest.MonkeyPatch

    def test_fixture_request_alias(self, اختبارات):
        assert اختبارات.طلب_المثبت is pytest.FixtureRequest

    def test_capture_fixture_alias(self, اختبارات):
        assert اختبارات.مثبت_التقاط is pytest.CaptureFixture

    def test_log_capture_fixture_alias(self, اختبارات):
        assert اختبارات.مثبت_السجل is pytest.LogCaptureFixture

    def test_warnings_recorder_alias(self, اختبارات):
        assert اختبارات.مسجل_التحذيرات is pytest.WarningsRecorder

    def test_temp_path_factory_alias(self, اختبارات):
        assert اختبارات.مصنع_مسار_مؤقت is pytest.TempPathFactory

    def test_test_report_alias(self, اختبارات):
        assert اختبارات.تقرير_الاختبار is pytest.TestReport

    def test_exit_code_alias(self, اختبارات):
        assert اختبارات.رمز_الخروج is pytest.ExitCode

    def test_config_alias(self, اختبارات):
        assert اختبارات.اعداد_pytest is pytest.Config

    def test_usage_error_alias(self, اختبارات):
        assert اختبارات.خطا_الاستخدام is pytest.UsageError


# ── Functional ────────────────────────────────────────────────────────────────


class TestFunctional:
    def test_raises_catches_exception(self, اختبارات):
        """يثير (raises) actually catches exceptions as a context manager."""
        with اختبارات.يثير(ValueError):
            raise ValueError("test error")

    def test_approx_float_comparison(self, اختبارات):
        """تقريبا (approx) works for floating-point comparisons."""
        assert اختبارات.تقريبا(0.3) == 0.1 + 0.2

    def test_approx_list(self, اختبارات):
        assert اختبارات.تقريبا([0.1, 0.2]) == [0.1, 0.2]

    def test_warns_catches_warning(self, اختبارات):
        """يحذر (warns) catches warnings as a context manager."""
        import warnings

        with اختبارات.يحذر(UserWarning):
            warnings.warn("test warning", UserWarning, stacklevel=2)

    def test_param_creates_param_set(self, اختبارات):
        """معامل (param) creates a ParameterSet."""
        p = اختبارات.معامل(1, 2, id="pair")
        assert hasattr(p, "values")
        assert p.values == (1, 2)

    def test_importorskip_returns_module(self, اختبارات):
        """استورد_او_تخطي (importorskip) returns the module when available."""
        os = اختبارات.استورد_او_تخطي("os")
        import os as real_os

        assert os is real_os

    def test_importorskip_skips_missing(self, اختبارات):
        """استورد_او_تخطي skips when the module does not exist."""
        with pytest.raises(pytest.skip.Exception):
            اختبارات.استورد_او_تخطي("_no_such_module_xyz_")

    def test_exit_code_values(self, اختبارات):
        """رمز_الخروج (ExitCode) has the standard OK value."""
        assert اختبارات.رمز_الخروج.OK == pytest.ExitCode.OK
        assert اختبارات.رمز_الخروج.TESTS_FAILED == pytest.ExitCode.TESTS_FAILED

    def test_deprecated_call_catches_deprecation(self, اختبارات):
        """استدعاء_مهمل (deprecated_call) catches DeprecationWarning."""
        import warnings

        def old_func():
            warnings.warn("old", DeprecationWarning, stacklevel=2)

        with اختبارات.استدعاء_مهمل():
            old_func()

    def test_monkeypatch_setattr(self, اختبارات):
        """ترقيع_القرد (MonkeyPatch) can be instantiated and used."""
        mp = اختبارات.ترقيع_القرد()

        class Obj:
            x = 1

        mp.setattr(Obj, "x", 99)
        assert Obj.x == 99
        mp.undo()
        assert Obj.x == 1
