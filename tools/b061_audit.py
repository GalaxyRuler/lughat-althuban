"""
B-061 audit script: test real CPython error messages against translate_exception_message().
Collects misses (untranslated messages) and reports coverage.
"""

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, ".")
from arabicpython.tracebacks import translate_exception_message

hits = []
misses_list = []


def check(desc: str, msg: str) -> bool:
    result = translate_exception_message(msg)
    translated = result != msg
    if translated:
        hits.append((desc, msg, result))
    else:
        misses_list.append((desc, msg))
    return translated


# ── ZeroDivisionError ─────────────────────────────────────────────────────────
check("ZDE/basic", "division by zero")
check("ZDE/int", "integer division or modulo by zero")
check("ZDE/float", "float division by zero")
check("ZDE/float-modulo", "float modulo")
check("ZDE/complex", "complex division by zero")

# ── NameError ────────────────────────────────────────────────────────────────
check("NE/basic", "name 'foo' is not defined")
check("NE/suggest", "name 'foo' is not defined. Did you mean: 'for'?")

# ── AttributeError ───────────────────────────────────────────────────────────
check("AE/basic", "'list' object has no attribute 'push'")
check("AE/suggest", "'list' object has no attribute 'push'. Did you mean: 'pop'?")
check("AE/module", "module 'os' has no attribute 'pathh'")
check("AE/module-suggest", "module 'os' has no attribute 'pathh'. Did you mean: 'path'?")

# ── TypeError ────────────────────────────────────────────────────────────────
check("TE/not-subscriptable", "'int' object is not subscriptable")
check("TE/not-callable", "'int' object is not callable")
check("TE/not-iterable", "'int' object is not iterable")
check("TE/arg-not-iterable", "argument of type 'int' is not iterable")
check("TE/no-len", "object of type 'int' has no len()")
check("TE/unhashable", "unhashable type: 'list'")
check("TE/not-iterator", "'list' object is not an iterator")
check("TE/bytes-like", "a bytes-like object is required, not 'str'")
check("TE/operand", "unsupported operand type(s) for +: 'int' and 'str'")
check("TE/concat", 'can only concatenate str (not "int") to str')
check("TE/int-interpret", "'str' object cannot be interpreted as an integer")
check("TE/list-indices", "list indices must be integers or slices, not str")
check("TE/tuple-indices", "tuple indices must be integers or slices, not str")
check("TE/string-indices", "string indices must be integers")
check("TE/string-indices-not", "string indices must be integers, not 'str'")
check("TE/seq-item", "sequence item 0: expected str instance, int found")
check("TE/takes-pos", "foo() takes 1 positional argument but 2 were given")
check("TE/missing-pos", "foo() missing 1 required positional argument: 'x'")
check("TE/unexpected-kw", "foo() got an unexpected keyword argument 'z'")
check("TE/multiple-values", "foo() got multiple values for argument 'x'")
check("TE/bad-unary", "bad operand type for unary -: 'str'")
check("TE/no-item-assign", "'tuple' object does not support item assignment")
check("TE/no-item-delete", "'tuple' object doesn't support item deletion")
check("TE/cant-multiply", "can't multiply sequence by non-int of type 'float'")
check("TE/str-not", "expected str, bytes or os.PathLike object, not int")
check(
    "TE/descriptor",
    "descriptor 'append' for 'list' objects doesn't apply to a 'tuple' object",
)

# ── ValueError ───────────────────────────────────────────────────────────────
check("VE/invalid-int", "invalid literal for int() with base 10: 'abc'")
check("VE/no-float", "could not convert string to float: 'abc'")
check("VE/too-many-unpack", "too many values to unpack (expected 2)")
check("VE/too-few-unpack", "not enough values to unpack (expected 2, got 1)")
check("VE/math-domain", "math domain error")
check("VE/substring", "substring not found")
check("VE/list-remove", "list.remove(x): x not found")
check("VE/closed-file", "I/O operation on closed file.")
check("VE/json-circular", "Circular reference detected")
check("VE/empty-separator", "empty separator")
check(
    "VE/dict-update-seq",
    "dictionary update sequence element #0 has length 3; 2 is required",
)

# ── IndexError ───────────────────────────────────────────────────────────────
check("IE/list", "list index out of range")
check("IE/tuple", "tuple index out of range")
check("IE/string", "string index out of range")
check("IE/pop", "pop index out of range")
check("IE/bytearray", "bytearray index out of range")
check("IE/range", "range object index out of range")

