import importlib
import pathlib
import sys
import tomllib

import pytest

yaml = pytest.importorskip("yaml", reason="PyYAML not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"
EXAMPLES_DIR = pathlib.Path(__file__).parent.parent / "examples"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    original_path = list(sys.path)
    sys.modules.pop("يامل", None)
    sys.modules.pop("C23_yaml_demo", None)
    yield
    sys.modules.pop("يامل", None)
    sys.modules.pop("C23_yaml_demo", None)
    sys.meta_path[:] = original_meta_path
    sys.path[:] = original_path


@pytest.fixture()
def يامل_proxy():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("يامل", None, None)
    assert spec is not None, "AliasFinder did not find 'يامل'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_import_يامل_works(clean_import_state):
    from arabicpython.aliases import install

    install()
    import يامل

    assert يامل.حمل_امن is yaml.safe_load
    assert يامل.صدر_امن is yaml.safe_dump


def test_core_symbols_resolve_correctly(يامل_proxy):
    assert يامل_proxy.حمل_امن is yaml.safe_load
    assert يامل_proxy.صدر_امن is yaml.safe_dump
    assert يامل_proxy.حمل_كامل is yaml.full_load
    assert يامل_proxy.حمل_امن_الكل is yaml.safe_load_all
    assert يامل_proxy.صدر_امن_الكل is yaml.safe_dump_all
    assert يامل_proxy.صدر is yaml.dump
    assert يامل_proxy.حمل is yaml.load
    assert يامل_proxy.خطا_يامل is yaml.YAMLError
    assert يامل_proxy.محمل is yaml.Loader
    assert يامل_proxy.محمل_امن is yaml.SafeLoader
    assert يامل_proxy.مصدر is yaml.Dumper
    assert يامل_proxy.مصدر_امن is yaml.SafeDumper
    assert يامل_proxy.اضف_منشئ is yaml.add_constructor
    assert يامل_proxy.اضف_ممثل is yaml.add_representer


def test_yaml_round_trip_via_arabic_aliases(يامل_proxy):
    data = {
        "اسم": "ليلى",
        "نشط": True,
        "درجات": [95, 88, 91],
        "وسوم": {"لغة": "عربي", "صيغة": "YAML"},
    }

    yaml_text = يامل_proxy.صدر_امن(data, allow_unicode=True, sort_keys=True)

    assert isinstance(yaml_text, str)
    assert "اسم" in yaml_text
    assert يامل_proxy.حمل_امن(yaml_text) == data


def test_yaml_all_documents_round_trip(يامل_proxy):
    documents = [{"اسم": "اول"}, {"اسم": "ثاني"}]

    yaml_text = يامل_proxy.صدر_امن_الكل(documents, allow_unicode=True, sort_keys=True)

    assert list(يامل_proxy.حمل_امن_الكل(yaml_text)) == documents


def test_yaml_toml_loads_without_error():
    from arabicpython.aliases._loader import load_mapping

    mapping = load_mapping(ALIASES_DIR / "yaml.toml")
    assert mapping.arabic_name == "يامل"
    assert mapping.python_module == "yaml"
    assert mapping.entries["حمل_امن"] == "safe_load"
    assert mapping.entries["صدر_امن"] == "safe_dump"
    assert len(mapping.entries) == 14


def test_yaml_toml_meta_parseable():
    path = ALIASES_DIR / "yaml.toml"
    with path.open("rb") as f:
        data = tomllib.load(f)

    assert data["meta"] == {
        "arabic_name": "يامل",
        "python_module": "yaml",
        "dict_version": "ar-v1",
        "schema_version": 1,
    }


def test_yaml_demo_imports(clean_import_state):
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install as install_apy

    install_apy()
    install_aliases()
    sys.path.insert(0, str(EXAMPLES_DIR))

    importlib.import_module("C23_yaml_demo")
