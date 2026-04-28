# tests/aliases/test_pytest.py
# B-015: Arabic aliases for pytest — بايتست

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def بايتست():
    """Return a ModuleProxy wrapping `pytest`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("بايتست", None, None)
    assert spec is not None, "AliasFinder did not find 'بايتست'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core helpers ──────────────────────────────────────────────────────────────


class TestCoreHelpers:
    def test_fixture(self, بايتست):
        assert بايتست.مثبت is pytest.fixture

    def test_raises_alias(self, بايتست):
        assert بايتست.يثير is pytest.raises

    def test_warns_alias(self, بايتست):
        assert بايتست.يحذر is pytest.warns

    def test_approx_alias(self, بايتست):
        assert بايتست.تقريبا is pytest.approx

    def test_fail_alias(self, بايتست):
        assert بايتست.افشل is pytest.fail

    def test_skip_alias(self, بايتست):
        assert بايتست.تخطي is pytest.skip

    def test_xfail_alias(self, بايتست):
        assert بايتست.فشل_متوقع is pytest.xfail

    def test_param_alias(self, بايتست):
        assert بايتست.معامل is pytest.param

    def test_importorskip_alias(self, بايتست):
        assert بايتست.استورد_او_تخطي is pytest.importorskip

    def test_deprecated_call_alias(self, بايتست):
        assert بايتست.استدعاء_مهمل is pytest.deprecated_call


# ── Marks ─────────────────────────────────────────────────────────────────────


class TestMarks:
    def test_mark_alias(self, بايتست):
        assert بايتست.علامه is pytest.mark

    def test_mark_parametrize_accessible(self, بايتست):
        """Sub-marks are accessed via the MarkGenerator returned by العلامه."""
        assert hasattr(بايتست.علامه, "parametrize")

    def test_mark_skip_accessible(self, بايتست):
        assert hasattr(بايتست.علامه, "skip")

    def test_mark_skipif_accessible(self, بايتست):
        assert hasattr(بايتست.علامه, "skipif")

    def test_mark_xfail_accessible(self, بايتست):
        assert hasattr(بايتست.علامه, "xfail")


# ── Runner ────────────────────────────────────────────────────────────────────


class TestRunner:
    def test_main_alias(self, بايتست):
        assert بايتست.شغل_الاختبارات is pytest.main

    def test_exit_alias(self, بايتست):
        assert بايتست.اخرج_pytest is pytest.exit


# ── Types ─────────────────────────────────────────────────────────────────────


class TestTypes:
    def test_exception_info_alias(self, بايتست):
        assert بايتست.معلومات_الخطا is pytest.ExceptionInfo

    def test_monkeypatch_alias(self, بايتست):
        assert بايتست.ترقيع_القرد is pytest.MonkeyPatch

    def test_fixture_request_alias(self, بايتست):
        assert بايتست.طلب_المثبت is pytest.FixtureRequest

    def test_capture_fixture(self, بايتست):
        assert بايتست.مثبت_التقاط is pytest.CaptureFixture

    def test_log_capture_fixture(self, بايتست):
        assert بايتست.مثبت_السجل is pytest.LogCaptureFixture

    def test_warnings_recorder_alias(self, بايتست):
        assert بايتست.مسجل_التحذيرات is pytest.WarningsRecorder

    def test_temp_path_factory_alias(self, بايتست):
        assert بايتست.مصنع_مسار_مؤقت is pytest.TempPathFactory

    def test_test_report_alias(self, بايتست):
        assert بايتست.تقرير_الاختبار is pytest.TestReport

    def test_exit_code_alias(self, بايتست):
        assert بايتست.رمز_الخروج is pytest.ExitCode

    def test_config_alias(self, بايتست):
        assert بايتست.اعداد_pytest is pytest.Config

    def test_usage_error_alias(self, بايتست):
        assert بايتست.خطا_الاستخدام is pytest.UsageError


# ── Functional ────────────────────────────────────────────────────────────────


class TestFunctional:
    def test_raises_catches_exception(self, بايتست):
        """يثير (raises) actually catches exceptions as a context manager."""
        with بايتست.يثير(ValueError):
            raise ValueError("test error")

    def test_approx_float_comparison(self, بايتست):
        """تقريبا (approx) works for floating-point comparisons."""
        assert بايتست.تقريبا(0.3) == 0.1 + 0.2

    def test_approx_list(self, بايتست):
        assert بايتست.تقريبا([0.1, 0.2]) == [0.1, 0.2]

    def test_warns_catches_warning(self, بايتست):
        """يحذر (warns) catches warnings as a context manager."""
        import warnings

        with بايتست.يحذر(UserWarning):
            warnings.warn("test warning", UserWarning, stacklevel=2)

    def test_param_creates_param_set(self, بايتست):
        """معامل (param) creates a ParameterSet."""
        p = بايتست.معامل(1, 2, id="pair")
        assert hasattr(p, "values")
        assert p.values == (1, 2)

    def test_importorskip_returns_module(self, بايتست):
        """استورد_او_تخطي (importorskip) returns the module when available."""
        os = بايتست.استورد_او_تخطي("os")
        import os as real_os

        assert os is real_os

    def test_importorskip_skips_missing(self, بايتست):
        """استورد_او_تخطي skips when the module does not exist."""
        with pytest.raises(pytest.skip.Exception):
            بايتست.استورد_او_تخطي("_no_such_module_xyz_")

    def test_exit_code_values(self, بايتست):
        """رمز_الخروج (ExitCode) has the standard OK value."""
        assert بايتست.رمز_الخروج.OK == pytest.ExitCode.OK
        assert بايتست.رمز_الخروج.TESTS_FAILED == pytest.ExitCode.TESTS_FAILED

    def test_deprecated_call_catches_deprecation(self, بايتست):
        """استدعاء_مهمل (deprecated_call) catches DeprecationWarning."""
        import warnings

        def old_func():
            warnings.warn("old", DeprecationWarning, stacklevel=2)

        with بايتست.استدعاء_مهمل():
            old_func()

    def test_monkeypatch_setattr(self, بايتست):
        """ترقيع_القرد (MonkeyPatch) can be instantiated and used."""
        mp = بايتست.ترقيع_القرد()

        class Obj:
            x = 1

        mp.setattr(Obj, "x", 99)
        assert Obj.x == 99
        mp.undo()
        assert Obj.x == 1
