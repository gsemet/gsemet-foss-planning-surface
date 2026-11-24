# Check that a stack's branches really chain at ship

Check that a stack's branches really chain (from the Markdown Studio batch-07 retro, re-checked 2026-11-22).

May no longer be valid: check on current main first.

What happened: an ordered stack 439..445 was not a git chain (some branches cut from main, only the forge bases linear); `take` was refused, a stack-driver wrongly said no restack was needed, and two restacks followed.

State on main 687a4723 (read-only check): `ship` (cli/commands/delivery.py:230-276) does not check that the branch contains the previous CR's head; the stack-driver card relies on `restack:` notes, not on `git merge-base`.

Wanted: `ship` in a stack batch checks the ancestry against the previous CR's head; the stack-driver checks with `git merge-base` before concluding that no restack is needed.
