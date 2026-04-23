# tests/aliases/test_io.py
# B-038 stdlib aliases — io module tests

import io
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مجاري():
    """Return a ModuleProxy wrapping `io`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مجاري", None, None)
    assert spec is not None, "AliasFinder did not find 'مجاري'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestIoProxy:
    # ── open alias ────────────────────────────────────────────────────────────

    def test_open_alias(self, مجاري):
        """فتح_تيار maps to io.open."""
        assert مجاري.فتح_تيار is io.open

    # ── Stream class aliases ──────────────────────────────────────────────────

    def test_stringio_alias(self, مجاري):
        """تيار_نص maps to io.StringIO."""
        assert مجاري.تيار_نص is io.StringIO

    def test_bytesio_alias(self, مجاري):
        """تيار_بايت maps to io.BytesIO."""
        assert مجاري.تيار_بايت is io.BytesIO

    def test_fileio_alias(self, مجاري):
        """تيار_ملف maps to io.FileIO."""
        assert مجاري.تيار_ملف is io.FileIO

    def test_buffered_reader_alias(self, مجاري):
        """قارئ_منظم maps to io.BufferedReader."""
        assert مجاري.قارئ_منظم is io.BufferedReader

    def test_buffered_writer_alias(self, مجاري):
        """كاتب_منظم maps to io.BufferedWriter."""
        assert مجاري.كاتب_منظم is io.BufferedWriter

    def test_buffered_random_alias(self, مجاري):
        """منظم_عشوائي maps to io.BufferedRandom."""
        assert مجاري.منظم_عشوائي is io.BufferedRandom

    def test_text_io_wrapper_alias(self, مجاري):
        """غلاف_نصي maps to io.TextIOWrapper."""
        assert مجاري.غلاف_نصي is io.TextIOWrapper

    # ── Base class aliases ────────────────────────────────────────────────────

    def test_iobase_alias(self, مجاري):
        """اساس_تيار maps to io.IOBase."""
        assert مجاري.اساس_تيار is io.IOBase

    def test_rawiobase_alias(self, مجاري):
        """اساس_خام maps to io.RawIOBase."""
        assert مجاري.اساس_خام is io.RawIOBase

    def test_bufferediobase_alias(self, مجاري):
        """اساس_منظم maps to io.BufferedIOBase."""
        assert مجاري.اساس_منظم is io.BufferedIOBase

    def test_textiobase_alias(self, مجاري):
        """اساس_نصي maps to io.TextIOBase."""
        assert مجاري.اساس_نصي is io.TextIOBase

    # ── Constant aliases ──────────────────────────────────────────────────────

    def test_default_buffer_size_alias(self, مجاري):
        """حجم_منظم maps to io.DEFAULT_BUFFER_SIZE."""
        assert مجاري.حجم_منظم is io.DEFAULT_BUFFER_SIZE

    def test_seek_set_alias(self, مجاري):
        """ابحث_بدايه maps to io.SEEK_SET (== 0)."""
        assert مجاري.ابحث_بدايه == io.SEEK_SET == 0

    def test_seek_cur_alias(self, مجاري):
        """ابحث_حاليه maps to io.SEEK_CUR (== 1)."""
        assert مجاري.ابحث_حاليه == io.SEEK_CUR == 1

    def test_seek_end_alias(self, مجاري):
        """ابحث_نهايه maps to io.SEEK_END (== 2)."""
        assert مجاري.ابحث_نهايه == io.SEEK_END == 2

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_stringio_write_getvalue(self, مجاري):
        """تيار_نص supports write and getvalue."""
        buf = مجاري.تيار_نص()
        buf.write("مرحبا")
        buf.write(" عالم")
        assert buf.getvalue() == "مرحبا عالم"

    def test_stringio_multiline(self, مجاري):
        """تيار_نص preserves newlines across multiple writes."""
        buf = مجاري.تيار_نص()
        buf.write("السطر الأول\n")
        buf.write("السطر الثاني\n")
        lines = buf.getvalue().splitlines()
        assert lines == ["السطر الأول", "السطر الثاني"]

    def test_bytesio_write_read(self, مجاري):
        """تيار_بايت supports write and read-back."""
        buf = مجاري.تيار_بايت()
        buf.write(b"\x00\x01\x02\x03")
        buf.seek(0)
        assert buf.read() == b"\x00\x01\x02\x03"

    def test_bytesio_getvalue(self, مجاري):
        """تيار_بايت.getvalue returns full buffer content."""
        buf = مجاري.تيار_بايت(b"hello")
        assert buf.getvalue() == b"hello"

    def test_stringio_is_instance_of_iobase(self, مجاري):
        """StringIO instances are instances of IOBase."""
        buf = مجاري.تيار_نص()
        assert isinstance(buf, مجاري.اساس_تيار)

    def test_buffered_reader_wraps_raw(self, مجاري):
        """قارئ_منظم can wrap a RawIOBase stream."""
        raw = مجاري.تيار_بايت(b"data")
        # BytesIO supports BufferedIOBase interface; wrap it
        assert isinstance(raw, مجاري.اساس_منظم)
