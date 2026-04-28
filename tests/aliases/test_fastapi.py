# tests/aliases/test_fastapi.py
# B-011: Arabic aliases for FastAPI — فاست_أبي

import pathlib

import pytest

fastapi = pytest.importorskip("fastapi", reason="fastapi not installed — skipping")

import fastapi as fa  # noqa: E402
import fastapi.responses as fa_responses  # noqa: E402
import fastapi.security as fa_security  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def فاست_أبي():
    """Return a ModuleProxy wrapping `fastapi`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("فاست_أبي", None, None)
    assert spec is not None, "AliasFinder did not find 'فاست_أبي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core app & routing ────────────────────────────────────────────────────────


class TestCoreApp:
    def test_fastapi_class_alias(self, فاست_أبي):
        assert فاست_أبي.تطبيق_سريع is fa.FastAPI

    def test_api_router_alias(self, فاست_أبي):
        assert فاست_أبي.موجه_api is fa.APIRouter

    def test_fastapi_instantiable(self, فاست_أبي):
        app = فاست_أبي.تطبيق_سريع()
        assert hasattr(app, "get")
        assert hasattr(app, "post")
        assert hasattr(app, "include_router")

    def test_router_instantiable(self, فاست_أبي):
        router = فاست_أبي.موجه_api()
        assert hasattr(router, "get")
        assert hasattr(router, "post")


# ── Parameter functions ───────────────────────────────────────────────────────


class TestParamFunctions:
    def test_query_alias(self, فاست_أبي):
        assert فاست_أبي.استعلام is fa.Query

    def test_path_alias(self, فاست_أبي):
        assert فاست_أبي.مسار_معامل is fa.Path

    def test_body_alias(self, فاست_أبي):
        assert فاست_أبي.جسم is fa.Body

    def test_form_alias(self, فاست_أبي):
        assert فاست_أبي.استماره is fa.Form

    def test_header_alias(self, فاست_أبي):
        assert فاست_أبي.ترويسه is fa.Header

    def test_cookie_alias(self, فاست_أبي):
        assert فاست_أبي.كوكي is fa.Cookie

    def test_file_alias(self, فاست_أبي):
        assert فاست_أبي.ملف is fa.File

    def test_upload_file_alias(self, فاست_أبي):
        assert فاست_أبي.ملف_مرفوع is fa.UploadFile


# ── Dependency injection ──────────────────────────────────────────────────────


class TestDependencyInjection:
    def test_depends_alias(self, فاست_أبي):
        assert فاست_أبي.يعتمد_علي is fa.Depends

    def test_security_alias(self, فاست_أبي):
        assert فاست_أبي.امان is fa.Security

    def test_depends_callable(self, فاست_أبي):
        """Depends wraps a callable and produces a dependency marker."""

        def get_db():
            return "db"

        dep = فاست_أبي.يعتمد_علي(get_db)
        assert dep.dependency is get_db


# ── HTTP primitives ───────────────────────────────────────────────────────────


class TestHTTPPrimitives:
    def test_http_exception_alias(self, فاست_أبي):
        assert فاست_أبي.استثناء_http is fa.HTTPException

    def test_request_alias(self, فاست_أبي):
        assert فاست_أبي.طلب_http is fa.Request

    def test_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_http is fa.Response

    def test_background_tasks_alias(self, فاست_أبي):
        assert فاست_أبي.مهام_خلفيه is fa.BackgroundTasks

    def test_http_exception_is_exception(self, فاست_أبي):
        assert issubclass(فاست_أبي.استثناء_http, Exception)

    def test_http_exception_has_status_code(self, فاست_أبي):
        exc = فاست_أبي.استثناء_http(status_code=404, detail="not found")
        assert exc.status_code == 404
        assert exc.detail == "not found"


# ── WebSocket ─────────────────────────────────────────────────────────────────


class TestWebSocket:
    def test_websocket_alias(self, فاست_أبي):
        assert فاست_أبي.وصله_ويب is fa.WebSocket

    def test_websocket_disconnect_alias(self, فاست_أبي):
        assert فاست_أبي.قطع_وصله_ويب is fa.WebSocketDisconnect

    def test_websocket_exception_alias(self, فاست_أبي):
        assert فاست_أبي.استثناء_وصله_ويب is fa.WebSocketException


# ── Response types ────────────────────────────────────────────────────────────


class TestResponseTypes:
    def test_json_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_json is fa_responses.JSONResponse

    def test_html_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_html is fa_responses.HTMLResponse

    def test_plain_text_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_نص is fa_responses.PlainTextResponse

    def test_streaming_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_تدفق is fa_responses.StreamingResponse

    def test_file_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_ملف is fa_responses.FileResponse

    def test_redirect_response_alias(self, فاست_أبي):
        assert فاست_أبي.رد_توجيه is fa_responses.RedirectResponse

    def test_json_response_functional(self, فاست_أبي):
        """رد_json produces a valid JSONResponse with the given content."""
        resp = فاست_أبي.رد_json(content={"مرحبا": "عالم"})
        assert resp.status_code == 200

    def test_html_response_functional(self, فاست_أبي):
        resp = فاست_أبي.رد_html(content="<h1>مرحبا</h1>")
        assert resp.status_code == 200


# ── Security ──────────────────────────────────────────────────────────────────


class TestSecurity:
    def test_api_key_header_alias(self, فاست_أبي):
        assert فاست_أبي.مفتاح_api_راس is fa_security.APIKeyHeader

    def test_api_key_query_alias(self, فاست_أبي):
        assert فاست_أبي.مفتاح_api_استعلام is fa_security.APIKeyQuery

    def test_api_key_cookie_alias(self, فاست_أبي):
        assert فاست_أبي.مفتاح_api_كوكي is fa_security.APIKeyCookie

    def test_oauth2_bearer_alias(self, فاست_أبي):
        assert فاست_أبي.حامل_oauth2 is fa_security.OAuth2PasswordBearer

    def test_oauth2_form_alias(self, فاست_أبي):
        assert فاست_أبي.نموذج_oauth2 is fa_security.OAuth2PasswordRequestForm

    def test_http_basic_alias(self, فاست_أبي):
        assert فاست_أبي.http_اساسي is fa_security.HTTPBasic

    def test_http_bearer_alias(self, فاست_أبي):
        assert فاست_أبي.http_حامل is fa_security.HTTPBearer

    def test_oauth2_bearer_instantiable(self, فاست_أبي):
        """OAuth2PasswordBearer requires tokenUrl at construction."""
        scheme = فاست_أبي.حامل_oauth2(tokenUrl="token")
        assert hasattr(scheme, "model")


# ── Submodules ────────────────────────────────────────────────────────────────


class TestSubmodules:
    def test_responses_submodule_alias(self, فاست_أبي):
        assert فاست_أبي.استجابات is fa.responses

    def test_status_submodule_alias(self, فاست_أبي):
        assert فاست_أبي.رموز_الحاله_http is fa.status

    def test_security_submodule_alias(self, فاست_أبي):
        assert فاست_أبي.امان_fastapi is fa.security

    def test_status_codes_accessible(self, فاست_أبي):
        """HTTP status codes accessible via رموز_الحاله_http."""
        assert فاست_أبي.رموز_الحاله_http.HTTP_200_OK == 200
        assert فاست_أبي.رموز_الحاله_http.HTTP_404_NOT_FOUND == 404
        assert فاست_أبي.رموز_الحاله_http.HTTP_500_INTERNAL_SERVER_ERROR == 500
