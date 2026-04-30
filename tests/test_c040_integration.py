from __future__ import annotations

import importlib
import pathlib
import sys

import pytest

pytest.importorskip("fastapi", reason="fastapi not installed")
pytest.importorskip("pymongo", reason="pymongo not installed")
pytest.importorskip("celery", reason="celery not installed")
pytest.importorskip("jwt", reason="PyJWT not installed")
pytest.importorskip("openpyxl", reason="openpyxl not installed")
pytest.importorskip("mongomock", reason="mongomock not installed")
pytest.importorskip("httpx", reason="httpx not installed")

from tests.test_phase_a_compat import PROJECT_ROOT, run_apy_program

EXAMPLES_DIR = PROJECT_ROOT / "examples"
DEMO = EXAMPLES_DIR / "C40_full_stack_demo.apy"


@pytest.fixture()
def clean_import_state():
    original_meta_path = list(sys.meta_path)
    original_path = list(sys.path)
    for name in (
        "C40_full_stack_demo",
        "فاست_أبي",
        "قاعده_وثائق",
        "مهام_خلفيه",
        "جي_دبليو_تي",
        "جداول_اكسل",
        "مجاري",
        "اسماء_بديله",
    ):
        sys.modules.pop(name, None)

    yield

    for name in (
        "C40_full_stack_demo",
        "فاست_أبي",
        "قاعده_وثائق",
        "مهام_خلفيه",
        "جي_دبليو_تي",
        "جداول_اكسل",
        "مجاري",
        "اسماء_بديله",
    ):
        sys.modules.pop(name, None)
    sys.meta_path[:] = original_meta_path
    sys.path[:] = original_path


def test_c040_demo_runs_end_to_end() -> None:
    rc, stdout, stderr = run_apy_program(DEMO, timeout=20.0, cwd=PROJECT_ROOT)

    assert rc == 0, f"C40 demo exited {rc}.\nstderr:\n{stderr}"
    assert stdout == "token issued\nreport generated\nphase c complete\n"
    assert stderr == ""


def test_c040_demo_exposes_arabic_methods_on_all_five_libraries(clean_import_state) -> None:
    from arabicpython.aliases import install as install_aliases
    from arabicpython.import_hook import install as install_apy

    install_apy()
    install_aliases()
    sys.path.insert(0, str(EXAMPLES_DIR))

    demo = importlib.import_module("C40_full_stack_demo")

    assert demo.وكيل_صنف is demo.اسماء_بديله.وكيل_صنف
    assert demo.حمل_خريطه is demo.اسماء_بديله.حمل_خريطه

    app = demo.تطبيق
    assert callable(app.انشر)
    assert callable(app.احصل_مسار)
    assert callable(app.ضم_موجه)
    assert demo.صفات_فاست["ترويسات"] == "headers"
    assert demo.عميل_اختبار_فاست.عميل_اختبار.__name__ == "TestClient"

    celery_app = demo.تطبيق_مهام
    assert callable(celery_app.ارسل_مهمه)
    assert callable(celery_app.توقيع_مهمه)
    task = demo.احسب_احصاءات
    async_result = task.اجل([{"المبلغ": 7}, {"المبلغ": 5}])
    result_proxy = demo.وكيل_صنف(async_result, demo.صفات_سيلري)
    assert result_proxy.جاهز()
    assert result_proxy.احصل_نتيجه() == {"عدد": 2, "المجموع": 12}

    mongo_client = demo.عميل_مونجو
    assert callable(mongo_client.احصل_قاعده_بيانات)
    assert demo.مونجو_وهمي.عميل_مونجو_وهمي.__name__ == "MongoClient"
    collection = demo.مجموعه_تقارير
    assert callable(collection.ادخل_واحد)
    assert callable(collection.اجمع)

    jwt_proxy = demo.جي_دبليو_تي
    assert callable(jwt_proxy.شفر)
    assert callable(jwt_proxy.فك_التشفير)

    excel_proxy = demo.جداول_اكسل
    workbook = excel_proxy.مصنف()
    assert callable(workbook.احفظ_مصنف)
    sheet = demo.وكيل_صنف(workbook.ورقه_نشطه, demo.صفات_اكسل)
    sheet.اضف_صف(["القسم", "المبلغ"])
    assert sheet.عدد_صفوف == 1


def test_c040_spec_exists() -> None:
    spec = pathlib.Path(PROJECT_ROOT / "specs" / "C-040-integration-demo-v1.md")
    assert spec.exists()
