import pytest

from arabicpython.pretokenize import pretokenize


# Basic passthrough (5)
def test_empty_string():
    assert pretokenize("") == ""


def test_pure_ascii_passthrough():
    src = "x = 1\nprint(x)\n"
    assert pretokenize(src) == src


def test_arabic_identifier_passthrough():
    src = "اسم = 1\n"
    assert pretokenize(src) == src


def test_keyword_chars_passthrough():
    src = "def foo():\n    pass\n"
    assert pretokenize(src) == src


def test_only_whitespace_passthrough():
    src = "   \n\t\n  "
    assert pretokenize(src) == src


# Arabic-Indic digit folding (5)
def test_single_arabic_indic_digit():
    assert pretokenize("x = ٥") == "x = 5"


def test_multi_digit_arabic_indic():
    assert pretokenize("x = ١٢٣") == "x = 123"


def test_arabic_indic_in_expression():
    assert pretokenize("y = ٢ + ٣") == "y = 2 + 3"


def test_arabic_indic_zero():
    assert pretokenize("x = ٠") == "x = 0"


def test_arabic_indic_all_digits():
    assert pretokenize("x = ٠١٢٣٤٥٦٧٨٩") == "x = 0123456789"


# Eastern Arabic-Indic digit folding (3)
def test_eastern_indic_digit():
    assert pretokenize("x = ۵") == "x = 5"


def test_eastern_indic_multi():
    assert pretokenize("x = ۱۲۳") == "x = 123"


def test_eastern_indic_all():
    assert pretokenize("x = ۰۱۲۳۴۵۶۷۸۹") == "x = 0123456789"


# Arabic punctuation folding (4)
def test_arabic_comma():
    assert pretokenize("foo(a، b)") == "foo(a, b)"


def test_arabic_semicolon():
    assert pretokenize("a = 1؛ b = 2") == "a = 1; b = 2"


def test_arabic_question_mark():
    assert pretokenize("x ؟ y") == "x ? y"


def test_multiple_arabic_commas():
    assert pretokenize("foo(a، b، c، d)") == "foo(a, b, c, d)"


# Mixed-digit literal rejection (3)
def test_mixed_arabic_and_ascii_raises():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("x = ١2")
    msg = str(exc.value)
    assert "mixed digit" in msg
    assert "١2" in msg


def test_mixed_arabic_and_eastern_raises():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("x = ١۲")
    assert "mixed digit" in str(exc.value)


def test_mixed_in_middle_of_expression_raises():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("y = 5 + ١2 - 3")
    assert "mixed digit" in str(exc.value)


# String preservation (8)
def test_arabic_digit_inside_single_quoted():
    assert pretokenize("x = '٥'") == "x = '٥'"


def test_arabic_digit_inside_double_quoted():
    assert pretokenize('x = "٥"') == 'x = "٥"'


def test_arabic_digit_inside_triple_single():
    assert pretokenize("x = '''٥'''") == "x = '''٥'''"


def test_arabic_digit_inside_triple_double():
    assert pretokenize('x = """٥"""') == 'x = """٥"""'


def test_arabic_punct_inside_string():
    assert pretokenize("x = 'a، b'") == "x = 'a، b'"


def test_arabic_digit_outside_then_inside():
    assert pretokenize("x = ٥; y = '٥'") == "x = 5; y = '٥'"


def test_escaped_quote_in_string():
    src = "x = 'a\\'b'"
    assert pretokenize(src) == src


def test_string_after_string():
    src = "x = 'a' + 'b'"
    assert pretokenize(src) == src


# String prefixes (4)
def test_raw_string_prefix():
    src = "x = r'٥'"
    assert pretokenize(src) == src


def test_byte_string_prefix():
    src = "x = b'٥'"
    assert pretokenize(src) == src


def test_f_string_prefix_content_preserved():
    src = "x = f'٥'"
    assert pretokenize(src) == src


def test_uppercase_prefix():
    src = "x = R'٥'"
    assert pretokenize(src) == src


