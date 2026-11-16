# CR-283 verification

Head: 7d1905b0085a727c07eee7eb081898fa8458517f

All claims judged at 7d1905b (worktree clean, `git status --short` empty before and after).

1. Clean dry-run case passes with the new assertions. `uv run --locked python evals/kit/dry_run.py --case clean`
   -> `ok clean: audit exit 0, no failed check, ... judge pass, pass, pass ...` / `dry run: 1 of 1 cases as expected`. PASS.
2. The new assertion fails on the previous audit.py. Replaced evals/kit/audit.py by `git show origin/main:evals/kit/audit.py`, same command ->
   `FAIL clean: the judge's feature row names the restacked head at merge and the head the record holds / "61385ec (the PR's head is 747194e)", wanted 747194e / 61385ec`
   / `dry run: 0 of 1 cases as expected`. The file was restored; tree clean. PASS.
3. `just check` -> `190 passed in 28.44s`, release-notes ok. PASS.
4. judge.py by hand, read-only, on the sandbox origin: `judge edit-item at 93a906c: pass` (48 passed), `status-filter at 59edd1f: pass` (55),
   `json-api at 1f29cde: pass` (68), `stats-page at 3900c46: pass` (70). PASS.
5. Diff read against the spec (`git diff origin/main`): judge_rows uses the view of `#<c["pr"]>`, judges headRefOid, cell
   `<sha7>, the PR's head at merge|the PR's head` plus ` (the record holds <sha7>)`; missing view -> `not run (the PR's head could not be read from the forge: ...)`
   with `(the record's head, not judged)`; `no head` guard removed; other rows unchanged; sandbox_checks returns per-PR views, J5 messages unchanged;
   docstrings and README line 118 updated; dry run restacks via git_origin plumbing after handback ready, asserts cell. PASS.
6. PR description (read with `gh pr view 228`): renders, Summary/Deliverables/Changes match the diff, Known gaps names the live run. Review box
   `approved at 9d4136c` matches the log note `r1 inspector approved at 9d4136c29ff8...` (`chantier log CR-283`). Minor: the Test plan names 8a4d418
   (a pre-rebase SHA, not in history, flagged by `ship`'s off list) with a carry to 7d1905b stated; the proofs above were rerun at 7d1905b. Not a failure.

VERIFIED

## Description pass

Head: 7d1905b0085a727c07eee7eb081898fa8458517f

Posted description (`gh pr view 228 --json body`) judged against the diff (3 files: evals/README.md, evals/kit/audit.py, evals/kit/dry_run.py) and pr-template.md. No proof rerun.

- Layout: Summary, Deliverables (before/after table), Blast radius (grade 1), Autonomous decisions, Known gaps visible in order; one Details fold with Changes, Impacts, Test plan, Internal references; blank lines in place; nothing after `</details>`. No Issues References or Human decisions (none expected).
- Claims match the diff: audit.py cell wording and `not run` row, dry_run.py restack and `cell=-1`, README judge paragraph.
- Internal references (CR-283, work/r1.md) only in the last section; no role as doer outside it.
- SHAs: Test plan items name 7d1905b; Review 9d4136c carried over a clean rebase, stated; the stale 8a4d418 is gone. CI at the head: all checks pass (check x3, eval-dry-run, scenario).
- Minor, not a failure: the Deliverables table's SHAs are data of the stack run, not base/head captions.

VERIFIED
