# Project Context

## Domain

`lughat-althuban` / Apython is an Arabic-first Python dialect built on CPython. The project lets authors write `.apy` files using Arabic keywords, library aliases, examples, docs, and user-facing messages while preserving normal Python behavior underneath.

## Core Concepts

- **Arabic-first source**: Public examples and showcase code should use Arabic identifiers, Arabic-facing text, and Arabic library aliases wherever practical.
- **Translator**: The runtime translates `.apy` source into normal Python syntax before execution.
- **Alias lexicon**: `lexicon/` is the canonical source for library alias names, generated alias TOML files, generated docs, and consistency checks.
- **Runtime aliases**: `arabicpython/aliases/` maps Arabic import names and member names to Python libraries and APIs.
- **Playground**: `docs/playground.html` and related `docs/` assets provide the GitHub Pages browser experience for trying examples.
- **Gallery examples**: `docs/gallery.html`, `docs/games/`, `docs/showcases/`, and `examples/` demonstrate what Arabic programming can do.
- **Arabic traceback/messages**: CLI and runtime output should make errors understandable to Arabic-speaking users without hiding Python compatibility.

## Engineering Boundaries

- Do not fork Python semantics. Prefer token translation, import hooks, alias wrappers, and generated data over creating a separate runtime model.
- Update `lexicon/` before changing generated alias docs or alias runtime outputs.
- Keep Arabic examples substantial enough to demonstrate real programming capability, not only toy text output.
- Preserve Windows validation behavior for Arabic text by setting `PYTHONIOENCODING=utf-8` when needed.

## Architecture Decisions

Architectural decision records live in `decisions/`. Read the relevant ADRs before changing language semantics, bidi behavior, normalization, lexicon governance, phase roadmaps, packaging, or playground architecture.
