# tests/aliases/test_random.py
# B-035 stdlib aliases — random module tests
#
# All randomness is seeded before use (ابذر / seed) so results are reproducible.
# Module-level functions operate on the global RandomState instance.

import pathlib
import random

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def عشوائيات():
    """Return a ModuleProxy wrapping `random`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("عشوائيات", None, None)
    assert spec is not None, "AliasFinder did not find 'عشوائيات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestRandomProxy:
    # ── Function aliases ──────────────────────────────────────────────────────

    def test_random_alias(self, عشوائيات):
        """عشوائي maps to random.random."""
        assert عشوائيات.عشوائي is random.random

    def test_randint_alias(self, عشوائيات):
        """عدد_عشوائي maps to random.randint."""
        assert عشوائيات.عدد_عشوائي is random.randint

    def test_randrange_alias(self, عشوائيات):
        """نطاق_عشوائي maps to random.randrange."""
        assert عشوائيات.نطاق_عشوائي is random.randrange

    def test_choice_alias(self, عشوائيات):
        """اختر maps to random.choice."""
        assert عشوائيات.اختر is random.choice

    def test_choices_alias(self, عشوائيات):
        """اختر_عده maps to random.choices."""
        assert عشوائيات.اختر_عده is random.choices

    def test_sample_alias(self, عشوائيات):
        """عينه maps to random.sample."""
        assert عشوائيات.عينه is random.sample

    def test_shuffle_alias(self, عشوائيات):
        """خلط maps to random.shuffle."""
        assert عشوائيات.خلط is random.shuffle

    def test_seed_alias(self, عشوائيات):
        """ابذر maps to random.seed."""
        assert عشوائيات.ابذر is random.seed

    def test_uniform_alias(self, عشوائيات):
        """موحد maps to random.uniform."""
        assert عشوائيات.موحد is random.uniform

    def test_gauss_alias(self, عشوائيات):
        """اعتدالي maps to random.gauss."""
        assert عشوائيات.اعتدالي is random.gauss

    def test_getstate_alias(self, عشوائيات):
        """احضر_حاله maps to random.getstate."""
        assert عشوائيات.احضر_حاله is random.getstate

    def test_setstate_alias(self, عشوائيات):
        """ضبط_حاله maps to random.setstate."""
        assert عشوائيات.ضبط_حاله is random.setstate

    def test_system_random_alias(self, عشوائيات):
        """عشوائي_نظام maps to random.SystemRandom."""
        assert عشوائيات.عشوائي_نظام is random.SystemRandom

    # ── Functional tests (all seeded for reproducibility) ─────────────────────

    def test_random_returns_float_in_range(self, عشوائيات):
        """عشوائي() returns a float in [0.0, 1.0)."""
        عشوائيات.ابذر(42)
        val = عشوائيات.عشوائي()
        assert isinstance(val, float)
        assert 0.0 <= val < 1.0

    def test_randint_in_bounds(self, عشوائيات):
        """عدد_عشوائي(1, 10) always returns an int in [1, 10]."""
        عشوائيات.ابذر(0)
        for _ in range(20):
            n = عشوائيات.عدد_عشوائي(1, 10)
            assert 1 <= n <= 10

    def test_choice_picks_from_list(self, عشوائيات):
        """اختر returns an element from the given list."""
        items = ["a", "b", "c", "d"]
        عشوائيات.ابذر(1)
        result = عشوائيات.اختر(items)
        assert result in items

    def test_sample_correct_size(self, عشوائيات):
        """عينه returns a list of the requested size without replacement."""
        pool = list(range(100))
        عشوائيات.ابذر(7)
        s = عشوائيات.عينه(pool, 10)
        assert len(s) == 10
        assert len(set(s)) == 10  # no duplicates
        assert all(item in pool for item in s)

    def test_shuffle_reorders_in_place(self, عشوائيات):
        """خلط shuffles a list in place."""
        lst = list(range(10))
        original = lst.copy()
        عشوائيات.ابذر(99)
        عشوائيات.خلط(lst)
        assert set(lst) == set(original)  # same elements
        assert lst != original  # order changed (probabilistically true for seed=99)

    def test_uniform_in_range(self, عشوائيات):
        """موحد(a, b) returns a float in [a, b]."""
        عشوائيات.ابذر(5)
        val = عشوائيات.موحد(10.0, 20.0)
        assert 10.0 <= val <= 20.0

    def test_seed_reproducible(self, عشوائيات):
        """ابذر with same seed produces same sequence."""
        عشوائيات.ابذر(42)
        first = عشوائيات.عشوائي()
        عشوائيات.ابذر(42)
        second = عشوائيات.عشوائي()
        assert first == second

    def test_getstate_setstate_roundtrip(self, عشوائيات):
        """احضر_حاله + ضبط_حاله replays the same sequence."""
        عشوائيات.ابذر(13)
        state = عشوائيات.احضر_حاله()
        val1 = عشوائيات.عشوائي()
        عشوائيات.ضبط_حاله(state)
        val2 = عشوائيات.عشوائي()
        assert val1 == val2

    def test_choices_with_k(self, عشوائيات):
        """اختر_عده returns k items (with replacement)."""
        عشوائيات.ابذر(3)
        pool = ["x", "y", "z"]
        result = عشوائيات.اختر_عده(pool, k=5)
        assert len(result) == 5
        assert all(item in pool for item in result)
