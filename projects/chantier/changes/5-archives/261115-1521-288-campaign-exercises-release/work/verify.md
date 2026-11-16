# Verify CR-288

Head: 64acc00f84bd04288b57165c5a719e561fab69bd

All claims judged at 64acc00 (`git rev-parse HEAD` in the worktree; tree clean).

1. validate_notes, on the function (script and output in `work/verifier/evidence/proof.py`, `proof.txt`), notes built from the 0.9.0 notes:
   - no bullet, version 0.10.0: refused with `The notes must say, under For contributors, "- **Not exercised by an eval.** ..." (docs/release-process.md)`.
   - bullet listing claims, 0.10.0: accepted. "None: ..." form, 0.10.0: accepted.
   - 0.9.0 notes unchanged (no bullet; `grep -c "Not exercised by an eval"` gives 0), version 0.9.0: accepted.
   (A fourth text of my own, title changed to 0.10 and checked as 0.9.0, was refused for the title: expected, not a claim.)
2. `uv run --no-project python evals/kit/audit.py --help`: usage printed, exit 0. `audit.scorecard_rows()` (`evidence/reader.py`, `reader.txt`): 49 rows, no duplicate id; C21, J27, J28 parse as rail rows (id, 5 cells), all `by hand`. `git diff origin/main..HEAD -- evals/kit skills/chantier/references/release-template.md` is empty: kit and template unchanged.
3. Docs against the spec (`git diff origin/main..HEAD`): SCORECARD rows C21, J27, J28 and the C6 sentence present with the specified text (the `from` cells drop the CR numbers; J28 has no real-direct, and `grep merge-tree` finds it only in foreman.md, not chief-of-staff.md); README section "Before a release: the claims", the "## Claims" report section and the "Which campaign" clause; release-process sources and the `**Not exercised by an eval.**` bullet with its None form; CONTRIBUTING clause. Code named by the `from` cells exists (`orders_apply._merged`, `gate_run.stop_gate`; driver.md names the pipeline-job long gate).
4. `just check` at 64acc00 (Windows): ruff ok, mypy ok, 190 passed, `release-notes: ... 2026-11-13-v0.9.0/release-notes.md ok`. Linux and macOS: CI green on 5 jobs at 64acc00 (Driver's note, not re-run by me).
5. Review box: `chantier log 288` has "r1 approved at 842b800, committed as 64acc00": proves the box.
6. PR description (read with `gh pr view 235`, headRefOid 64acc00f...): Summary, Deliverables and Changes match the diff; Known gaps names J27 and C21. Minor: the Test plan's Evidence line says "(pending)"; the Driver may point it at `work/verifier/evidence/proof.txt` before marking it done.
7. No long gate (docs and release-notes check only, per the specification); `ship` lists "no long gate passed" as off, to be waived by the steering session.

VERIFIED

## Description pass (head unchanged, 64acc00)

PR 235 body vs diff: Summary, Deliverables, Changes, Autonomous decisions and Known gaps match the diff; test-plan SHAs all 64acc00 and true (CI: 5 jobs pass; Evidence line now filled; review logged); no internal reference outside Internal references.

VERIFIED
