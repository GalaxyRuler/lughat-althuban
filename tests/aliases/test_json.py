# tests/aliases/test_json.py
# B-033 stdlib aliases — json module tests

import json
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def جيسون():
    """Return a ModuleProxy wrapping `json`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("جيسون", None, None)
    assert spec is not None, "AliasFinder did not find 'جيسون'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestJsonProxy:
    def test_dumps_alias(self, جيسون):
        """نص maps to json.dumps."""
        assert جيسون.نص is json.dumps

    def test_loads_alias(self, جيسون):
        """من_نص maps to json.loads."""
        assert جيسون.من_نص is json.loads

    def test_dump_alias(self, جيسون):
        """حفظ maps to json.dump."""
        assert جيسون.حفظ is json.dump

    def test_load_alias(self, جيسون):
        """تحميل maps to json.load."""
        assert جيسون.تحميل is json.load

    def test_json_encoder_alias(self, جيسون):
        """مرمز maps to json.JSONEncoder."""
        assert جيسون.مرمز is json.JSONEncoder

    def test_json_decoder_alias(self, جيسون):
        """محلل maps to json.JSONDecoder."""
        assert جيسون.محلل is json.JSONDecoder

    def test_json_decode_error_alias(self, جيسون):
        """خطا_تفكيك maps to json.JSONDecodeError."""
        assert جيسون.خطا_تفكيك is json.JSONDecodeError

    def test_arabic_roundtrip_dumps_loads(self, جيسون):
        """Arabic dict survives JSON encode → decode round-trip."""
        data = {"اسم": "محمد", "عمر": 30, "مدينة": "الرياض"}
        encoded = جيسون.نص(data, ensure_ascii=False)
        decoded = جيسون.من_نص(encoded)
        assert decoded == data
        assert "محمد" in encoded

    def test_dumps_with_indent(self, جيسون):
        """نص(data, indent=2) produces formatted JSON."""
        data = {"key": "value"}
        result = جيسون.نص(data, indent=2)
        assert "\n" in result

    def test_dump_load_file_roundtrip(self, جيسون, tmp_path):
        """حفظ writes JSON to a file; تحميل reads it back."""
        data = {"نص": "مرحبا", "رقم": 42}
        file_path = tmp_path / "test.json"
        with open(file_path, "w", encoding="utf-8") as f:
            جيسون.حفظ(data, f, ensure_ascii=False)
        with open(file_path, encoding="utf-8") as f:
            loaded = جيسون.تحميل(f)
        assert loaded == data

    def test_decode_error_raised_on_invalid_json(self, جيسون):
        """خطا_تفكيك is raised when parsing invalid JSON."""
        with pytest.raises(json.JSONDecodeError):
            جيسون.من_نص("{not valid json}")

    def test_encoder_encode_unbound(self, جيسون):
        """رمز is JSONEncoder.encode (unbound); encoding a list works."""
        encoder = json.JSONEncoder()
        result = جيسون.رمز(encoder, [1, 2, 3])
        assert result == "[1, 2, 3]"

    def test_decoder_decode_unbound(self, جيسون):
        """فكك is JSONDecoder.decode (unbound); decoding a string works."""
        decoder = json.JSONDecoder()
        result = جيسون.فكك(decoder, '{"a": 1}')
        assert result == {"a": 1}
