# CR-169 verification at f323bc9 (verifier, 2026-11-11)
1. just check (worktree, head f323bc9): 41 passed; release-notes ok.
2. Scenario: github-20261111-002337.md 451/451, gitlab-20261111-002936.md 451/451 (both after the 00:17 commit). S1-S6 checks all [x] (S1 x3, S2 x3, S3, S4 x11, S5, S6). Earlier FAIL log (000604) was before the fix commit f323bc9.
3. By hand, scratch repo %TEMP%\v169 (python chantier.py):
 - no yaml: exit 0, "playbook: no chantier.yaml, the plugin's agents and models", 12 roles "(its file's)"; copilot ids chantier-<role>.
 - valid (coder agent/model haiku/skills/tools, cr-driver my-driver): resolved "model=haiku (claude-haiku-5-5, Claude Haiku 5.5)", needs line.
 - BOM (EF BB BF bytes): valid.
 - refusals, exit 2, with line: unknown role (2), unknown key (3), unknown top key (1), empty role (2), tab (2), anchor (2), duplicate key (4, first at 3), "opus 5.6" unknown listing models (3), "5.5" and "5.6" no-letter (3), gpt --host copilot ambiguous Luna/Sol (3), model on --host copilot "cannot set a model ... (hosts/copilot.md, "Models")" (3).
 - preflight: P12 ok "chantier.yaml valid: 1 roles configured"; invalid: P12 FAIL with first problem + run playbook.
 - open on invalid: exit 2 with the line, CR folder still in 2-backlog, nothing moved. open on valid: batch-01 opened, batch.json holds playbook (agent, model id/name/start); playbook --batch prints it and keeps it after chantier.yaml edited.
4. git status after open: only .agents/changes/ paths (batch.json is gitignored inside it).
5. grep "only configuration": AGENTS.md, README, 4 SKILL.md, session-start.md all carry the amendment; no unamended sentence.
6. hosts/claude-code.md rows 26, 27, 34: alias haiku -> claude-haiku-5-5, proved 2026-11-10; copilot.md row 21: capability none, unproved, with trial.
Not re-run by me: the 2026-11-10 trial itself (no transcript in the CR folder); take/handoff team: lines and needs warning only via scenario checks.
