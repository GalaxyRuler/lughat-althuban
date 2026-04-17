# apython — Arabic Python

A Python dialect where keywords, built-ins, and exceptions are written in Arabic.

**Status**: Phase 0 — design decisions. No working code yet.
**Scope**: Two-phase project. Phase A ships a learning dialect; Phase B builds a production replacement.
**License**: Apache 2.0.
**Repo**: Private until Phase A ships.

## What this is

`apython` lets you write Python programs in Arabic:

```python
# This will run after Phase A is complete
دالة مرحبا(اسم):
    اطبع(f"مرحبا يا {اسم}")

إذا __name__ == "__main__":
    مرحبا("عالم")
```

Under the hood, your `.apy` file is translated to standard Python at load time and executed by CPython. No interpreter fork for Phase A.

## Why

Arabic-speaking learners — especially children and adults whose English literacy is the barrier, not their reasoning ability — benefit from native-language syntax. Precedents exist (Hedy, قلب/Qalb, Kalimat) but none targeted Python specifically.

Production use in Arabic is a harder problem — see `decisions/0007-scope.md` and the 9-layer analysis in `docs/architecture-overview.md` (forthcoming). Phase B addresses it.

## Project structure

```
apython/
├── decisions/        ADRs for every architectural choice (immutable once accepted)
├── dictionaries/     Arabic↔English symbol tables, curated data
├── specs/            Handoff packets from planner to implementer
├── arabicpython/     Python package (the actual transpiler) — empty until Phase A
├── tests/            pytest suite — empty until Phase A
├── examples/         .apy programs — empty until Phase A
├── docs/             Longer-form design docs
└── .github/workflows/ CI
```

## Development model

This project uses a **planner/implementer split**:

- **Claude** (planner): writes ADRs, curates dictionaries, authors spec packets, reviews code.
- **Codex** (implementer): reads spec packets, writes code, runs tests, iterates.

Every unit of work is a spec packet in `specs/`. Codex produces a delivery note alongside the packet when done. Claude reviews the diff and either approves or writes a fix-up packet.

See `specs/0000-template.md` for the packet format.

## Roadmap

| Phase | Content | Status |
|---|---|---|
| 0 | Design decisions (ADRs) | in progress |
| A | Learning dialect: tokenizer + import hook + REPL + translated tracebacks | not started |
| B | Production replacement: aliasing, stdlib port, CPython fork, tooling | not started |

## Acknowledgements

- **zhpy** (gasolin, 2014): the tokenize-based Chinese Python dialect that the core architecture is modeled on.
- **Ramsey Nasser's قلب (Qalb)**: the critique this project takes seriously, and the reason Phase B is a distinct phase.
- **Hedy**: the gradual-syntax teaching language that proved multilingual Python-like education works at scale.
