import pathlib
import tomllib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"

langchain_core = pytest.importorskip("langchain_core", reason="langchain-core not installed")


@pytest.fixture(scope="module")
def سلسلة_لغه():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("سلسلة_لغه", None, None)
    assert spec is not None
    return spec.loader.create_module(spec)


def test_core_entries(سلسلة_لغه):
    from langchain_core.messages import HumanMessage
    from langchain_core.prompts import PromptTemplate

    assert سلسلة_لغه.رساله_انسان is HumanMessage
    assert سلسلة_لغه.قالب_موجه is PromptTemplate


def test_toml_meta():
    data = tomllib.loads((ALIASES_DIR / "langchain_core.toml").read_text(encoding="utf-8"))
    assert data["meta"]["python_module"] == "langchain_core"
    assert data["meta"]["arabic_name"] == "سلسلة_لغه"
    assert len(data["entries"]) >= 15
