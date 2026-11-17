# 180 — Stress flake: alert-dropdown type change times out

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

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
