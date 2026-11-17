# Choosing a radio option with Space or a click drops keyboard focus to the page

Severity Medium · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-GFM-039 specifies selection, arrows and Space, not where focus goes afterwards) · Area Radio choice lists · Side preview · c2-1 · Replay `scenarios/215-c2-1-radio-choice-drops-keyboard-focus.json`

## Currently / Expected

No visual possible: the symptom is the focused element, not a pixel.

| Currently | Expected |
| --- | --- |
| Tab to the selected option, ArrowDown, Space: the file is written, `document.activeElement` is `BODY`. Same after a mouse click and after an external rewrite of the file. | The chosen option keeps focus (the control is re-created with focus restored), as in any native radio group (source: WAI-ARIA radio group pattern). |

## Why this is wrong

A keyboard author who picks an option with Space loses their place: the next ArrowUp or Space goes nowhere
and the Tab order restarts at the top of the page, where about 7 Tab presses are needed to come back to
the group. Changing a decision twice costs the whole walk again. Native radio groups and the WAI-ARIA
pattern keep focus on the chosen option. The task checkbox behaves the same today (focus is on BODY after
a click), so the preview as a whole drops focus on re-render, but the radio group is the first control
meant to be used repeatedly with the keyboard.

## Steps to reproduce

1. Fixture `fixtures-visual/74-radio-plan.md`, side preview.
2. Click the heading, press Tab 7 times (focus reaches the selected option of "Fix direction").
3. ArrowDown, Space.
4. `document.activeElement` is BODY. Buffer diff is correct (two lines).

## Impact

Keyboard-only and screen-reader users cannot change a choice more than once without re-tabbing.

## Suggested direction

- (x) After the re-render, restore focus to the option with the same source line and column
- ( ) Update the DOM in place for a choice instead of re-rendering the list
- ( ) Leave as is and document it

## Test to add

Real-input E2E: Tab to a radio, ArrowDown, Space, assert the buffer diff and that the focused element is the radio now selected.

Uncheck to disagree: [x]

## Requirement to write or change

SwRS-MDOKFSTUDIO-GFM-039: add "after a choice, focus stays on the chosen option" to the Space and Enter row.

Uncheck to disagree: [x]

## Done when

- [ ] After Space or a click, the chosen option has focus.
- [ ] The replay scenario passes.
