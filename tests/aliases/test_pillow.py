# tests/aliases/test_pillow.py
# B-018: Arabic aliases for Pillow image processing — بيلو

import pathlib

import pytest

PIL = pytest.importorskip("PIL", reason="Pillow not installed — skipping")

from PIL import Image  # noqa: E402

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def بيلو():
    """Return a ModuleProxy wrapping `PIL.Image`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("بيلو", None, None)
    assert spec is not None, "AliasFinder did not find 'بيلو'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


# ── Core functions ────────────────────────────────────────────────────────────


class TestCoreFunctions:
    def test_open_alias(self, بيلو):
        assert بيلو.افتح_صوره is Image.open

    def test_new_alias(self, بيلو):
        assert بيلو.جديد is Image.new

    def test_fromarray_alias(self, بيلو):
        assert بيلو.من_مصفوفه is Image.fromarray

    def test_frombytes_alias(self, بيلو):
        assert بيلو.من_بايتات is Image.frombytes

    def test_frombuffer_alias(self, بيلو):
        assert بيلو.من_مخزن is Image.frombuffer

    def test_merge_alias(self, بيلو):
        assert بيلو.ادمج_قنوات is Image.merge

    def test_blend_alias(self, بيلو):
        assert بيلو.امزج is Image.blend

    def test_composite_alias(self, بيلو):
        assert بيلو.مركب is Image.composite

    def test_alpha_composite_alias(self, بيلو):
        assert بيلو.مركب_شفافيه is Image.alpha_composite


# ── Image class ───────────────────────────────────────────────────────────────


class TestImageClass:
    def test_image_class_alias(self, بيلو):
        assert بيلو.فئه_الصوره is Image.Image

    def test_image_class_is_type(self, بيلو):
        assert isinstance(بيلو.فئه_الصوره, type)


# ── Resampling constants ──────────────────────────────────────────────────────


class TestResamplingConstants:
    def test_nearest_alias(self, بيلو):
        assert بيلو.اقرب == Image.NEAREST

    def test_lanczos_alias(self, بيلو):
        assert بيلو.لانكزوس == Image.LANCZOS

    def test_bilinear_alias(self, بيلو):
        assert بيلو.ثنائي_خطي == Image.BILINEAR

    def test_bicubic_alias(self, بيلو):
        assert بيلو.تكعيبي == Image.BICUBIC

    def test_box_alias(self, بيلو):
        assert بيلو.صندوقي == Image.BOX

    def test_hamming_alias(self, بيلو):
        assert بيلو.هامينغ == Image.HAMMING


# ── Transpose constants ───────────────────────────────────────────────────────


class TestTransposeConstants:
    def test_flip_left_right_alias(self, بيلو):
        assert بيلو.اقلب_افقيا == Image.FLIP_LEFT_RIGHT

    def test_flip_top_bottom_alias(self, بيلو):
        assert بيلو.اقلب_عموديا == Image.FLIP_TOP_BOTTOM

    def test_rotate_90_alias(self, بيلو):
        assert بيلو.دوران_90 == Image.ROTATE_90

    def test_rotate_180_alias(self, بيلو):
        assert بيلو.دوران_180 == Image.ROTATE_180

    def test_rotate_270_alias(self, بيلو):
        assert بيلو.دوران_270 == Image.ROTATE_270


# ── Exceptions ────────────────────────────────────────────────────────────────


class TestExceptions:
    def test_unidentified_image_error_alias(self, بيلو):
        assert بيلو.خطا_صوره_مجهوله is Image.UnidentifiedImageError

    def test_decompression_bomb_error_alias(self, بيلو):
        assert بيلو.خطا_ضغط_انفجاري is Image.DecompressionBombError

    def test_errors_are_exceptions(self, بيلو):
        assert issubclass(بيلو.خطا_صوره_مجهوله, Exception)
        assert issubclass(بيلو.خطا_ضغط_انفجاري, Exception)


# ── Functional ────────────────────────────────────────────────────────────────


class TestFunctional:
    def test_new_creates_image(self, بيلو):
        """جديد creates a blank PIL.Image.Image instance."""
        img = بيلو.جديد("RGB", (100, 100), color=(255, 0, 0))
        assert isinstance(img, بيلو.فئه_الصوره)
        assert img.size == (100, 100)
        assert img.mode == "RGB"

    def test_fromarray_roundtrip(self, بيلو):
        """من_مصفوفه converts a numpy-style list-of-lists to an Image."""
        pytest.importorskip("numpy")
        import numpy as np

        arr = np.zeros((50, 50, 3), dtype=np.uint8)
        arr[:, :, 0] = 128  # red channel
        img = بيلو.من_مصفوفه(arr)
        assert isinstance(img, بيلو.فئه_الصوره)
        assert img.size == (50, 50)

    def test_blend_produces_image(self, بيلو):
        """امزج blends two images with a given alpha."""
        a = بيلو.جديد("RGB", (10, 10), color=(0, 0, 0))
        b = بيلو.جديد("RGB", (10, 10), color=(255, 255, 255))
        blended = بيلو.امزج(a, b, alpha=0.5)
        assert isinstance(blended, بيلو.فئه_الصوره)
        px = blended.getpixel((0, 0))
        assert px == (127, 127, 127)

    def test_merge_rgb_channels(self, بيلو):
        """ادمج_قنوات merges three L-mode images into one RGB image."""
        r = بيلو.جديد("L", (4, 4), 200)
        g = بيلو.جديد("L", (4, 4), 100)
        b = بيلو.جديد("L", (4, 4), 50)
        rgb = بيلو.ادمج_قنوات("RGB", (r, g, b))
        assert rgb.mode == "RGB"
        assert rgb.getpixel((0, 0)) == (200, 100, 50)

    def test_resampling_constants_are_distinct(self, بيلو):
        """The six resampling constants all have distinct values."""
        values = {
            بيلو.اقرب,
            بيلو.لانكزوس,
            بيلو.ثنائي_خطي,
            بيلو.تكعيبي,
            بيلو.صندوقي,
            بيلو.هامينغ,
        }
        assert len(values) == 6

    def test_unidentified_image_error_raised(self, بيلو, tmp_path):
        """خطا_صوره_مجهوله is raised when opening a non-image file."""
        bad = tmp_path / "not_an_image.jpg"
        bad.write_bytes(b"this is not an image")
        with pytest.raises(بيلو.خطا_صوره_مجهوله):
            بيلو.افتح_صوره(str(bad))
