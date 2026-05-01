import os
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _run_tool(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    return subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


def test_lexicon_validator_passes():
    result = _run_tool("tools/validate_lexicon.py")
    assert result.returncode == 0, result.stderr
    assert "تم التحقق من المعجم العربي" in result.stdout


def test_generated_lexicon_outputs_are_fresh():
    result = _run_tool("tools/generate_lexicon_outputs.py", "--check")
    assert result.returncode == 0, result.stdout + result.stderr


def test_every_alias_file_has_library_lexicon_entry():
    with (ROOT / "lexicon" / "libraries.toml").open("rb") as f:
        libraries = tomllib.load(f)
    indexed = {item["alias_file"] for item in libraries["library"]}
    alias_files = {path.name for path in (ROOT / "arabicpython" / "aliases").glob("*.toml")}
    assert alias_files <= indexed
