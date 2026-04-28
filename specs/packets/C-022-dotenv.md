# C-022 — python-dotenv aliases (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-022 — Arabic aliases for `python-dotenv`

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/aliases/flask.toml (TOML format)

## Steps

Create: arabicpython/aliases/dotenv.toml
Arabic module name: دوت_إنف

Required [entries]:
  load_dotenv      →  حمل_البيئه
  dotenv_values    →  قيم_البيئه
  get_key          →  اجلب_مفتاح
  set_key          →  عيّن_مفتاح
  unset_key        →  احذف_مفتاح
  find_dotenv      →  ابحث_عن_بيئه

Create: examples/C22_dotenv_demo.apy — load a .env file, read a key,
  print it. Show both load_dotenv + os.environ and dotenv_values approaches.

Create: tests/test_aliases_dotenv.py — standard alias smoke tests.
Update specs/INDEX.md: C-022 → delivered.
