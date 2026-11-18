Head: b69d4b1418884ccada52e456d4ffc1bc998f8135

VERIFIED

1. Diff touches exactly the three cards (b69d4b1). `git diff --stat origin/main...HEAD`:
   inspector.md 4+, spec-critic.md 4+/1-, spec-writer.md 5+ (3 files, 12 insertions, 1 deletion). Tree clean.
2. Wording matches spec sections 1-3 (b69d4b1). `git diff origin/main...HEAD` shows: the spec-writer bullet
   right before "The evidence that proves it" (verbatim section 1); the kind-1 sentence at the end of
   spec-critic kind 1, with the "evidence, not an implementation detail" clause (section 2), no fifth
   kind added; the inspector paragraph right after the host and default matrix paragraph, `blocking` (section 3).
   Agent files untouched (not in the stat).
3. PR #310 description (b69d4b1): body from `gh pr view 310` equals work/pr-body.md; sections render,
   Summary/Deliverables/Changes match the diff, Known gaps "None" with no UNVERIFIED claim, no image,
   no role-name misuse. Reading check present and sound: CR-344 spec (3-done/344.../03-change-spec.md)
   reads `<web>` (lines 40, 361) and has a "The checker refuses" test of prepared texts (line 384) next to
   the real-sheet checks; the written prepared-text-only example gets a one-line fix from kind 1.
4. Review box "approved at ef9f979": `chantier log 349` has "r1 approved at ef9f9779..., committed as b69d4b14".
5. CI: Driver's note, all 5 checks pass at b69d4b1 (scenario ubuntu pass); not re-run by me.

Description pass (b69d4b1418884ccada52e456d4ffc1bc998f8135), on `gh pr view 310 --repo gsemet/chantier --json body`:
6. Posted body at headRefOid b69d4b1 (same as `git rev-parse HEAD`): visible order Summary, Deliverables, Blast radius,
   Autonomous decisions, Known gaps, then one Details fold with blank lines after summary and before the close; nothing after
   `</details>`. No image, so no username/home path. No internal reference outside the last section; role names (spec-writer,
   spec critic, inspector) are product terms of cards the diff changes.
7. Consistent with the diff (`git diff origin/main...HEAD`): spec-writer.md one bullet in "## Output" before the evidence bullet;
   spec-critic.md sentence at end of kind 1 in "## What you look for"; inspector.md one paragraph after the host and default
   matrix paragraph in "## Your part"; 3 files only. Table text and Changes match. Known gaps "None": no UNVERIFIED claim.
8. Test plan SHAs: Review `ef9f979` committed as `b69d4b1` matches the log note "r1 approved at ef9f9779..., committed as b69d4b14";
   gate/CI/Verified cite b69d4b1 (log: "just check: pass", "all 5 pass"). No STALE mark.
