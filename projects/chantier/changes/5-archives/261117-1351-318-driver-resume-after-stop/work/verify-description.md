VERIFIED

Head: b9daeffc7fb140f2ee5b8addea4e85312fa98438

Description of PR 273 (`gh pr view 273 --repo gsemet/chantier --json body,headRefOid`; headRefOid = b9daeff, same as `git rev-parse HEAD`), judged at b9daeff against `git diff origin/main --stat` (9 files) and pr-template.md.

- Layout: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps visible in order; one Details fold (Changes, Human decisions, Impacts, Test plan, Internal references), blank lines after `</summary>` and before `</details>`, nothing after. No Issues References (none expected).
- Summary/Deliverables/Changes match the diff: the 9 changed files are all named in Changes or Deliverables (foreman, concepts, hosts/claude-code, hosts/copilot, chief-of-staff cards; costs/stopped.py new; activity.py; batch_status.py; scenario/run_scenario.py). Flag text `Driver <id> stopped from outside, no hand-back recorded` found in the diff. Scenario `driver_liveness` checks found in the diff.
- Test plan SHAs: `git log` shows b9daeff on top of 8e3ab4b; `$CHANTIER log 318` has "r2 inspector approved at 8f2b9cf", "r2 committed as edd01d7", "clean rebase ... b9daeff", "CI: gh pr checks 273 at b9daeff ... all pass": Review box (approved at 8f2b9cf, committed as edd01d7, carried to b9daeff) is proved by the note. `just check` 382 tests and qa-driver 68/68 are in work/r2.md; qa-driver 68/68 at b9daeff also in work/verify.md. Timing 0.005 s / 0.007 s in work/r1.md/r2.md.
- No internal reference outside Internal references: only the CR name/batch are in the last section; roles named (foreman, steering session) are product terms of the changed cards; the session id is batch evidence, not an internal reference class of the template.
- Known gaps: the three unproved items (user's stop in the app, status timing not whole-command, Copilot) match the Unproved parts in the diff and r1/r2; no UNVERIFIED mark in the body needs a missing bullet; no STALE mark. No images attached.
