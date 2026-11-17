# Answers

## 2026-11-13: grill, questions to the owner

Q1. Rename this CR to what the probe found (`grid-after-tab-list-marker-line-offset`)?
Recommendation: yes; the "no card" case follows CommonMark.

Q2. The empty grid when the body is indented less than the item's content column: keep the
CommonMark reading with no extra signal (recommended), or add a hint in the writing skill
(`skills/writing-for-markdown-okf-schema-studio/`) that a tab after a list marker means a 4-column
body indentation?

## 2026-11-13: owner's answers

Owner, 2026-11-13: « Q1 oui, Q2 ok ».

- Q1: renamed to `grid-after-tab-list-marker-line-offset`; the CR fixes the line offset only.
- Q2: the CommonMark reading stays, with no hint in the writing skill. The empty grid with a
  2-space body is not a bug.
