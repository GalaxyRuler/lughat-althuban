# tests/aliases/test_matplotlib.py
# C-010: Arabic aliases for matplotlib

import pathlib

import pytest

matplotlib = pytest.importorskip("matplotlib", reason="matplotlib not installed")
matplotlib.use("Agg", force=True)
plt = pytest.importorskip("matplotlib.pyplot", reason="matplotlib.pyplot not installed")

import matplotlib.axes as mpl_axes  # noqa: E402
import matplotlib.colors as mpl_colors  # noqa: E402
import matplotlib.figure as mpl_figure  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def رسوم_بيانيه():
    """Return a ModuleProxy wrapping `matplotlib`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("رسوم_بيانيه", None, None)
    assert spec is not None, "AliasFinder did not find 'رسوم_بيانيه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestMatplotlibCore:
    def test_pyplot_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.بايبلوت is plt

    def test_figure_class_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.شكل is mpl_figure.Figure

    def test_axes_class_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.محاور is mpl_axes.Axes

    def test_rcparams_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.اعدادات is matplotlib.rcParams


class TestMatplotlibPyplot:
    def test_plot_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.ارسم is plt.plot

    def test_scatter_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.نثر is plt.scatter

    def test_subplots_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.شكل_ومحاور is plt.subplots

    def test_title_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.عنوان is plt.title

    def test_savefig_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.احفظ_شكل is plt.savefig

    def test_close_alias(self, رسوم_بيانيه):
        assert رسوم_بيانيه.اغلق is plt.close

    def test_color_helpers(self, رسوم_بيانيه):
        assert رسوم_بيانيه.لون_الي_hex is mpl_colors.to_hex
        assert رسوم_بيانيه.لون_الي_rgba is mpl_colors.to_rgba


class TestMatplotlibFunctional:
    def test_create_plot_without_display(self, رسوم_بيانيه):
        fig, ax = رسوم_بيانيه.شكل_ومحاور()
        ax.plot([1, 2, 3], [1, 4, 9])
        ax.set_title("growth")

        assert isinstance(fig, mpl_figure.Figure)
        assert isinstance(ax, mpl_axes.Axes)
        assert ax.get_title() == "growth"

        رسوم_بيانيه.اغلق(fig)

    def test_axes_attributes_work_with_class_proxy(self, رسوم_بيانيه):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "matplotlib.toml")
        fig, ax = رسوم_بيانيه.شكل_ومحاور()
        proxy = ClassProxy(ax, mapping.attributes)

        proxy.عنوان("عنوان عربي")
        proxy.وسم_س("س")
        proxy.وسم_ص("ص")

        assert ax.get_title() == "عنوان عربي"
        assert ax.get_xlabel() == "س"
        assert ax.get_ylabel() == "ص"

        رسوم_بيانيه.اغلق(fig)


class TestMatplotlibTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "matplotlib.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "matplotlib"
        assert data["meta"]["arabic_name"] == "رسوم_بيانيه"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "matplotlib.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 40
