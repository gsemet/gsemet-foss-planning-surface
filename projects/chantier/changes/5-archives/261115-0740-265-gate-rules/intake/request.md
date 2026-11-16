# Four long-gate rules: the next merge first, early push, clean rebase, the stack's one gate

Filed 2026-11-14 by the Chief of Staff, on the user's word (Scen-Q1, then Scen-Q5, the Fable
plan): the third of three CRs, after `baseline-and-legacy` and `fast-scenario`, because it adds
scenario cases to the new units. Its grill so far is in `1-inbox/fast-scenario/02-answers.md`
(Scen-Q1) and the source items' text in `1-inbox/fast-scenario/00-absorbed.md`
(`gate-priority`, `long-gate-defaults`).

1. Order: the PR the user merges next takes the first place in the long-gate queue; a gate
   already running is never stopped.
2. Push early: a PR that already exists is pushed at once after a rebase, kept in draft, so CI
   runs while its gate waits; it leaves draft once the long gate and CI pass at the same head. A
   new PR still waits for its long gate (`AGENTS.md`).
3. Clean rebase: a rebase with no conflict runs no new long gate; green CI at the new head is
   enough. A rebase with a conflict runs it.
4. Stack: the user chooses, at the go or during the run, one long gate on the stack's top PR
   only; the lower PRs are ready to merge once CI is green, the Verifier says VERIFIED and they
   are handed back. Shown in `chantier status` (text, `STATUS.md`, `STATUS.json`), the CR board
   pane (`hooks/register.tsx`, so `just mod` and a pane screenshot) and the web board: each CR
   says whether its long gate was waived and which PR carries the stack's validating gate.

To grill further: whether rule 4 is cut from rules 1-3 (a guess of Fable's).

Split 2026-11-14 (GR-Q1, `02-answers.md`): this CR keeps rules 1-3; rule 4 and draft 4 moved to
`1-inbox/stack-gate-waiver/`.
