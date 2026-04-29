"""Translate apython source to Python source."""

import io
import re
import sys
import tokenize
from typing import TYPE_CHECKING

from arabicpython._fstring_311 import rewrite_fstring_literal
from arabicpython.dialect import load_dialect
from arabicpython.normalize import normalize_identifier
from arabicpython.pretokenize import pretokenize

if TYPE_CHECKING:
    from arabicpython.dialect import Dialect


_DIRECTIVE_RE = re.compile(r"#\s*(?:arabicpython|apython)\s*:\s*dict\s*=\s*(\S+)")

_AR_V2_REPLACED_KEYWORDS = {
    normalize_identifier("كـ"): "باسم",
    normalize_identifier("بوصفه"): "باسم",
    normalize_identifier("مرر"): "تجاوز",
    normalize_identifier("طالما"): "بينما",
    normalize_identifier("هو"): "يكون",
}


def _parse_file_directive(source: str) -> "str | None":
    """Return the dict version named by the first per-file directive, or None."""
    for line in source.splitlines()[:5]:
        m = _DIRECTIVE_RE.search(line)
        if m:
            return m.group(1)
    return None


def _raise_replaced_keyword_error(token: tokenize.TokenInfo, replacement: str) -> None:
    message = f"الكلمة '{token.string}' غير معرّفة في ar-v2؛ استخدم '{replacement}'"
    raise SyntaxError(
        message,
        (
            None,
            token.start[0],
            token.start[1] + 1,
            token.line,
            token.end[0],
            token.end[1] + 1,
        ),
    )


