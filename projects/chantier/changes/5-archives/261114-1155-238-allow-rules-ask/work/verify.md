# Verify CR-238

Head: 9d44a00162ec8b5b397d5f1a391b0501ec79f494
Verdict: VERIFIED

Run at 9d44a00 in the worktree, worktree CLI (`uv run --locked --project .`), scratch HOME/USERPROFILE/CLAUDE_CONFIG_DIR.

1. Restack changed nothing of the CR. `git range-diff 3a96b35...9d44a00`: commit 8 (the CR) is `=` to 3a96b35; only the base moved (commit 6 new, from main). Gate pass and the 3a96b35 proofs are carried from 3a96b35 (gate log 20261114-075221.log, `result: pass at 3a96b35...`): the patch is identical; the user waiver (Rebase-Q1 A) covers a new local gate.
2. P10. `pytest -q` in skills/chantier/scripts/cli -> `63 passed` (at 9d44a00). Empty settings -> `P10 warn 15 of 15 commands ...` (gh stack installed), no `release create` in the line. Settings holding all 35 RECOMMENDED_ALLOW (none has `release`) -> `P10 ok   the commands chantier's agents run are allowed by your settings`.
3. Templates extracted from hosts/claude-code.md and run on scratch homes, each case twice (absent / other keys / partial): PowerShell 5.1 and sh give valid JSON, bom=False, no duplicate, other keys and `Bash(ls*)`/deny kept (counts 3, 3, 5 for 3 rules). preflight reads the partial result as `P10 warn 13 of 15` (only 2 of the 3 test rules in the set), i.e. it parses the file.
4. Cards/docs: diff matches spec sections 2-6b; grep over README, CONTRIBUTING, AGENTS, docs, scenario, cards for "never writes/edits ... settings", "16 commands", "gh release create*" -> no hit. `git diff --name-only origin/main...HEAD -- agents com.github.copilot` -> empty. Worktree clean.
5. PR body (#176, posted): sections in order, one fold, Known gaps names the real-session proof, POSIX-only-on-Git-for-Windows and escapes; Changes match the diff; its two pending boxes are this verdict and CI at 9d44a00. VERIFIED.

Not proved here (as the PR says): a real session with the Chief of Staff question; Linux/macOS sh.
