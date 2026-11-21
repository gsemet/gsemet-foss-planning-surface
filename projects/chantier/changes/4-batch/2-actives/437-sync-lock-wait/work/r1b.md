# Round 1b (A-9)

Changed: the `$CHANTIER` paragraph of the four SKILL.md files is short and byte-identical (check command, exit reading, never stop or kill, `sync pending: held by`, 3 minutes, pointer to session-start.md "6. Sync the checkout"). The six steps and their detail (holders row, offer, Own, yes/no, ordinary failure) moved to a new "## 6. Sync the checkout" in session-start.md. chief-of-staff.md preflight now points at it. Tests: test_launch_modes.py splits the phrases (paragraph vs section 6), the `uv sync --locked --project` form is asserted in session-start.md.
Gates: ruff format/check clean; `just check` pass (1631 passed). STARTUP_LIMIT unchanged 12544; worst startup 11383, worst reload 12178.
Open: none. Scenario not run.
