# Spec Packet B-011: aliases-fastapi-v1

**Phase**: B
**Depends on**: B-001 (alias-runtime-v1), B-002 (phase-a-compat-suite), B-040 (dictionary-v1.1-async-match)
**Estimated size**: medium
**Owner**: —

## Goal

Ship the Arabic alias mapping for FastAPI, including support for async route handlers. Mirror the structure of B-010 (Flask).

## Non-goals

- No Pydantic-specific mapping (beyond what's needed for FastAPI basic usage).
- No SQLAlchemy/Databases integration (handled in B-013).
- No production deployment (uvicorn/gunicorn).

## Files

### Files to create

- `arabicpython/aliases/fastapi.toml`
- `tests/test_aliases_fastapi.py`
- `examples/B11_fastapi_hello.apy`
- `examples/B11_README-ar.md`

## Public interfaces

### `arabicpython/aliases/fastapi.toml`

[meta]
arabic_name    = "فاست_أبي"
python_module  = "fastapi"
dict_version   = "ar-v1"
schema_version = 1
proxy_classes  = ["FastAPI", "APIRouter"]

[entries]
"تطبيق_سريع"          = "FastAPI"
"موجه_api"             = "APIRouter"

"اضف_برمجيات_وسيطه"   = "FastAPI.add_middleware"
"احصل_مسار"            = "FastAPI.get"
"ضم_موجه"              = "FastAPI.include_router"
"انشر"                 = "FastAPI.post"

"احصل_موجه"            = "APIRouter.get"
"ضم_موجه_فرعي"         = "APIRouter.include_router"
"انشر_موجه"            = "APIRouter.post"

"استعلام"              = "Query"
"مسار_معامل"           = "Path"
"جسم"                  = "Body"
"استماره"              = "Form"
"ترويسه"               = "Header"
"كوكي"                 = "Cookie"
"ملف"                  = "File"
"ملف_مرفوع"            = "UploadFile"

"يعتمد_علي"            = "Depends"
"امان"                 = "Security"

"استثناء_http"         = "HTTPException"
"طلب_http"             = "Request"
"رد_http"              = "Response"
"مهام_خلفيه"           = "BackgroundTasks"

"وصله_ويب"             = "WebSocket"
"قطع_وصله_ويب"         = "WebSocketDisconnect"
"استثناء_وصله_ويب"     = "WebSocketException"

"رد_json"              = "responses.JSONResponse"
"رد_html"              = "responses.HTMLResponse"
"رد_نص"                = "responses.PlainTextResponse"
"رد_تدفق"              = "responses.StreamingResponse"
"رد_ملف"               = "responses.FileResponse"
"رد_توجيه"             = "responses.RedirectResponse"

"مفتاح_api_راس"        = "security.APIKeyHeader"
"مفتاح_api_استعلام"    = "security.APIKeyQuery"
"مفتاح_api_كوكي"       = "security.APIKeyCookie"
"حامل_oauth2"          = "security.OAuth2PasswordBearer"
"نموذج_oauth2"         = "security.OAuth2PasswordRequestForm"
"http_اساسي"           = "security.HTTPBasic"
"http_حامل"            = "security.HTTPBearer"

"استجابات"             = "responses"
"رموز_الحاله_http"     = "status"
"امان_fastapi"         = "security"
"برمجيات_وسيطه"        = "middleware"

[attributes]
"اضف_برمجيات_وسيطه"   = "add_middleware"
"احصل"                 = "get"
"المحتوي"              = "content"
"انشر"                 = "post"
"حموله_json"           = "json"
"رمز_الحاله"           = "status_code"
"ضم_موجه"              = "include_router"

Note: `احصل_مسار` is the FastAPI app-level GET route decorator. The shorter
`احصل` entry belongs to `طلبات.get` and remains available as a generic
returned-object attribute alias for wrapped objects whose Python method is
named `get`.

### `examples/B11_fastapi_hello.apy`

```python
# arabicpython: dict=ar-v1.1
استورد فاست_أبي

تطبيق = فاست_أبي.تطبيق_سريع()

@تطبيق.احصل_مسار("/")
متزامن دالة الرئيسيه():
    ارجع {"رسالة": "مرحبا بك في فاست أبي العربي"}

@تطبيق.احصل_مسار("/سلام/{اسم}")
متزامن دالة سلام_على(اسم: نص):
    ارجع {"رسالة": f"السلام عليكم يا {اسم}"}

إذا __اسم__ == "__main__":
    استورد uvicorn
    uvicorn.run(تطبيق, host="0.0.0.0", port=8000)
```

## Implementation constraints

- **Cite B-010 as structural prior.** This packet follows the same deliverable structure and naming conventions.
- **Instance methods:** `FastAPI` and `APIRouter` are listed in
  `proxy_classes`, so returned application/router objects expose curated Arabic
  method names. Use `احصل_مسار` for `FastAPI.get` to avoid the existing
  `طلبات.احصل` module-entry collision; use `احصل_موجه` for `APIRouter.get`.
- **Acceptance checklist must include Phase A compat assertion.**
- **Ensure all Arabic names round-trip through `normalize_identifier`.**

## Test requirements

- Similar to B-010, but specifically testing async route handling and FastAPI-specific dependency injection (`Depends`).

## Acceptance checklist

- [ ] `arabicpython/aliases/fastapi.toml` shipped with at least 40 entries.
- [ ] All integration tests pass.
- [ ] `examples/B11_fastapi_hello.apy` runs end-to-end.
- [ ] `examples/B11_README-ar.md` written.
- [ ] Phase A compat assertion: `tests/test_phase_a_compat.py` still passes.
