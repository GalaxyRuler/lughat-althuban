# C-023 — PyYAML aliases (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-023 — Arabic aliases for `PyYAML` (import yaml)

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/aliases/flask.toml (TOML format)

## Steps

Create: arabicpython/aliases/yaml.toml
Arabic module name: يامل

Required [entries]:
  safe_load        →  حمل_آمن
  safe_dump        →  صدّر_آمن
  full_load        →  حمل_كامل
  safe_load_all    →  حمل_آمن_الكل
  safe_dump_all    →  صدّر_آمن_الكل
  dump             →  صدّر
  load             →  حمل
  YAMLError        →  خطا_يامل
  Loader           →  محمّل
  SafeLoader       →  محمّل_آمن
  Dumper           →  مصدّر
  SafeDumper       →  مصدّر_آمن
  add_constructor  →  اضف_منشئ
  add_representer  →  اضف_ممثّل

Create: examples/C23_yaml_demo.apy — serialize a dict to YAML string,
  deserialize back, verify round-trip.

Create: tests/test_aliases_yaml.py — standard alias smoke tests.
Update specs/INDEX.md: C-023 → delivered.
