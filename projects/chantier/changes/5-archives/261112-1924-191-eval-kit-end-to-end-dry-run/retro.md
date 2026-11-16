# batch-14 retro

## 2026-11-12, pause 1: CR-191, CR-192, CR-193, CR-194, CR-195

- CR-191 needed 5 rounds; round 3's Coder wrote a UTF-8 BOM into evals/kit/dry_run.py on Windows and round 4 existed only to strip it: `just check` rejects a byte-order mark in any tracked text file, so a BOM is red at the gate, not at review.
- CR-191's local long gate passed at 40860c6 but the new CI job `just eval-dry-run` was red on ubuntu (`uv lock --offline` with a cold uv cache), which cost round 5: an eval-kit change that adds a CI job runs its recipe once locally with an empty uv cache (`UV_CACHE_DIR` set to a fresh folder) before the push; the spec-writer names the CI environment when a spec adds a job.
- One batch-wide gate lock queued four long gates behind one another and Drivers sat "waiting on own background work" for long stretches; CR-194's Driver started a second gate while its first was still queued (inbox item stop-own-gate, and parallel-rebase-cost for the re-gates after each merge).
- The main checkout's CLI stayed at be32d09 after CR-192 merged, so `cost` still left 17 claude-fable-5-2 calls unpriced: the steering session fast-forwards a clean main checkout after each merge it records (never touching untracked files), or the CLI is run from origin's head.
- A Driver's PowerShell escape put a form feed into PR 136's body and two description passes failed before it was re-posted from a file: the PR body is always written with the Write tool and posted with `--body-file`, never built in a PowerShell string.
- The desktop app's Auto-fix event on PR 136 asked to fix and merge the base branch in while the CR's own Driver was fixing it: hosts/claude-code.md says an Auto-fix event on a CR with a live Driver is left to that Driver, and the project's rebase rule ranks above Auto-fix's merge rule.
- The suspension on the user's word (all Drivers stopped, one order note each, heartbeat stopped) and the resume by the restart path lost no work: no fix needed; the 6 Driver restarts in `cost --explain` come from it and from CR-191's extra rounds.
