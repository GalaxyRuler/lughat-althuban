# tests/aliases/test_sqlalchemy.py
# B-013 third-party aliases — sqlalchemy database toolkit tests
#
# All tests use an in-memory SQLite engine ("sqlite:///:memory:") so no on-disk
# state is created.  ORM tests build a tiny declarative model on the fly.

import pathlib

import pytest
import sqlalchemy as sa

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


@pytest.fixture(scope="module")
def ألكيمي():
    """Return a ModuleProxy wrapping `sqlalchemy`."""
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec("ألكيمي", None, None)
    assert spec is not None, "AliasFinder did not find 'ألكيمي'"
    proxy = spec.loader.create_module(spec)
    assert proxy is not None
    return proxy


class TestSqlaEngine:
    def test_create_engine_alias(self, ألكيمي):
        assert ألكيمي.انشئ_محرك is sa.create_engine

    def test_text_alias(self, ألكيمي):
        assert ألكيمي.نص_خام is sa.text

    def test_url_alias(self, ألكيمي):
        assert ألكيمي.رابط_url is sa.URL

    def test_make_url_alias(self, ألكيمي):
        assert ألكيمي.احلل_url is sa.make_url

    def test_inspect_alias(self, ألكيمي):
        assert ألكيمي.افحص_محرك is sa.inspect


class TestSqlaSession:
    def test_session_alias(self, ألكيمي):
        from sqlalchemy.orm import Session

        assert ألكيمي.جلسه_قاعده is Session

    def test_sessionmaker_alias(self, ألكيمي):
        from sqlalchemy.orm import sessionmaker

        assert ألكيمي.صانع_جلسات is sessionmaker

    def test_scoped_session_alias(self, ألكيمي):
        from sqlalchemy.orm import scoped_session

        assert ألكيمي.جلسه_موجهه is scoped_session


class TestSqlaOrmMapping:
    def test_declarative_base_alias(self, ألكيمي):
        from sqlalchemy.orm import DeclarativeBase

        assert ألكيمي.اساس_تعريفي is DeclarativeBase

    def test_mapped_column_class_alias(self, ألكيمي):
        from sqlalchemy.orm import MappedColumn

        assert ألكيمي.عمود_موجه is MappedColumn

    def test_mapped_column_factory_alias(self, ألكيمي):
        from sqlalchemy.orm import mapped_column

        assert ألكيمي.عرف_عمود is mapped_column

    def test_relationship_alias(self, ألكيمي):
        from sqlalchemy.orm import relationship

        assert ألكيمي.علاقه is relationship

    def test_backref_alias(self, ألكيمي):
        from sqlalchemy.orm import backref

        assert ألكيمي.علاقه_عكسيه is backref

    def test_mapped_alias(self, ألكيمي):
        from sqlalchemy.orm import Mapped

        assert ألكيمي.موجه is Mapped

    def test_registry_alias(self, ألكيمي):
        from sqlalchemy.orm import registry

        assert ألكيمي.سجل_تعيينات is registry


class TestSqlaTypes:
    def test_column_alias(self, ألكيمي):
        assert ألكيمي.عمود is sa.Column

    def test_integer_alias(self, ألكيمي):
        assert ألكيمي.نوع_عدد_صحيح is sa.Integer

    def test_string_alias(self, ألكيمي):
        assert ألكيمي.نوع_نص is sa.String

    def test_float_alias(self, ألكيمي):
        assert ألكيمي.نوع_عشري is sa.Float

    def test_boolean_alias(self, ألكيمي):
        assert ألكيمي.نوع_منطقي is sa.Boolean

    def test_date_alias(self, ألكيمي):
        assert ألكيمي.نوع_تاريخ is sa.Date

    def test_datetime_alias(self, ألكيمي):
        assert ألكيمي.نوع_تاريخ_وقت is sa.DateTime

    def test_time_alias(self, ألكيمي):
        assert ألكيمي.نوع_وقت is sa.Time

    def test_text_type_alias(self, ألكيمي):
        assert ألكيمي.نوع_نص_طويل is sa.Text

    def test_foreign_key_alias(self, ألكيمي):
        assert ألكيمي.مفتاح_اجنبي is sa.ForeignKey

    def test_primary_key_constraint_alias(self, ألكيمي):
        assert ألكيمي.قيد_مفتاح_رئيسي is sa.PrimaryKeyConstraint

    def test_unique_constraint_alias(self, ألكيمي):
        assert ألكيمي.قيد_فريد is sa.UniqueConstraint

    def test_index_alias(self, ألكيمي):
        assert ألكيمي.فهرس_جدول is sa.Index


