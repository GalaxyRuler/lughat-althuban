"""tests/test_aliases_toml_invariants.py

Repo-wide invariants for every ``arabicpython/aliases/*.toml``:

* Every Arabic key in ``[entries]`` and ``[attributes]`` must round-trip
  through :func:`arabicpython.normalize.normalize_identifier` unchanged.
  (Catches typos like un-stripped shadda / ta-marbuta / hamza variants.)
* Within a single file, no two ``[entries]`` keys may map to the same
  Python attribute path. (Catches accidental duplicates.)
* Cross-file collisions among ``[entries]`` keys are budgeted: legitimate
  collisions across libraries (e.g. ``استجابه`` in ``requests`` vs
  ``httpx``) are allowed because each toml lives in its own module
  namespace, but the test fails loudly if a new toml introduces a large
  burst of fresh collisions — pointing the contributor at the
  disambiguation guidance in CONTRIBUTING.md.
"""

from __future__ import annotations

import pathlib
import tomllib

import pytest

from arabicpython.normalize import normalize_identifier

ALIASES_DIR = pathlib.Path(__file__).parent.parent / "arabicpython" / "aliases"
TOML_FILES = sorted(ALIASES_DIR.glob("*.toml"))

# Budget current as of Phase D source-of-truth generation: 91 cross-file
# [entries]-key collisions, all reviewed and accepted. Phase D adds broad
# AI/stdlib coverage and keeps common learner-facing words consistent across
# modules; the budget still catches surprise growth beyond this reviewed set.
COLLISION_BUDGET = 100


def _load(path: pathlib.Path) -> dict:
    with path.open("rb") as f:
        return tomllib.load(f)


@pytest.mark.parametrize("toml_path", TOML_FILES, ids=lambda p: p.stem)
def test_keys_round_trip_through_normalize(toml_path: pathlib.Path) -> None:
    """Every Arabic key must equal normalize_identifier(key)."""
    data = _load(toml_path)
    bad: list[str] = []
    for section in ("entries", "attributes"):
        for key in data.get(section, {}):
            normalized = normalize_identifier(key)
            if normalized != key:
                bad.append(f"[{section}] {key!r} -> {normalized!r}")
    assert not bad, (
        f"{toml_path.name}: keys do not round-trip through normalize_identifier; "
        "rewrite each key to its normalized form (ة→ه, أ/إ/آ→ا, ى→ي, no shadda):\n  "
        + "\n  ".join(bad)
    )


@pytest.mark.parametrize("toml_path", TOML_FILES, ids=lambda p: p.stem)
def test_no_duplicate_python_values_within_file(toml_path: pathlib.Path) -> None:
    """No two [entries] keys in the same file may map to the same Python attribute."""
    data = _load(toml_path)
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for key, value in data.get("entries", {}).items():
        if value in seen:
            duplicates.append(f"{key!r} and {seen[value]!r} both map to {value!r}")
        else:
            seen[value] = key
    assert (
        not duplicates
    ), f"{toml_path.name}: duplicate Python attribute values:\n  " + "\n  ".join(duplicates)


def test_cross_file_entry_collisions_within_budget() -> None:
    """Cross-file [entries]-key collision count must stay within budget.

    Legitimate collisions are allowed (e.g. ``خطا_مهله`` in several
    HTTP-client tomls), because each toml is its own module namespace.
    The test exists to flag *new* collisions introduced by a packet so the
    author can pick disambiguating names where appropriate.
    """
    keys_to_files: dict[str, list[str]] = {}
    for path in TOML_FILES:
        data = _load(path)
        for key in data.get("entries", {}):
            keys_to_files.setdefault(key, []).append(path.name)

    collisions = {k: v for k, v in keys_to_files.items() if len(v) > 1}
    assert len(collisions) <= COLLISION_BUDGET, (
        f"{len(collisions)} cross-file [entries]-key collisions "
        f"(budget: {COLLISION_BUDGET}). Either disambiguate new keys with "
        "domain-specific suffixes (see jwt.toml, sqlalchemy.toml for "
        "examples) or — if the new collisions are intentional and reviewed "
        "— bump COLLISION_BUDGET in this file."
    )
