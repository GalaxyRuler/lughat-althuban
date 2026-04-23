# tests/aliases/test_stdlib_B034_cross_consistency.py
# B-034 cross-consistency — re, string, textwrap
#
# Verifies no Arabic name collisions within B-034 and between B-034 and
# earlier B-batches (B-030 through B-033).

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


# ── B-034 internal collision checks ──────────────────────────────────────────


def test_no_collision_re_vs_string():
    """تعابير_نمطيه and نصوص share no Arabic entry keys."""
    re_keys = _load_keys("تعابير_نمطيه")
    str_keys = _load_keys("نصوص")
    overlap = re_keys & str_keys
    assert not overlap, f"Collision between تعابير_نمطيه and نصوص: {overlap}"


def test_no_collision_re_vs_textwrap():
    """تعابير_نمطيه and تنسيق_نص share no Arabic entry keys."""
    re_keys = _load_keys("تعابير_نمطيه")
    tw_keys = _load_keys("تنسيق_نص")
    overlap = re_keys & tw_keys
    assert not overlap, f"Collision between تعابير_نمطيه and تنسيق_نص: {overlap}"


def test_no_collision_string_vs_textwrap():
    """نصوص and تنسيق_نص share no Arabic entry keys."""
    str_keys = _load_keys("نصوص")
    tw_keys = _load_keys("تنسيق_نص")
    overlap = str_keys & tw_keys
    assert not overlap, f"Collision between نصوص and تنسيق_نص: {overlap}"


# ── Documented divergences (for code-review) ─────────────────────────────────


def test_re_groups_vs_match_groups_distinct():
    """مجموعات (Match.groups) in re ≠ مجموعات (Match.groups) name ambiguity check.

    re.Match.groups → مجموعات  (tuple of all capture groups on a match object)
    This same Arabic word is NOT used in collections (مجموعات is the module name,
    not an entry key).  The two usages are in separate namespaces and don't clash.
    """
    re_keys = _load_keys("تعابير_نمطيه")
    col_keys = _load_keys("مجموعات")  # collections module
    # مجموعات is used as the *module name* for collections, not as an entry key;
    # re has مجموعات as an entry for Match.groups — no actual collision.
    assert "مجموعات" in re_keys  # re has it as an entry
    assert "مجموعات" not in col_keys  # collections does NOT have it as an entry


# ── B-034 vs earlier B-batches ───────────────────────────────────────────────

B034_MODULES = ["تعابير_نمطيه", "نصوص", "تنسيق_نص"]
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
]


@pytest.mark.parametrize("b034_mod", B034_MODULES)
@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(b034_mod, earlier_mod):
    """B-034 module shares no Arabic entry keys with an earlier batch module."""
    b034_keys = _load_keys(b034_mod)
    earlier_keys = _load_keys(earlier_mod)
    overlap = b034_keys & earlier_keys
    assert not overlap, f"Collision between {b034_mod} and {earlier_mod}: {overlap}"
