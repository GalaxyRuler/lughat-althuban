# Spec Packet NNNN: <short-name>

**Phase**: A | B
**Depends on**: packet numbers that must be merged first, or "—"
**Estimated size**: small (1 session) | medium (2–3 sessions) | large (break this up)

## Goal

One paragraph explaining what this packet delivers and why it matters in the larger plan. The reader should finish this paragraph knowing whether the packet is worth their time.

## Non-goals

Bulleted list of things this packet does NOT do. Prevents scope creep. Every item here is something a reasonable implementer might otherwise assume is in scope.

- Does not modify X.
- Does not handle Y.
- Does not introduce dependency Z.

## Files

### Files to create

- `path/to/new_file.py`
- `tests/test_new_file.py`

### Files to modify

- `path/to/existing_file.py` — what changes and why

### Files to read (do not modify)

- `path/to/reference.py` — what information to extract

## Public interfaces

Every function, class, or constant this packet must expose. Include full type annotations, docstring-level contracts, and 2–3 concrete input/output examples per interface. If the interface is a Protocol or ABC, specify it fully.

```python
def example(x: int, *, flag: bool = False) -> str:
    """One-line summary.

    Longer description if needed. State:
      - Preconditions
      - Postconditions
      - Exceptions raised and when
      - Side effects (should be "none" when possible)

    Examples:
      >>> example(5)
      '5'
      >>> example(5, flag=True)
      'FLAG:5'
      >>> example(-1)
      Traceback (most recent call last):
        ...
      ValueError: x must be non-negative
    """
```

## Implementation constraints

- **Python version**: 3.11+ unless otherwise specified.
- **Dependencies allowed**: stdlib only | list specific pinned packages.
- **Forbidden**: globals, module-level mutable state, `from X import *`, etc. (list per packet).
- **Style**: `ruff` and `black` at project defaults (line length 100).
- **Performance budget**: if any; e.g. "must translate a 1000-line file in <50 ms on a modern machine."
- **Security**: any packet-specific constraints beyond the project-wide ADRs.

## Test requirements

List every test this packet must include. Each test has:

- A name (`test_*`)
- Inputs (concrete, not abstract)
- Expected outputs or expected exceptions (with message fragment to assert on)

Tests ARE the acceptance criteria. When tests pass, the packet is done.

1. `test_XXX`:
   - Input: `...`
   - Expected: `...`
2. `test_YYY`:
   - Input: `...`
   - Expected: raises `ValueError` with message containing `"..."`

Edge cases that must be covered:
- Empty input
- Unicode edge cases (normalization forms, RTL/LTR mixing)
- Round-trip invariants (if applicable)

## Reference materials

Links to the minimum context Codex needs, pre-digested so it doesn't waste tokens researching:

- Decision docs: `decisions/NNNN-*.md` (which ones are load-bearing for this packet)
- Python stdlib docs: direct links to the relevant modules/functions
- Prior-art: specific file paths in zhpy, CPython, etc.
- Unicode references: specific code charts or tables

## Open questions for the planner

Empty is best. If a question is here, the packet is under-specified; Claude should answer it before Codex starts.

- ...

## Acceptance checklist

- [ ] All listed files created or modified.
- [ ] All listed tests present and passing.
- [ ] `ruff check .` passes.
- [ ] `black --check .` passes.
- [ ] `pytest` passes on Python 3.11.
- [ ] Delivery note `NNNN-short-name.delivery.md` written.
