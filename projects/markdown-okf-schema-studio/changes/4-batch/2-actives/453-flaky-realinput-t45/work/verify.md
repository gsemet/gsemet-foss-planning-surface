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
