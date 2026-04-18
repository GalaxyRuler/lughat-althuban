# Spec Packet 0009: translated-tracebacks-v1

**Phase**: A (final core packet)
**Depends on**: Packet 0006 (cli); Packet 0008 (repl); ADR 0001 (architecture), ADR 0007 (scope).
**Estimated size**: medium-large (one focused implementer session, possibly two)
**Owner**: Gemini 3.1 Flash

## Goal

When a user's `.apy` program raises an uncaught exception, render the traceback header, frame lines, and the exception's type+message in Arabic. After this packet lands, a learner who divides by zero sees Arabic text describing the error, not English.

This is the last Phase A core packet. After it lands, Phase A is functionally complete: a learner can write Arabic code, run it from the CLI or REPL, import other Arabic modules, and read errors in Arabic.

## Non-goals

- **No translation of stdlib internal exception messages.** A `json.JSONDecodeError` raised from inside `json.loads` keeps its English message. Only exceptions whose message comes from CPython's interpreter itself (the ~30 patterns in this packet) get translated. Library-raised messages are out of scope per ADR 0007.
- **No translation of third-party library exception messages.** Same reason.
- **No translation of the offending source line.** When a traceback shows `    x = 1 / 0`, the source line is shown verbatim from the user's `.apy` file. No re-translation, no normalization. (The line came from the user; printing it as-typed is the right behavior.)
- **No localization framework.** This is a hard-coded Arabic translation, not a gettext-style i18n layer. A general localization layer is Phase B work.
- **No translation of exception class names AS REFERENCED in user code.** `try: ... except ValueError:` — `ValueError` is a Python identifier the user typed; if they typed `خطأ_القيمة` the dictionary already aliases it. The class name in the traceback header IS translated for display only — the actual class identity is unchanged.
- **No translation of warnings.** `DeprecationWarning` and friends print via `warnings.formatwarning`; out of scope. (Few learners hit warnings; revisit if asked.)
- **No translation of `traceback.print_exc()` calls inside user code.** If the user's `.apy` script explicitly imports `traceback` and calls its formatter, the output is English. We only override what's printed by `sys.excepthook` (CLI) and `code.InteractiveConsole.showtraceback` (REPL). Document this limitation in the delivery note.
- **No suggestion translation.** Python 3.12+ adds "Did you mean: '...'" suggestions to `NameError` and `AttributeError`. We strip the suggestion in v1 (or pass it through verbatim — implementer's choice; document the choice). Translating suggestions properly requires understanding their structure; deferred.

## Files

### Files to create

- `arabicpython/tracebacks.py` — translation tables, formatter, and excepthook installer.
- `dictionaries/exceptions-ar-v1.md` — human-readable reference doc listing every translated exception type and message template. **The runtime data lives in `tracebacks.py`**; the doc is the curatorial layer (mirrors the relationship between `ar-v1.md` and `dialect.py`).
- `tests/test_tracebacks.py`

### Files to modify

- `arabicpython/cli.py` — replace the `traceback.print_exc()` calls inside `main()` with calls to the new formatter. Approximately 3-4 line edits in the existing exception-handling blocks.
- `arabicpython/repl.py` — override `ArabicConsole.showtraceback()` to use the new formatter.
- `arabicpython/__init__.py` — re-export `format_translated_exception` and `install_excepthook` for ergonomics.

### Files to read (do not modify)

- `arabicpython/cli.py`, `arabicpython/repl.py` — current exception-handling code.
- `dictionaries/ar-v1.md` — reference for naming style consistency.
- `decisions/0001-architecture.md`, `decisions/0007-scope.md`.
- Python `traceback` module: https://docs.python.org/3/library/traceback.html
- CPython `Lib/traceback.py` — for the canonical structure of `TracebackException` and `format_exception_only`.

## Public interface

```python
# arabicpython/tracebacks.py

import re
import sys
import traceback
from typing import IO


# --- Translation tables (data) ---

EXCEPTION_NAMES_AR: dict[str, str] = {
    "ZeroDivisionError": "خطأ_القسمة_على_صفر",
    # ... see "Translation tables" below for full list
}

# Each entry: (compiled_regex, arabic_template_with_named_groups)
MESSAGE_TEMPLATES_AR: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^division by zero$"), "القسمة على صفر"),
    (re.compile(r"^name '(?P<name>[^']+)' is not defined$"),
     "الاسم '{name}' غير معرّف"),
    # ... see "Translation tables" below
]


# --- Public API ---

def translate_exception_name(name: str) -> str:
    """Look up the Arabic display name for an exception class.

    Returns the original name if no translation exists.
    """


def translate_exception_message(message: str) -> str:
    """Translate a CPython interpreter-level exception message to Arabic.

    Walks MESSAGE_TEMPLATES_AR; on first regex match, formats the Arabic
    template with the named groups from the match. Returns the original
    message if no template matches.
    """


def format_translated_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
) -> str:
    """Format an exception in Arabic. Returns the formatted string.

    Output structure (one block, each line ending with \\n):

        تتبع_الأخطاء (المكدس الأحدث آخرا):
          ملف "{path}", سطر {N}, في {scope}
            {source_line}
          ملف "{path}", سطر {N}, في {scope}
            {source_line}
        {ArabicTypeName}: {translated_message}

    For SyntaxError specifically, also include the "    ^" caret line as
    stock Python does (untranslated marker; it points at a column).
    """


def print_translated_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
    file: "IO[str] | None" = None,
) -> None:
    """Format and write the traceback to `file` (default sys.stderr)."""


def install_excepthook() -> None:
    """Set sys.excepthook to print_translated_exception.

    Idempotent: calling install_excepthook() twice does not re-install. The
    previous excepthook is saved at module level so uninstall() can restore it.
    """


def uninstall_excepthook() -> None:
    """Restore the excepthook saved before install_excepthook(). Idempotent."""
```

## Translation tables

The full v1 tables. Implementer must include all entries below verbatim. Do NOT add entries beyond this list in v1 — keeping the surface small makes it easy to audit and document. Adding more is a v1.1 task.

### Exception type names (30)

| Python | Arabic |
|---|---|
| `BaseException` | `استثناء_أساسي` |
| `Exception` | `استثناء` |
| `ArithmeticError` | `خطأ_حسابي` |
| `AssertionError` | `خطأ_تأكيد` |
| `AttributeError` | `خطأ_خاصية` |
| `BlockingIOError` | `خطأ_إدخال_إخراج_حاجب` |
| `EOFError` | `خطأ_نهاية_الملف` |
| `FileExistsError` | `خطأ_الملف_موجود` |
| `FileNotFoundError` | `خطأ_الملف_غير_موجود` |
| `FloatingPointError` | `خطأ_فاصلة_عائمة` |
| `ImportError` | `خطأ_استيراد` |
| `IndentationError` | `خطأ_إزاحة` |
| `IndexError` | `خطأ_فهرس` |
| `IsADirectoryError` | `خطأ_هذا_مجلد` |
| `KeyError` | `خطأ_مفتاح` |
| `KeyboardInterrupt` | `مقاطعة_لوحة_المفاتيح` |
| `LookupError` | `خطأ_بحث` |
| `MemoryError` | `خطأ_ذاكرة` |
| `ModuleNotFoundError` | `خطأ_الوحدة_غير_موجودة` |
| `NameError` | `خطأ_اسم` |
| `NotADirectoryError` | `خطأ_ليس_مجلدا` |
| `NotImplementedError` | `خطأ_غير_منفذ` |
| `OSError` | `خطأ_نظام` |
| `OverflowError` | `خطأ_فيضان` |
| `PermissionError` | `خطأ_صلاحيات` |
| `RecursionError` | `خطأ_عودية` |
| `RuntimeError` | `خطأ_تشغيل` |
| `StopIteration` | `إيقاف_التكرار` |
| `SyntaxError` | `خطأ_صياغة` |
| `SystemExit` | `خروج_نظام` |
| `TabError` | `خطأ_تبويب` |
| `TimeoutError` | `خطأ_انتهاء_مهلة` |
| `TypeError` | `خطأ_نوع` |
| `UnicodeDecodeError` | `خطأ_فك_يونيكود` |
| `UnicodeEncodeError` | `خطأ_ترميز_يونيكود` |
| `UnicodeError` | `خطأ_يونيكود` |
| `ValueError` | `خطأ_قيمة` |
| `ZeroDivisionError` | `خطأ_القسمة_على_صفر` |

(38 entries total. Underscores for word-joins per ADR 0001 conventions; matches the keyword dictionary style.)

### Message templates (~25)

Order matters — `MESSAGE_TEMPLATES_AR` is walked top-to-bottom and the first matching regex wins. Put more specific patterns first. Each pattern is anchored with `^...$` to prevent partial matches on long messages.

| Pattern (Python regex) | Arabic template |
|---|---|
| `^division by zero$` | `القسمة على صفر` |
| `^integer division or modulo by zero$` | `قسمة صحيحة أو باقي على صفر` |
| `^float division by zero$` | `قسمة عشرية على صفر` |
| `^name '(?P<name>[^']+)' is not defined$` | `الاسم '{name}' غير معرّف` |
| `^name '(?P<name>[^']+)' is not defined\. Did you mean: '(?P<sugg>[^']+)'\?$` | `الاسم '{name}' غير معرّف. هل تقصد: '{sugg}'؟` |
| `^free variable '(?P<name>[^']+)' referenced before assignment in enclosing scope$` | `المتغير الحر '{name}' مستخدم قبل تعريفه في النطاق المحيط` |
| `^local variable '(?P<name>[^']+)' referenced before assignment$` | `المتغير المحلي '{name}' مستخدم قبل تعريفه` |
| `^'(?P<type>[^']+)' object has no attribute '(?P<attr>[^']+)'$` | `الكائن من نوع '{type}' لا يملك الخاصية '{attr}'` |
| `^'(?P<type>[^']+)' object is not subscriptable$` | `الكائن من نوع '{type}' لا يقبل الفهرسة` |
| `^'(?P<type>[^']+)' object is not callable$` | `الكائن من نوع '{type}' غير قابل للاستدعاء` |
| `^'(?P<type>[^']+)' object is not iterable$` | `الكائن من نوع '{type}' غير قابل للتكرار` |
| `^'(?P<type>[^']+)' object cannot be interpreted as an integer$` | `الكائن من نوع '{type}' لا يمكن تفسيره كعدد صحيح` |
| `^argument of type '(?P<type>[^']+)' is not iterable$` | `الوسيط من نوع '{type}' غير قابل للتكرار` |
| `^list index out of range$` | `فهرس القائمة خارج النطاق` |
| `^tuple index out of range$` | `فهرس الصف خارج النطاق` |
| `^string index out of range$` | `فهرس النص خارج النطاق` |
| `^pop from empty list$` | `إخراج من قائمة فارغة` |
| `^pop from an empty (set\|deque\|dict)$` | `إخراج من {1} فارغ` |
| `^dictionary changed size during iteration$` | `تغير حجم القاموس أثناء التكرار` |
| `^maximum recursion depth exceeded(?P<rest>.*)$` | `تم تجاوز عمق العودية الأقصى{rest}` |
| `^No module named '(?P<name>[^']+)'$` | `لا توجد وحدة باسم '{name}'` |
| `^cannot import name '(?P<name>[^']+)' from '(?P<module>[^']+)'(?P<rest>.*)$` | `لا يمكن استيراد الاسم '{name}' من '{module}'{rest}` |
| `^unsupported operand type\(s\) for (?P<op>\S+): '(?P<a>[^']+)' and '(?P<b>[^']+)'$` | `أنواع المعاملات غير مدعومة لـ {op}: '{a}' و '{b}'` |
| `^can only concatenate (?P<a>\w+) \(not "(?P<b>\w+)"\) to \w+$` | `يمكن فقط ضم {a} (لا {b}) إلى {a}` |
| `^invalid literal for int\(\) with base (?P<base>\d+): '(?P<val>[^']*)'$` | `قيمة غير صالحة للدالة int() بالأساس {base}: '{val}'` |
| `^could not convert string to float: '(?P<val>[^']*)'$` | `تعذر تحويل النص إلى عدد عشري: '{val}'` |
| `^expected (?P<n>\d+) (?P<arg_kind>positional argument\|positional arguments), got (?P<got>\d+)$` | `كان متوقعا {n} {arg_kind} لكن تم تمرير {got}` |
| `^(?P<func>\w+)\(\) missing (?P<n>\d+) required positional argument(?P<plural>s?): (?P<rest>.+)$` | `{func}() ينقصها {n} وسيط إجباري{plural}: {rest}` |
| `^(?P<func>\w+)\(\) got an unexpected keyword argument '(?P<name>[^']+)'$` | `{func}() استلمت وسيطا مفتاحيا غير متوقع '{name}'` |
| `^\[Errno (?P<errno>\d+)\] (?P<msg>[^:]+): '(?P<path>.+)'$` | `[رقم الخطأ {errno}] {msg}: '{path}'` *(Note: `{msg}` itself remains English for now — translating Errno text is a follow-up.)* |

(~30 entries. Implementer: exact escaping of regex special characters in Python string literals is tedious; use raw strings (`r"..."`) throughout.)

### Header / frame line strings

| English | Arabic |
|---|---|
| `Traceback (most recent call last):` | `تتبع_الأخطاء (المكدس الأحدث آخرا):` |
| `  File "{path}", line {N}, in {scope}` | `  ملف "{path}", سطر {N}, في {scope}` |
| `  File "{path}", line {N}` (SyntaxError, no scope) | `  ملف "{path}", سطر {N}` |
| `<module>` (top-level scope marker) | `<الوحدة>` |

For `<module>`, `<lambda>`, `<listcomp>`, `<genexpr>`, `<dictcomp>`, `<setcomp>` — translate `<module>` to `<الوحدة>` and leave the others in English (they're rare and the labels are programmer-facing). Document the choice.

## Behavior

### `format_translated_exception` algorithm

```
1. Build a list of frame strings by walking exc_tb (use traceback.extract_tb).
   For each FrameSummary:
      - Translate the frame line: 'ملف "{filename}", سطر {lineno}, في {name}'
        where {name} is the function name; substitute "<الوحدة>" if name is "<module>".
      - Append the source line (frame.line) indented by 4 spaces, if non-empty.
2. Translate the exception type name via translate_exception_name(exc_type.__name__).
3. Translate the message via translate_exception_message(str(exc_value)).
4. Combine:
      "تتبع_الأخطاء (المكدس الأحدث آخرا):\n"
      + "\n".join(frame_strings) + "\n"
      + "{translated_type}: {translated_message}\n"
5. SyntaxError special case: include the source-line "^" caret marker exactly
   as stock traceback.format_exception_only does. The caret line is unchanged
   (it's just spaces and "^"); the lead-in "  File ..." line uses the Arabic form.
6. If exc_value has __cause__ or __context__ (chained exceptions), recurse on
   the cause/context and prepend its formatted output with one of:
      "السبب المباشر للاستثناء أعلاه:\n\n"  (for __cause__, "raise X from Y")
      "أثناء معالجة الاستثناء أعلاه, حدث استثناء آخر:\n\n"  (for __context__)
   Match stock Python's chaining order (cause/context printed FIRST, then
   the current exception).
```

### `install_excepthook`

```python
_saved_excepthook = None

def install_excepthook() -> None:
    global _saved_excepthook
    if sys.excepthook is print_translated_exception:
        return  # idempotent
    _saved_excepthook = sys.excepthook
    sys.excepthook = print_translated_exception

def uninstall_excepthook() -> None:
    global _saved_excepthook
    if _saved_excepthook is not None:
        sys.excepthook = _saved_excepthook
        _saved_excepthook = None
```

### CLI integration

In `arabicpython/cli.py`, replace the `traceback.print_exc()` calls with `print_translated_exception(*sys.exc_info())`. The three call sites are:

- The `except SyntaxError:` block (around line 128) — already prints SyntaxError specially today; keep that special handling but route through our formatter.
- The general `except Exception:` block at the end of the compile step (around line 132).
- The `except Exception:` block around the `exec` call (around line 164).

Also: at the top of `main()`, after `install()` for the import hook, add `install_excepthook()`. (The excepthook only fires for *uncaught* exceptions; since the CLI catches everything inside `main`, the explicit `print_translated_exception` calls do the actual work. But `install_excepthook` ensures that if a `.apy` program crashes via unhandled exception in a thread or background task, the user still sees Arabic.)

### REPL integration

In `arabicpython/repl.py`, override `ArabicConsole.showtraceback`:

```python
def showtraceback(self) -> None:
    from arabicpython.tracebacks import print_translated_exception
    exc_type, exc_value, exc_tb = sys.exc_info()
    # Trim the top frame which is the InteractiveConsole's exec call;
    # we only want frames inside user code. Match what the parent's
    # showtraceback does — it strips its own frame.
    if exc_tb is not None:
        exc_tb = exc_tb.tb_next
    print_translated_exception(exc_type, exc_value, exc_tb, file=sys.stderr)
```

Do NOT override `showsyntaxerror` in v1 — translate-time SyntaxErrors are already handled by `_write_translate_error` from Packet 0008, and runtime SyntaxErrors during `exec` are exceedingly rare. Document if you decide otherwise.

## Implementation constraints

- **Dependencies**: stdlib only (`re`, `sys`, `traceback`, `types`, `typing`).
- **Python version**: 3.11+.
- **Style**: pass `ruff check .` and `black --check .` at project defaults (line length 100).
- **Encoding**: all Arabic strings are UTF-8 in the source. Add `# -*- coding: utf-8 -*-` at the top of `tracebacks.py` ONLY if `ruff` complains (modern Python doesn't need it but some linters insist).
- **No I/O at import time**: do not read the dictionary file at import. The runtime tables are Python literals.

## Test requirements

All tests in `tests/test_tracebacks.py`. Pytest only.

### Translation lookups (8)

1. `test_translate_exception_name_known`: `translate_exception_name("ZeroDivisionError") == "خطأ_القسمة_على_صفر"`.
2. `test_translate_exception_name_unknown_passes_through`: `translate_exception_name("MyCustomError") == "MyCustomError"`.
3. `test_translate_message_division_by_zero`: `translate_exception_message("division by zero") == "القسمة على صفر"`.
4. `test_translate_message_name_error`: `translate_exception_message("name 'foo' is not defined") == "الاسم 'foo' غير معرّف"`.
5. `test_translate_message_attribute_error`: matches `"'list' object has no attribute 'frobnicate'"` and substitutes both `{type}` and `{attr}`.
6. `test_translate_message_unknown_passes_through`: an arbitrary string not matching any pattern returns unchanged.
7. `test_translate_message_first_match_wins`: a message that COULD match two patterns returns the result of the first.
8. `test_all_38_exception_names_have_translations`: iterate `EXCEPTION_NAMES_AR` and assert every value is non-empty Arabic text (contains at least one Arabic codepoint U+0600–U+06FF).

### Type-name table coverage (4)

9. `test_table_includes_zero_division_error`: `"ZeroDivisionError" in EXCEPTION_NAMES_AR`.
10. `test_table_includes_all_common_types`: assert all of `{"NameError", "TypeError", "ValueError", "IndexError", "KeyError", "AttributeError", "ImportError", "FileNotFoundError", "ZeroDivisionError"}` are keys.
11. `test_table_no_duplicate_arabic_values`: every Arabic name in `EXCEPTION_NAMES_AR` is unique. (Catches accidental copy-paste duplication.)
12. `test_table_arabic_names_are_normalized`: each Arabic value, when passed through `arabicpython.normalize.normalize_identifier`, is unchanged. (Ensures the names follow the same normalization conventions as the keyword dictionary.)

### Message template coverage (3)

13. `test_message_templates_compiled`: every entry in `MESSAGE_TEMPLATES_AR` has a compiled `re.Pattern` as element 0.
14. `test_message_templates_arabic_present`: every template in element 1 contains at least one Arabic codepoint.
15. `test_message_templates_anchored`: every regex pattern starts with `^` and ends with `$`. (Prevents accidental partial matching.)

### `format_translated_exception` (5)

16. `test_format_zero_division_simple`: build a `ZeroDivisionError("division by zero")` with a fake traceback (use `try: 1/0\nexcept: tb = sys.exc_info()`); assert formatted output contains both `خطأ_القسمة_على_صفر` and `القسمة على صفر` and `تتبع_الأخطاء`.
17. `test_format_includes_arabic_module_marker`: a top-level frame's scope shows as `<الوحدة>` not `<module>`.
18. `test_format_includes_file_path_and_line`: formatted output contains `ملف "..."`, `سطر 1` (or whatever).
19. `test_format_chained_exception_with_from`: `try: raise A; except: raise B from A` — formatted output includes the Arabic "السبب المباشر..." marker and BOTH exception types.
20. `test_format_chained_exception_implicit_context`: `try: raise A; except: raise B` (no `from`) — formatted output includes "أثناء معالجة الاستثناء أعلاه...".

### `print_translated_exception` (2)

21. `test_print_writes_to_stderr_by_default`: trigger a `ZeroDivisionError`, call `print_translated_exception(*sys.exc_info())`, capture stderr, assert Arabic content present.
22. `test_print_accepts_custom_file`: pass a `StringIO`, assert it receives the output and `sys.stderr` does not.

### `install_excepthook` / `uninstall_excepthook` (4)

23. `test_install_replaces_excepthook`: after `install_excepthook()`, `sys.excepthook is print_translated_exception`.
24. `test_install_is_idempotent`: call twice, the saved `_saved_excepthook` is the ORIGINAL (not our own hook).
25. `test_uninstall_restores_previous`: install, then uninstall, then `sys.excepthook` is back to its pre-install value.
26. `test_uninstall_idempotent`: calling uninstall without prior install does not raise. Use a fixture to snapshot/restore `sys.excepthook` per test.

### CLI integration (3)

27. `test_cli_runtime_error_shows_arabic(tmp_path, capsys)`: write `"x = 1 / 0\n"` to a `.apy` file, call `cli.main([str(f)])`, assert exit 1 and stderr contains `خطأ_القسمة_على_صفر` and `القسمة على صفر`.
28. `test_cli_name_error_shows_arabic(tmp_path, capsys)`: write `"undefined_var\n"`, assert stderr contains `خطأ_اسم` and `الاسم 'undefined_var' غير معرّف`.
29. `test_cli_unknown_exception_falls_through_to_english_message(tmp_path, capsys)`: write code that raises a custom exception with a unique message; assert the type name passes through (since `MyError` not in table) and the message is shown verbatim.

### REPL integration (2)

30. `test_repl_runtime_error_shows_arabic(monkeypatch, capsys)`: pipe `"١/٠\n"` through stdin to `run_repl(banner='', exit_msg='')`, assert stderr contains `خطأ_القسمة_على_صفر`.
31. `test_repl_name_error_shows_arabic(monkeypatch, capsys)`: pipe `"undefined_in_repl\n"`, assert Arabic NameError text.

### Class identity preservation (1)

32. `test_exception_class_identity_unchanged(tmp_path, capsys)`: write a `.apy` file that does `try: 1/0; except ZeroDivisionError: print("caught")` — assert exit 0 and stdout contains `caught`. Confirms our display translation does NOT replace the actual exception class (which would break user `except` clauses).

(32 tests total.)

## Reference materials

- `decisions/0001-architecture.md`, `decisions/0007-scope.md`
- Python `traceback` module: https://docs.python.org/3/library/traceback.html
- CPython `Lib/traceback.py` (look at `TracebackException.format` and `format_exception_only` for the structure we mirror): https://github.com/python/cpython/blob/main/Lib/traceback.py
- CPython exception messages live in C code (`Objects/exceptions.c`, `Python/errors.c`) and BUILTINS (`Python/bltinmodule.c`). The patterns above were collected by inspection of CPython 3.11/3.12/3.13 sources.

## Open questions for the planner

If during implementation you find:

- A message-text divergence between Python 3.11/3.12/3.13 for any pattern in the table (e.g., 3.12 added "Did you mean" suggestions and the regex needs adjustment) — flag with the diverging texts in the delivery note. Do NOT add per-version regexes silently; that's a planner call.
- A genuine ambiguity about how to handle exception chaining when one exception in the chain is a translatable type and another is not — pick a sensible default (translate per-frame, fall through individually) and document.

## Acceptance checklist

- [ ] `arabicpython/tracebacks.py` created with all listed public symbols.
- [ ] `dictionaries/exceptions-ar-v1.md` created listing all 38 type names and all message templates with their patterns.
- [ ] `arabicpython/cli.py` modified to use `print_translated_exception` at all three call sites + `install_excepthook` at top of `main`.
- [ ] `arabicpython/repl.py` modified to override `showtraceback`.
- [ ] `arabicpython/__init__.py` re-exports `format_translated_exception`, `install_excepthook`, `uninstall_excepthook`.
- [ ] `tests/test_tracebacks.py` created with all 32 tests.
- [ ] `pytest` (full suite, including all 284 prior tests) passes on Python 3.11, 3.12, 3.13.
- [ ] `ruff check .` clean; `black --check .` clean.
- [ ] No new dependencies in `pyproject.toml`.
- [ ] CI green across all 9 matrix cells.
- [ ] After installing locally, `apython -c "1/0"` shows an Arabic traceback.
- [ ] `specs/0009-translated-tracebacks-v1.delivery.md` written.

## Workflow for the implementer

1. Create branch `packet/0009-translated-tracebacks-v1` from `main`.
2. Implement `arabicpython/tracebacks.py` starting with the data tables. Write all 38 type names and ~30 templates verbatim from this spec — do NOT paraphrase.
3. Implement `translate_exception_name`, `translate_exception_message`, and the lookup-only tests (1-15). Get those green first.
4. Implement `format_translated_exception` and the formatting tests (16-22).
5. Implement `install_excepthook` / `uninstall_excepthook` and tests 23-26.
6. Wire CLI and REPL integration. Get tests 27-32 passing.
7. Write `dictionaries/exceptions-ar-v1.md` as a faithful human-readable mirror of the runtime tables.
8. Run `pytest` (full suite) until green.
9. Run `ruff check .` and `black --check .` until clean. **Do not push without running both.**
10. Optionally `pip install -e .` and run `apython -c "1/0"` and `apython` (REPL) → trigger a few errors → confirm Arabic output by eye.
11. Commit using **explicit `git add <file>`** per file (not `git add .`). Suggested message: `Packet 0009: implement translated tracebacks`.
12. Push.
13. Write `specs/0009-translated-tracebacks-v1.delivery.md`.
14. Open a PR titled `Packet 0009: translated-tracebacks-v1` linking back to this spec.
15. Wait for CI green, then planner review.

## Allowed edit scope

- `arabicpython/tracebacks.py` (new)
- `dictionaries/exceptions-ar-v1.md` (new)
- `arabicpython/cli.py` (replace 3 traceback.print_exc call sites; add 1 install_excepthook call)
- `arabicpython/repl.py` (override showtraceback)
- `arabicpython/__init__.py` (re-exports)
- `tests/test_tracebacks.py` (new)
- `specs/0009-translated-tracebacks-v1.delivery.md` (new)

Do NOT modify: any other module, any ADR, the `ar-v1.md` dictionary, `pyproject.toml`, the CI workflow, or any other existing tests. If you believe the spec has a bug, flag it in the delivery note rather than silently deviating.
