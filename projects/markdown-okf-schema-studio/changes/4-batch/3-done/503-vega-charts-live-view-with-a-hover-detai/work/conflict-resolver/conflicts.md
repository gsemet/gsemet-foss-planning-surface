# CR-503 restack onto CR-502

`git rebase --onto chantier/batch-09/cr-502-... 3df0c861`: done, not pushed.

- Old base 3df0c86, old head 124a348.
- New base 316f283e, new head 1f209e13 (one commit, `feat(render): draw charts as live views with a
  hover detail`, message unchanged). Worktree clean.

## Conflicts of 4404b98

| File and hunk | Choice |
| --- | --- |
| `advanced-renderings-tour/clip.md` (modify/delete) | kept absent (`git rm`); the clip is not in this base |
| `advanced-renderings-tour/scenario.mjs` (modify/delete) | kept absent (`git rm`) |
| `export-html/clip.md`, one region (expected result and review notes) | base text kept; the rework text not brought in |
| `export-html/scenario.mjs`, region 1 (table, drawing and scroll helpers, `panelShown`) | base `panelShown` kept; rework helpers not brought in |
| `export-html/scenario.mjs`, region 2 (`run`, mark 2) | base tab-set mark kept |
| `export-html/scenario.mjs`, region 3 (`verify`) | base checks kept |

- Both `export-html` files equal 316f283e. Nothing in the base version needed a change for live svg
  charts: its stage `team-handbook.md` has a Mermaid flowchart and a tab set, no chart, and its
  scenario selects no chart element.
- `requirements/tiers/log.md`: no conflict; the only addition is the CR-503 entry above CR-502's.
  No clip CR entry.
- `theme-switch` clip changes merged cleanly and are kept (the only `docs/demo-video` diff).
- `just requirements-update`: 0 files, indexes and projections updated. `just requirements-lint`:
  passed, 1227 requirements, 0 errors, 26 warnings (broken cross-links in files outside the conflicts).

## 124a348

Conflicted in `export-html/scenario.mjs` (`verify`): its one change (expect no hover box element)
edits a line of the rework, which this base does not have. Nothing of it remains: skipped with
`git rebase --skip`, so no message rewrite was needed.

## Clip hunks for later

`clip-hunks-for-later.patch` (this folder) holds the `advanced-renderings-tour` and `export-html`
hunks of 4404b98, then the `export-html` hunk of 124a348, for the clip CRs above this one.
Written by hand with the Write tool; checked with `git apply --numstat` (it parses, and the per-file
line counts of the 4404b98 part match `git diff --numstat 3df0c861 4404b98`). It was not
test-applied: writing a helper script to the scratchpad was refused ("refused: .../scratchpad/check_patch.py
is outside the folders this agent may write in (...); write there"), and the check was dropped.

## For the Driver

`work/pr-body.md` still speaks of clip scenarios (line 30) and of `export-html` round 4, 124a348 and
a passing `just clip export-html take` (lines 47, 49; line 9 cites 4404b98). These no longer
describe this head.

## Fast gate

`just --justfile <worktree>/justfile --working-directory <worktree> check` at 1f209e13: passed
(exit 0). Test summaries: 35/35; 5297 tests, 5277 pass, 0 fail, 20 skipped; 107/107.
`just preflight` was not run.
