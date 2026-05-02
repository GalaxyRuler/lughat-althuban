from __future__ import annotations

import contextlib
import io
import re
from pathlib import Path

import pytest

from arabicpython.translate import translate

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLAYGROUND = PROJECT_ROOT / "docs" / "playground.html"
EXAMPLE_RE = re.compile(
    r'\{\s*id:\s*"(?P<id>[^"]+)".*?code:\s*`(?P<code>.*?)`\s*\n\s*\}',
    re.S,
)
LATIN_LETTER_RE = re.compile(r"[A-Za-z]")


def _playground_examples() -> list[tuple[str, str]]:
    html = PLAYGROUND.read_text(encoding="utf-8")
    return [(match.group("id"), match.group("code")) for match in EXAMPLE_RE.finditer(html)]


@pytest.mark.parametrize(("example_id", "source"), _playground_examples())
def test_playground_example_output_stays_arabic_first(example_id: str, source: str) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    translated = translate(source)
    compiled = compile(translated, f"<playground:{example_id}>", "exec")

    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(compiled, {"__name__": "__main__"})  # noqa: S102

    output = stdout.getvalue() + stderr.getvalue()
    assert not LATIN_LETTER_RE.search(output), (
        f"{example_id} printed Latin letters; playground examples must keep "
        f"runtime output Arabic-first.\n{output}"
    )
