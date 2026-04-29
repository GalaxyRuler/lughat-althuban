# tests/aliases/test_pydantic.py
# C-012: Arabic aliases for Pydantic v2

import pathlib

import pytest

pydantic = pytest.importorskip("pydantic", minversion="2.0", reason="pydantic v2 not installed")

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def نماذج_بيانات():
    """Return a ModuleProxy wrapping `pydantic`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("نماذج_بيانات", None, None)
    assert spec is not None, "AliasFinder did not find 'نماذج_بيانات'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestPydanticCore:
    def test_base_model_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.نموذج_اساسي is pydantic.BaseModel

    def test_field_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.حقل is pydantic.Field

    def test_config_dict_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.اعدادات is pydantic.ConfigDict

    def test_validation_error_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.خطا_تحقق is pydantic.ValidationError

    def test_create_model_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.انشئ_نموذج is pydantic.create_model


class TestPydanticValidators:
    def test_field_validator_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.تحقق_حقل is pydantic.field_validator

    def test_model_validator_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.تحقق_نموذج is pydantic.model_validator

    def test_computed_field_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.حقل_محسوب is pydantic.computed_field

    def test_type_adapter_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.محول_نوع is pydantic.TypeAdapter


class TestPydanticTypes:
    def test_secret_str_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.نص_سري is pydantic.SecretStr

    def test_http_url_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.رابط_http is pydantic.HttpUrl

    def test_positive_int_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.عدد_موجب == pydantic.PositiveInt

    def test_strict_str_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.نص_صارم == pydantic.StrictStr

    def test_constrained_string_alias(self, نماذج_بيانات):
        assert نماذج_بيانات.قيد_نص is pydantic.constr


class TestPydanticFunctional:
    def test_model_validation_with_aliases(self, نماذج_بيانات):
        class User(نماذج_بيانات.نموذج_اساسي):
            name: str = نماذج_بيانات.حقل(min_length=2)
            age: نماذج_بيانات.عدد_غير_سالب

            @نماذج_بيانات.تحقق_حقل("name")
            @classmethod
            def strip_name(cls, value: str) -> str:  # noqa: N805
                return value.strip()

        user = User(name="  Layla  ", age=31)

        assert user.name == "Layla"
        assert user.age == 31
        with pytest.raises(نماذج_بيانات.خطا_تحقق):
            User(name="A", age=-1)

    def test_type_adapter_alias(self, نماذج_بيانات):
        adapter = نماذج_بيانات.محول_نوع(list[int])

        assert adapter.validate_python(["1", 2, 3]) == [1, 2, 3]

    def test_model_attributes_work_with_class_proxy(self, نماذج_بيانات):
        from arabicpython.aliases import ClassProxy, load_mapping

        mapping = load_mapping(ALIASES_DIR / "pydantic.toml")

        class Item(نماذج_بيانات.نموذج_اساسي):
            sku: str
            price: float

        item = Item(sku="A-1", price=12.5)
        proxy = ClassProxy(item, mapping.attributes)

        assert proxy.افرغ() == {"sku": "A-1", "price": 12.5}
        copied = proxy.انسخ_النموذج(update={"price": 13.0})
        assert copied.price == 13.0


class TestPydanticTomlMeta:
    def test_toml_parseable(self):
        import tomllib

        p = ALIASES_DIR / "pydantic.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert data["meta"]["python_module"] == "pydantic"
        assert data["meta"]["arabic_name"] == "نماذج_بيانات"

    def test_entry_count(self):
        import tomllib

        p = ALIASES_DIR / "pydantic.toml"
        with open(p, "rb") as f:
            data = tomllib.load(f)
        assert len(data["entries"]) >= 35
