# Verify CR-265

Head: cd51c8b2418d290eb538b50f987f294e32084791 (git 2.56.0.windows.4)

1. New pytest files, at cd51c8b: `uv run --locked --project . pytest tests/test_gate_carry.py tests/test_gate_queue_order.py -q` -> `15 passed`. Covers rule 1's three-step order and the git < 2.38 refusal text.
2. Coverage contract: `pytest skills/chantier/scripts/cli/tests/test_scenario_coverage.py` -> `1 passed`.
3. Search "arrival order|first come first served" over the repo (outside .agents): the remaining hits are the new wording (docs/gates.md, driver.md, concepts.md, declare/gate.py: "next merge's first, then those moved first, then arrival order") and the scenario's lock-order checks, which do not contradict rule 1. No "first come first served" left. driver.md line 168: "After a rebase with no conflict, run no long gate".
4. Rule 3 in a temporary git repo (`carry_check`): clean rebase onto a docs-only main change -> `None` (carries); rebase with a resolved conflict -> `the replay conflicts` (refused). Git older than 2.38 -> message via test 1.
5. `just scenario` passed at this head (work/gates/20261115-021210.log); CI green; not rerun, as instructed. `just check` on other OSes: CI.

Verdict: VERIFIED

## Description pass (head cd51c8b2418d290eb538b50f987f294e32084791, code unchanged)

Checked the posted PR body against pr-template.md "The audit" and the diff. Sections 1, 2, 3, 5 (one gap), 6, 7, 9, 10 fine: order and fold correct, no internal id or role outside Internal references, SHAs cd51c8b on every Test plan item, the 330 -> 400 s budget matches the diff (scenario/README.md, run_scenario.py).
Failed: audit 4. Deliverables holds four bullets and no visual (no flowchart, sequence, before/after table or code sketch); the change is structural (shared CLI code), so "None" is not allowed either. Add e.g. a before/after table of the gate queue order or a short sequence of the push-early flow.
Minor (audit 5): Changes omits the scenario budget files (scenario/README.md, scenario/run_scenario.py) and the gate_lock.py docstring.

Verdict: NOT VERIFIED (description only)

## Description pass 2 (head cd51c8b2418d290eb538b50f987f294e32084791, code unchanged)

Re-read the posted body: Deliverables now holds a before/after table (audit 4 met); Changes names gate_lock.py, scenario/run_scenario.py and scenario/README.md (audit 5 met). Audit 1-3, 6, 7, 9, 10 still hold. Nit: the "Conflicted rebase" After cell wording is slightly muddled; not blocking.

Verdict: VERIFIED
