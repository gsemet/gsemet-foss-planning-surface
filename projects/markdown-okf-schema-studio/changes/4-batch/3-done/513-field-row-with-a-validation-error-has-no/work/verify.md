# CR-513 verification

Head: 223a8c49a47f8af786412e7cff748860b18d3782

Base: `e2b2235d8b031d1542761d2b9d5070af2e975d9d` (`main`). Verdict: **VERIFIED**.

Claims 1 to 12 were judged at `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f` on base
`abfa71e58f2f150d028781beaeecc2bede4c8182`. Each is **carried from cd3b8e6**: the forge rewrote the
branch when the PRs below it merged, the three commits are identical and both the head tree and the
base tree are unchanged (claim 0b). Claim 13 (the posted description) was judged at `223a8c4`; it
replaces claim 11 for the current head. No build, test or capture ran at `223a8c4` in this pass.

`<W>` = CR worktree (HEAD `cd3b8e6`, `git status --porcelain` empty at the end), `<B>` = my detached
worktree of the base with the head's `test/` folder checked out over it (removed), `<S>` =
`work/scratch`, `<E>` = `work/verifier/evidence`. Claims 0 to 12 are at `cd3b8e6` unless said otherwise.
`chantier.yaml` has no long gate, so there is no gate pass to cite.

## Summary

| # | Claim | Verdict |
| --- | --- | --- |
| 0b | Head `223a8c4` and its base have the trees judged at `cd3b8e6` | VERIFIED |
| 1 | Unit test red on the base, green at the head | VERIFIED |
| 2 | Visual scenarios v32 to v35 fail on the base, pass at the head | VERIFIED |
| 3 | The look in the four preview modes on a dark and a light host | VERIFIED |
| 4 | The specification's walk in a real VS Code window | VERIFIED |
| 5 | Edit mode: hover, no underline under the editor or its menu | VERIFIED |
| 6 | Nothing else changes (badge, information rows, whole-document error row, markup) | VERIFIED |
| 7 | Whole-table warning wraps; tokens unset give the fallbacks | VERIFIED |
| 8 | Requirements | VERIFIED |
| 9 | `just preflight` | VERIFIED |
| 10 | CHANGELOG line | VERIFIED |
| 11 | PR description | VERIFIED |
| 12 | CI at the head (read, not run) | VERIFIED |
| 13 | PR description as posted, at `223a8c4` | VERIFIED |

## 0. Head and history

- `git rev-parse HEAD` in `<W>`: `cd3b8e6a8f02c18e3bca13aa5a32259ef01f720f`; `git status --porcelain`:
  empty.
- `git range-diff 928ebd7..7f7cc06 abfa71e..cd3b8e6`: `552cfac4 = 49022ec6`, `7e702282 = e9c82c57`,
  `7f7cc06f = cd3b8e6a` (all three identical).
- `git diff --stat 7f7cc06 cd3b8e6a -- src test`: only `test/build/*` and `test/visual/capture.py`,
  `capture_report.py`, `merge_parts.py` (brought by the base).
- `git diff abfa71e cd3b8e6 --stat`: 19 files, +570/-11; under `src/` only `pageChromeStyles.ts`,
  `propertiesStyles.ts` and their two marker files.

## 1. Unit test - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

- `<B>`: compile, `node --test out/test/core/preview/fieldIssueStyles.test.js`
  (`<S>/ver2-before-unit.log`): `tests 8, pass 0, fail 8`.
- `<W>`: `just preflight` (`<S>/ver2-preflight.log` lines 1345-1352): the 8 tests pass.
- The file (read at the head) asserts every item of section 3 of the specification: error name colour
  and background, wavy underlines, `rgba(` before `color-mix(` for the warning, the whole-document
  warning row with its wrapping, a fallback on every `var(`, no rule for information rows, markers
  084#S1, 084#S6, 023#S5. It also covers 084#S8, #S9, #S10 and 023#S10.

## 2. Visual scenarios v32 to v35 - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

- `fnm exec -- npm.cmd run visual:render`, then
  `uv run --no-sync --group docs python test/visual/capture.py --group frontmatter-schema`.
- `<B>` (`<S>/ver2-before-capture.log`): exit 1, 31 passed, v32, v33, v34, v35 failed (assertion
  failures 11, 11, 2, 2).
- `<W>` (`<S>/ver2-head-capture.log`): `{"status": "passed", "scenario_count": 35,
  "screenshot_count": 28}`, manifest revision `cd3b8e6`.
