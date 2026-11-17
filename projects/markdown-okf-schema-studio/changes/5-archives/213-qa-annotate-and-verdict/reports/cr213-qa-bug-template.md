# QA bug template

One template for every QA bug. The same text is the campaign sheet and, after triage, the backlog
item's `01-intent.md`: the coordinator copies it as is and appends the priority to the line under the
title ("· P2"). There is no front matter and no second format. Write it with `skills/writing-for-markdown-okf-schema-studio/SKILL.md`, kept modest:
one alert at most, tables, the Currently / Expected images.

:::{tip}
A campaign hunts for bad behaviours that no test and no requirement covers yet. A **Gap** is the main
target, not a weaker bug. Search `requirements/` only to tell a Gap from a **Decision**.
:::

## Full form (High and Medium)

````markdown
# Tab through a wide table leaves the cell editor outside the visible preview

Severity Medium · Reproduced · Verdict Gap · Requirements: none found · Area Tables · Side preview ·
QA210-06 · Replay `scenarios/c5-1-wide-table-tab-editor-offscreen.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](evidence/currently.jpg) | ![expected](evidence/expected.jpg) |
| After 9 Tabs the editor sits at x=1859 in a 393 px pane. | The table scrolls so the edited cell stays in view (source: spreadsheet convention, and the first column already works). |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

3 to 6 lines. What the author was trying to do and what the behaviour costs them (lost work, wrong
result, lost context, extra steps, confusion). Which expectation it breaks and where that expectation
comes from: a requirement, an invariant, an in-product case that works, a named convention (VS Code,
Obsidian, spreadsheet) or plain user logic. Why a reasonable author would not accept it. A reader who
does not know the code must be able to agree or disagree from this section alone.

## Steps to reproduce

1. Fixture `synth/<file>.md` (its text below if it is not in `assets/synth/`).
2. Exact actions and keys, one per step.

## Impact

Consequence for the author, in one or two lines.

## Where it comes from

`src/…/file.ts` around line N, at the tested commit. Code reading comes after the observation.

## Suggested direction

A direction, not a patch.

## Test to add

The unit or real-input E2E assertion that would have caught it. For a **Gap**, also the SwRS to write
(title and one EARS sentence).

## Done when

- [ ] An observable acceptance criterion.
- [ ] The replay scenario passes.
````

## Short form (Low)

Keeps the title, the line under it, Currently / Expected and Why this is wrong. Steps, impact, origin,
direction, test and done-when fold into three lines:

```markdown
**Steps.** Fixture and exact keys, in one or two lines.
**Fix.** Direction, with a file and line pointer if known.
**Test / done when.** The assertion to add; for a Gap, the SwRS to write.
```

## Verdict

| Verdict | When | At triage |
| --- | --- | --- |
| **Bug** | A requirement is violated, or an objective invariant breaks (buffer diff beyond the edited lines, data loss, error, element off-viewport, focus stuck), or the product contradicts itself (the same input works elsewhere). | Backlog item, carrying the requirement ID. |
| **Gap** | No requirement and no test covers this. | Backlog item; the fix CR writes the SwRS and the test. |
| **Decision** | A requirement explicitly specifies the observed behaviour, but it looks wrong. | Never a bug: listed under "Decisions for the owner" in the index. |

## Currently / Expected

- **Currently**: a clipped JPEG of the symptom (`q shot --clip`), mandatory whenever it is visible.
- **Expected**, by what exists: a shot of the working case; else the Currently shot annotated (outline or
  arrow plus a one-line note); for a buffer defect, today's diff and the expected diff as code blocks.
  The caption names the source of the expectation.
- No visual possible (focus, timing): one line saying why, plus the measurements.
- At most two images per finding, about 1000 px wide, in `evidence/` next to the sheet.

## The line under the title

One plain line, in this order: `Severity <High|Medium|Low> · <Reproduced|Observed once|Code review> ·
Verdict <Bug|Gap|Decision> · Requirements: <IDs or none found> · Area <area> · <Side preview|Open With
editor|Both> · <finding ID> · Replay scenarios/<file>.json`. At triage the coordinator appends `· P1`,
`· P2` or `· P3`.
