# C-015 — rich aliases (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-015 — Arabic aliases for the `rich` terminal library

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/aliases/flask.toml (TOML format),
            arabicpython/aliases/__init__.py (registration pattern)

## Steps

Create: arabicpython/aliases/rich.toml
Arabic module name: ريتش

Required [entries] — cover the main rich surface:
  Console, print (rich's print), inspect, Pretty
  Table, Column, box (box styles)
  Progress, track, TaskID, BarColumn, TextColumn, TimeElapsedColumn
  Panel, Group, Rule, Padding, Align
  Markdown, Syntax, Pretty, JSON
  Spinner, Live
  Text, Style, Color
  tree.Tree, tree.add
  logging.RichHandler
  Prompt, Confirm (from rich.prompt)
  status (context manager)

Arabic naming guide:
  Console → وحده_التحكم, print → اطبع, Table → جدول,
  Panel → لوحه, Progress → تقدم, track → تتبع,
  Markdown → نص_تنسيق, Syntax → بناء_جمله, Spinner → دوار,
  Live → مباشر, Text → نص_منسق, Rule → فاصل,
  Prompt → مطالبه, Confirm → تاكيد, Tree → شجره

Create: examples/C15_rich_demo.apy — demonstrate:
  Console output with styles, a Table with data rows, a Panel,
  a Progress bar tracking a loop, a Markdown render.

Create: tests/test_aliases_rich.py:
  - import ريتش works
  - Core symbols resolve correctly
  - Console can be instantiated via وحده_التحكم

Update specs/INDEX.md: C-015 → delivered.
