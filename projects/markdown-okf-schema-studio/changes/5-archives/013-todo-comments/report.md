# Report — todo-comments

Status: **done** (feature session, 2026-10-16, branch `dev/gsemet`), pending the idle e2e re-run.

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T14 | HTML comments show as a gray chip, the word TODO and `<!-- TODO … -->` as a green chip; tool comments (markdownlint, prettier-ignore, toc, cspell, vale) stay hidden; edit mode opens a comment block on its raw text; a comment in a heading does not change its TOC or sticky label | `817e056` |
| T15 | A chip opens an admonition-like box with the comment text (click, Enter, Space), kept open while typing, no reading-line jump; setting `preview.showComments` hides the gray chips live | `6eebd07` |

## Proof of completion

- T14: 13 rendering tests (9 failed before), a real-input scenario for the edit-mode click; review
  APPROVE in round 2 (heading-label leak fixed). The 22 white-paper chapters render 49 gray and 4
  green chips without errors.
- T15: 8 chip-toggle tests, configuration and package-contract tests, visual fixture in light, dark
  and cream; review APPROVE.
- Phase 3 e2e (2026-10-16, `4c5c869`, clean tree): unit 952, contract 2, security 23, visual 154
  checks / 149 images green; integration **not green**: one scroll scenario (solo-block-independent,
  no scroll feedback). A control run of the same e2e on `5406410` (before T19) also failed
  (checkbox undo timeout). All failures this day were timeouts in different suites while the machine
  was in active use; direct runs passed. **Pending: re-run the e2e on an idle machine** (tracked in
  followups.md; also covered by the final `just preflight`).

## Open items

- Inline TODO words in prose have no body, so they do not expand.
- No integration test for an inline chip click in edit mode.
- MyST `% comment` lines are unchanged (not shown as chips).

## Addendum (2026-10-21)

The pending e2e re-run is done: the phase 5 e2e on `5eae169` (later tree, unlocked idle machine)
passed in full, including every integration host, the keyboard suites (75 real-input screenshots)
and checkboxToggle; visual 162 scenarios / 157 screenshots. Status is now **done** without
reservation.

- Final gate: `just preflight` green in CI on `8c55e48` (run 39753045267); merged to `main` with PR #11 on 2026-10-22.
