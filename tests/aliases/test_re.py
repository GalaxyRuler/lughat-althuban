# tests/aliases/test_re.py
# B-034 stdlib aliases — re module tests

import pathlib
import re

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def تعابير_نمطيه():
    """Return a ModuleProxy wrapping `re`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("تعابير_نمطيه", None, None)
    assert spec is not None, "AliasFinder did not find 'تعابير_نمطيه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestReProxy:
    # ── Class and exception aliases ───────────────────────────────────────────

    def test_pattern_alias(self, تعابير_نمطيه):
        """نمط maps to re.Pattern."""
        assert تعابير_نمطيه.نمط is re.Pattern

    def test_match_alias(self, تعابير_نمطيه):
        """نتيجة_بحث maps to re.Match."""
        assert تعابير_نمطيه.نتيجة_بحث is re.Match

    def test_pattern_error_alias(self, تعابير_نمطيه):
        """خطا_نمط maps to re.error (re.PatternError alias added in 3.13)."""
        assert تعابير_نمطيه.خطا_نمط is re.error

    # ── Flag aliases ──────────────────────────────────────────────────────────

    def test_ignorecase_alias(self, تعابير_نمطيه):
        """تجاهل_حاله maps to re.IGNORECASE."""
        assert تعابير_نمطيه.تجاهل_حاله == re.IGNORECASE

    def test_multiline_alias(self, تعابير_نمطيه):
        """متعدد_اسطر maps to re.MULTILINE."""
        assert تعابير_نمطيه.متعدد_اسطر == re.MULTILINE

    def test_dotall_alias(self, تعابير_نمطيه):
        """نقطة_للكل maps to re.DOTALL."""
        assert تعابير_نمطيه.نقطة_للكل == re.DOTALL

    # ── Module-level function aliases ─────────────────────────────────────────

    def test_search_alias(self, تعابير_نمطيه):
        """بحث maps to re.search."""
        assert تعابير_نمطيه.بحث is re.search

    def test_match_func_alias(self, تعابير_نمطيه):
        """طابق maps to re.match."""
        assert تعابير_نمطيه.طابق is re.match

    def test_findall_alias(self, تعابير_نمطيه):
        """ابحث_الكل maps to re.findall."""
        assert تعابير_نمطيه.ابحث_الكل is re.findall

    def test_finditer_alias(self, تعابير_نمطيه):
        """ابحث_مكرر maps to re.finditer."""
        assert تعابير_نمطيه.ابحث_مكرر is re.finditer

    def test_sub_alias(self, تعابير_نمطيه):
        """عوض maps to re.sub."""
        assert تعابير_نمطيه.عوض is re.sub

    def test_split_alias(self, تعابير_نمطيه):
        """قسم maps to re.split."""
        assert تعابير_نمطيه.قسم is re.split

    def test_compile_alias(self, تعابير_نمطيه):
        """رجم maps to re.compile."""
        assert تعابير_نمطيه.رجم is re.compile

    def test_escape_alias(self, تعابير_نمطيه):
        """هرب maps to re.escape."""
        assert تعابير_نمطيه.هرب is re.escape

    def test_fullmatch_alias(self, تعابير_نمطيه):
        """طابق_كامل maps to re.fullmatch."""
        assert تعابير_نمطيه.طابق_كامل is re.fullmatch

    # ── Functional search tests ───────────────────────────────────────────────

    def test_search_finds_digit(self, تعابير_نمطيه):
        """بحث finds a digit pattern in an Arabic/English string."""
        m = تعابير_نمطيه.بحث(r"\d+", "السعر: 42 ريال")
        assert m is not None
        assert m.group(0) == "42"

    def test_findall_arabic_words(self, تعابير_نمطيه):
        """ابحث_الكل returns all Arabic word matches."""
        words = تعابير_نمطيه.ابحث_الكل(r"[\u0600-\u06ff]+", "hello مرحبا world عالم")
        assert words == ["مرحبا", "عالم"]

    def test_sub_replaces_digits(self, تعابير_نمطيه):
        """عوض (re.sub) replaces all digits with X."""
        result = تعابير_نمطيه.عوض(r"\d", "X", "abc 123 def 456")
        assert result == "abc XXX def XXX"

    def test_split_on_comma(self, تعابير_نمطيه):
        """قسم splits a string on commas."""
        parts = تعابير_نمطيه.قسم(r",\s*", "a, b, c")
        assert parts == ["a", "b", "c"]

    def test_ignorecase_flag(self, تعابير_نمطيه):
        """تجاهل_حاله flag makes search case-insensitive."""
        m = تعابير_نمطيه.بحث("hello", "HELLO WORLD", تعابير_نمطيه.تجاهل_حاله)
        assert m is not None

    # ── Compiled pattern (unbound method) tests ───────────────────────────────

    def test_compile_and_pattern_search_unbound(self, تعابير_نمطيه):
        """رجم + بحث_نمط (Pattern.search unbound) finds a match."""
        pat = تعابير_نمطيه.رجم(r"\d+")
        m = تعابير_نمطيه.بحث_نمط(pat, "price: 99")
        assert m is not None
        assert m.group(0) == "99"

    def test_pattern_findall_unbound(self, تعابير_نمطيه):
        """ابحث_الكل_نمط is Pattern.findall (unbound); returns all matches."""
        pat = re.compile(r"[A-Z]+")
        result = تعابير_نمطيه.ابحث_الكل_نمط(pat, "Hello World FOO")
        assert result == ["H", "W", "FOO"]

    def test_pattern_split_unbound(self, تعابير_نمطيه):
        """قسم_نمط is Pattern.split (unbound); splits correctly."""
        pat = re.compile(r"\s+")
        result = تعابير_نمطيه.قسم_نمط(pat, "hello world  test")
        assert result == ["hello", "world", "test"]

    # ── Match object (unbound method) tests ──────────────────────────────────

    def test_match_group_unbound(self, تعابير_نمطيه):
        """مجموعه is Match.group (unbound); returns the full match."""
        m = re.search(r"(\d+)", "abc 42")
        assert تعابير_نمطيه.مجموعه(m, 0) == "42"
        assert تعابير_نمطيه.مجموعه(m, 1) == "42"

    def test_match_span_unbound(self, تعابير_نمطيه):
        """نطاق is Match.span (unbound); returns (start, end) tuple."""
        m = re.search(r"\d+", "price: 99 sar")
        start, end = تعابير_نمطيه.نطاق(m)
        assert start == 7
        assert end == 9

    def test_match_groups_unbound(self, تعابير_نمطيه):
        """مجموعات is Match.groups (unbound); returns all capture groups."""
        m = re.search(r"(\d+)-(\d+)", "range: 10-20")
        groups = تعابير_نمطيه.مجموعات(m)
        assert groups == ("10", "20")

    # ── Error handling ────────────────────────────────────────────────────────

    def test_pattern_error_raised_on_bad_regex(self, تعابير_نمطيه):
        """خطا_نمط (re.error) is raised for an invalid regular expression."""
        with pytest.raises(re.error):
            تعابير_نمطيه.رجم("[invalid(")
