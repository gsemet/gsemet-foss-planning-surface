# 207 — Force a repro: integration toc edit-mode toggle flake

CI flake batch 2026-10-31 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Backlog (P2): integration step `toc` — "Edit mode did not switch to off after 3 clicks"
> 
> Seen in heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40784022530
> (CR 173 branch, 2026-10-29); the next heavy run of the same code was green. Similar click timeout on
> main (b71f run).
> 
> - Where: `setEditMode` helper in `test/integration/realInput/harness.ts`, real VS Code window under
>   xvfb, trusted suite step `toc`.
> - Symptom: three clicks on the Edit toolbar button do not switch edit mode off.
> - Not diagnosed: whether the click misses (toolbar collapsed, overlay, focus) or the page ignores it.
> - Next step: log the button state (`data-edit-mode`, `aria-pressed`, bounding box, element at the
>   click point) before each click; wait on state, not time. Fix test-side unless a product bug shows.
> - Rule 12: a flake is fixed, never ignored.
> 
> Second occurrence: heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40790025503
> (CR 187 branch, scenarioToc in tocWindow.js); rerun green.
> 
> ## Status after CR 192 (2026-10-29, PR #205 — instrumentation + stress coverage, cause not proven)
> 
> `setEditMode` waits for boot, records the toggle state before each click, retries only on a proven
> miss, and its failure message names the cause (reached toggle without switching → `applyEditMode`;
> render restored mode → theme path; boot timeout → `runtime.ts`). `toc` added to the stress plan.
> Keep open until a failure records the state.


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

#205 records the toggle state on failure. Reproduce the toc edit-mode toggle flake (loop the
scenario, inject delays around the toggle) and use the recorded state to find the cause.
