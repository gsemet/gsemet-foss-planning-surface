# Verify: CR-209 (delta after restack onto CR-208)

Head: e28788ab8142dee3eb721b3fa6e690718b091c34

Move: 8821eb0 (on origin/main d178c7e) to e28788a (on 2da9cf5), conflict in SCORECARD C9 resolved, then amended.

## Judged again

- The CR's own patch is unchanged: `git patch-id --stable` of `d178c7e..8821eb0` and of `2da9cf5..e28788a` (evals/) are equal (8a38ce39...). Same 2 files, +21 -6.
- Resolved hunk, SCORECARD C9: the row keeps the CR's "status --refresh on a wake" and the audit column's direct-batch sentence, and carries the base's "cancel without --epoch is refused (exit 2)" clause. Read in the diff: correct.
- audit.py merged without conflict; the only difference from 8821eb0 in that file is the base's C11 line (`"ask", "merge"`), not the CR's.
- `git diff --name-only d178c7e 2da9cf5` (56 files) touches the CR's two files only through CR-196's C11 line and CR-208-side SCORECARD C9; no card, CLI or hooks change is in this CR's diff.
- Claim "J3 and C9 pass on lawful behaviour, fail on forbidden": run 1 transcripts through this head's audit.py (`work/run1_recheck.py`): J3 x3 Verifier detached worktrees PASS; C9 direct PASS (0 without epoch, 3 refreshes with none); J3 `run3.py` write FAIL; J14 FAIL. Both real FAILs remain.
- `just check` at e28788a: 58 passed, release-notes ok.
- `just eval-dry-run` at e28788a: 6 of 6 cases as expected (Foreman C9 and planted cases intact).

## Carried

- CI green, review approval, the PR-body evidence output: carried from 8821eb0: same patch (patch-id); CI must be seen again at e28788a.
- Long gate: not run, per the brief (the stack's top gets it once).

## Verdict

VERIFIED at e28788a.
