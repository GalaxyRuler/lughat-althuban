# tests/aliases/test_contextlib.py
# B-038 stdlib aliases — contextlib module tests

import contextlib
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مدير_سياق():
    """Return a ModuleProxy wrapping `contextlib`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مدير_سياق", None, None)
    assert spec is not None, "AliasFinder did not find 'مدير_سياق'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestContextlibProxy:
    # ── Decorator aliases ─────────────────────────────────────────────────────

    def test_contextmanager_alias(self, مدير_سياق):
        """مدير_سياق_داله maps to contextlib.contextmanager."""
        assert مدير_سياق.مدير_سياق_داله is contextlib.contextmanager

    def test_asynccontextmanager_alias(self, مدير_سياق):
        """مدير_سياق_متزامن maps to contextlib.asynccontextmanager."""
        assert مدير_سياق.مدير_سياق_متزامن is contextlib.asynccontextmanager

    # ── Utility aliases ───────────────────────────────────────────────────────

    def test_closing_alias(self, مدير_سياق):
        """اغلاق_تلقائي maps to contextlib.closing."""
        assert مدير_سياق.اغلاق_تلقائي is contextlib.closing

    def test_suppress_alias(self, مدير_سياق):
        """اكتم maps to contextlib.suppress."""
        assert مدير_سياق.اكتم is contextlib.suppress

    def test_nullcontext_alias(self, مدير_سياق):
        """سياق_فارغ maps to contextlib.nullcontext."""
        assert مدير_سياق.سياق_فارغ is contextlib.nullcontext

    def test_redirect_stdout_alias(self, مدير_سياق):
        """اعد_خارج maps to contextlib.redirect_stdout."""
        assert مدير_سياق.اعد_خارج is contextlib.redirect_stdout

    def test_redirect_stderr_alias(self, مدير_سياق):
        """اعد_خطا_خارج maps to contextlib.redirect_stderr."""
        assert مدير_سياق.اعد_خطا_خارج is contextlib.redirect_stderr

    # ── Stack aliases ─────────────────────────────────────────────────────────

    def test_exitstack_alias(self, مدير_سياق):
        """مكدس_خروج maps to contextlib.ExitStack."""
        assert مدير_سياق.مكدس_خروج is contextlib.ExitStack

    def test_asyncexitstack_alias(self, مدير_سياق):
        """مكدس_خروج_متزامن maps to contextlib.AsyncExitStack."""
        assert مدير_سياق.مكدس_خروج_متزامن is contextlib.AsyncExitStack

    # ── Abstract base class aliases ───────────────────────────────────────────

    def test_abstract_cm_alias(self, مدير_سياق):
        """مدير_سياق_مجرد maps to contextlib.AbstractContextManager."""
        assert مدير_سياق.مدير_سياق_مجرد is contextlib.AbstractContextManager

    def test_abstract_async_cm_alias(self, مدير_سياق):
        """مدير_سياق_متزامن_مجرد maps to contextlib.AbstractAsyncContextManager."""
        assert مدير_سياق.مدير_سياق_متزامن_مجرد is contextlib.AbstractAsyncContextManager

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_contextmanager_decorator(self, مدير_سياق):
        """مدير_سياق_داله turns a generator into a context manager."""
        log = []

        @مدير_سياق.مدير_سياق_داله
        def managed():
            log.append("enter")
            yield 42
            log.append("exit")

        with managed() as val:
            log.append(f"inside:{val}")

        assert log == ["enter", "inside:42", "exit"]

    def test_suppress_hides_exception(self, مدير_سياق):
        """اكتم suppresses the specified exception type."""
        result = []
        with مدير_سياق.اكتم(ZeroDivisionError):
            result.append(1 / 0)  # raises, but suppressed
        assert result == []  # never appended

    def test_suppress_does_not_hide_other_exceptions(self, مدير_سياق):
        """اكتم does not suppress unrelated exception types."""
        with pytest.raises(ValueError), مدير_سياق.اكتم(ZeroDivisionError):
            raise ValueError("not suppressed")

    def test_nullcontext_returns_value(self, مدير_سياق):
        """سياق_فارغ passes its argument through as the context value."""
        with مدير_سياق.سياق_فارغ(99) as val:
            assert val == 99

    def test_closing_calls_close(self, مدير_سياق):
        """اغلاق_تلقائي calls .close() on exit."""
        import io

        buf = io.StringIO()
        with مدير_سياق.اغلاق_تلقائي(buf):
            buf.write("data")
        assert buf.closed

    def test_redirect_stdout_captures(self, مدير_سياق):
        """اعد_خارج redirects stdout to a StringIO buffer."""
        import io

        out = io.StringIO()
        with مدير_سياق.اعد_خارج(out):
            print("captured")
        assert out.getvalue().strip() == "captured"

    def test_exitstack_callbacks(self, مدير_سياق):
        """مكدس_خروج runs registered callbacks in LIFO order on exit."""
        log = []
        with مدير_سياق.مكدس_خروج() as stack:
            stack.callback(log.append, "first")
            stack.callback(log.append, "second")
        assert log == ["second", "first"]
