## Summary

The local Windows run of the long gate was owed by the top of the stack only. In a parallel batch there is no stack: each PR lands alone on main, so that exemption never applied, and four PRs were handed back with no local run. The local run now depends on the batch's shape, and the shape is asked of the user when a batch opens instead of defaulting to parallel.

## Deliverables

- `AGENTS.md`: "Windows coverage" by shape. Parallel and series: each PR the long gate covers runs `chantier gate <cr> scenario` locally at its head before it is called ready (a docs-only or eval-kit-only PR owes none). Stack: only the top, a docs-only top included, and the run moves to a CR that joins on top. No Windows run on the merged result.
- Cards: the reading of a project rule "by shape" is stated once (`driver.md`, carries and early push) and referred to from the others; the "batch's top" definition is gone. The Foreman sends back a covered CR handed back `--no-gate` with the note `long gate: this CR runs <command> locally`, and the rebase `take` after a merge carries it. Each covered CR's ask carries the local-gate clause.
- Opening: the Chief of Staff asks parallel, series or stack, with a recommendation drawn from the links and the overlap of the CRs' files and the local-gate cost per shape, and always passes `open --mode`. `open`'s CLI default stays parallel.
- Docs that said parallel needs no question (`README.md`, `CONTRIBUTING.md`, `docs/use-cases-foreman.md`, `docs/use-cases-direct.md`, `docs/batch-modes-texts.md`, `docs/batch-modes.svg`, `docs/planning-folder.md`) say that the shape is asked.

Reading proof, one line per case (cards only):

- Parallel: each covered PR runs `chantier gate <cr> scenario` before its ready hand-back and hands back with no `--no-gate`; an exempt PR owes none; a `--no-gate` hand-back of a covered PR goes back with `long gate: this CR runs <command> locally`.
- Series: the same, and the rebase `take` after a predecessor's merge carries the note when there is no pass or carry at the new head.
- Stack: the top runs it, a docs-only top included; the mergeable-top rule is unchanged.
- Project rule: one that names each shape is followed as written; one that names the stack's top alone is read by shape.
- Opening: the plan asks parallel, series or stack with a recommendation and names the shared files; `open`'s default stays parallel.

Evidence at `2693d35`: `grep -rn "batch's top" skills/chantier/references/` prints nothing; `grep -n "Windows coverage" AGENTS.md` prints line 9, the rule by shape; `grep -rn -i "ask for nothing\|no flag, no word" README.md docs/` prints nothing.

## Blast radius

Grade: 2. Cards and docs only, no code; the cards steer every batch, so a wording slip changes agent behaviour. Revert restores the previous wording.

## Autonomous decisions

- `docs/batch-modes.svg` also said "(the default)" and "Ask: nothing", so its text was edited by hand to match the doc.

## Known gaps

- No Windows run covers the merged result; accepted, the pipeline's ubuntu job covers it.
- None beyond the above.

<details>
<summary>Details</summary>

## Changes

- `AGENTS.md`, `skills/chantier/references/{driver,foreman,foreman-stack,chief-of-staff,concepts}.md`, and the docs above.

## Human decisions

- Each PR of a parallel or series batch owes the local run; a stack's top alone owes it, a docs-only top included.
- The shape is asked at every opening, with a recommendation; no default.
- A project rule that names each shape is followed as written.

## Impacts

Maintainers running batches are asked the shape and run the local gate once per covered PR in parallel or series.

## Test plan

- [x] New or changed tests: No behaviour change (cards and docs)
- [x] Local gates at `2693d35`: `just check` pass; `chantier gate scenario` (`just scenario`) pass
- [x] Evidence: the three greps above at `2693d35`
- [x] Review: approved at `2693d35` (reviewed at 627bd4d, committed as 2693d35)
- [x] Verified at `2693d35`
- [x] CI green at `2693d35`

## Internal references

CR-473 own-gate
</details>


🤖 Generated with [Claude Code](https://claude.com/claude-code)