- Pairs `<E>/cd3b8e6-{before,after}-v3[2-5]-*.png`, each opened: plain rows before; coloured names,
  wavy underlines and coloured whole-table warning row after. No username, no path.

## 3. Preview modes and hosts - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

`uv run --no-sync --group docs python <S>/r4_modes_probe.py <W> <S>/ver2-modes-shots`
(`<S>/ver2-modes-probe.log`): exit 0, `RESULT: 0 failed check(s)`. Contrast of the marked text
against what is painted behind it:

| Row | Cream | White | Dark | Current, light host | Current, dark host |
| --- | --- | --- | --- | --- | --- |
| field error | 4.77 | 5.55 | 5.42 | 2.6 | 3.85 |
| field warning | 4.81 | 4.47 | 5.65 | 2.7 | 5.57 |
| whole-table warning | 4.81 | 4.47 | 5.65 | 2.7 | 5.57 |

- Cream, White and Dark print the same colours on the dark and on the light host; background as light
  as the page; hover of a field name 4.54 or more. The cells that failed at `1fa9587` (1.9 to 1.97)
  are fixed.
- Whole-document error row (unchanged by this CR): Cream on a dark host 1.97, White on a dark host
  1.95, Dark on a light host 1.9. Listed in the PR's Known gaps, as is Current on a light host.
- `git grep -n sphinx-preview-issue cd3b8e6a -- src`: only the palette declarations
  (`pageChromeStyles.ts` 35-36, 82-83, 143-144 and markers) and the new rules of
  `propertiesStyles.ts`.

## 4. The walk, in a real VS Code window - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

VS Code 1.148.0 on Windows, Extension Development Host with its own user-data and extensions folders,
bundle built at the head (`fnm exec -- npm.cmd run bundle`, `<S>/ver2-bundle.log`); no other test
window was running. `fnm exec -- node <S>/ver2_walk_run.js <W> <S>/walk2 <E>/window-cd3b8e6`
(`<S>/ver2-walk.log`): exit 0, `walk: passed`, 136 `ok`, 0 `FAIL`. Themes Dark Modern and Light
Modern; their variables are printed in the log. The preview opens in Cream.

- Step 1, both themes: `status` name `rgb(179, 38, 30)` on `rgba(179, 38, 30, 0.12)`, painted
  contrast 4.77; wavy underline under `publshed` in that colour; value text colour equals an unmarked
  value's (`rgb(43, 42, 39)`); other rows plain; badge 1 error.
- Step 2: with the strict setting turned on, `bonus_field` takes the warning colour and underline
  without a refresh (4.81).
- Step 3, through the page (select `draft` and Enter, then "Remove field"): both marks go, no
  whole-table row, no badge counts.
- Step 4: one "Schema could not be parsed" row, warning colour on a 14% tint, spanning the table.
- Both themes times the four preview modes: same figures as claim 3; forced modes identical on both.
- All 33 pictures in `<E>/window-cd3b8e6/` opened: they show their step; no username, no path.

## 5. Edit mode - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

- Real window (same log): hovered error and warning names take the theme's edit hover background and
  keep their severity colour; the open editor of the error value (select and field menu) and of the
  warning value (textarea and menu) draws no underline; the underline is back after Escape.
- `uv run --no-sync --group docs python <S>/ver_edit_probe.py <W> <B> <S>/ver2-edit-shots`
  (`<S>/ver2-edit-probe.log`): `RESULT before: 16 failed check(s)`, `RESULT after: 0 failed
  check(s)`.
- Reason for dropping the underline, `<S>/ver2_underline_probe.py` (`<S>/ver2-underline-probe.log`):
  with the rule overridden, the edited cell's decoration is `underline`, as shipped `none`;
  `<E>/cd3b8e6-underline-rule-off-on.png` (opened) shows the lines on the editor and the menu items
  only with the rule overridden.

## 6. Nothing else changes - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

`uv run --no-sync --group docs python <S>/ver2_unchanged_probe.py <W> <B>`
(`<S>/ver2-unchanged-probe.log`): exit 0; 35 scenarios (34 with a properties block), 4 modes on 2
hosts: `markup differences: 0` (badge included), cell count differences 0. Computed style differences
only in marked field rows (value decoration; name colour and background) and in whole-table warning
rows (colour, background). None in information rows (16 `th` compared), whole-document error rows
(48), unmarked field rows (2112 `td`, 1304 `th`) or other rows. The probe normalises the two build
folder paths in the markup (its first run reported those paths as differences). Validation, messages
and badge code: not in the diff (claim 0).

## 7. Wrapping and fallbacks - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

