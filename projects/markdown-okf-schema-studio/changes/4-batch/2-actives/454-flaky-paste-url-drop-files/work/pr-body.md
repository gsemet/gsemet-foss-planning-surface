## Summary

The real VS Code window step `paste-url` failed on CI several times without a related change, and `drop-files` belongs to the same family. The observed failure was a wait on a stored edit mode that commit e05f0b51 already removed; this change removes the two remaining waits on time in these scenarios, adds a failure trace to the CI log, and puts both scenarios in the default `just ci-stress` plan so a race shows up on every push to `main`.

## Deliverables

- `paste-url`: one click then a wait on the block text box, instead of a 30 s click loop with a 700 ms pause.
- `drop-files`: a wait on the drop marker, instead of a 400 ms pause; edit mode is turned off best-effort in its `finally`, like `paste-url`.
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

No product change and no visual change. The `stress` job (advisory on `main`) runs two more scenarios per round.

## Blast radius

Grade: 1. Test and CI configuration only; a plain `git revert` restores the previous plan.

## Test plan

- [x] New or changed tests: `test/build/realWindowTrace.test.ts`, `test/build/stressPlan.test.ts`, `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py`
- [x] Requirements: no behaviour change; `just requirements-update` reports no change
- [x] Changelog: no user-facing change
- [ ] Local gates: `just check` (pass), `test_workflows.py` (81 passed)
- [ ] Review
- [ ] CI green
- [ ] Heavy dispatch on the branch (integration and stress at 11 rounds, duration against the 24-minute deadline), focused loop of 100 rounds of both scenarios, and the forced-failure trace proof: results to be added.
