# Tabbing into a radio group takes four stops before the first option

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-GFM-039 (one tab stop per group, selected option is the only tabindex 0) · Area Radio choice lists, keyboard · Side preview · 215-c1-1 · Replay `scenarios/215-c1-1-radio-tab-entry-extra-stops.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/215-c1-1-currently.jpg) | ![expected](../evidence/215-c1-1-expected.jpg) |
| The first Tab from the label lands on the list itself (`ul[role=radiogroup]`, tabindex 0); then the item `li`, then its `p`, and only the fourth Tab reaches the radio. | The first Tab from the label lands on the selected option, which takes arrows, Space and Enter (SwRS-MDOKFSTUDIO-GFM-039: the group is one tab stop). |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

A writer who tabs through a plan to answer its questions expects one stop per group, then the arrows. Here Tab reaches the group three times without any effect (arrows, Space and Enter do nothing on the `ul`, `li` or `p`), so a keyboard-only author thinks the group is dead or presses Space and sees nothing. SwRS-MDOKFSTUDIO-GFM-039 and its visual note say the selected option is the only element with tabindex 0 and that each group has one tab stop. The real-input E2E focuses the option with `.focus()`, so it never walks the Tab order. Every preview block carries `tabindex="0"` (all `p`, `ul`, `li`); the radio group inherits this.

## Steps to reproduce

1. Fixture `synth/radio-c1.md` (copied to the skill's `assets/synth/`), side preview.
2. Click the paragraph "Two items:" and press Tab four times, reading the focused element each time.
3. Observed: `UL radiogroup`, `LI none`, `P`, `SPAN radio`; Space on the first stop writes nothing.

## Impact

Keyboard-only authors cannot reach an option in one Tab and get no feedback on three stops. A 3-option group costs 4 stops, and the following Shift+Tab walks the same stops back.

## Where it comes from

Block-level `tabindex="0"` set on the group `ul`, its `li` (role none) and the label `p`; the roving tab stop only applies to the `span[role=radio]`. Look at `src/page/features/checkboxes.ts` and the code that adds `tabindex` to source blocks.

## Suggested direction

- (x) Remove tabindex from the radio `ul`/`li`/label `p` inside a group (or make the group container non-focusable) so the roving option is the single stop
- ( ) Leave the stops but forward Arrow/Space/Enter from the `ul` to the selected option
- ( ) Leave as is and document it

## Test to add

Real-input E2E: from the label paragraph press Tab once and assert the focused element is `[role=radio]` with `aria-checked`; extend `test/integration/radioChoice.test.ts` (today it only calls `.focus()`). The replay scenario already asserts this.

Uncheck to disagree: [x]

## Requirement to write or change

Amend SwRS-MDOKFSTUDIO-GFM-039: "When a writer presses Tab from the label of a radio group, the first focused element SHALL be the group's tab stop option." Uncheck to disagree: [x]

## Done when

- [ ] One Tab from the label focuses the selected option (else the first).
- [ ] The replay scenario passes.
