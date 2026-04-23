# tests/aliases/test_hashlib.py
# B-038 stdlib aliases — hashlib module tests

import hashlib
import pathlib

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def هاشلب():
    """Return a ModuleProxy wrapping `hashlib`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("هاشلب", None, None)
    assert spec is not None, "AliasFinder did not find 'هاشلب'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestHashlibProxy:
    # ── Constructor alias ─────────────────────────────────────────────────────

    def test_new_alias(self, هاشلب):
        """هاش_جديد maps to hashlib.new."""
        assert هاشلب.هاش_جديد is hashlib.new

    # ── Named constructor aliases ─────────────────────────────────────────────

    def test_md5_alias(self, هاشلب):
        """مد5 maps to hashlib.md5."""
        assert هاشلب.مد5 is hashlib.md5

    def test_sha1_alias(self, هاشلب):
        """شا1 maps to hashlib.sha1."""
        assert هاشلب.شا1 is hashlib.sha1

    def test_sha224_alias(self, هاشلب):
        """شا224 maps to hashlib.sha224."""
        assert هاشلب.شا224 is hashlib.sha224

    def test_sha256_alias(self, هاشلب):
        """شا256 maps to hashlib.sha256."""
        assert هاشلب.شا256 is hashlib.sha256

    def test_sha384_alias(self, هاشلب):
        """شا384 maps to hashlib.sha384."""
        assert هاشلب.شا384 is hashlib.sha384

    def test_sha512_alias(self, هاشلب):
        """شا512 maps to hashlib.sha512."""
        assert هاشلب.شا512 is hashlib.sha512

    def test_sha3_256_alias(self, هاشلب):
        """شا3_256 maps to hashlib.sha3_256."""
        assert هاشلب.شا3_256 is hashlib.sha3_256

    def test_sha3_512_alias(self, هاشلب):
        """شا3_512 maps to hashlib.sha3_512."""
        assert هاشلب.شا3_512 is hashlib.sha3_512

    def test_blake2b_alias(self, هاشلب):
        """بليك_ب maps to hashlib.blake2b."""
        assert هاشلب.بليك_ب is hashlib.blake2b

    def test_blake2s_alias(self, هاشلب):
        """بليك_ص maps to hashlib.blake2s."""
        assert هاشلب.بليك_ص is hashlib.blake2s

    # ── Algorithm set aliases ─────────────────────────────────────────────────

    def test_algorithms_available_alias(self, هاشلب):
        """خوارزميات_متاحه maps to hashlib.algorithms_available."""
        assert هاشلب.خوارزميات_متاحه is hashlib.algorithms_available

    def test_algorithms_guaranteed_alias(self, هاشلب):
        """خوارزميات_مضمونه maps to hashlib.algorithms_guaranteed."""
        assert هاشلب.خوارزميات_مضمونه is hashlib.algorithms_guaranteed

    # ── Key derivation and file hashing ──────────────────────────────────────

    def test_pbkdf2_alias(self, هاشلب):
        """مشتق_مفتاح maps to hashlib.pbkdf2_hmac."""
        assert هاشلب.مشتق_مفتاح is hashlib.pbkdf2_hmac

    def test_file_digest_alias(self, هاشلب):
        """هاش_ملف maps to hashlib.file_digest."""
        assert هاشلب.هاش_ملف is hashlib.file_digest

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_sha256_hexdigest(self, هاشلب):
        """شا256 produces correct SHA-256 digest for known input."""
        data = b"arabicpython"
        expected = hashlib.sha256(data).hexdigest()
        result = هاشلب.شا256(data).hexdigest()
        assert result == expected
        assert len(result) == 64  # SHA-256 produces 64 hex chars

    def test_md5_hexdigest(self, هاشلب):
        """مد5 produces correct MD5 digest for known input."""
        data = b"test"
        expected = hashlib.md5(data).hexdigest()
        assert هاشلب.مد5(data).hexdigest() == expected
        assert len(هاشلب.مد5(data).hexdigest()) == 32

    def test_new_creates_hash(self, هاشلب):
        """هاش_جديد creates a hash object by algorithm name."""
        data = b"hello"
        h = هاشلب.هاش_جديد("sha256", data)
        assert h.hexdigest() == hashlib.sha256(data).hexdigest()

    def test_algorithms_guaranteed_contains_sha256(self, هاشلب):
        """sha256 is always in خوارزميات_مضمونه."""
        assert "sha256" in هاشلب.خوارزميات_مضمونه

    def test_sha256_different_inputs(self, هاشلب):
        """Different inputs produce different SHA-256 digests."""
        h1 = هاشلب.شا256(b"hello").hexdigest()
        h2 = هاشلب.شا256(b"world").hexdigest()
        assert h1 != h2

    def test_pbkdf2_returns_bytes(self, هاشلب):
        """مشتق_مفتاح returns bytes of the requested length."""
        dk = هاشلب.مشتق_مفتاح("sha256", b"password", b"salt", 1, 32)
        expected = hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 1, 32)
        assert dk == expected
        assert len(dk) == 32
