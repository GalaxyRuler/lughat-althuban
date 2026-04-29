"""Import hook for .apy files."""

import importlib.abc
import importlib.machinery
import importlib.util
import marshal
import os
import struct
import sys
from collections.abc import Sequence

from arabicpython.translate import translate

# Magic number for .apy bytecode cache files.  Increment whenever the
# translation pipeline changes in a way that invalidates cached bytecode.
# Format: b"APY" + 1-byte version.
_CACHE_MAGIC = b"APY\x02"
_CACHE_MAGIC_LEN = 4
# Header: magic(4) + source_mtime_ns(8) + source_size(8) = 20 bytes
_HEADER_LEN = 20


def _cache_path(source_path: str) -> str:
    """Return the __pycache__ path for a .apy source file's translated bytecode."""
    head, tail = os.path.split(source_path)
    base, _ = os.path.splitext(tail)
    tag = sys.implementation.cache_tag  # e.g. "cpython-313"
    return os.path.join(head, "__pycache__", f"{base}.{tag}.apyc")


def _read_cache(cache_path: str, source_mtime_ns: int, source_size: int):
    """Return cached code object if the cache is valid, else None."""
    try:
        with open(cache_path, "rb") as f:
            data = f.read()
    except (FileNotFoundError, PermissionError, OSError):
        return None

    if len(data) < _HEADER_LEN:
        return None
    if data[:_CACHE_MAGIC_LEN] != _CACHE_MAGIC:
        return None

    cached_mtime_ns, cached_size = struct.unpack_from("<qq", data, _CACHE_MAGIC_LEN)
    if cached_mtime_ns != source_mtime_ns or cached_size != source_size:
        return None

    try:
        return marshal.loads(data[_HEADER_LEN:])
    except (ValueError, EOFError, TypeError):
        return None


def _write_cache(cache_path: str, source_mtime_ns: int, source_size: int, code) -> None:
    """Write compiled code object to cache.  Silently ignores all errors."""
    try:
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        header = _CACHE_MAGIC + struct.pack("<qq", source_mtime_ns, source_size)
        with open(cache_path, "wb") as f:
            f.write(header + marshal.dumps(code))
    except (PermissionError, OSError):
        pass  # Cache writes are best-effort; never fail an import because of them.


class ApyFinder(importlib.abc.MetaPathFinder):
    """Locate `.apy` modules and packages on sys.path / parent __path__."""

    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: object | None = None,
    ) -> importlib.machinery.ModuleSpec | None:
        if path is None:
            path = sys.path

        name = fullname.split(".")[-1]

        for entry in path:
            # Check for package
            pkg_dir = os.path.join(entry, name)
            if os.path.isdir(pkg_dir):
                init_apy = os.path.join(pkg_dir, "__init__.apy")
                if os.path.isfile(init_apy):
                    loader = ApyLoader(fullname, init_apy, is_package=True)
                    return importlib.util.spec_from_file_location(
                        fullname, init_apy, loader=loader, submodule_search_locations=[pkg_dir]
                    )

            # Check for module
            apy_file = os.path.join(entry, f"{name}.apy")
            if os.path.isfile(apy_file):
                loader = ApyLoader(fullname, apy_file, is_package=False)
                return importlib.util.spec_from_file_location(fullname, apy_file, loader=loader)

        return None


class ApyLoader(importlib.abc.Loader):
    """Translate, compile, and exec a `.apy` module.

    Caches compiled bytecode in __pycache__/<name>.<tag>.apyc so that
    subsequent imports of unchanged files skip translation entirely.
    """

    def __init__(self, fullname: str, path: str, *, is_package: bool = False) -> None:
        self.fullname = fullname
        self.path = path
        self._is_package = is_package

    def is_package(self, fullname: str) -> bool:
        """Return True if the module is a package."""
        return self._is_package

    def create_module(self, spec):
        return None  # use default module creation

    def _get_source(self) -> str:
        try:
            with open(self.path, encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError as e:
            raise ImportError(f"can't decode {self.path}: {e}") from e
        except FileNotFoundError:
            raise ImportError(f"file not found: {self.path}") from None

    def _compile(self, source: str) -> object:
        """Translate source and compile to a code object.  Uses .apyc cache."""
        # Stat the source file for cache invalidation.
        try:
            st = os.stat(self.path)
            mtime_ns = st.st_mtime_ns
            size = st.st_size
        except OSError:
            mtime_ns = 0
            size = 0

        cpath = _cache_path(self.path)
        code = _read_cache(cpath, mtime_ns, size)
        if code is not None:
            return code

        try:
            translated = translate(source)
            code = compile(translated, self.path, "exec")
        except SyntaxError as e:
            if e.filename is None:
                e.filename = self.path
            raise

        _write_cache(cpath, mtime_ns, size, code)
        return code

    def exec_module(self, module) -> None:
        source = self._get_source()
        code = self._compile(source)
        exec(code, module.__dict__)

    def get_source(self, fullname: str) -> str:
        """Return the original .apy source (used by linecache / tracebacks)."""
        return self._get_source()


def install() -> None:
    """Idempotent: insert ApyFinder at the FRONT of sys.meta_path if not already there."""
    for finder in sys.meta_path:
        if isinstance(finder, ApyFinder):
            return
    sys.meta_path.insert(0, ApyFinder())


def uninstall() -> None:
    """Idempotent: remove any ApyFinder instances from sys.meta_path."""
    sys.meta_path[:] = [f for f in sys.meta_path if not isinstance(f, ApyFinder)]
