# C-014 — click aliases (Implementation Prompt)

**Depends on:** C-001 ✅  
**Size:** S  

---

## Task

Implement C-014 — Arabic aliases for the `click` CLI library

Repository: https://github.com/GalaxyRuler/lughat-althuban
Read first: arabicpython/aliases/flask.toml (TOML format),
            arabicpython/aliases/_loader.py (what fields [meta] requires),
            specs/INDEX.md

## Steps

Create: arabicpython/aliases/click.toml
Arabic module name: كليك

Required [meta]:
  arabic_name    = "كليك"
  python_module  = "click"
  dict_version   = "ar-v1"
  schema_version = 1

Required [entries] — cover all commonly used click symbols:
  Decorators: command, group, option, argument, pass_context, pass_obj,
              make_pass_decorator, version_option, help_option
  Core classes: BaseCommand, Command, Group, Argument, Option,
                Context, Parameter
  Types: STRING, INT, FLOAT, BOOL, UUID, File, Path, Choice,
         IntRange, FloatRange, DateTime, Tuple
  Functions: echo, style, secho, prompt, confirm, pause, clear,
             get_terminal_size, format_filename, open_file,
             get_current_context, make_context
  Exceptions: ClickException, UsageError, BadParameter, Abort, Exit

Arabic naming guide:
  command → امر, group → مجموعه, option → خيار, argument → معامل,
  echo → اطبع, style → نسق, prompt → اسال, confirm → اكد,
  Context → سياق, Choice → اختيار, File → ملف, Path → مسار,
  ClickException → خطا_نقر, UsageError → خطا_استخدام

Create: examples/C14_click_demo.apy — a small CLI tool in Arabic using click:
  a command group with two subcommands, one with --option flags,
  one with arguments. Demonstrate echo, style, prompt.

Create: tests/test_aliases_click.py — at minimum:
  - import كليك works
  - كليك.امر is click.command
  - TOML loads without error
  - CliRunner integration test of the demo commands

Register the alias in arabicpython/aliases/__init__.py and add كليك
to the alias finder.

Update specs/INDEX.md: C-014 → delivered.
