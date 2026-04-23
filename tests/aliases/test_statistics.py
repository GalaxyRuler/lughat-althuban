# tests/aliases/test_statistics.py
# B-035 stdlib aliases — statistics module tests

import pathlib
import statistics

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def احصاء():
    """Return a ModuleProxy wrapping `statistics`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("احصاء", None, None)
    assert spec is not None, "AliasFinder did not find 'احصاء'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestStatisticsProxy:
    # ── Function aliases ──────────────────────────────────────────────────────

    def test_mean_alias(self, احصاء):
        """وسط maps to statistics.mean."""
        assert احصاء.وسط is statistics.mean

    def test_fmean_alias(self, احصاء):
        """وسط_دقيق maps to statistics.fmean."""
        assert احصاء.وسط_دقيق is statistics.fmean

    def test_median_alias(self, احصاء):
        """وسيط maps to statistics.median."""
        assert احصاء.وسيط is statistics.median

    def test_mode_alias(self, احصاء):
        """منوال maps to statistics.mode."""
        assert احصاء.منوال is statistics.mode

    def test_stdev_alias(self, احصاء):
        """انحراف maps to statistics.stdev."""
        assert احصاء.انحراف is statistics.stdev

    def test_variance_alias(self, احصاء):
        """تباين maps to statistics.variance."""
        assert احصاء.تباين is statistics.variance

    def test_pstdev_alias(self, احصاء):
        """انحراف_سكاني maps to statistics.pstdev."""
        assert احصاء.انحراف_سكاني is statistics.pstdev

    def test_pvariance_alias(self, احصاء):
        """تباين_سكاني maps to statistics.pvariance."""
        assert احصاء.تباين_سكاني is statistics.pvariance

    def test_geometric_mean_alias(self, احصاء):
        """وسط_هندسي maps to statistics.geometric_mean."""
        assert احصاء.وسط_هندسي is statistics.geometric_mean

    def test_harmonic_mean_alias(self, احصاء):
        """وسط_توافقي maps to statistics.harmonic_mean."""
        assert احصاء.وسط_توافقي is statistics.harmonic_mean

    def test_multimode_alias(self, احصاء):
        """منوالات maps to statistics.multimode."""
        assert احصاء.منوالات is statistics.multimode

    def test_quantiles_alias(self, احصاء):
        """كميات maps to statistics.quantiles."""
        assert احصاء.كميات is statistics.quantiles

    def test_covariance_alias(self, احصاء):
        """تغاير maps to statistics.covariance."""
        assert احصاء.تغاير is statistics.covariance

    def test_correlation_alias(self, احصاء):
        """ارتباط maps to statistics.correlation."""
        assert احصاء.ارتباط is statistics.correlation

    def test_statistics_error_alias(self, احصاء):
        """خطا_احصائي maps to statistics.StatisticsError."""
        assert احصاء.خطا_احصائي is statistics.StatisticsError

    def test_normal_dist_alias(self, احصاء):
        """توزيع_طبيعي maps to statistics.NormalDist."""
        assert احصاء.توزيع_طبيعي is statistics.NormalDist

    # ── Functional tests ──────────────────────────────────────────────────────

    DATA = [2, 4, 4, 4, 5, 5, 7, 9]

    def test_mean_value(self, احصاء):
        """وسط([2,4,4,4,5,5,7,9]) == 5.0."""
        assert احصاء.وسط(self.DATA) == pytest.approx(5.0)

    def test_median_value(self, احصاء):
        """وسيط of even-length list is average of two middle values."""
        assert احصاء.وسيط(self.DATA) == pytest.approx(4.5)

    def test_mode_value(self, احصاء):
        """منوال returns the most common value."""
        assert احصاء.منوال(self.DATA) == 4

    def test_stdev_value(self, احصاء):
        """انحراف of the test dataset matches statistics.stdev."""
        assert احصاء.انحراف(self.DATA) == pytest.approx(statistics.stdev(self.DATA))

    def test_variance_value(self, احصاء):
        """تباين == stdev²."""
        var = احصاء.تباين(self.DATA)
        std = احصاء.انحراف(self.DATA)
        assert var == pytest.approx(std**2)

    def test_multimode_returns_list(self, احصاء):
        """منوالات returns a list of modes."""
        data = [1, 1, 2, 2, 3]
        modes = احصاء.منوالات(data)
        assert set(modes) == {1, 2}

    def test_covariance_value(self, احصاء):
        """تغاير([1,2,3], [1,2,3]) == 1.0 (perfect covariance)."""
        x = [1, 2, 3]
        y = [1, 2, 3]
        assert احصاء.تغاير(x, y) == pytest.approx(1.0)

    def test_correlation_perfect(self, احصاء):
        """ارتباط([1,2,3], [1,2,3]) == 1.0 (perfect positive)."""
        assert احصاء.ارتباط([1, 2, 3], [1, 2, 3]) == pytest.approx(1.0)

    def test_statistics_error_raised(self, احصاء):
        """خطا_احصائي is raised when data is empty."""
        with pytest.raises(statistics.StatisticsError):
            احصاء.وسط([])

    def test_geometric_mean_value(self, احصاء):
        """وسط_هندسي([1,4,16]) == 4.0."""
        assert احصاء.وسط_هندسي([1, 4, 16]) == pytest.approx(4.0)
