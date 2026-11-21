## Summary

The real VS Code window step `paste-url` failed on CI several times without a related change, and `drop-files` belongs to the same family. The failures seen on CI were a wait on a stored edit mode that commit e05f0b51 already removed; the first runs of the new default stress plan also showed that the second CDP connection these two scenarios open reset the run's 1400x900 viewport to 1200x800, after which round 2 lost its first edit-mode clicks (a likely cause, not reproduced locally). This change removes the two remaining waits on time in these scenarios, adds a failure trace to the CI log, and puts both scenarios in the default `just ci-stress` plan so a race shows up on every push to `main`.

## Deliverables

- `paste-url`: one click then a wait on the block text box, instead of a 30 s click loop with a 700 ms pause.
- `drop-files`: a wait on the drop marker, instead of a 400 ms pause; edit mode is turned off best-effort in its `finally`, like `paste-url`.
- Both scenarios now set the run's own viewport (`RUN_VIEWPORT`, 1400x900, in `test/integration/realWindowViewport.ts`), as `checkbox-toggle` does, instead of 1200x800 on their second connection.
- A failure trace line per scenario: `<scenario> failed: ...` then `<scenario> failure trace: {json}` (host state, source document, frame edit mode, editor tabs, last progress marker, failures).
- Default stress plan: 21 scenarios at 11 rounds (`DEFAULT_STRESS_REPEAT`), `paste-url` and `drop-files` last.

## Changes

- `test/integration/pasteUrl.test.ts`, `test/integration/dropFiles.test.ts`: waits on page state, progress markers at each phase, bodies wrapped in `withFailureTrace`.
- `test/shared/realWindowTrace.ts` (pure `formatScenarioTrace`, `withFailureTrace` with a 5 s bound on the collector), `test/integration/scenarioTrace.ts` (the collector), `test/build/realWindowTrace.test.ts`.
- `test/shared/stressPlan.ts`, `test/integration/realInput/run.ts`, `test/shared/hangWatchdog.ts`, `justfile`, `.github/workflows/ci.yml`: both names in the default trusted plan, default rounds 12 to 11 read from one constant. The 12 x 21 plan would compute a 1,027,920 ms launch deadline against the 960,000 ms ceiling and fail its guard; 11 x 21 computes 944,760 ms.
- `test/build/stressPlan.test.ts`: the test that said these two scenarios are never in the default plan changes intent at the owner's request: it now asserts both are in the default trusted plan, still run alone when named and absent from the untrusted window.
- `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py`: updated for 11 rounds.
- `requirements/tiers/log.md`: dated entry.

## Impacts

No product change and no visual change. The viewport cause is unproven locally (no Chromium could run where it was diagnosed); CI runs decide. The `stress` job (advisory on `main`) runs two more scenarios per round.

## Blast radius

Grade: 1. Test and CI configuration only; a plain `git revert` restores the previous plan.

## Test plan

- [x] New or changed tests: `test/build/realWindowTrace.test.ts`, `test/build/stressPlan.test.ts`, `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py`
- [x] Requirements: no behaviour change; `just requirements-update` at 845997b reports 0 indexes and 0 projections updated and leaves the tree clean
- [x] Changelog: no user-facing change
- [x] Local gates: `just check` (pass), `test_workflows.py` (81 passed), `just preflight` on Windows (static stage, pass)
- [x] Review: approved at 845997b (carried from 7eeeb33 and the viewport round: the rebase onto main changed only the requirements log context)
- [x] Verified at 845997b (the default-plan heavy proof carried from the head before the rebase, same patch)
- [x] CI green at 845997b (static, static-windows, visual, viewer-graph, checks, report; `report` and `checks` re-run once after an infrastructure error in a setup step)
- [x] Viewport fix proof, at the head before the rebase onto main (the rebase changed only the requirements log): default stress run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44903251073 green (integration green, `stress` job 16 min against the 24-minute deadline, 21 scenarios at 11 rounds); narrow plan `paste-url,frontmatter-rename,frontmatter-title` at 20 rounds https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44903254624 green (`stress` job under 4 min). Before the fix the default stress failed twice at round 2 `frontmatter-title`.
- [x] Forced-failure trace proof: a throwaway branch (deleted) forcing one failure after the first phase of each scenario; the `stress` job logs print `paste-url failed: ...` and `paste-url failure trace: {...}` (https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44905091608), then the same for `drop-files` (https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44905104654).
- [x] Focused loop of 100 rounds of both scenarios at the pushed head: https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44904977842 green (`stress` job 7 min).

Trace lines from the forced-failure runs (stress job logs):

```
paste-url failed: Error: forced failure for the trace proof
paste-url failure trace: {"preview":{"phase":"ready","requestId":1,"documentVersion":1,"webviewReady":true,"deferredWorkPending":false,"blockEditOpen":false,"pageEditorOpen":true,"contentPatches":0,"htmlAssignments":4,"panelActive":true},"source":{"version":1,"text":"Read the guide for details.\nLogo:  then text.\nHome:  then text.\n\nSecond paragraph.\n"},"frame":{"found":true,"editMode":"on"},"tabs":[[{"label":"preview.md","inputType":"Hc"},{"label":"paste.md","inputType":"Hc"}],[{"label":"Studio · paste.md","inputType":"Lf"}]],"failures":[],"lastProgress":"paste-url: first paste (link)"}
drop-files failed: Error: forced failure for the trace proof
drop-files failure trace: {"preview":{"phase":"ready","requestId":1,"documentVersion":1,"webviewReady":true,"deferredWorkPending":false,"blockEditOpen":false,"pageEditorOpen":false,"contentPatches":0,"htmlAssignments":4,"panelActive":true},"source":{"version":1,"text":"First paragraph of the page.\n\nSecond paragraph of the page.\n"},"frame":{"found":true,"editMode":"on"},"tabs":[[{"label":"preview.md","inputType":"Hc"},{"label":"page.md","inputType":"Hc"}],[{"label":"Studio · page.md","inputType":"Lf"}]],"failures":[],"lastProgress":"drop-files: first drop (Markdown file)"}
```

## Known gaps

- `run.ts` carries the 1400x900 viewport as a literal beside `RUN_VIEWPORT`; left because it is a duplicated constant with no behaviour risk.
- The comment on the viewport states the Chromium behaviour as fact while it is a diagnosis proven only by the stress runs passing.
- In `dropFiles.test.ts` an empty `try/catch` around the drop-marker wait drops that wait's own timeout message (the scenario's failure trace still names the last progress marker).
