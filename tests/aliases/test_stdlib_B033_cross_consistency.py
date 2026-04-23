# tests/aliases/test_stdlib_B033_cross_consistency.py
# B-033 cross-consistency — json, csv, sqlite3
#
# Verifies:
#   1. No Arabic name collision between the three B-033 modules.
#   2. No Arabic name collision with B-030 (os, pathlib, sys, io) modules.
#   3. No Arabic name collision with B-031 (collections, itertools, functools) modules.
#   4. No Arabic name collision with B-032 (datetime, time, calendar) modules.

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


def _load_keys(arabic_module_name: str) -> set[str]:
    """Return the set of Arabic entry keys for a given module alias name."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_module_name, None, None)
    if spec is None:
        pytest.skip(f"Module alias {arabic_module_name!r} not found — skipping")
    proxy = spec.loader.create_module(spec)
    # _mapping is a mappingproxy of the entries dict; .keys() gives Arabic names
    return set(proxy._mapping.keys())


# ── B-033 internal collision checks ──────────────────────────────────────────


def test_no_collision_json_vs_csv():
    """جيسون and ملفات_csv share no Arabic entry keys."""
    json_keys = _load_keys("جيسون")
    csv_keys = _load_keys("ملفات_csv")
    overlap = json_keys & csv_keys
    assert not overlap, f"Collision between جيسون and ملفات_csv: {overlap}"


def test_no_collision_json_vs_sqlite3():
    """جيسون and قاعدة_بيانات share no Arabic entry keys."""
    json_keys = _load_keys("جيسون")
    sqlite_keys = _load_keys("قاعدة_بيانات")
    overlap = json_keys & sqlite_keys
    assert not overlap, f"Collision between جيسون and قاعدة_بيانات: {overlap}"


def test_no_collision_csv_vs_sqlite3():
    """ملفات_csv and قاعدة_بيانات share no Arabic entry keys."""
    csv_keys = _load_keys("ملفات_csv")
    sqlite_keys = _load_keys("قاعدة_بيانات")
    overlap = csv_keys & sqlite_keys
    assert not overlap, f"Collision between ملفات_csv and قاعدة_بيانات: {overlap}"


# ── B-033 vs earlier B-batches ───────────────────────────────────────────────

B033_MODULES = ["جيسون", "ملفات_csv", "قاعدة_بيانات"]
EARLIER_MODULES = [
    # B-030
    "نظام_تشغيل",
    "مسار_مكتبه",
    "نظام",
    # B-031
    "مجموعات",
    "ادوات_تكرار",
    "ادوات_داليه",
    # B-032
    "مكتبة_تاريخ",
    "وقت_نظام",
    "روزنامه",
]


@pytest.mark.parametrize("b033_mod", B033_MODULES)
@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(b033_mod, earlier_mod):
    """B-033 module shares no Arabic entry keys with an earlier batch module."""
    b033_keys = _load_keys(b033_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = b033_keys & earlier_keys
    assert not overlap, f"Collision between {b033_mod} and {earlier_mod}: {overlap}"
