# CR-513 verification

Head: 1fa9587eb1f6a5e53ef5bce5269d292bc2517859

Base: `9d7e788a479dec70fd882d295bf0d5e78f4f6b98`. Verdict: **NOT VERIFIED**.

All claims are judged at `1fa9587` (the head; `git ls-remote origin` of the branch and `gh pr view 535`
give the same SHA, `git status --short` of the worktree is empty). `<W>` = CR worktree, `<B>` =
detached worktree of the base (head's test files copied over the base's source), `<S>` =
`work/scratch`, `<E>` = `work/verifier/evidence`. Raw logs: `<S>/ver-*.log`. `chantier.yaml` has no
long gate, so there is no gate pass to cite.

## Failed claims

| # | Claim | Verdict |
| --- | --- | --- |
| 5b, 6a | A marked field shows its name in red on a light red background in every preview mode | NOT VERIFIED |
| 10b | The CHANGELOG sentence "in red on a light red background" | NOT VERIFIED |
| 11 | The PR description | NOT VERIFIED |

## 1. Unit test: red on the base, green at the head - VERIFIED

- Base, `<B>`: compile, then the compiled `fieldIssueStyles.test.js` (`ver-before-unit.log`):
  `tests 5, pass 0, fail 5`.
- Head, `just preflight` (`ver-preflight.log` lines 1345-1349): the 5 tests of
  `fieldIssueStyles.test.ts` pass.
- The file asserts every item of section 3 of the specification (read at the head).

## 2. Visual scenarios v32 to v35 - VERIFIED

- `fnm exec -- npm.cmd run visual:render` then
  `uv run --no-sync --group docs python test/visual/capture.py --group frontmatter-schema`.
- `<B>`: exit 1, 31 passed, v32, v33, v34, v35 failed, 16 assertion failures (7, 7, 1, 1).
- `<W>`: exit 0, manifest revision 1fa9587, 35 of 35 passed, 0 failures, 28 screenshots.
- The assertion lists of section 4 are all present (`git diff 9d7e788 1fa9587` of
  `scenarioAssertions.ts`, `scenarioDefinitions2.ts`, `scenarioIds.ts`).

## 3. Before and after screenshots, light and dark - VERIFIED

- Field rows and whole-table warning row: `<E>/{before,after}-v3[2-5]-*.png`, each opened: plain
  rows before; coloured names, wavy underlines and coloured warning row after. No username, no path.
- Listed in `<E>/before-after.md`. These show the harness themes only (fallback colours).

## 4. Edit mode in a rendered page - VERIFIED

- `uv run --no-sync --group docs python <S>/ver_edit_probe.py <W> <B> <E>`: exit 0,
  `RESULT before: 16 failed check(s)`, `RESULT after: 0 failed check(s)`.
- After, light and dark: a hovered marked name cell takes the same background as a hovered unmarked
  edit cell and keeps its severity colour; the edited value cell has `text-decoration: none`, no
  descendant draws a line, and the underline is back after Escape.
- Same behaviour in the real window (claim 6): hover background of the page, colour kept, no
  underline on the open editor. Pictures `edit-hover-*`, `edit-open-*`, `real-window-edit-*`.

## 5. Host and default matrix

### 5a. Tokens unset and tokens set - VERIFIED

- Unset: unit test (claim 1) and, in the edit probe, computed fallbacks `rgb(241, 76, 76)`,
  `rgba(235, 80, 80, 0.12)`, `rgb(191, 136, 3)`, 14% mix of it, hover `rgba(128, 128, 128, 0.12)`.
- Set, light and dark: `uv run --no-sync --group docs python <S>/ver_token_probe.py <W> <E>`:
  `RESULT: 0 failed check(s)`; every colour follows the four variables set on the root.
- The specification says v32 to v35 are the "tokens set" cells. That premise is wrong: the same
  probe prints the four variables as `''` in those pages (the harness themes set none), so v32 to
  v35 prove the fallbacks only. The cells are proved here by injection and by the real window.

### 5b. "The look depends on [the tokens], not on a setting" - NOT VERIFIED

The look depends on the preview theme mode, whose default is Cream. See 6a.

