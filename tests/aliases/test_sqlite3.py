# tests/aliases/test_sqlite3.py
# B-033 stdlib aliases — sqlite3 module tests
#
# Uses ":memory:" database throughout — no file I/O, no cleanup needed.
# Unbound methods are called with the connection/cursor instance as first arg:
#   قاعدة_بيانات.نفذ(conn, "SQL") ≡ conn.execute("SQL")

import pathlib
import sqlite3

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def قاعدة_بيانات():
    """Return a ModuleProxy wrapping `sqlite3`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("قاعدة_بيانات", None, None)
    assert spec is not None, "AliasFinder did not find 'قاعدة_بيانات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


@pytest.fixture()
def اتصال(قاعدة_بيانات):
    """Open an in-memory SQLite connection; close it after the test."""
    conn = قاعدة_بيانات.اتصل(":memory:")
    yield conn
    conn.close()


class TestSqlite3Proxy:
    # ── Class and function aliases ─────────────────────────────────────────────

    def test_connect_alias(self, قاعدة_بيانات):
        """اتصل maps to sqlite3.connect."""
        assert قاعدة_بيانات.اتصل is sqlite3.connect

    def test_connection_class_alias(self, قاعدة_بيانات):
        """وصله maps to sqlite3.Connection."""
        assert قاعدة_بيانات.وصله is sqlite3.Connection

    def test_cursor_class_alias(self, قاعدة_بيانات):
        """مؤشر maps to sqlite3.Cursor."""
        assert قاعدة_بيانات.مؤشر is sqlite3.Cursor

    def test_row_class_alias(self, قاعدة_بيانات):
        """صف maps to sqlite3.Row."""
        assert قاعدة_بيانات.صف is sqlite3.Row

    def test_database_error_alias(self, قاعدة_بيانات):
        """خطا_قاعدة_بيانات maps to sqlite3.DatabaseError."""
        assert قاعدة_بيانات.خطا_قاعدة_بيانات is sqlite3.DatabaseError

    def test_operational_error_alias(self, قاعدة_بيانات):
        """خطا_تشغيل maps to sqlite3.OperationalError."""
        assert قاعدة_بيانات.خطا_تشغيل is sqlite3.OperationalError

    # ── Connect and basic execute ─────────────────────────────────────────────

    def test_connect_returns_connection(self, قاعدة_بيانات):
        """اتصل(":memory:") returns a sqlite3.Connection instance."""
        conn = قاعدة_بيانات.اتصل(":memory:")
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_execute_creates_table(self, قاعدة_بيانات, اتصال):
        """نفذ (Connection.execute) runs DDL without raising."""
        قاعدة_بيانات.نفذ(اتصال, "CREATE TABLE طلاب (id INTEGER, اسم TEXT)")

    # ── Commit / rollback ─────────────────────────────────────────────────────

    def test_commit_persists_data(self, قاعدة_بيانات):
        """ثبت commits inserted rows; a new cursor can see them."""
        conn = قاعدة_بيانات.اتصل(":memory:")
        قاعدة_بيانات.نفذ(conn, "CREATE TABLE items (val TEXT)")
        قاعدة_بيانات.نفذ(conn, "INSERT INTO items VALUES ('مرحبا')")
        قاعدة_بيانات.ثبت(conn)
        cur = conn.execute("SELECT * FROM items")
        rows = cur.fetchall()
        assert len(rows) == 1
        assert rows[0][0] == "مرحبا"
        conn.close()

    def test_rollback_discards_data(self, قاعدة_بيانات):
        """تراجع discards uncommitted rows."""
        conn = قاعدة_بيانات.اتصل(":memory:", isolation_level="DEFERRED")
        قاعدة_بيانات.نفذ(conn, "CREATE TABLE temp_tbl (val TEXT)")
        قاعدة_بيانات.ثبت(conn)  # commit table creation
        قاعدة_بيانات.نفذ(conn, "INSERT INTO temp_tbl VALUES ('test')")
        قاعدة_بيانات.تراجع(conn)
        cur = conn.execute("SELECT * FROM temp_tbl")
        assert cur.fetchall() == []
        conn.close()

    # ── Cursor-level fetch methods ────────────────────────────────────────────

    def test_fetchall_unbound(self, قاعدة_بيانات, اتصال):
        """اجلب_الكل is Cursor.fetchall (unbound); returns all rows."""
        قاعدة_بيانات.نفذ(اتصال, "CREATE TABLE nums (n INTEGER)")
        قاعدة_بيانات.نفذ_عديد(اتصال, "INSERT INTO nums VALUES (?)", [(i,) for i in range(5)])
        cur = اتصال.execute("SELECT n FROM nums ORDER BY n")
        rows = قاعدة_بيانات.اجلب_الكل(cur)
        assert [r[0] for r in rows] == [0, 1, 2, 3, 4]

    def test_fetchone_unbound(self, قاعدة_بيانات, اتصال):
        """اجلب_واحد is Cursor.fetchone (unbound); returns the first row."""
        قاعدة_بيانات.نفذ(اتصال, "CREATE TABLE vals (v TEXT)")
        قاعدة_بيانات.نفذ(اتصال, "INSERT INTO vals VALUES ('first')")
        قاعدة_بيانات.نفذ(اتصال, "INSERT INTO vals VALUES ('second')")
        cur = اتصال.execute("SELECT v FROM vals")
        first = قاعدة_بيانات.اجلب_واحد(cur)
        assert first[0] == "first"

    def test_executemany_unbound(self, قاعدة_بيانات, اتصال):
        """نفذ_عديد is Connection.executemany (unbound); bulk inserts work."""
        قاعدة_بيانات.نفذ(اتصال, "CREATE TABLE lang (name TEXT)")
        names = [("Python",), ("Arabic",), ("عربي",)]
        قاعدة_بيانات.نفذ_عديد(اتصال, "INSERT INTO lang VALUES (?)", names)
        count = اتصال.execute("SELECT COUNT(*) FROM lang").fetchone()[0]
        assert count == 3

    def test_cursor_new_alias(self, قاعدة_بيانات, اتصال):
        """مؤشر_جديد is Connection.cursor (unbound); creates a new Cursor."""
        cur = قاعدة_بيانات.مؤشر_جديد(اتصال)
        assert isinstance(cur, sqlite3.Cursor)

    def test_close_connection_unbound(self, قاعدة_بيانات):
        """اغلق is Connection.close (unbound); connection is unusable after."""
        conn = قاعدة_بيانات.اتصل(":memory:")
        قاعدة_بيانات.اغلق(conn)
        with pytest.raises(sqlite3.ProgrammingError):
            conn.execute("SELECT 1")

    # ── Error handling ────────────────────────────────────────────────────────

    def test_operational_error_on_bad_sql(self, قاعدة_بيانات, اتصال):
        """خطا_تشغيل is raised when executing malformed SQL."""
        with pytest.raises(sqlite3.OperationalError):
            قاعدة_بيانات.نفذ(اتصال, "SELECT * FROM nonexistent_table")
