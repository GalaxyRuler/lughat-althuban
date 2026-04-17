# Spec packets

Every implementation task is handed off from the planner (Claude) to the implementer (Codex) as a **spec packet** — a single markdown file in this directory.

## Packet lifecycle

1. **Author** (Claude): write `NNNN-short-name.md` in this directory using `0000-template.md`. Commit as `spec: NNNN <short-name>`.
2. **Implement** (Codex): create a branch `packet/NNNN-short-name`, implement the spec, run tests until green, write `NNNN-short-name.delivery.md` alongside the spec with a short delivery note (what shipped, deviations, open concerns, any questions for the planner).
3. **Review** (Claude): code-review the diff against the packet. Either approve (merge to main) or write `NNNN-short-name.fixup-M.md` with concrete corrections. Revision packets chain forward, not backward.
4. **Close**: once merged, mark the packet's status in `specs/INDEX.md`.

## File naming

- `NNNN-short-name.md` — the packet itself
- `NNNN-short-name.delivery.md` — Codex's delivery note
- `NNNN-short-name.fixup-M.md` — Claude's fix-up revisions (M = 1, 2, ...)

## Discipline

- **Tests are the contract.** If the tests pass, Codex's work is done even if Claude later decides something was missing. If something was missing, it's Claude's fault for under-specifying; write a fix-up packet, don't blame Codex.
- **One open packet at a time.** Claude does not hand Codex a second packet until the first is reviewed and merged. This keeps the review discipline sharp.
- **No backchannel decisions.** If Codex encounters something the packet doesn't cover, it asks in the "Open Questions" section of the delivery note. Claude answers by amending the packet or writing a fix-up. Verbal/chat decisions are not durable and must not guide implementation.

## Index

See `INDEX.md` for the running list of packets and their status.
