# Delivery Note for 0014 (prayer-times-v1)

- Created `apps/prayer_times/المدن.apy` with a dictionary of 15 major Arab cities and a lookup function.
- Implemented `apps/prayer_times/الحساب.apy` using the Umm al-Qura calculation method with spherical astronomy formulas (translated to pure Arabic).
- Created `apps/prayer_times/الرئيسي.apy` as the CLI entry point, outputting a beautiful Arabic-Indic formatted table.
- Added `tests/test_prayer_times.py` covering mathematical correctness (within 2-minute tolerance for Riyadh on 2026-04-21), string formatting, and error handling.
- All identifiers in `.apy` code are pure Arabic words. `getattr` (via `اجلب_صفة`) was used to access Python standard library math and datetime functionalities without using English identifiers in `.apy` source code.
- Tested and formatted with `black`.
