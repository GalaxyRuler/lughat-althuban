# tests/aliases/test_sys.py
# B-030 stdlib aliases — sys module tests

import pathlib
import sys

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نظام_بايثون():
    """Return a ModuleProxy wrapping `sys` via the real sys.toml mapping."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نظام_بايثون", None, None)
    assert spec is not None, "AliasFinder did not find 'نظام_بايثون'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSysProxy:
    def test_argv_alias(self, نظام_بايثون):
        """الوسائط maps to sys.argv (the same list object)."""
        assert نظام_بايثون.الوسائط is sys.argv

    def test_path_alias(self, نظام_بايثون):
        """مسارات_الاستيراد maps to sys.path (the same list object)."""
        assert نظام_بايثون.مسارات_الاستيراد is sys.path

    def test_version_alias(self, نظام_بايثون):
        """الاصدار maps to sys.version (a non-empty string)."""
        v = نظام_بايثون.الاصدار
        assert isinstance(v, str)
        assert len(v) > 0

    def test_platform_alias(self, نظام_بايثون):
        """المنصه maps to sys.platform."""
        assert نظام_بايثون.المنصه == sys.platform

    def test_getrecursionlimit_alias(self, نظام_بايثون):
        """حد_العوديه maps to sys.getrecursionlimit; returns a positive int."""
        limit = نظام_بايثون.حد_العوديه()
        assert isinstance(limit, int)
        assert limit > 0

    def test_stdout_alias(self, نظام_بايثون):
        """معيار_الاخراج maps to sys.stdout."""
        assert نظام_بايثون.معيار_الاخراج is sys.stdout
