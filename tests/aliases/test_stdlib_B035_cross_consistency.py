# tests/aliases/test_stdlib_B035_cross_consistency.py
# B-035 cross-consistency — math, statistics, random
#
# Verifies no Arabic name collisions within B-035 and between B-035 and
# earlier B-batches (B-030 through B-034).

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
    return set(proxy._mapping.keys())


# ── B-035 internal collision checks ──────────────────────────────────────────


def test_no_collision_math_vs_statistics():
    """رياضيات and احصاء share no Arabic entry keys."""
    math_keys = _load_keys("رياضيات")
    stat_keys = _load_keys("احصاء")
    overlap = math_keys & stat_keys
    assert not overlap, f"Collision between رياضيات and احصاء: {overlap}"


def test_no_collision_math_vs_random():
    """رياضيات and عشوائيات share no Arabic entry keys."""
    math_keys = _load_keys("رياضيات")
    rand_keys = _load_keys("عشوائيات")
    overlap = math_keys & rand_keys
    assert not overlap, f"Collision between رياضيات and عشوائيات: {overlap}"


def test_no_collision_statistics_vs_random():
    """احصاء and عشوائيات share no Arabic entry keys."""
    stat_keys = _load_keys("احصاء")
    rand_keys = _load_keys("عشوائيات")
    overlap = stat_keys & rand_keys
    assert not overlap, f"Collision between احصاء and عشوائيات: {overlap}"


# ── B-035 vs earlier B-batches ───────────────────────────────────────────────

B035_MODULES = ["رياضيات", "احصاء", "عشوائيات"]
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
    # B-033
    "جيسون",
    "ملفات_csv",
    "قاعدة_بيانات",
    # B-034
    "تعابير_نمطيه",
    "نصوص",
    "تنسيق_نص",
]


@pytest.mark.parametrize("b035_mod", B035_MODULES)
@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(b035_mod, earlier_mod):
    """B-035 module shares no Arabic entry keys with an earlier batch module."""
    b035_keys = _load_keys(b035_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = b035_keys & earlier_keys
    assert not overlap, f"Collision between {b035_mod} and {earlier_mod}: {overlap}"
