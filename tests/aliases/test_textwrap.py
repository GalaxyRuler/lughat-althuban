# tests/aliases/test_textwrap.py
# B-034 stdlib aliases — textwrap module tests

import pathlib
import textwrap

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def تنسيق_نص():
    """Return a ModuleProxy wrapping `textwrap`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("تنسيق_نص", None, None)
    assert spec is not None, "AliasFinder did not find 'تنسيق_نص'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestTextwrapProxy:
    # ── Class and function aliases ────────────────────────────────────────────

    def test_textwrapper_alias(self, تنسيق_نص):
        """ملتف_نص maps to textwrap.TextWrapper."""
        assert تنسيق_نص.ملتف_نص is textwrap.TextWrapper

    def test_wrap_alias(self, تنسيق_نص):
        """التف maps to textwrap.wrap."""
        assert تنسيق_نص.التف is textwrap.wrap

    def test_fill_alias(self, تنسيق_نص):
        """امل maps to textwrap.fill."""
        assert تنسيق_نص.امل is textwrap.fill

    def test_shorten_alias(self, تنسيق_نص):
        """اختصر maps to textwrap.shorten."""
        assert تنسيق_نص.اختصر is textwrap.shorten

    def test_dedent_alias(self, تنسيق_نص):
        """ازل_مسافه maps to textwrap.dedent."""
        assert تنسيق_نص.ازل_مسافه is textwrap.dedent

    def test_indent_alias(self, تنسيق_نص):
        """اضف_بادئه maps to textwrap.indent."""
        assert تنسيق_نص.اضف_بادئه is textwrap.indent

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_wrap_splits_long_line(self, تنسيق_نص):
        """التف wraps a long string into lines of the given width."""
        long_text = "This is a long line that needs to be wrapped properly."
        lines = تنسيق_نص.التف(long_text, width=20)
        assert isinstance(lines, list)
        assert all(len(line) <= 20 for line in lines)
        assert len(lines) > 1

    def test_fill_returns_string(self, تنسيق_نص):
        """امل returns a single wrapped string (joined lines)."""
        result = تنسيق_نص.امل("Hello world test string for wrapping.", width=15)
        assert isinstance(result, str)
        assert "\n" in result

    def test_shorten_truncates(self, تنسيق_نص):
        """اختصر shortens a long string to fit the given width."""
        result = تنسيق_نص.اختصر("This is a very long sentence that exceeds the limit.", width=25)
        assert len(result) <= 25
        assert result.endswith("[...]") or "..." in result or len(result) <= 25

    def test_dedent_removes_common_indent(self, تنسيق_نص):
        """ازل_مسافه removes common leading whitespace from all lines."""
        indented = "    line one\n    line two\n    line three"
        result = تنسيق_نص.ازل_مسافه(indented)
        assert not result.startswith(" ")
        assert "line one" in result

    def test_indent_adds_prefix(self, تنسيق_نص):
        """اضف_بادئه prepends a prefix to each line."""
        text = "line one\nline two\nline three"
        result = تنسيق_نص.اضف_بادئه(text, "  > ")
        for line in result.splitlines():
            assert line.startswith("  > ")

    # ── TextWrapper unbound method tests ──────────────────────────────────────

    def test_textwrapper_wrap_unbound(self, تنسيق_نص):
        """التف_كائن is TextWrapper.wrap (unbound); wraps using wrapper settings."""
        wrapper = textwrap.TextWrapper(width=20)
        lines = تنسيق_نص.التف_كائن(wrapper, "A moderately long sentence that wraps.")
        assert isinstance(lines, list)
        assert all(len(line) <= 20 for line in lines)

    def test_textwrapper_fill_unbound(self, تنسيق_نص):
        """امل_كائن is TextWrapper.fill (unbound); returns wrapped string."""
        wrapper = textwrap.TextWrapper(width=15)
        result = تنسيق_نص.امل_كائن(wrapper, "Hello world this is a test.")
        assert isinstance(result, str)

    def test_wrap_arabic_text(self, تنسيق_نص):
        """التف wraps an Arabic string into lines."""
        arabic = "هذا نص عربي طويل يحتاج إلى تقسيم على عدة أسطر للعرض الصحيح في التطبيق"
        lines = تنسيق_نص.التف(arabic, width=20)
        assert len(lines) > 1
