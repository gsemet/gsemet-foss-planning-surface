# Orchestrator notes

Hand-written part of `ORCHESTRATOR.md`, included as is by `just orchestrator`. Edit this file, never the
generated tables.

## Run log 2026-10-31

Run 2026-10-31 (Foreman driven by the Chief of Staff): night batch landed as stack #230 → #234 (gh stack 235, merged by the user, main 5ebd3b2f): CRs 203, 204, 205, 207, 208; CR 206 not reproduced (no PR). CR 209 (#229) landed separately as #236. P1 unnecessary-table-margin-breakage is parked by the owner (hypothesis recorded).

Later the same day: #237 (QA Drivers) with #239 (QA template), #240 (radio choice lists, auto-merged by the
owner) and #242 (generated ORCHESTRATOR.md, superseding #238 and #241) landed; main 18c4f020.

## Planner-tick mode (retired 2026-11-03)

Replaced by the foreman session and its loop, see the guideline section "Foreman session and its loop".

## Run 2026-11-03: foreman as a nested session (trial)

CRs 236, 237, 238 run in parallel under the new workflow: the foreman is a nested session of the
main session and keeps a self-paced `/loop` (wake-up every 270 s) while at least one driver is live;
it stops the loop when none is. This replaces the planner-tick mode above for this run. Rules: the
draft guideline in the worktree `.claude/worktrees/angry-noether-edbfbb` (not yet merged). CR 170
(demo video) went back to the backlog, P2, as `02-backlog/P2/demo-video` (owner, 2026-11-03).

## P1 grill 2026-11-03

Next batch, as a stack: bug-toc-column-not-displayed-on-narrow, bug-row-anchors-in-margin-break,
option-button. Decisions in each item's `02-decisions.md`. New P1 items from splits:
admonition-type-picker, syntax-coverage-audit, myst-code-block-editor. The two table-margin items
become one CR (variant D).

## Run 2026-11-03 (afternoon): close P1 and P2, then 1.3.0

CRs 242-253, one stack, run by a new foreman session (brief archived as
[RUN-BRIEF-2026-11-03-afternoon.md](../5-archives/RUN-BRIEF-2026-11-03-afternoon.md)). Done: 16 CRs
landed, 253 closed without a change; the foreman session is finished and its loop stopped.
P2 `demo-video` stays in the backlog (owner).

## Release 1.3 (main session)

1.3.0 (#303) and 1.3.1 (#308) were merged but never tagged: real VS Code jobs failed on a cell
editor bug and on stale scenarios that expected edit mode to carry over (fixed in #306 and #309).
Shipped as 1.3.2 (#310) on 2026-11-03; CR 254 archived with its report. Open VSX publication is a P1 backlog item, waiting for
the owner's registration.
