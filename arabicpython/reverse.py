"""Reverse translation from Python source to Arabic Python source."""

from __future__ import annotations

import ast
import io
import tokenize
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from arabicpython.dialect import load_dialect
from arabicpython.normalize import normalize_identifier

if TYPE_CHECKING:
    from arabicpython.dialect import Dialect


_LEVEL_CATEGORIES: dict[int, frozenset[str]] = {
    1: frozenset({"keyword", "literal"}),
    2: frozenset({"keyword", "literal", "type", "function"}),
    3: frozenset({"keyword", "literal", "type", "function", "exception"}),
}


@dataclass(frozen=True)
class ReverseTranslation:
    source: str
    replacements: int


class _BoundNameVisitor(ast.NodeVisitor):
    """Collect Python names that are user-bound and should not be Arabicized."""

    def __init__(self) -> None:
        self.names: set[str] = set()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.names.add(node.name)
        self._visit_arguments(node.args)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.visit_FunctionDef(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.names.add(node.name)
        self.generic_visit(node)

    def visit_arg(self, node: ast.arg) -> None:
        self.names.add(node.arg)

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, (ast.Store, ast.Del)):
            self.names.add(node.id)

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.name:
            self.names.add(node.name)
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            self.names.add(alias.asname or alias.name.split(".", 1)[0])

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        for alias in node.names:
            self.names.add(alias.asname or alias.name)

    def _visit_arguments(self, node: ast.arguments) -> None:
        for arg in [*node.posonlyargs, *node.args, *node.kwonlyargs]:
            self.names.add(arg.arg)
        if node.vararg:
            self.names.add(node.vararg.arg)
        if node.kwarg:
            self.names.add(node.kwarg.arg)


def _bound_names(source: str) -> set[str]:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return set()
    visitor = _BoundNameVisitor()
    visitor.visit(tree)
    return visitor.names


def _category_for_python_name(dialect: Dialect, python_name: str) -> str | None:
    arabic = dialect.reverse_names.get(python_name)
    if arabic is None:
        return None
    return dialect.categories.get(normalize_identifier(arabic))


def reverse_translate(
    source: str,
    *,
    dialect: Dialect | None = None,
    dict_version: str | None = None,
    level: int = 2,
) -> str:
    """Translate Python source to لغة الثعبان source.

    Level 1 translates keywords and literals.
    Level 2 also translates built-in functions and types.
    Level 3 also translates built-in exception names.
    """
    return reverse_translate_with_count(
        source,
        dialect=dialect,
        dict_version=dict_version,
        level=level,
    ).source


def reverse_translate_with_count(
    source: str,
    *,
    dialect: Dialect | None = None,
    dict_version: str | None = None,
    level: int = 2,
) -> ReverseTranslation:
    if dialect is not None and dict_version is not None:
        raise ValueError(
            "reverse_translate(): supply at most one of 'dialect' and 'dict_version', not both"
        )
    if level not in _LEVEL_CATEGORIES:
        raise ValueError("reverse_translate(): level must be 1, 2, or 3")
    if dialect is None:
        dialect = load_dialect(dict_version or "ar-v2")

    try:
        tokens = list(tokenize.tokenize(io.BytesIO(source.encode("utf-8")).readline))
    except tokenize.TokenError as exc:
        msg, loc = exc.args
        raise SyntaxError(msg, ("<string>", loc[0], loc[1], "", loc[0], loc[1])) from exc

    line_starts = [0]
    for idx, ch in enumerate(source):
        if ch == "\n":
            line_starts.append(idx + 1)

    def abs_pos(row: int, col: int) -> int:
        return line_starts[row - 1] + col

    allowed = _LEVEL_CATEGORIES[level]
    bound_names = _bound_names(source)
    changes: list[tuple[int, int, str]] = []

    last_significant_type: int | None = None
    last_significant_string: str | None = None

    for tok in tokens:
        is_significant = tok.type not in (
            tokenize.NL,
            tokenize.NEWLINE,
            tokenize.INDENT,
            tokenize.DEDENT,
            tokenize.COMMENT,
            tokenize.ENCODING,
            tokenize.ENDMARKER,
        )

        if tok.type == tokenize.NAME:
            is_attr = last_significant_type == tokenize.OP and last_significant_string == "."
            replacement = None
            if not is_attr and tok.string not in bound_names:
                category = _category_for_python_name(dialect, tok.string)
                if category in allowed:
                    replacement = dialect.reverse_names[tok.string]

            if replacement and replacement != tok.string:
                changes.append((abs_pos(*tok.start), abs_pos(*tok.end), replacement))

        if is_significant:
            last_significant_type = tok.type
            last_significant_string = tok.string

    if not changes:
        return ReverseTranslation(source, 0)

    parts: list[str] = []
    prev_end = len(source)
    for start, end, replacement in reversed(changes):
        parts.append(source[end:prev_end])
        parts.append(replacement)
        prev_end = start
    parts.append(source[:prev_end])
    return ReverseTranslation("".join(reversed(parts)), len(changes))


def reverse_file(
    path: str | Path,
    *,
    dict_version: str | None = None,
    level: int = 2,
) -> ReverseTranslation:
    source = Path(path).read_text(encoding="utf-8")
    return reverse_translate_with_count(source, dict_version=dict_version, level=level)
