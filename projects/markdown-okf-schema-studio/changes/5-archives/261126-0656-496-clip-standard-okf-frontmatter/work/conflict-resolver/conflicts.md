# Conflicts: stack restack of CR-496 (batch-09)

Branch `chantier/batch-09/cr-496-feature-clip-edit-the-standard-okf-front` replayed with
`git rebase --onto cae819b9 da86d6e8` on
`chantier/batch-09/cr-495-feature-clip-edit-a-figure-in-one-form` (cae819b9, local). The rebase
stopped at commit 2 of 2 (39d3eb31) and is now complete.

Result: c83e4c8d (`docs: add the standard OKF frontmatter feature clip`, replay of b9adf4d2, same
patch), then d386ff61 (head, `test: check the frontmatter clip's storyboard, stage and docs
page`, replay of 39d3eb31). Commit messages kept, no merge commit, nothing pushed, working tree
clean. The branch differs from its remote branch (rewritten history): a push needs
force-with-lease.

## Conflicted hunks

Commit 2 (39d3eb31), `docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base added "radio", "table" and
   "figure"; the commit added "frontmatter". Choice: one title naming all of them: "drag, paste,
   raw copy, export, diff, grid, theme, renderings tour, radio, table, figure and frontmatter
   clips".
2. End of that test. Base added the `radio-buttons`, `table-anchors` and `figure-editor` imports
   and assertions; the commit added the `okf-frontmatter` ones. Choice: keep all four, base first,
   then frontmatter; each expects what its own side expected (frontmatter
   `{ editMode: "on", paste: false }`).

Commit 2, `docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. Imports: base added `EXPECTED_RADIO`; the commit added `EXPECTED_FRONTMATTER` and
   `STAGE_FRONTMATTER` at the same place. Choice: keep both lines, radio first.
4. End of file: base added the `table-anchors` and `figure-editor` tests; the commit added the
   three `okf-frontmatter` tests at the same place, sharing the closing `});`. Choice: keep all
   complete tests, base first, then frontmatter, each with its own closing line. The `existsSync`
   import auto-merged.

Auto-merged in commit 2, not edited: `test/site/siteClips.test.ts` (the "OKF page" test added
beside the base's clip tests).

No marker left; the resolved files start with the same bytes as before (no byte-order mark).
Against the base, the branch changes only its own 20 files (the `okf-frontmatter` clip folder,
`docs/user/okf.md` and the three test files): the other clips' files, `advanced-renderings-tour`
included, are as the base has them. File-size ratchet kept: no baseline change. No requirements
file conflicted, so `just requirements-update` was not run.

## Checks

- Targeted: `node --test` on the two resolved clip kit test files: 38 pass, 0 fail.
- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-496/justfile" check`
  (resolved tree of d386ff61): passed. Clip kit 47/47; unit 5302 tests, 5295 pass, 0 fail, 7
  skipped; contract run reports 0 tests; security 107/107; release pytest 205 passed; release notes
  ok; requirements lint 0 errors, 26 warnings; coverage check 0 files would change; use case
  diagrams parse; file-size ratchet passed (1340 files, 0 on the size baseline). Tree clean
  afterwards.
- Not run: `just ci-static`, `just preflight`.
