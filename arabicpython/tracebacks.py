"""Translated tracebacks for Arabic Python."""

import re
import sys
import traceback
import types
from typing import IO, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any


# --- Translation tables (data) ---

EXCEPTION_NAMES_AR: dict[str, str] = {
    # ── Base hierarchy ────────────────────────────────────────────────────────
    "BaseException": "استثناء_اساسي",
    "Exception": "استثناء",
    "GeneratorExit": "خروج_مولد",
    "KeyboardInterrupt": "مقاطعه_لوحه_المفاتيح",
    "SystemExit": "خروج_نظام",
    # ── Arithmetic ────────────────────────────────────────────────────────────
    "ArithmeticError": "خطا_حسابي",
    "FloatingPointError": "خطا_فاصله_عائمه",
    "OverflowError": "خطا_فيضان",
    "ZeroDivisionError": "خطا_القسمه_على_صفر",
    # ── Assertion / attribute / name ──────────────────────────────────────────
    "AssertionError": "خطا_تاكيد",
    "AttributeError": "خطا_خاصيه",
    "NameError": "خطا_اسم",
    "UnboundLocalError": "خطا_متغير_غير_مرتبط",
    # ── Buffer ────────────────────────────────────────────────────────────────
    "BufferError": "خطا_مخزن_مؤقت",
    # ── EOF ───────────────────────────────────────────────────────────────────
    "EOFError": "خطا_نهايه_الملف",
    # ── Import ────────────────────────────────────────────────────────────────
    "ImportError": "خطا_استيراد",
    "ModuleNotFoundError": "خطا_الوحده_غير_موجوده",
    # ── Lookup ────────────────────────────────────────────────────────────────
    "LookupError": "خطا_بحث",
    "IndexError": "خطا_فهرس",
    "KeyError": "خطا_مفتاح",
    # ── Memory ───────────────────────────────────────────────────────────────
    "MemoryError": "خطا_ذاكره",
    # ── OS / IO errors ────────────────────────────────────────────────────────
    "OSError": "خطا_نظام",
    "EnvironmentError": "خطا_بيئه",  # alias for OSError in Python 3
    "IOError": "خطا_ادخال_اخراج",  # alias for OSError in Python 3
    "BlockingIOError": "خطا_ادخال_اخراج_حاجب",
    "ChildProcessError": "خطا_عمليه_فرعيه",
    "ConnectionError": "خطا_اتصال",
    "BrokenPipeError": "خطا_انبوب_مكسور",
    "ConnectionAbortedError": "خطا_اتصال_ملغي",
    "ConnectionRefusedError": "خطا_اتصال_مرفوض",
    "ConnectionResetError": "خطا_اتصال_منقطع",
    "FileExistsError": "خطا_الملف_موجود",
    "FileNotFoundError": "خطا_الملف_غير_موجود",
    "InterruptedError": "خطا_مقاطعه",
    "IsADirectoryError": "خطا_هذا_مجلد",
    "NotADirectoryError": "خطا_ليس_مجلدا",
    "PermissionError": "خطا_صلاحيات",
    "ProcessLookupError": "خطا_بحث_عمليه",
    "TimeoutError": "خطا_انتهاء_مهله",
    # ── Reference ────────────────────────────────────────────────────────────
    "ReferenceError": "خطا_مرجع",
    # ── Runtime ──────────────────────────────────────────────────────────────
    "RuntimeError": "خطا_تشغيل",
    "NotImplementedError": "خطا_غير_منفذ",
    "RecursionError": "خطا_عوديه",
    "SystemError": "خطا_نظام_داخلي",
    # ── StopIteration ────────────────────────────────────────────────────────
    "StopIteration": "ايقاف_التكرار",
    "StopAsyncIteration": "ايقاف_التكرار_المتزامن",
    # ── Syntax ───────────────────────────────────────────────────────────────
    "SyntaxError": "خطا_صياغه",
    "IndentationError": "خطا_ازاحه",
    "TabError": "خطا_تبويب",
    # ── Type ─────────────────────────────────────────────────────────────────
    "TypeError": "خطا_نوع",
    # ── Unicode ──────────────────────────────────────────────────────────────
    "UnicodeError": "خطا_يونيكود",
    "UnicodeDecodeError": "خطا_فك_يونيكود",
    "UnicodeEncodeError": "خطا_ترميز_يونيكود",
    "UnicodeTranslateError": "خطا_ترجمه_يونيكود",
    # ── Value ────────────────────────────────────────────────────────────────
    "ValueError": "خطا_قيمه",
    # ── Warning hierarchy ────────────────────────────────────────────────────
    "Warning": "تحذير",
    "BytesWarning": "تحذير_بايت",
    "DeprecationWarning": "تحذير_اهمال",
    "EncodingWarning": "تحذير_ترميز",
    "FutureWarning": "تحذير_مستقبلي",
    "ImportWarning": "تحذير_استيراد",
    "PendingDeprecationWarning": "تحذير_اهمال_قادم",
    "ResourceWarning": "تحذير_موارد",
    "RuntimeWarning": "تحذير_تشغيل",
    "SyntaxWarning": "تحذير_صياغه",
    "UnicodeWarning": "تحذير_يونيكود",
    "UserWarning": "تحذير_مستخدم",
    # ── Exception groups (Python 3.11+) ──────────────────────────────────────
    "BaseExceptionGroup": "مجموعه_استثنائات_اساسيه",
    "ExceptionGroup": "مجموعه_استثنائات",
}

