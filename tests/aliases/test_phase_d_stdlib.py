import datetime
import os
import pathlib
import sys
import typing

ALIASES_DIR = pathlib.Path(__file__).parent.parent.parent / "arabicpython" / "aliases"


def _proxy(arabic_name: str):
    from arabicpython.aliases._finder import AliasFinder

    finder = AliasFinder(mappings_dir=ALIASES_DIR)
    spec = finder.find_spec(arabic_name, None, None)
    assert spec is not None, f"AliasFinder did not find {arabic_name!r}"
    return spec.loader.create_module(spec)


def test_phase_d_canonical_os_name():
    نظام = _proxy("نظام")
    assert نظام.الدليل_الحالي is os.getcwd
    assert نظام.مسار_نظام is os.path


def test_phase_d_canonical_sys_name():
    نظام_بايثون = _proxy("نظام_بايثون")
    assert نظام_بايثون.الوسائط is sys.argv


def test_phase_d_canonical_pathlib_name():
    مسار = _proxy("مسار")
    assert مسار.مسار is pathlib.Path


def test_phase_d_canonical_datetime_name():
    تاريخ_وقت = _proxy("تاريخ_وقت")
    assert تاريخ_وقت.تاريخ is datetime.date
    assert تاريخ_وقت.اليوم() == datetime.date.today()


def test_phase_d_typing_threading_and_os_path():
    تنميط = _proxy("تنميط")
    خيوط = _proxy("خيوط")
    مسار_نظام = _proxy("مسار_نظام")

    assert تنميط.اي is typing.Any
    from arabicpython.aliases._proxy import ClassFactory

    assert isinstance(خيوط.خيط, ClassFactory)
    assert مسار_نظام.يوجد is os.path.exists
