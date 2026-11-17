# Report — bug-edition-mode

Status: **done** (P2 bug run, 2026-10-15, branch `dev/gsemet`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T3 | Cancel label, Esc = Cancel, status on the button row, smaller text, Cmd/Ctrl+Enter | `03fda60` |
| T3 follow-up | Status centred with its buttons | `ef9d645` |
| T4 | Home/End stay inside the edited block and table cell | `c2281b4` |
| T5 | Table-cell editor gets the block-editor look; arrow keys move cell to cell | `273fcc8` |

## Proof of completion

- T3: 14 new tests failed before the fix and pass after; visual suite green (100 scenarios);
  independent review APPROVE (IME guard added).
- T4: real End-key visual guard fails before the fix; review APPROVE.
- T5: 5 new tests failed before the fix; visual suite green (101 scenarios); review APPROVE.
- Final run: 775 unit + 2 contract + 20 security tests pass; visual 119 scenarios green.

## Open item

Keyboard-injection integration suites (`checkboxToggle`, `realInput`) were not run because the
screen was locked. Re-run `npm run test:e2e` on an unlocked session to close this out.