# ── KeyError ─────────────────────────────────────────────────────────────────
check("KE/str", "'missing_key'")

# ── ImportError ──────────────────────────────────────────────────────────────
check("ImE/no-module", "No module named 'foo'")
check("ImE/no-name", "cannot import name 'Bar' from 'foo' (/path/to/foo.py)")
check("ImE/relative", "attempted relative import with no known parent package")
check(
    "ImE/partial-init",
    "cannot import name 'Bar' from partially initialized module 'foo' "
    "(most likely due to a circular import) (/path/to/foo.py)",
)

# ── OverflowError ────────────────────────────────────────────────────────────
check("OFE/math-range", "math range error")
check("OFE/int-float", "int too large to convert to float")
check("OFE/result-large", "(34, 'Result too large')")

# ── RecursionError ───────────────────────────────────────────────────────────
check("RE/basic", "maximum recursion depth exceeded")
check("RE/compare", "maximum recursion depth exceeded in comparison")

# ── RuntimeError ─────────────────────────────────────────────────────────────
check("RTE/gen-exec", "generator already executing")
check("RTE/coro-exec", "coroutine already executing")
check("RTE/dict-changed", "dictionary changed size during iteration")
check("RTE/set-changed", "Set changed size during iteration")
check("RTE/async-gen", "asynchronous generator raised StopIteration")

# ── SyntaxError ──────────────────────────────────────────────────────────────
check("SE/invalid-syntax", "invalid syntax")
check("SE/invalid-syntax-comma", "invalid syntax. Perhaps you forgot a comma?")
check("SE/unterminated-str", "unterminated string literal (detected at line 1)")
check("SE/EOL-string", "EOL while scanning string literal")
check("SE/EOF-parsing", "unexpected EOF while parsing")
check("SE/line-cont", "unexpected character after line continuation character")
check("SE/invalid-char", "invalid character '،' (U+060C)")
check("SE/indented-block", "expected an indented block")
check("SE/tabs-spaces", "inconsistent use of tabs and spaces in indentation")
check("SE/unindent", "unindent does not match any outer indentation level")
check("SE/missing-parens", "Missing parentheses in call to 'print'. Did you mean print(...)?")
check("SE/f-string-expr", "f-string expression part cannot include a backslash")

# ── StopIteration ─────────────────────────────────────────────────────────────
check("SI/coro", "coroutine raised StopIteration")

# ── UnboundLocalError ─────────────────────────────────────────────────────────
check("ULE/ref-before", "local variable 'x' referenced before assignment")
check("ULE/no-value", "cannot access local variable 'x' where it is not associated with a value")
check("ULE/free-var", "free variable 'x' referenced before assignment in enclosing scope")

# ── OSError / FileNotFoundError ───────────────────────────────────────────────
check("OSE/errno-path", "[Errno 2] No such file or directory: '/tmp/x'")
check("OSE/errno", "[Errno 13] Permission denied")
check("OSE/winerror", "[WinError 2] The system cannot find the file specified")

# ── Connection errors ─────────────────────────────────────────────────────────
check("CE/refused", "Connection refused")
check("CE/reset", "Connection reset by peer")
check("CE/pipe", "Broken pipe")
check("CE/timeout", "Connection timed out")
check("CE/timed-out", "timed out")

# ── Unicode errors ────────────────────────────────────────────────────────────
check(
    "UCE/decode-byte",
    "'utf-8' codec can't decode byte 0xff in position 0: invalid start byte",
)
check(
    "UCE/decode-range",
    "'utf-8' codec can't decode bytes in position 0-1: invalid continuation byte",
)
check(
    "UCE/encode-char",
    "'ascii' codec can't encode character '\\u0041' in position 0: ordinal not in range(128)",
)
check(
    "UCE/encode-range",
    "'ascii' codec can't encode characters in position 0-3: ordinal not in range(128)",
)

# ── Report ───────────────────────────────────────────────────────────────────
total = len(hits) + len(misses_list)
print(f"\n{'='*64}")
print("تقرير تغطية رسائل الأخطاء (B-061)")
print(f"{'='*64}")
print(f"المجموع  : {total}")
print(f"مغطى     : {len(hits)}  ({len(hits)/total*100:.1f}%)")
print(f"ثغرات    : {len(misses_list)}  ({len(misses_list)/total*100:.1f}%)")
print()
print("الثغرات:")
for desc, msg in misses_list:
    print(f"  ❌  [{desc}]  {msg!r}")