- `grep` of `src/core`: `DEFAULT_PREVIEW_THEME_MODE ... = "cream"` (`previewTheme.ts:10`);
  `--studio-errorForeground:` is set by the forced palettes (`pageChromeStyles.ts` lines 29, 74,
  133); no forced palette sets `--studio-inputValidation-errorBackground` or
  `--studio-editorWarning-foreground`, so the VS Code theme's values apply inside them.

## 6. The specification's scenario, in a real VS Code window

Surface: VS Code 1.148.0 on Windows, Extension Development Host with its own user-data and extensions
folders, driven over CDP, bundle built at the head (`fnm exec -- npm.cmd run bundle`, exit 0); no
other test window was running. Command:
`fnm exec -- node <S>/ver_walk_run.js <W> <S>/walk <E>` (`ver-walk.log`): 116 checks ok, 16 failed.
All 16 failures are readability checks of my own (contrast of the name against what is painted behind
it at least 3, and a light background on a light page). The 3:1 threshold is mine, not the
specification's.

### 6a. Step 1, enum error "name in red on a light red background" - NOT VERIFIED

- VS Code "Default Dark Modern", preview as it opens (Cream): the name `status` is
  `rgb(179, 38, 30)` on `rgb(90, 29, 29)`: dark red on dark maroon on a cream page, contrast
  **1.97**; an unmarked name in the same table is 6.24. Not light, barely readable, and harder to
  read than the same name before the change. Pictures `real-window-step1-enum-error-dark.png`,
  `real-window-step2-workbench-dark.png`.
- Forced modes across hosts: White on a dark theme 1.95 (same maroon); Dark on a light theme 1.9
  (`rgb(244, 135, 113)` on pink `rgb(242, 222, 222)` on a dark page).
- Passing cells: Cream on a light theme 5.07, White on light 5.12, Dark on dark 5.25, Current on
  dark 3.85. Current on a light theme is 2.6 with VS Code's own two colours (observation, not
  counted against the change: the specification asks for those tokens).
