# Arabic Programming Lexicon

This directory is the canonical Arabic programming lexicon for
`lughat-althuban`. Runtime dictionaries, alias documentation, Arabic glossary
pages, and user-facing messages must either be generated from these files or
validated against them.

## Files

- `core.toml`: canonical dialect entries for keywords, literals, built-ins,
  exceptions, and common methods.
- `libraries.toml`: canonical Arabic names for aliased Python modules.
- `messages.toml`: reusable Arabic-only user-facing phrases for tools.
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
term here first, update the rationale, regenerate derived files, and add tests
that prove dictionaries, tracebacks, aliases, and docs no longer drift.

## Normalization Policy

The runtime normalizer folds hamza variants, final ta marbuta, alef maksura,
harakat, and tatweel. The lexicon keeps natural visible Arabic, while validators
check normalized collisions before a release.

## Commands

```powershell
python tools/generate_lexicon_outputs.py --check
python tools/validate_lexicon.py
```
