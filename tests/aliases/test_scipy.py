# tests/aliases/test_scipy.py
# B-058: Arabic aliases for scipy

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

scipy = pytest.importorskip("scipy", reason="scipy not installed")


@pytest.fixture(scope="module")
def سايباي():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("سايباي", None, None)
    assert spec is not None, "AliasFinder did not find 'سايباي'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestScipyAliasesExist:
    def test_stats_alias(self, سايباي):
        import scipy.stats

        assert سايباي.احصاء_متقدم is scipy.stats

    def test_optimize_alias(self, سايباي):
        import scipy.optimize

        assert سايباي.تحسين is scipy.optimize

    def test_integrate_alias(self, سايباي):
        import scipy.integrate

        assert سايباي.تكامل is scipy.integrate

    def test_linalg_alias(self, سايباي):
        import scipy.linalg

        assert سايباي.جبر_خطي_علمي is scipy.linalg

    def test_interpolate_alias(self, سايباي):
        import scipy.interpolate

        assert سايباي.استيفاء is scipy.interpolate

    def test_fft_alias(self, سايباي):
        import scipy.fft

        assert سايباي.تحويل_فوريه is scipy.fft

    def test_signal_alias(self, سايباي):
        import scipy.signal

        assert سايباي.معالجه_اشارات is scipy.signal

    def test_sparse_alias(self, سايباي):
        import scipy.sparse

        assert سايباي.مصفوفات_مبعثره is scipy.sparse

    def test_spatial_alias(self, سايباي):
        import scipy.spatial

        assert سايباي.هندسه_فضائيه is scipy.spatial

    def test_constants_alias(self, سايباي):
        import scipy.constants

        assert سايباي.ثوابت is scipy.constants

    def test_special_alias(self, سايباي):
        import scipy.special

        assert سايباي.دالات_خاصه is scipy.special


class TestScipyTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "scipy.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "scipy"
        assert data["meta"]["arabic_name"] == "سايباي"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "scipy.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 10
