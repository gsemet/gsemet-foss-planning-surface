# Change Specification: the README says what a batch costs, Foreman or direct

## Goal

The user's word, 2026-11-15: put a few facts on costs in the README, for instance whether steering
a batch directly from Opus costs more than a Foreman on Sonnet, and whether that Foreman does the
job well. The README gives the measured figures of batch-18's two real eval runs, says plainly what
they let a reader conclude and what not, and tells a user how to measure their own batches.

## Which README

- **The root `README.md`** gets the section. It is the user's page, it already sells "Direct or
  Foreman" (its first bullets) and links [Costs and budgets](docs/costs.md); the choice between the
  two modes is a user's choice, so its cost belongs there.
- **`evals/README.md` does not change.** It is the maintainers' page for running campaigns; its
  Campaigns table already carries each campaign's cost and last run, and refreshing those rows from
  the 2026-11-15 runs is the eval kit's business (other CRs of the batch), not this one.
- **`docs/costs.md` does not change.** It explains how the cost is measured and capped; the new
  section links to it for that.

## What changes

One file: `README.md` at the repository's root. A new section `## What a batch costs`, placed right
after `## Batch modes` and before `## Change Requests Lifecycle` (it compares the steering modes
the reader has just met in "How Chantier works" and "Batch modes"). Plain English, the repository's
voice; no other section is edited.

The section holds, in this order:

1. **One sentence of frame:** the figures come from two real batches of chantier's own eval, run on
   2026-11-15 on a small sandbox repository: the same five frozen CRs, budget $20, one run each.
   Run 1 was steered by a Foreman on Sonnet 5.5, in stack mode; run 2 by the Chief of Staff in
   direct mode on Opus 5.5, in parallel mode. The workers (Drivers, Coder, Inspector, Verifier,
   conflict resolver) ran on Sonnet 5.5 in both. They are orders of magnitude, not averages.
2. **A compact table** (these rows, these figures; dollar figures as below, rounded as below):

   | | Run 1: Foreman (Sonnet 5.5), stack | Run 2: direct (Opus 5.5), parallel |
   |---|---|---|
   | The batch (its budget's spend) | $10.28 | $11.52 ($11.91 once closed) |
   | Steering, inside that spend | $2.10 (20%) | $3.39 (30%) |
   | The Chief of Staff's session, outside the budget | about $4.67 | $0.05 |
   | All in | about $14.6-15.0 | about $11.5-11.9 |

   One short line under the table says where the Chief of Staff's $4.67 came from in Foreman mode:
   it was woken at each Foreman turn, with a context of about 200k tokens.
3. **What the two runs show** (a short list):
   - Steering and Drivers together are over 60% of the batch in both runs; coding is 7-8%.
   - A steering session starts at about 70k tokens of context before any work.
   - Inside the budget, the Sonnet Foreman cost less than the Opus Chief of Staff steering the same
     five CRs ($2.10 against $3.39, with about as many calls); but Foreman mode adds a second
     session, the Chief of Staff's, and in run 1 it cost more outside the budget than the Foreman
     saved: all in, run 1 cost about $3 more than run 2.
   - The workers' cost follows the batch mode, not the steering: parallel mode spent more on
     Verifiers and on rebases, stack mode spent on its stack driver.
4. **What they do not show** (a short list, said plainly):
   - No general conclusion that a Foreman is cheaper or dearer than direct mode: one run each, and
     the two runs differ in batch mode as well as in steering.
   - Nothing on whether a Sonnet Foreman steers as well as the Opus Chief of Staff: both batches
     ended green, on a small sandbox, with an operator who knew the answers.
   - No spread: a fair comparison needs the same batch mode in both steerings and a few runs each.
5. **How to measure your own** (one short paragraph or list): `chantier cost` (the batch's spend
   by role: the steering line, each Driver type, each worker type), `chantier cost --by cr` (by CR),
   `chantier cost --explain` (what explains each figure: agents, calls, model, cache shares), and
   the Chief of Staff's own session, priced apart on its own lines and never in the budget. In the
   README's own words the user can simply ask "what did it cost?" (the `## Use` table's row). It
   ends with a link to [Costs and budgets](docs/costs.md) for how the cost is measured and capped.

The section stays short: about 30-40 lines of Markdown, table included. The Driver words it; the
figures, the two lists' substance and the commands above are fixed.

## Decisions carried from `02-answers.md`

- Answer 1 (the user, 2026-11-15, "ok pour ces 12 en parallel", then "oui planifie les 19"): the
  request's scope stands as written, planned in the next parallel batch before the next release.
  This specification takes the request's figures, its conclusion ("no general Foreman vs direct
  conclusion") and its "how to measure one's own" (`chantier cost`, `--by cr`, `--explain`) as they
  are; implementation detail (the README chosen, the section's place and wording) is the agents'.

## Sources of the figures

All figures come from `intake/request.md`, which takes them from the study of batch-18's two real
eval runs (section C, "Costs") and the two audits:
`C:/Users/gaeta/Projets/chantier-eval/real-foreman-2026-11-15.audit.md` (run 1 in this spec; the
real-foreman campaign's run 2) and `C:/Users/gaeta/Projets/chantier-eval/real-direct-2026-11-15.audit.md`
(run 2 in this spec; the real-direct campaign's run 3). The figures are copied into this
specification above so the Driver needs neither; the audits live outside the repository and the
README names no local path, no session id and no workspace.

Figures used, for the Driver's check: run 1 batch $10.282 over 501 calls, Foreman $2.101 (67 calls,
20%), operator about $4.67 final ($4.34 at the audit); run 2 batch $11.518 over 506 calls ($11.91 in
the closed record), Chief of Staff steering $3.390 (62 calls, 30%), grill $0.05; steering plus
Drivers 61% (run 1) and 63-64% (run 2); coder 8% and 7%; steering sessions' first context 70,777
(Foreman), 70,351 (direct), 68,372 (operator) tokens.

## Out of scope

- `evals/README.md` (its Campaigns table rows) and `docs/costs.md`: unchanged.
- Any change to the CLI's `cost` command, its lines or its figures, and the disagreement of the
  end-of-run cost figures (pause, `cost`, `--explain`, archived record; study item B21): other CRs.
- Any new eval run or any new measurement.
- Any claim about Copilot costs: both runs were on Claude Code.
- Images: no screenshot or chart is added.

## Evidence

- `just check` passes; it covers the README's relative links
  (`test_skill_and_references_links_resolve` in
  `skills/chantier/scripts/cli/tests/test_plugin_files.py` checks every relative link of the root
  `README.md` and `docs/*.md`), so the link to `docs/costs.md` must resolve.
- The diff touches `README.md` only.
- A reading check, in the Verifier's note: every dollar figure and percentage in the section matches
  the table and lists of this specification; the section says "one run each" and "no general
  conclusion" in plain words; it names `chantier cost`, `--by cr` and `--explain`; it links
  `docs/costs.md`; it names no local path, session id or person.
- The CR is docs-only: by `AGENTS.md`, a change to the docs alone needs no `just scenario` run before
  its PR.

## Open questions for the user

None. The answers leave no behaviour question open; the choice of README (root `README.md`, not
`evals/README.md`) is the spec-writer's reading, stated above, and the Chief of Staff may raise it
with the user if it wants a word.
