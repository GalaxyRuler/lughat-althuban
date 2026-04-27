# tests/aliases/test_secrets.py
# B-039 stdlib aliases — secrets module tests

import pathlib
import secrets

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def اسرار():
    """Return a ModuleProxy wrapping `secrets`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("اسرار", None, None)
    assert spec is not None, "AliasFinder did not find 'اسرار'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSecretsProxy:
    # ── Token generator aliases ────────────────────────────────────────────────

    def test_token_bytes_alias(self, اسرار):
        """رمز_بايت maps to secrets.token_bytes."""
        assert اسرار.رمز_بايت is secrets.token_bytes

    def test_token_hex_alias(self, اسرار):
        """رمز_سادس_عشري maps to secrets.token_hex."""
        assert اسرار.رمز_سادس_عشري is secrets.token_hex

    def test_token_urlsafe_alias(self, اسرار):
        """رمز_رابط maps to secrets.token_urlsafe."""
        assert اسرار.رمز_رابط is secrets.token_urlsafe

    # ── Secure random utility aliases ─────────────────────────────────────────

    def test_choice_alias(self, اسرار):
        """اختر_امن maps to secrets.choice."""
        assert اسرار.اختر_امن is secrets.choice

    def test_randbelow_alias(self, اسرار):
        """عشوائي_اقل maps to secrets.randbelow."""
        assert اسرار.عشوائي_اقل is secrets.randbelow

    def test_randbits_alias(self, اسرار):
        """بتات_سريه maps to secrets.randbits."""
        assert اسرار.بتات_سريه is secrets.randbits

    def test_system_random_alias(self, اسرار):
        """عشوائي_امن maps to secrets.SystemRandom."""
        assert اسرار.عشوائي_امن is secrets.SystemRandom

    # ── Comparison alias ──────────────────────────────────────────────────────

    def test_compare_digest_alias(self, اسرار):
        """قارن_بصمه maps to secrets.compare_digest."""
        assert اسرار.قارن_بصمه is secrets.compare_digest

    # ── Configuration alias ───────────────────────────────────────────────────

    def test_default_entropy_alias(self, اسرار):
        """انتروبيا_افتراضيه maps to secrets.DEFAULT_ENTROPY."""
        assert اسرار.انتروبيا_افتراضيه is secrets.DEFAULT_ENTROPY

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_token_bytes_length(self, اسرار):
        """رمز_بايت(n) returns exactly n bytes."""
        for n in (8, 16, 32):
            assert len(اسرار.رمز_بايت(n)) == n

    def test_token_hex_length(self, اسرار):
        """رمز_سادس_عشري(n) returns a hex string of length 2n."""
        token = اسرار.رمز_سادس_عشري(16)
        assert len(token) == 32
        assert all(c in "0123456789abcdef" for c in token)

    def test_token_urlsafe_is_string(self, اسرار):
        """رمز_رابط returns a URL-safe base64 string."""
        token = اسرار.رمز_رابط(16)
        assert isinstance(token, str)
        # URL-safe base64 chars only (plus optional padding =)
        import re

        assert re.match(r"^[A-Za-z0-9_=-]+$", token)

    def test_token_bytes_unique(self, اسرار):
        """Successive رمز_بايت calls produce different values."""
        a = اسرار.رمز_بايت(32)
        b = اسرار.رمز_بايت(32)
        assert a != b

    def test_choice_picks_from_sequence(self, اسرار):
        """اختر_امن returns an element from the given sequence."""
        population = ["ألف", "باء", "تاء", "ثاء"]
        for _ in range(20):
            assert اسرار.اختر_امن(population) in population

    def test_randbelow_in_range(self, اسرار):
        """عشوائي_اقل(n) returns integers in [0, n)."""
        for _ in range(50):
            val = اسرار.عشوائي_اقل(100)
            assert 0 <= val < 100

    def test_randbits_bit_length(self, اسرار):
        """بتات_سريه(k) returns a non-negative integer with at most k bits."""
        for k in (8, 16, 32, 64):
            val = اسرار.بتات_سريه(k)
            assert 0 <= val < 2**k

    def test_compare_digest_equal(self, اسرار):
        """قارن_بصمه returns True for equal strings (constant-time)."""
        assert اسرار.قارن_بصمه("abc", "abc") is True

    def test_compare_digest_unequal(self, اسرار):
        """قارن_بصمه returns False for different strings."""
        assert اسرار.قارن_بصمه("abc", "xyz") is False

    def test_default_entropy_is_positive_int(self, اسرار):
        """انتروبيا_افتراضيه is a positive integer (byte count)."""
        assert isinstance(اسرار.انتروبيا_افتراضيه, int)
        assert اسرار.انتروبيا_افتراضيه > 0