- `uv run --no-sync --group docs python <S>/ver_wrap_probe.py <W> <B> <S>/ver2-wrap-shots`
  (`<S>/ver2-wrap-probe.log`): at 360 px the head's warning row wraps to 3 lines in a cell of 301 px
  in a table of 302 px, in the warning colour on its tint; the base row wraps but is plain;
  `RESULT after: 0 failed check(s)`.
- Tokens unset (edit probe log and unit test): `rgb(241, 76, 76)` on `rgba(235, 80, 80, 0.12)`,
  `rgb(191, 136, 3)` on its 14% tint, hover `rgba(128, 128, 128, 0.12)`.
- Tokens set, light and dark: v32 to v35 (claim 2) assert the exact theme colours in the Current
  mode; the real window gives the same (claim 4).

## 8. Requirements - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

- `just requirements-update` (`<S>/ver2-requirements-update.log`): exit 0, `0 indexes updated, 0
  requirement OKF projections updated`; `git status --porcelain` empty.
- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`
  (`<S>/ver2-okfreq-validate.log`): exit 0, `1228 requirements, 0 errors, 26 warnings`; no line names
  FMSCHEMA-023 or -084.
- Diff of the two SwRS and `tiers/log.md` read: 084 changes S1 and S6 and adds S8, S9, S10, a known
  issue and Method lines; 023 changes S5 and adds S10; log entry present. The texts match claims 3 to
  7; the named test files and titles exist.

## 9. `just preflight` - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

At `cd3b8e6`, 13:54:50Z to 14:02:17Z, exit 0, tree clean after (`<S>/ver2-preflight.log`):
`check-no-merge-commits: passed`; Node 56/56; unit tests 5375, 5367 pass, 0 fail, 8 skipped; Node
116/116; Python `296 passed` and `4 passed`; `1228 requirements, 0 errors, 26 warnings`;
`ci-static: passed` (Windows runs the static stage only).

## 10. CHANGELOG line - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6: identical head and base trees at `223a8c4` (claim 0b).*

`git diff abfa71e cd3b8e6 -- CHANGELOG.md`: one entry under `## Unreleased` (wrapped like its
neighbours), ending `(CR-513 field-error, PR #535)` as the guideline orders. "Name in red on a
red-tinted background and a wavy red underline", the warning sentence and the whole-table row hold
(claims 3, 4).

## 11. PR description - VERIFIED

*Judged at `cd3b8e6`; carried from cd3b8e6 for the unchanged parts of the body only: claim 13 judges the body posted now.*

Read at head `cd3b8e6` at 14:19:25Z: title `fix(frontmatter): mark the rows that carry a schema error
or warning`, draft, base CR-511's branch, posted body equal to `work/pr-body.md` (0 differences).
Read again after the move (`<S>/ver2-posted-body-final.md`): the only difference is a trailing blank
line. No STALE mark; no change request number or role name outside "Internal references"; no `issue:`
line in the intent, so no `Fixes`.

- Summary, Deliverables table and paragraph: base rows have no mark (claim 2, `<B>`); each row of the
  table and each sentence on modes, value colour and edit hover: claims 3 to 7.
