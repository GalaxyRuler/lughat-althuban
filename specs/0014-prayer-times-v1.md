# Spec Packet 0014: prayer-times-v1

**Phase**: A (showcase app)
**Depends on**: 0001–0011 all merged (0013 can run in parallel)
**Estimated size**: small (1 session)

## Goal

Build a prayer time calculator written entirely in apython (`.apy` files). Given
a city name or geographic coordinates, it calculates the five daily Islamic
prayer times using real spherical astronomy formulas and displays them in a
beautiful formatted Arabic table using Arabic-Indic numerals. No external
library. Every identifier in the source is Arabic. This app demonstrates that
apython can implement real mathematical/scientific computation in readable Arabic
code — and tells the story that Arab astronomers invented the mathematics behind
this very calculation a thousand years ago.

## Non-goals

- Does not use any third-party library. stdlib only (`math`, `datetime`, `sys`).
- Does not connect to the internet.
- Does not provide a GUI — terminal output only.
- Does not handle Qibla direction, Hijri calendar conversion, or adhan audio.
- Does not modify any existing project file outside `apps/prayer_times/` and
  `tests/test_prayer_times.py`.

## Files

### Files to create

```
apps/
└── prayer_times/
    ├── المدن.apy
    ├── الحساب.apy
    └── الرئيسي.apy

tests/
└── test_prayer_times.py
```

---

## Calculation method: Umm al-Qura (أم القرى)

Use the Umm al-Qura method — the official method of Saudi Arabia and the Arab
world. All formulas below use degrees; convert to radians where `math` requires.

### Step 1 — Julian Day Number

```
JD = 367×Y - INT(7×(Y + INT((M+9)/12)) / 4) + INT(275×M/9) + D + 1721013.5
```
Where Y=year, M=month, D=day. UT=0 (calculate for local midnight then shift).

### Step 2 — Sun's position

```
d  = JD - 2451543.5                        # days since J2000
g  = 357.529 + 0.98560028 × d             # mean anomaly (degrees, normalize 0–360)
q  = 280.459 + 0.98564736 × d             # mean longitude (degrees, normalize 0–360)
L  = q + 1.915 × sin(g) + 0.020 × sin(2g) # ecliptic longitude
e  = 23.439 - 0.00000036 × d              # obliquity of ecliptic
RA = atan2(cos(e) × sin(L), cos(L))       # right ascension (degrees)
D  = asin(sin(e) × sin(L))                # solar declination (degrees)
EqT = q/15 - RA/15                         # equation of time (hours, RA in degrees/15)
```
Normalize angles to 0–360 range after each step: `angle % 360`.

### Step 3 — Solar noon (الظهر)

```
ظهر = 12 - EqT - (خط_الطول / 15 - المنطقة_الزمنية)
```
Result is a decimal hour in local time.

### Step 4 — Hour angle for prayer angles

For a given solar depression angle `α` (negative = below horizon):
```
cos(H) = (sin(α) - sin(خط_العرض) × sin(D)) / (cos(خط_العرض) × cos(D))
```
If `|cos(H)| > 1`: sun never reaches that angle (polar day/night). Handle
gracefully: print `"---"` for that prayer.

`H` in degrees = `acos(cos(H))`.

**Prayer angles (Umm al-Qura):**

| الصلاة | الزاوية / الطريقة |
|--------|------------------|
| الفجر | α = -18.5° → وقت الظهر - H/15 |
| الشروق | α = -0.833° → وقت الظهر - H/15 (not a prayer, used internally) |
| الظهر | Solar noon (Step 3) |
| العصر | Shadow method (Step 5 below) |
| المغرب | α = -0.833° → وقت الظهر + H/15 (same H as sunrise) |
| العشاء | المغرب + 1.5 ساعة (Umm al-Qura fixed interval) |

### Step 5 — Asr time (shadow factor = 1, Shafi'i)

```
Asr_angle = -acot(1 + tan(|خط_العرض - D|))   # result is negative (below horizon reference)
```
Use `acot(x) = atan(1/x)` when x > 0, `atan(1/x) + π` when x < 0.
Then apply hour angle formula from Step 4 with this angle.

### Step 6 — Convert decimal hours to HH:MM

```python
دالة ساعات_إلى_نص(ساعات_عشرية):
    # round to nearest minute
    # handle next-day overflow (> 24) and previous-day (< 0)
    # return string like "04:21"
```

