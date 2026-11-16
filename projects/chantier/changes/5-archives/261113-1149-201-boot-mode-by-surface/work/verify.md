# Verify CR-201 at 6f9a236

Verdict: VERIFIED.

1. just check: relied on the gate log (work/gates/20261112-235739.log), pass at 6f9a236.
2. just scenario: log shows github and gitlab 586/586, "result: pass at 6f9a236".
3. SHA-256 of the seven docs/*.png equal intake/screenshots/*.png: all True.
4. Old wording search (README, CONTRIBUTING, docs, skills, evals RUNBOOKs): no match.
5. README has no "What is Chantier?" / "Repository layout"; CONTRIBUTING has both as ### under "How the project is built"; its relative links all exist, its one anchor is README.md#batch-modes.
6. README headings in the required order; #batch-modes and #change-requests-lifecycle present.
7. RUNBOOKs: real-foreman and full start `/chantier:chief-of-staff foreman Run...`; real-direct `... direct Run...`.
8. Both simple SVGs rendered (evidence/*.png): entry line fits its box; texts.md equal the SVG lines.

Cards against rules 1-10: all carried (chief-of-staff.md Starting a batch steps 1-2, SKILL files, session-start, init, hosts). Minor, not blocking: rule 7's "a Foreman batch followed from the phone keeps working through orders" is not stated as such in the card; the "keeps the steering it was opened with" bullet covers the rest.
Not checked: the PR body's pending items (SHAs, README board screenshot in Deliverables) are the Driver's.

## Pass 2: posted PR description, head 6f9a236

Verdict: VERIFIED.

- Head is 6f9a236; every Test plan item names it. CI: check (3 OS), eval-dry-run and scenario pass.
- Diff (origin/main..6f9a236): 29 files, matches Changes: cards, README, CONTRIBUTING, docs, 7 PNGs, 2 SVGs and texts, 2 RUNBOOKs.
- Image link (raw.githubusercontent, pinned to 6f9a236) answers 200. README and boards.md structure match the Deliverables claims.
- Mode table matches chief-of-staff.md Starting a batch; claude-code card still marks the argument handling unproved (Autonomous decision true). boards.md subsections and last guard section present.
- Layout per pr-template.md: order right, one details block, blank lines after summary and before closing tag, nothing after, no BOM, internal reference only in the last section.
- Note: no forge review is posted (reviews empty); "Review: approved" rests on the batch's own review.

## Pass 3: restack, head dce25c9

Head: dce25c9
Verdict: VERIFIED.

Move: 6f9a236 (on origin/main d178c7e) to dce25c9 (on CR-200's head 373d347). range-diff: the CR's one commit is `=` (patch identical); the six new commits below it are CR-200's chain.
Judged again (the base touched the same files: chief-of-staff.md, concepts.md, README, docs/use-cases-*, evals, status-layout):
- just check at dce25c9, run here: pass (58 passed, release-notes ok).
- The seven docs/*.png hash-equal to intake/screenshots: all True at dce25c9.
- chief-of-staff.md routing row and "Starting a batch" anchor present after the restack.
Carried from 6f9a236: the diff is patch-identical, so claims 4-8 (old wording search, README/CONTRIBUTING structure, RUNBOOK commands, SVG renders), the cards-vs-rules reading and the PR body layout pass stand.
Carried from 6f9a236: just scenario (586/586 on both forges); the stack's top gets the long gate once, not run here.
