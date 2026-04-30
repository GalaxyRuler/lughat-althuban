"""TOML alias mapping loader and validator."""

from __future__ import annotations

import importlib
import sys
import tomllib
import types
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from arabicpython.normalize import normalize_identifier

REQUIRED_META_FIELDS: frozenset[str] = frozenset(
    {"arabic_name", "python_module", "dict_version", "schema_version"}
)


class AliasMappingError(Exception):
    """Raised when a TOML alias mapping file is malformed or invalid."""


@dataclass(frozen=True)
class AliasMapping:
    """Validated, immutable representation of one alias mapping file."""

    arabic_name: str  # e.g. "طلبات" — the name users import
    python_module: str  # e.g. "requests" — the wrapped stdlib/third-party module
    dict_version: str  # e.g. "ar-v1" — tracks ADR 0003 dictionary versioning
    entries: dict[str, str]  # Arabic attribute → Python attribute name
    attributes: dict[str, str]  # Arabic instance attribute → Python instance attribute
    source_path: Path  # for error messages
    proxy_classes: frozenset[str]  # class names whose *instances* get proxied


def _resolve_dotted_attr(obj: Any, dotted_name: str) -> Any:
    """Resolve a potentially dotted attribute path, e.g. ``'adapters.HTTPAdapter'``.

    If a path step's getattr fails on a module (because the submodule has not
    been imported yet — e.g. ``django.shortcuts``), this attempts an explicit
    ``importlib.import_module`` for that submodule before retrying.  This makes
    libraries that don't auto-import submodules (Django) work transparently.
    """
    result = obj
    for part in dotted_name.split("."):
        try:
            result = getattr(result, part)
        except AttributeError:
            if isinstance(result, types.ModuleType):
                submod_name = f"{result.__name__}.{part}"
                try:
                    importlib.import_module(submod_name)
                except ImportError:
                    # Attribute doesn't exist as a submodule either (e.g.
                    # subprocess.STARTUPINFO on non-Windows).  Re-raise as
                    # AttributeError so load_mapping's version-skipping logic
                    # can issue a warning and continue gracefully.
                    raise AttributeError(
                        f"module {result.__name__!r} has no attribute {part!r}"
                    ) from None
                result = getattr(result, part)
            else:
                raise
    return result


def _validate_alias_table(
    table: Any,
    *,
    toml_path: Path,
    section_name: str,
) -> dict[str, str]:
    """Validate one Arabic→Python TOML table and return a plain dict."""
    if not isinstance(table, dict):
        raise AliasMappingError(f"{toml_path}: [{section_name}] must be a TOML table")

    validated: dict[str, str] = {}
    for arabic_key, python_attr in table.items():
        if not isinstance(python_attr, str):
            raise AliasMappingError(
                f"{toml_path}: [{section_name}] value for {arabic_key!r} must be "
                f"a string, got {type(python_attr).__name__!r}"
            )

        normalized = normalize_identifier(arabic_key)
        if normalized != arabic_key:
            raise AliasMappingError(
                f"{toml_path}: Arabic key {arabic_key!r} does not round-trip through "
                f"normalize_identifier() — got {normalized!r}. "
                f"Store the normalized form as the key."
            )

        validated[arabic_key] = python_attr

    seen_python: dict[str, str] = {}  # python_attr → first arabic_key that claimed it
    for arabic_key, python_attr in validated.items():
        if python_attr in seen_python:
            raise AliasMappingError(
                f"{toml_path}: Python attribute {python_attr!r} is claimed by two Arabic "
                f"keys: {seen_python[python_attr]!r} and {arabic_key!r}. "
                f"Each Python name may appear at most once in the mapping."
            )
        seen_python[python_attr] = arabic_key

    return validated


