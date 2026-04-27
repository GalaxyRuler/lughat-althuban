# tests/aliases/test_argparse.py
# B-039 stdlib aliases — argparse module tests

import argparse
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def محلل_وسائط():
    """Return a ModuleProxy wrapping `argparse`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("محلل_وسائط", None, None)
    assert spec is not None, "AliasFinder did not find 'محلل_وسائط'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestArgparseProxy:
    # ── Main class ────────────────────────────────────────────────────────────

    def test_argument_parser_alias(self, محلل_وسائط):
        """محلل_الوسائط maps to argparse.ArgumentParser."""
        assert محلل_وسائط.محلل_الوسائط is argparse.ArgumentParser

    # ── Result container ──────────────────────────────────────────────────────

    def test_namespace_alias(self, محلل_وسائط):
        """فضاء_اسماء maps to argparse.Namespace."""
        assert محلل_وسائط.فضاء_اسماء is argparse.Namespace

    # ── Action types ──────────────────────────────────────────────────────────

    def test_action_alias(self, محلل_وسائط):
        """اجراء maps to argparse.Action."""
        assert محلل_وسائط.اجراء is argparse.Action

    def test_boolean_optional_action_alias(self, محلل_وسائط):
        """اجراء_منطقي maps to argparse.BooleanOptionalAction."""
        assert محلل_وسائط.اجراء_منطقي is argparse.BooleanOptionalAction

    # ── Formatters ────────────────────────────────────────────────────────────

    def test_help_formatter_alias(self, محلل_وسائط):
        """منسق_مساعده maps to argparse.HelpFormatter."""
        assert محلل_وسائط.منسق_مساعده is argparse.HelpFormatter

    def test_raw_text_formatter_alias(self, محلل_وسائط):
        """منسق_نص_خام maps to argparse.RawTextHelpFormatter."""
        assert محلل_وسائط.منسق_نص_خام is argparse.RawTextHelpFormatter

    def test_raw_description_formatter_alias(self, محلل_وسائط):
        """منسق_وصف_خام maps to argparse.RawDescriptionHelpFormatter."""
        assert محلل_وسائط.منسق_وصف_خام is argparse.RawDescriptionHelpFormatter

    def test_argument_defaults_formatter_alias(self, محلل_وسائط):
        """منسق_قيم_افتراضيه maps to argparse.ArgumentDefaultsHelpFormatter."""
        assert محلل_وسائط.منسق_قيم_افتراضيه is argparse.ArgumentDefaultsHelpFormatter

    def test_metavar_type_formatter_alias(self, محلل_وسائط):
        """منسق_نوع_متغير maps to argparse.MetavarTypeHelpFormatter."""
        assert محلل_وسائط.منسق_نوع_متغير is argparse.MetavarTypeHelpFormatter

    # ── FileType helper ───────────────────────────────────────────────────────

    def test_file_type_alias(self, محلل_وسائط):
        """نوع_ملف maps to argparse.FileType."""
        assert محلل_وسائط.نوع_ملف is argparse.FileType

    # ── Sentinel constants ────────────────────────────────────────────────────

    def test_one_or_more_alias(self, محلل_وسائط):
        """واحد_او_اكثر maps to argparse.ONE_OR_MORE."""
        assert محلل_وسائط.واحد_او_اكثر is argparse.ONE_OR_MORE

    def test_zero_or_more_alias(self, محلل_وسائط):
        """صفر_او_اكثر maps to argparse.ZERO_OR_MORE."""
        assert محلل_وسائط.صفر_او_اكثر is argparse.ZERO_OR_MORE

    def test_optional_alias(self, محلل_وسائط):
        """اختياري maps to argparse.OPTIONAL."""
        assert محلل_وسائط.اختياري is argparse.OPTIONAL

    def test_remainder_alias(self, محلل_وسائط):
        """باقي maps to argparse.REMAINDER."""
        assert محلل_وسائط.باقي is argparse.REMAINDER

    def test_suppress_alias(self, محلل_وسائط):
        """اخفاء maps to argparse.SUPPRESS."""
        assert محلل_وسائط.اخفاء is argparse.SUPPRESS

    # ── Exception types ───────────────────────────────────────────────────────

    def test_argument_error_alias(self, محلل_وسائط):
        """خطا_وسيطه maps to argparse.ArgumentError."""
        assert محلل_وسائط.خطا_وسيطه is argparse.ArgumentError

    def test_argument_type_error_alias(self, محلل_وسائط):
        """خطا_نوع_وسيطه maps to argparse.ArgumentTypeError."""
        assert محلل_وسائط.خطا_نوع_وسيطه is argparse.ArgumentTypeError

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_parser_parses_positional(self, محلل_وسائط):
        """محلل_الوسائط parses a positional argument into فضاء_اسماء."""
        p = محلل_وسائط.محلل_الوسائط(prog="test")
        p.add_argument("اسم")
        ns = p.parse_args(["أحمد"])
        assert isinstance(ns, محلل_وسائط.فضاء_اسماء)
        assert ns.اسم == "أحمد"

    def test_parser_parses_optional_flag(self, محلل_وسائط):
        """Parser handles optional --flag with a default."""
        p = محلل_وسائط.محلل_الوسائط()
        p.add_argument("--عدد", type=int, default=0)
        ns = p.parse_args(["--عدد", "42"])
        assert ns.عدد == 42

    def test_suppress_hides_default(self, محلل_وسائط):
        """اخفاء sentinel suppresses the default value from the namespace."""
        p = محلل_وسائط.محلل_الوسائط()
        p.add_argument("--مخفي", default=محلل_وسائط.اخفاء)
        ns = p.parse_args([])
        assert not hasattr(ns, "مخفي")

    def test_one_or_more_nargs(self, محلل_وسائط):
        """واحد_او_اكثر as nargs requires at least one value."""
        p = محلل_وسائط.محلل_الوسائط()
        p.add_argument("قيم", nargs=محلل_وسائط.واحد_او_اكثر)
        ns = p.parse_args(["a", "b", "c"])
        assert ns.قيم == ["a", "b", "c"]

    def test_zero_or_more_nargs(self, محلل_وسائط):
        """صفر_او_اكثر as nargs allows an empty list."""
        p = محلل_وسائط.محلل_الوسائط()
        p.add_argument("قيم", nargs=محلل_وسائط.صفر_او_اكثر)
        ns = p.parse_args([])
        assert ns.قيم == []

    def test_boolean_optional_action(self, محلل_وسائط):
        """اجراء_منطقي creates --flag / --no-flag pair."""
        p = محلل_وسائط.محلل_الوسائط()
        p.add_argument("--مفعل", action=محلل_وسائط.اجراء_منطقي)
        ns_on = p.parse_args(["--مفعل"])
        ns_off = p.parse_args(["--no-مفعل"])
        assert ns_on.مفعل is True
        assert ns_off.مفعل is False

    def test_namespace_equality(self, محلل_وسائط):
        """فضاء_اسماء objects with equal attributes compare equal."""
        ns1 = محلل_وسائط.فضاء_اسماء(x=1, y=2)
        ns2 = محلل_وسائط.فضاء_اسماء(x=1, y=2)
        assert ns1 == ns2

    def test_argument_type_error_is_exception(self, محلل_وسائط):
        """خطا_نوع_وسيطه is a subclass of Exception."""
        assert issubclass(محلل_وسائط.خطا_نوع_وسيطه, Exception)
