# Implementation Packets

Ready-to-use prompts for Codex, Gemini, or any contributor. The files currently in this directory are historical Phase C packets; Phase D is tracked in [`../../ROADMAP-PHASE-D.md`](../../ROADMAP-PHASE-D.md) and [`../../decisions/0012-phase-d-charter.md`](../../decisions/0012-phase-d-charter.md).

Each file is self-contained — paste it directly as a prompt with no extra context needed.

## Dependency order

Phase C is complete. The dependency order below is preserved for archaeology and release-history review.

```
C-002 (ClassProxy)          ← implement first; blocks 9 packets
audit-fixes                 ← can run in parallel with C-002
C-014, C-015, C-022,
C-023, C-026, C-030         ← all independent; run in parallel
```

## Packets

| File | Packet | Blocks | Size |
|---|---|---|---|
| [C-002-class-proxy.md](C-002-class-proxy.md) | ClassProxy runtime | C-010–C-013, C-018, C-020–C-021, C-024–C-025 | M |
| [audit-fixes.md](audit-fixes.md) | Make example files fully Arabic | — | M |
| [C-014-click.md](C-014-click.md) | click CLI aliases | — | S |
| [C-015-rich.md](C-015-rich.md) | rich terminal aliases | — | S |
| [C-022-dotenv.md](C-022-dotenv.md) | python-dotenv aliases | — | S |
| [C-023-pyyaml.md](C-023-pyyaml.md) | PyYAML aliases | — | S |
| [C-026-pyjwt.md](C-026-pyjwt.md) | PyJWT aliases | — | S |
| [C-030-ar-v2-dictionary.md](C-030-ar-v2-dictionary.md) | ar-v2 opt-in dictionary | — | S |

## Naming convention

Brand names are written in Arabic script (not translated):
- flask → فلاسك, numpy → نمباي, pandas → باندا, pytest → بايتست
- seaborn → سيبورن, scipy → سايباي, sqlalchemy → ألكيمي
- aiohttp → أيو_هتب, fastapi → فاست_أبي, pillow → بيلو
- click → كليك, rich → ريتش, jwt → جي_دبليو_تي, yaml → يامل

Stdlib/concept modules keep descriptive Arabic names:
- asyncio → اتزامن, logging → تسجيل, datetime → مكتبة_تاريخ, etc.