# Each entry: (compiled_regex, arabic_template_with_named_groups)
MESSAGE_TEMPLATES_AR: list[tuple[re.Pattern, str]] = [
    (re.compile(r"^division by zero$"), "القسمة على صفر"),
    (re.compile(r"^integer division or modulo by zero$"), "قسمة صحيحة أو باقي على صفر"),
    (re.compile(r"^float division by zero$"), "قسمة عشرية على صفر"),
    (
        re.compile(r"^name '(?P<name>[^']+)' is not defined$"),
        "الاسم '{name}' غير معرّف",
    ),
    (
        re.compile(r"^name '(?P<name>[^']+)' is not defined\. Did you mean: '(?P<sugg>[^']+)'\?$"),
        "الاسم '{name}' غير معرّف. هل تقصد: '{sugg}'؟",
    ),
    (
        re.compile(
            r"^free variable '(?P<name>[^']+)' referenced before assignment in enclosing scope$"
        ),
        "المتغير الحر '{name}' مستخدم قبل تعريفه في النطاق المحيط",
    ),
    (
        re.compile(r"^local variable '(?P<name>[^']+)' referenced before assignment$"),
        "المتغير المحلي '{name}' مستخدم قبل تعريفه",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object has no attribute '(?P<attr>[^']+)'$"),
        "الكائن من نوع '{type}' لا يملك الخاصية '{attr}'",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object is not subscriptable$"),
        "الكائن من نوع '{type}' لا يقبل الفهرسة",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object is not callable$"),
        "الكائن من نوع '{type}' غير قابل للاستدعاء",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object is not iterable$"),
        "الكائن من نوع '{type}' غير قابل للتكرار",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object cannot be interpreted as an integer$"),
        "الكائن من نوع '{type}' لا يمكن تفسيره كعدد صحيح",
    ),
    (
        re.compile(r"^argument of type '(?P<type>[^']+)' is not iterable$"),
        "الوسيط من نوع '{type}' غير قابل للتكرار",
    ),
    (re.compile(r"^list index out of range$"), "فهرس القائمة خارج النطاق"),
    (re.compile(r"^tuple index out of range$"), "فهرس الصف خارج النطاق"),
    (re.compile(r"^string index out of range$"), "فهرس النص خارج النطاق"),
    (re.compile(r"^pop from empty list$"), "إخراج من قائمة فارغة"),
    (re.compile(r"^pop from an empty (set|deque|dict)$"), "إخراج من {1} فارغ"),
    (
        re.compile(r"^maximum recursion depth exceeded(?P<rest>.*)$"),
        "تم تجاوز عمق العودية الأقصى{rest}",
    ),
    (re.compile(r"^No module named '(?P<name>[^']+)'$"), "لا توجد وحدة باسم '{name}'"),
    (
        re.compile(r"^cannot import name '(?P<name>[^']+)' from '(?P<module>[^']+)'(?P<rest>.*)$"),
        "لا يمكن استيراد الاسم '{name}' من '{module}'{rest}",
    ),
    (
        re.compile(
            r"^unsupported operand type\(s\) for (?P<op>\S+): "
            r"'(?P<a>[^']+)' and '(?P<b>[^']+)'$"
        ),
        "أنواع المعاملات غير مدعومة لـ {op}: '{a}' و '{b}'",
    ),
    (
        re.compile(r"^can only concatenate (?P<a>\w+) \(not \"(?P<b>\w+)\"\) to \w+$"),
        "يمكن فقط ضم {a} (لا {b}) إلى {a}",
    ),
    (
        re.compile(r"^invalid literal for int\(\) with base (?P<base>\d+): '(?P<val>[^']*)'$"),
        "قيمة غير صالحة للدالة int() بالأساس {base}: '{val}'",
    ),
    (
        re.compile(r"^could not convert string to float: '(?P<val>[^']*)'$"),
        "تعذر تحويل النص إلى عدد عشري: '{val}'",
    ),
    (
        re.compile(
            r"^expected (?P<n>\d+) "
            r"(?P<arg_kind>positional argument|positional arguments), got (?P<got>\d+)$"
        ),
        "كان متوقعا {n} {arg_kind} لكن تم تمرير {got}",
    ),
    (
        re.compile(
            r"^(?P<func>\w+)\(\) missing (?P<n>\d+) "
            r"required positional argument(?P<plural>s?): (?P<rest>.+)$"
        ),
        "{func}() ينقصها {n} وسيط إجباري{plural}: {rest}",
    ),
    (
        re.compile(r"^(?P<func>\w+)\(\) got an unexpected keyword argument '(?P<name>[^']+)'$"),
        "{func}() استلمت وسيطا مفتاحيا غير متوقع '{name}'",
    ),
    (
        re.compile(r"^\[Errno (?P<errno>\d+)\] (?P<msg>[^:]+): '(?P<path>.+)'$"),
        "[رقم الخطأ {errno}] {msg}: '{path}'",
    ),
    # OSError without a path
    (
        re.compile(r"^\[Errno (?P<errno>\d+)\] (?P<msg>.+)$"),
        "[رقم الخطأ {errno}] {msg}",
    ),
    # Windows OSError format
    (
        re.compile(r"^\[WinError (?P<errno>\d+)\] (?P<msg>.+)$"),
        "[خطأ ويندوز {errno}] {msg}",
    ),
    # ── TypeError variants ────────────────────────────────────────────────────
    (
        re.compile(r"^list indices must be integers or slices, not (?P<type>\w+)$"),
        "فهارس القائمة يجب أن تكون أعداداً صحيحة أو شرائح، لا '{type}'",
    ),
    (
        re.compile(r"^tuple indices must be integers or slices, not (?P<type>\w+)$"),
        "فهارس الصف يجب أن تكون أعداداً صحيحة أو شرائح، لا '{type}'",
    ),
    (
        re.compile(r"^string indices must be integers(?:, not '(?P<type>[^']+)')?$"),
        "فهارس النص يجب أن تكون أعداداً صحيحة",
    ),
    (
        re.compile(r"^object of type '(?P<type>[^']+)' has no len\(\)$"),
        "الكائن من نوع '{type}' لا يملك دالة len()",
    ),
    (
        re.compile(r"^unhashable type: '(?P<type>[^']+)'$"),
        "النوع '{type}' غير قابل للتجزئة",
    ),
    (
        re.compile(r"^'(?P<type>[^']+)' object is not an iterator$"),
        "الكائن من نوع '{type}' ليس مكرراً",
    ),
    (
        re.compile(r"^a bytes-like object is required, not '(?P<type>[^']+)'$"),
        "مطلوب كائن من نوع bytes، لا '{type}'",
    ),
    (
        re.compile(
            r"^(?P<func>\w+)\(\) takes (?P<n>\d+) positional argument(?P<plural>s?) "
            r"but (?P<got>\d+) (?:were|was) given$"
        ),
        "{func}() تأخذ {n} وسيط موضعي{plural} لكن تم تمرير {got}",
    ),
    (
        re.compile(r"^sequence item (?P<n>\d+): expected str instance, (?P<got>\w+) found$"),
        "عنصر المتسلسلة {n}: متوقع نص، وجد {got}",
    ),
    # ── UnboundLocalError (Python 3.12+ message) ──────────────────────────────
    (
        re.compile(
            r"^cannot access local variable '(?P<name>[^']+)' "
            r"where it is not associated with a value$"
        ),
        "لا يمكن الوصول إلى المتغير المحلي '{name}' لأنه غير مرتبط بقيمة",
    ),
    # ── AttributeError with suggestion ───────────────────────────────────────
    (
        re.compile(
            r"^'(?P<type>[^']+)' object has no attribute '(?P<attr>[^']+)'\. "
            r"Did you mean: '(?P<sugg>[^']+)'\?$"
        ),
        "الكائن من نوع '{type}' لا يملك الخاصية '{attr}'. هل تقصد: '{sugg}'؟",
    ),
    # ── ValueError variants ───────────────────────────────────────────────────
    (
        re.compile(r"^too many values to unpack \(expected (?P<n>\d+)\)$"),
        "قيم كثيرة جداً للتفريغ (متوقع {n})",
    ),
    (
        re.compile(r"^not enough values to unpack \(expected (?P<n>\d+), got (?P<got>\d+)\)$"),
        "قيم غير كافية للتفريغ (متوقع {n}، حصلنا على {got})",
    ),
    (
        re.compile(r"^math domain error$"),
        "خطأ في نطاق الرياضيات",
    ),
    # ── OverflowError ─────────────────────────────────────────────────────────
    (
        re.compile(r"^math range error$"),
        "خطأ في مجال الرياضيات",
    ),
    (
        re.compile(r"^int too large to convert to float$"),
        "العدد الصحيح كبير جداً للتحويل إلى عشري",
    ),
    # ── RuntimeError variants ─────────────────────────────────────────────────
    (
        re.compile(r"^generator already executing$"),
        "المولّد قيد التنفيذ بالفعل",
    ),
    (
        re.compile(r"^coroutine already executing$"),
        "الكوروتين قيد التنفيذ بالفعل",
    ),
    # ── SyntaxError / IndentationError messages ───────────────────────────────
    (
        re.compile(r"^expected an indented block(?P<rest>.*)$"),
        "متوقع كتلة مزاحة{rest}",
    ),
    (
        re.compile(r"^inconsistent use of tabs and spaces in indentation$"),
        "استخدام غير متسق للجداول والمسافات في الإزاحة",
    ),
    (
        re.compile(r"^unindent does not match any outer indentation level$"),
        "الإزاحة لا تطابق أي مستوى خارجي",
    ),
    # ── StopIteration / StopAsyncIteration ───────────────────────────────────
    (
        re.compile(r"^coroutine raised StopIteration$"),
        "الكوروتين أطلق ايقاف_التكرار",
    ),
    # ── Connection errors ─────────────────────────────────────────────────────
    (
        re.compile(r"^Connection refused$"),
        "رُفض الاتصال",
    ),
    (
        re.compile(r"^Connection reset by peer$"),
        "أعاد الطرف الآخر ضبط الاتصال",
    ),
    (
        re.compile(r"^Broken pipe$"),
        "الأنبوب معطوب",
    ),
]


