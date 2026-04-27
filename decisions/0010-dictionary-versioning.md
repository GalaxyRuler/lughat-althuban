# ADR 0010 — Dictionary versioning policy

**Date**: 2026-04-27  
**Status**: accepted  
**Supersedes**: none  
**Cited by**: `dictionaries/ar-v1.1.md`, spec B-040  

---

## Context

Phase A shipped `ar-v1.md` as the canonical Arabic Python dictionary and locked it
permanently per ADR 0008 § B.0. Phase B then shipped `ar-v2.md` as the active
dictionary (ADR 0009), which is a superset of v1 with a handful of changed entries
(`as`, `is`, `RecursionError`, three new OSError subclasses).

Spec B-040 called for a third dictionary — `ar-v1.1` — to add four keywords
(`async`, `await`, `match`, `case`) that were absent when the spec was written.
By the time B-040 was implemented, three of those four were already present in
`ar-v1.md`. The one genuine addition was `متزامن` → `async`: a shorter MSA term
that the spec recommended but that `ar-v1` never adopted (it used `غير_متزامن`).

This ADR records the versioning precedent set by that first successor dictionary.

---

## Decision

### 1. Versioning scheme

Dictionary files live in `dictionaries/` and are named `ar-vMAJOR.MINOR.md` (e.g.
`ar-v1.1.md`) or `ar-vMAJOR.md` as shorthand for `ar-vMAJOR.0`. The loader
accepts either form: `load_dialect("ar-v1.1")` resolves to
`dictionaries/ar-v1.1.md`.

Minor versions (`ar-v1.1`, `ar-v1.2`, …) are **strict supersets** of the
preceding minor version: every `(Arabic, Python)` pair from `ar-vX.Y` must
appear identically in `ar-vX.Y+1`. The test
`tests/test_dictionary_v1_1.py::test_v1_1_is_strict_superset_of_v1` enforces
this programmatically.

Major versions (`ar-v2`, `ar-v3`, …) may change or remove entries from the
preceding major version; they require their own ADR.

### 2. Multiple Arabic spellings for the same Python symbol

`ar-v1.1` introduces the first case where two Arabic words both map to the same
Python keyword (`غير_متزامن` and `متزامن` both → `async`). The dialect loader
allows this: the forward map (Arabic → Python) is still one-to-one, but the
reverse map (Python → Arabic) records the first canonical seen. No error is
raised when a second Arabic word maps to an existing Python symbol.

This is intentional: future minor versions may add alternate spellings for
usability without breaking existing code. Programs using the original spelling
always continue to work.

### 3. Selecting a dictionary at runtime

Three mechanisms select the dictionary, in decreasing precedence:

| Mechanism | Example | Scope |
|---|---|---|
| `--dict` CLI flag | `ثعبان --dict ar-v1.1 file.apy` | invocation |
| Per-file directive | `# arabicpython: dict=ar-v1.1` in first 5 lines | file |
| Default | `ar-v2` | global |

The `translate()` function accepts a `dict_version: str | None` keyword argument
(None → use current default). Supplying both `dialect` and `dict_version` raises
`ValueError`.

If the `--dict` flag and the per-file directive are both present and disagree,
the CLI exits with code 1 and prints both versions to stderr. Explicit always
wins over implicit; ambiguity is a hard error.

### 4. Backward compatibility guarantee

A `.apy` file with no directive and run without `--dict` uses `ar-v2` — the same
behaviour as before B-040. No existing program is silently upgraded or broken.

The `ar-v1.md` file is byte-frozen; any modification is caught by the SHA-256
snapshot in `tests/test_dictionary_v1_1.py::test_v1_file_unchanged`.

### 5. What requires a new ADR

- Removing any entry from a dictionary (major version bump)
- Changing the Python symbol an Arabic word maps to (major version bump)
- Adding a new `dict_version` selection mechanism beyond the three above
- Deprecating or removing an existing dictionary version

---

## Consequences

- `ar-v1.1.md` ships with one new entry (`متزامن` → `async`), giving Arabic
  programmers the shorter recommended spelling for coroutine definitions.
- The `--dict` flag and per-file directive give individual files and invocations
  explicit control over which dictionary is active, without affecting the global
  default.
- The precedent for minor-version dictionaries is established: future packets
  (e.g. B-040b, type alias keyword) can ship as `ar-v1.2` following the same
  strict-superset rule.
- The dialect loader's reverse-map now allows many-to-one Arabic → Python
  mappings, which is a small relaxation of the previous strict bijection. The
  forward map (Arabic → Python) remains strictly one-to-one.

---

## Alternatives considered

**Keep a single mutable dictionary**: rejected. ADR 0008 § B.0 explicitly freezes
`ar-v1` for the lifetime of Phase A. Mutating it would invalidate any program
pinned to v1 behaviour.

**Use `ar-v2.1` instead of `ar-v1.1`**: rejected. `ar-v2` already changes `as`
and `is` from `ar-v1`; a strict-superset extension of v1 is a different thing.
Programs on `ar-v1.1` get `متزامن` without the `as`/`is` changes in `ar-v2`.

**Alias `متزامن` directly in `ar-v2`**: possible, but `ar-v2` is already shipped.
Adding entries to a released major version requires an ADR per § 5. A minor
version is the lighter-weight path.