---

## Module specifications

### `المدن.apy`

A dictionary of major Arab cities with coordinates and UTC offset.
Implement as a module-level dict `المدن` and a lookup function.

```python
المدن = {
    "الرياض":   {"خط_العرض": 24.69, "خط_الطول": 46.72,  "المنطقة_الزمنية": 3},
    "مكة":      {"خط_العرض": 21.42, "خط_الطول": 39.83,  "المنطقة_الزمنية": 3},
    "المدينة":  {"خط_العرض": 24.47, "خط_الطول": 39.61,  "المنطقة_الزمنية": 3},
    "جدة":      {"خط_العرض": 21.54, "خط_الطول": 39.17,  "المنطقة_الزمنية": 3},
    "القاهرة":  {"خط_العرض": 30.06, "خط_الطول": 31.25,  "المنطقة_الزمنية": 2},
    "دبي":      {"خط_العرض": 25.20, "خط_الطول": 55.27,  "المنطقة_الزمنية": 4},
    "بغداد":    {"خط_العرض": 33.34, "خط_الطول": 44.40,  "المنطقة_الزمنية": 3},
    "عمّان":    {"خط_العرض": 31.95, "خط_الطول": 35.93,  "المنطقة_الزمنية": 3},
    "بيروت":    {"خط_العرض": 33.89, "خط_الطول": 35.50,  "المنطقة_الزمنية": 2},
    "تونس":     {"خط_العرض": 36.82, "خط_الطول": 10.17,  "المنطقة_الزمنية": 1},
    "الرباط":   {"خط_العرض": 34.02, "خط_الطول": -6.84,  "المنطقة_الزمنية": 1},
    "الكويت":   {"خط_العرض": 29.37, "خط_الطول": 47.98,  "المنطقة_الزمنية": 3},
    "أبوظبي":   {"خط_العرض": 24.47, "خط_الطول": 54.37,  "المنطقة_الزمنية": 4},
    "الدوحة":   {"خط_العرض": 25.29, "خط_الطول": 51.53,  "المنطقة_الزمنية": 3},
    "مسقط":     {"خط_العرض": 23.61, "خط_الطول": 58.59,  "المنطقة_الزمنية": 4},
}

دالة ابحث_عن_مدينة(الاسم):
    # tries exact match, then partial match (الاسم in key)
    # returns dict with خط_العرض, خط_الطول, المنطقة_الزمنية
    # raises خطأ_مفتاح if not found
```

### `الحساب.apy`

Class `حاسبة_الصلاة`:

```python
صنف حاسبة_الصلاة:
    دالة __init__(الذات, خط_العرض, خط_الطول, المنطقة_الزمنية):
        ...

    دالة احسب(الذات, السنة, الشهر, اليوم):
        # returns ordered dict:
        # {"الفجر": "04:21", "الشروق": "05:47", "الظهر": "11:52",
        #  "العصر": "15:18", "المغرب": "18:09", "العشاء": "19:39"}
        # Use "---" for any prayer that cannot be calculated (polar)

    # private helpers:
    دالة _رقم_يوليان(الذات, س, ش, ي):   ...
    دالة _موقع_الشمس(الذات, ي_يوليان):  ... # returns (الميل, EqT)
    دالة _زاوية_ساعة(الذات, الميل, الزاوية): ...  # returns H or None if polar
    دالة _وقت_العصر(الذات, الميل):       ...
    دالة _إلى_نص(الذات, ساعات):          ...  # decimal hours → "HH:MM"
```

### `الرئيسي.apy`

Entry point. Behavior:

1. **With city name argument**: `apython apps/prayer_times/الرئيسي.apy الرياض`
2. **With date argument**: `apython apps/prayer_times/الرئيسي.apy الرياض 2026-04-21`
3. **Interactive** (no args): prompts for city, uses today's date

