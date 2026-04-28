# C-026 — PyJWT aliases (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-026 — Arabic aliases for `PyJWT` (import jwt)

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/aliases/flask.toml (TOML format)

## Steps

Create: arabicpython/aliases/jwt.toml
Arabic module name: جي_دبليو_تي

Required [entries]:
  encode                →  شفّر
  decode                →  فكّ_التشفير
  get_unverified_header →  اجلب_الراس_دون_تحقق
  PyJWTError            →  خطا_jwt
  InvalidTokenError     →  خطا_رمز_غير_صالح
  DecodeError           →  خطا_فك_تشفير
  ExpiredSignatureError →  خطا_رمز_منتهي
  InvalidSignatureError →  خطا_توقيع_غير_صالح
  InvalidAlgorithmError →  خطا_خوارزميه_غير_صالحه
  algorithms            →  خوارزميات

Create: examples/C26_jwt_demo.apy — encode a payload with a secret,
  decode it, handle ExpiredSignatureError.

Create: tests/test_aliases_jwt.py — standard alias smoke tests.
Update specs/INDEX.md: C-026 → delivered.