def translate(
    source: str,
    *,
    dialect: "Dialect | None" = None,
    dict_version: "str | None" = None,
) -> str:
    """Translate apython source to Python source.

    Pipeline:
      1. pretokenize(source) — fold Arabic digits/punctuation, reject bidi
         outside strings (raises SyntaxError on bidi or mixed-digit literals).
      2. tokenize.tokenize on the result, treated as UTF-8 bytes.
      3. Walk the token stream. For each NAME token:
         - If the previous non-whitespace, non-comment token is OP('.'),
           look up normalize_identifier(name) in dialect.attributes.
         - Otherwise, look up normalize_identifier(name) in dialect.names.
         - On hit, replace the token's string with the dictionary's Python
           symbol (e.g., 'إذا' → 'if', 'قراءة' → 'read').
         - On miss, replace with normalize_identifier(name) — collapses
           harakat/hamza variants per ADR 0004 so equivalent spellings refer
           to the same Python identifier.
         - ASCII-only NAME tokens pass through untouched (fast path).
      4. Apply all changes right-to-left by byte offset into the intermediate
         source, preserving all whitespace and indentation from the original.

    Args:
        source: the .apy source text.
        dialect: optional pre-loaded Dialect to use.  Mutually exclusive with
            dict_version — if both are supplied a ValueError is raised.
        dict_version: name of the dictionary to load (e.g. ``"ar-v1.1"``).
            When omitted and dialect is None, a per-file ``# apython: dict=...``
            directive is honored; otherwise defaults to ``"ar-v1"``.

    Returns:
        Python source text suitable for compile(src, path, "exec").

    Raises:
        ValueError: if both dialect and dict_version are supplied.
        FileNotFoundError: if dict_version doesn't resolve to a dictionary file.
        SyntaxError: propagated from pretokenize (bidi, mixed digits) or
            from tokenize (e.g., unclosed string literal).
        DialectError: propagated from load_dialect on first call when no
            explicit dialect is provided.
    """
    if dialect is not None and dict_version is not None:
        raise ValueError(
            "translate(): supply at most one of 'dialect' and 'dict_version', not both"
        )
    if dialect is None:
        effective_dict = dict_version or _parse_file_directive(source) or "ar-v1"
        dialect = load_dialect(effective_dict)

    # Fast path: pure ASCII source has no Arabic keywords or identifiers to
    # translate.  Skip the entire pipeline and return the source unchanged.
    # This makes translate() essentially free for .py files loaded via the hook.
    if source.isascii():
        return source

    # Step 1: pretokenize
    intermediate = pretokenize(source)

    # Strip UTF-8 BOM if present.  The tokenizer skips the BOM when reporting
    # token positions, so our line→char-offset table must NOT include it.
    # We restore the BOM at the end if the original source had one.
    _had_bom = intermediate.startswith("﻿")
    if _had_bom:
        intermediate = intermediate[1:]

    # Step 2: tokenize
    try:
        tokens_gen = tokenize.tokenize(io.BytesIO(intermediate.encode("utf-8")).readline)
        tokens = list(tokens_gen)
    except tokenize.TokenError as e:
        msg, loc = e.args
        raise SyntaxError(msg, ("<string>", loc[0], loc[1], "", loc[0], loc[1])) from e

    for tok in tokens:
        if tok.type == tokenize.ERRORTOKEN:
            raise SyntaxError(
                f"tokenization error near {tok.string!r}",
                ("<string>", tok.start[0], tok.start[1], tok.line, tok.start[0], tok.start[1]),
            )

    # Step 3: NAME rewrite — collect (char_start, char_end, new_str) for each
    # token whose string changes.  Applied right-to-left in Step 4 so earlier
    # character offsets stay valid as we splice from the right.
    #
    # Positional note: tokenize reports tok.start / tok.end as (row, col) where
    # col is a CHARACTER offset in the decoded line (not a byte offset).  We
    # build a line→char-offset table once so each lookup is O(1).
    _line_starts: list[int] = [0]
    for _idx, _ch in enumerate(intermediate):
        if _ch == "\n":
            _line_starts.append(_idx + 1)

    def _abs(row: int, col: int) -> int:
        return _line_starts[row - 1] + col

    # Track last significant token for attribute-context detection.
    # Also track the significant token *before* the most recent '.' to detect
    # the `from . import` pattern where `import`/`استورد` follows a dot but is
    # still a keyword, not an attribute.
    last_significant_type = None
    last_significant_string = None
    before_dot_string: str | None = None

    # changes: (char_start, char_end, new_str) in token order.
    changes: list[tuple[int, int, str]] = []

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
            key = normalize_identifier(tok.string)

            if dialect.name == "ar-v2" and key in _AR_V2_REPLACED_KEYWORDS:
                _raise_replaced_keyword_error(tok, _AR_V2_REPLACED_KEYWORDS[key])

            # Keywords translate even after '.' only in `from . import` context
            # (token before the dot was `from`/`من`).  In normal attribute access
            # (`obj.اطبع`) the keyword table is suppressed so user-defined method
            # names don't accidentally map to Python builtins.
            _bds_key = normalize_identifier(before_dot_string) if before_dot_string else ""
            is_from_keyword = _bds_key in dialect.names and dialect.names[_bds_key] == "from"
            is_relative_import_ctx = is_attr and (is_from_keyword or before_dot_string == "from")

            if (not is_attr or is_relative_import_ctx) and key in dialect.names:
                new_string = dialect.names[key]
            elif is_attr and key in dialect.attributes:
                new_string = dialect.attributes[key]
            else:
                new_string = key

            if new_string != tok.string:
                changes.append((_abs(*tok.start), _abs(*tok.end), new_string))

        elif tok.type == tokenize.STRING and sys.version_info < (3, 12):
            # TODO(phase-b-drop-311): delete this branch when 3.11 support drops.
            new_literal = rewrite_fstring_literal(tok.string, dialect)
            if new_literal != tok.string:
                changes.append((_abs(*tok.start), _abs(*tok.end), new_literal))

        if is_significant:
            if tok.type == tokenize.OP and tok.string == ".":
                before_dot_string = last_significant_string
            last_significant_type = tok.type
            last_significant_string = tok.string

    # Step 4: apply changes right-to-left so earlier character offsets stay valid.
    if not changes:
        result_str = intermediate
    else:
        parts: list[str] = []
        prev_end = len(intermediate)
        for cs, ce, replacement in reversed(changes):
            parts.append(intermediate[ce:prev_end])
            parts.append(replacement)
            prev_end = cs
        parts.append(intermediate[:prev_end])
        result_str = "".join(reversed(parts))

    # BOM was stripped from intermediate before tokenizing; don't restore it —
    # compile() rejects U+FEFF as a non-printable character in Python 3.13+.

    return result_str
