import pathlib
import tomllib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

transformers = pytest.importorskip("transformers", reason="transformers not installed")


@pytest.fixture(scope="module")
def محولات():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("محولات", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


def test_core_entries(محولات):
    assert محولات.نموذج_تلقائي is transformers.AutoModel
    assert محولات.مرمز_تلقائي is transformers.AutoTokenizer
    assert محولات.خط_انابيب is transformers.pipeline


def test_toml_meta():
    data = tomllib.loads((ALIASES_DIR / "transformers.toml").read_text(encoding="utf-8"))
    assert data["meta"]["python_module"] == "transformers"
    assert data["meta"]["arabic_name"] == "محولات"
    assert len(data["entries"]) >= 20
