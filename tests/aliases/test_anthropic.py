import pathlib
import tomllib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

anthropic = pytest.importorskip("anthropic", reason="anthropic not installed")


@pytest.fixture(scope="module")
def كلود_عربي():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("كلود_عربي", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


def test_core_entries(كلود_عربي):
    from arabicpython.aliases._proxy import ClassFactory

    assert isinstance(كلود_عربي.عميل, ClassFactory)
    assert كلود_عربي.خطا_مهله_ai is anthropic.APITimeoutError


def test_toml_meta():
    data = tomllib.loads((ALIASES_DIR / "anthropic.toml").read_text(encoding="utf-8"))
    assert data["meta"]["python_module"] == "anthropic"
    assert data["meta"]["arabic_name"] == "كلود_عربي"
    assert len(data["entries"]) >= 20