- Cause (5b): the text comes from the preview palette, the background from the VS Code theme. This is
  against the intent of SwRS-MDOKFSTUDIO-THEME-025 ("every forced mode looks the same on a dark and
  on a light VS Code theme"; its normative list does not name the properties table). The code follows
  section 1 of the specification to the letter; the result misses field-error-Q1 and step 1 in these
  cells. The harness covers none of them. The older whole-document error row reads the same two
  tokens, so it likely shares the mix (inferred from the stylesheet, not measured).
- The rest of step 1 passes: wavy underline under `publshed` in the name's colour, value text keeps
  its colour, valid rows plain, badge 1 error.

### 6b. Step 2, undeclared field with the strict setting - VERIFIED

Setting off by default and `bonus_field` plain; once on, without a refresh, the warning colour on a
light background of it (in Cream) and the wavy underline; badge 1 error, 1 warning. Observation: the
warning name is faint in several cells (field row: light theme Cream 2.42, Current 2.7, White 2.7;
dark theme Cream 1.86, White 2.07, where the theme's `#cca700` lands on a light page). The first is
the specification's fallback colour family; the dark-theme cells are the same cause as 5b.

### 6c. Step 3, fix the value and remove the field - VERIFIED

Through the page (select `draft` then Enter; "Remove frontmatter field" button): the source is
updated, both marks go, no badge, no whole-table row. `real-window-step3-fixed-*.png`.

### 6d. Step 4, schema with a trailing comma - VERIFIED

One row "Schema could not be parsed: Expected double-quoted property name in JSON at position 118
(line 8 column 3)", warning colour on a 14% mix of it, as wide as the table, badge 1 warning.
Observation: contrast of the row text as in 6b (1.86 to 5.65 by theme and mode).

Not driven: nothing of steps 1 to 4. Real-window run on the base: not made (see `before-after.md`).

## 7. Requirements - VERIFIED

- `just requirements-update`: exit 0, `0 files updated`, `0 indexes updated`,
  `0 requirement OKF projections updated`; `git status --porcelain` empty.
- `uv run --no-sync --group requirements okfreq validate --check-links --project-root .`: exit 0,
  `1228 requirements, 0 errors, 26 warnings`; none names FMSCHEMA-023 or -084.
- FMSCHEMA-084 and -023 list `propertiesStyles.markers.ts` in `implemented_in_files`, and
  `fieldIssueStyles.test.ts` and `scenarioDefinitions2.ts` in `tested_in_files`; the text changes of
  section 2 and the log entry are in the diff (S8 and S9 are additions, named in the PR).

## 8. Gates - VERIFIED

`just preflight` at 1fa9587: exit 0, `ci-static: passed` (Windows runs the static stage only); unit
tests 5371, pass 5363, fail 0, skipped 8; other node runs 56/56 and 116/116; Python 254 and 4 passed;
`check-no-merge-commits: passed`; worktree clean before and after.

## 9. Scope of the source change - VERIFIED

`git diff --stat 9d7e788 1fa9587`: 14 files, +329/-8; under `src/` only
`propertiesStyles.ts` and its marker file, so markup, validation, messages and badge are unchanged.
360 px probe (`ver_wrap_probe.py`, `RESULT after: 0 failed check(s)`): the whole-table row wraps to 3
lines inside the table, coloured; at 900 px it fits on one line.

## 10. CHANGELOG

- 10a. One entry under `## Unreleased`, references in one group at the end,
  `(CR-513 field-error, PR #535)` (diff of `CHANGELOG.md`) - VERIFIED.
- 10b. Its statement "shows its name in red on a light red background" - NOT VERIFIED in the cells of
  6a, the default Cream mode on a dark VS Code theme among them.

## 11. PR description - NOT VERIFIED

Read with `gh pr view 535 --json body,isDraft,baseRefName,headRefOid,title`: same text as
`work/pr-body.md`, draft, head 1fa9587, base still CR-509's branch (known, left to the stack driver).
No image, so none to check. Markdown structure reads well; no role name as a doer; the only change
request reference is under "Internal references".

Failing:

- Impacts holds neither before/after evidence nor "No visual change" ("provisional, not yet
  attached"). `pull-request.guidelines.md`: "the Verifier fails a body whose Impacts has neither".
  The pictures now exist in `<E>`.
- Deliverables: "The colours come from the editor theme, with a fallback where the theme sets none."
  False in the forced modes, default Cream included: the error colour is the preview palette's
  (`#b3261e` in Cream) while the background is the editor theme's (5b).
- Deliverables table and Human decisions: "name in the error colour on a light red background" does
  not hold in the cells of 6a.
- `project.guidelines.md` ("During a change"): "The PR body's Tests section lists the requirement
  IDs added or changed with their source and test files." The Test plan names the two IDs without
  their files, and the body never names `test/visual/scenarioDefinitions2.ts` (small, same edit).

Verified in the body: Summary (base rows have no mark, claim 2); Changes (diff); edit-mode sentences
and "value text keeps its own colour" (claims 4, 6); "text wrapping" (claim 9); the three Autonomous
decisions (diff, claim 4, `work/conflicts.md`); the three Known gaps bullets (no repository test
drives a real window on this look; 900 px one line; no visual scenario covers hover or edit); Human
decisions match `02-answers.md` (Q1, Q3); "Requirements", "Changelog" (form) and "Local gates" boxes
(claims 7, 10a, 8, 2); "Review: approved at 1fa9587" (`$CHANTIER log CR-513`, 2026-11-26T10:16:28Z:
`move 0c9cab3..1fa9587 (conflict) inspector approved at 1fa9587eb1f6a...`). No STALE mark. "New or
changed tests", "Evidence", "Verified", "CI green" are unchecked "provisional" boxes.

When the body is next edited, Known gaps also needs a bullet for any failed claim that is accepted
rather than fixed.

## 12. CI (read, not run) - VERIFIED

`gh pr checks 535`: checks, report, static, static-windows, viewer-graph, visual pass (run
45799835412, attempt 2). `gh run list --commit 1fa9587...`: that run and heavy run 45799904002 both
`success`.

## Follow-ups and run notes

- The badge click jumps to field rows only (Coder's note, outside this change).
- The floating toolbar covers the top right of the table in several pictures, before and after.
- One of my shell calls changed folder into `work/scratch`, against the startup core; not repeated.
  Some calls used `cd` to a worktree, a leading assignment or a redirect into `work/scratch`; no
  redirect wrote to a worktree file. No command was refused.
- Cleanup: the base worktree, `<S>/walk`, `<W>/out/ver-walk` and the VS Code copy downloaded to
  `<W>/.vscode-test` are removed at the end of the run.
