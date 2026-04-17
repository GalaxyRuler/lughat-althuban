# 0002 — File extension: `.apy`

**Status**: accepted
**Date**: 2026-04-17
**Deciders**: project planner

## Context

The dialect needs a file extension that distinguishes its files from plain Python. The extension affects: shell tooling, editor syntax recognition, git/GitHub rendering, import hooks, CI pipelines, and first impressions. Once published it is effectively irreversible because third-party tooling and documentation will bake it in.

Candidates considered:
- `.apy` — "Arabic Python" initialism, ASCII only
- `.arpy` — longer-form, ASCII only
- `.pyar` — variant of the above
- `.py` — piggyback on existing extension, disambiguate by content
- `.بايثون` — symbolic native-script choice
- `.عربي.py` — hybrid

## Decision

**Use `.apy` as the primary and only file extension.**

The import hook's `MetaPathFinder` recognizes `.apy`. No aliases are accepted in v1; adding an alias later is additive and safe, removing one is not.

## Consequences

**Positive:**
- ASCII-only extension works on every filesystem, shell, and CI pipeline without Unicode-normalization hazards.
- Three characters is memorable and fast to type.
- Short enough to work well as a CLI namespace: `apython`, `apyc` (future bytecode), `.apy` extension.
- No collision with existing Python tooling that assumes `.py` files are executable Python.

**Negative:**
- Loses some symbolic value. A file ending in `.بايثون` would be a small act of cultural affirmation every time a learner sees it. We accept the loss because tooling compatibility matters more.
- Slightly ambiguous: "apy" could be read as "apathy" or misread in RTL rendering contexts. Not a major concern but worth noting.

**Neutral:**
- The Python *package* name is `arabicpython`, not `apython`. This separates the installable namespace (long, descriptive) from the file extension and CLI (short). `apython` is the CLI name and the repo name.

## Alternatives considered

**`.py`, disambiguated by shebang or magic comment.** Rejected. Creates a two-class system where every tool must inspect file contents to know what it's dealing with. Editors and linters will treat these files as plain Python and produce misleading errors.

**`.بايثون` (Arabic for "python").** Rejected on tooling grounds. Windows filesystems, git for Windows, older shells, some editor plugins, and many CI systems normalize Unicode filenames inconsistently (NFC vs NFD). Even where they work, the rendering in LTR editor file trees is visually confusing. The symbolic value is real but not worth the daily friction.

**`.عربي.py` (double extension).** Rejected. Double extensions are a minor footgun: some tools treat everything after the first `.` as extension, others treat only the last. Mixed-script filenames reintroduce the bidi rendering issue.

**`.arpy` / `.pyar`.** Rejected. Longer and less memorable than `.apy` with no upside.

## Implementation notes

- The `MetaPathFinder` in Phase 2 must register `.apy` with the import system. It should NOT also match `.py` — that would cause `apython` to hijack every Python file on the system.
- Editor support (syntax highlighting, LSP) should key off `.apy` specifically.
- Consider registering a MIME type (`text/x-apython`) when Phase A is published.

## References

- Python import system: https://docs.python.org/3/reference/import.html
- Precedents: `.twpy`/`.cnpy` (zhpy), `.hedy` (Hedy)