**Output format** (use today's date from `datetime.date.today()`):

```
╔══════════════════════════════════════╗
║    أوقات الصلاة — الرياض             ║
║    الثلاثاء، ٢١ أبريل ٢٠٢٦           ║
╠══════════════════════════════════════╣
║  الفجر              ٠٤:٢١            ║
║  الشروق             ٠٥:٤٧            ║
║  الظهر              ١١:٥٢            ║
║  العصر              ١٥:١٨            ║
║  المغرب             ١٨:٠٩            ║
║  العشاء             ١٩:٣٩            ║
╠══════════════════════════════════════╣
║  الصلاة القادمة: المغرب  (بعد ٢:١٤)  ║
╚══════════════════════════════════════╝
```

**"الصلاة القادمة"** row: compare current time (`datetime.datetime.now()`) with
prayer times to find the next upcoming prayer. Show time remaining as `س:دد`
in Arabic-Indic digits.

**Arabic-Indic conversion** (same as 0013):
```python
دالة إلى_أرقام_عربية(نص_الرقم):
    جدول = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    ارجع نص_الرقم.translate(جدول)
```

**Day name in Arabic**: derive from `datetime.date.weekday()`:
```python
أيام_الأسبوع = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
```

**Month name in Arabic**:
```python
أشهر_السنة = ["يناير","فبراير","مارس","أبريل","مايو","يونيو",
               "يوليو","أغسطس","سبتمبر","أكتوبر","نوفمبر","ديسمبر"]
```

If city not found, print: `"المدينة غير موجودة. المدن المتاحة: ..."` listing all
keys of `المدن`, then exit with code 1.

---

## Implementation constraints

- **Python version**: 3.11+
- **Dependencies**: `math`, `datetime`, `sys` only.
- **All `.apy` identifiers in Arabic** — same rule as 0013.
- **Style**: `python -m black .` before committing (Python test file only).
- **Encoding**: UTF-8.
- **Accuracy target**: results must be within ±2 minutes of established prayer
  time apps for major cities on the test dates. Verify manually for Riyadh on a
  known date before submitting.

---

## Test requirements (`tests/test_prayer_times.py`)

Use known correct prayer times for Riyadh on 2026-04-21 (verify against
https://www.islamicfinder.org or similar before writing assertions — use
rounded values with ±2 min tolerance).

1. `test_arabic_indic_conversion`:
   - Input: `"04:21"`
   - Expected: `"٠٤:٢١"`

2. `test_julian_day_known_date`:
   - Input: 2000-01-01
   - Expected JD: `2451544.5` (±0.01)

3. `test_dhuhr_riyadh`:
   - Location: Riyadh (24.69°N, 46.72°E, UTC+3)
   - Date: 2026-04-21
   - Expected Dhuhr: between `"11:45"` and `"11:55"`

4. `test_fajr_riyadh`:
   - Same location and date
   - Expected Fajr: between `"04:15"` and `"04:30"`

5. `test_maghrib_riyadh`:
   - Same location and date
   - Expected Maghrib: between `"18:00"` and `"18:20"`

6. `test_isha_is_maghrib_plus_90_minutes`:
   - Isha time = Maghrib time + 90 minutes (Umm al-Qura rule)
   - Parse both times, assert difference is exactly 90 minutes

7. `test_all_six_prayers_returned`:
   - `احسب()` returns dict with exactly these keys:
     `{"الفجر", "الشروق", "الظهر", "العصر", "المغرب", "العشاء"}`

8. `test_city_lookup_riyadh`:
   - `ابحث_عن_مدينة("الرياض")` returns dict with `"خط_العرض"` ≈ 24.69

9. `test_city_lookup_partial`:
   - `ابحث_عن_مدينة("مكة")` returns a result without raising

10. `test_city_not_found`:
    - `ابحث_عن_مدينة("طوكيو")` raises `KeyError`

---

## Acceptance checklist

- [ ] `المدن.apy` contains all 15 cities with correct coordinates.
- [ ] `الحساب.apy` implements full Umm al-Qura calculation.
- [ ] Prayer times for Riyadh on 2026-04-21 are within ±2 min of reference.
- [ ] `الرئيسي.apy` works with city arg, city+date arg, and interactive mode.
- [ ] Output uses Arabic-Indic digits and box-drawing characters.
- [ ] "الصلاة القادمة" row shows correct next prayer and time remaining.
- [ ] All `.apy` identifiers are Arabic words.
- [ ] All 10 tests pass: `pytest tests/test_prayer_times.py`
- [ ] Full test suite still passes: `pytest` (no regressions).
- [ ] `python -m black .` passes.
- [ ] Committed and pushed. Delivery note at
  `specs/0014-prayer-times-v1.delivery.md`.
