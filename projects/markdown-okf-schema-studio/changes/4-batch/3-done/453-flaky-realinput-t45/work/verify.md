# Verify CR-453 (scope: the Driver's brief: forced failure and three code checks)

Head: 8071d21712ab1389f6b8cc244a344497c2b4265e

Not judged here (outside the brief): PR description, Review box, gate pass, stress run proofs.

## Claim 1: forced failure holds every part of spec section 1 (judged at 8071d217)
Command: STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_REPEAT=1 STUDIO_STRESS_SCENARIOS=table-insert-slash npm run test:integration -- --trusted-only, with the expectation of the last expectState changed to "| :---: | FORCED |" (reverted after; `git status --short` empty).
Output: work/forced-failure.md (raw: work/verifier/forced-run.log line 325). One message, `Timed out waiting for only the delimiter cell of the first column centred.` holding:
- steps with ms: open preview 0 ... Center pressed 1981: present
- host request: {"requestId":2,"documentVersion":1,"phase":"ready"}: present
- buffer: source version 2, dirty true, full text: present
- editor state: {"value":...,"start":30,"end":30}: present
- focus report: windowFocusReport with frames, documentId/version/requestId/visibility and editorTrace (mousedown option=center prevented=true ...), VS Code window state, page focus: present
- page trace start: pageTraceStart 333: present
- landing summary: `landing workbench [none] host [none]`: present (note: it read none although the editor trace shows the press reached the content frame as mousedown option=center; the probe records nothing in this run, content only to be aware of, the section is printed)
Followed by the suite's workbench focus dump. VERIFIED.

## Claim 2: STRESS_ON_DEMAND_SCENARIOS holds table-insert-slash only; default plan 11 rounds (8071d217)
`grep -n "STRESS_ON_DEMAND_SCENARIOS: \|DEFAULT_STRESS_REPEAT =" test/shared/stressPlan.ts`:
`DEFAULT_STRESS_REPEAT = 11`; `STRESS_ON_DEMAND_SCENARIOS: readonly string[] = ["table-insert-slash"];`
`node --test out/test/build/stressPlan.test.js` after `tsc -p .`: 9 pass, 0 fail, including "CR 453: table-insert-slash is on demand in the trusted window and never in the default plan". VERIFIED.

## Claim 3: the Center press uses clickListOption (8071d217)
tableInsertSlash.ts: `clickListOption(page, frame, "center", "[data-edit-action='columnAlign']")` inside `withCurrentFrame`, wrapped in `guarded`. The forced run's editor trace shows `mousedown option=center prevented=true`. VERIFIED.

VERIFIED

## Description pass (PR 465 body as posted, judged at 8071d217)
Command: gh pr view 465 -R gsemet/markdown-okf-schema-studio --json body,title; git diff --stat a106fa7b..8071d217 (4 test files: stressPlan.test.ts, realInput/run.ts, tableInsertSlash.ts, shared/stressPlan.ts); `$CHANTIER log CR-453`; gh run view on the 6 stress runs.
- Audit 1-2, 6-7, 10: sections in order, fold after Autonomous decisions holding Changes, Impacts, Test plan, Internal references; Known gaps has 3 bullets (cause unproved, no pre-fix run, landing summary read none) matching the notes; no STALE mark. OK.
- Audit 3: title and body outside Internal references hold no CR, batch or role name. Scenario name `table-insert-slash` appears as a code identifier that exists in the diff (stress registration); accepted.
- Audit 4-5: Deliverables has the failure message, a before/after sequenceDiagram, the on-demand registration; Changes match the diff (traces/message, clickListOption, STRESS_ON_DEMAND_SCENARIOS plus unit test). Nothing unmentioned. No images, so no username/home check applies.
- Review box: log shows "r1 inspector approved at 845997bb..."; carry events at 01287be and 8071d21 (patch unchanged). OK.
- Gates: log shows just preflight pass at 1d2c9a3, carried to 8071d21; `just check` pass at 8071d21 noted. Stress runs: 44912543237, 44912545451, 44912547780 completed success at head 8071d21 (44912543237 jobs: integration, stress, static, static-windows, visual, report, checks success); 44909129414, 44909131656, 44909133730 success at 1d2c9a3. PR is draft, base main, head 8071d21.
- Claims 9 pass at 8071d21: claim 2 above.
Description: VERIFIED at 8071d21712ab1389f6b8cc244a344497c2b4265e.
