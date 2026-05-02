"""Generate dictionaries and Arabic reference docs from the canonical lexicon."""

from __future__ import annotations

import argparse
import difflib
import sys
import tomllib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEXICON_DIR = ROOT / "lexicon"
PACKAGE_DICTIONARIES = ROOT / "arabicpython" / "dictionaries"
PACKAGE_DIR = ROOT / "arabicpython"
ROOT_DICTIONARIES = ROOT / "dictionaries"
DOCS_AR = ROOT / "docs" / "ar"
ALIASES_DIR = ROOT / "arabicpython" / "aliases"

CATEGORY_ORDER = [
    ("keyword", "## 1. Control-flow keywords"),
    ("literal", "## 2. Literal keywords"),
    ("type", "## 3. Built-in types"),
    ("function", "## 4. Built-in functions"),
    ("exception", "## 5. Built-in exceptions"),
    ("method", "## 6. Common methods on built-in types"),
]

CATEGORY_AR = {
    "keyword": "كلمة تحكم",
    "literal": "قيمة حرفية",
    "type": "نوع مدمج",
    "function": "دالة مدمجة",
    "exception": "استثناء",
    "method": "صفة/طريقة شائعة",
}

GENERATED_DIALECTS = {"ar-v1.1", "ar-v2"}


def _load_toml(path: Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


def _quote_toml(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _quote_toml_list(values: list[str]) -> str:
    return "[" + ", ".join(_quote_toml(value) for value in values) + "]"


def _entries_by_dialect() -> dict[str, list[dict]]:
    data = _load_toml(LEXICON_DIR / "core.toml")
    entries: dict[str, list[dict]] = defaultdict(list)
    for entry in data["dialect_entry"]:
        entries[entry["dialect"]].append(entry)
    return dict(entries)


def _format_alternates(alternates: list[str]) -> str:
    return "، ".join(alternates) if alternates else "—"


def render_dictionary(dialect: str, entries: list[dict]) -> str:
    lines = [
        f"# Arabic dialect dictionary — {dialect}",
        "<!-- Generated from lexicon/core.toml. Do not edit by hand. -->",
        "",
        "**Status**: active" if dialect == "ar-v2" else "**Status**: compatibility",
        "**Source of truth**: `lexicon/core.toml`",
        "",
        "## Reading this file",
        "",
        "- **Python**: the Python symbol this entry translates.",
        "- **Canonical**: the visible Arabic spelling shown to learners.",
        "- **Alternates**: defensible non-canonical spellings; not accepted as canonical.",
        "- **Rationale**: why this Arabic term was chosen.",
        "",
        "The runtime normalizer folds hamza variants, final ta marbuta, alef maksura,",
        "harakat, and tatweel. This file keeps the natural visible form.",
        "",
    ]

    grouped: dict[str, list[dict]] = defaultdict(list)
    for entry in entries:
        grouped[entry["category"]].append(entry)

    for category, heading in CATEGORY_ORDER:
        rows = grouped.get(category, [])
        if not rows:
            continue
        lines.extend(
            [heading, "", "| Python | Canonical | Alternates | Rationale |", "|---|---|---|---|"]
        )
        for entry in rows:
            py_symbol = entry["python"]
            lines.append(
                f"| `{py_symbol}` | {entry['canonical']} | "
                f"{_format_alternates(entry.get('alternates', []))} | {entry['rationale']} |"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_glossary(entries_by_dialect: dict[str, list[dict]]) -> str:
    entries = entries_by_dialect["ar-v2"]
    lines = [
        "# معجم البرمجة العربي",
        "",
        "هذا الملف مولد من `lexicon/core.toml`، "
        "وهو مرجع المصطلحات العربية المعتمدة في لغة الثعبان.",
        "",
        "| الرمز في Python | العربية المعتمدة | النوع | بدائل موثقة |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            f"| `{entry['python']}` | {entry['canonical']} | "
            f"{CATEGORY_AR.get(entry['category'], entry['category'])} | "
            f"{_format_alternates(entry.get('alternates', []))} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def render_alias_index() -> str:
    data = _load_toml(LEXICON_DIR / "libraries.toml")
    grouped = _libraries_by_group(data)
    lines = [
        "# فهرس الأسماء العربية للمكتبات",
        "",
        "هذا الفهرس مولد من `lexicon/libraries.toml` وملفات `arabicpython/aliases/*.toml`.",
        "",
    ]
    lines.extend(_render_library_tables(grouped, heading_level=2))
    return "\n".join(lines).rstrip() + "\n"


def render_alias_mapping(library: dict) -> str:
    """Render one runtime alias TOML from its canonical lexicon entry."""
    lines = [
        f"# arabicpython/aliases/{library['alias_file']}",
        "# Generated from lexicon/libraries.toml. Do not edit by hand.",
        "# Schema version: 1",
        "",
        "[meta]",
        f"arabic_name   = {_quote_toml(library['arabic_name'])}",
        f"python_module = {_quote_toml(library['python_module'])}",
        f"dict_version  = {_quote_toml(library.get('dict_version', 'ar-v1'))}",
        f"schema_version = {int(library.get('schema_version', 1))}",
    ]
    maintainer = library.get("maintainer")
    if maintainer is not None:
        lines.append(f"maintainer    = {_quote_toml(str(maintainer))}")

    aliases = library.get("arabic_aliases", [])
    if aliases:
        lines.append(f"arabic_aliases = {_quote_toml_list(aliases)}")

    proxy_classes = library.get("proxy_classes", [])
    if proxy_classes:
        lines.append(f"proxy_classes = {_quote_toml_list(proxy_classes)}")

    lines.extend(["", "[entries]"])
    for arabic_key, python_attr in library.get("entries", {}).items():
        lines.append(f"{_quote_toml(arabic_key)} = {_quote_toml(python_attr)}")

    lines.extend(["", "[attributes]"])
    for arabic_key, python_attr in library.get("attributes", {}).items():
        lines.append(f"{_quote_toml(arabic_key)} = {_quote_toml(python_attr)}")

    return "\n".join(lines).rstrip() + "\n"


def render_alias_mappings() -> dict[Path, str]:
    data = _load_toml(LEXICON_DIR / "libraries.toml")
    return {
        ALIASES_DIR / library["alias_file"]: render_alias_mapping(library)
        for library in data.get("library", [])
    }


def _message_entries() -> dict[str, str]:
    data = _load_toml(LEXICON_DIR / "messages.toml")
    return {
        f"{section}.{key}": value
        for section, values in data.items()
        if isinstance(values, dict)
        for key, value in values.items()
    }


def render_messages_module() -> str:
    entries = _message_entries()
    lines = [
        '"""Generated Arabic user-facing message data."""',
        "",
        "# Generated from lexicon/messages.toml. Do not edit by hand.",
        "# fmt: off",
        "# ruff: noqa: E501",
        "",
        "MESSAGES: dict[str, str] = {",
    ]
    for key in sorted(entries):
        lines.append(f"    {key!r}: {entries[key]!r},")
    lines.extend(["}", ""])
    return "\n".join(lines)


def render_traceback_data_module() -> str:
    data = _load_toml(LEXICON_DIR / "messages.toml")
    exceptions = data.get("traceback_exception", [])
    patterns = data.get("traceback_pattern", [])
    lines = [
        '"""Generated Arabic traceback localization data."""',
        "",
        "# Generated from lexicon/messages.toml. Do not edit by hand.",
        "# fmt: off",
        "# ruff: noqa: E501",
        "",
        "import re",
        "",
        "EXCEPTION_NAMES_AR: dict[str, str] = {",
    ]
    for item in exceptions:
        lines.append(f"    {item['python']!r}: {item['arabic']!r},")
    lines.extend(
        [
            "}",
            "",
            "_MSG_PATTERNS: list[tuple[re.Pattern[str], str]] = [",
        ]
    )
    for item in patterns:
        lines.append(f"    (re.compile({item['pattern']!r}), {item['template']!r}),")
    lines.extend(
        [
            "]",
            "",
            "MESSAGE_TEMPLATES_AR = _MSG_PATTERNS",
            "",
        ]
    )
    return "\n".join(lines)


def _libraries_by_group(data: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for library in data.get("library", []):
        grouped[library.get("group", "third_party")].append(library)
    return dict(grouped)


def _render_library_tables(grouped: dict[str, list[dict]], *, heading_level: int) -> list[str]:
    group_titles = {
        "stdlib": "المكتبة القياسية",
        "web": "الويب",
        "data": "البيانات والعلوم",
        "testing": "الاختبار",
        "documents": "المستندات",
        "media": "الوسائط",
        "ai": "الذكاء الاصطناعي",
        "third_party": "حزم أخرى",
    }
    lines: list[str] = []
    marker = "#" * heading_level
    for group in sorted(grouped):
        lines.extend(
            [
                f"{marker} {group_titles.get(group, group)}",
                "",
                "| العربية | وحدة Python | ملف الخريطة |",
                "|---|---|---|",
            ]
        )
        for library in sorted(grouped[group], key=lambda item: item["arabic_name"]):
            lines.append(
                f"| {library['arabic_name']} | `{library['python_module']}` | "
                f"`arabicpython/aliases/{library['alias_file']}` |"
            )
        lines.append("")
    return lines


def render_unified_lexicon(entries_by_dialect: dict[str, list[dict]]) -> str:
    entries = entries_by_dialect["ar-v2"]
    libraries = _libraries_by_group(_load_toml(LEXICON_DIR / "libraries.toml"))
    lines = [
        "# المعجم العربي الموحد",
        "",
        "هذا الملف هو المرجع العلني الواحد للمصطلحات البرمجية العربية في لغة الثعبان.",
        "يولد من `lexicon/core.toml` و`lexicon/libraries.toml`، "
        "وتبقى الصفحات المتخصصة مثل `glossary.md` و`aliases-index.md` و`stdlib-reference.md` "
        "واجهات مشتقة للتصفح السريع وليست مصادر مستقلة.",
        "",
        "## المصطلحات الأساسية",
        "",
        "| الرمز في Python | العربية المعتمدة | النوع | بدائل موثقة |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        lines.append(
            f"| `{entry['python']}` | {entry['canonical']} | "
            f"{CATEGORY_AR.get(entry['category'], entry['category'])} | "
            f"{_format_alternates(entry.get('alternates', []))} |"
        )

    lines.extend(
        [
            "",
            "## أسماء المكتبات والوحدات",
            "",
            "الأسماء التالية هي الأسماء العربية المعتمدة للاستيراد عبر نظام الأسماء المستعارة.",
            "",
        ]
    )
    lines.extend(_render_library_tables(libraries, heading_level=3))
    lines.extend(
        [
            "## صفحات مشتقة",
            "",
            "- [مسرد المصطلحات الأساسي](glossary.md)",
            "- [فهرس أسماء المكتبات](aliases-index.md)",
            "- [مرجع المكتبة القياسية](stdlib-reference.md)",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def _write_or_check(path: Path, content: str, *, check: bool) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if old == content:
        return False
    if check:
        diff = "\n".join(
            difflib.unified_diff(
                old.splitlines(),
                content.splitlines(),
                fromfile=str(path),
                tofile=f"{path} (generated)",
                lineterm="",
            )
        )
        print(diff)
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def generate(*, check: bool = False) -> int:
    entries_by_dialect = _entries_by_dialect()
    changed = False

    for dialect, entries in sorted(entries_by_dialect.items()):
        if dialect not in GENERATED_DIALECTS:
            continue
        content = render_dictionary(dialect, entries)
        for directory in (PACKAGE_DICTIONARIES, ROOT_DICTIONARIES):
            changed |= _write_or_check(directory / f"{dialect}.md", content, check=check)

    changed |= _write_or_check(
        DOCS_AR / "glossary.md", render_glossary(entries_by_dialect), check=check
    )
    changed |= _write_or_check(DOCS_AR / "aliases-index.md", render_alias_index(), check=check)
    changed |= _write_or_check(
        DOCS_AR / "lexicon.md", render_unified_lexicon(entries_by_dialect), check=check
    )

    for path, content in sorted(render_alias_mappings().items()):
        changed |= _write_or_check(path, content, check=check)

    changed |= _write_or_check(
        PACKAGE_DIR / "_generated_messages.py", render_messages_module(), check=check
    )
    changed |= _write_or_check(
        PACKAGE_DIR / "_generated_traceback_data.py",
        render_traceback_data_module(),
        check=check,
    )

    if check and changed:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ولّد الملفات المشتقة من المعجم العربي.")
    parser.add_argument("--check", action="store_true", help="تحقق من حداثة الملفات دون كتابتها.")
    args = parser.parse_args(argv)
    return generate(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
