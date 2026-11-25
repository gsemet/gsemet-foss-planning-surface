# Conflicts: stack restack of CR-494 (batch-09)

Branch `chantier/batch-09/cr-494-feature-clip-move-table-rows-and-columns` rebased on
`chantier/batch-09/cr-492-feature-clip-pick-an-option-the-file-fol` (1d55649b). The rebase stopped at
commit 2 of 2 (6b54c6e6, `test: check the table handles clip storyboard and its docs page`) and is
now complete.

Result: cc917941 (`docs: add the table row and column handles feature clip`), then c3c3a57e (head,
the `test:` commit). Commit messages kept, no merge commit, nothing pushed, working tree clean. The
branch differs from its remote branch (rewritten history): a push needs force-with-lease.

## Conflicted hunks

Both in `docs/demo-video/clip-kit/lib/check.test.mjs`.

1. Title of "the shipped scenarios declare their checks". Base added "export", "renderings tour" and
   "radio"; the commit added "table". Choice: one title naming all of them: "drag, paste, raw copy,
   export, diff, grid, theme, renderings tour, radio and table clips".
2. End of that test. Base added the `advanced-renderings-tour` and `radio-buttons` imports and
   assertions; the commit added the `table-anchors` ones. Choice: keep all three, base first, then
   table; each expects what its own side expected (tour and radio `{ editMode: "off", paste: false }`,
   table `{ editMode: "on", paste: false }`).

Auto-merged, not edited: `docs/demo-video/clip-kit/lib/storyboard.test.mjs` and
`test/site/siteClips.test.ts` (staged by Git); `docs/user/editing.md` holds the renderings tour,
table and radio GIFs.

No marker left; the resolved file starts with the same bytes as on the base (no byte-order mark).
File-size ratchet kept: no baseline change.

## Checks

- `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-494/justfile" requirements-update`
  (run before `rebase --continue`): 0 files updated, 0 indexes, 0 projections.
- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-494/justfile" check`
  (head c3c3a57e): passed. Clip kit 42/42; unit 5300 tests, 5293 pass, 0 fail, 7 skipped; contract
  run reports 0 tests; security 107/107; release pytest 205 passed; release notes ok; requirements
  lint 0 errors, 26 warnings; file-size ratchet passed (1340 files, 0 on the size baseline). Tree
  clean afterwards.
- Not run: `just ci-static`, `just preflight`.
