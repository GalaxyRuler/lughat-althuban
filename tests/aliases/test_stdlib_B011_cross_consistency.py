# tests/aliases/test_stdlib_B011_cross_consistency.py
# B-011 cross-consistency — FastAPI (واجهه_برمجيه)
#
# Verifies no Arabic name collisions between واجهه_برمجيه and all earlier
# B-batch modules.

import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


def _load_keys(arabic_module_name: str) -> set[str]:
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_module_name, None, None)
    if spec is None:
        pytest.skip(f"Module alias {arabic_module_name!r} not found — skipping")
    proxy = spec.loader.create_module(spec)
    return set(proxy._mapping.keys())


EARLIER_MODULES = [
    "طلبات",
    "دجانغو",
    "قاعده_علائقيه",
    "اختبارات",
    "نمباي",
    "بانداس",
    "صور",
    "نظام_تشغيل",
    "مسار_مكتبه",
    "نظام",
    "مجموعات",
    "ادوات_تكرار",
    "ادوات_داليه",
    "مكتبة_تاريخ",
    "وقت_نظام",
    "روزنامه",
    "جيسون",
    "ملفات_csv",
    "قاعدة_بيانات",
    "تعابير_نمطيه",
    "نصوص",
    "تنسيق_نص",
    "رياضيات",
    "احصاء",
    "عشوائيات",
    "تسجيل",
    "اتزامن",
    "هاشلب",
    "مجاري",
    "مدير_سياق",
    "عملية_فرعية",
    "ادوات_ملفات",
    "محلل_وسائط",
    "اسرار",
    "معرفات_فريده",
]


@pytest.mark.parametrize("earlier_mod", EARLIER_MODULES)
def test_no_collision_with_earlier_batches(earlier_mod):
    """واجهه_برمجيه shares no Arabic entry keys with any earlier batch module."""
    fastapi_keys = _load_keys("واجهه_برمجيه")
    earlier_keys = _load_keys(earlier_mod)
    overlap = fastapi_keys & earlier_keys
    assert not overlap, f"Collision between واجهه_برمجيه and {earlier_mod}: {overlap}"
