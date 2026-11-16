# The report, the board and STATUS.md draw the same icons

## Problem

The Chief of Staff's report and the record use two sets of icons: a CR waiting for a slot is 🟠 in
the report and 🟡 on the board, a ready CR 🔵 and 🟢, a merged CR ✅ and 🟢. The user reads one state
in two colours.

## Change

The CLI draws the icon, and the report copies it. In
`skills/chantier/scripts/cli/src/chantier/status.py`, `label()` draws, from the state:

| Icon | State |
| --- | --- |
| ⚪ | queued with a free slot and nothing in `waits`; dropped |
| 🟠 | queued with no free slot, or with `waits`; blocked with the reason `waits: …` |
| 🟡 | working |
| 🔴 | blocked, any other reason |
| 🔵 | ready |
| ✅ | merged |

A slot is free by the rule `take` applies, QA drivers included.

`waits:` is a new word of `handback <cr> blocked`, for a CR that waits for a thing already on its
way: the stack driver, another CR. `step()` knows it, the usage message of `handback` names it, and
the CR's `Next` line says what it waits for, not the user's answer.

`severity` and its values do not change, so `schema` stays. `hooks/register.tsx` reads `label` and
needs no change; only its tests move if a fixture no longer matches.

In the cards:

- `chief-of-staff.md`: the report takes each icon from `status`, no longer from the Chief of Staff's
  judgement; the legend keeps its six icons, and ⚪ also covers a dropped CR. The line that says the
  report's icons are its own, and `STATUS.md` keeps its own, goes.
- `driver.md`: the hand-back `blocked waits: <what>`, and when to use it.

The README's status text follows if it names an icon that changed.

## Depends on

CR-134, for the legend and the 🟠 rule it adds to `chief-of-staff.md`.

## Out of scope

The `state` values of the record, and the board's layout.

## Done when

- A test or scenario check shows each row of the table in `STATUS.md` and `STATUS.json`, a queued CR
  both with and without a free slot.
- The same CR shows the same icon in `status`'s `STATUS.md` and on the board.
- The cards say all of the above.
- `claude plugin test .` and `just check` pass; the CLI changes, so `just scenario` passes too.
