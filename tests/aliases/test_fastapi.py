# tests/aliases/test_fastapi.py
# B-011: Arabic aliases for FastAPI — واجهه_برمجيه

import pathlib

import pytest

fastapi = pytest.importorskip("fastapi", reason="fastapi not installed — skipping")

import fastapi as fa  # noqa: E402
import fastapi.responses as fa_responses  # noqa: E402
import fastapi.security as fa_security  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def واجهه_برمجيه():
    """Return a ModuleProxy wrapping `fastapi`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("واجهه_برمجيه", None, None)
    assert spec is not None, "AliasFinder did not find 'واجهه_برمجيه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core app & routing ────────────────────────────────────────────────────────


class TestCoreApp:
    def test_fastapi_class_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.تطبيق_سريع is fa.FastAPI

    def test_api_router_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.موجه_api is fa.APIRouter

    def test_fastapi_instantiable(self, واجهه_برمجيه):
        app = واجهه_برمجيه.تطبيق_سريع()
        assert hasattr(app, "get")
        assert hasattr(app, "post")
        assert hasattr(app, "include_router")

    def test_router_instantiable(self, واجهه_برمجيه):
        router = واجهه_برمجيه.موجه_api()
        assert hasattr(router, "get")
        assert hasattr(router, "post")


# ── Parameter functions ───────────────────────────────────────────────────────


class TestParamFunctions:
    def test_query_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.استعلام is fa.Query

    def test_path_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.مسار_معامل is fa.Path

    def test_body_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.جسم is fa.Body

    def test_form_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.استماره is fa.Form

    def test_header_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.ترويسه is fa.Header

    def test_cookie_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.كوكي is fa.Cookie

    def test_file_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.ملف is fa.File

    def test_upload_file_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.ملف_مرفوع is fa.UploadFile


# ── Dependency injection ──────────────────────────────────────────────────────


class TestDependencyInjection:
    def test_depends_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.يعتمد_علي is fa.Depends

    def test_security_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.امان is fa.Security

    def test_depends_callable(self, واجهه_برمجيه):
        """Depends wraps a callable and produces a dependency marker."""

        def get_db():
            return "db"

        dep = واجهه_برمجيه.يعتمد_علي(get_db)
        assert dep.dependency is get_db


# ── HTTP primitives ───────────────────────────────────────────────────────────


class TestHTTPPrimitives:
    def test_http_exception_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.استثناء_http is fa.HTTPException

    def test_request_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.طلب_http is fa.Request

    def test_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_http is fa.Response

    def test_background_tasks_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.مهام_خلفيه is fa.BackgroundTasks

    def test_http_exception_is_exception(self, واجهه_برمجيه):
        assert issubclass(واجهه_برمجيه.استثناء_http, Exception)

    def test_http_exception_has_status_code(self, واجهه_برمجيه):
        exc = واجهه_برمجيه.استثناء_http(status_code=404, detail="not found")
        assert exc.status_code == 404
        assert exc.detail == "not found"


# ── WebSocket ─────────────────────────────────────────────────────────────────


class TestWebSocket:
    def test_websocket_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.وصله_ويب is fa.WebSocket

    def test_websocket_disconnect_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.قطع_وصله_ويب is fa.WebSocketDisconnect

    def test_websocket_exception_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.استثناء_وصله_ويب is fa.WebSocketException


# ── Response types ────────────────────────────────────────────────────────────


class TestResponseTypes:
    def test_json_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_json is fa_responses.JSONResponse

    def test_html_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_html is fa_responses.HTMLResponse

    def test_plain_text_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_نص is fa_responses.PlainTextResponse

    def test_streaming_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_تدفق is fa_responses.StreamingResponse

    def test_file_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_ملف is fa_responses.FileResponse

    def test_redirect_response_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رد_توجيه is fa_responses.RedirectResponse

    def test_json_response_functional(self, واجهه_برمجيه):
        """رد_json produces a valid JSONResponse with the given content."""
        resp = واجهه_برمجيه.رد_json(content={"مرحبا": "عالم"})
        assert resp.status_code == 200

    def test_html_response_functional(self, واجهه_برمجيه):
        resp = واجهه_برمجيه.رد_html(content="<h1>مرحبا</h1>")
        assert resp.status_code == 200


# ── Security ──────────────────────────────────────────────────────────────────


class TestSecurity:
    def test_api_key_header_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.مفتاح_api_راس is fa_security.APIKeyHeader

    def test_api_key_query_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.مفتاح_api_استعلام is fa_security.APIKeyQuery

    def test_api_key_cookie_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.مفتاح_api_كوكي is fa_security.APIKeyCookie

    def test_oauth2_bearer_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.حامل_oauth2 is fa_security.OAuth2PasswordBearer

    def test_oauth2_form_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.نموذج_oauth2 is fa_security.OAuth2PasswordRequestForm

    def test_http_basic_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.http_اساسي is fa_security.HTTPBasic

    def test_http_bearer_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.http_حامل is fa_security.HTTPBearer

    def test_oauth2_bearer_instantiable(self, واجهه_برمجيه):
        """OAuth2PasswordBearer requires tokenUrl at construction."""
        scheme = واجهه_برمجيه.حامل_oauth2(tokenUrl="token")
        assert hasattr(scheme, "model")


# ── Submodules ────────────────────────────────────────────────────────────────


class TestSubmodules:
    def test_responses_submodule_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.استجابات is fa.responses

    def test_status_submodule_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.رموز_الحاله_http is fa.status

    def test_security_submodule_alias(self, واجهه_برمجيه):
        assert واجهه_برمجيه.امان_fastapi is fa.security

    def test_status_codes_accessible(self, واجهه_برمجيه):
        """HTTP status codes accessible via رموز_الحاله_http."""
        assert واجهه_برمجيه.رموز_الحاله_http.HTTP_200_OK == 200
        assert واجهه_برمجيه.رموز_الحاله_http.HTTP_404_NOT_FOUND == 404
        assert واجهه_برمجيه.رموز_الحاله_http.HTTP_500_INTERNAL_SERVER_ERROR == 500
