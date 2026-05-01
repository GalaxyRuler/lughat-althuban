"""Pre-process Arabic Python source for Python's tokenizer."""

import re
import unicodedata

from arabicpython.messages import msg

_BIDI_CONTROLS = frozenset(
    "\u061c"  # ARABIC LETTER MARK (ALM)
    "\u200e"  # LEFT-TO-RIGHT MARK (LRM)
    "\u200f"  # RIGHT-TO-LEFT MARK (RLM)
    "\u202a\u202b\u202c\u202d\u202e"  # LRE, RLE, PDF, LRO, RLO
    "\u2066\u2067\u2068\u2069"  # LRI, RLI, FSI, PDI
)
_ASCII_DIGITS = frozenset("0123456789")
_ARABIC_INDIC_DIGITS = frozenset("٠١٢٣٤٥٦٧٨٩")
_EASTERN_ARABIC_INDIC_DIGITS = frozenset("۰۱۲۳۴۵۶۷۸۹")
_ALL_DIGITS = _ASCII_DIGITS | _ARABIC_INDIC_DIGITS | _EASTERN_ARABIC_INDIC_DIGITS
_DIGIT_SYSTEM_NAMES_AR = {
    "ASCII": "الأرقام اللاتينية",
    "Arabic-Indic": "الأرقام العربية الهندية",
    "Eastern Arabic-Indic": "الأرقام العربية الهندية الشرقية",
}

# Single compiled regex that matches any character pretokenize needs to act on.
# If this pattern does not match anywhere in the source, the source can be
# returned unchanged immediately (skipping the full O(n) Python char-loop).
# Covers: Arabic-Indic digits (U+0660–U+0669), Eastern Arabic-Indic digits
# (U+06F0–U+06F9), Arabic punctuation (،؛؟), and all 12 BiDi control chars.
_PRETOKENIZE_TRIGGER = re.compile(r"[٠-٩۰-۹،؛؟" r"؜‎‏‪-‮⁦-⁩]")

# Arabic escape sequences: \س → \n, \ج → \t, etc.
_ARABIC_ESCAPE = {
    "س": "n",  # newline
    "ج": "t",  # tab
    "ر": "r",  # carriage return
    "م": "b",  # backspace
    "ف": "f",  # form feed
    "ع": "v",  # vertical tab
    "ن": "a",  # alert/bell
}

# Arabic numeric literal prefixes: 0س → 0x (hex), 0ث → 0b (binary), 0ذ → 0o (octal)
_ARABIC_NUM_PREFIX = {
    "س": "x",  # سِتَّة عشر (hexadecimal)
    "ث": "b",  # ثنائي (binary)
    "ذ": "o",  # ذو ثمانية (octal)
}

# Arabic string type prefixes: ت"..." → f"...", ب"..." → b"...", خ"..." → r"...", ي"..." → u"..."
_ARABIC_STR_PREFIX = {
    "ت": "f",  # تنسيق (format)
    "ب": "b",  # بايت (bytes)
    "خ": "r",  # خام (raw)
    "ي": "u",  # يونيكود (unicode)
}
# Two-letter combinations (e.g., raw-format, raw-bytes)
_ARABIC_STR_PREFIX_2 = {
    "خت": "rf",
    "تخ": "fr",
    "خب": "rb",
    "بخ": "br",
}
_ARABIC_STR_PREFIX_CHARS = frozenset("تبخي")

# Supplemental triggers for the new Arabic-ification features.
# These are checked in addition to _PRETOKENIZE_TRIGGER.
_STR_PREFIX_TRIGGER = re.compile(r"(?:خت|تخ|خب|بخ|[تبخي])['\"]")
_ESCAPE_TRIGGER = re.compile(r"\\[سجرمفعن]")
_NUM_PREFIX_TRIGGER = re.compile(r"0[سثذ]")

_PUNCTUATION_TRANSLATE = str.maketrans(
    {
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "،": ",",
        "؛": ";",
        "؟": "?",
    }
)


