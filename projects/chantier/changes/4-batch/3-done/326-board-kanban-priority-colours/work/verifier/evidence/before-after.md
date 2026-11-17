# Before / after (CR-326)

Before: detached worktree at 33a2305 (the merge base of the PR; origin/main has since moved to a111e18, a Configuration-page change). After: the PR head de0993f.
Both: board served by `chantier board` from the worktree over the fictional demo (docs/demo, plus one P3 item), in a fresh temp folder, removed at the end; 1280x800 and 390x800, Chromium via Playwright.
Reproduce: `uv run --script work/verifier/shots.py <worktree> <out dir> <label>`. Logs: work/verifier/before.log, after.log. Paths on screen are made up (/home/demo/...), no username.

| Pair | Shows |
| --- | --- |
| kanban-pc, kanban-phone | before: board bottom at 1151px in an 800px window; after: 776px, priority chips and left borders, column headers one teal tint, dots unchanged; phone: one column, snap kept |
| triage-pc, triage-phone | four lanes, one card selected, chips and left borders kept |
| panel-item-pc | P1 chip in the panel head |
| panel-pc | CR panel with the tinted "working" chip |
| costs-pc/phone | four teal figure cards |
| batch-pc/phone | tinted state badges, breadcrumb chip |
| project-pc/phone, picker-pc | tinted sidebar, active row, project mark |
| all-projects-pc/phone | three project marks (D, M, S) |

Not captured: the Kanban's horizontal scrollbar itself (overlay scrollbar in headless Chromium); proven by measured sizes in verify.md.
