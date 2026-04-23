# tests/aliases/test_math.py
# B-035 stdlib aliases — math module tests

import math
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def رياضيات():
    """Return a ModuleProxy wrapping `math`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("رياضيات", None, None)
    assert spec is not None, "AliasFinder did not find 'رياضيات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestMathProxy:
    # ── Constant aliases ──────────────────────────────────────────────────────

    def test_pi_alias(self, رياضيات):
        """باي maps to math.pi."""
        assert رياضيات.باي == math.pi

    def test_e_alias(self, رياضيات):
        """اساس_طبيعي maps to math.e."""
        assert رياضيات.اساس_طبيعي == math.e

    def test_tau_alias(self, رياضيات):
        """ثاو maps to math.tau."""
        assert رياضيات.ثاو == math.tau

    def test_inf_alias(self, رياضيات):
        """لانهايه maps to math.inf."""
        assert رياضيات.لانهايه == math.inf

    def test_nan_alias(self, رياضيات):
        """غير_محدد maps to math.nan."""
        assert math.isnan(رياضيات.غير_محدد)

    # ── Function aliases ──────────────────────────────────────────────────────

    def test_sqrt_alias(self, رياضيات):
        """جذر maps to math.sqrt."""
        assert رياضيات.جذر is math.sqrt

    def test_floor_alias(self, رياضيات):
        """ارضيه maps to math.floor."""
        assert رياضيات.ارضيه is math.floor

    def test_ceil_alias(self, رياضيات):
        """سقف maps to math.ceil."""
        assert رياضيات.سقف is math.ceil

    def test_log_alias(self, رياضيات):
        """لوغاريتم maps to math.log."""
        assert رياضيات.لوغاريتم is math.log

    def test_sin_alias(self, رياضيات):
        """جيب maps to math.sin."""
        assert رياضيات.جيب is math.sin

    def test_cos_alias(self, رياضيات):
        """جيب_تمام maps to math.cos."""
        assert رياضيات.جيب_تمام is math.cos

    def test_factorial_alias(self, رياضيات):
        """مصنوعيه maps to math.factorial."""
        assert رياضيات.مصنوعيه is math.factorial

    def test_gcd_alias(self, رياضيات):
        """قاسم_مشترك maps to math.gcd."""
        assert رياضيات.قاسم_مشترك is math.gcd

    def test_degrees_alias(self, رياضيات):
        """درجات maps to math.degrees."""
        assert رياضيات.درجات is math.degrees

    def test_radians_alias(self, رياضيات):
        """قطاع maps to math.radians."""
        assert رياضيات.قطاع is math.radians

    def test_isclose_alias(self, رياضيات):
        """قريب_منه maps to math.isclose."""
        assert رياضيات.قريب_منه is math.isclose

    def test_isnan_alias(self, رياضيات):
        """غير_محدده maps to math.isnan."""
        assert رياضيات.غير_محدده is math.isnan

    def test_isinf_alias(self, رياضيات):
        """لانهائي_سالب maps to math.isinf."""
        assert رياضيات.لانهائي_سالب is math.isinf

    def test_comb_alias(self, رياضيات):
        """توليفه maps to math.comb."""
        assert رياضيات.توليفه is math.comb

    def test_perm_alias(self, رياضيات):
        """تباديل_عدد maps to math.perm."""
        assert رياضيات.تباديل_عدد is math.perm

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_sqrt_of_nine(self, رياضيات):
        """جذر(9) == 3.0."""
        assert رياضيات.جذر(9) == pytest.approx(3.0)

    def test_floor_rounds_down(self, رياضيات):
        """ارضيه(3.9) == 3."""
        assert رياضيات.ارضيه(3.9) == 3

    def test_ceil_rounds_up(self, رياضيات):
        """سقف(3.1) == 4."""
        assert رياضيات.سقف(3.1) == 4

    def test_factorial_five(self, رياضيات):
        """مصنوعيه(5) == 120."""
        assert رياضيات.مصنوعيه(5) == 120

    def test_gcd_correct(self, رياضيات):
        """قاسم_مشترك(48, 18) == 6."""
        assert رياضيات.قاسم_مشترك(48, 18) == 6

    def test_pi_approx(self, رياضيات):
        """باي ≈ 3.14159."""
        assert رياضيات.باي == pytest.approx(3.14159, rel=1e-5)

    def test_sin_zero(self, رياضيات):
        """جيب(0) == 0.0."""
        assert رياضيات.جيب(0) == pytest.approx(0.0)

    def test_cos_zero(self, رياضيات):
        """جيب_تمام(0) == 1.0."""
        assert رياضيات.جيب_تمام(0) == pytest.approx(1.0)

    def test_degrees_pi(self, رياضيات):
        """درجات(باي) == 180."""
        assert رياضيات.درجات(رياضيات.باي) == pytest.approx(180.0)

    def test_comb_value(self, رياضيات):
        """توليفه(5, 2) == 10."""
        assert رياضيات.توليفه(5, 2) == 10

    def test_log_e(self, رياضيات):
        """لوغاريتم(اساس_طبيعي) == 1.0."""
        assert رياضيات.لوغاريتم(رياضيات.اساس_طبيعي) == pytest.approx(1.0)

    def test_isclose_true(self, رياضيات):
        """قريب_منه returns True for values within default tolerance."""
        assert رياضيات.قريب_منه(1.0, 1.0 + 1e-10)

    def test_lcm_alias(self, رياضيات):
        """مضاعف_مشترك maps to math.lcm and returns correct value."""
        assert رياضيات.مضاعف_مشترك is math.lcm
        assert رياضيات.مضاعف_مشترك(4, 6) == 12
