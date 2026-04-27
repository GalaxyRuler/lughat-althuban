# tests/aliases/test_shutil.py
# B-039 stdlib aliases — shutil module tests

import pathlib
import shutil
import tempfile

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def ادوات_ملفات():
    """Return a ModuleProxy wrapping `shutil`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ادوات_ملفات", None, None)
    assert spec is not None, "AliasFinder did not find 'ادوات_ملفات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestShutilProxy:
    # ── Copy aliases ──────────────────────────────────────────────────────────

    def test_copy_alias(self, ادوات_ملفات):
        """انسخ maps to shutil.copy."""
        assert ادوات_ملفات.انسخ is shutil.copy

    def test_copy2_alias(self, ادوات_ملفات):
        """انسخ_مع_بيانات maps to shutil.copy2."""
        assert ادوات_ملفات.انسخ_مع_بيانات is shutil.copy2

    def test_copyfile_alias(self, ادوات_ملفات):
        """انسخ_ملف maps to shutil.copyfile."""
        assert ادوات_ملفات.انسخ_ملف is shutil.copyfile

    def test_copyfileobj_alias(self, ادوات_ملفات):
        """انسخ_كائن_ملف maps to shutil.copyfileobj."""
        assert ادوات_ملفات.انسخ_كائن_ملف is shutil.copyfileobj

    def test_copymode_alias(self, ادوات_ملفات):
        """انسخ_صلاحيات maps to shutil.copymode."""
        assert ادوات_ملفات.انسخ_صلاحيات is shutil.copymode

    def test_copystat_alias(self, ادوات_ملفات):
        """انسخ_احصائيات maps to shutil.copystat."""
        assert ادوات_ملفات.انسخ_احصائيات is shutil.copystat

    def test_copytree_alias(self, ادوات_ملفات):
        """انسخ_شجره maps to shutil.copytree."""
        assert ادوات_ملفات.انسخ_شجره is shutil.copytree

    # ── Move / delete aliases ──────────────────────────────────────────────────

    def test_move_alias(self, ادوات_ملفات):
        """انقل maps to shutil.move."""
        assert ادوات_ملفات.انقل is shutil.move

    def test_rmtree_alias(self, ادوات_ملفات):
        """احذف_شجره maps to shutil.rmtree."""
        assert ادوات_ملفات.احذف_شجره is shutil.rmtree

    # ── Archive aliases ────────────────────────────────────────────────────────

    def test_make_archive_alias(self, ادوات_ملفات):
        """اصنع_ارشيف maps to shutil.make_archive."""
        assert ادوات_ملفات.اصنع_ارشيف is shutil.make_archive

    def test_unpack_archive_alias(self, ادوات_ملفات):
        """فك_ارشيف maps to shutil.unpack_archive."""
        assert ادوات_ملفات.فك_ارشيف is shutil.unpack_archive

    def test_get_archive_formats_alias(self, ادوات_ملفات):
        """صيغ_الارشيف maps to shutil.get_archive_formats."""
        assert ادوات_ملفات.صيغ_الارشيف is shutil.get_archive_formats

    def test_get_unpack_formats_alias(self, ادوات_ملفات):
        """صيغ_فك_الارشيف maps to shutil.get_unpack_formats."""
        assert ادوات_ملفات.صيغ_فك_الارشيف is shutil.get_unpack_formats

    # ── Introspection aliases ─────────────────────────────────────────────────

    def test_disk_usage_alias(self, ادوات_ملفات):
        """استخدام_القرص maps to shutil.disk_usage."""
        assert ادوات_ملفات.استخدام_القرص is shutil.disk_usage

    def test_get_terminal_size_alias(self, ادوات_ملفات):
        """حجم_نافذه_طرفيه maps to shutil.get_terminal_size."""
        assert ادوات_ملفات.حجم_نافذه_طرفيه is shutil.get_terminal_size

    def test_which_alias(self, ادوات_ملفات):
        """اين maps to shutil.which."""
        assert ادوات_ملفات.اين is shutil.which

    def test_ignore_patterns_alias(self, ادوات_ملفات):
        """انماط_تجاهل maps to shutil.ignore_patterns."""
        assert ادوات_ملفات.انماط_تجاهل is shutil.ignore_patterns

    def test_chown_alias(self, ادوات_ملفات):
        """غير_المالك maps to shutil.chown."""
        assert ادوات_ملفات.غير_المالك is shutil.chown

    # ── Exception type aliases ─────────────────────────────────────────────────

    def test_error_alias(self, ادوات_ملفات):
        """خطا_ملفات maps to shutil.Error."""
        assert ادوات_ملفات.خطا_ملفات is shutil.Error

    def test_same_file_error_alias(self, ادوات_ملفات):
        """خطا_نفس_الملف maps to shutil.SameFileError."""
        assert ادوات_ملفات.خطا_نفس_الملف is shutil.SameFileError

    def test_special_file_error_alias(self, ادوات_ملفات):
        """خطا_ملف_خاص maps to shutil.SpecialFileError."""
        assert ادوات_ملفات.خطا_ملف_خاص is shutil.SpecialFileError

    def test_read_error_alias(self, ادوات_ملفات):
        """خطا_قراءه_ارشيف maps to shutil.ReadError."""
        assert ادوات_ملفات.خطا_قراءه_ارشيف is shutil.ReadError

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_copy_creates_file(self, ادوات_ملفات):
        """انسخ copies a file to a new location."""
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp) / "src.txt"
            dst = pathlib.Path(tmp) / "dst.txt"
            src.write_text("test content", encoding="utf-8")
            ادوات_ملفات.انسخ(src, dst)
            assert dst.exists()
            assert dst.read_text(encoding="utf-8") == "test content"

    def test_move_relocates_file(self, ادوات_ملفات):
        """انقل moves a file to a new location."""
        with tempfile.TemporaryDirectory() as tmp:
            src = pathlib.Path(tmp) / "original.txt"
            dst = pathlib.Path(tmp) / "moved.txt"
            src.write_text("data", encoding="utf-8")
            ادوات_ملفات.انقل(str(src), str(dst))
            assert not src.exists()
            assert dst.read_text(encoding="utf-8") == "data"

    def test_copytree_copies_tree(self, ادوات_ملفات):
        """انسخ_شجره copies a directory tree."""
        with tempfile.TemporaryDirectory() as tmp:
            src_dir = pathlib.Path(tmp) / "src"
            src_dir.mkdir()
            (src_dir / "file.txt").write_text("hello")
            dst_dir = pathlib.Path(tmp) / "dst"
            ادوات_ملفات.انسخ_شجره(src_dir, dst_dir)
            assert (dst_dir / "file.txt").read_text() == "hello"

    def test_rmtree_removes_tree(self, ادوات_ملفات):
        """احذف_شجره removes a directory tree."""
        with tempfile.TemporaryDirectory() as tmp:
            target = pathlib.Path(tmp) / "to_delete"
            target.mkdir()
            (target / "f.txt").write_text("x")
            ادوات_ملفات.احذف_شجره(target)
            assert not target.exists()

    def test_disk_usage_returns_named_tuple(self, ادوات_ملفات):
        """استخدام_القرص returns a named tuple with total/used/free."""
        import pathlib

        usage = ادوات_ملفات.استخدام_القرص(pathlib.Path("."))
        assert hasattr(usage, "total")
        assert hasattr(usage, "used")
        assert hasattr(usage, "free")
        assert usage.total > 0

    def test_which_finds_python(self, ادوات_ملفات):
        """اين locates an executable on PATH."""
        import sys

        result = ادوات_ملفات.اين("python") or ادوات_ملفات.اين("python3")
        # At least one of the two should be found in any Python environment.
        assert result is not None or sys.platform == "win32"

    def test_get_archive_formats_returns_list(self, ادوات_ملفات):
        """صيغ_الارشيف returns a list of (name, description) tuples."""
        formats = ادوات_ملفات.صيغ_الارشيف()
        assert isinstance(formats, list)
        assert any(name == "zip" for name, _ in formats)

    def test_same_file_error_is_os_error(self, ادوات_ملفات):
        """خطا_نفس_الملف is a subclass of OSError."""
        assert issubclass(ادوات_ملفات.خطا_نفس_الملف, OSError)

    def test_copyfile_same_source_raises(self, ادوات_ملفات):
        """انسخ_ملف raises خطا_نفس_الملف when src == dst."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            p = pathlib.Path(f.name)
        try:
            with pytest.raises(ادوات_ملفات.خطا_نفس_الملف):
                ادوات_ملفات.انسخ_ملف(p, p)
        finally:
            p.unlink(missing_ok=True)
