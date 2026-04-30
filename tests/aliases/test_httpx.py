# tests/aliases/test_httpx.py
# C-013: Arabic aliases for HTTPX

import pathlib

import pytest

httpx = pytest.importorskip("httpx", reason="httpx not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def طلبات_حديثه():
    """Return a ModuleProxy wrapping `httpx`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("طلبات_حديثه", None, None)
    assert spec is not None, "AliasFinder did not find 'طلبات_حديثه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestHttpxTopLevel:
    def test_verbs(self, طلبات_حديثه):
        assert طلبات_حديثه.احصل is httpx.get
        assert طلبات_حديثه.نشر is httpx.post
        assert طلبات_حديثه.ضع is httpx.put
        assert طلبات_حديثه.احذف is httpx.delete
        assert طلبات_حديثه.عدل is httpx.patch
        assert طلبات_حديثه.راس is httpx.head
        assert طلبات_حديثه.خيارات is httpx.options
        assert طلبات_حديثه.اطلب is httpx.request

    def test_core_classes(self, طلبات_حديثه):
        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(طلبات_حديثه.عميل, ClassFactory)
        assert isinstance(طلبات_حديثه.عميل_غير_متزامن, ClassFactory)
        assert طلبات_حديثه.طلب is httpx.Request
        assert طلبات_حديثه.استجابه is httpx.Response
        assert طلبات_حديثه.ترويسات is httpx.Headers
        assert طلبات_حديثه.كوكيز is httpx.Cookies
        assert طلبات_حديثه.ناقل_وهمي is httpx.MockTransport

    def test_exceptions(self, طلبات_حديثه):
        assert طلبات_حديثه.خطا_http is httpx.HTTPError
        assert طلبات_حديثه.خطا_طلب is httpx.RequestError
        assert طلبات_حديثه.خطا_حاله_http is httpx.HTTPStatusError
        assert طلبات_حديثه.خطا_مهله is httpx.TimeoutException
        assert طلبات_حديثه.خطا_اتصال is httpx.ConnectError


class TestHttpxFunctional:
    def test_client_alias_uses_mock_transport(self, طلبات_حديثه):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.method == "GET"
            return httpx.Response(200, json={"ok": True}, request=request)

        transport = طلبات_حديثه.ناقل_وهمي(handler)
        client = طلبات_حديثه.عميل(transport=transport, base_url="https://example.test")

        response = client.احصل_عميل("/ping")

        assert response.status_code == 200
        assert response.json() == {"ok": True}
        client.اغلق_عميل()

    def test_response_attributes_work_with_class_proxy(self):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "httpx.toml")
        request = httpx.Request("GET", "https://example.test/data")
        response = httpx.Response(201, json={"created": True}, request=request)
        proxy = ClassProxy(response, mapping.attributes)

        assert proxy.رمز_الحاله == 201
        assert proxy.بيانات_json() == {"created": True}
        assert str(proxy.رابط) == "https://example.test/data"


class TestHttpxTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "httpx.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "httpx"
        assert data["meta"]["arabic_name"] == "طلبات_حديثه"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "httpx.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 50
