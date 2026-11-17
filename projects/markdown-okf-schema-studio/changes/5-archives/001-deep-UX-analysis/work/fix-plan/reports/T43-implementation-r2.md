# T43 implementation — round 2

STATUS: DONE (no code change; the scroll failures are not caused by T43 logic)

## Root cause
I could not tie any scroll-suite failure to T43 code. I reproduced the failures, instrumented the extension host, and in every captured failure none of the T43 code paths had run.

- I added temporary file logging to the extension: LOAD, ACTIVATE, RESOLVE, every queue phase, every `assignWebviewHtml` call and every overlay show. All of it is removed (`rg t43dbg` finds nothing).
- In 18 instrumented scroll runs, 3 failed:
  - `T43-loop1` and `T43-loop13`: "Timed out waiting for the custom editor render". The debug file was never created, so not even `activate()` had run. The extension host had not activated or resolved the custom editor within the suite's 10 s wait, before any T43 code could execute.
  - `T43-loop25` (`paired-editing-independent`): "Timed out waiting for … preview reaches end", after 104 s. Its debug trace shows exactly one request per preview, no overlay and no mid-test assignment. The system load average had spiked to 32 (Spotlight and mediaanalysisd at 100–150 % CPU).
- In every passing run, the trace shows the same single request per preview, so no overlay ever appeared and no mid-test render landed (3 previews per run, each with debouncing, building and ready at about 200 ms for the 4000-line file).
- Reading the code against hypotheses 1–3 gives the same result:
  - `assignWebviewHtml` always performs the real assignment, so nothing is skipped; only the counter and the overlay state depend on `changed`.
  - `readyRequestId` and `shownStatus` only matter while a render is pending over a rendered page, which the scroll suite does not do.
  - The overlay timer is cleared on every changed assignment, on ready or failed results and on dispose, and the overlay only appears after 1.5 s of pending.

The "no scroll feedback" and "textarea" failures from the orchestrator's runs did not occur again in my 24 scroll runs this round, so I cannot show their trace. Given the load-induced failures above, a flake from CPU starvation is the most likely cause, but this is inference. Machine load is the only difference I found from the earlier steady runs.

## Fix
None. I made no source or test change in this round. The debug instrumentation is removed, and the working tree is the r1 state.

## Gate results
- `gate.sh T43-impl2 unit types contracts` — PASS.
- `gate.sh T43-impl2-scroll{1,2,3} scroll` — PASS, PASS, PASS (110 s, 111 s, 110 s).
- `gate.sh T43-impl2 full` — PASS (236 s; `T43-impl2-full.log`).
- Instrumented diagnostic runs: `T43-r2a/r2b`, `T43-loop*` logs in `logs/`.

## Open points
- If the scroll suite fails again, check the machine load first, and whether `ACTIVATE` and `RESOLVE` appear in the log.
- The suite's 10 s waits for the first render and for the preview to reach the end are sensitive to load.
