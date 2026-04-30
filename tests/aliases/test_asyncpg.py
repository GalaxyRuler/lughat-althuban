# tests/aliases/test_asyncpg.py
# C-019: Arabic aliases for asyncpg

import pathlib

import pytest

asyncpg = pytest.importorskip("asyncpg", reason="asyncpg not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def قاعده_بوست():
    """Return a ModuleProxy wrapping `asyncpg`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("قاعده_بوست", None, None)
    assert spec is not None, "AliasFinder did not find 'قاعده_بوست'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestAsyncpgCore:
    def test_connection_entry_points(self, قاعده_بوست):
        assert قاعده_بوست.اتصل is asyncpg.connect
        assert قاعده_بوست.انشئ_مجمع is asyncpg.create_pool
        assert قاعده_بوست.اتصال is asyncpg.Connection
        assert قاعده_بوست.مجمع is asyncpg.Pool
        assert قاعده_بوست.سجل_قاعده is asyncpg.Record

    def test_exceptions(self, قاعده_بوست):
        import asyncpg.exceptions

        assert قاعده_بوست.خطا_بوست is asyncpg.PostgresError
        assert قاعده_بوست.خطا_واجهه is asyncpg.InterfaceError
        assert قاعده_بوست.خطا_تفرد is asyncpg.exceptions.UniqueViolationError
        assert قاعده_بوست.خطا_مفتاح_خارجي is asyncpg.exceptions.ForeignKeyViolationError


class TestAsyncpgNoServer:
    def test_connection_methods_are_mapped_without_connecting(self):
        from arabicpython.aliases import load_mapping

        mapping = load_mapping(ALIASES_DIR / "asyncpg.toml")
        for arabic_name in ["اجلب", "اجلب_صف", "اجلب_قيمه", "نفذ", "حضر", "عامله"]:
            assert hasattr(asyncpg.Connection, mapping.attributes[arabic_name])

    def test_pool_methods_are_mapped_without_connecting(self):
        from arabicpython.aliases import load_mapping

        mapping = load_mapping(ALIASES_DIR / "asyncpg.toml")
        for arabic_name in ["اجلب", "اجلب_صف", "اجلب_قيمه", "نفذ", "استحوذ", "حرر"]:
            assert hasattr(asyncpg.Pool, mapping.attributes[arabic_name])


class TestAsyncpgTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "asyncpg.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "asyncpg"
        assert data["meta"]["arabic_name"] == "قاعده_بوست"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "asyncpg.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 15
