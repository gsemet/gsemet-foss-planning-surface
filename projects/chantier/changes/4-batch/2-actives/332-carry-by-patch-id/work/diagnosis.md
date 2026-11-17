# Diagnosis: surface-board check "model: default ... [reset in repository]" red at 9251f79

Reproduction (worktree, ~172 s, fails the same locally on Windows):
`uv run --locked python scenario/run_scenario.py --unit surface-board --forge github`

Cause: not this CR's diff. The check (scenario/run_scenario.py ~line 7846) compares `coder_line()` to the exact string
`coder: agent=chantier:coder model=(its file's) [reset in repository]`. Since 253fca6 (CR-331, "configure the escalation
model per host and role", playbook/lines.py) the playbook line carries a trailing
` escalation=opus (claude-opus-5-5, Claude Opus 5.5)`. Observed (transcript line 695):
`coder: agent=chantier:coder model=(its file's) [reset in repository] escalation=opus (claude-opus-5-5, Claude Opus 5.5)`.
Equality fails on the suffix. The batch half (`coder_line("--batch") == frozen`) holds (it printed haiku [repository], as frozen).

CR-331 did not touch scenario/run_scenario.py (253fca6 stat: playbook/*.py and tests only), and the assertion is
identical at 253fca6 (line 7765). So CR-331's code already breaks this check; its "green" run did not exercise it
(or the unit was not run/was red there). CR-332's diff (25 files, none under playbook/) neither causes nor
changes it: its scenario edits are only in gate_carry / new gate_carry_stack.

Place to fix: scenario/run_scenario.py, the check at ~7846-7848 (and the sibling checks at ~7842 and ~7852 use
`in`, so they pass): expect `coder_line().startswith("coder: agent=chantier:coder model=(its file's) [reset in repository]")`
(or include the ` escalation=...` suffix). Belongs in CR-331 (the CR that changed the line), then CR-332 inherits it.
