# Conflicts: stack restack of CR-498 (batch-09)

Branch `chantier/batch-09/cr-498-feature-clip-a-very-wide-table-in-auto-w` replayed with
`git rebase --onto af4a4aa6 d930238c` (base: CR-497's local branch). The rebase stopped at commit
2 of 2 (cb1ccf69) and is now complete.

Result: 35c8a05c (`docs: add the wide table Auto width feature clip`, replay of 1223027a), then
37ef61b338b3ca56d1cb428983c78ebdb54684f0 (head, `test: check the wide table clip's storyboard,
stage and docs page`, replay of cb1ccf69). Commit messages kept, linear history, nothing pushed,
working tree clean. The branch differs from its remote branch (rewritten history): a push needs
force-with-lease.

## Conflicted hunks

Commit 2 (cb1ccf69), `docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base added "export", "renderings tour",
   "radio", "table", "frontmatter" and "modes"; the commit added "wide table". Choice: one title
   naming all of them: "drag, paste, raw copy, export, diff, grid, theme, renderings tour, radio,
   table, figure, frontmatter, modes and wide table clips".
2. End of that test. Base added the `okf-frontmatter` and `block-editor-modes` imports and
   assertions; the commit added the `wide-table-auto-width` ones. Choice: keep all, base first;
   each expects what its own side expected (wide `{ editMode: "off", paste: false }`).

Commit 2, `docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. Constants: base added `MARKS_TABLE`, `STAGE_TABLE` and `MARKS_MODES`; the commit added
   `MARKS_WIDE` at the same place, sharing the closing `];`. Choice: keep all four, base first,
   each with its own closing line.
4. Tests after the theme-switch stage test: base added the `table-anchors` tests; the commit added
   the two `wide-table-auto-width` tests at the same place, sharing the closing `});`. Choice: keep
   all complete tests, base first, then wide, each with its own closing line. The `STAGE_WIDE`
   import and `ZOOM_HOLD_WIDE` auto-merged.

Commit 2, `test/site/siteClips.test.ts`:

5. Base added the "frontmatter clip" test; the commit added the "wide table clip" test at the same
   place, sharing the closing loop body. Choice: keep both complete tests, base first, then wide,
   each with its own closing lines and its `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

## Pages and clip files checked

- `docs/user/wide-tables.md` (auto-merged in commit 1): against `origin/main` (17b779d5, which
  holds CR-508's commit c6a1cda8 and is the merge base of the CR-497 base) the only difference is
  the added blank line and wide table GIF line. So CR-508's code block paragraph and this CR's clip
  entry are both in the result.
- `docs/user/editing.md`: no difference from the base af4a4aa6. Its 7 clip GIF entries
  (advanced-renderings-tour, drag-list-item, block-editor-modes, figure-editor,
  paste-spreadsheet-cells, table-anchors, radio-buttons) include the 3 of the old head d930238c.
- `docs/demo-video/clips/figure-editor/`: no difference from the base af4a4aa6.
- Against the base, the three resolved files differ by exactly the commit's own additions (61
  insertions, 1 deletion: the title); their first lines are unchanged (no byte-order mark added).
  The branch changes 19 files against the base, all its own.
- File-size ratchet kept: no baseline change. No requirements file conflicted, so
  `just requirements-update` was not run.

## Checks

- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-498/justfile" check`
  (at head 37ef61b3): passed (exit 0). Clip kit 51/51; unit 5304 tests, 5297 pass, 0 fail, 7
  skipped; contract run reports 0 tests; security 107/107; release pytest 205 passed; requirements
  lint 0 errors, 26 warnings; coverage check 0 files would change; use case diagrams parse;
  file-size ratchet passed (1340 files, 0 on the size baseline). Tree clean afterwards. Raw log:
  `just-check.log` beside this file.
- Not run: `just ci-static`, `just preflight`.