def load_mapping(toml_path: Path, *, validate_target: bool = True) -> AliasMapping:
    """Parse and validate one alias TOML file.

    Parameters
    ----------
    toml_path:
        Absolute path to a ``*.toml`` alias mapping file.
    validate_target:
        When true, import the target Python module and verify mapped names.
        ``AliasFinder`` uses ``False`` so installing Arabic aliases stays cheap
        and does not import optional third-party dependencies until use.

    Returns
    -------
    AliasMapping
        A frozen dataclass containing the validated mapping.

    Raises
    ------
    AliasMappingError
        On any of: malformed TOML, missing required fields, duplicate Arabic
        keys (rejected by the TOML parser itself), duplicate Python values,
        Arabic keys that don't round-trip through ``normalize_identifier``,
        module not importable, or mapped Python attributes that don't exist.
    """
    # ------------------------------------------------------------------ #
    # 1. Parse TOML
    # ------------------------------------------------------------------ #
    try:
        raw: dict[str, Any] = tomllib.loads(toml_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise AliasMappingError(f"{toml_path}: TOML parse error: {exc}") from exc

    # ------------------------------------------------------------------ #
    # 2. Validate [meta]
    # ------------------------------------------------------------------ #
    meta = raw.get("meta")
    if meta is None:
        raise AliasMappingError(f"{toml_path}: missing [meta] section")

    missing_fields = REQUIRED_META_FIELDS - set(meta.keys())
    if missing_fields:
        raise AliasMappingError(
            f"{toml_path}: [meta] is missing required fields: {sorted(missing_fields)}"
        )

    arabic_name: str = meta["arabic_name"]
    python_module: str = meta["python_module"]
    dict_version: str = meta["dict_version"]

    # Optional proxy_classes — class names whose instances get wrapped
    proxy_classes_raw = meta.get("proxy_classes", [])
    if not isinstance(proxy_classes_raw, list) or not all(
        isinstance(c, str) for c in proxy_classes_raw
    ):
        raise AliasMappingError(
            f"{toml_path}: [meta].proxy_classes must be a list of strings, "
            f"got {proxy_classes_raw!r}"
        )
    proxy_classes: frozenset[str] = frozenset(proxy_classes_raw)

    # ------------------------------------------------------------------ #
    # 3. Validate [entries]
    # ------------------------------------------------------------------ #
    entries_raw = raw.get("entries")
    if entries_raw is None:
        raise AliasMappingError(f"{toml_path}: missing [entries] section")

    entries = _validate_alias_table(entries_raw, toml_path=toml_path, section_name="entries")

    # ------------------------------------------------------------------ #
    # 3c. Validate optional [attributes]
    # ------------------------------------------------------------------ #
    attributes_raw = raw.get("attributes", {})
    attributes = _validate_alias_table(
        attributes_raw,
        toml_path=toml_path,
        section_name="attributes",
    )

    if not validate_target:
        return AliasMapping(
            arabic_name=arabic_name,
            python_module=python_module,
            dict_version=dict_version,
            entries=entries,
            attributes=attributes,
            source_path=toml_path,
            proxy_classes=proxy_classes,
        )

    # ------------------------------------------------------------------ #
    # 4. Import the target module
    # ------------------------------------------------------------------ #
    try:
        module = importlib.import_module(python_module)
    except (ImportError, RuntimeError) as exc:
        raise AliasMappingError(
            f"{toml_path}: Python module {python_module!r} is not importable: {exc}"
        ) from exc

    # ------------------------------------------------------------------ #
    # 5. Verify all mapped Python attributes exist
    #    Attributes absent on the *current* Python version (e.g. Path.walk
    #    added in 3.12) are skipped with a warning rather than aborting the
    #    entire mapping.  This lets a single TOML stay canonical across
    #    versions while gracefully degrading on older interpreters.
    # ------------------------------------------------------------------ #
    validated_entries: dict[str, str] = {}
    for arabic_key, python_attr in entries.items():
        try:
            _resolve_dotted_attr(module, python_attr)
            validated_entries[arabic_key] = python_attr
        except AttributeError:
            warnings.warn(
                f"{toml_path.name}: attribute {python_attr!r} not found in "
                f"{python_module!r} on Python {sys.version_info[:2]}; "
                f"Arabic key {arabic_key!r} will not be available.",
                ImportWarning,
                stacklevel=2,
            )

    # ------------------------------------------------------------------ #
    # 6. Verify proxy_classes entries are actual classes in the module
    # ------------------------------------------------------------------ #
    for cls_name in proxy_classes:
        cls = getattr(module, cls_name, None)
        if cls is None:
            raise AliasMappingError(
                f"{toml_path}: proxy_classes entry {cls_name!r} does not exist "
                f"in module {python_module!r}"
            )
        if not isinstance(cls, type):
            raise AliasMappingError(
                f"{toml_path}: proxy_classes entry {cls_name!r} is not a class "
                f"(got {type(cls).__name__!r})"
            )

    return AliasMapping(
        arabic_name=arabic_name,
        python_module=python_module,
        dict_version=dict_version,
        entries=validated_entries,
        attributes=attributes,
        source_path=toml_path,
        proxy_classes=proxy_classes,
    )
