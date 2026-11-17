# Answers

## 2026-11-14: picked for batch-04

Owner, 2026-11-14: « Faisons les 3 CR. Uniquement pose moi les questions impactantes ». The
three open items after v1.9.1 (lost edit-toggle clicks, palette focus bounce, Cursor
compatibility) go into batch-04. Priority P1. The Chief of Staff decides every question without a
user impact; only questions with a user impact go to the owner.

Decided by the Chief of Staff (no user impact):

- First establish the cause: test host (late window activation, xdotool/CDP focus) or VS Code
  moving the focus in a focused window. Use CR-326's diagnostics; a reproducing loop on palette
  and alert-dropdown.
- A host cause: fix the harness (wait on a real focus state), or a documented host-only redo per
  CR-326's Decision 5.
- A product cause (a user's block editor closes right after a click): the question of the fix
  goes to the owner before the CR ships.
- No test removed or skipped, no timeout raised. Proof: stress green over 60 rounds on palette and
  alert-dropdown, and a branch heavy run green.
- This and the lost-clicks CR may share a cause: the spec-writers check, and one may wait for the
  other.