# Comments (3)
def test_arabic_digit_in_comment_folded():
    assert pretokenize("# value is ٥\nx = 1") == "# value is 5\nx = 1"


def test_arabic_punct_in_comment_folded():
    assert pretokenize("# a، b\nx = 1") == "# a, b\nx = 1"


def test_comment_ends_at_newline():
    assert pretokenize("# ٥\n٥ = 1") == "# 5\n5 = 1"


# Bidi rejection (12) — see ADR 0009 (supersedes ADR 0006's 9-codepoint set)
def _check_bidi_rejection(codepoint: str, expected_name: str):
    with pytest.raises(SyntaxError) as exc:
        pretokenize(f"x = {codepoint}")
    msg = str(exc.value)
    assert codepoint not in msg  # Ensure it prints the U+XXXX, not literal codepoint optionally
    hex_code = f"U+{ord(codepoint):04X}"
    assert hex_code in msg
    assert expected_name in msg
    assert "trojansource.codes" in msg


def test_bidi_alm_rejected():
    _check_bidi_rejection("\u061c", "ARABIC LETTER MARK")


def test_bidi_lrm_rejected():
    _check_bidi_rejection("\u200e", "LEFT-TO-RIGHT MARK")


def test_bidi_rlm_rejected():
    _check_bidi_rejection("\u200f", "RIGHT-TO-LEFT MARK")


def test_bidi_lre_rejected():
    _check_bidi_rejection("\u202a", "LEFT-TO-RIGHT EMBEDDING")


def test_bidi_rle_rejected():
    _check_bidi_rejection("\u202b", "RIGHT-TO-LEFT EMBEDDING")


def test_bidi_pdf_rejected():
    _check_bidi_rejection("\u202c", "POP DIRECTIONAL FORMATTING")


def test_bidi_lro_rejected():
    _check_bidi_rejection("\u202d", "LEFT-TO-RIGHT OVERRIDE")


def test_bidi_rlo_rejected():
    _check_bidi_rejection("\u202e", "RIGHT-TO-LEFT OVERRIDE")


def test_bidi_lri_rejected():
    _check_bidi_rejection("\u2066", "LEFT-TO-RIGHT ISOLATE")


def test_bidi_rli_rejected():
    _check_bidi_rejection("\u2067", "RIGHT-TO-LEFT ISOLATE")


def test_bidi_fsi_rejected():
    _check_bidi_rejection("\u2068", "FIRST STRONG ISOLATE")


def test_bidi_pdi_rejected():
    _check_bidi_rejection("\u2069", "POP DIRECTIONAL ISOLATE")


# Bidi inside strings is allowed (3)
def test_bidi_in_single_quoted_passes():
    src = "x = '\u202e'"
    assert pretokenize(src) == src


def test_bidi_in_triple_quoted_passes():
    src = "x = '''\u202e'''"
    assert pretokenize(src) == src


def test_bidi_in_docstring_passes():
    src = '"""\u202e"""\n'
    assert pretokenize(src) == src


def test_alm_in_string_passes():
    # ALM is the 0009-added codepoint most likely to appear legitimately in
    # Arabic data (as a per-character RTL hint inside a quoted Arabic string).
    src = "x = '\u061c'"
    assert pretokenize(src) == src


# Bidi in comments is REJECTED (1)
def test_bidi_in_comment_rejected():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("# \u202e hidden")
    msg = str(exc.value)
    assert "U+202E" in msg


# Line/column accuracy in error messages (2)
def test_bidi_error_line_column():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("x = 1\ny = \u202e")
    msg = str(exc.value)
    assert "line 2" in msg
    assert "column 4" in msg


def test_mixed_digit_error_line_column():
    with pytest.raises(SyntaxError) as exc:
        pretokenize("a = 1\nb = ١2")
    msg = str(exc.value)
    assert "line 2" in msg


# Idempotency on ASCII (1)
def test_idempotent_on_ascii_python():
    src = """def foo(x, y):
    if x > y:
        return x
    return y
"""
    assert pretokenize(src) == src


