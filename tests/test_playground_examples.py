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
    r'^  \{\s*\n\s*id:\s*"(?P<id>[^"]+)"(?P<body>.*?)(?=^  \},?\s*$)',
    re.M | re.S,
)
CODE_RE = re.compile(r"code:\s*`(?P<code>.*?)`", re.S)
SOURCE_RE = re.compile(r'source:\s*"(?P<source>[^"]+)"')
LATIN_LETTER_RE = re.compile(r"[A-Za-z]")
EXAMPLE_INPUTS = {
    "desert-treasure": ["شرق", "شرق", "شمال", "بحث"],
}


def _playground_examples() -> list[tuple[str, str]]:
    html = PLAYGROUND.read_text(encoding="utf-8")
    examples = []
    for match in EXAMPLE_RE.finditer(html):
        example_id = match.group("id")
        body = match.group("body")
        code_match = CODE_RE.search(body)
        if code_match:
            examples.append((example_id, code_match.group("code")))
            continue

        source_match = SOURCE_RE.search(body)
        if source_match:
            source_path = PLAYGROUND.parent / source_match.group("source")
            examples.append((example_id, source_path.read_text(encoding="utf-8")))
            continue

        raise AssertionError(f"playground example {example_id!r} has no code or source")

    assert examples
    return examples


@pytest.mark.parametrize(("example_id", "source"), _playground_examples())
def test_playground_example_output_stays_arabic_first(
    monkeypatch: pytest.MonkeyPatch,
    example_id: str,
    source: str,
) -> None:
    stdout = io.StringIO()
    stderr = io.StringIO()
    translated = translate(source)
    compiled = compile(translated, f"<playground:{example_id}>", "exec")
    answers = iter(EXAMPLE_INPUTS.get(example_id, []))

    def fake_input(prompt: object = "") -> str:
        with contextlib.suppress(StopIteration):
            return next(answers)
        return ""

    monkeypatch.setattr("builtins.input", fake_input)
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        exec(compiled, {"__name__": "__main__"})  # noqa: S102

    output = stdout.getvalue() + stderr.getvalue()
    assert not LATIN_LETTER_RE.search(output), (
        f"{example_id} printed Latin letters; playground examples must keep "
        f"runtime output Arabic-first.\n{output}"
    )


def test_desert_treasure_source_uses_no_latin_letters() -> None:
    source = (PROJECT_ROOT / "docs" / "games" / "كنز_الصحراء.apy").read_text(encoding="utf-8")
    assert not LATIN_LETTER_RE.search(source)