def pretokenize(source: str) -> str:
    """Pre-process Arabic Python source for Python's tokenizer.

    Performs three transformations during a single left-to-right walk:

    1. Outside string literals: replace U+0660-U+0669 (Arabic-Indic digits)
       and U+06F0-U+06F9 (Eastern Arabic-Indic digits) with the corresponding
       ASCII digits 0-9.
    2. Outside string literals: replace U+060C (،) with U+002C (,),
       U+061B (؛) with U+003B (;), U+061F (؟) with U+003F (?).
    3. Outside string literals: raise SyntaxError if any of the 12 bidi
       formatting characters from UAX #9 is encountered — U+061C (ALM),
       U+200E (LRM), U+200F (RLM), U+202A-U+202E (LRE/RLE/PDF/LRO/RLO),
       U+2066-U+2069 (LRI/RLI/FSI/PDI). Inside string literals these pass
       through unchanged. Per ADR 0009 (which supersedes ADR 0006's
       narrower 9-codepoint reject set).

    Single-line and multi-line string literals (', ", ''', \"\"\") and string
    prefixes (r, b, u, f, and case-insensitive combinations) are recognized.
    String contents are preserved byte-for-byte.

    Comments (# ... newline) are NOT string literals: substitutions apply and
    bidi controls are rejected (per ADR 0006: comments are an attack vector,
    not a safe haven).

    A run of consecutive digit characters that mixes digit systems (e.g.,
    `١2` mixing Arabic-Indic and ASCII) raises SyntaxError. Pure-system runs
    are folded to ASCII; pure-ASCII runs pass through unchanged.

    Args:
        source: the .apy source text.

    Returns:
        Source text with the substitutions applied.

    Raises:
        SyntaxError: with the exact format from ADR 0006 for bidi controls,
            or a clear message naming the offending characters and line/column
            for mixed-digit literals.
    """
    # Fast path: if none of the characters pretokenize cares about appear in the
    # source at all, return immediately.  The regex runs in C and short-circuits
    # at the first hit, so for clean sources this is much faster than the Python
    # char-loop below.
    if (
        not _PRETOKENIZE_TRIGGER.search(source)
        and not _STR_PREFIX_TRIGGER.search(source)
        and not _ESCAPE_TRIGGER.search(source)
        and not _NUM_PREFIX_TRIGGER.search(source)
    ):
        return source

    state = "DEFAULT"
    out = []
    line = 1
    col = 0
    i = 0
    n = len(source)

    escape_next = False

    while i < n:
        ch = source[i]

        if escape_next:
            # Translate Arabic escape letters to their ASCII equivalents.
            out.append(_ARABIC_ESCAPE.get(ch, ch))
            escape_next = False
            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        if state == "DEFAULT":
            if ch in _BIDI_CONTROLS:
                name = unicodedata.name(ch, "UNKNOWN")
                code = f"U+{ord(ch):04X}"
                raise SyntaxError(
                    f"{msg('pretokenize.bidi_control')}: {code} ({name})، "
                    f"السطر {line}، العمود {col}. {msg('pretokenize.bidi_reason')}."
                )

            if ch == "#":
                state = "COMMENT"
                out.append(ch)
                col += 1
                i += 1
                continue

            # Arabic string type prefix: ت/ب/خ/ي (or two-letter combo) before a quote.
            if ch in _ARABIC_STR_PREFIX_CHARS and i + 1 < n:
                # Check two-letter combo first.
                two = source[i : i + 2]
                if two in _ARABIC_STR_PREFIX_2 and i + 2 < n and source[i + 2] in ("'", '"'):
                    out.append(_ARABIC_STR_PREFIX_2[two])
                    col += 2
                    i += 2
                    ch = source[i]
                    # fall through to quote handling below
                elif source[i + 1] in ("'", '"'):
                    out.append(_ARABIC_STR_PREFIX[ch])
                    col += 1
                    i += 1
                    ch = source[i]
                    # fall through to quote handling below
                # else: Arabic letter not followed by a quote — normal char, fall through

            if ch in ("'", '"'):
                if source[i : i + 3] == "'''":
                    state = "STRING_TSQ"
                    out.append("'''")
                    col += 3
                    i += 3
                    continue
                elif source[i : i + 3] == '"""':
                    state = "STRING_TDQ"
                    out.append('"""')
                    col += 3
                    i += 3
                    continue
                else:
                    state = "STRING_SQ" if ch == "'" else "STRING_DQ"
                    out.append(ch)
                    col += 1
                    i += 1
                    continue

            # Arabic numeric literal prefix: 0س → 0x, 0ث → 0b, 0ذ → 0o
            if ch == "0" and i + 1 < n and source[i + 1] in _ARABIC_NUM_PREFIX:
                out.append("0")
                out.append(_ARABIC_NUM_PREFIX[source[i + 1]])
                col += 2
                i += 2
                continue

            if ch in _ALL_DIGITS:
                start_i = i
                while i < n and source[i] in _ALL_DIGITS:
                    i += 1
                run = source[start_i:i]
                sys_names = []
                if any(c in _ASCII_DIGITS for c in run):
                    sys_names.append(_DIGIT_SYSTEM_NAMES_AR["ASCII"])
                if any(c in _ARABIC_INDIC_DIGITS for c in run):
                    sys_names.append(_DIGIT_SYSTEM_NAMES_AR["Arabic-Indic"])
                if any(c in _EASTERN_ARABIC_INDIC_DIGITS for c in run):
                    sys_names.append(_DIGIT_SYSTEM_NAMES_AR["Eastern Arabic-Indic"])

                if len(sys_names) > 1:
                    if len(sys_names) == 2:
                        sys_str = f"{sys_names[0]} و{sys_names[1]}"
                    else:
                        sys_str = "، ".join(sys_names[:-1]) + f"، و{sys_names[-1]}"
                    raise SyntaxError(
                        f"{msg('pretokenize.mixed_digits')}: السطر {line}، العمود {col}؛ "
                        f"وجدت {sys_str} في '{run}'. {msg('pretokenize.one_digit_system')}."
                    )

                translated = run.translate(_PUNCTUATION_TRANSLATE)
                out.append(translated)
                col += len(run)
                continue

            # Normal char
            out.append(ch.translate(_PUNCTUATION_TRANSLATE))
            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        elif state == "COMMENT":
            if ch in _BIDI_CONTROLS:
                name = unicodedata.name(ch, "UNKNOWN")
                code = f"U+{ord(ch):04X}"
                raise SyntaxError(
                    f"{msg('pretokenize.bidi_control')}: {code} ({name})، "
                    f"السطر {line}، العمود {col}. {msg('pretokenize.bidi_reason')}."
                )
            out.append(ch.translate(_PUNCTUATION_TRANSLATE))
            if ch == "\n":
                state = "DEFAULT"
                line += 1
                col = 0
            else:
                col += 1
            i += 1
            continue

        elif state.startswith("STRING_"):
            out.append(ch)
            if ch == "\\":
                escape_next = True
                col += 1
                i += 1
                continue

            if state == "STRING_SQ" and ch == "'" or state == "STRING_DQ" and ch == '"':
                state = "DEFAULT"
            elif state == "STRING_TSQ" and ch == "'":
                if source[i : i + 3] == "'''":
                    out.append("''")
                    col += 3
                    i += 3
                    state = "DEFAULT"
                    continue
            elif state == "STRING_TDQ" and ch == '"' and source[i : i + 3] == '"""':
                out.append('""')
                col += 3
                i += 3
                state = "DEFAULT"
                continue

            if ch == "\n":
                line += 1
                col = 0
            else:
                col += 1
            i += 1

    return "".join(out)
