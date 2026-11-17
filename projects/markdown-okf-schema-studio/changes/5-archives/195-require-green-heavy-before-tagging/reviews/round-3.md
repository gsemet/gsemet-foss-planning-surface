# CR 195 — Inspector review, round 3

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-195 (uncommitted diff).

## Verdict: APPROVE

Round 3 changed only documentation, and every round-2 finding that called for a change is
addressed. Nothing else regressed.

## Round-2 findings: status

1. **Fixed (MINOR, design.md artifact code path).**
   - The note no longer claims that `filterLatest` covers Pages.
   - It now says `report` downloads by `pattern:` and Pages downloads `studio-reports` by `name:`,
     which is a different code path. The latest-wins behaviour for `name:` is marked "not verified
     against the source here", and the proof run decides it.
   - The proof workflow section names the expected evidence: the summary shows artifact
     "attempt 2".
2. **Fixed (NIT, CONTRIBUTING contradiction).** It now reads "On a pull request and an ordinary
   push (no version change), CI runs only the simulated tests". This is consistent with the
   version-change sentence a few lines below.
3. **Fixed (NIT, rule 13 title).** The title, "**Real VS Code jobs are manual, except on a
   version-change push (rule 14).**", now fits on one line within 100 characters. No added line in
   ci.guidelines.md or CONTRIBUTING.md is over 101 characters.
4. **INFO, no action needed.** The proof workflow is still outside the repo
   (/private/tmp/claude-502/cr195-driver/). Delete it from the branch before the squash if it is
   ever pushed there.
5. **Done (INFO, limits).** The CONTRIBUTING recovery section ends with "GitHub allows re-runs for
   30 days and at most 50 attempts per run; after that, release a new version." This matches the
   verbatim quotes recorded in design.md.

## Regression check

- `git diff --stat`: the same 12 files as round 2 (630+/62-). There are no new or unexpected
  files.
- `uv run --group requirements okfreq validate --check-links --project-root .`: 1067
  requirements, 0 errors, 0 warnings.
- `uv run pytest test/build -q`: 115 passed. The 12 warnings are pytest temp-dir cleanup noise.

## Findings

1. **[NIT] design.md line 114 is 102 characters.** It is a working note, so this does not block.
   The URL lines at 77–78 are long, which is fine.

Nothing left running.
