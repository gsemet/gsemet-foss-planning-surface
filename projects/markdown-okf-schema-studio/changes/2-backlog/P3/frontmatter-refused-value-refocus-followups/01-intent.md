# Refocus after a refused frontmatter value: menu and list editor

Type: bug · Priority: P3 · Filed 2026-11-01 from CR 218 round 1 inspector (optional items 1 and 2)

## Today

CR 218 refocuses the editor control when the host refuses a value (`receiveFrontmatterResult` in the
frontmatter editor). Two edge cases remain:
- The "inside the value cell" condition includes the field menu or picker. If a writer opens the
  Add field picker while the save runs, the focus is pulled back to the control when the refusal
  arrives. Fix idea: exclude `[data-okf-frontmatter-menu]` from `focusLost`.
- The list editor refocuses its first item, not the one being edited, and no unit test covers it.
- Smaller test nits from the same review (Escape test has a conditional branch; RI-T44's message
  cannot detect a re-post) can be tidied in the same change.

## Expected

The menu keeps focus while it is open. The list editor refocuses the item that was being edited, with
a unit test.

Proof: unit tests for both cases that fail before the change.
