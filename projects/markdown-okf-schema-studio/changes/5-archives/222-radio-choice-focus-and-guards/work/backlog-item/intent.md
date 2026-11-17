# Radio choice lists: keyboard focus and the write guards break at the edges

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-GFM-039, SwRS-MDOKFSTUDIO-BLOCK-041, SwRS-MDOKFSTUDIO-TRUST-005 · Area Radio choice lists · Side preview · QA215-02, QA215-03, QA215-04, QA215-05 · P2

> [!NOTE]
> The radio lists of #240 hold up under real use: no click ever changed more than two lines, and one undo
> step always restored the source. These four defects sit at the edges: keyboard entry, focus after a
> choice, the open-editor guard and read-only files. One section per finding; the fix CR does only the
> sections still ticked.

| # | Finding | Verdict | Replay (`scenarios/`) |
| --- | --- | --- | --- |
| 1 | Tab takes four stops to reach the first option | Bug (GFM-039) | `215-c1-1-radio-tab-entry-extra-stops.json` |
| 2 | A choice drops keyboard focus to the page body | Gap | `215-c2-1-radio-choice-drops-keyboard-focus.json` |
| 3 | A click with a block editor open writes when the option first scrolls into view | Bug (GFM-039, BLOCK-041) | `c7-1-radio-click-with-open-editor-writes.json` |
| 4 | On a read-only file a click shows the new choice, writes nothing, says nothing | Bug (GFM-039, TRUST-005) | `c7-2-readonly-radio-click-silent.json` |

Fixtures: `fixtures-visual/74-radio-plan.md` and `synth/radio-c1.md` (the second is promoted to the QA
skill's `assets/synth/` by the QA skill feedback CR).

## 1. Tab entry takes four stops (QA215-02)

| Currently | Expected |
| --- | --- |
| ![Tab stops on ul, li, p before the radio](evidence/tab-currently.jpg) | ![One Tab lands on the selected option](evidence/tab-expected.jpg) |
| From the label, Tab lands on `ul[role=radiogroup]`, then the `li`, then its `p`; only the fourth Tab reaches the radio. | One Tab lands on the selected option (GFM-039: one tab stop per group). |

**Why this is wrong.** A keyboard author tabbing through a plan expects one stop per group, then the
arrows. Here three stops do nothing (arrows, Space and Enter are ignored on `ul`, `li`, `p`), so the group
looks dead. GFM-039 says the selected option is the only `tabindex="0"`. Every preview block carries
`tabindex="0"`, and the group inherits it; the E2E focuses the option with `.focus()`, so it never walks
the Tab order.

- (x) Remove `tabindex` from the group's `ul`, `li` and label `p` so the roving option is the single stop
- ( ) Keep the stops and forward Arrow, Space and Enter from the `ul` to the selected option

**Test.** Real-input E2E in `test/integration/radioChoice.test.ts`: from the label press Tab once, assert
the focused element is `[role=radio]`. Uncheck to disagree: [x]

## 2. A choice drops keyboard focus (QA215-03)

No visual: the symptom is the focused element. After Tab to the selected option, ArrowDown and Space, the
file is written correctly but `document.activeElement` is `BODY`; the same after a click and after an
external rewrite. Expected: the chosen option keeps focus, as in a native radio group (WAI-ARIA radio
group pattern).

**Why this is wrong.** Changing a decision twice costs a walk of about seven Tabs from the top. The task
checkbox loses focus the same way, but the radio group is the first control meant to be used repeatedly
from the keyboard. Folds the "focus after write" row of P3 `radio-choice-followups`.

- (x) After the re-render, restore focus to the option with the same source line and column
- ( ) Update the DOM in place for a choice instead of re-rendering the list

**Requirement.** GFM-039: add "after a choice, focus stays on the chosen option" to the Space and Enter
row. **Test.** Real-input E2E: Tab, ArrowDown, Space, assert the diff and that focus is on the newly
selected radio. Uncheck to disagree: [x]

## 3. A click with a block editor open writes (QA215-04)

```text
Currently: edit mode, editor open on "## Tasks", wheel up, click the second option of "Fix direction".
           The editor closes, the source changes by two lines (-2 +2 at L9), no message. 4 of 4 times.
Expected:  the editor stays open, nothing is written, the editor status reads
           "Save or cancel this edit before choosing an option." (GFM-039)
```

**Why this is wrong.** An author mid-edit expects one edit at a time (BLOCK-041). A stray click both ends
the edit and records a choice they may not have meant. The guard exists: an option already in view is
refused correctly. It is bypassed when the click first scrolls or blurs the preview, so the editor's
blur-commit runs before the guard.

- (x) Evaluate the open-editor guard on `mousedown`, before the editor's blur-commit
- ( ) Treat a radio click as not blurring the open editor

**Test.** Real-input E2E: open a block editor, click an unselected option that needs a scroll to reach,
assert the diff is empty and the editor is still open. It earns a test: the defect writes to the buffer
silently. Uncheck to disagree: [x]

## 4. Read-only file: silent, wrong selection (QA215-05)

| Currently | Expected |
| --- | --- |
| ![Preview shows "Leave as is" selected, source unchanged](evidence/readonly-currently.jpg) | The first option stays selected (as in the source) and the reason shows next to the clicked option, or every control is disabled with a tooltip, as in Restricted Mode. |

**Why this is wrong.** With `files.readonlyInclude` on the file, the preview shows the new choice while
the buffer and disk are unchanged: the author believes the decision is recorded. No toast, note or
tooltip, and no `aria-disabled`. Restricted Mode, by contrast, disables all five controls with "Editing
requires a trusted workspace.". Both the read-only row and the refusal row of GFM-039 are broken.

**Direction.** Treat a read-only document like Restricted Mode (controls disabled up front, with the
reason), and on any failed apply restore the selection and show the refusal note.
Uncheck to disagree: [x]

**Test.** Integration: with `files.readonlyInclude` set, click an option, assert the selection returns
to the source's and a reason is visible. Uncheck to disagree: [x]

## Done when

- [ ] The four replay scenarios pass.
- [ ] One Tab from the label focuses the selected option; focus stays on the chosen option after a choice.
- [ ] A click with an editor open, or on a read-only file, writes nothing and says why.

Sources: [campaign 215 index](../../../215-qa-campaign-2026-10-31/work/00-index.md), sheets in
[01-radio-choice-lists](../../../215-qa-campaign-2026-10-31/work/01-radio-choice-lists).