class TestSqlaQuery:
    def test_select_alias(self, ألكيمي):
        assert ألكيمي.اختر_من is sa.select

    def test_insert_alias(self, ألكيمي):
        assert ألكيمي.ادخل_صف is sa.insert

    def test_update_alias(self, ألكيمي):
        assert ألكيمي.حدث_صفوف is sa.update

    def test_delete_alias(self, ألكيمي):
        assert ألكيمي.احذف_صفوف is sa.delete

    def test_and_alias(self, ألكيمي):
        assert ألكيمي.اجتماع is sa.and_

    def test_or_alias(self, ألكيمي):
        assert ألكيمي.افتراق is sa.or_

    def test_not_alias(self, ألكيمي):
        assert ألكيمي.نفي is sa.not_

    def test_func_alias(self, ألكيمي):
        assert ألكيمي.داله_sql is sa.func

    def test_case_alias(self, ألكيمي):
        assert ألكيمي.حاله_sql is sa.case

    def test_cast_alias(self, ألكيمي):
        assert ألكيمي.حول_نوع is sa.cast

    def test_literal_alias(self, ألكيمي):
        assert ألكيمي.قيمه_حرفيه_sql is sa.literal

    def test_label_alias(self, ألكيمي):
        assert ألكيمي.وسم_عمود is sa.label


class TestSqlaOrmQueryHelpers:
    def test_query_alias(self, ألكيمي):
        from sqlalchemy.orm import Query

        assert ألكيمي.كائن_استعلام_orm is Query

    def test_joinedload_alias(self, ألكيمي):
        from sqlalchemy.orm import joinedload

        assert ألكيمي.تحميل_مدمج is joinedload

    def test_subqueryload_alias(self, ألكيمي):
        from sqlalchemy.orm import subqueryload

        assert ألكيمي.تحميل_فرعي is subqueryload

    def test_selectinload_alias(self, ألكيمي):
        from sqlalchemy.orm import selectinload

        assert ألكيمي.تحميل_بالاختيار is selectinload

    def test_contains_eager_alias(self, ألكيمي):
        from sqlalchemy.orm import contains_eager

        assert ألكيمي.يحوي_فورا is contains_eager

    def test_defer_alias(self, ألكيمي):
        from sqlalchemy.orm import defer

        assert ألكيمي.اجل_تحميل is defer

    def test_undefer_alias(self, ألكيمي):
        from sqlalchemy.orm import undefer

        assert ألكيمي.الغ_تاجيل is undefer


class TestSqlaResults:
    def test_row_alias(self, ألكيمي):
        assert ألكيمي.صف_نتيجه is sa.Row

    def test_result_alias(self, ألكيمي):
        assert ألكيمي.نتيجه_استعلام is sa.Result

    def test_scalar_result_alias(self, ألكيمي):
        assert ألكيمي.نتيجه_عدديه is sa.ScalarResult

    def test_cursor_result_alias(self, ألكيمي):
        assert ألكيمي.نتيجه_مؤشر is sa.CursorResult


