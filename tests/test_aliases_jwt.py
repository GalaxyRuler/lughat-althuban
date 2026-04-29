import importlib
import pathlib
import sys
import tomllib
import datetime as _dt
from datetime import datetime, timedelta

import pytest

jwt = pytest.importorskip("jwt", reason="PyJWT not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    original_path = list(sys.path)
    sys.modules.pop("جي_دبليو_تي", None)
    sys.modules.pop("C26_jwt_demo", None)
    yield
    sys.modules.pop("جي_دبليو_تي", None)
    sys.modules.pop("C26_jwt_demo", None)
    sys.meta_path[:] = original_meta_path
    sys.path[:] = original_path


@pytest.fixture()
def جي_دبليو_تي_proxy():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("جي_دبليو_تي", None, None)
    assert spec is not None, "AliasFinder did not find 'جي_دبليو_تي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_import_جي_دبليو_تي_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    import جي_دبليو_تي

    assert جي_دبليو_تي.شفر is jwt.encode
    assert جي_دبليو_تي.فك_التشفير is jwt.decode


def test_core_symbols_resolve_correctly(جي_دبليو_تي_proxy):
    assert جي_دبليو_تي_proxy.شفر is jwt.encode
    assert جي_دبليو_تي_proxy.فك_التشفير is jwt.decode
    assert جي_دبليو_تي_proxy.اجلب_الراس_دون_تحقق is jwt.get_unverified_header
    assert جي_دبليو_تي_proxy.خطا_jwt is jwt.PyJWTError
    assert جي_دبليو_تي_proxy.خطا_رمز_غير_صالح is jwt.InvalidTokenError
    assert جي_دبليو_تي_proxy.خطا_فك_تشفير is jwt.DecodeError
    assert جي_دبليو_تي_proxy.خطا_رمز_منتهي is jwt.ExpiredSignatureError
    assert جي_دبليو_تي_proxy.خطا_توقيع_غير_صالح is jwt.InvalidSignatureError
    assert جي_دبليو_تي_proxy.خطا_خوارزميه_غير_صالحه is jwt.InvalidAlgorithmError
    assert جي_دبليو_تي_proxy.خوارزميات is jwt.algorithms


def test_jwt_round_trip_via_arabic_aliases(جي_دبليو_تي_proxy):
    secret = "c26-test-secret-key-with-at-least-32-bytes"
    payload = {"sub": "user-123", "اسم": "ليلى"}

    token = جي_دبليو_تي_proxy.شفر(payload, secret, algorithm="HS256")
    decoded = جي_دبليو_تي_proxy.فك_التشفير(token, secret, algorithms=["HS256"])
    header = جي_دبليو_تي_proxy.اجلب_الراس_دون_تحقق(token)

    assert decoded == payload
    assert header["alg"] == "HS256"


def test_expired_signature_error_alias(جي_دبليو_تي_proxy):
    secret = "c26-test-secret-key-with-at-least-32-bytes"
    token = جي_دبليو_تي_proxy.شفر(
        {
            "sub": "expired",
            "exp": datetime.now(_dt.UTC) - timedelta(seconds=1),
        },
        secret,
        algorithm="HS256",
    )

    with pytest.raises(جي_دبليو_تي_proxy.خطا_رمز_منتهي):
        جي_دبليو_تي_proxy.فك_التشفير(token, secret, algorithms=["HS256"])


def test_jwt_toml_loads_without_error():
    from arabicpython.aliases._loader import load_mapping

    mapping = load_mapping(ALIASES_DIR / "jwt.toml")
    assert mapping.arabic_name == "جي_دبليو_تي"
    assert mapping.python_module == "jwt"
    assert mapping.entries["شفر"] == "encode"
    assert mapping.entries["فك_التشفير"] == "decode"
    assert mapping.entries["خطا_رمز_منتهي"] == "ExpiredSignatureError"
    assert len(mapping.entries) == 10


def test_jwt_toml_meta_parseable():
    path = ALIASES_DIR / "jwt.toml"
    with path.open("rb") as f:
        data = tomllib.load(f)

    assert data["meta"] == {
        "arabic_name": "جي_دبليو_تي",
        "python_module": "jwt",
        "dict_version": "ar-v1",
        "schema_version": 1,
        "maintainer": "—",
    }


def test_jwt_demo_imports(clean_import_state, capsys):
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install as install_apy

    install_apy()
    install_aliases()
    sys.path.insert(0, str(EXAMPLES_DIR))

    importlib.import_module("C26_jwt_demo")

    out, _ = capsys.readouterr()
    assert out == "JWT round-trip ok\nليلى\nexpired token handled\n"
