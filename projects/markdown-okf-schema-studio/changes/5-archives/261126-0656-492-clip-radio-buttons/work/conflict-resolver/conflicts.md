# Conflicts: stack restack of CR-492 (batch-09)

Branch `chantier/batch-09/cr-492-feature-clip-pick-an-option-the-file-fol` rebased on
`chantier/batch-09/cr-493-clip-the-advanced-renderings-tour-and-cl` (8c6845a5). The rebase stopped at
commit 2 of 2 (211f3a59, `test: check the radio clip's storyboard, stage and docs page`) and is now
complete.

Result: fd5cbb9f (`docs: add the radio choice feature clip`), then 1d55649b (head, the `test:`
commit). Commit messages kept, no merge commit, nothing pushed, working tree clean.

## Conflicted hunks

1. `docs/demo-video/clip-kit/lib/check.test.mjs`, title of "the shipped scenarios declare their
   checks". Base added "export" and "renderings tour"; the commit added "radio". Choice: one title
   naming all of them: "drag, paste, raw copy, export, diff, grid, theme, renderings tour and radio
   clips".
2. Same file, end of that test. Base added the `advanced-renderings-tour` import and assertion; the
   commit added the `radio-buttons` ones. Choice: keep both, tour first, then radio; both expect
   `{ editMode: "off", paste: false }` as on their own side.
3. `test/site/siteClips.test.ts`, one hunk where each side added a test of the editing page at the
   same place, sharing the closing loop body. Choice: keep both complete tests ("renderings tour
   clip", then "radio clip"), each with its own closing lines and its
   `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

Auto-merged, not edited: `docs/demo-video/clip-kit/lib/storyboard.test.mjs` (staged by Git);
`docs/user/editing.md` holds both clip GIFs.

No marker left; both resolved files start with the same bytes as before (no byte-order mark).

## Checks at the rebased head

- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-492/justfile" check`
  (head 1d55649b): passed. Clip kit 40/40; unit 5299 tests, 5291 pass, 0 fail, 8 skipped; contract
  run reports 0 tests; security 107/107; release pytest 205 passed; release notes ok; requirements
  lint ok (warnings only); file-size ratchet passed (1340 files, 0 on the size baseline). Tree clean
  afterwards.
- `just ... requirements-update` (run before `rebase --continue`): 0 files updated, 0 indexes, 0
  projections.
- Not run: `just ci-static`, `just preflight`.
