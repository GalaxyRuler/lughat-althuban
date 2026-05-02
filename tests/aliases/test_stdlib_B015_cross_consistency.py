# tests/aliases/test_stdlib_B015_cross_consistency.py
# B-015 cross-consistency — pytest (بايتست)
#
# Verifies no Arabic name collisions between بايتست and all earlier
# B-batch modules (B-001/requests, B-012/django, B-013/sqlalchemy,
# B-014/requests-extras already in requests.toml, B-016/numpy,
# B-017/pandas, B-030 through B-039).
#
# Known intentional overlaps: none.

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
    # B-001 / B-014
    "طلبات",
    # B-012
    "دجانغو",
    # B-013
    "ألكيمي",
    # B-016
    "نمباي",
    # B-017
    "بانداس",
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
    # B-037
    "اتزامن",
    # B-038
    "هاشلب",
    "مجاري",
    "مدير_سياق",
    # B-039
    "عملية_فرعية",
    "ادوات_ملفات",
    "محلل_وسائط",
    "اسرار",
    "معرفات_فريده",
]


@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(earlier_mod):
    """بايتست shares no Arabic entry keys with any earlier batch module."""
    pytest_keys = _load_keys("بايتست")
    earlier_keys = _load_keys(earlier_mod)
    overlap = pytest_keys & earlier_keys
    assert not overlap, f"Collision between بايتست and {earlier_mod}: {overlap}"
