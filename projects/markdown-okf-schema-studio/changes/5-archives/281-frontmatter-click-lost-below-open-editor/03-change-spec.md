---
title: Change spec - click on a properties field below an open field editor is lost
cr: 281
slug: frontmatter-click-lost-below-open-editor
source: QA campaign 271, QA271-07 (Medium, Gap), priority P2
issue: none
date: 2026-11-10
base: origin/main a12a16bc
---

# Change spec: click on a properties field below an open field editor is lost

Read from `origin/main` (a12a16bc). Rules: `.agents/constitution.md`, `AGENTS.md`,
`requirements/guidelines/` (project guidelines, "During a change").

## Problem

In edit mode, with a field editor open and its value unchanged (for example `title`), one click on
the value cell of a field **below** it (`notes`, `summary`, `priority`) opens nothing and changes
nothing; a second click is needed. A click on a field **above** the open editor works. Replay:
`synth/frontmatter-edge.md`, title -> notes (sheet
`4-archives/271-qa-campaign-tables-2026-11-10/05-frontmatter-table/c4-1-click-field-below-open-editor-is-lost.md`).

## Root cause (hypothesis, strong)

A click is mousedown + mouseup; the browser fires `click` on the nearest common ancestor of the two
targets. The sequence on `origin/main`:

1. mousedown on the `notes` value cell. Its default action moves the focus to the cell
   (`tabindex="0"`, set by `setFrontmatterEditCells`), so the open control blurs.