- Changes: each bullet matches the diff (claim 0); "markup, validation, messages and badge are
  unchanged" (claim 6); palette variables "read only by the rows this change styles" (claim 3, `git
  grep`); the unit test and the four scenarios (claims 1, 2); `e2eGroups.test.ts` 523 to 527; two
  fixtures and one schema file.
- Impacts: 10 pictures, all fetched (HTTP 200, `image/png`) and opened, no username or path.
  `uv run --no-sync --group docs python -I <S>/ver2_posted_compare.py <F> <downloads>`
  (`<S>/ver2-posted-compare.log`): each has the sha256 of its file in `<F>/evidence/` and differs by
  no pixel from the top of this pass's capture, `RESULT: 0 picture(s) differ`. So "before at
  `abfa71e`, carried from `9d7e788`" and "after at `cd3b8e6`, carried from `7f7cc06`" hold. The
  sentences on the status colours of the two sets match the themes (`themes.ts` unchanged
  `9d7e788..abfa71e`; `STATUS_THEME_VARIABLES` at the head).
- Blast radius: in `<B>` checked out at `cd3b8e6`, `git revert --no-commit abfa71e..cd3b8e6`: exit
  0, no conflict, `git write-tree` = `ff7c89e5d9d346ee99a349f658deb1b4ea2cb684` = the base tree; then
  `git revert --quit`, nothing committed.
- Autonomous decisions: 1, the 1.9 to 1.97 figures of the `1fa9587` pass, requirements and tests
  (claims 1, 3, 8); 2, claim 5 and 084#S8; 3, claim 5 and 084#S9; 4, `work/conflicts.md` (conflicts
  only in `tiers/log.md` and the generated test file lists, entries kept, lists regenerated).
- Known gaps: 1 and 2, figures of claim 3; 3, search of `test/integration` for the new colours,
  underline and warning row: no match (the existing steps check classes only); 4 and 5, all 527
  visual pages loaded: marked rows only in `frontmatter-schema` v06, v07, v21, v32, v33 and
  `layout-width` v36 to v38, none asserting hover, underline during an edit or a forced mode over a
  theme; the warning row only in v34 and v35, on one line (30 px) at 900 px. No claim of this note is
  unverified or accepted as failed, and no pair the plan names is missing.
- Human decisions: match `02-answers.md` Q1 and Q3.
- Test plan: Requirements (claim 8), Changelog (claim 10), Local gates: preflight counts equal claim
  9 except Python, `254 passed` and 4 in `<S>/r5-preflight.log` (carried from `7f7cc06`: clean
  rebase, claim 0; `296` at `cd3b8e6` because the base added Python tests); visual group 35 (claim 2
  and `<S>/driver-capture-7f7cc06.log`). Evidence: Impacts above. Review "approved at `cd3b8e6`
  (carried from `7f7cc06`)": `$CHANTIER log CR-513`, 12:49:20Z and 12:49:36Z "r5 approved at
  7e70228..., committed as 7f7cc06fcfeba466ed7fa87a5d000e0c10c90496 (diff equals the reviewed
  state, tree clean ...)", then the clean rebases of 13:13:40Z and 13:33:04Z.
- "New or changed tests" (claims 1, 2: they fail on the base), "Verified" and "CI green" are
  unticked, left to the Driver.

## 12. CI at the head (read, not run) - VERIFIED

*Judged at `cd3b8e6`; kept as the record of that head. CI at `223a8c4` is read in claim 13.*

`gh pr checks 535` while the head was `cd3b8e6`: checks, report, static, static-windows,
viewer-graph, visual, visual-2 pass. `gh run view <id> --json headSha,conclusion,status` for
45829907654 and heavy run 45830014522 (again at 14:31:55Z): `cd3b8e6a`, completed, success; the
heavy run's jobs include acceptance (trust-security), integration and stress, all passed.

## 0b. The moved head - VERIFIED

At `223a8c4`, in `<W>` (`git rev-parse HEAD` = `223a8c49a47f8af786412e7cff748860b18d3782`,
`git status --porcelain` empty before and after this pass).

- `git range-diff abfa71e..cd3b8e6 e2b2235..223a8c4`: `49022ec6 = e34029be`, `e9c82c57 = e6c77338`,
  `cd3b8e6a = 223a8c49` (3 of 3 identical).
- `git rev-parse "cd3b8e6^{tree}" "223a8c4^{tree}"`: `e6f6894de333c24969709306715c4f3c06d06418` twice.
- `git rev-parse "abfa71e^{tree}" "e2b2235^{tree}"`: `ff7c89e5d9d346ee99a349f658deb1b4ea2cb684` twice.
- `git range-diff 928ebd7..7f7cc06 e2b2235..223a8c4`: `552cfac4 = e34029be`, `7e702282 = e6c77338`,
  `7f7cc06f = 223a8c49`; `git diff --stat 7f7cc06 223a8c4 -- src`: empty.
- `git ls-remote origin refs/heads/main refs/pull/535/head`: `e2b2235...`, `223a8c4...`.

## 13. PR description at `223a8c4` - VERIFIED

`gh pr view 535 --repo gsemet/markdown-okf-schema-studio --json
body,headRefOid,baseRefName,baseRefOid,isDraft,title,state` (`<S>/ver3/pr.json`, read again at
14:37Z, `<S>/ver3/pr-end.json`, body unchanged): head `223a8c4`, base `main` at `e2b2235`, draft,
open, title `fix(frontmatter): mark the rows that carry a schema error or warning`.

- Posted body against `work/pr-body.md`: `diff --strip-trailing-cr`, no difference.
- Against the body of claim 11 (`<S>/ver2-posted-body-final.md`): `diff` shows only the before and
  after captions, the Cream caption, the eight Test plan lines (SHAs, `carried from`, Python `296`,
  three boxes ticked) and a trailing blank line. Every other sentence is the one claim 11 judged,
  against a diff whose trees are unchanged (claim 0b). `git diff --stat e2b2235 223a8c4`: 19 files,
  +570/-11, as at `cd3b8e6`.
- Rendering: `gh api .../pulls/535 -H "Accept: application/vnd.github.html+json"`, then
  `python -I <S>/ver3_render_check.py body.html posted-body.md`: 10 headings in order, those of the
  project template and Internal references, plus Autonomous decisions, Known gaps and Human decisions;
  2 tables, 10 images, 8 task boxes all checked; no raw Markdown, no comment, no `STALE` or
  `UNVERIFIED` mark; no change request number, batch, round, order or role name before "Internal
  references"; no user name or home path. No details fold: the project template has none.
- Images: the 10 URLs of the body, fetched with `curl -sSL`: each HTTP 200, `image/png`; each
  `sha256sum` equals its file in `<F>/evidence/` in the slot its caption names (before/after, light/
  dark, Cream). All ten files opened: they show what their captions say; no user name, no path.
- Captions "before at `e2b2235`, carried from `9d7e788`" and "after at `223a8c4`, carried from
  `7f7cc06`": base tree and head tree equal those of claim 11's pixel comparison (claim 0b);
  `git diff --stat 9d7e788 e2b2235 -- src test/visual/themes.ts` shows nothing.
- New or changed tests "at `223a8c4`, carried from `cd3b8e6`, fail on the previous code": claims 1
  and 2.
- Requirements, Changelog: claims 8 and 10; `git diff e2b2235 223a8c4 -- CHANGELOG.md` shows the one
  entry under `## Unreleased` ending `PR #535)`.