# Combined transformation (2)
def test_full_arabic_function():
    src_content = "def اضافة(a، b):\n    return a + b\n\nprint(اضافة(٢، ٣))\n"
    expected_content = "def اضافة(a, b):\n    return a + b\n\nprint(اضافة(2, 3))\n"
    assert pretokenize(src_content) == expected_content


def test_string_with_arabic_inside_arabic_function():
    src = 'تحية = "مرحبا، يا عالم"\n'
    assert pretokenize(src) == src


# Arabic escape sequences (9)


def test_escape_newline_arabic():
    assert pretokenize(r'x = "\س"') == r'x = "\n"'


def test_escape_tab_arabic():
    assert pretokenize(r'x = "\ج"') == r'x = "\t"'


def test_escape_carriage_return_arabic():
    assert pretokenize(r'x = "\ر"') == r'x = "\r"'


def test_escape_backspace_arabic():
    assert pretokenize(r'x = "\م"') == r'x = "\b"'


def test_escape_form_feed_arabic():
    assert pretokenize(r'x = "\ف"') == r'x = "\f"'


def test_escape_vertical_tab_arabic():
    assert pretokenize(r'x = "\ع"') == r'x = "\v"'


def test_escape_alert_arabic():
    assert pretokenize(r'x = "\ن"') == r'x = "\a"'


def test_escape_unknown_arabic_letter_passthrough():
    # Arabic letter that is NOT in the escape table: passes through unchanged.
    assert pretokenize(r'x = "\ق"') == r'x = "\ق"'


def test_escape_multiple_in_string():
    assert pretokenize(r'x = "\س\ج"') == r'x = "\n\t"'


# Arabic numeric literal prefixes (6)


def test_num_prefix_hex():
    assert pretokenize("x = 0سFF") == "x = 0xFF"


def test_num_prefix_binary():
    assert pretokenize("x = 0ث1010") == "x = 0b1010"


def test_num_prefix_octal():
    assert pretokenize("x = 0ذ17") == "x = 0o17"


def test_num_prefix_hex_zero():
    assert pretokenize("x = 0س0") == "x = 0x0"


def test_num_prefix_no_match_regular_zero():
    # Plain 0 without an Arabic prefix letter: unaffected.
    assert pretokenize("x = 0") == "x = 0"


def test_num_prefix_ascii_prefix_unaffected():
    # Standard 0x/0b/0o: must not be affected.
    assert pretokenize("x = 0xFF") == "x = 0xFF"


# Arabic string type prefixes (11)


def test_str_prefix_f_arabic():
    assert pretokenize('x = ت"hello"') == 'x = f"hello"'


def test_str_prefix_b_arabic():
    assert pretokenize('x = ب"data"') == 'x = b"data"'


def test_str_prefix_r_arabic():
    assert pretokenize('x = خ"path"') == 'x = r"path"'


def test_str_prefix_u_arabic():
    assert pretokenize('x = ي"text"') == 'x = u"text"'


def test_str_prefix_single_quote():
    assert pretokenize("x = ت'hello'") == "x = f'hello'"


def test_str_prefix_rf_combo():
    assert pretokenize('x = خت"path"') == 'x = rf"path"'


def test_str_prefix_fr_combo():
    assert pretokenize('x = تخ"path"') == 'x = fr"path"'


def test_str_prefix_rb_combo():
    assert pretokenize('x = خب"data"') == 'x = rb"data"'


def test_str_prefix_br_combo():
    assert pretokenize('x = بخ"data"') == 'x = br"data"'


def test_str_prefix_arabic_letter_not_before_quote_passthrough():
    # Arabic letter NOT immediately before a quote: treated as identifier, pass through.
    result = pretokenize("ت = 1\n")
    assert result == "ت = 1\n"


def test_str_prefix_triple_quote():
    assert pretokenize('x = ت"""hello"""') == 'x = f"""hello"""'
