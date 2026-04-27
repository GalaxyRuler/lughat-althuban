# tests/aliases/test_uuid.py
# B-039 stdlib aliases — uuid module tests

import pathlib
import uuid

import pytest

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def معرفات_فريده():
    """Return a ModuleProxy wrapping `uuid`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("معرفات_فريده", None, None)
    assert spec is not None, "AliasFinder did not find 'معرفات_فريده'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestUuidProxy:
    # ── Generator aliases ──────────────────────────────────────────────────────

    def test_uuid1_alias(self, معرفات_فريده):
        """معرف1 maps to uuid.uuid1."""
        assert معرفات_فريده.معرف1 is uuid.uuid1

    def test_uuid3_alias(self, معرفات_فريده):
        """معرف3 maps to uuid.uuid3."""
        assert معرفات_فريده.معرف3 is uuid.uuid3

    def test_uuid4_alias(self, معرفات_فريده):
        """معرف4 maps to uuid.uuid4."""
        assert معرفات_فريده.معرف4 is uuid.uuid4

    def test_uuid5_alias(self, معرفات_فريده):
        """معرف5 maps to uuid.uuid5."""
        assert معرفات_فريده.معرف5 is uuid.uuid5

    # ── Class aliases ─────────────────────────────────────────────────────────

    def test_uuid_class_alias(self, معرفات_فريده):
        """معرف_فريد maps to uuid.UUID."""
        assert معرفات_فريده.معرف_فريد is uuid.UUID

    def test_safe_uuid_alias(self, معرفات_فريده):
        """معرف_فريد_امن maps to uuid.SafeUUID."""
        assert معرفات_فريده.معرف_فريد_امن is uuid.SafeUUID

    # ── Node alias ────────────────────────────────────────────────────────────

    def test_getnode_alias(self, معرفات_فريده):
        """عقده maps to uuid.getnode."""
        assert معرفات_فريده.عقده is uuid.getnode

    # ── Namespace UUID aliases ────────────────────────────────────────────────

    def test_namespace_dns_alias(self, معرفات_فريده):
        """فضاء_دنس maps to uuid.NAMESPACE_DNS."""
        assert معرفات_فريده.فضاء_دنس is uuid.NAMESPACE_DNS

    def test_namespace_url_alias(self, معرفات_فريده):
        """فضاء_رابط maps to uuid.NAMESPACE_URL."""
        assert معرفات_فريده.فضاء_رابط is uuid.NAMESPACE_URL

    def test_namespace_oid_alias(self, معرفات_فريده):
        """فضاء_oid maps to uuid.NAMESPACE_OID."""
        assert معرفات_فريده.فضاء_oid is uuid.NAMESPACE_OID

    def test_namespace_x500_alias(self, معرفات_فريده):
        """فضاء_x500 maps to uuid.NAMESPACE_X500."""
        assert معرفات_فريده.فضاء_x500 is uuid.NAMESPACE_X500

    # ── Functional tests ──────────────────────────────────────────────────────

    def test_uuid4_generates_valid_uuid(self, معرفات_فريده):
        """معرف4 generates a valid UUID4."""
        u = معرفات_فريده.معرف4()
        assert isinstance(u, معرفات_فريده.معرف_فريد)
        assert u.version == 4

    def test_uuid4_unique(self, معرفات_فريده):
        """Successive معرف4 calls return different UUIDs."""
        assert معرفات_فريده.معرف4() != معرفات_فريده.معرف4()

    def test_uuid1_generates_valid_uuid(self, معرفات_فريده):
        """معرف1 generates a valid UUID1."""
        u = معرفات_فريده.معرف1()
        assert isinstance(u, معرفات_فريده.معرف_فريد)
        assert u.version == 1

    def test_uuid3_deterministic(self, معرفات_فريده):
        """معرف3 with same namespace and name always returns the same UUID."""
        u1 = معرفات_فريده.معرف3(معرفات_فريده.فضاء_دنس, "python.org")
        u2 = معرفات_فريده.معرف3(معرفات_فريده.فضاء_دنس, "python.org")
        assert u1 == u2

    def test_uuid5_deterministic(self, معرفات_فريده):
        """معرف5 with same namespace and name always returns the same UUID."""
        u1 = معرفات_فريده.معرف5(معرفات_فريده.فضاء_دنس, "python.org")
        u2 = معرفات_فريده.معرف5(معرفات_فريده.فضاء_دنس, "python.org")
        assert u1 == u2

    def test_uuid3_and_uuid5_differ_for_same_input(self, معرفات_فريده):
        """معرف3 and معرف5 use different hash algorithms (MD5 vs SHA1)."""
        u3 = معرفات_فريده.معرف3(معرفات_فريده.فضاء_دنس, "python.org")
        u5 = معرفات_فريده.معرف5(معرفات_فريده.فضاء_دنس, "python.org")
        assert u3 != u5

    def test_uuid_from_string(self, معرفات_فريده):
        """معرف_فريد parses a UUID string."""
        s = "12345678-1234-5678-1234-567812345678"
        u = معرفات_فريده.معرف_فريد(s)
        assert str(u) == s

    def test_uuid_str_format(self, معرفات_فريده):
        """UUID string representation is in standard hyphenated form."""
        u = معرفات_فريده.معرف4()
        parts = str(u).split("-")
        assert len(parts) == 5
        assert [len(p) for p in parts] == [8, 4, 4, 4, 12]

    def test_namespace_dns_is_uuid(self, معرفات_فريده):
        """فضاء_دنس is a UUID instance."""
        assert isinstance(معرفات_فريده.فضاء_دنس, معرفات_فريده.معرف_فريد)

    def test_getnode_returns_int(self, معرفات_فريده):
        """عقده returns a non-negative integer."""
        node = معرفات_فريده.عقده()
        assert isinstance(node, int)
        assert node >= 0
