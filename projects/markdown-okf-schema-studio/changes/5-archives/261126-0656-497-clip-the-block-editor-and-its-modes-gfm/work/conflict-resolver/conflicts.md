# Conflicts: stack restack of CR-497 (batch-09)

Branch `chantier/batch-09/cr-497-feature-clip-the-block-editor-and-its-gf` rebased on
`chantier/batch-09/cr-496-feature-clip-edit-the-standard-okf-front` (d386ff61, local). The rebase
stopped at commit 2 of 2 (18583968) and is now complete.

Result: c86a68f5 (`docs: add the block editor modes feature clip`, replay of c2adb8e9, same
patch), then af4a4aa62da55cd2093d30c7a5763c0b6bdee8ea (head, `test: check the block editor modes
clip's storyboard, stage and docs page`, replay of 18583968). Commit messages kept, no merge
commit, nothing pushed, working tree clean. The branch differs from its remote branch (rewritten
history): a push needs force-with-lease.

## Conflicted hunks

Commit 2 (18583968), `docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base added "export", "renderings tour",
   "radio", "table", "figure" and "frontmatter"; the commit added "modes". Choice: one title naming
   all of them: "drag, paste, raw copy, export, diff, grid, theme, renderings tour, radio, table,
   figure, frontmatter and modes clips".
2. End of that test. Base added the `advanced-renderings-tour`, `radio-buttons`, `table-anchors`,
   `figure-editor` and `okf-frontmatter` imports and assertions; the commit added the
   `block-editor-modes` ones. Choice: keep all, base first, then modes; each expects what its own
   side expected (modes `{ editMode: "on", paste: false }`).

Commit 2, `docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. Constants: base added `MARKS_TABLE` and `STAGE_TABLE`; the commit added `MARKS_MODES` at the
   same place. Choice: keep all three, base first.
4. End of file: base added the `table-anchors`, `figure-editor` and `okf-frontmatter` tests; the
   commit added the two `block-editor-modes` tests at the same place, sharing the closing `});`.
   Choice: keep all complete tests, base first, then modes, each with its own closing line. The
   `STAGE_MODES` import auto-merged.

Commit 2, `test/site/siteClips.test.ts`:

5. Base added the "renderings tour clip" and "radio clip" tests; the commit added the "block editor
   modes clip" test at the same place, sharing the closing loop body. Choice: keep all three
   complete tests, base first, then modes, each with its own closing lines and its
   `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

Commit 1 (c2adb8e9) applied without a stop (`docs/user/editing.md` auto-merged; the base's clip
GIFs and the modes GIF are all in the page).

No marker left; the diff of the three resolved files against the base shows no change on their
first line (no byte-order mark added). Against the base, the branch changes only its own 23 files
(the `block-editor-modes` clip folder, `docs/user/editing.md` and the three test files).
File-size ratchet kept: no baseline change. No requirements file conflicted, so
`just requirements-update` was not run.

## Checks

- Targeted: `node --test` on the two resolved clip kit test files: 40 pass, 0 fail.
- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-497/justfile" check`
  (resolved tree of af4a4aa6): passed. Clip kit 49/49; unit 5303 tests, 5296 pass, 0 fail, 7
  skipped (the 13 site clip video tests pass); contract run reports 0 tests; security 107/107;
  release pytest 205 passed; release notes ok; requirements lint 0 errors, 26 warnings; coverage
  check 0 files would change; use case diagrams parse; file-size ratchet passed (1340 files, 0 on
  the size baseline). Tree clean afterwards.
- Not run: `just ci-static`, `just preflight`.
