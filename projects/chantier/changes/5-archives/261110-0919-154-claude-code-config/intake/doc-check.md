# Documentation check (2026-11-09, code.claude.com/docs)

| Claim | Result | Source |
| --- | --- | --- |
| `*` matches anywhere; `cmd *` (space) is a word boundary and also matches bare `cmd` | verified | permissions |
| `Bash(git push …)` does not match `git -C . push` | verified | permissions |
| `PowerShell(...)` rules have the Bash shape; aliases canonicalized, case-insensitive | verified | permissions |
| Auto mode drops broad allow rules on entry: `Bash(*)`, `PowerShell(*)`, interpreter wildcards, package-manager run commands, **`Agent` rules**, `Monitor` rules; restored on leaving | verified | permission-modes, auto-mode-config |
| `uv run --script *chantier.py *` kept or dropped in auto mode ("package-manager run commands"?) | unverified | — |
| Compound command: every subcommand must be allowed (`&&`, `\|\|`, `;`, `\|`, `&`, newline; PowerShell `\|`, `;`, 7+: `&&`, `\|\|`) | verified | permissions |
| Bash: an allow rule does not match past a leading assignment, except known-safe env vars; deny/ask do | verified | permissions |
| PowerShell `$w='...'` assignments | not documented | — |
| `Agent(Name)` rule form exists; plugin names such as `Agent(chantier:cr-driver)` | form verified; plugin names not documented | permissions, tools-reference |
| Allow/ask/deny matches resolve at once in auto mode, without the classifier (except protected paths, critical-path rm/rmdir, per-command domains) | verified | permission-modes |
| `mcp__<server>__<tool>` exact name; bare tool name matches all uses | verified | permissions |
| `SendMessage` as a rule | not documented (absent from tools-reference) | — |
| `Edit(~/path/**)`: `~` is home, `**` gitignore-style; Edit rules cover Write and NotebookEdit | verified | permissions, tools-reference |
| `autoCompactWindow`: 100000–1000000, default tuned per model, capped at the model's context window | verified | settings-reference |
| Compaction at 165–170k with `autoCompactWindow: 300000` | not explained by the docs | — |
| `idleCompaction`: default true, compacts after about an hour idle, v2.1.290+ | verified | settings-reference |
| Prompt cache: 1 h on a subscription within plan usage, 5 min on API key or cloud; `promptCacheTtl` | verified | prompt-caching |
| Settings files and precedence (managed > CLI > local > project > user); deny > ask > allow; user deny blocks project allow | verified | settings, permissions |
| Classifier label "Git Destructive"; `claude auto-mode defaults` lists the rules | verified | auto-mode-config |
| Labels "Merge Without Review", "Create Public Surface" | not documented | — |
| Write to an unread existing file fails on older models; newer models may overwrite under conditions (v2.1.228+) | verified; exact text "File has not been read yet" not documented | tools-reference |
| `CLAUDE_CODE_ENTRYPOINT` and its values (`claude-desktop`) | not documented (preflight P1 relies on it) | env-vars |