2. Blur handler in `openFrontmatterValueEditor`
   (`src/page/features/frontmatterValueEditor.ts`, `control.addEventListener("blur", ...)`, about
   line 280; the list editor's `focusout` at about line 268) calls `saveValue()`. The value is
   unchanged, so `saveValue` takes the `unchanged` branch (about line 199) and calls
   `rt.frontmatter.closeFrontmatterEditor("save of an unchanged value")`
   (`src/page/features/frontmatterEditor.ts`, `closeFrontmatterEditor`): the editor is removed and
   the display shown again. The title row shrinks from about 108 px to 31 px, so every row below
   moves up about 77 px. (The key editor does the same: `saveKey` "key unchanged".)
3. mouseup lands at the same screen point, now on another row (or below the table). The `click`
   target is the common ancestor (the `tbody` or higher), not a `[data-okf-edit-cell]`.
4. The properties click handler in `installPageInput` (`src/page/features/pageInput.ts`, the
   `document.addEventListener("click", ...)` marked FMEDIT-001/FMEDIT-019, about lines 189-212)
   resolves `event.target.closest("[data-okf-edit-cell]")` to nothing and returns. The click is lost.

Why above works: rows above the open editor do not move. Why the refused-value case works
(CR 218): the blur handler returns early on `holdsRefusedText()`, so the editor stays open during
the press, nothing moves, and the click handler's `closeRefusedEditorFor(cell)` closes it and opens
the clicked field in the click. (The QA sheet's "opens on mouse down as the refused path does" is
inaccurate: the refused path also opens on click.) Changed-value case: the blur posts a save, the
editor stays open (saving) until the host answers, nothing moves during the press, and the click
opens nothing by design (FMEDIT-019 refusal table, "a click on another field then saves it and
opens no other editor in that click"). That stays as it is.

The implementer confirms step 3 first with the replay or the real-input test (editor trace: a
"frontmatter control blur" then "frontmatter editor closed ... save of an unchanged value", and no
"frontmatter editor opened" for notes).

## Fix (direction)

The press decides the field, not the release. In `src/page/features/pageInput.ts`:

1. A document `mousedown` listener (capture phase, never `preventDefault`, so focus, selection and
   the other mousedown listeners behave as today) that, in edit mode, for a primary-button press
   without modifier on a `[data-okf-edit-cell]` of an editable row that is not inside
   `[data-okf-frontmatter-editor]`, while `state.activeFrontmatterEdit` exists and its `valueCell`
   is not that cell, remembers the press: the cell, its row's `data-okf-field` and the cell kind
   (`data-okf-edit-cell`). Any other mousedown clears it.
2. In the properties click handler, when `closest("[data-okf-edit-cell]")` finds nothing, fall back
   to the remembered press when the click completes it: the click target contains the pressed cell
   (the common-ancestor rule). If the pressed cell was disconnected (the close applied deferred
   properties markup through `applyPropertiesMarkup`), re-resolve it by field name and cell kind in
   the current `[data-okf-properties]` and require the click target to contain that section or lie
   inside it. The remembered press is cleared on every click.
3. The fallback then runs the existing path unchanged (`closeRefusedEditorFor`, key editor,
   checkbox `toggleBoolean`, value editor). `openFrontmatterValueEditor` and
   `openFrontmatterKeyEditor` already return when an editor is still open, which keeps the
   changed-value case ("saves, opens nothing") as specified.

Rejected: opening the field on mousedown (the mousedown default then moves the focus to the cell
and blurs the new control; text selection by drag breaks); keeping the editor row at the closed
height (the editor holds a textarea, the status line and the field menu). A small helper (for
example `pressedFieldCell(event)`) keeps the handler readable; `pageInput.ts` is 299 lines, far
from the 800-line limit.

Keyboard (Enter or Space on a cell) is not affected: no layout shift happens between key events.

## Requirements (okfreq)

| ID | Change | Status |
| --- | --- | --- |
| SwRS-MDOKFSTUDIO-FMEDIT-019 | Amend: new scenario, verification notes, criteria | `req_lifecycle: proposed`, `status: stable`: no owner approval needed (not `approved`) |

No new SwRS: the behaviour belongs to FMEDIT-019 ("A field editor saves a changed value ...";
it already holds the unchanged-value close and the refused-value click). Amendment:

- New scenario, `### Scenario (nominal): A click on another field opens it after an unchanged
  editor closes`:
  - GIVEN a field editor (value or key) whose value is unchanged, above other fields of the
    properties table
  - WHEN the writer clicks the value or key cell of another field, and closing the editor on the
    press moves that cell before the button is released
  - THEN the editor closes without a post and the clicked field's editor opens in the same click;
    a click on a field above the editor does the same
- Refusal table row (existing scenario, changed-value row stays as is); add one row to make the
  limit explicit: "A press on a field cell released outside it without an editor open: nothing
  opens".
- Verification notes: add the new unit tests (test/page/runtimeFrontmatterEditor.test.ts) and the
  real-input part (test/integration/realInput/frontmatterFields.ts,
  scenarioRefusedValueKeepsEditorUsable, part 3). Criteria: "the properties click handler resolves
  a click whose target contains the cell pressed while an editor was open to that cell".
- `implemented_in_files` and `tested_in_files` already list `pageInput.ts`,
  `runtimeFrontmatterEditor.test.ts` and `realInput/markers.ts`; `just requirements-update`
  refreshes them. Markers: `@implements_req SwRS-MDOKFSTUDIO-FMEDIT-019` on the new mousedown
  listener and the fallback; `@tests_req SwRS-MDOKFSTUDIO-FMEDIT-019` on each new unit test
  (the real-input scenario is already marked in `markers.ts`).
- Dated entry in `requirements/tiers/log.md` (2026-11-10, QA271-07, CR 281).

## Tests first (each fails on origin/main)

Unit, `test/page/runtimeFrontmatterEditor.test.ts` (fake DOM harness, `trackFocus` and
`blurOnFocusChange`; 1280 lines, limit 1500). Build a title row and a priority row under the same
parent (as `refusedNumberEditor` does); open title by a click; then:

1. "a click on a field below an unchanged editor opens it when the close moved the field":
   dispatch document `mousedown` on the priority cell, focus the priority cell (the blur closes the
   unchanged title editor, no post), dispatch document `click` with the rows' common parent as
   target: the priority editor is open (`aria-label="Frontmatter priority"` created, its display
   hidden), no `previewFrontmatterSave` posted.
2. Same with a changed title value: one save posted, no priority editor opened (FMEDIT-019 as
   today).
3. A click on the common parent without a prior press on a cell opens nothing; a press on the
   priority cell followed by a click whose target does not contain it opens nothing.
4. Key cell: press on another row's name cell, then the click on the parent opens the key editor.

The harness dispatches capture listeners in registration order unless `captureOrder` is set; set
it if the order with the other mousedown listeners matters.

Real input, `test/integration/realInput/frontmatterFields.ts`, extend
`scenarioRefusedValueKeepsEditorUsable` (RI-T44) with a part 3 (as the sheet asks; no `run.ts`
change): with `REFUSED_DOCUMENT` (title above priority), click the title value cell (editor open,
unchanged), record the priority cell's bounding box, click the priority value cell once with the
real mouse; assert the title row grew (the priority cell top had moved down by more than 20 px, so
the test really exercises the shift), the focused control is `INPUT Frontmatter priority`, no
title editor is left, and the buffer equals `REFUSED_DOCUMENT`. Then Escape, and the reverse
(priority -> title) still opens title in one click. Update the scenario's doc comment (QA271-07,
CR 281).

Replay promoted: `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c4-1-click-field-below-open-editor-is-lost.json`
from local branch `qa/271-table-campaign-replays` (87307e8f), taken alone
(`git checkout 87307e8f -- <that path>`); its fixture `assets/synth/frontmatter-edge.md` is already
on `origin/main`. It must pass (both checks: notes opens; title above still opens; buffer
unchanged; no errors) after the fix. Note: the earlier 271 promotion (81b019ae, 271-c2-1) added
only the real-input test, not the JSON; this CR adds the JSON as the owner's answers ask.

## Files expected to change

- `src/page/features/pageInput.ts` (mousedown listener, click fallback)
- `test/page/runtimeFrontmatterEditor.test.ts` (unit tests)
- `test/integration/realInput/frontmatterFields.ts` (RI-T44 part 3)
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c4-1-click-field-below-open-editor-is-lost.json` (new, promoted replay)
- `requirements/tiers/swrs/frontmatter-editing/SwRS-MDOKFSTUDIO-FMEDIT-019.md`
- `requirements/tiers/log.md`
- Generated by `just requirements-update` (links/coverage/index files it rewrites, for example
  `requirements/tiers/swrs/frontmatter-editing/index.md`)
- `CHANGELOG.md` (one user-facing Fixed line, as 81b019ae did)

Not expected: `frontmatterValueEditor.ts`, `frontmatterEditor.ts`, `pageRuntime.ts` (the press
stays local to `installPageInput`), `test/integration/realInput/run.ts`, the writing skill (no
rendered syntax changes), visual scenarios.

## Stack ordering (277-282)

This CR touches no table code (`tableCellEditor.ts`, `blockEditor.ts`, `src/core` table tools) and
no shared runtime type. Its only overlaps with the five table CRs are the shared append-only files:
`requirements/tiers/log.md`, `CHANGELOG.md` and the generated requirements files, plus
`test/integration/realInput/frontmatterFields.ts` only if another CR also edits it (none of the
table CRs should). It can sit anywhere in the stack; putting it on top keeps its rebase to those
appends.

## Blast radius

- Every click in the properties table in edit mode goes through the changed handler. The fallback
  only acts when `closest("[data-okf-edit-cell]")` is empty and a remembered press is completed by
  this click, so direct clicks on cells, links in values (`bindEditModeCaptureClicks` runs first),
  the field menu, the description toggle and the frontmatter collapse toggle are unchanged.
- The new mousedown listener coexists with the other document mousedown listeners
  (`checkboxes.ts` guardPress capture, `blockSelectionView.ts` Shift+mousedown,
  `commentCompose.ts`, `tableCellEditor.ts` pointerdown): it never prevents a default nor stops
  propagation.
- Drag risk: a press on a field cell dragged off and released elsewhere inside the table while an
  editor was open would open the pressed field; acceptable (the writer pressed that field) and
  bounded to the press-with-editor-open case.
- No host, protocol or rendering change; reading mode untouched (`state.editMode` gate).

## Gates

- `just check` (TypeScript, boundaries, file size, unused exports, unit, contract, requirements).
- `just requirements-update`, then `okfreq validate --check-links --project-root .` as CI runs it.
- Headless visual of the group: `npm run visual:render` then
  `uv run --no-sync --group docs python test/visual/capture.py --group frontmatter-editing`
  (no visual change expected; it guards the properties table).
- Replay `271-c4-1` passes against the built extension.
- Heavy CI on the branch (real VS Code, runs the real-input suite):
  `gh workflow run ci.yml --ref <branch> -f heavy=true`; then `just preflight` per the completion
  gate.

## Open questions

None.
