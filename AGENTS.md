# AGENTS.md

## Project

`lughat-althuban` / Apython is an Arabic-first Python dialect implemented on top of CPython. `.apy` files are translated at load/run time without forking Python, and the project includes runtime aliases, traceback translation, formatter/linter tooling, a pytest plugin, docs, examples, and playground assets.

## Working Rules

- Keep user-facing examples, docs, names, and showcase work Arabic-first. English can support maintainer clarity, but it should not replace the Arabic programming experience.
- Treat `lexicon/` as the source of truth for core words, aliases, messages, and generated docs. When changing terms, update the lexicon first, then regenerate/check outputs.
- Preserve compatibility with normal CPython semantics. The dialect should translate tokens and aliases without inventing a separate language runtime.
- Be careful with Windows console output. Set `$env:PYTHONIOENCODING="utf-8"` before validating Arabic stdout/stderr or commands that print Arabic.
- Avoid one-letter Arabic names in tests or examples when they normalize into Python keywords; a known trap is `ك`, which normalizes to `as`.
- Do not silently downgrade Arabic coverage in examples, gallery pages, or docs. Substantial examples should demonstrate real programs, not toy snippets.

## Common Commands

```powershell
python -m pip install -e ".[dev]"
$env:PYTHONIOENCODING="utf-8"
python -m pytest
ruff check .
black --check .
python tools/validate_lexicon.py
python tools/generate_lexicon_outputs.py --check
ثعبان --help
ثعبان --version
```

For full optional library and AI alias coverage:

```powershell
python -m pip install -e ".[all]"
python -m pytest
```

## Important Files

- `README.md` - current public project status and Arabic-first overview.
- `CONTRIBUTING.md` - contribution and verification checklist.
- `ROADMAP-PHASE-D.md` - current active roadmap.
- `decisions/` - architectural decisions and phase charters.
- `lexicon/` - canonical terms and generated output inputs.
- `arabicpython/` - translator, runtime, aliases, CLI, formatter, linter, traceback tooling.
- `examples/` and `docs/` - public examples, gallery, Arabic docs, and showcase material.
- `tests/` - pytest suite, including `.apy` plugin coverage.

## Definition of Done

- Run the narrowest useful tests first, then the broader suite when touching shared translation, lexicon, CLI, import hook, traceback, formatter, linter, or docs generation behavior.
- Generated lexicon outputs are checked or refreshed.
- Arabic CLI examples are manually smoke-tested when changing command behavior.
- Public-facing Arabic text remains idiomatic and consistent with the lexicon.

## Agent skills

### Issue tracker

Issues are tracked in GitHub Issues for `GalaxyRuler/lughat-althuban`. See `docs/agents/issue-tracker.md`.

### Triage labels

Triage uses the repo's GitHub label vocabulary, with `question` for info requests and `help wanted` for human-ready work. See `docs/agents/triage-labels.md`.

### Domain docs

This is a single-context repo with root `CONTEXT.md` and ADR-style decisions in `decisions/`. See `docs/agents/domain.md`.
