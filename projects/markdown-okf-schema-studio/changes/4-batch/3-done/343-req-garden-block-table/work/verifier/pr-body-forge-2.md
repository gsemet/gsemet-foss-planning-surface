## Summary

The block-editing and table-editing requirements had accumulated duplicates, SwRS that mixed several behaviours, stale parents, and implementation and test markers stacked on a few hub functions and one list in a shared test file. A reviewer could not read a use case in its StRS and find the code and the tests that check it. This PR gardens those two scopes: duplicate behaviours are merged (superseded, never deleted), markers sit on the code and tests that do the behaviour, the in-force StRS that may change get a use-case diagram and a validation scenario, and a few untested scenarios get tests. No product behaviour changes.

Four approved StRS get the corrections the owner agreed in advance, one commit each, for the owner's review on this PR: BLOCK-025 (stale CRLF known issue removed, diagram), BLOCK-003 and TABLE-001 (rationale trimmed to what a writer sees, diagram), TABLE-012 (superseded by two StRS: formatting a cell, inserting a table from the palette). Shared rules BLOCK-041, BLOCK-058 and BLOCK-109 keep one parent; the other StRS that rely on them cite them with `depends_on`, Main paths included.

## Approved requirements changed

Owner review requested. Each corrected approved StRS is its own commit; `approved_by` is the owner, `approved_at` is the time of this change. The commits to review:

