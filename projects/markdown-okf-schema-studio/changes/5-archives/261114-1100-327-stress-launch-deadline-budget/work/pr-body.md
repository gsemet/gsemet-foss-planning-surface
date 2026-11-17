## Summary

The stress job's launch deadline was a fixed 26 minutes. After the stress list grew to 17 trusted scenarios, a 20-round run needs about 24 minutes, so a slow runner could cut a healthy run. The deadline now follows the work, and the default run is shorter.

## Deliverables

| | Before | After |
|-|--------|-------|
| Launch deadline | fixed 26 min | 2 min + 6 s per scenario run (rounds x scenarios), capped at 24 min |
| Default stress rounds | 20 | 12 |
| Job limit | 30 min | 30 min (unchanged) |

12 rounds of 17 scenarios: about 14 min expected, computed deadline 22.4 min. The launcher prints the deadline before each stress window opens.

## Changes

- `test/shared/hangWatchdog.ts`: `stressLaunchDeadlineMs`, the three constants, and `launchDeadlineMs` using the stress plan; an explicit `STUDIO_LAUNCH_TIMEOUT_MS` still wins.
- `test/integration/run-tests.ts`: prints the stress launch deadline line.
- `justfile`, `.github/workflows/ci.yml`: default 12 rounds; the fixed exported timeout is removed.
- `CONTRIBUTING.md`, `.agents/guidelines/ci.guidelines.md`: real figures (about 4 s per scenario run, up to about 220 scenario runs per window under the ceiling).
- Tests: formula, plan, override, invalid repeat and a margin guard in `hangWatchdog.test.ts`; workflow tests expect 12 and no fixed timeout.

## Impacts

No change to the extension (`src/`). Pushes to `main` run 12 stress rounds instead of 20.

Proof, branch heavy run at the default repeat (run 43585513894, all jobs green): printed deadline 1 344 000 ms (22.4 min); trusted window 13.1 min (10:29:55 to 10:43:00), a 41 % margin; Restricted Mode window 0.5 min; stress job 14.0 min against its 30 minutes, a 53 % margin. No launch timeout.

## Blast radius

Grade: 1. CI harness and docs only; a plain revert restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: No behaviour change (SwRS-MDOKFSTUDIO-CORE-076 unchanged)
- [x] Changelog: No user-facing change
- [x] Local gates: `just check`, unit and workflow tests pass; `ci-static` passes in `just preflight`. The local app-window stages (visual, integration) fail on this machine in tests this change does not touch; CI is the proof.
- [x] Review
- [x] CI green, including the heavy run (see Impacts)
