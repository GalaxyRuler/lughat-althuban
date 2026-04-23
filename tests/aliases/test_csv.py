# tests/aliases/test_csv.py
# B-033 stdlib aliases — csv module tests
#
# Normalization notes:
#   اقتباس_ادني  ← QUOTE_MINIMAL  (final ى→ي in "أدنى")
#   لهجه         ← Dialect        (final ة→ه)
#   اكتب_سطر     ← DictWriter.writerow

import csv
import io
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def ملفات_csv():
    """Return a ModuleProxy wrapping `csv`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ملفات_csv", None, None)
    assert spec is not None, "AliasFinder did not find 'ملفات_csv'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestCsvProxy:
    def test_reader_alias(self, ملفات_csv):
        """قارئ maps to csv.reader."""
        assert ملفات_csv.قارئ is csv.reader

    def test_writer_alias(self, ملفات_csv):
        """كاتب maps to csv.writer."""
        assert ملفات_csv.كاتب is csv.writer

    def test_dict_reader_alias(self, ملفات_csv):
        """قارئ_قاموس maps to csv.DictReader."""
        assert ملفات_csv.قارئ_قاموس is csv.DictReader

    def test_dict_writer_alias(self, ملفات_csv):
        """كاتب_قاموس maps to csv.DictWriter."""
        assert ملفات_csv.كاتب_قاموس is csv.DictWriter

    def test_quote_constants(self, ملفات_csv):
        """QUOTE_* constants have correct values."""
        assert ملفات_csv.اقتباس_ادني == csv.QUOTE_MINIMAL
        assert ملفات_csv.اقتباس_الكل == csv.QUOTE_ALL
        assert ملفات_csv.اقتباس_غير_رقمي == csv.QUOTE_NONNUMERIC
        assert ملفات_csv.بلا_اقتباس == csv.QUOTE_NONE

    def test_csv_reader_reads_arabic(self, ملفات_csv):
        """قارئ reads CSV with Arabic content correctly."""
        data = "اسم,عمر\nمحمد,30\nفاطمة,25\n"
        rows = list(ملفات_csv.قارئ(io.StringIO(data)))
        assert rows[0] == ["اسم", "عمر"]
        assert rows[1] == ["محمد", "30"]

    def test_csv_writer_writes_arabic(self, ملفات_csv):
        """كاتب writes Arabic values to CSV correctly."""
        output = io.StringIO()
        w = ملفات_csv.كاتب(output)
        w.writerow(["اسم", "مدينة"])
        w.writerow(["علي", "الرياض"])
        content = output.getvalue()
        assert "اسم" in content
        assert "الرياض" in content

    def test_csv_writer_handles_commas_in_values(self, ملفات_csv):
        """كاتب quotes values that contain the delimiter."""
        output = io.StringIO()
        w = ملفات_csv.كاتب(output)
        w.writerow(["value, with comma", "normal"])
        content = output.getvalue()
        assert '"value, with comma"' in content

    def test_dict_reader_maps_columns(self, ملفات_csv):
        """قارئ_قاموس produces dicts keyed by header row."""
        data = "name,city\nAli,Riyadh\nSara,Jeddah\n"
        rows = list(ملفات_csv.قارئ_قاموس(io.StringIO(data)))
        assert rows[0]["name"] == "Ali"
        assert rows[1]["city"] == "Jeddah"

    def test_dict_writer_writerow_unbound(self, ملفات_csv):
        """اكتب_سطر is DictWriter.writerow (unbound); writes a dict row."""
        output = io.StringIO()
        dw = csv.DictWriter(output, fieldnames=["الاسم", "المدينة"])
        dw.writeheader()
        ملفات_csv.اكتب_سطر(dw, {"الاسم": "سلمى", "المدينة": "مكة"})
        content = output.getvalue()
        assert "سلمى" in content
        assert "مكة" in content

    def test_dict_writer_writeheader_unbound(self, ملفات_csv):
        """اكتب_راس is DictWriter.writeheader (unbound); writes the header."""
        output = io.StringIO()
        dw = csv.DictWriter(output, fieldnames=["ح1", "ح2"])
        ملفات_csv.اكتب_راس(dw)
        content = output.getvalue()
        assert "ح1" in content
        assert "ح2" in content

    def test_dialect_alias(self, ملفات_csv):
        """لهجه maps to csv.Dialect."""
        assert ملفات_csv.لهجه is csv.Dialect

    def test_register_dialect_alias(self, ملفات_csv):
        """سجل_لهجه maps to csv.register_dialect."""
        assert ملفات_csv.سجل_لهجه is csv.register_dialect
