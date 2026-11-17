# 194 — alert-dropdown stress: immune to a window blur (test side)

Night batch 2026-10-29 (CoS: run tonight, last; test-side only; no BLOCK-047 product change; if unproven after the last round, out of the stack and the item stays open). Based on PR #194's branch (CR 180 traces).

Backlog intent (verbatim):

> # Stress flake: alert-dropdown "Timed out waiting for Warning to change the type"
> 
> Filed 2026-10-28 by the Foreman from the 1.0.0 heavy runs on main b723e176.
> 
> - Run 40778738577 (heavy, main b723e176), stress job, round 2/20, scenario `alert-dropdown`:
>   `Timed out waiting for Warning to change the type. Editor state: {"tag":"BODY"}` (VS Code 1.144.0),
>   at `out/test/integration/realInput/run.js:93` (`runStress`). Log: `stress-b723e176.log` (this
>   folder).
> - Same commit, run 40778781367: stress failed instead on the known `review-threads` flake (round
>   10/20); alert-dropdown passed there.
> - Heavy on the alert line-map fix branch (run 40774494253, head 81af33d7, same code as b723e176
>   minus the version bump): alert-dropdown passed 20/20.
> - Suspect: a race in the alert type dropdown (focus lands on BODY), possibly sensitive to the alert
>   rewrite/line map merged in a8267570 (the type change edits the `[!TYPE]` marker line). Check that
>   the type-change edit targets the marker line with the new line map, then the timing.
> 
> ## Status after CR 180 (2026-10-29, PR #194, diagnostics only — not fixed)
> 
> - Hypothesis: an OS/window blur during the WARNING click commits and closes the block editor
>   (commit on leave, BLOCK-047). No page or host code steals the focus.
> - New evidence on the next failure: page trace entries for every `mousedown` (target, cancelled) and
>   every block-editor blur (related target, commit or kept, page focus); the scenario failure message
>   carries a timed step log, host document state, focus commands and the window focus report. A blur
>   with no preceding `mousedown option=WARNING` means the press never reached the page.
> - Next step: make the stress run immune to a window blur (a blur is not a product bug in itself).
> - Product question to the owner (open): should the editor commit when the whole window loses focus?
>   Until answered, keep commit on window blur (no data loss).
