# gate runs only named commands; lease hold runs nothing

Split from `permissions-bypass` on the user's answer perm-bypass-Q17 (A, 2026-11-21), its second step, after a Fable critic's review. `chantier gate <cr> "<command>"` runs its text through a shell (gate.py:113-114) and `chantier lease hold -- <command>` runs what it is given (leases.py:95); both are covered by chantier's allow rules, so an agent with Bash can run any command with no prompt.

Scope: `gate` runs only commands named in the project's chantier.yaml (permissions-bypass answers Q1, Q9, Q14, Q15 carry over); `lease hold` runs nothing and keeps the lease for a bounded time (for instance `--minutes 45`) instead of watching a PID (replaces Q2 and Q13; the user has not decided the bounded time yet). Known limit: `just scenario` runs the worktree's justfile, which a Coder edits, so this protects against the read-only roles, not a Coder.

See ../permissions-bypass/02-answers.md (entries 1-18) and its 03-change-spec.md for the earlier work.