- `docs: re-approve the exact-edit stakeholder need without its known issue` (BLOCK-025)
- `docs: re-approve the framed block editor need with a trimmed rationale` (BLOCK-003)
- `docs: re-approve the table cell editing need with a trimmed rationale` (TABLE-001)
- `docs: split the table formatting and insertion need in two` (TABLE-012)
- `docs: list the shared block-editing rules in depends_on instead of deriving them` (the shared rules, REVIEW-015's one line)

The requirements:

- StRS-MDOKFSTUDIO-BLOCK-025: "Known issue" on a second CRLF save removed (fixed by BLOCK-234), `depends_on` BLOCK-041, use case diagram.
- StRS-MDOKFSTUDIO-BLOCK-003: rationale trimmed (two pointers to other scopes dropped), use case diagram.
- StRS-MDOKFSTUDIO-TABLE-001: rationale cut to the constraints a writer sees, use case diagram.
- StRS-MDOKFSTUDIO-TABLE-012: superseded by two new proposed StRS, each with Main paths, a diagram and a validation scenario.
- StRS-MDOKFSTUDIO-REVIEW-015 (other scope): one-line `depends_on` added for a shared rule, as the owner answered, no authored text changed.
- Generated Links changed on approved StRS (children added or removed): listed in `requirements/tiers/log.md`, entry "Garden block-editing and table-editing" (the owner answered that this needs no re-approval).

## Deliverables

Requirements in the two scopes, before and after:

| | Before | After |
|---|---|---|
| Duplicate SwRS merged by `okfreq supersede` | none | BLOCK-236 to 245 into one validator SwRS, TABLE-070/073/074/076/080 into one conversion SwRS, TABLE-003/004/005 into TABLE-055, BLOCK-029 into 033, BLOCK-002 into 014, BLOCK-129 into 109, TABLE-102 into 094, BLOCK-258 into two, TABLE-035 into four, TABLE-118 into BLOCK-255 |
| StRS TABLE-011 | two needs in one | superseded by two StRS: table conversion, minimal diff |
| StRS TABLE-012 (approved) | two needs in one | superseded by two StRS: cell formatting, table insertion from the palette |
| CSS marker stacks (`editModeStyles.ts`, `contentBlockStyles.ts`) | one header per file | one marker per named CSS constant, produced CSS byte-identical |
| Hub-function marker stacks | `openBlockEditor`, `closeBlockEdit`, `openMappedEditor`, `receiveBlockEditSource`, `renderTableCellEditor` | one marker per branch that does the behaviour |
| Use-case diagrams | none | every in-force StRS of the two scopes, the four approved ones and the new StRS included |

The full old-to-new mapping is in `requirements/tiers/log.md`, entry "Garden block-editing and table-editing".

## Blast radius

Requirements text, markers, CSS constants split without changing the produced CSS, and tests. No runtime change. Revert with a plain `git revert`.

Grade: 1

## Autonomous decisions

- SwRS BLOCK-261 is titled "commits on Enter and ignores Tab": the code swallows Tab in a one-line editor, and the specification's "leaves on Tab" does not match it.
- BLOCK-109 is treated as a shared rule with one parent (StRS BLOCK-014); FMEDIT-008 cites it with `depends_on`.
- Where an audit "untested" scenario was already covered by an existing test (BLOCK-174, 053, 079, 140, 166, TABLE-106), no test was added.

## Known gaps

- Owner question: should a reopened preview start in the edit mode last chosen? The text of StRS-MDOKFSTUDIO-BLOCK-001 (description, user need, Path 2, "remembered per workspace") says yes, while SwRS-MDOKFSTUDIO-LIFE-170 and LIFE-172 and the code start every new preview panel in preview mode. This PR keeps the product's behaviour: the StRS text is left as is, its diagram and the real-window reopen step follow the code, and the question is logged in `requirements/tiers/log.md`.
- The long gate ran on Windows, where `just preflight` runs the static stage only; the real VS Code jobs (integration, stress), with the new real-window steps (BLOCK-001 hover, click and reopen; BLOCK-016 Ctrl+C; inserting a 3x2 table from the slash menu), ran only in CI's heavy run on Linux, green at d99d2ef.
- TABLE-124 "final save cannot be posted" has no test: the harness cannot reach it.
- The TABLE-012 split reparents PALETTE-031 (palette scope) to its successor StRS, so this PR touches one SwRS of another scope.
- SwRS BLOCK-261 keeps the code's behaviour (Tab is ignored in a one-line editor) where the specification said Tab leaves it; the owner decides which is wanted.
- BLOCK-109 is treated as a shared rule with one parent (StRS BLOCK-014), cited by FMEDIT-008 through `depends_on`; the owner confirms it.

<details>
<summary>Details</summary>

## Changes

- `requirements/`: supersessions, new SwRS and StRS, rewordings (TABLE-013, BLOCK-191, BLOCK-102/253, BLOCK-069), parent changes, generated coverage and Links, log entry.
- `src/`: markers only (CSS constants in `editModeStyles.ts` and `contentBlockStyles.ts`, branch markers in the block and table editors).
- `docs/VISION.md`: the Tables row names the two StRS that supersede TABLE-012 (TABLE-015 and TABLE-016).
- `test/`: markers moved onto the scenarios that check them (`realInput/markers.ts` shrunk, the marker-gate baseline shrunk), new tests for BLOCK-259, BLOCK-058, TABLE-018, TABLE-122, TABLE-094, and two real-window steps; a new `runtimeTableCellBlur.test.ts`; a new real-window scenario file `realInput/tableInsertSlash.ts` (inserting a 3x2 table with column alignment from the slash menu). The edit-mode no-reflow real-window scenario now measures only visible paragraphs in its click check: the paragraph being edited is hidden, its height read 0 and stopped the scenario before preview editing. Its reopen step checks that a new preview panel starts in preview mode (SwRS LIFE-172).

## Impacts

No visual change: requirement text, markers and tests only, and the CSS split into named constants produces byte-identical CSS.

## Test plan

- [x] New or changed tests: new unit tests pass; marker moves have no behaviour change; the new real-window steps pass in the heavy CI run at d99d2ef
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: No user-facing change
- [x] Local gates at d99d2ef: `just requirements-lint` pass (main paths: 81 StRS checked, 542 SwRS citations, all valid); `just check` pass; `just preflight` pass
- [x] Review: approved; the last review's changes are committed as b7cd8df and d99d2ef
- [x] CI green at d99d2ef: checks, report, static, static-windows, visual; heavy run integration and stress

## Internal references

- CR-343 req-garden-block-table, batch-06; stacks on the use-case-diagram, marker-gate and toolbar/lifecycle requirement changes, now merged.

</details>

