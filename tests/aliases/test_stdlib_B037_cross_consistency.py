# tests/aliases/test_stdlib_B037_cross_consistency.py
# B-037 cross-consistency — asyncio
#
# Verifies no Arabic name collisions between اتزامن (asyncio) and all
# earlier B-batch modules (B-030 through B-036).
#
# Known intentional overlaps:
#   اغلق — asyncio does NOT use this; only logging/sqlite3 do.
#   (No intentional overlaps expected for asyncio.)

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
    # B-035
    "رياضيات",
    "احصاء",
    "عشوائيات",
    # B-036
    "تسجيل",
]


@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(earlier_mod):
    """اتزامن shares no Arabic entry keys with an earlier batch module."""
    asyncio_keys = _load_keys("اتزامن")
    earlier_keys = _load_keys(earlier_mod)
    overlap = asyncio_keys & earlier_keys
    assert not overlap, f"Collision between اتزامن and {earlier_mod}: {overlap}"
