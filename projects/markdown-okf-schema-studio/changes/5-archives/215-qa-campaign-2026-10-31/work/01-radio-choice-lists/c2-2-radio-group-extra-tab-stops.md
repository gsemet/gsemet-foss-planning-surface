# A radio group costs six Tab stops before its option, against the "one tab stop" rule

Severity Low · Reproduced · Verdict Gap · Requirements: none found for page-wide tab stops (SwRS-MDOKFSTUDIO-GFM-039 says the selected option is the only radio with tabindex 0) · Area Radio choice lists · Side preview · c2-2 · Replay `scenarios/215-c2-1-radio-choice-drops-keyboard-focus.json` (last check)

## Currently / Expected

No visual possible: tab order. Measured: Tab from the heading visits `BUTTON, P, P, UL[radiogroup], LI, P, LI, P, SPAN[radio]`. The `UL` has tabindex 0 and arrows do nothing on it; every `LI` and `P` also has tabindex 0 (the same on plain lists and tasks). Expected: Tab reaches the radiogroup's selected option once (ARIA radio pattern: the group is one tab stop).

## Why this is wrong

The requirement and the ARIA pattern promise one tab stop per group, but the generic block tab stops make a
three-option group cost about seven presses, and the group element itself takes focus without any
function. Low: the page-wide tabindex is shared with every block, so it is an intent question.

**Steps.** `fixtures-visual/74-radio-plan.md`, side preview, click the heading, press Tab repeatedly and read `document.activeElement`.
**Fix.** Do not give the `UL role=radiogroup` or its `LI`/`P` children a tab stop. Uncheck to disagree: [x]
**Test.** No test: shares the replay of c2-1 (last check). Uncheck to disagree: [x]
**Requirement.** SwRS-GFM-039: say "the group is reached by one Tab". Uncheck to disagree: [x]
