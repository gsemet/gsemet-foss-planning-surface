# Conflicts: CR-432 rebased onto origin/main 36240e0f

Commit b4687677 (feat(editor): reorder list items with a handle, like table rows) replayed onto
origin/main 36240e0f (CR-428, CR-430, CR-431). New head: a4110666, commit message unchanged.

## Conflicted hunks

- `CHANGELOG.md`, `## Unreleased`: main added the line on the failed render's fallback text
  (CR-431); the CR added the list item handle line. Both kept, main's line first, the CR's after.
- `requirements/tiers/log.md`, `## 2026-11-20`: main added "### Five code and SwRS mismatches of
  CR-347 settled (CR-431)"; the CR added "### List item handles". Both entries kept under the date
  heading, main's first, the CR's after, before "### Use case diagrams parsed at the requirements
  lint (CR-429)".

Neither file has a byte-order mark, before or after.

## Requirements

- SwRS-MDOKFSTUDIO-BLOCK-262: no file and no reference on origin/main (`git ls-tree`, `git grep`);
  okfreq validate/lint pass with it, so the id does not collide.
- `just requirements-update`, run after the hand merge: 0 coverage files, 0 indexes, 0 OKF
  projections updated, so nothing was regenerated or staged. `block-editing/index.md` lists
  BLOCK-262, and its `tested_in_files` lists the 7 test files of the CR.

## Fast gate

Run in the worktree, after staging and before `git rebase --continue`:

- `just check`: exit 0. Unit tests 4138, 4123 pass, 0 fail; second suite 101, 99 pass, 0 fail
  (the rest skipped); check-markers and requirements-lint as below. Log:
  `work/gates/cr-just-check.log`.
- `just check-markers`: exit 0, "9 companion file(s), 406 in-force SwRS marked, 25 files on the
  marker baseline".
- `just requirements-lint`: exit 0, 0 indexes / 0 projections / 0 coverage files would change;
  main paths: 92 StRS checked, 581 SwRS citations, all valid; use case diagrams: 93 StRS checked,
  all parse. The W002 and W2 lint warnings (prose, links in other SwRS) are warnings only and fail
  nothing. Log: `work/gates/cr-requirements-lint.log`.
