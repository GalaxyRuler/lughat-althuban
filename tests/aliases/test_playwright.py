# tests/aliases/test_playwright.py
# C-024: Arabic aliases for Playwright async API

import pathlib

import pytest

playwright_async = pytest.importorskip("playwright.async_api", reason="playwright not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def متصفح_الي():
    """Return a ModuleProxy wrapping `playwright.async_api`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("متصفح_الي", None, None)
    assert spec is not None, "AliasFinder did not find 'متصفح_الي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestPlaywrightCore:
    def test_async_entry_point_and_core_classes(self, متصفح_الي):
        assert متصفح_الي.شغل_غير_متزامن is playwright_async.async_playwright
        assert متصفح_الي.متصفح is playwright_async.Browser
        assert متصفح_الي.سياق_متصفح is playwright_async.BrowserContext
        assert متصفح_الي.صفحه is playwright_async.Page
        assert متصفح_الي.محدد is playwright_async.Locator
        assert متصفح_الي.توقع is playwright_async.expect

    def test_errors(self, متصفح_الي):
        assert متصفح_الي.خطا_بلاي_رايت is playwright_async.Error
        assert متصفح_الي.خطا_مهله is playwright_async.TimeoutError


class TestPlaywrightNoBrowser:
    def test_page_locator_and_browser_methods_are_mapped_without_launching(self):
        from arabicpython.aliases import load_mapping

        mapping = load_mapping(ALIASES_DIR / "playwright.toml")

        for arabic_name in ["اذهب", "انقر", "املا", "محدد", "حسب_نص", "لقطه_شاشه"]:
            assert hasattr(playwright_async.Page, mapping.attributes[arabic_name])

        for arabic_name in ["انقر", "املا", "عدد", "اول", "اخر", "رقم", "انتظر"]:
            assert hasattr(playwright_async.Locator, mapping.attributes[arabic_name])

        assert hasattr(playwright_async.BrowserContext, mapping.attributes["صفحه_جديده"])
        assert hasattr(playwright_async.Browser, mapping.attributes["سياق_جديد"])


class TestPlaywrightTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "playwright.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "playwright.async_api"
        assert data["meta"]["arabic_name"] == "متصفح_الي"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "playwright.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 15
