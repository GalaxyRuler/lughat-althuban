"""Translated tracebacks for Arabic Python."""

import sys
import traceback
import types
from pathlib import Path
from typing import IO, Any

# --- Translation tables (data) ---
from arabicpython._generated_traceback_data import (
    EXCEPTION_NAMES_AR,
    MESSAGE_TEMPLATES_AR,
)

# --- Public API ---


def translate_exception_name(name: str) -> str:
    """Look up the Arabic display name for an exception class.

    Returns the original name if no translation exists.
    """
    return EXCEPTION_NAMES_AR.get(name, name)


def translate_exception_message(
    message: str | type[BaseException], exc_value: BaseException | None = None
) -> str:
    """Translate a CPython interpreter-level exception message to Arabic.

    Walks MESSAGE_TEMPLATES_AR; on first regex match, formats the Arabic
    template with the named groups from the match. Returns the original
    message if no template matches.
    """
    message = str(exc_value) if exc_value is not None else str(message)
    for pattern, template in MESSAGE_TEMPLATES_AR:
        match = pattern.match(message)
        if match:
            # For "pop from an empty (set|deque|dict)", we need to handle
            # positional groups if any. The spec says "إخراج من {1} فارغ"
            # but also "template with the named groups from the match".
            # match.groupdict() only has named groups.
            # If the template has {1}, it's probably positional.
            groups: dict[str, Any] = match.groupdict()
            # If there are positional groups, let's add them too as string keys
            for i, val in enumerate(match.groups(), 1):
                groups[str(i)] = val
            return template.format(**groups)
    return message


def format_translated_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
    *,
    message_mode: str = "arabic",
) -> str:
    """Format an exception in Arabic. Returns the formatted string.

    Output structure (one block, each line ending with \n):

        تتبع_الأخطاء (المكدس الأحدث آخرا):
          ملف "{path}", سطر {N}, في {scope}
            {source_line}
          ملف "{path}", سطر {N}, في {scope}
            {source_line}
        {ArabicTypeName}: {translated_message}
    """
    blocks = []

    # Handle chaining
    if exc_value.__cause__ is not None:
        blocks.append(
            format_translated_exception(
                type(exc_value.__cause__),
                exc_value.__cause__,
                exc_value.__cause__.__traceback__,
                message_mode=message_mode,
            )
        )
        blocks.append("\nالسبب المباشر للاستثناء أعلاه:\n\n")
    elif exc_value.__context__ is not None and not exc_value.__suppress_context__:
        blocks.append(
            format_translated_exception(
                type(exc_value.__context__),
                exc_value.__context__,
                exc_value.__context__.__traceback__,
                message_mode=message_mode,
            )
        )
        blocks.append("\nأثناء معالجة الاستثناء أعلاه, حدث استثناء آخر:\n\n")

    current_blocks = []
    current_blocks.append("تتبع_الأخطاء (المكدس الأحدث آخرا):\n")

    if exc_tb:
        for frame in traceback.extract_tb(exc_tb):
            if Path(frame.filename).name == "cli.py" and frame.name == "main":
                continue
            scope = frame.name
            if scope == "<module>":
                scope = "<الوحدة>"
            current_blocks.append(f'  ملف "{frame.filename}", سطر {frame.lineno}, في {scope}\n')
            if frame.line:
                current_blocks.append(f"    {frame.line}\n")

    # Special handling for SyntaxError - leads with a File line and shows caret
    if isinstance(exc_value, SyntaxError) and not exc_tb and exc_value.filename:
        # SyntaxError usually has filename, lineno, offset, text
        # If it's a SyntaxError, stock Python often prints a different lead-in
        # but the spec says to match the Arabic type/message.
        # traceback.format_exception_only(exc_type, exc_value) handles the caret part.

        # The spec says: "For SyntaxError specifically, also include the '    ^' caret line
        # as stock Python does (untranslated marker; it points at a column).
        # the lead-in '  File ...' line uses the Arabic form."

        # If we have no traceback (like in compile), we might still want to print the File line.
        current_blocks.append(f'  ملف "{exc_value.filename}", سطر {exc_value.lineno or 1}\n')
        if exc_value.text:
            current_blocks.append(f"    {exc_value.text.strip()}\n")
            if exc_value.offset is not None:
                # offset is 1-indexed
                current_blocks.append("    " + " " * (exc_value.offset - 1) + "^\n")

    type_name = translate_exception_name(exc_type.__name__)
    # For some exceptions like KeyError, str(exc_value) might be the key's repr.
    # We should match what format_exception_only does if possible, but the spec
    # says translate_exception_message(str(exc_value)).
    if message_mode == "english":
        message = str(exc_value)
    else:
        message = translate_exception_message(str(exc_value))

    current_blocks.append(f"{type_name}: {message}\n")

    blocks.append("".join(current_blocks))
    return "".join(blocks)


def format_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
    *,
    mode: str = "arabic",
) -> str:
    """Format an exception according to the requested traceback localization mode."""
    if mode == "english":
        return "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    if mode == "mixed":
        return format_translated_exception(
            exc_type,
            exc_value,
            exc_tb,
            message_mode="english",
        )
    if mode != "arabic":
        raise ValueError("traceback mode must be 'arabic', 'english', or 'mixed'")
    return format_translated_exception(exc_type, exc_value, exc_tb)


def format_arabic_traceback(
    exc_info: tuple[type[BaseException], BaseException, types.TracebackType | None],
    *,
    level: str = "full",
) -> str:
    """Phase D compatibility wrapper for Arabic traceback formatting."""
    if level not in {"full", "message"}:
        raise ValueError("level must be 'full' or 'message'")
    exc_type, exc_value, exc_tb = exc_info
    return format_translated_exception(exc_type, exc_value, exc_tb)


def print_translated_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
    file: "IO[str] | None" = None,
    *,
    mode: str | None = None,
) -> None:
    """Format and write the traceback to `file` (default sys.stderr)."""
    if file is None:
        file = sys.stderr
    file.write(format_exception(exc_type, exc_value, exc_tb, mode=mode or _traceback_mode))


_saved_excepthook = None
_traceback_mode = "arabic"


def install_excepthook(mode: str = "arabic") -> None:
    """Set sys.excepthook to print_translated_exception.

    Idempotent: calling install_excepthook() twice does not re-install. The
    previous excepthook is saved at module level so uninstall() can restore it.
    """
    global _saved_excepthook, _traceback_mode
    if mode not in {"arabic", "english", "mixed"}:
        raise ValueError("traceback mode must be 'arabic', 'english', or 'mixed'")
    _traceback_mode = mode
    if sys.excepthook is print_translated_exception:
        return
    _saved_excepthook = sys.excepthook
    sys.excepthook = print_translated_exception


def uninstall_excepthook() -> None:
    """Restore the excepthook saved before install_excepthook(). Idempotent."""
    global _saved_excepthook
    if _saved_excepthook is not None:
        sys.excepthook = _saved_excepthook
        _saved_excepthook = None
