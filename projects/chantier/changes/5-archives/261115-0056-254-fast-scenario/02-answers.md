# Grill answers

## 2026-11-14

- Scen-Q1, scope: this CR also runs the long gate on main and fixes what fails
  (`long-gate-after-batch-17`), and changes the four gate rules below; the three inbox items
  `long-gate-after-batch-17`, `gate-priority` and `long-gate-defaults` are folded into it (their
  intake in `00-absorbed.md`) and moved to the trash.
  1. Order: the PR the user merges next takes the first place in the long-gate queue; a gate
     already running is never stopped.
  2. Push early: a PR that already exists is pushed at once after a rebase, kept in draft, so CI
     runs while its gate waits; it leaves draft once the long gate and CI pass at the same head.
     A new PR still waits for its long gate (`AGENTS.md`).
  3. Clean rebase: a rebase with no conflict runs no new long gate; green CI at the new head is
     enough. A rebase with a conflict runs it.
  4. Stack: the user chooses, at the go or during the run, one long gate on the stack's top PR
     only; the lower PRs are ready to merge once CI is green, the Verifier says VERIFIED and they
     are handed back. Shown in `chantier status` (text, `STATUS.md`, `STATUS.json`), the CR board
     pane (`hooks/register.tsx`) and the web board: each CR says whether its long gate was waived
     and which PR carries the stack's validating gate.

- Scen-Q5 and Scen-Q6 (the user asked a Fable subagent to advise, then took its whole plan, A):
  - Three CRs, in order: `baseline-and-legacy` (the long gate on main and its fixes, the one-off
    migration, the legacy readers and their scenario cases removed), then `fast-scenario` (this
    CR: units, the parallel runner, the moves to pytest, the cut waits, the README contract,
    GitLab reduced; no change under `src/`), then `gate-rules` (the four gate rules of Scen-Q1).
  - Scen-Q6: the 14 archived `STATUS.json` files with old batch ids (5-archives and 6-trash) are
    rewritten to `batch-NN` by the migration script; the records keep `backfill.former_id` as the
    trace.
  - Scen-Q3 amended: 4 workers by default, with `--jobs N`; the CR measures 4 against 8 once
    and records it. Units are smaller than workers: about 9 units, the longest first.
  - Step 0, before any cut: one instrumented run of today's scenario printing seconds and
    command count per case; the unit budgets come from it.
  - The runner prints, on every run, a table per unit (checks, commands, seconds) and the wall time.
  - Done: three consecutive green runs under 300 s on the user's Windows machine, one green run
    under 300 s on Linux CI, every README coverage bullet mapped to a unit or a test.
  - A standing rule (`scenario/README.md` or `CONTRIBUTING.md`): a new case joins an existing
    unit's batch or goes to pytest; a unit over its budget prints a warning the Inspector reads;
    the run never fails on time.
  - Scenario CLI calls stay real processes (end to end); in-process calls only in pytest.
  - The analysis and the advice are kept in `analysis/`.
- FS-Q1, a hung unit: past 600 s, or 4 times its budget if longer, the unit is killed with its
  process tree and the run fails; slowness alone is only a warning (A).
- FS-Q2, the coverage contract: a structure test checks that each `scenario/README.md` coverage
  bullet names an existing unit or test, beside the Inspector's reading (A).
- Scen-Q2, where the 5-minute target holds: on the user's Windows machine, both forges, and on
  Linux CI (A).
- Scen-Q3, how many scenario units run at once: a fixed number, 4 (B).
- Scen-Q4, how no coverage is lost: the coverage list of `scenario/README.md` is the contract;
  each bullet maps to a scenario unit or a test, and the Inspector checks that nothing leaves it
  unnamed (A).

- The spec's last open point (Linux CI runner size): gsemet/chantier is public, so `ubuntu-latest` has 4 vCPU; no CI change. Settled by the Chief of Staff from the forge, 2026-11-14.

