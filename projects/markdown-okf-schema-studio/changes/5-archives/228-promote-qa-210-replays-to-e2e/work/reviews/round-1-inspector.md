# CR 228 — round 1 Inspector review

Worktree `markdown-okf-schema-studio-wt-228`, branch `change-requests/228-promote-qa-210-replays-to-e2e`,
base `e1005766`, uncommitted diff (11 files modified, 1 new: `test/integration/realInput/qa210Replays.ts`).
Read-only review. No real-window test was run.

## 1. Mapping honesty (COVERED claims)

Each COVERED claim was checked against the replay JSON in
`.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/`.

| Replay | Claimed test | Verdict |
| --- | --- | --- |
| c6-1 | `scenarioRefusedValueKeepsEditorUsable` part 1 (`frontmatterFields.ts:743-756`) | Honest. Priority 7, Enter, refusal, focus back in the INPUT (`:745`), Escape closes (`:748`), title opens as TEXTAREA (`:752`), buffer unchanged (`:753`). Same as all four replay checks. |
| ux-38 | same, part 2 (`frontmatterFields.ts:758-768`) | Honest. The replay clicks `reviewed_on`; the test clicks `title`. The journey and outcome are the same: another field opens while one is refused, and the buffer is unchanged. |
| c0-1 | `scenarioLinkClickEditsInEditMode` (`linkEditMode.ts:91-95`) | Honest. A plain click on the link of the link-only paragraph opens the editor; `assertStayedOn`. The buffer check after Escape is now also covered by the new `:126`. |
| c2-1 | `scenarioHiddenReviewMarks` (`blockKeys.ts:177-190`) | Honest. Toggle off, mark background `rgba(0, 0, 0, 0)`, `tabIndex -1`. a1ae30a6 landed REVIEW-152, so the intent's "wait for REVIEW-152" is met. |
| ux-03 | `scenarioUndoStaysInEditor(..., "open-with")` (`textEditing.ts:378-423`, `run.ts:194`) | Honest. Open-with, type, Cmd+Z, active element still TEXTAREA. |
| ux-12 | `scenarioTableMinimalDiff` (`blockKeys.ts:476-493`) | Honest. Cell edit + Enter, `lineDelta` exactly one line. |
| ux-25 | `scenarioPreviewKeepsMarkdown` (`editorWidgets.ts:618-640`) | Honest. A non-Markdown editor becomes active; the preview keeps the Markdown document and is not `missing-source`. |
| c5-1 | "covered by wide-table-tab with its fix" | Matches the brief (c0211344 is not on this branch). |
| c7-1 | BLOCKED | Matches the brief. |

No coverage is claimed wrongly.

## 2. New and extended scenarios

All of them use real input only: Playwright mouse and keyboard on the workbench frame. Fixture setup
goes through `createFixture`/`withDocument`. No page or host message is injected, and nothing writes
state directly.

- **c1-1 EXTEND** (`linkEditMode.ts:110-126`, fix 7be6b5dc). Header click, then title click; the
  textarea must hold `:::{grid-item-card} Linked card`; `assertStayedOn`; buffer back to `LINKS`.
  - Before 7be6b5dc the card was one stretched link, so a plain click navigated and `waitForEditor`
    times out.
  - Escape restoring an autosaved edit is current behaviour (`textEditing.ts:253-262`), so `:126` holds
    on HEAD.
- **c1-2 ADD** (`qa210Replays.ts:64-84`, fix 9e49ae07). Before the fix, Enter inserted a newline and
  the editor stayed open, so `waitForNoBlockEditor` (`:76`) fails. On HEAD, `edit.singleLine` Enter
  saves (`blockSourceEditor.ts`), and `lineDelta` is exactly the header line. The visual v35 asserts
  the same thing.
- **c3-1 ADD** (`:106-128`, fix 4777e249). `aside[data-okf-github-alert]` is real
  (`mystNormalize.ts:365`). Before the fix the lazy line was a separate paragraph after the alert, so
  `:114` fails.
- **c4-1 ADD** (`:148-181`, fix e1005766). Before the fix the planner skipped the whole list block, so
  the buffer never equals `expected` (`:176`). The selectors `data-find-input/count/toggle-replace/
  replace-input/replace-all` exist (`findBar.ts:470-490`). A reading-mode click only calls
  `revealRange`, which does not take the focus, and the focus wait at `:155` guards it.
- **c6-2 ADD** (`:226-268`, fix a123bf4e). Before the fix the warning set was the first 500
  alphabetical stems, so the `zz-` target warns and `:256` times out. On HEAD the `known` stems are
  merged (`frontmatterListEditor.ts`).
