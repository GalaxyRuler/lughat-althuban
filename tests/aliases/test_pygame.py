import os
import pathlib

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pytest

pygame = pytest.importorskip("pygame", reason="pygame-ce not installed")

from arabicpython.translate import translate  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def لعبه():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("لعبه", None, None)
    assert spec is not None, "AliasFinder did not find 'لعبه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


def test_pygame_core_aliases(لعبه):
    assert لعبه.ابدا is pygame.init
    assert لعبه.اغلق is pygame.quit
    assert لعبه.مستطيل is pygame.Rect
    assert لعبه.ساعه is pygame.time.Clock
    assert لعبه.نافذه is pygame.display.set_mode
    assert لعبه.عنوان_النافذه is pygame.display.set_caption
    assert لعبه.ارسم_مستطيل is pygame.draw.rect
    assert لعبه.خروج == pygame.QUIT
    assert لعبه.مفتاح_يمين == pygame.K_RIGHT


def test_pygame_alias_finder_accepts_arabic_spelling():
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    assert finder.find_spec("لعبه", None, None) is not None
    assert finder.find_spec("لعبة", None, None) is not None


def test_pygame_draws_surface_with_arabic_api(لعبه):
    لعبه.ابدا()
    try:
        نافذه = لعبه.نافذه((64, 48))
        مربع = لعبه.مستطيل(4, 5, 10, 12)

        لعبه.املا(نافذه, (0, 0, 0))
        لعبه.ارسم_مستطيل(نافذه, (255, 0, 0), مربع)
        اطار = لعبه.سطح_مستطيل(نافذه)
        ساعه = لعبه.ساعه()

        assert اطار.width == 64
        assert اطار.height == 48
        assert لعبه.يتصادم(اطار, مربع)
        assert لعبه.انتظر_اطار(ساعه, 60) >= 0
    finally:
        لعبه.اغلق()


def test_translated_arabic_pygame_program_runs():
    from arabicpython import install_aliases

    install_aliases()
    source = """
استورد لعبه

لعبه.ابدا()
نافذه = لعبه.نافذه((٦٤، ٤٨))
لعبه.عنوان_النافذه("اختبار عربي")
مربع = لعبه.مستطيل(٤، ٥، ١٠، ١٢)
لعبه.املا(نافذه، (٠، ٠، ٠))
لعبه.ارسم_مستطيل(نافذه، (٢٥٥، ٠، ٠)، مربع)
اطار = لعبه.سطح_مستطيل(نافذه)
ساعه = لعبه.ساعه()
لعبه.انتظر_اطار(ساعه، ٦٠)
لعبه.اغلق()
"""

    namespace: dict[str, object] = {}
    exec(compile(translate(source), "<pygame-arabic>", "exec"), namespace)  # noqa: S102
    assert namespace["اطار"].width == 64
