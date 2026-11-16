# Verify CR-266

Head: 233de2fbf562e3700e6e40da22ca629ba8a490d4

All claims at 233de2f (worktree clean).

1. Scenario cases. `uv run --locked python scenario/run_scenario.py --unit stack --unit gates --keep`:
   stack github 113/113, gates github 79/79, exit 0 (stack 327 s over its 320 s budget: WARN only).
   Section 13b checks all `[x]`: no waiver -> lower CR refused; `order waive stack` records O-1/stack/note on each CR;
   a CR's waiver inside a waived stack not withdrawn alone; `handoff` prints
   `gate: waived (O-1, stack): run no long gate; validated by CR-107` (lower) and
   `gate: this CR's long gate validates the stack (CR-105, CR-106, CR-107)` (top);
   status/STATUS.md/STATUS.json `waived -> CR-k (#n)` and `validates CR-105, CR-106`;
   lower CR ready with no gate and no --no-gate (event has the order); top refused without its gate
   (`no long gate passed at 70428e3...`); `order add` on top moves validation (`... validates the stack (..., CR-108)`,
   `validated by CR-108`); `order waive stack --note -` makes a lower CR need its gate again, handed-back CR keeps its waiver.
   Gates unit: `carried from <sha7>` in STATUS.md.
2. Refusals. `uv run --locked pytest .../test_gate_waiver_orders.py test_gate_waiver_handback.py test_gate_view.py -q`:
   29 passed (stack waiver refused outside stack mode; `waive <cr>` refused without `--follow-up` and with a missing folder).
3. `just mod` equivalent `uv run --no-project python scripts/mod.py`: exit 0, 59 pass 0 fail.
4. Audit C7. Wrapper (scratchpad c7.py) ran the stack unit and called `audit.event_checks` on the live record right
   after the waiver case: batch-02, CR-105 ready with handback `gate_waiver: O-1`, no gate event.
   Output: `(True, 'each CR handed back ready has a verdict VERIFIED and a passed long gate (or a no_gate, gate_from or gate_waiver hand-back) at its head (1 CRs)', 'C7')`.
   Limit: event_checks only (not a full `audit.py <workspace>` run: the scenario closes its batch, the audit needs an open one); only one CR was ready at that point.
5. Not run (agent cannot): `just check` on three OSes (CI green per caller), pane screenshot, `just docs-screenshots`, web board capture:
   gaps named in work/pr-body.md; judged as gaps. Nothing placed under evidence/.

Notes for the PR body: the C7 output above is not yet in pr-body.md (it says "No C7 output yet").

## PR 215 description pass

Head: 233de2fbf562e3700e6e40da22ca629ba8a490d4

VERIFIED. Posted body equals work/pr-body.md; sections and fold order match the template; no internal reference outside Internal references (opening Stacked on #214 line is the ordered exception; CR-k in the column table is product output wording); Changes file list matches the diff; Known gaps as recorded. Minor: Chief of Staff in Human decisions is a product term (card changed) but not defined on first use.

## Re-verify after restack (233de2f -> f86d5b4, onto CR-262 af97942)

Head: f86d5b47e949892c687c6d9f8e638bab57ca114e

All claims at f86d5b4 (worktree clean).

1. Scenario. `uv run --locked python scenario/run_scenario.py --unit stack --unit gates`: stack github 121/121, gates github 82/82
   (stack 368.6 s over its 320 s budget: WARN only). Same section 13b behaviour as before (waive, carried gate, handoff lines, status surfaces).
   Long gate `just scenario` pass at f86d5b4: work/gates/20261115-054626.log.
2. Refusals. `uv run --locked pytest` on test_gate_waiver_orders.py, test_gate_waiver_handback.py, test_gate_view.py (skills/chantier/scripts/cli/tests): 29 passed.
3. `uv run --no-project python scripts/mod.py`: 59 pass, 0 fail.
4. Not rerun: C7 audit wrapper (covered by the stack unit passing); CI 5 checks green per caller. Gaps unchanged.

Verdict: VERIFIED at f86d5b4.
