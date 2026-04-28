# tests/aliases/test_seaborn.py
# B-057: Arabic aliases for seaborn

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

seaborn = pytest.importorskip("seaborn", reason="seaborn not installed")


@pytest.fixture(scope="module")
def سيبورن():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("سيبورن", None, None)
    assert spec is not None, "AliasFinder did not find 'سيبورن'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestSeabornAliasesExist:
    def test_lineplot(self, سيبورن):
        assert سيبورن.خط_بياني is seaborn.lineplot

    def test_scatterplot(self, سيبورن):
        assert سيبورن.مخطط_نقاط is seaborn.scatterplot

    def test_histplot(self, سيبورن):
        assert سيبورن.توزيع_بيانات is seaborn.histplot

    def test_kdeplot(self, سيبورن):
        assert سيبورن.كثافه_احتماليه is seaborn.kdeplot

    def test_barplot(self, سيبورن):
        assert سيبورن.مخطط_شريطي is seaborn.barplot

    def test_boxplot(self, سيبورن):
        assert سيبورن.مخطط_صندوقي is seaborn.boxplot

    def test_heatmap(self, سيبورن):
        assert سيبورن.خريطه_حراره is seaborn.heatmap

    def test_pairplot(self, سيبورن):
        assert سيبورن.شبكه_زوجيه is seaborn.pairplot

    def test_set_theme(self, سيبورن):
        assert سيبورن.ضبط_موضوع is seaborn.set_theme

    def test_set_style(self, سيبورن):
        assert سيبورن.ضبط_نمط is seaborn.set_style

    def test_load_dataset(self, سيبورن):
        assert سيبورن.حمل_بيانات is seaborn.load_dataset

    def test_color_palette(self, سيبورن):
        assert سيبورن.احضر_لوحه is seaborn.color_palette

    def test_violinplot(self, سيبورن):
        assert سيبورن.مخطط_كمان is seaborn.violinplot

    def test_relplot(self, سيبورن):
        assert سيبورن.شبكه_علاقات is seaborn.relplot

    def test_jointplot(self, سيبورن):
        assert سيبورن.مخطط_مشترك is seaborn.jointplot


class TestSeabornTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "seaborn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "seaborn"
        assert data["meta"]["arabic_name"] == "سيبورن"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "seaborn.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 20
