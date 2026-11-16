## What

A new role, the spec-writer (Opus 5.5), writes a CR's Change Specification from its grill. The Chief of Staff starts it in the background on the user's word, outside any batch.

- Card `references/spec-writer.md`; agent files on both hosts with identical bodies.
- `specifying` / `specified` state read from the folder (`work/specifying`, `03-change-spec.md`), shown in `STATUS.json`, `STATUS.md` and the board's backlog table.
- Chief of Staff card: no longer writes the specification (release and fix ones stay its own); reviews the result against `02-answers.md`.
- Cost: a spec-writer is on the Chief of Staff's line, left out of a direct batch's spend and budget.
- Docs: concepts, routing, host references, README, SKILL.

## Evidence

`just check` and `just scenario` pass (scenario covers the state in `STATUS.json` and the direct-batch cost).
