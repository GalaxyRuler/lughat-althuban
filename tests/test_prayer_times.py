import pytest

import arabicpython

arabicpython.install()

import apps.prayer_times.المدن as المدن  # noqa: E402, I001
import apps.prayer_times.الحساب as الحساب  # noqa: E402, I001
import apps.prayer_times.الرئيسي as الرئيسي  # noqa: E402, I001


def test_arabic_indic_conversion():
    assert الرئيسي.الى_ارقام_عربيه("04:21") == "٠٤:٢١"


def test_julian_day_known_date():
    calc = الحساب.حاسبة_الصلاه(0, 0, 0)
    jd = calc._رقم_يوليان(2000, 1, 1)
    assert abs(jd - 2451544.5) < 0.01


def test_dhuhr_riyadh():
    calc = الحساب.حاسبة_الصلاه(24.69, 46.72, 3)
    times = calc.احسب(2026, 4, 21)
    dhuhr = times["الظهر"]
    assert "11:45" <= dhuhr <= "11:55"


def test_fajr_riyadh():
    calc = الحساب.حاسبة_الصلاه(24.69, 46.72, 3)
    times = calc.احسب(2026, 4, 21)
    fajr = times["الفجر"]
    assert "04:00" <= fajr <= "04:10"


def test_maghrib_riyadh():
    calc = الحساب.حاسبة_الصلاه(24.69, 46.72, 3)
    times = calc.احسب(2026, 4, 21)
    maghrib = times["المغرب"]
    assert "18:00" <= maghrib <= "18:25"


def test_isha_is_maghrib_plus_90_minutes():
    calc = الحساب.حاسبة_الصلاه(24.69, 46.72, 3)
    times = calc.احسب(2026, 4, 21)
    maghrib = times["المغرب"]
    isha = times["العشاء"]
    m_parts = maghrib.split(":")
    i_parts = isha.split(":")
    m_mins = int(m_parts[0]) * 60 + int(m_parts[1])
    i_mins = int(i_parts[0]) * 60 + int(i_parts[1])
    assert i_mins - m_mins == 90


def test_all_six_prayers_returned():
    calc = الحساب.حاسبة_الصلاه(24.69, 46.72, 3)
    times = calc.احسب(2026, 4, 21)
    assert set(times.keys()) == {"الفجر", "الشروق", "الظهر", "العصر", "المغرب", "العشاء"}


def test_city_lookup_riyadh():
    city = المدن.ابحث_عن_مدينه("الرياض")
    assert abs(city["خط_العرض"] - 24.69) < 0.01


def test_city_lookup_partial():
    city = المدن.ابحث_عن_مدينه("مكة")
    assert city["خط_العرض"] == 21.42


def test_city_not_found():
    with pytest.raises(KeyError):
        المدن.ابحث_عن_مدينه("طوكيو")
