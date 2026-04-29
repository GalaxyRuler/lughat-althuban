import importlib
import pathlib
import sys
import tomllib

import pytest

click = pytest.importorskip("click", reason="click not installed")
from click.testing import CliRunner  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    original_path = list(sys.path)
    sys.modules.pop("كليك", None)
    sys.modules.pop("C14_click_demo", None)
    yield
    sys.modules.pop("كليك", None)
    sys.modules.pop("C14_click_demo", None)
    sys.meta_path[:] = original_meta_path
    sys.path[:] = original_path


@pytest.fixture()
def كليك_proxy():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("كليك", None, None)
    assert spec is not None, "AliasFinder did not find 'كليك'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_import_كليك_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    import كليك

    assert كليك.امر is click.command


def test_كليك_امر_is_click_command(كليك_proxy):
    assert كليك_proxy.امر is click.command
    assert كليك_proxy.نسق is click.style
    assert كليك_proxy.format is click.style


def test_click_toml_loads_without_error():
    from arabicpython.aliases._loader import load_mapping

    path = ALIASES_DIR / "click.toml"
    mapping = load_mapping(path)
    assert mapping.arabic_name == "كليك"
    assert mapping.python_module == "click"
    assert mapping.entries["امر"] == "command"
    assert len(mapping.entries) >= 45


def test_click_toml_meta_parseable():
    path = ALIASES_DIR / "click.toml"
    with path.open("rb") as f:
        data = tomllib.load(f)

    assert data["meta"] == {
        "arabic_name": "كليك",
        "python_module": "click",
        "dict_version": "ar-v1",
        "schema_version": 1,
    }


def test_click_demo_cli_runner(clean_import_state):
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install as install_apy

    install_apy()
    install_aliases()
    sys.path.insert(0, str(EXAMPLES_DIR))
    demo = importlib.import_module("C14_click_demo")

    runner = CliRunner()

    greet = runner.invoke(demo.تطبيق, ["رحب", "--مرات", "2"], input="ليلى\n")
    assert greet.exit_code == 0, greet.output
    assert "الاسم" in greet.output
    assert greet.output.count("مرحبا ليلى") == 2

    total = runner.invoke(demo.تطبيق, ["اجمع", "2", "3", "5"])
    assert total.exit_code == 0, total.output
    assert "المجموع: 10" in total.output
