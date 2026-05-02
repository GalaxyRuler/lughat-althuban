import subprocess
import sys

from arabicpython.reverse import reverse_translate, reverse_translate_with_count
from arabicpython.translate import translate


def test_keywords_only():
    result = reverse_translate("if x:\n    pass\n", level=1)
    assert "إذا" in result
    assert "مرر" in result


def test_builtins_default_level():
    result = reverse_translate("print(len(x))\n")
    assert "اطبع" in result
    assert "طول" in result


def test_exceptions_level3():
    result = reverse_translate("try:\n    pass\nexcept ValueError:\n    pass\n", level=3)
    assert "خطأ_قيمة" in result


def test_preserves_user_bound_names():
    result = reverse_translate("def f(print):\n    return print\n", level=2)
    assert "def f" not in result
    assert "دالة f" in result
    assert "اطبع" not in result


def test_round_trip_reference_programs():
    programs = [
        'print("hello")\n',
        "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)\n",
        "values = [x * x for x in range(5)]\nprint(values)\n",
        'try:\n    int("x")\nexcept ValueError:\n    print("bad")\n',
        "class Box:\n    def __init__(self, value):\n        self.value = value\n",
    ]
    for source in programs:
        assert translate(reverse_translate(source, level=3)) == source


def test_replacement_count():
    result = reverse_translate_with_count("print(len(x))\n")
    assert result.replacements == 2


def test_cli_stdout(tmp_path):
    path = tmp_path / "hello.py"
    path.write_text('print("hello")\n', encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "arabicpython.cli",
            "ترجمة-عكسية",
            str(path),
            "--stdout",
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0
    assert "اطبع" in result.stdout