- Local gates: `<S>/ver2-preflight.log` (my run at `cd3b8e6`): Node `tests 56`, `pass 56`; unit
  `tests 5375`, `pass 5367`, `fail 0`, `skipped 8`; Node `116`, `116`; `296 passed`; `4 passed`;
  `ci-static: passed`. `<S>/ver2-head-capture.log`: `"status": "passed", "scenario_count": 35`. The
  Python count `296` now matches this run.
- Evidence: the captions above.
- Review "approved at `223a8c4`, carried from `7f7cc06`": `$CHANTIER log CR-513` 12:49:20Z and
  12:49:36Z (round 5 approved, committed as `7f7cc06`); the three commits of `223a8c4` are identical
  to those of `7f7cc06` (claim 0b).
- "Verified at `223a8c4`, carried from `cd3b8e6`": the log's verdict of 14:33:24Z, `VERIFIED` at
  `cd3b8e6`; trees identical (claim 0b).
- "CI green at `223a8c4`": `gh pr checks 535` (14:36Z and 14:37Z): checks, report, static,
  static-windows, viewer-graph, visual, visual-2 pass, the rest skipped; `gh run view 45838047081`:
  head `223a8c4`, completed, success. `statusCheckRollup` holds no entry other than success or
  skipped.
- Blast radius: the head's diff against its base has the two trees above, so reverting it gives the
  base tree again (claim 11's revert check, same trees).
- Autonomous decisions, Known gaps, Human decisions: unchanged text (claim 11). Decision 4 matches
  `work/conflicts.md`; `02-answers.md` Q4 and its follow-up concern the PR's base, not the change.

Not judged, cited by no claim of the body: heavy run 45840378393 at `223a8c4`. At 14:37:26Z it was
`in_progress` (viewer-graph and acceptance (trust-security) success; static, static-windows, visual,
visual-2, stress, integration running).

## Observations

- The PR's pictures come from the visual harness, as the PR guideline allows; the real-window
  pictures of this pass stay in `<E>/window-cd3b8e6/`. No real-window run was made on the base.
- White mode warning contrast is 4.47, the lowest forced-mode figure of a marked row at rest.
- In the Current mode on Dark Modern the error background is the theme's dark red, not a light one;
  this follows section 1 of the specification and the body says the theme's colours apply there.

## Run notes

- Description pass at `223a8c4`: no command refused; nothing pushed, no PR edit. Downloads and
  the render check are in `<S>/ver3/`, its script `<S>/ver3_render_check.py`.

- No command was refused. Some shell calls used `cd` to `<W>`, a leading assignment, a chain or a
  redirect into `work/scratch`; no redirect wrote to a worktree file.
- Temporary base worktree and downloaded pictures were in the session scratchpad (the brief allows a
  system temp place); both are removed (`git worktree remove --force`, exit 0). The VS Code copy this
  walk downloaded to `<W>/.vscode-test` is removed (0 processes ran from it); `<W>/out/ver-walk` is
  absent. `<S>/walk2` is kept to reproduce the walk. Other worktrees were not touched.

VERIFIED
