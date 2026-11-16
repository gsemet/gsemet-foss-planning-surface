Head: a246894665412ae1c1f8f2afc442eca02e0cb209

# Verify CR-204 (delta assessment after a restack)

Move: 10ff69c (on origin/main d178c7e) to a246894 (on CR-203's head 901c916), clean rebase.
`git range-diff d178c7e..10ff69c 901c916..a246894`: one commit, patch identical; only the context
line of the CI green item in pr-template.md differs (CR-203's comment now in the base). The three
files touched are the same as before (driver.md, pr-template.md, worker.md); no CLI file.

## Claims

- Diff content (spec section 1-4: CR driver order, Stack driver note-first, Verifier Review box,
  template Review item and rule): VERIFIED at a246894, judged again by reading
  `git diff 901c916 a246894`; all four spec points present, no CLI or agent file touched.
- Review: approved at 10ff69c: carried from 10ff69c: patch unchanged by the restack (range-diff);
  note "r1 approved at ... committed as 10ff69c" is in `$CHANTIER log CR-204`.
- Local gates `just check` and `just scenario`: `just check` judged again at a246894, passes (58 passed,
  release notes ok). `just scenario`: carried from 10ff69c: cards-only patch unchanged, long gate
  left to the stack's top by order.
- Evidence (no new test, no CLI change): carried from 10ff69c: still true, diff touches three
  cards only.
- CI green: not judged here; the forge checks at a246894 are the Driver's to read.

Verdict: VERIFIED
