# tests/aliases/test_bs4.py
# C-025: Arabic aliases for Beautiful Soup

import pathlib

import pytest

bs4 = pytest.importorskip("bs4", reason="beautifulsoup4 not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def تحليل_ويب():
    """Return a ModuleProxy wrapping `bs4`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("تحليل_ويب", None, None)
    assert spec is not None, "AliasFinder did not find 'تحليل_ويب'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestBeautifulSoupCore:
    def test_parser_and_node_classes(self, تحليل_ويب):
        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(تحليل_ويب.حساء_جميل, ClassFactory)
        assert isinstance(تحليل_ويب.وسم, ClassFactory)
        assert تحليل_ويب.نص_ملاحي is bs4.NavigableString
        assert تحليل_ويب.تعليق_html is bs4.Comment
        assert تحليل_ويب.مصفاه_حساء is bs4.SoupStrainer
        assert تحليل_ويب.خطا_ميزهه is bs4.FeatureNotFound


class TestBeautifulSoupFunctional:
    def test_soup_and_tag_aliases(self, تحليل_ويب):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "bs4.toml")
        soup = تحليل_ويب.حساء_جميل(
            "<html><body><h1>مرحبا</h1><a href='/docs'>docs</a></body></html>",
            "html.parser",
        )

        title = soup.ابحث_حساء("h1")
        links = soup.حدد_حساء("a")
        title_proxy = ClassProxy(title, mapping.attributes)

        assert title_proxy.احصل_نص() == "مرحبا"
        assert links[0]["href"] == "/docs"
        assert soup.نص_حساء(strip=True) == "مرحباdocs"

    def test_tag_attributes_work_with_class_proxy(self):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "bs4.toml")
        soup = bs4.BeautifulSoup("<p data-kind='note'>hello <b>world</b></p>", "html.parser")
        tag = soup.find("p")
        proxy = ClassProxy(tag, mapping.attributes)

        assert proxy.احصل("data-kind") == "note"
        assert proxy.ابحث("b").text == "world"
        assert proxy.احصل_نص(" ", strip=True) == "hello world"


class TestBeautifulSoupTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "bs4.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "bs4"
        assert data["meta"]["arabic_name"] == "تحليل_ويب"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "bs4.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 20
