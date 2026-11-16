## Summary

Two quick sandbox campaigns, `real-foreman` (stack mode, steered by a Foreman) and `real-direct` (parallel mode, direct mode), were run once each on the current `main` (0.9.0, `fa97e70`) against the eval sandbox, with GitHub only. This PR delivers their two reports and the campaigns' rows, to measure the new chantier on the path a user takes and bring back findings.

## Deliverables

| Campaign | Mode | CRs merged | Audit | Judge | Cost |
| --- | --- | --- | --- | --- | --- |
| real-foreman, run 2 | stack | 5 of 5 | 513/514 | 2 pass, 0 fail, 4 not run | $10.28 |
| real-direct, run 3 | parallel | 5 of 5 | 553/555 | 6 pass, 0 fail, 0 not run | $11.52 at the audit |

- `evals/results/real-foreman-2026-11-15-run2.md` and `evals/results/real-direct-2026-11-15-run3.md`: verdict, the audit's run table verbatim, per-CR account, numbered findings, the scorecard, numbers and maintainer notes.
- `evals/README.md`: the "Last run" and cost cells of the two campaign rows.
- `evals/real-foreman/RUNBOOK.md`: the "Cost and time" row, written from the first sandbox run.

## Blast radius

Low: documentation and eval reports only; no code, card or eval-kit file changes. Roll back by reverting the commit.

## Autonomous decisions

- The reports compare real-direct with its 2026-11-12 run only where the audit tables agree; the sandbox base was compared between the two audits' tables, not against `kit/sandbox.json`.
- Run 3's final cost is given as the audit's figure with the other two figures noted, not reconciled.

## Known gaps

- Copilot and GitLab are not covered by these runs.
- Auto-fix state in the real-foreman run is not recorded; in the real-direct run it was on until it was turned off for one sandbox PR mid-run.
- The scorecard rows for J16, J18 and J20 (and J25, J8 in the real-direct report) are marked "not seen": the by-hand rows were not read.
- The cause of the audit's J1 failure in the real-foreman run, and the source of the "[foreman->...]" labels in direct mode, were not found.
- The real-foreman run merged with the sandbox kit's fix branch, not `main`'s script, because `main`'s `sandbox.py merge` fails on a native stack PR (the fix has since reached `main`).
- Run 3's final cost has three figures (audit $11.52, operator note $11.80, archive $11.91), not reconciled.

<details><summary>Details</summary>

## Changes

- Adds the two result reports; edits two rows of `evals/README.md` and one row of `evals/real-foreman/RUNBOOK.md`.

## Impacts

No user-visible change; maintainers get the measured behaviour of the new chantier.

## Test plan

- [x] `just check` passes at `2e2a20e` (carried from `ebe3c94` over a clean rebase): CI lists `just check` (ubuntu, macOS, Windows), `just eval-dry-run` and `just scenario (ubuntu-latest)` all passing.
- [x] Review: approved at `2e2a20e` (carried from `ebe3c94` over a clean rebase) (the reviewed tree, committed unchanged).
- [x] Verifier: VERIFIED at `2e2a20e` (carried from `ebe3c94` over a clean rebase): both reports present, run tables verbatim from the audit files, judge and audit counts match, diff touches only the three paths.
- No long gate: a change to the docs or the eval kit alone needs none (AGENTS.md).

Candidate inbox items from the findings (offered after the merge):

1. `sandbox.py merge` cannot merge a native-stack PR (fix branch has it).
2. Judge "not run" on CRs whose recorded head a stack restack replaced.
3. `handback` prints "PR in draft ... waits on main" for a stack PR already ready.
4. Stack mode starts every CR on main, then restacks (cost).
5. PR bodies reach the Inspector and Verifier with missing sections or placeholders; lint first.
6. `cost`, `cost --explain`, `cost --by cr` refuse on a paused batch without `--batch`.
7. The write guard refuses a shell write that names the allowed folder as `/c/...`.
8. Drivers pass `gate long` to `chantier phase`; refused repeatedly.
9. Preflight's trial push of `chantier/preflight-trial` fails (no local ref) and proves nothing.
10. Audit J1 fails on the retro-critic's prompt in the Foreman run; cause not found.
11. `status` without `--refresh` shows stale spend.
12. Direct run: Auto-fix on until mid-run; record `mcp__ccd_pr__set_monitor` in `hosts/claude-code.md`.
13. Direct mode labels messages and asks "[foreman->...]" with no Foreman.
14. Stale SHAs in `before-after.md` give NOT VERIFIED after a rebase; the Verifier re-run costs $2.46.
15. Board port clash (WinError 10048) again.
16. Audit J14/J26 failures in run 3 are operator slips.

## Internal references

- CR-275, batch-18; specification `.agents/changes/4-batch/2-actives/275-evals-run-b18/03-change-spec.md`.

</details>
