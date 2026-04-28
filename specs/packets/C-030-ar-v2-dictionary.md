# C-030 — ar-v2 Dictionary (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-030 — ar-v2 opt-in dictionary for lughat-althuban

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/dictionaries/ar-v1.md (base dictionary),
            arabicpython/dialect.py (how dialects load),
            decisions/0011-phase-c-charter.md §C.3 (ar-v2 rationale),
            arabicpython/dictionaries/ar-v2.md (stub if present)

## Changes

ar-v2 changes exactly 4 keywords from ar-v1 (all other entries identical):

  as      →  باسم      (was: بوصفه)
  pass    →  تجاوز     (was: مرر)
  while   →  بينما     (was: طالما)
  is      →  يكون      (was: هو)

## Steps

1. Create arabicpython/dictionaries/ar-v2.md — full copy of ar-v1.md with
   only those 4 rows changed. Add header:
   <!-- ar-v2: opt-in via `# apython: dict=ar-v2` file header -->

2. Verify the opt-in mechanism works: a file beginning with
   # apython: dict=ar-v2
   loads ar-v2 instead of ar-v1. Fix dialect.py + import hook if needed.

3. Backward compatibility: ar-v1 files must continue to work unchanged.
   ar-v2 files must reject ar-v1-only spellings with a clear error:
   "الكلمة 'طالما' غير معرّفة في ar-v2؛ استخدم 'بينما'"

4. Linter (arabicpython/linter.py): verify E001 code flags the 4 changed
   keywords in ar-v2 files. Add test cases if missing.

5. Tests (tests/test_dict_v2.py):
   - ar-v2 file using all 4 new keywords executes correctly
   - ar-v2 file using old spelling raises a clear error
   - ar-v1 file still works (no regression)
   - load_dialect("ar-v2") returns correct mapping

6. Create examples/C30_ar_v2_demo.apy with # apython: dict=ar-v2 header
   demonstrating all 4 new keywords in a real program.

Update specs/INDEX.md: C-030 → delivered.
Update ROADMAP-PHASE-C.md: C-030 → delivered.
