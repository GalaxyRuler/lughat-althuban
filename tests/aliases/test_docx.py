# tests/aliases/test_docx.py
# C-021: Arabic aliases for python-docx

import pathlib

import pytest

docx = pytest.importorskip("docx", reason="python-docx not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مستندات_وورد():
    """Return a ModuleProxy wrapping `docx`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مستندات_وورد", None, None)
    assert spec is not None, "AliasFinder did not find 'مستندات_وورد'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestDocxCore:
    def test_document_classes(self, مستندات_وورد):
        import docx.document
        import docx.table
        import docx.text.paragraph
        import docx.text.run

        assert مستندات_وورد.مستند is docx.Document
        assert مستندات_وورد.فئه_مستند is docx.document.Document
        assert مستندات_وورد.فقره is docx.text.paragraph.Paragraph
        assert مستندات_وورد.تشغيل is docx.text.run.Run
        assert مستندات_وورد.جدول is docx.table.Table

    def test_shared_helpers_and_enums(self, مستندات_وورد):
        import docx.enum.text
        import docx.shared

        assert مستندات_وورد.محاذاه_فقره is docx.enum.text.WD_ALIGN_PARAGRAPH
        assert مستندات_وورد.فاصل is docx.enum.text.WD_BREAK
        assert مستندات_وورد.بوصات is docx.shared.Inches
        assert مستندات_وورد.لون_rgb is docx.shared.RGBColor


class TestDocxFunctional:
    def test_document_attributes_work_with_class_proxy(self, مستندات_وورد, tmp_path):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "docx.toml")
        document = مستندات_وورد.مستند()
        document_proxy = ClassProxy(document, mapping.attributes)

        paragraph = document_proxy.اضف_فقره("مرحبا")
        paragraph_proxy = ClassProxy(paragraph, mapping.attributes)
        run = paragraph_proxy.اضف_تشغيل(" من وورد")
        run_proxy = ClassProxy(run, mapping.attributes)
        run_proxy.غامق = True

        table = document_proxy.اضف_جدول(rows=1, cols=2)
        table_proxy = ClassProxy(table, mapping.attributes)

        output = tmp_path / "demo.docx"
        document_proxy.احفظ(output)

        assert paragraph.text == "مرحبا من وورد"
        assert run.bold is True
        assert len(table_proxy.صفوف) == 1
        assert output.exists()


class TestDocxTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "docx.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "docx"
        assert data["meta"]["arabic_name"] == "مستندات_وورد"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "docx.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 15
