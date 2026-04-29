import importlib
import os
import pathlib
import sys
import tomllib

import pytest

dotenv = pytest.importorskip("dotenv", reason="python-dotenv not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    original_path = list(sys.path)
    sys.modules.pop("دوت_إنف", None)
    sys.modules.pop("دوت_انف", None)
    yield
    sys.modules.pop("دوت_إنف", None)
    sys.modules.pop("دوت_انف", None)
    sys.meta_path[:] = original_meta_path
    sys.path[:] = original_path


@pytest.fixture()
def دوت_إنف_proxy():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("دوت_إنف", None, None)
    assert spec is not None, "AliasFinder did not find 'دوت_إنف'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_import_دوت_إنف_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    دوت_إنف = importlib.import_module("دوت_إنف")

    assert دوت_إنف.حمل_البيئه is dotenv.load_dotenv


def test_translated_normalized_module_name_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    دوت_انف = importlib.import_module("دوت_انف")

    assert دوت_انف.قيم_البيئه is dotenv.dotenv_values


def test_dotenv_aliases_map_to_python_dotenv(دوت_إنف_proxy):
    assert دوت_إنف_proxy.حمل_البيئه is dotenv.load_dotenv
    assert دوت_إنف_proxy.قيم_البيئه is dotenv.dotenv_values
    assert دوت_إنف_proxy.اجلب_مفتاح is dotenv.get_key
    assert دوت_إنف_proxy.عين_مفتاح is dotenv.set_key
    assert دوت_إنف_proxy.احذف_مفتاح is dotenv.unset_key
    assert دوت_إنف_proxy.ابحث_عن_بيئه is dotenv.find_dotenv


def test_dotenv_toml_loads_without_error():
    from arabicpython.aliases._loader import load_mapping

    path = ALIASES_DIR / "dotenv.toml"
    mapping = load_mapping(path)
    assert mapping.arabic_name == "دوت_إنف"
    assert mapping.python_module == "dotenv"
    assert mapping.entries["حمل_البيئه"] == "load_dotenv"
    assert mapping.entries["قيم_البيئه"] == "dotenv_values"
    assert mapping.entries["عين_مفتاح"] == "set_key"
    assert len(mapping.entries) == 6


def test_dotenv_toml_meta_parseable():
    path = ALIASES_DIR / "dotenv.toml"
    with path.open("rb") as f:
        data = tomllib.load(f)

    assert data["meta"] == {
        "arabic_name": "دوت_إنف",
        "python_module": "dotenv",
        "dict_version": "ar-v1",
        "schema_version": 1,
        "maintainer": "—",
    }


def test_dotenv_load_and_values_smoke(دوت_إنف_proxy, tmp_path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text("C22_GREETING=مرحبا\n", encoding="utf-8")
    monkeypatch.delenv("C22_GREETING", raising=False)

    assert دوت_إنف_proxy.حمل_البيئه(env_path, override=True) is True
    assert os.environ["C22_GREETING"] == "مرحبا"

    values = دوت_إنف_proxy.قيم_البيئه(env_path)
    assert values["C22_GREETING"] == "مرحبا"
    assert دوت_إنف_proxy.اجلب_مفتاح(env_path, "C22_GREETING") == "مرحبا"


def test_dotenv_key_helpers_and_find(دوت_إنف_proxy, tmp_path, monkeypatch):
    env_path = tmp_path / ".env"
    env_path.write_text("C22_GREETING=مرحبا\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    found = دوت_إنف_proxy.ابحث_عن_بيئه(usecwd=True)
    assert pathlib.Path(found) == env_path

    دوت_إنف_proxy.عين_مفتاح(env_path, "C22_OTHER", "42")
    assert دوت_إنف_proxy.اجلب_مفتاح(env_path, "C22_OTHER") == "42"

    دوت_إنف_proxy.احذف_مفتاح(env_path, "C22_OTHER")
    assert دوت_إنف_proxy.اجلب_مفتاح(env_path, "C22_OTHER") is None


def test_dotenv_demo_runs(clean_import_state, capsys):
    from arabicpython.cli import main

    path = EXAMPLES_DIR / "C22_dotenv_demo.apy"
    assert main([str(path)]) == 0
    out, _ = capsys.readouterr()
    assert out == (
        "os.environ: مرحبا من dotenv\n"
        "dotenv_values: مرحبا من dotenv\n"
    )
