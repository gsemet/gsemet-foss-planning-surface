# Report: CR 243

Status: **done** (2026-11-03, branch `change-requests/243-bug-missing-slash-for-version-admonitions`, PR [#297](https://github.com/gsemet/markdown-okf-schema-studio/pull/297), merged as 7c7fefc8 and 0e1bc4f0, top of stack #296).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | The MyST slash menu lists versionadded, versionchanged and deprecated; every admonition kind gets the icon of its preview callout; choosing a version admonition inserts `:::{versionadded} 1.0` with `1.0` selected. New constant `VERSION_ADMONITION_TYPES` (the type popover of the picker CR is untouched). | 7c7fefc8 |
| T1 round 3 | Two simulated `palette-slash` scenarios `v34-slash-myst-admonitions-light-900` and `v35-slash-myst-admonitions-dark-900` with light and dark screenshots on the `-assets` branch (owner decision). | 0e1bc4f0 |

Requirements: new SwRS PALETTE-268 (`proposed`), PALETTE-238 updated, log entry, one CHANGELOG line.

## Proof of completion

- `just check` passed (3570 tests plus 73 security); `palette-slash` 35 scenarios; scenario count 440 to 442. Reviews: round 1 FIX-REQUIRED (wording), rounds 2 and 3 APPROVE (3 of 3 rounds used). CI green. Real-window jobs not run.
- Changed assertion: the "every icon is used" check in `paletteActions.test.ts` also counts icons used by slash variants (same intent: no orphan icon).

## Open items

- The menu shows at most 10 rows, so no frame shows all 14 entries (Admonition to Hint scroll out of view).
- The version entries have lowercase labels ("versionadded admonition") while the others are capitalised.
- `capture_comment_checks.py` is at 1480 of 1500 lines.
