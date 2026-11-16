Recommend and check the Claude Code configuration chantier needs

chantier should know how to recommend the right Claude Code configuration to its users, and
check it at start, where it already runs its other host checks (e.g. "host is Claude Desktop",
`preflight` P1). Goal: fewer auto-mode interruptions, and long sessions that hold.

## What happened on the user's machine over one week (Nov 3-9, 33 sessions, 575 subagents)

1. Auto mode refused normal chantier actions:
   - `git -C <worktree> push --force-with-lease=<branch>:<sha> -u origin chantier/...` refused
     as "Git Destructive" (4 times). The user's rules covered only
     `git push --force-with-lease origin chantier/*`, without `-C`.
   - `uv run --script .../chantier.py merge|ship|spawn ...` refused as "Merge Without Review",
     or with no classifier verdict (5 times).
   - `gh pr create ...` refused as "Git Destructive" (once).
   - `mcp__ccd_pr__set_monitor` (a PR's auto-fix) refused (twice).
   - The Foreman's `SendMessage` to a Driver refused (twice).
   - `Agent` starting chantier:release-driver or chantier:cr-driver refused (3 times:
     "Create Public Surface", "Merge Without Review", "Git Destructive").
2. Refusals that were right: chantier must not do these, or must ask first:
   - `git commit --amend --reset-author`, `git branch -D` + `git push origin --delete`,
     `git update-ref -d`.
   - `Remove-Item -Recurse -Force` on `.claude`, or on %TEMP% folders named by a wildcard
     (`claude-eval-*`, `chsmoke-*`).
3. The allow rules the user plans for `~/.claude/settings.json`:
   ```
   "PowerShell(git push --force-with-lease*)",
   "PowerShell(git -C * push --force-with-lease*)",
   "Bash(git push --force-with-lease*)",
   "Bash(git -C * push --force-with-lease*)",
   "PowerShell(uv run --script *chantier.py *)",
   "Bash(uv run --script *chantier.py *)",
   "PowerShell(gh pr create*)",
   "PowerShell(gh pr checks*)",
   "mcp__ccd_pr__set_monitor",
   "SendMessage",
   "Edit(~/Projets/**)"
   ```
   Known constraints: in auto mode Claude Code ignores rules that are too broad
   (`PowerShell(*)`, `PowerShell(uv run *)`). A chained command (`a; b; c`) passes only if
   each part matches a rule. Unknown: whether an allow rule on `Agent(...)` bypasses the
   classifier, and how assignments such as `$w='...'` are treated by these rules.
4. Context and compaction:
   - Chief of Staff and Foreman sessions last days: 393 messages and 50 compactions in 45 h for
     one, 21 compactions for another.
   - The user just set `"idleCompaction": true` (many pauses over an hour, and the cache expires
     after 1 h). They have `"autoCompactWindow": 300000`, yet sessions compact around
     165-170k tokens.
5. Errors that come from chantier's own agents:
   - 177 times "File has not been read yet": agents (mostly subagents) `Write` an existing file
     without reading it first.
   - Long commands chaining 5 to 10 parts, which keeps allow rules from applying.
   - `claude` missing from PATH (5 failures), and `python` resolving to the Microsoft Store
     alias (15 failures, fixed since on the user's machine).

## What the user wants

- A reference in the plugin (e.g. `skills/chantier/references/`) saying what to configure to run
  chantier on Claude Code: recommended allow rules, each with the risk it accepts; what must stay
  blocked and why; compaction settings; prerequisites (git, bash, uv, python, gh, claude).
  Written in the project's language, each Claude Code claim checked against the official
  documentation before it is written; what cannot be checked is marked unverified.
- A check at start, next to the existing host checks, that reads `~/.claude/settings.json` (and
  the project's `.claude/settings.json`), reports the missing rules and absent prerequisites,
  and gives the user the exact JSON block to add. It never changes the user's settings itself.
- In the contracts of the roles that run commands: one command per call when possible, rather
  than long chains; read a file before overwriting it; `git -C <worktree>` accepted, but push
  only with `--force-with-lease`.

First step asked by the user: say where this goes in chantier (which files, which CRs) and what
could be verified in the documentation, before writing anything.
