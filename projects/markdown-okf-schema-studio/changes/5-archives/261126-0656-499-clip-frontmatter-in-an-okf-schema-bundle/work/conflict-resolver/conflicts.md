# Conflicts: stack restack of CR-499 (batch-09)

Branch `chantier/batch-09/cr-499-feature-clip-the-frontmatter-in-an-okf-s` replayed on
`chantier/batch-09/cr-498-feature-clip-a-very-wide-table-in-auto-w` (37ef61b3, local). The rebase
had stopped at its only commit (635f1ba0) and is now complete.

Result: b7518fb3c16b8ac5da27f87c1165837530e5127f (head, `docs: add the OKF Schema bundle
frontmatter feature clip`, replay of 635f1ba0). Commit message kept, no merge commit, nothing
pushed, working tree clean. The branch differs from its remote branch (rewritten history): a push
needs force-with-lease. The raw links of the PR body at the old head 635f1ba point to the old
commit.

## Conflicted hunks

`docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base listed every sibling clip; the commit
   added "bundle frontmatter". Choice: the base's title with "bundle frontmatter" added last.
2. End of that test. Base added the tour, radio, table, figure, frontmatter, modes and wide imports
   and assertions; the commit added the `okf-schema-bundle-frontmatter` ones. Choice: keep all, base
   first; bundle expects its own `{ editMode: "on", paste: false }`.

`docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. Imports: base added `EXPECTED_FIGURE`; the commit added `EXPECTED_BUNDLE`, `FIXED` and `TYPO` at
   the same place. Choice: keep both lines, figure first.
4. End of file: base added the table-anchors, wide table, figure editor, okf-frontmatter and block
   editor modes tests; the commit added its two bundle tests at the same place, sharing the closing
   `});`. Choice: keep all complete tests, base first, then bundle, each with its own closing line.

`docs/user/okf.md`:

5. Both sides added an image after the same paragraph. Choice: keep both, the standard
   `okf-frontmatter` GIF first, a blank line, then the bundle GIF (specification, section 6). Both
   alt texts unchanged.

`test/site/siteClips.test.ts`:

6. Base added the "frontmatter clip" and "wide table clip" tests; the commit added the "schema bundle
   frontmatter clip" test at the same place, sharing the closing loop body. Choice: keep all complete
   tests, base first, then bundle, each with its own closing lines and its
   `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

No marker left; the diff of the four resolved files against the base leaves their first lines
unchanged (no byte-order mark added) and holds only the commit's own additions (61 insertions, 1
deletion: the title). The branch changes 23 files against the base, all its own. File-size ratchet
kept: no baseline change. No requirements file conflicted, so `just requirements-update` was not
run.

## Checks

- Targeted: `node --test` on the two resolved clip kit test files: 44 pass, 0 fail.
- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-499/justfile" check`
  (resolved tree of b7518fb3): passed (exit 0). Clip kit 53/53; unit 5305 tests, 5297 pass, 0 fail,
  8 skipped; contract run reports 0 tests; security 107/107; release pytest 205 passed; release notes
  ok; requirements lint 0 errors, 26 warnings; coverage check 0 files would change; use case diagrams
  parse; file-size ratchet passed (1340 files, 0 on the size baseline). Tree clean afterwards. Raw
  log: `just-check.log` beside this file.
- Not run: `just ci-static`, `just preflight`.
