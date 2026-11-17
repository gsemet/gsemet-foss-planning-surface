# 205 — Force a repro: alert-dropdown window-blur flake

CI flake batch 2026-10-31 (user request via the Chief of Staff). From origin/main, one PR.

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
> 
> ## Same family: slash-menu (2026-10-29)
> 
> Heavy run 40798585280 (CR 192 branch) failed stress round 7, scenario `slash-menu` ("Timed out waiting
> for the menu to open for /tab") with `windowState.active:false`, `activeTextEditor:null`. CR 198
> (workbench focus thief) investigates both.
> 
> ## User impact answered by CR 198 (2026-10-29, PR #218): users NOT affected
> 
> The alert type control is a custom DOM menu (src/page/modules/editPalette.ts:285-341), not a native
> `<select>`; its option mousedown is cancelled, so the pick does not move the focus. Real-window probe on
> CI (run 40806677284, `ALERT-PICK-PROBE`): keyboard pick TIP and mouse pick WARNING both applied, final
> Markdown has the chosen type; blur/commit/close happen only after the pick. The stress failure is a test
> artefact. Lead: the harness's `workbench.action.focusFirstEditorGroup` focuses an EMPTY first editor
> group while Studio sits in another group (slash-menu dump, same run) — CR 199 targets the Studio group.
> 
> ## Decision (owner, 2026-10-29): keep BLOCK-047 as is
> 
> When the whole window loses focus, the block editor commits and closes. This is intended and
> stays. No code change. The rationale is recorded in SwRS-MDOKFSTUDIO-BLOCK-047 by CR 200.
> The remaining harness-side flake (custom alert menu during window blur) is a test concern only.


## Owner decisions (2026-10-31, via the Chief of Staff)

Goal: FORCE a reproduction before fixing. Tools: stress loops of the scenario (N >= 60 rounds),
injected delays, and the diagnostics from #193 (integration heartbeat/hang dump), #205 (recorded
toggle state) and #218/#220 (workbench focus dump read at the failing step).

- Reproduction runs in a real window only through CI (heavy or a dedicated loop job dispatched on
  the CR branch); no local real-window runs. Headless reproductions are welcome too.
- If reproduced: fix the ROOT CAUSE. Test-side unless a product bug shows; a product bug gets a
  regression test that fails without the fix.
- If not reproduced after a serious attempt: write up the attempts and the number of clean rounds,
  and close the backlog item (archive it with the report). A diagnostic-only PR is fine if it adds
  lasting value; otherwise no PR.
- Delivery: a READY PR on main (or a small stack). Never merge. Normal CI green plus one heavy run
  on the PR head.

## Specific

First check whether #220/#221 (workbench focus: dump before cleanup, waitForActiveSourceEditor,
undo race fix, ALERT-PICK-PROBE moved to integration) already removed this flake: count its
occurrences in heavy/stress runs on main since 9b53edbe. Then run the alert-dropdown scenario in a
loop, N >= 60 rounds, in a real window via CI.
