# Arabic Programming Lexicon

This directory is the canonical Arabic programming lexicon for
`lughat-althuban`. Runtime dictionaries, alias TOMLs, alias documentation,
Arabic glossary pages, traceback message tables, and user-facing messages must
either be generated from these files or validated against them.

## Files

- `core.toml`: canonical dialect entries for keywords, literals, built-ins,
  exceptions, and common methods.
- `libraries.toml`: canonical Arabic names for aliased Python modules, import
  compatibility aliases, `[entries]`, `[attributes]`, optional extras, entry
  floors, and proxy-class metadata.
- `messages.toml`: reusable Arabic-only user-facing phrases for tools, plus
  traceback exception/message localization patterns.
- `schema.json`: structural contract for the TOML files.

## Governance

Every entry records:

- the Python symbol;
- the visible Arabic canonical spelling;
- rejected or non-canonical alternates;
- the rationale for the Arabic choice.

The visible spelling is what learners see in documentation, diagnostics, and
tooltips. Runtime lookup still applies the normalizer, so variants such as
`خطأ` and `خطا` resolve together where the dialect accepts an identifier.

Changing an existing canonical term is a compatibility decision. Add the new
term here first, preserve an old non-conflicting import spelling in
`arabic_aliases` when needed, regenerate derived files, and add tests that prove
dictionaries, tracebacks, aliases, and docs no longer drift.

Do not edit generated outputs by hand. Files under `arabicpython/aliases/*.toml`,
`arabicpython/_generated_messages.py`,
`arabicpython/_generated_traceback_data.py`, generated dictionary markdown, and
generated Arabic lexicon/index docs all carry a generated-file header. Their
reviewable source is this directory.

## Normalization Policy

The runtime normalizer folds hamza variants, final ta marbuta, alef maksura,
harakat, and tatweel. The lexicon keeps natural visible Arabic, while validators
check normalized collisions before a release.

## Commands

```powershell
python tools/generate_lexicon_outputs.py --check
python tools/validate_lexicon.py
python -m pytest tests/test_aliases_toml_invariants.py tests/test_reverse.py tests/test_tracebacks_arabic.py
```
