# tests/aliases/test_pymongo.py
# C-018: Arabic aliases for PyMongo

import pathlib

import pytest

pymongo = pytest.importorskip("pymongo", reason="pymongo not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def قاعده_وثائق():
    """Return a ModuleProxy wrapping `pymongo`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("قاعده_وثائق", None, None)
    assert spec is not None, "AliasFinder did not find 'قاعده_وثائق'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestPymongoCore:
    def test_client_and_document_classes(self, قاعده_وثائق):
        import pymongo.collection
        import pymongo.cursor
        import pymongo.database

        from arabicpython.aliases._proxy import ClassFactory

        assert isinstance(قاعده_وثائق.عميل_مونجو, ClassFactory)
        assert قاعده_وثائق.قاعده_بيانات is pymongo.database.Database
        assert قاعده_وثائق.مجموعه is pymongo.collection.Collection
        assert قاعده_وثائق.مؤشر is pymongo.cursor.Cursor

    def test_operations_and_constants(self, قاعده_وثائق):
        assert قاعده_وثائق.اتجاه_تصاعدي == pymongo.ASCENDING
        assert قاعده_وثائق.اتجاه_تنازلي == pymongo.DESCENDING
        assert قاعده_وثائق.نموذج_فهرس is pymongo.IndexModel
        assert قاعده_وثائق.ادراج_واحد is pymongo.InsertOne
        assert قاعده_وثائق.تحديث_واحد is pymongo.UpdateOne
        assert قاعده_وثائق.حذف_واحد is pymongo.DeleteOne

    def test_exceptions(self, قاعده_وثائق):
        import pymongo.errors

        assert قاعده_وثائق.خطا_بايمونجو is pymongo.errors.PyMongoError
        assert قاعده_وثائق.خطا_اتصال is pymongo.errors.ConnectionFailure
        assert قاعده_وثائق.خطا_اختيار_خادم is pymongo.errors.ServerSelectionTimeoutError
        assert قاعده_وثائق.خطا_مفتاح_مكرر is pymongo.errors.DuplicateKeyError


class TestPymongoFunctional:
    def test_client_instance_methods_resolve_without_server(self, قاعده_وثائق):
        client = قاعده_وثائق.عميل_مونجو(
            "mongodb://localhost:27017",
            connect=False,
            serverSelectionTimeoutMS=1,
        )
        wrapped = object.__getattribute__(client, "_wrapped")

        assert client.احصل_قاعده_بيانات == wrapped.get_database
        assert client.اسماء_قواعد_بيانات == wrapped.list_database_names
        assert client.اغلق_عميل == wrapped.close
        client.اغلق_عميل()

    def test_collection_and_cursor_attributes_work_with_class_proxy(self):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "pymongo.toml")
        client = pymongo.MongoClient(
            "mongodb://localhost:27017",
            connect=False,
            serverSelectionTimeoutMS=1,
        )
        collection = client.get_database("demo").get_collection("items")
        collection_proxy = ClassProxy(collection, mapping.attributes)

        assert collection_proxy.ابحث_واحد == collection.find_one
        assert collection_proxy.حدث_واحد == collection.update_one
        assert collection_proxy.اجمع == collection.aggregate

        cursor = collection.find({})
        cursor_proxy = ClassProxy(cursor, mapping.attributes)

        assert cursor_proxy.حدد == cursor.limit
        assert cursor_proxy.رتب == cursor.sort
        assert cursor_proxy.تخطي == cursor.skip
        client.close()


class TestPymongoTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "pymongo.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "pymongo"
        assert data["meta"]["arabic_name"] == "قاعده_وثائق"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "pymongo.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 40
