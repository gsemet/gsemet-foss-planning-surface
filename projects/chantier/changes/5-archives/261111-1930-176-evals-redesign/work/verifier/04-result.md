# Verifier result, CR-176 at fb0d409 (pushed head, PR 118)

Verdict: VERIFIED.

Rerun by the verifier, none of the coder's outputs trusted.

1. Links: a one-off script over `evals/**/*.md`, `README.md`, `CONTRIBUTING.md`: 73 relative links, 0 broken, `#run-a-campaign` resolves (`evals/README.md` line 31).
2. Old names: `git grep` outside `evals/results` and `.agents` finds only the old-report-names line, the claude-planted "as claude-full" last-run cell, and the `evals/real/` citation note in real-foreman. All intended.
3. Setup: `claude-planted` stages 8 CRs in `2-backlog/P1/`, with docs-review and style-review in `AGENTS.md`, exit 0. `claude-smoke` is refused (exit 1, "one of claude-planted, copilot", nothing created). `copilot` stages. Temp folders removed.
4. Staged audit: on a hand-built batch it prints PASS/FAIL/NOT SEEN lines with rail ids and the scorecard table. With a copy of `SCORECARD.md` missing J3 it prints `UNKNOWN RAIL J3` and exits 1.
5. Real audit: a sample batch (running, one `ready` CR on PR 118, one `blocked question:` CR, a stray file plus a pre-dirty file in `porcelain-at-open.txt`), read-only `gh pr view` on PR 118.
   - J5 reports the real forge facts (no eval line, head differs from the recorded one), J13 flags only the stray file, and C14/C16/C20/C11 rows are `not seen` or blank.
   - `cost` fails in the sample: the exact error is printed, the cost and steering share say `not measured`.
   - The `steering: direct` variant adds "Started by the Chief of Staff outside the batch: 1 (not audited)", takes the Chief of Staff's transcript, and names the "Chief of Staff, steering the batch" row.
6. Runbook commands: every `$CHANTIER` command and option in the three runbooks matches `--help` (close --yes, cost --by cr / --explain, log, open with --direct and --release, order add/approve/confirm/drop/grant/merged/note/qa with --note, --fix-for, pause --epoch, preflight --direct, status).
7. `just check`: 44 passed, release-notes ok, exit 0.

Also checked:

- `git diff` against the CR-174 base shows nothing under `evals/copilot` or `evals/results`.
- The "Nothing merges" section of real-foreman is the old one word for word, plus the end-state sentence.
- The README and CONTRIBUTING changes match answer 7.
- The `claude-planted` runbook keeps smoke's docs-reviewer and B-green checks, and adds the `order confirm` turn (as the PR body says).
- The PR body's claims (rails C15-C20 and J18-J24 added in `SCORECARD.md`, nothing removed, the CLI/cards untouched) hold. The remote branch head is fb0d409.

Nothing blocking. Minor, not a defect: in staged mode the audit's J13 also counts files that were dirty before the run, as the spec says (staged workspaces start clean).
