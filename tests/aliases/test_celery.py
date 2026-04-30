# tests/aliases/test_celery.py
# C-017: Arabic aliases for Celery

import pathlib

import pytest

celery = pytest.importorskip("celery", reason="celery not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def مهام_خلفيه():
    """Return a ModuleProxy wrapping `celery`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("مهام_خلفيه", None, None)
    assert spec is not None, "AliasFinder did not find 'مهام_خلفيه'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestCeleryCore:
    def test_app_and_task_classes(self, مهام_خلفيه):
        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(مهام_خلفيه.تطبيق_سيلري, ClassFactory)
        assert مهام_خلفيه.مهمه is celery.Task
        assert مهام_خلفيه.مهمه_مشتركه is celery.shared_task

    def test_canvas_aliases(self, مهام_خلفيه):
        assert مهام_خلفيه.سلسله is celery.chain
        assert مهام_خلفيه.مجموعة_مهام is celery.group
        assert مهام_خلفيه.وتر is celery.chord
        assert مهام_خلفيه.توقيع is celery.signature

    def test_schedule_and_result_aliases(self, مهام_خلفيه):
        import celery.result
        import celery.schedules

        assert مهام_خلفيه.جدوله_cron is celery.schedules.crontab
        assert مهام_خلفيه.نتيجه_غير_متزامنه is celery.result.AsyncResult
        assert مهام_خلفيه.نتيجه_مجموعه is celery.result.GroupResult

    def test_exceptions(self, مهام_خلفيه):
        import celery.exceptions

        assert مهام_خلفيه.خطا_سيلري is celery.exceptions.CeleryError
        assert مهام_خلفيه.اعد_المحاوله is celery.exceptions.Retry
        assert مهام_خلفيه.تجاهل is celery.exceptions.Ignore
        assert مهام_خلفيه.ارفض is celery.exceptions.Reject


class TestCeleryFunctional:
    def test_task_decorator_runs_eagerly_without_broker(self, مهام_خلفيه):
        app = مهام_خلفيه.تطبيق_سيلري(
            "demo",
            broker="memory://",
            backend="cache+memory://",
        )
        app.conf.task_always_eager = True
        app.conf.task_store_eager_result = True

        @app.عرف_مهمه
        def add(x: int, y: int) -> int:
            return x + y

        result = add.delay(2, 3)

        assert result.result == 5
        assert app.مهام_مسجله is object.__getattribute__(app, "_wrapped").tasks

    def test_attributes_work_with_class_proxy(self):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "celery.toml")
        app = celery.Celery("demo", broker="memory://", backend="cache+memory://")
        proxy = ClassProxy(app, mapping.attributes)

        assert proxy.عرف_مهمه == app.task
        assert proxy.ارسل_مهمه == app.send_task
        assert proxy.التكوين is app.conf


class TestCeleryTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "celery.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "celery"
        assert data["meta"]["arabic_name"] == "مهام_خلفيه"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "celery.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 30
