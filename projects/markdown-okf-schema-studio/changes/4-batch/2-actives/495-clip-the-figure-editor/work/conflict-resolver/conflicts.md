# Conflicts: stack restack of CR-495 (batch-09)

Branch `chantier/batch-09/cr-495-feature-clip-edit-a-figure-in-one-form` rebased on
`chantier/batch-09/cr-494-feature-clip-move-table-rows-and-columns` (c3c3a57e, local). The rebase
stopped at commit 1 of 2 (acd68b6d), then at commit 2 of 2 (d930238c), and is now complete.

Result: 5dfa76e5 (`docs: add the figure editor feature clip`), then cae819b9 (head,
`test: play the figure editor clip on the editing page of the docs site`). Commit messages kept, no
merge commit, nothing pushed, working tree clean. The branch differs from its remote branch
(rewritten history): a push needs force-with-lease.

## Conflicted hunks

Commit 1 (acd68b6d), `docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base added "export", "renderings tour",
   "radio" and "table"; the commit added "figure". Choice: one title naming all of them: "drag,
   paste, raw copy, export, diff, grid, theme, renderings tour, radio, table and figure clips".
2. End of that test. Base added the `advanced-renderings-tour`, `radio-buttons` and `table-anchors`
   imports and assertions; the commit added the `figure-editor` ones. Choice: keep all four, base
   first, then figure; each expects what its own side expected (figure
   `{ editMode: "on", paste: false }`).

Commit 1, `docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. End of file: base added the two `table-anchors` tests (storyboard, stage); the commit added the
   two `figure-editor` tests (storyboard, stage) at the same place, sharing the closing `});`.
   Choice: keep all four complete tests, table first, then figure, each with its own closing line.
   The imports and `LENGTH_FIGURE` auto-merged.

Auto-merged in commit 1, not edited: `docs/user/editing.md` (the figure GIF added beside the base's
clip GIFs).

Commit 2 (d930238c), `test/site/siteClips.test.ts`:

4. Base added the "table handles clip" test; the commit added the "figure editor clip" test at the
   same place, sharing the closing loop body. Choice: keep both complete tests, table first, then
   figure, each with its own closing lines and its `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

No marker left; the three resolved files start with the same bytes as on the base (no byte-order
mark). File-size ratchet kept: no baseline change. No requirements file conflicted, so
`just requirements-update` was not run.

## Checks

- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-495/justfile" check`
  (head cae819b9): passed. Clip kit 44/44; unit 5301 tests, 5294 pass, 0 fail, 7 skipped; contract
  run reports 0 tests; security 107/107; release pytest 205 passed; release notes ok; requirements
  lint 0 errors, 26 warnings; coverage check 0 files would change; file-size ratchet passed (1340
  files, 0 on the size baseline). Tree clean afterwards.
- Not run: `just ci-static`, `just preflight`.
