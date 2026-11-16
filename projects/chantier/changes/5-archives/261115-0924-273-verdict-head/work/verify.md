# Verify CR-273

Head: 6af61f5dfda0a8e20aea72146f6c364299dbc565

All claims judged at 6af61f5dfda0a8e20aea72146f6c364299dbc565 (worktree HEAD, `git rev-parse HEAD`, clean tree).

## 1. Three refusals, with exit code, message and no new event (scratch batch outside the repository)

SHA 6af61f5. Scratch repo `...\scratchpad\scr\proj` (batch-01, CR-101, worktree head aaa7f72), CLI run as
`uv run --no-sync --project C:\Users\gaeta\Projets\chantier.worktrees\batch-18-CR-273 chantier verdict CR-101 VERIFIED`.
Full transcript: `work/verifier/evidence/scratch-run.txt`. Count of `"verdict"` lines in the scratch `events.jsonl`:

- No file: `verdict events before=0 after=0`, `exit=2`, `... for the head aaa7f72 it records: no such file`.
- Note with no `Head:` line: `before=0 after=0`, `exit=2`, `... it records: no Head: line`.
- Stale `Head: 0123456789abcdef...`: `before=0 after=0`, `exit=2`, `... it records: its Head: line names 0123456`.

## 2. Accepted VERIFIED once the note names the head

SHA 6af61f5. Note `Head: aaa7f726bad93f08ef054be20932623c49585439`: output `verdict CR-101 VERIFIED at aaa7f72`, `exit=0`, events before=0 after=1.

## 3. NOT VERIFIED accepted with no note

SHA 6af61f5. Note removed: `verdict CR-101 NOT VERIFIED at aaa7f72`, `exit=0`, events before=1 after=2.

## 4. Diff stat limited to the spec's files

SHA 6af61f5, `git diff --stat origin/main...HEAD`: 9 files, 145 insertions, 24 deletions: evals/SCORECARD.md, evals/kit/dry_run.py, scenario/README.md, scenario/run_scenario.py, references/concepts.md, driver.md, worker.md, commands/delivery.py, tests/test_verdict_note.py. These are the spec's list plus the new test file the spec allows. No `agents/`, `hooks/` or `types/` file.

## 5. `just check` in the worktree

SHA 6af61f5, command `just check`, `exit=0`: mypy "Success: no issues found in 162 source files", biome "Checked 98 files ... No fixes applied", `168 passed in 70.35s`, release-notes ok. Log: `work/verifier/evidence/just-check.txt`.

## Not re-run by me

The long gate `just scenario` and CI (5 jobs) are cited from the PR as passed at this head (the prompt); `just eval-dry-run` not run by me. These are carried, not proved here.

VERIFIED
