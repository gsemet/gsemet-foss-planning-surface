# Report: CR 241

Status: **done** (2026-11-03, branch `change-requests/241-option-button`, PR [#286](https://github.com/gsemet/markdown-okf-schema-studio/pull/286), merged by the owner as 3b899f70, middle of stack #288).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A "Toggle option" toolbar button after Checkbox, in the GFM and MyST palettes and the slash menu, turns the selected lines into `- ( ) ` and back. In the block editor, Enter at the end of an option item starts the next line with `- ( ) `; Enter on an empty `- ( ) ` ends the list. | 3b899f70 |

Requirements: SwRS PALETTE-267 (new, `proposed`), BLOCK-061 updated (`proposed`), dated entry in `requirements/tiers/log.md`, CHANGELOG entry.

## Proof of completion

- `just check` passed (3535 unit tests); all 33 palette-slash scenarios passed in simulation; new scenarios v30 to v33. Only expected values changed in existing assertions (`option` added to action lists, control count 39 to 40).
- CI run 41635061966 green. Real-window jobs not run (manual). One round (1 of 3), reviewer APPROVE.
- Screenshots on branch `change-requests/241-option-button-assets`.

## Open items

- The button icon is a ring with a dot; the owner may want another.
- One unit test ("linked target replaced by a rename (atomic save)") failed once and did not reproduce.
