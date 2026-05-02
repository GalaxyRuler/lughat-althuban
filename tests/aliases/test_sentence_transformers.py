import pathlib
import tomllib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

sentence_transformers = pytest.importorskip(
    "sentence_transformers", reason="sentence-transformers not installed"
)


@pytest.fixture(scope="module")
def محولات_جمل():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("محولات_جمل", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


def test_core_entries(محولات_جمل):
    from arabicpython.aliases._proxy import ClassFactory

    assert isinstance(محولات_جمل.محول_جمل, ClassFactory)
    assert محولات_جمل.تشابه_جيب_تمام is sentence_transformers.util.cos_sim


def test_toml_meta():
    data = tomllib.loads((ALIASES_DIR / "sentence_transformers.toml").read_text(encoding="utf-8"))
    assert data["meta"]["python_module"] == "sentence_transformers"
    assert data["meta"]["arabic_name"] == "محولات_جمل"
    assert len(data["entries"]) >= 15