# --- Public API ---


def translate_exception_name(name: str) -> str:
    """Look up the Arabic display name for an exception class.

    Returns the original name if no translation exists.
    """
    return EXCEPTION_NAMES_AR.get(name, name)


def translate_exception_message(message: str) -> str:
    """Translate a CPython interpreter-level exception message to Arabic.

    Walks MESSAGE_TEMPLATES_AR; on first regex match, formats the Arabic
    template with the named groups from the match. Returns the original
    message if no template matches.
    """
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
                type(exc_value.__cause__), exc_value.__cause__, exc_value.__cause__.__traceback__
            )
        )
        blocks.append("\nالسبب المباشر للاستثناء أعلاه:\n\n")
    elif exc_value.__context__ is not None and not exc_value.__suppress_context__:
        blocks.append(
            format_translated_exception(
                type(exc_value.__context__),
                exc_value.__context__,
                exc_value.__context__.__traceback__,
            )
        )
        blocks.append("\nأثناء معالجة الاستثناء أعلاه, حدث استثناء آخر:\n\n")

    current_blocks = []
    current_blocks.append("تتبع_الأخطاء (المكدس الأحدث آخرا):\n")

    if exc_tb:
        for frame in traceback.extract_tb(exc_tb):
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
    message = translate_exception_message(str(exc_value))

    current_blocks.append(f"{type_name}: {message}\n")

    blocks.append("".join(current_blocks))
    return "".join(blocks)


def print_translated_exception(
    exc_type: type[BaseException],
    exc_value: BaseException,
    exc_tb: "types.TracebackType | None",
    file: "IO[str] | None" = None,
) -> None:
    """Format and write the traceback to `file` (default sys.stderr)."""
    if file is None:
        file = sys.stderr
    file.write(format_translated_exception(exc_type, exc_value, exc_tb))


_saved_excepthook = None


def install_excepthook() -> None:
    """Set sys.excepthook to print_translated_exception.

    Idempotent: calling install_excepthook() twice does not re-install. The
    previous excepthook is saved at module level so uninstall() can restore it.
    """
    global _saved_excepthook
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
