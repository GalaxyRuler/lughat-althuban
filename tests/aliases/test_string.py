# tests/aliases/test_string.py
# B-034 stdlib aliases — string module tests

import pathlib
import string

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نصوص():
    """Return a ModuleProxy wrapping `string`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نصوص", None, None)
    assert spec is not None, "AliasFinder did not find 'نصوص'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestStringProxy:
    # ── Constant aliases ──────────────────────────────────────────────────────

    def test_ascii_letters_alias(self, نصوص):
        """احرف_اسكي maps to string.ascii_letters."""
        assert نصوص.احرف_اسكي == string.ascii_letters

    def test_ascii_lowercase_alias(self, نصوص):
        """احرف_صغيره maps to string.ascii_lowercase."""
        assert نصوص.احرف_صغيره == string.ascii_lowercase

    def test_ascii_uppercase_alias(self, نصوص):
        """احرف_كبيره maps to string.ascii_uppercase."""
        assert نصوص.احرف_كبيره == string.ascii_uppercase

    def test_digits_alias(self, نصوص):
        """ارقام maps to string.digits."""
        assert نصوص.ارقام == string.digits

    def test_hexdigits_alias(self, نصوص):
        """ارقام_سداسيه maps to string.hexdigits."""
        assert نصوص.ارقام_سداسيه == string.hexdigits

    def test_octdigits_alias(self, نصوص):
        """ارقام_ثمانيه maps to string.octdigits."""
        assert نصوص.ارقام_ثمانيه == string.octdigits

    def test_printable_alias(self, نصوص):
        """قابل_طباعه maps to string.printable."""
        assert نصوص.قابل_طباعه == string.printable

    def test_punctuation_alias(self, نصوص):
        """ترقيم maps to string.punctuation."""
        assert نصوص.ترقيم == string.punctuation

    def test_whitespace_alias(self, نصوص):
        """فراغات maps to string.whitespace."""
        assert نصوص.فراغات == string.whitespace

    # ── Function aliases ──────────────────────────────────────────────────────

    def test_capwords_alias(self, نصوص):
        """حرف_اول_كبير maps to string.capwords."""
        assert نصوص.حرف_اول_كبير is string.capwords

    def test_capwords_functional(self, نصوص):
        """حرف_اول_كبير capitalizes each word."""
        assert نصوص.حرف_اول_كبير("hello world") == "Hello World"
        assert نصوص.حرف_اول_كبير("مرحبا بالعالم") == "مرحبا بالعالم"

    # ── Class aliases ─────────────────────────────────────────────────────────

    def test_template_alias(self, نصوص):
        """قالب maps to string.Template."""
        assert نصوص.قالب is string.Template

    def test_formatter_alias(self, نصوص):
        """منسق maps to string.Formatter."""
        assert نصوص.منسق is string.Formatter

    # ── Template unbound method tests ─────────────────────────────────────────

    def test_template_substitute_unbound(self, نصوص):
        """بديل is Template.substitute (unbound); substitutes variables."""
        t = string.Template("مرحبا $name!")
        result = نصوص.بديل(t, name="محمد")
        assert result == "مرحبا محمد!"

    def test_template_safe_substitute_unbound(self, نصوص):
        """بديل_امن is Template.safe_substitute (unbound); missing keys left as-is."""
        t = string.Template("Hello $name, from $place!")
        result = نصوص.بديل_امن(t, name="Ali")
        assert "Ali" in result
        assert "$place" in result  # missing key left unchanged

    # ── Constant content checks ───────────────────────────────────────────────

    def test_digits_content(self, نصوص):
        """ارقام contains exactly '0123456789'."""
        assert نصوص.ارقام == "0123456789"

    def test_ascii_letters_contains_both_cases(self, نصوص):
        """احرف_اسكي contains both lower and upper case letters."""
        assert "a" in نصوص.احرف_اسكي
        assert "Z" in نصوص.احرف_اسكي
        assert len(نصوص.احرف_اسكي) == 52
