# Verify: CR-208

Head: 2da9cf597282a9fb984c4391a34c36531f85b682

Delta assessment after the restack (206bf6c on d178c7e -> 2da9cf5 on CR-207's 94c27be). The base moved a lot (d178c7e..94c27be touches claude-code.md, foreman.md, evals/README.md, among 60 files); the CR's own diff is 3 files (evals/README.md, foreman.md, hosts/claude-code.md), chief-of-staff.md unchanged.

## Judged again at 2da9cf5
- Heartbeat wording: "every `30m`" absent from claude-code.md; prompt is the command alone, ScheduleWakeup 30 min (1800 s); the rest of the section intact. Cosmetic: the first sentence's line wrapping is ragged (short and long lines mixed); not a spec failure.
- "## Auto-fix events" present after "## Heartbeat", before "## Configuration": points 1 to 11 all there, turn-off line marked unproved with its trial, section marked unproved with its trial.
- set_monitor bullet: says no card uses it, to arm or to disarm, points to "Auto-fix events"; marks kept. Cosmetic: the added line is long.
- foreman.md: one pointer bullet after the "rebase:" bullet, on a line with the hosts/ link, no host tool name.
- evals/README.md: one bullet in "Before you start", links the section, says the way is unproved and gives no path; copilot and claude-planted not named.
- `pytest tests/test_structure.py` in skills/chantier/scripts/cli: 41 passed (includes the host-tool test).
- Spot check: no mojibake in the file (the "â€¦" seen in the spec is console display only).

## Carried
- carried from 206bf6c: `just check` and `just scenario` pass (run 20261113-014004-31032); the restack's own fast gate passed (58 tests per work/conflicts.md); the long gate is not rerun here, the stack's top gets it once.
- carried from 206bf6c: no hooks/ or types/ change by the CR, so no `just mod`.
- carried from 206bf6c: the behaviour itself is proved by the next real campaign (spec point 11), not by this PR.
