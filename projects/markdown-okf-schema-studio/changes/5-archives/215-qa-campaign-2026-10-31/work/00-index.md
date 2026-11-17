# QA campaign 215 — radio choice lists, cards, comments

Date: 2026-10-31. Subject: markdown-okf-schema-studio at commit `18c4f020` (main, clean tree).
Revision: `18c4f020`
Status: **partial**

> [!IMPORTANT]
> Status is **partial** for one reason: the Agents window (#223) is not covered (owner,
> 2026-10-31: ignore for now). Everything else ran. First real use of the QA skill as
> merged in #237 and #239: what did not work as written is in [skill-feedback.md](skill-feedback.md).

## Summary

- **Radio choice lists (#240)** hold up well under real use: no click ever changed more than two lines, one undo
  step always restored the source, every palette mode and theme rendered. Four Medium defects sit
  in the edges: keyboard entry, focus after a choice, the open-editor guard, read-only files.
- **One High:** in edit mode, a click on the footer of a `:link:` card follows the link, and typing
  then lands in the other file.
- **Regression pass:** all 9 open P1/P2 items from campaign 210 still reproduce; none was fixed by the
  changes since.
- **Undo in the Open With editor** works (C7b re-check): the earlier failure was a harness limit with
  the side preview also open, not a regression of UX-03.

## Findings

| ID | Severity | Verdict | Finding | Sheet | Evidence | approved | Backlog |
| --- | --- | --- | --- | --- | --- | --- | --- |
| QA215-01 | High | Bug | Edit mode: a click on a `:link:` card footer navigates away; typing then edits the target file | [sheet](02-grid-cards/c3-1-link-card-footer-click-navigates.md) | [currently](../evidence/c3-1-currently.jpg) | [x] | [P1](../../2-backlog/P1/link-only-targets-not-editable/01-intent.md) |
| QA215-02 | Medium | Bug | Tab into a radio group stops on the list, item and paragraph before the first option (GFM-039) | [sheet](01-radio-choice-lists/215-c1-1-radio-tab-entry-extra-stops.md) | [currently](../evidence/215-c1-1-currently.jpg), [expected](../evidence/215-c1-1-expected.jpg) | [x] | [P2](../../2-backlog/P2/radio-choice-focus-and-guards/01-intent.md) |
| QA215-03 | Medium | Gap | A radio choice (click, Space, external rewrite) drops keyboard focus to the page body | [sheet](01-radio-choice-lists/c2-1-radio-choice-drops-keyboard-focus.md) | none: focus, measured | [x] | [P2](../../2-backlog/P2/radio-choice-focus-and-guards/01-intent.md) |
| QA215-04 | Medium | Bug | A radio click while a block editor is open writes two lines and closes the editor when the option first scrolls into view (GFM-039, BLOCK-041) | [sheet](01-radio-choice-lists/c7-1-radio-click-with-open-editor-writes.md) | diff in the sheet | [x] | [P2](../../2-backlog/P2/radio-choice-focus-and-guards/01-intent.md) |
| QA215-05 | Medium | Bug | On a read-only file a radio click shows the new choice, writes nothing and gives no reason | [sheet](01-radio-choice-lists/c7-2-readonly-radio-click-silent.md) | [currently](../evidence/c7-2-currently.jpg) | [x] | [P2](../../2-backlog/P2/radio-choice-focus-and-guards/01-intent.md) |
| QA215-06 | Medium | Gap | The Comments button hides the chips but leaves review-thread highlights and badges visible and clickable | [sheet](03-review-comments/c4-1-comments-button-leaves-review-threads.md) | [currently](../evidence/c4-1-currently.jpg) | [x] | [P2](../../2-backlog/P2/comments-button-hides-chips-only/01-intent.md) |
| QA215-07 | Low | Gap | A numbered grid-card title (`1. First *card*`) shows its asterisks literally | [sheet](02-grid-cards/c3-2-numbered-card-title-keeps-markup-literal.md) | [currently](../evidence/c3-2-currently.jpg) | [x] | [P3](../../../2-backlog/P3/grid-card-title-and-options/01-intent.md) |
| QA215-08 | Low | Gap | `:header:` / `:footer:` options of a grid-item-card dropped without a hint (observed once) | [sheet](02-grid-cards/c3-3-grid-card-header-option-dropped.md) | none: 0 option nodes measured | [x] | [P3](../../../2-backlog/P3/grid-card-title-and-options/01-intent.md) |
| QA215-09 | Low | Gap | A failed comment save or Resolve shows a raw `Error: EACCES … open '<path>'`; a popover draft is lost silently when its thread vanishes | end of the [QA215-06 sheet](03-review-comments/c4-1-comments-button-leaves-review-threads.md) | none | [x] | [P3](../../../2-backlog/P3/comment-failure-messages-and-lost-drafts/01-intent.md) |

Merged: `c2-2` (extra Tab stops, counted 6) into QA215-02. Triage (owner-approved, 2026-10-31):
QA215-01 merged into the link-only item, raised to P1; QA215-02 to 05 form one P2 item (the "focus
after write" row of P3 `radio-choice-followups` folded in); QA215-06 merged into the Comments item,
raised to P2; QA215-07 and 08 share a cause (one P3), QA215-09 is its own P3. The skill feedback
becomes P2 `qa-skill-215-feedback`. Notes:

- QA215-06 widens the existing P3 item `comments-button-hides-chips-only` (REVIEW-152) rather than
  making a new one: propose raising that item to P2.
- QA215-01 shares its root with P2 `link-only-targets-not-editable` (a link click wins over editing
  in edit mode); the fix CR for either should look at both.
- QA215-04: the editor had no typed text, and the sheet points to a blur-commit, so no data loss is shown;
  Medium stands.

## Decisions for the owner

No finding has the verdict **Decision**: none contradicts a requirement that specifies it. Owner
questions raised by the campaign:

| # | Question | Why |
| --- | --- | --- |
| Q1 | Test the Agents window with a signed-in VS Code profile? | **Owner: ignore for now** (2026-10-31). |
| Q2 | Raise P3 `comments-button-hides-chips-only` to P2 with QA215-06? | **Owner: yes**, merged and raised to P2. |
| Q3 | Publish the radio "before" screenshots of #240? | **Owner: no**; the shots were deleted. |

## Regression pass (C6)

| Item | Result |
| --- | --- |
| P1 frontmatter-editor-stuck-after-rejected-value | still reproduces |
| P2 link-only-targets-not-editable | still reproduces |
| P2 card-header-option-enter-adds-blank-line | still reproduces |
| P2 alert-palette-after-lazy-continuation | still reproduces |
| P2 replace-all-skips-blocks-with-link-url-match | still reproduces |
| P2 wide-table-tab-editor-offscreen | still reproduces |
| P2 okf-link-hint-ignores-document-folder | still reproduces |
| P2 schemaless-number-editor-cannot-commit | still reproduces |
| P2 narrow-toolbar-covers-first-lines | still reproduces |

P1 `unnecessary-table-margin-breakage` skipped (parked).

## New-feature coverage

| PR | Feature | Charter | Result |
| --- | --- | --- | --- |
| [#240](https://github.com/gsemet/markdown-okf-schema-studio/pull/240) | Radio choice lists, decide in the page | C1, C2, C7, C7b | QA215-02, 03, 04, 05; all else PASS |
| [#223](https://github.com/gsemet/markdown-okf-schema-studio/pull/223) | Studio in the VS Code Agents window (merged before the baseline, never covered) | C5 | not run: harness cannot reach the window |
| [#230](https://github.com/gsemet/markdown-okf-schema-studio/pull/230), [#236](https://github.com/gsemet/markdown-okf-schema-studio/pull/236) | Grid card layout, card title editor (re-check; covered in 210) | C3 | QA215-01, 07, 08; title editor PASS |
| [#234](https://github.com/gsemet/markdown-okf-schema-studio/pull/234) | Comment threads hardening (re-check; covered in 210) | C4 | PASS; QA215-06 and 09 not caused by #234 |

Not user-facing, confirmed: #237, #239, #242 (QA skill and tooling).

## Severity scale

| Severity | Meaning |
| --- | --- |
| High | Data goes to the wrong place or is lost, or a core journey is blocked. |
| Medium | A journey works only with a workaround, or a guard or requirement is broken without data loss. |
| Low | Friction, wording, a cosmetic or rare defect. An intent question is Low unless data is lost. |

## Method

- Foreman: scope from `coverage-map.py` and `new-features.py` (baseline campaign 210, `b9118506`),
  smoke check (doctor no FAIL, smoke scenario 5/5), charters in [charters.md](charters.md), triage
  from the Driver returns only.
- QA Drivers (Sonnet, effort medium), 3 windows at most in total:

| Driver | Charters | Budget used | Replays |
| --- | --- | --- | --- |
| A, radio (#240), 2 windows | C1 partial 31/40; C2 partial 40/40 | 71 calls | none (no High) |
| A2, radio follow-up, 1 window | C7 partial 40/40; C7b done 13/12 | 53 calls | none (reproduced in charter) |
| B, re-checks, 1 window | C0 done 19/40; C3 partial 38/40; C4 partial 41/40; C5 blocked 9/30; C6 done 12/30 | 119 calls | QA215-01: still reproduces |

- C0 sweeps: 0 CHANGED on `synth/tables.md`, `synth/frontmatter-edge.md` and chapters 04–06 (one
  false positive on a radio, see skill-feedback B1). Latency on chapter 08: p50 222 ms, max 300 ms
  (campaign 210: 56 / 272 ms on its probe; no regression seen).

## Limits

- **#223 Agents window: not covered (owner, 2026-10-31).** No backlog item; the harness notes are in the
  [gap sheet](08-test-campaign-gaps/c5-agents-window-unreachable.md).
- Not covered for radio lists: dark and high-contrast on the plan fixture in C7, a click before the
  preview re-renders after a source insert (wrote nothing, no message, cause not diagnosed), a book
  chapter turned into a radio group, a real screen reader, the 16 / 256 item limits.
- C3: no book chapter contains `{grid}` or `{card}`; only synth and visual fixtures were used.
- C4: two previews at once, a Resolve race against an external rewrite, threads from the compose UI.
- C0: chapters 08 and 02 only partly swept; table cells of 04 and 05 not swept.
- Test-campaign gaps: [radio Tab order not asserted](08-test-campaign-gaps/c1-radio-tab-order-not-asserted.md),
  [radio coverage note](08-test-campaign-gaps/c2-radio-coverage-note.md).

## Tests to promote

| Scenario (`$SK/scenarios/`) | Why |
| --- | --- |
| `c3-1-link-card-footer-click-navigates.json` | High, wrong-file edit; real-input E2E once fixed |
| `c7-1-radio-click-with-open-editor-writes.json` | Guard bypass with a buffer write |
| `215-c1-1-radio-tab-entry-extra-stops.json` | Tab order is not asserted anywhere |

The 7 new replay scenarios and the fixture they need (`synth/radio-c1.md`) were written in the QA
worktree only; copies are kept in [replay/](replay/scenarios). Promote the fixture with the
scenarios.
