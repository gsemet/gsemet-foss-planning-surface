# Conflicts: CR-477 rebase onto CR-479's final head

Rebase: `git rebase --onto origin/chantier/batch-09/cr-479-heavy-ci-red-on-main-preview-smoke-reads 39b2232d`
(onto 0303eaf7). Result: 1cc5fb19 (fix, was da565882), b54b414c (test, was 1f8496a0). Linear history,
no merge commit, nothing pushed.

## Hunks

1. `CHANGELOG.md`, `## Unreleased`, commit da565882.
   - HEAD (CR-479): `as in 1.12.0 (CR-479 heavy-red, PR #495).`
   - da565882 (CR-477): the same line with `PR #493`, followed by CR-477's new entry
     "A Markdown file now opens as text again ... (CR-477 raw-text, PR #0)."
   - Choice: kept CR-479's line with `PR #495` (HEAD side, its current PR) and CR-477's whole new
     entry right after it, unchanged (the `PR #0` placeholder is left for CR-478 to fill).
   - No byte-order mark before or after (file starts with `# C`). No conflict markers left.

Commit 1f8496a0 applied without conflict.

Untracked `test/integration/fixtures/open-at-line-*` directories were left alone.

## Fast gate

Command, as run in the worktree: `just check`
Result: pass (exit code 0). Raw log: `work/gates/conflict-resolver-just-check.log`.
