# tests/aliases/test_redis.py
# C-016: Arabic aliases for redis-py

import pathlib

import pytest

redis = pytest.importorskip("redis", reason="redis not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مخزن_سريع():
    """Return a ModuleProxy wrapping `redis`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مخزن_سريع", None, None)
    assert spec is not None, "AliasFinder did not find 'مخزن_سريع'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestRedisCore:
    def test_client_classes(self, مخزن_سريع):
        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(مخزن_سريع.رديس, ClassFactory)
        assert isinstance(مخزن_سريع.رديس_صارم, ClassFactory)
        assert مخزن_سريع.مجمع_اتصالات is redis.ConnectionPool
        assert مخزن_سريع.مجمع_اتصالات_مانع is redis.BlockingConnectionPool
        assert مخزن_سريع.انشئ_من_رابط is redis.from_url

    def test_submodules(self, مخزن_سريع):
        import redis.asyncio
        import redis.lock

        assert مخزن_سريع.غير_متزامن is redis.asyncio
        assert مخزن_سريع.اقفال is redis.lock

    def test_exceptions(self, مخزن_سريع):
        assert مخزن_سريع.خطا_رديس is redis.RedisError
        assert مخزن_سريع.خطا_اتصال is redis.ConnectionError
        assert مخزن_سريع.خطا_مهله is redis.TimeoutError
        assert مخزن_سريع.خطا_بيانات is redis.DataError


class TestRedisFunctional:
    def test_client_instance_methods_resolve_without_server(self, مخزن_سريع):
        client = مخزن_سريع.رديس(host="localhost", port=6379, db=0)
        wrapped = object.__getattribute__(client, "_wrapped")

        assert client.احصل_مفتاح == wrapped.get
        assert client.عين_مفتاح == wrapped.set
        assert client.انبوب == wrapped.pipeline
        assert client.اقرا_اشترك == wrapped.pubsub
        assert client.سجل_نص_lua == wrapped.register_script

    def test_attributes_work_with_class_proxy(self):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "redis.toml")
        client = redis.Redis(host="localhost", port=6379, db=0)
        proxy = ClassProxy(client, mapping.attributes)

        assert proxy.احصل == client.get
        assert proxy.عين == client.set
        assert proxy.انبوب == client.pipeline


class TestRedisTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "redis.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "redis"
        assert data["meta"]["arabic_name"] == "مخزن_سريع"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "redis.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 40
