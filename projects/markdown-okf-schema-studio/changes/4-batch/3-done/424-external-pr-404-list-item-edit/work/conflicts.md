# Conflicts: cherry-pick of external PR 404 onto CR-351's head

- Worktree: `C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-424`, branch
  `chantier/batch-06/cr-424-take-ownership-of-external-pr-404-list-i`, base `3d1c337` (CR-351's head).
- Operation: `git cherry-pick 3de1bc46d8b69ee75318838b018fed0762a482fd` (one commit of PR 404,
  written on main at `24c9eef0`), started by the Driver; two files conflicted, the rest applied.
- Result: commit `d582d008` "feat(editor): a click on a list item edits that item only", author
  `pspozio <242682982+pspozio@users.noreply.github.com>` (kept), committer Gaetan SEMET; message
  unchanged (`-c core.editor=true cherry-pick --continue`). Not pushed.

## `requirements/tiers/log.md`

- Hunk: under `## 2026-11-20`, the base's entry `### Gallery and site on a heavy CI dispatch
  (CR-350)` against the contribution's entry `### A click on a list item edits that item; list
  items can be listed in the TOC`.
- Choice: both entries kept, unchanged, under the one `## 2026-11-20` heading (one heading per date,
  `requirements/guidelines/project.guidelines.md`); the base's entry first, the contribution's
  appended after it (the rule says to append to an existing date section), with a blank line between.
- No generated block of the requirements bundle conflicted, so `just requirements-update` was not
  run; the gate's `okfreq lint --check` and `update-coverage --check` report 0 changes.

## `test/core/preview/previewStyles.test.ts`

- Hunk: at the end of the file, the base's test `code blocks use one font scale, one box, and scroll
  a long line only when it does not fit` (`@tests_req SwRS-MDOKFSTUDIO-CODE-007`) against the
  contribution's test `the editor of an ordered list item counts as that item, so the next items
  keep their numbers` (`@tests_req SwRS-MDOKFSTUDIO-BLOCK-014`); both added a test in the same place
  and shared the closing `});`.
- Choice: both tests kept, the base's first, each with its own `});`, separated by a blank line.
  No assertion changed.

## Byte-order mark

Both resolved files start as before the conflict (`# U` and `imp`, no BOM).

## Fast gate

- Setup: `just dev` (exit 0), log `work/gates/conflict-resolver-dev.log`.
- Command, as run in the worktree after the cherry-pick completed: `just check`.
- Result: pass (exit 0). Node tests 4091, pass 4076, fail 0; second suite 101, pass 99, fail 0;
  pytest build tests, `release_notes.py --check`, `okfreq validate/lint/update-coverage --check` and
  `check_main_paths.py` all pass (lint: 0 indexes, 0 projections, 0 coverage files would change). The
  `W2 Broken cross-link` warnings are existing example links in PALETTE/GFM/BLOCK requirements, not
  failures. Raw log: `work/gates/conflict-resolver-check.log`.
