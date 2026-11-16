# Proof rules taken from jleechan's pr-lifecycle skill

## The user's words (2026-11-09, French, verbatim)

> Compare chantier à https://github.com/jleechanorg/jleechan-skills/blob/main/.claude/skills/pr-lifecycle/SKILL.md

Then, on the Chief of Staff's five suggestions:

> 1, 2, 3, 5oui dans une CR dédiée.

## The four points kept

1. **Proof bound to the head.** Every judgment (the Inspector's verdict, the Verifier's
   `verify.md`, the evidence) names the SHA it judged; once the head moves (a new round, a
   rebase, a restack), only the part the move touched is judged again (their "delta
   assessment"), and the PR says which SHA each proof covers.
2. **`UNVERIFIED` rather than silence.** A claim in the PR with no proof is marked unverified,
   not left out or stated as fact; a claim can also be narrowed honestly instead.
3. **Unknown, never zero, in metrics.** A cost or time chantier did not observe is shown as
   unknown, never as 0 (`cost`, `cost --explain`, the reports' tables).
4. **One long wait during CI.** A Driver whose CI runs does all its other work first, then waits
   once, long, instead of polling; it records what wakes it. Measure the tokens a Driver spends
   waiting on CI today before choosing the means.

Left out on purpose: their `Goal:` status line and the six stage labels (ceremony; the Chief of
Staff already keeps the state). Point 4 of the comparison (an independent visual check) is
discussed separately with the user.

## Chief of Staff notes

- Source read: the skill's `SKILL.md` only (2026-11-09); its linked files (`review-routing.md`,
  `review-recovery.md`, `exceptions.md`, `review-records.md`, `six-stage.md`) were not read.
- v0.8.0 already has part of point 1: the Verifier writes the head SHA in `verify.md`
  (`references/worker.md`, Verifier). Open: the Inspector's verdict, the evidence in the PR, and
  what happens to a `VERIFIED` once the head moves.
- Point 2 meets the P1 `pr-details-fold` (the Test plan section, folded); point 3 meets the
  report format (same tables in every report, spend refreshed first).
- Point 4: a new CLI tool only from measured token cost (AGENTS.md); the measure comes first.

## Open point to settle in the grill: a visual check for UI projects

The user (2026-11-09, French, verbatim):

> Pour chantier lui même non, mais pour un projet UI utilisant Chantier ça a du sens. Mais je ne
> comprend pas pourquoi ce ne serait pas le Vérifier lui même. Note ça dans cette nouvelle CR
> comme point à lever

- pr-lifecycle asks an independent seat (two for a headline UI claim) to check that the
  screenshots show what the PR claims. Not for chantier itself; it makes sense for a UI project
  that uses chantier.
- The question to settle: why not the Verifier itself? It already captures the before/after
  at the pushed head. Against: the one who takes the screenshots also judges them, and chantier's
  rule is that the one who checks is not the one who made (`concepts.md`). For: no new role, and
  the Verifier already never wrote the code.
- The Chief of Staff's first idea, not agreed: a project option in `AGENTS.md` ("add a visual
  review"), as the team already allows "add a <kind> review", rather than a built-in role.
