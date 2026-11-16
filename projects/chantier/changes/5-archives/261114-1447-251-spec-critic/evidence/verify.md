# Verify CR-251

Head: eb1b2e4b22a4c5239e83ac087d353ceadbaead8c

Verdict: pass (long gate waived; CI `just scenario` still pending at check time).

- pytest test_plugin_files.py + test_costs.py at the head (scratch HOME/USERPROFILE/CLAUDE_CONFIG_DIR): 47 passed.
- `chantier playbook` (no batch) prints `spec-critic prompt, first line: chantier spec-critic for the Chief of Staff, in the project <root>.` and the spec-writer's line unchanged. `rules.py` holds no role name (`chief_prompt_lines` reads the agent files' descriptions).
- Agent files: identical bodies and descriptions on both hosts; tools `Bash, PowerShell, Read, Grep, Glob` / `["execute","read","search"]` (no Write/Edit); Opus 5.5 on both; version line 0.9.0.
- Card `spec-critic.md` holds: who you are, input, three kinds of finding, what you do not do, reply shape.
- Cost: `costs/sessions.py` (`is_specification_agent`), `costs/transcripts.py` (`_grill_use`), `commands/cost/sessions.py` (grill line count "N spec-writers, M spec critics"); test_costs case added; AGENTS.md names the exception.
- Old rules updated: chief-of-staff.md (Say table l.25, roles list, own subagents l.168, release/fix spec l.224, direct mode l.607 and l.1177, cost l.1129), init, pr-template, routing, concepts (first-lines row, who reads what, restart, paragraph), status-layout, docs/costs.
- SVGs: 🧐 present in cr-lifecycle (3), cr-lifecycle-simple (3), the three how-chantier-works (1 each), matching their -texts.md counts; cr-lifecycle `<desc>` equals its texts line 3 (checked in diff). `cr-folder-lifecycle.svg` and its texts: no diff in the CR patch.
- Not rendered to image (no renderer used).

Notes, none blocking:
- Untracked `run_scenario.py` at the worktree root, not in the commit.
- A stale comment in test_plugin_files.py ("Sonnet by default") above CLAUDE_OPUS_ROLES, pre-existing.
- Scenario checks not run by me; CI scenario job pending.
