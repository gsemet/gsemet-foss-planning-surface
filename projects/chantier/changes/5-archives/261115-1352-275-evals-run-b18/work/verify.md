# Verify CR-275

Head: ebe3c94c698ee5d411c2932b1ad0487bcf940812

All claims judged at ebe3c94 (base origin/main b07c8d5; merge-base fa97e70).

1. Diff touches only the 4 expected paths: `git diff origin/main...HEAD --name-only` printed evals/README.md, evals/real-foreman/RUNBOOK.md, evals/results/real-direct-2026-11-15-run3.md, evals/results/real-foreman-2026-11-15-run2.md. Pass.
2. Report sections in order (`grep -n '^#'`): The run, What was tested, What happened, Findings, Scorecard, Numbers, For maintainers in both (direct adds two extra sections, "Run 1's findings, one by one" and "Direct mode: the host lines this run proved", between Findings and Scorecard; order of the README's sections kept). Pass.
3. `## The run` tables verbatim: awk-extracted table lines of each audit vs each report, `diff` printed nothing, "IDENTICAL" for both (16 and 14 lines). Pass.
4. Judge and audit counts: foreman audit "513/514 checks passed", "Judge: 2 pass, 0 fail, 4 not run"; direct audit "553/555 checks passed", "Judge: 6 pass, 0 fail, 0 not run"; the reports and README cells carry the same. Pass.
5. SCORECARD rows: all 46 ids of evals/SCORECARD.md found as rows in both reports' Scorecard sections (loop printed no MISSING). Pass.
6. Cost: both priced by the CLI ($10.282, $11.518); "Nothing is not measured" stated; no $0.00. Pass.
7. README rows link results/real-foreman-2026-11-15-run2.md and results/real-direct-2026-11-15-run3.md (git diff). Pass.
8. `just check` at ebe3c94 (clean tree): all passed, 190 passed in 25.92s, release-notes ok. `gh pr checks 225`: just check x3, eval-dry-run, scenario all pass.
9. Spot checks against the audits/forge: (a) steering 20.4%, Foreman $2.101 (audit l.672, 755); (b) CR-101 $2.983 in direct audit (l.703) vs report $2.98; (c) PR 12 mergedAt 2026-11-15T12:49:34Z via `gh pr view 12` matches the report's merge time. Also J14/J26 FAIL lines and J1 FAIL a609474ff1 match. Pass.
10. PR 225 body: Deliverables table and file list match the diff; Known gaps cover the not-seen rows, the unresolved J1 cause, the kit fix-branch merge and the three cost figures; Review/Verifier boxes pending, no STALE mark, no claim beyond the proofs. Pass.

VERIFIED

## Description-only pass (PR 225 body), judged at ebe3c94c698ee5d411c2932b1ad0487bcf940812

Head: ebe3c94c698ee5d411c2932b1ad0487bcf940812

- Posted body vs work/pr-body.md: `gh pr view 225 --json body` diffed (CR stripped) against pr-body.md: only a trailing blank line differs. Pass.
- Summary, Deliverables, Changes match `git diff --stat origin/main...HEAD` (4 files: README, RUNBOOK, two reports). Pass. Test plan SHAs are ebe3c94. Internal references only in the last section. Pass.
- Review box "Review: approved at ebe3c94": `chantier log CR-275 --batch batch-18 | grep -i -E "committed|carried|inspector"` shows only "r1 inspector approved at fa97e7037e6d9dbae8fcc6870e07b0994d0eb21b"; no note names ebe3c94 (no "committed as", no "carried from"). The box cites a SHA no approved-pass note proves. FAIL.

NOT VERIFIED

Head: 2e2a20e1e1c1c26f279cd3cc3677f91fc4ccb19c

Move pass ebe3c94..2e2a20e (clean rebase onto b07c8d5): git range-diff shows the commit unchanged (=); diff vs origin/main is the 4 files in the three paths (README, RUNBOOK, two reports); CI at 2e2a20e all pass (check x3, eval-dry-run, scenario); posted body equals pr-body.md (trailing blank line only); Test plan SHAs cite 2e2a20e carried from ebe3c94; earlier Review-box FAIL cleared by the driver notes (approved at fa97e70, committed as ebe3c94, carried).

VERIFIED
