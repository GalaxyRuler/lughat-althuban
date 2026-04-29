from __future__ import annotations

import pickle
import types
from pathlib import Path

import pytest

from arabicpython.aliases import ClassProxy, ModuleProxy, load_mapping


def test_class_proxy_forwards_arabic_attribute_access_to_real_object() -> None:
    class Original:
        def __init__(self) -> None:
            self.value = 7

        def double(self) -> int:
            return self.value * 2

    obj = Original()
    proxy = ClassProxy(obj, {"قيمه": "value", "ضاعف": "double"})

    assert proxy.قيمه == 7
    assert proxy.ضاعف() == 14

    proxy.قيمه = 11
    assert obj.value == 11


def test_class_proxy_isinstance_uses_wrapped_object_class() -> None:
    class Original:
        pass

    obj = Original()
    proxy = ClassProxy(obj, {})

    assert isinstance(proxy, Original)


def test_class_proxy_dunders_forward_to_wrapped_object() -> None:
    values = [1, 2, 3]
    proxy = ClassProxy(values, {})

    assert len(proxy) == 3
    assert list(iter(proxy)) == values
    assert repr(proxy) == repr(values)


def test_class_proxy_unknown_arabic_attribute_falls_through_to_real_object() -> None:
    class Original:
        pass

    obj = Original()
    obj.خاص = "real"
    proxy = ClassProxy(obj, {})

    assert proxy.خاص == "real"


def test_class_proxy_preserves_comparison_and_pickling() -> None:
    values = [1, 2, 3]
    proxy = ClassProxy(values, {})

    assert proxy == values
    assert pickle.loads(pickle.dumps(proxy)) == values


def test_attributes_section_in_toml_is_parsed_correctly(tmp_path: Path) -> None:
    toml = """\
[meta]
arabic_name   = "نظام"
python_module = "sys"
dict_version  = "ar-v1"
schema_version = 1
maintainer    = "—"

[entries]
"وسائط" = "argv"

[attributes]
"طريقه" = "method"
"""
    path = tmp_path / "sys_with_attributes.toml"
    path.write_text(toml, encoding="utf-8")

    mapping = load_mapping(path)

    assert mapping.attributes == {"طريقه": "method"}


def test_attributes_section_is_optional_for_existing_tomls() -> None:
    path = Path(__file__).parent / "fixtures" / "aliases" / "valid_minimal.toml"
    mapping = load_mapping(path)

    assert mapping.attributes == {}


def test_module_proxy_wraps_proxy_class_instances_in_class_proxy() -> None:
    class Original:
        def __init__(self) -> None:
            self.value = "wrapped"

    module = types.ModuleType("demo_module")
    module.obj = Original()

    proxy = ModuleProxy(
        module,
        {"كائن": "obj"},
        attributes={"قيمه": "value"},
        arabic_name="تجربه",
        proxy_classes=frozenset({"Original"}),
    )

    result = proxy.كائن

    assert isinstance(result, ClassProxy)
    assert isinstance(result, Original)
    assert result.قيمه == "wrapped"


def test_module_proxy_infers_instance_classes_from_module_class_entries() -> None:
    class Original:
        def __init__(self) -> None:
            self.value = "inferred"

    module = types.ModuleType("demo_module")
    module.Original = Original
    module.obj = Original()

    proxy = ModuleProxy(
        module,
        {"صنف": "Original", "كائن": "obj"},
        attributes={"قيمه": "value"},
        arabic_name="تجربه",
    )

    assert proxy.صنف is Original
    assert proxy.كائن.قيمه == "inferred"


def test_flask_request_method_accessible_as_arabic_attribute() -> None:
    flask = pytest.importorskip("flask")

    from arabicpython.aliases._finder import AliasFinder

    aliases_dir = Path(__file__).parent.parent / "arabicpython" / "aliases"
    finder = AliasFinder(mappings_dir=aliases_dir)
    spec = finder.find_spec("فلاسك", None, None)
    assert spec is not None
    flask_proxy = spec.loader.create_module(spec)

    app = flask.Flask(__name__)
    with app.test_request_context("/hello?name=codex", method="GET"):
        طلب = flask_proxy.طلب

        assert isinstance(طلب, ClassProxy)
        assert طلب.طريقه == "GET"
        assert طلب.وسيطات_الطلب["name"] == "codex"
