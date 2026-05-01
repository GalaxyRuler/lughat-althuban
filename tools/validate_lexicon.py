"""Validate the canonical Arabic programming lexicon and generated outputs."""

from __future__ import annotations

import contextlib
import re
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON_DIR = ROOT / "lexicon"
PACKAGE_DICTIONARIES = ROOT / "arabicpython" / "dictionaries"
ROOT_DICTIONARIES = ROOT / "dictionaries"
ALIASES_DIR = ROOT / "arabicpython" / "aliases"

CATEGORY_HEADINGS = {
    "## 1. Control-flow keywords": "keyword",
    "### Soft keywords": "keyword",
    "## 2. Literal keywords": "literal",
    "## 3. Built-in types": "type",
    "## 4. Built-in functions": "function",
    "## 5. Built-in exceptions": "exception",
    "## 6. Common methods on built-in types": "method",
}


def _load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def _clean_cell(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == "`" and value[-1] == "`":
        return value[1:-1].strip()
    return value


def _parse_dictionary(path: Path) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    category: str | None = None
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        for heading, heading_category in CATEGORY_HEADINGS.items():
            if stripped.startswith(heading):
                category = heading_category
                break
        else:
            if stripped.startswith("## "):
                category = "IGNORED"
            if not (stripped.startswith("|") and stripped.endswith("|")):
                continue
            if category in (None, "IGNORED"):
                continue
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if len(cells) >= 2 and (
                set(cells[0]) <= {"-"} or (cells[0] == "Python" and cells[1] == "Canonical")
            ):
                continue
            if len(cells) != 4:
                raise AssertionError(f"{path}:{line_no}: expected 4 table cells")
            entries.append((category, _clean_cell(cells[0]), _clean_cell(cells[1])))
    return entries


def _normalize(value: str) -> str:
    from arabicpython.normalize import normalize_identifier

    return normalize_identifier(value)


def validate_core_shape(errors: list[str]) -> dict:
    core = _load_toml(LEXICON_DIR / "core.toml")
    if "dialect_entry" not in core:
        errors.append("lexicon/core.toml: missing [[dialect_entry]]")
        return core
    required = {"dialect", "category", "python", "canonical", "alternates", "rationale"}
    seen: set[tuple[str, str, str, str]] = set()
    normalized_by_dialect: dict[tuple[str, str, str], str] = {}
    for idx, entry in enumerate(core["dialect_entry"], start=1):
        missing = required - set(entry)
        if missing:
            errors.append(f"core.toml entry {idx}: missing {sorted(missing)}")
            continue
        key = (entry["dialect"], entry["category"], entry["python"], entry["canonical"])
        if key in seen:
            errors.append(f"core.toml entry {idx}: duplicate {key}")
        seen.add(key)
        norm_key = (entry["dialect"], entry["category"], _normalize(entry["canonical"]))
        previous = normalized_by_dialect.get(norm_key)
        if previous and previous != entry["python"]:
            errors.append(
                f"core.toml entry {idx}: normalized Arabic collision "
                f"{entry['canonical']!r} between {previous!r} and {entry['python']!r}"
            )
        normalized_by_dialect[norm_key] = entry["python"]
    return core


def validate_dictionary_outputs(core: dict, errors: list[str]) -> None:
    expected: dict[str, set[tuple[str, str, str]]] = defaultdict(set)
    for entry in core.get("dialect_entry", []):
        expected[entry["dialect"]].add((entry["category"], entry["python"], entry["canonical"]))

    for dialect, expected_entries in expected.items():
        package_path = PACKAGE_DICTIONARIES / f"{dialect}.md"
        root_path = ROOT_DICTIONARIES / f"{dialect}.md"
        if package_path.read_text(encoding="utf-8") != root_path.read_text(encoding="utf-8"):
            errors.append(f"{dialect}: package and top-level dictionaries differ")
        actual = set(_parse_dictionary(package_path))
        if actual != expected_entries:
            missing = expected_entries - actual
            extra = actual - expected_entries
            if missing:
                errors.append(f"{dialect}: dictionary missing {len(missing)} lexicon entries")
            if extra:
                errors.append(f"{dialect}: dictionary has {len(extra)} entries outside lexicon")


def validate_traceback_exceptions(core: dict, errors: list[str]) -> None:
    from arabicpython.tracebacks import EXCEPTION_NAMES_AR

    active_exceptions = {
        entry["python"]: entry["canonical"]
        for entry in core.get("dialect_entry", [])
        if entry["dialect"] == "ar-v2" and entry["category"] == "exception"
    }
    for py_name, arabic_name in active_exceptions.items():
        display = EXCEPTION_NAMES_AR.get(py_name)
        if display is None:
            continue
        if display != arabic_name:
            errors.append(
                f"tracebacks: {py_name} displays {display!r}, "
                f"but ar-v2 lexicon uses {arabic_name!r}"
            )


def validate_libraries(errors: list[str]) -> None:
    libraries = _load_toml(LEXICON_DIR / "libraries.toml")
    by_file = {item["alias_file"]: item for item in libraries.get("library", [])}
    seen_normalized: dict[str, str] = {}
    for item in libraries.get("library", []):
        norm = _normalize(item["arabic_name"])
        previous = seen_normalized.get(norm)
        if previous and previous != item["python_module"]:
            errors.append(
                f"libraries.toml: normalized Arabic module collision for {item['arabic_name']!r}"
            )
        seen_normalized[norm] = item["python_module"]

    for path in sorted(ALIASES_DIR.glob("*.toml")):
        data = _load_toml(path)
        meta = data.get("meta", {})
        item = by_file.get(path.name)
        if item is None:
            errors.append(f"{path.name}: missing from lexicon/libraries.toml")
            continue
        if item["arabic_name"] != meta.get("arabic_name"):
            errors.append(f"{path.name}: Arabic library name differs from lexicon")
        if item["python_module"] != meta.get("python_module"):
            errors.append(f"{path.name}: Python module name differs from lexicon")


def validate_messages(errors: list[str]) -> None:
    messages = _load_toml(LEXICON_DIR / "messages.toml")
    from arabicpython.messages import MESSAGES

    flattened = {
        f"{section}.{key}": value
        for section, values in messages.items()
        if isinstance(values, dict)
        for key, value in values.items()
    }
    if flattened != MESSAGES:
        missing = set(flattened) - set(MESSAGES)
        extra = set(MESSAGES) - set(flattened)
        changed = {key for key in set(flattened) & set(MESSAGES) if flattened[key] != MESSAGES[key]}
        if missing:
            errors.append(
                f"messages.py: missing keys from lexicon/messages.toml: {sorted(missing)}"
            )
        if extra:
            errors.append(f"messages.py: keys outside lexicon/messages.toml: {sorted(extra)}")
        if changed:
            errors.append(
                f"messages.py: values differ from lexicon/messages.toml: {sorted(changed)}"
            )

    arabic_re = re.compile(r"[\u0600-\u06ff]")
    for section, values in messages.items():
        if not isinstance(values, dict):
            continue
        for key, value in values.items():
            if isinstance(value, str) and not arabic_re.search(value):
                errors.append(f"messages.toml: {section}.{key} has no Arabic text")


def validate() -> list[str]:
    errors: list[str] = []
    core = validate_core_shape(errors)
    if core:
        validate_dictionary_outputs(core, errors)
        validate_traceback_exceptions(core, errors)
    validate_libraries(errors)
    validate_messages(errors)
    return errors


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            with contextlib.suppress(AttributeError, OSError, ValueError):
                stream.reconfigure(encoding="utf-8")
    errors = validate()
    if errors:
        for error in errors:
            print(f"خطأ: {error}", file=sys.stderr)
        return 1
    print("تم التحقق من المعجم العربي.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