- **c6-3 ADD** (`:290-310`, fix 7394318e). Before the fix `Number.isFinite("3.5")` on the YAML string
  was false, so the value was refused and `:302` times out. `frontmatterValueEditor.ts:184-187` shows
  the HEAD path.
- **ux-16 ADD** (guard, `:355-373`). Same journey as the replay (blur by clicking the h1), with a
  trimmed `frontmatter-edge` fixture and a schema with `additionalProperties`.
- **ux-17 EXTEND** (`textEditing.ts:201-204`). `lineDelta` is one line, with no block scalar. It is
  deterministic after the existing `waitFor`.
- **ux-35 ADD** (guard, `:394-416`). The bare-LF check (`:410`) catches the 656727d9 regression
  (mixed endings) directly, and the alert selector depends on db98af6c.

Flake and cleanup:

- No fixed sleep was added. `closeOpenBlockEditor` is best effort, and `withDocument` cleanup closes
  everything anyway.
- Every fixture is disposed in `finally`.
- The 520 fillers are removed with their directory. The stem watcher invalidates on delete, and
  `resolveFilenameStem` rebuilds on a stale entry (`fileLinks.ts:244-250`). Later scenarios in
  `run.ts` do not depend on stem counts: list link completion runs before the replays.

## 3. Weakening

- No existing assertion is weakened or removed.
- No timeout is raised.
- No retry loop, no `force: true`, no skip.

## 4. Conventions

- Inline fixtures through `createFixture`/`withDocument` follow the repo convention. 7be6b5dc, 8afdd8a2
  and a1ae30a6 all use inline fixtures, which `createFixture` writes under `test/integration/fixtures/`
  at run time. That meets the intent's "fixture under the test fixtures".
- Inline `// @tests_req` markers match a1ae30a6 (`blockKeys.ts:139`). 7be6b5dc and 8afdd8a2 used
  `markers.ts` instead; both are accepted, and `check:markers` is ok.
- `run.ts` wiring follows the existing pattern: a sequence entry plus a `single` entry.
- No visual scenario was added, so `test/site/e2eGroups.test.ts` is rightly untouched.
- `check:limits` passed (917 files).

## 5. SwRS

- The 8 changed SwRS files each gain only one `tested_in_files` line.
- `req_lifecycle` values: 7 are `proposed`, TOOLBAR-012 is `draft`. None is approved.

## 6. Gates (run by the Inspector on the worktree)

| Gate | Result |
| --- | --- |
| `npm run check-types` | clean |
| `just check` | exit 0 |
| Unit tests | 3455/3455 |
| Untrusted manifest tests | 73/73 |
| pytest | 153 passed (warnings are tmp cleanup only) |
| `check:limits` | passed |
| `check:exports` | ok |
| `check:markers` | ok |
| okfreq lint and update-coverage `--check` | green |
| okfreq requirements | 1073 requirements, 0 errors, 21 warnings |

## Nits (not blocking)

1. **c6-2 fillers are redundant and costly** (`qa210Replays.ts:218, 231-233`). The repo alone already
   has about 1247 Markdown stems that sort before `zz-qa210-link-hint-target`, so the 500 cut happens
   without fillers. The 520 creates and 520 deletes each invalidate the stem index, which then
   re-walks the repo and `/tmp` (both are workspace roots, `run-tests.ts`). That adds time and timing
   noise in CI. Consider dropping the fillers or cutting them to a few, and saying in the comment
   that the workspace's own stems beat the cut.
2. **ux-35 stale check is weaker than the replay** (`:411-413`). The replay checks for "stale" while
   the editor is still open after autosave (before the commit click). The test checks after the
   commit, when the editor and its status line are gone. Move the check before the "Last paragraph"
   click, after an autosave wait on " Edited.". The CRLF assertion already guards the bug, so this is
   a nit.
3. **The replay mapping is not recorded in the repo.** The intent wants the next campaign to skip
   these journeys, and the request asks to "record which bug still blocks" c5-1 and c7-1. Add a short
   mapping to the `qa210Replays.ts` header comment, or make sure the PR body carries it. It should
   list each COVERED replay with its existing scenario, and c5-1/c7-1 as blocked.
4. **c6-2 does not use `withDocument`** (`:234-267`). Its hand-written try/finally loses the
   `withFocusDumpOnFailure` dump that `withDocument` gives. `scenarioListEditorClickAndKeys` has the
   same pattern, so this is optional.
5. **The 10 min real-input step budget** (`test/shared/hangWatchdog.ts:40`) now absorbs about 44 s
   more. That is worth watching on the CI run.

VERDICT: APPROVE-WITH-NITS
Must-fix: none.
