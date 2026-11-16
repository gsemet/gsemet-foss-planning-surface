## Why

The Chief of Staff's report and the record used two sets of icons: a CR waiting for a slot was 🟠
in the report and 🟡 on the board, a ready CR 🔵 and 🟢, a merged CR ✅ and 🟢. The user read one
state in two colours.

## What changes

- `status.py`: `label()` draws the icon from the state, no longer from `severity`.

  | Icon | State |
  | --- | --- |
  | ⚪ | queued, nothing keeps `take` from starting it; dropped |
  | 🟠 | queued that `take` refuses (no free slot, spent budget, `waits`); blocked with the reason `waits: …` |
  | 🟡 | working |
  | 🔴 | blocked, any other reason |
  | 🔵 | ready |
  | ✅ | merged |

- `rails.py`: `slot_free()`, the rule `check_slot` applies, QA drivers included, shared with the
  label. `waits_all()` now lists a release's fixes not ended, so a queued release with a pending
  fix shows `waits for CR-x` and draws 🟠.
- `waits:`, a new word of `handback <cr> blocked`, for a CR that waits for a thing already on its
  way. `step()` knows it, the usage message names it, and the CR's `Next` line says what it waits
  for.
- `chief-of-staff.md`: the report copies each icon from `status`. `driver.md`: the hand-back
  `blocked waits: <what>`.
- `foreman.md`: one line that the specification does not list. Without it the Foreman relays a
  `blocked waits:` to the user as a question.
- `severity`, its values and `schema` do not change. `hooks/register.tsx` does not change.

## Decided on the way

- By the user's word: a queued CR that `take` refuses draws 🟠, a release behind other CRs and a
  queued CR on a spent budget included. The label `blocked Waits 1/3` stays.
- A queued release with a pending fix follows that rule as a general one: 🟠, `waits for CR-x`.
- A `blocked waits:` CR keeps `severity: red` while its icon is 🟠, and resumes only when the
  Foreman takes it back.
- Archived and trashed CRs keep the label they had when last written.

## Out of scope

The `state` values of the record, and the board's layout.

## Evidence

At `b7e3517`, against its base `6f79dd3`, the same probe in a throwaway repository, through the
CLI and the scenario's fake forge:

| State | Before | After | `take` says |
| --- | --- | --- | --- |
| Queued, free slot, no waits | 🟡 queued | ⚪ queued | (starts) |
| Queued, a working CR and an open QA order hold all slots | 🟡 queued | 🟠 queued | no free slot for CR-102: 2 of 2 held (CR-101 working, O-1 qa) |
| Queued, `order done` frees the slot | 🟡 queued | ⚪ queued | |
| Queued, the one slot held by a working CR | 🟡 queued | 🟠 queued | no free slot: 1 of 1 held |
| Queued with `waits` | 🟡 queued, waits for CR-102 queued | 🟠 queued, waits for CR-102 queued | waits for CR-102 queued |
| Queued, spent budget | 🟡 queued | 🟠 queued (Now: "Waiting for the budget.") | budget spent: $2.00 of $1.0 (exit 5) |
| Queued, budget raised | 🟡 queued | ⚪ queued | |
| Queued release behind other CRs | 🟡 queued, waits for CR-105 queued | 🟠 same | waits for CR-105 queued |
| Queued release, the user's word pending | 🟡 queued, waits for the user's confirmation | 🟠 same | needs the user's confirmation |
| Queued release with a pending fix | 🟡 queued (no waits shown) | 🟠 queued, waits for CR-108 queued, CR-109 queued | waits for CR-108, CR-109 |
| Release, fixes ended | 🟡 queued | ⚪ queued | |
| Working | 🟡 working Round 1/3 | 🟡 working Round 1/3 | |
| Blocked `waits: the stack driver` | 🔴 blocked Blocked 1/3 | 🟠 blocked Waits 1/3, `severity` red, `Next`: "Waits for the stack driver; the Foreman takes it back when that lands." | |
| Blocked `question:` | 🔴 blocked Question 1/3 | 🔴 blocked Question 1/3 | |
| Ready | 🟢 ready Notify 1/3 | 🔵 ready Notify 1/3 | |
| Merged | 🟢 merged | ✅ merged | |
| Dropped | ⚪ dropped | ⚪ dropped | |

For each, the label is one string in the batch's `STATUS.md` and `STATUS.json`, the index's
`STATUS.json` and the CR's own files; merged and dropped CRs are not in the index, which lists
active CRs. The board prints `label` from `STATUS.json`: its new test renders one label per icon
and finds each unchanged.

The icons are the real code points (U+26AA, U+1F7E0, U+1F7E1, U+1F534, U+1F535, U+2705): the
changed files are valid UTF-8 with no BOM, and a scan of the tracked files finds no mojibake.

Not shown: the board in a real pane. The tests do not draw one.

The proof is text, which `gh pr edit --attach` does not upload: the raw before and after stay in
the CR's `work/verifier/evidence/` (`before-base.txt`, `after-head.txt`), with `work/verifier/probe.py`.

## Checks

- Long gate `just scenario`, local on Windows at `b7e3517`: 312/312 on the GitHub forge and 312/312
  on the GitLab forge. Run again by the Verifier, with the same result.
- `just check`: 28 passed. `claude plugin test .`: 22 passed.
- CI at `b7e3517`: `just check` passes on Linux, macOS and Windows, `just scenario` on Linux, none
  skipped.
