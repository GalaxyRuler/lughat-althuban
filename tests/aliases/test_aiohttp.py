# tests/aliases/test_aiohttp.py
# B-059: Arabic aliases for aiohttp

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

aiohttp = pytest.importorskip("aiohttp", reason="aiohttp not installed")


@pytest.fixture(scope="module")
def أيو_هتب():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("أيو_هتب", None, None)
    assert spec is not None, "AliasFinder did not find 'أيو_هتب'"
    proxy = spec.loader.create_module(spec)
    return proxy


class TestAiohttpAliasesExist:
    def test_client_session(self, أيو_هتب):
        assert أيو_هتب.جلسه_غير_متزامنه is aiohttp.ClientSession

    def test_client_error(self, أيو_هتب):
        assert أيو_هتب.خطا_عميل is aiohttp.ClientError

    def test_client_response_error(self, أيو_هتب):
        assert أيو_هتب.خطا_استجابه is aiohttp.ClientResponseError

    def test_client_connection_error(self, أيو_هتب):
        assert أيو_هتب.خطا_اتصال_غير_متزامن is aiohttp.ClientConnectionError

    def test_client_timeout(self, أيو_هتب):
        assert أيو_هتب.مهله_عميل is aiohttp.ClientTimeout

    def test_tcp_connector(self, أيو_هتب):
        assert أيو_هتب.اعدادات_اتصال is aiohttp.TCPConnector

    def test_basic_auth(self, أيو_هتب):
        assert أيو_هتب.ترميز_عنوان is aiohttp.BasicAuth

    def test_form_data(self, أيو_هتب):
        assert أيو_هتب.بيانات_متعدده is aiohttp.FormData

    def test_stream_reader(self, أيو_هتب):
        assert أيو_هتب.قارئ_مجري is aiohttp.StreamReader


class TestAiohttpTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "aiohttp.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "aiohttp"
        assert data["meta"]["arabic_name"] == "أيو_هتب"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "aiohttp.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 8
