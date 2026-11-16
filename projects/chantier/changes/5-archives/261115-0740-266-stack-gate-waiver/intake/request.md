# The stack's one long gate, and a long-gate waiver recorded per CR

Split 2026-11-14 from `1-inbox/gate-rules/` by the Chief of Staff, on the user's word (GR-Q1 in
`1-inbox/gate-rules/02-answers.md`): `gate-rules` keeps rules 1-3; this CR takes rule 4 and draft
4 of `.agents/changes/batch-17-issue-drafts.md`, and comes after `gate-rules`. The grill before
the split is in `1-inbox/fast-scenario/02-answers.md` (Scen-Q1) and the source items' text in
`1-inbox/fast-scenario/00-absorbed.md` (`gate-priority`, `long-gate-defaults`).

The user's rule 4 (Scen-Q1):

4. Stack: the user chooses, at the go or during the run, one long gate on the stack's top PR
   only; the lower PRs are ready to merge once CI is green, the Verifier says VERIFIED and they
   are handed back. Shown in `chantier status` (text, `STATUS.md`, `STATUS.json`), the CR board
   pane (`hooks/register.tsx`, so `just mod` and a pane screenshot) and the web board: each CR
   says whether its long gate was waived and which PR carries the stack's validating gate.

Draft 4: "A long-gate waiver is recorded per CR" (CR-228 thought its gate was waived, and the
follow-up gate on main was left to memory).
