import pathlib
import tomllib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

openai = pytest.importorskip("openai", reason="openai not installed")


@pytest.fixture(scope="module")
def ذكاء_مفتوح():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ذكاء_مفتوح", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


def test_core_entries(ذكاء_مفتوح):
    from arabicpython.aliases._proxy import ClassFactory

    assert isinstance(ذكاء_مفتوح.عميل, ClassFactory)
    assert ذكاء_مفتوح.خطا_مفتاح is openai.AuthenticationError


def test_toml_meta():
    data = tomllib.loads((ALIASES_DIR / "openai.toml").read_text(encoding="utf-8"))
    assert data["meta"]["python_module"] == "openai"
    assert data["meta"]["arabic_name"] == "ذكاء_مفتوح"
    assert len(data["entries"]) >= 20
