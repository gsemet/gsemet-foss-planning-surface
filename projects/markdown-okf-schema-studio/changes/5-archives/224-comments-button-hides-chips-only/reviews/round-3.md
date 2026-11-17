# Review round 3 — CR 224 (Comments button hides every review mark)

Inspector, final review of the uncommitted change in `markdown-okf-schema-studio-wt-224`
(base origin/main 0b4ede78).

Verdict: APPROVE

No findings. The two round-2 doc nits are fixed, the file set is the same as in round 2, and both
gates pass.

## Round-2 findings

1. **Line over 100 characters: fixed.** None of the added lines in `docs/user/settings.md`,
   `docs/user/review-comments.md`, `docs/user/toolbar.md` or `CHANGELOG.md` is over 100
   characters. The stray broken line ("chips in open" on its own line) is gone.
2. **"them" in settings.md: fixed.** The `preview.showComments` bullet now says that Off hides
   every review mark in open previews (gray and thread chips, highlighted quotes, badges, the
   Orphaned comments box) and removes the Comments button. It also says that while the setting is
   on, the button hides and shows the same review marks in preview and edit mode. This matches the
   behaviour note and the code: either trigger hides the same set, and the setting also removes the
   button. It is consistent with `docs/user/toolbar.md` (the toggle hides the gray chips and every
   review mark, in preview and edit mode) and with `docs/user/review-comments.md` (the button hides
   all of it, and the setting set to off does the same and removes the button). "TODO chips always
   show" is kept.

## New findings

None.

## What I checked

- File set: `git status` shows 27 modified files and 2 untracked files
  (`test/page/runtimeCommentsHidden.test.ts`, `test/visual/reviewMarksHiddenScenarios.ts`). This is
  the same set that round 2 reviewed. No new file was added in round 3.
- Leftovers: the added lines contain no `console.log`, `debugger` or `.only(`. The `TODO` matches
  are the TODO-chip wording. No `out/` file is tracked. Under `test/visual/`, the only files that
  are not committed are the ones above; `__pycache__/` and `fixtures/gen-huge-document.md` are
  ignored. No temporary scenario is left behind. No process from the worktree is still running.
- Gates (run by me):
  - `env -u VIRTUAL_ENV UV_NO_CONFIG=1 just check` exits 0:
    - unit: 3327/3327 pass;
    - security: 71/71 pass;
    - contracts: 0 tests, as on main;
    - Python: 153 passed;
    - requirements: 1072 requirements, 0 errors, 21 warnings, and 0 indexes, projections or files
      would change.
  - `okfreq validate --check-links`: exits 0, with 1072 requirements, 0 errors and 21 warnings. The
    warnings are older broken example links in other files. None is under `review-annotations`.
- I ran no visual captures.

## Open from earlier rounds (not blocking)

- Round 1 nit 5: add a backlog line to split `src/page/modules/commentThreads.ts`.
- Round 1 nit 6: the driver must list StRS-MDOKFSTUDIO-REVIEW-012 (approved; only the generated
  links block changed) in the PR body.
