# Conflicts: stack restack of CR-501 (batch-09)

Branch `chantier/batch-09/cr-501-clip-keyboard-navigation-in-nested-admon`: the commits above the old
head da86d6e8 replayed on b7518fb3 (CR-499 branch, local) with `git rebase --onto b7518fb3 da86d6e8`.
The rebase stopped on its second commit (66b84782) and is now complete.

Result: head 5a73b6ebcf66ef80b412afcdbfd09c4defc028d8, three commits, messages kept, no merge
commit, nothing pushed, working tree clean.

| Old | New | Subject | `range-diff` |
| --- | --- | --- | --- |
| 27f400b4 | 3736d08a | docs: add the keyboard navigation feature clip | identical |
| 66b84782 | 3647698e | test: check the keyboard navigation clip's storyboard, stage and docs page | conflicts resolved |
| 3ea161ce | 5a73b6eb | docs: say the clip edits the word inside the whole admonition editor | identical |

The branch differs from its remote branch (rewritten history): a push needs force-with-lease. Links
of the PR body at the old head 3ea161c point to the old commits.

## Conflicted hunks (all in 66b84782)

`docs/demo-video/clip-kit/lib/check.test.mjs`:

1. Title of "the shipped scenarios declare their checks". Base listed every sibling clip; the commit
   added "keyboard-navigation". Choice: the base's list with "keyboard-navigation" added last ("and"
   moved from before "bundle frontmatter" to before it).
2. End of that test. Base added the radio, table, figure, frontmatter, modes, wide and bundle imports
   and assertions; the commit added the keyboard ones. Choice: keep all, base first; keyboard keeps
   its own `{ editMode: "off", paste: false }`.

`docs/demo-video/clip-kit/lib/storyboard.test.mjs`:

3. Imports: base added `EXPECTED_FIGURE` and `EXPECTED_BUNDLE`, `FIXED`, `TYPO`; the commit added
   `EXPECTED_KEYBOARD`, `STAGE_KEYBOARD` at the same place. Choice: keep all three lines, base first.
4. End of file: base added the table-anchors, wide table, figure editor, okf-frontmatter, block editor
   modes and bundle tests; the commit added its two keyboard tests at the same place, sharing the
   closing `});`. Choice: keep all complete tests, base first, then keyboard, each with its own
   closing line.

`test/site/siteClips.test.ts`:

5. Base added the "radio clip" and "block editor modes clip" tests; the commit added the "keyboard
   navigation clip" test at the same place, sharing the closing loop body. Choice: keep all complete
   tests, base first, then keyboard, each with its own closing lines and its
   `@tests_req SwRS-MDOKFSTUDIO-CORE-095` marker.

## Checks on the result

- No marker left. The diff of the three resolved files against the base leaves their first lines
  unchanged (no byte-order mark added) and holds only the commit's own additions (70 insertions, 1
  deletion: the title).
- `git diff --stat b7518fb3 HEAD`: 27 files, all the branch's own (the `clips/keyboard-navigation/`
  folder, `docs/user/editing.md` with 3 added lines, the three test files). The other clips'
  folders (`advanced-renderings-tour` included), the clip kit sources, the guidelines and
  `scripts/file-size-baseline.json` are as the base has them.
- File-size ratchet: kept, no baseline change; `check-limits: passed (1340 files, 0 on the size
  baseline)`. It measures `src/` and `test/` only: `test/site/siteClips.test.ts` has 283 lines (limit
  1500). `storyboard.test.mjs` (837 lines) and `check.test.mjs` (95) are under `docs/`, not measured,
  and under 1500 anyway.
- No requirements file conflicted, so `just requirements-update` was not run.

## Checks run

- Targeted: `node --test` on the two resolved clip kit test files: 46 pass, 0 fail.
- Fast gate: `just --justfile "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-09-CR-501/justfile" check`
  (tree of 5a73b6eb): passed (exit 0). Clip kit 55/55; unit 5306 tests, 5299 pass, 0 fail, 7 skipped;
  contract run reports 0 tests; security 107/107; release pytest 205 passed; release notes ok;
  requirements lint 0 errors, 26 warnings; coverage check 0 files would change; use case diagrams
  parse. Tree clean afterwards. Raw log: `just-check.log` beside this file.
- Not run: `just ci-static`, `just preflight`; no retake of the clip.