class TestSqlaExceptions:
    def test_sqlalchemy_error_alias(self, ألكيمي):
        from sqlalchemy.exc import SQLAlchemyError

        assert ألكيمي.خطا_sqlalchemy is SQLAlchemyError

    def test_integrity_error_alias(self, ألكيمي):
        from sqlalchemy.exc import IntegrityError

        assert ألكيمي.خطا_تكامل_orm is IntegrityError

    def test_operational_error_alias(self, ألكيمي):
        from sqlalchemy.exc import OperationalError

        assert ألكيمي.خطا_تشغيلي is OperationalError

    def test_no_result_found_alias(self, ألكيمي):
        from sqlalchemy.exc import NoResultFound

        assert ألكيمي.لا_نتيجه is NoResultFound

    def test_multiple_results_found_alias(self, ألكيمي):
        from sqlalchemy.exc import MultipleResultsFound

        assert ألكيمي.نتائج_متعدده is MultipleResultsFound


class TestSqlaFunctional:
    """End-to-end ORM smoke tests using the Arabic aliases.

    Builds a tiny ``users`` table on an in-memory SQLite engine and exercises
    insert / select / update / delete via the proxied API.
    """

    @pytest.fixture()
    def setup(self, ألكيمي):
        from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

        class Base(DeclarativeBase):
            pass

        class User(Base):
            __tablename__ = "users"
            id: Mapped[int] = mapped_column(ألكيمي.نوع_عدد_صحيح, primary_key=True)
            name: Mapped[str] = mapped_column(ألكيمي.نوع_نص(50), nullable=False)

        engine = ألكيمي.انشئ_محرك("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        return engine, Base, User

    def test_create_engine_returns_engine(self, ألكيمي):
        eng = ألكيمي.انشئ_محرك("sqlite:///:memory:")
        assert eng.dialect.name == "sqlite"

    def test_insert_and_select(self, ألكيمي, setup):
        engine, Base, User = setup
        Session = ألكيمي.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="ali"))
            s.add(User(name="omar"))
            s.commit()
            stmt = ألكيمي.اختر_من(User).where(User.name == "ali")
            row = s.execute(stmt).scalar_one()
            assert row.name == "ali"

    def test_or_filter(self, ألكيمي, setup):
        engine, Base, User = setup
        Session = ألكيمي.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add_all([User(name="a"), User(name="b"), User(name="c")])
            s.commit()
            stmt = ألكيمي.اختر_من(User).where(
                ألكيمي.افتراق(User.name == "a", User.name == "c")
            )
            names = sorted(r.name for r in s.execute(stmt).scalars())
            assert names == ["a", "c"]

    def test_update_construct(self, ألكيمي, setup):
        engine, Base, User = setup
        Session = ألكيمي.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="x"))
            s.commit()
            stmt = ألكيمي.حدث_صفوف(User).where(User.name == "x").values(name="y")
            s.execute(stmt)
            s.commit()
            got = s.execute(ألكيمي.اختر_من(User)).scalar_one()
            assert got.name == "y"

    def test_delete_construct(self, ألكيمي, setup):
        engine, Base, User = setup
        Session = ألكيمي.صانع_جلسات(bind=engine)
        with Session() as s:
            s.add(User(name="z"))
            s.commit()
            stmt = ألكيمي.احذف_صفوف(User).where(User.name == "z")
            s.execute(stmt)
            s.commit()
            count = s.execute(
                ألكيمي.اختر_من(ألكيمي.داله_sql.count()).select_from(User)
            ).scalar()
            assert count == 0

    def test_text_construct(self, ألكيمي):
        eng = ألكيمي.انشئ_محرك("sqlite:///:memory:")
        with eng.connect() as conn:
            result = conn.execute(ألكيمي.نص_خام("SELECT 1"))
            assert result.scalar() == 1

    def test_no_result_found_raises(self, ألكيمي, setup):
        engine, Base, User = setup
        Session = ألكيمي.صانع_جلسات(bind=engine)
        with Session() as s:
            stmt = ألكيمي.اختر_من(User).where(User.id == 9999)
            with pytest.raises(ألكيمي.لا_نتيجه):
                s.execute(stmt).scalar_one()
