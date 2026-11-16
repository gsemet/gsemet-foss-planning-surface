# Verify CR-279

Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9

Judged at 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9 (git rev-parse HEAD in the worktree; tree clean).

## Claim 1: six check points refuse on the refreshed spend, record it and date it; a budget above passes
Command: uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_spend_check.py skills/chantier/scripts/cli/tests/test_cost_reading.py -v
Output: 21 passed in 12.50s. Includes test_a_budget_check_refreshes_the_spend_and_refuses_on_the_real_one[take|stack|round|qa|fix|release] (exit 5, spent_usd = real ~1.00 from stored 0.01, spent_at set), the six "budget above passes" cases, test_no_budget_reads_no_transcript_and_leaves_the_spend_alone, test_an_unreadable_spend_... [0.005-True / 50-False], test_status_says_how_old_..., test_pause_dates_the_spend_it_records, and the 4 test_cost_reading tests.

## Claim 2: real in-process run on a prepared batch (scratch tmp folder, not the live planning folder)
Command: PYTHONPATH=tests uv run --no-sync python -m pytest work/verifier/scratch/test_probe.py -p conftest (probe uses the test world; output in work/verifier/probe.log)
Output:
    before: spent_usd=0.01 spent_at=None
    status before: batch-01 running steering Foreman shape parallel live 2/4 queued 0 foreman local_foreman_t e1 heartbeat never spent $0.01 of $0.5, age unknown
    take (budget 0.5): exit=5 stderr=error: budget spent: $1.00 of $0.5; only the user raises it (`order budget`) stdout=[]
    after: spent_usd=0.9992 spent_at=2026-11-15T14:24:15Z
    status after: batch-01 running steering Foreman shape parallel live 2/4 queued 0 foreman local_foreman_t e1 heartbeat never spent $1.00 of $0.5, 0 min old
    STATUS.json spent_at=2026-11-15T14:24:15Z spent_usd=0.9992
    STATUS.md: ['Updated 2026-11-15T14:24:15Z · steered by a Foreman · independent PRs (parallel) · spent $1.00 as of 2026-11-15T14:24:15Z of $0.5 · 0 asks unread · 0 orders pending']
    take unreadable (budget 50): exit=0 last line=spend not refreshed: no Foreman transcript recorded; budget checked on $0.01 (age unknown)

Shows: stored 0.01 with budget 0.5 -> take exit 5 "budget spent: $1.00 of $0.5; only the user raises it (`order budget`)"; spent_usd rewritten to 0.9992 and spent_at set even though refused; status "..., 0 min old" (before: ", age unknown"); STATUS.json spent_at; STATUS.md "as of"; refresh failure -> line "spend not refreshed: no Foreman transcript recorded; budget checked on $0.01 (age unknown)", exit 0 under budget. No-budget case and unknown-spend status covered by Claim 1 tests.

## Gates
CI at 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9: all 5 jobs green including just scenario (ubuntu), per the prompt; not rerun. Not required: refresh-time measure (named in Known gaps).

Not checked by me: PR description, Review box (not in this brief's scope).

VERIFIED

## Description pass (PR 233 body)
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body; gh pr checks 233; git diff --stat origin/main...HEAD
Output: Summary, table, age text, Blast radius, decisions, evidence (stored $0.01, budget $0.5, exit 5, "0 min old"), review SHA f263b56 and CI (5 checks pass at 6dbb81d) match the diff and the claims above. Failure: Test plan line "Local gates at `6dbb81d`: `just check` and the parallel scenario unit passed before the rebase" labels a pre-rebase run with the post-rebase SHA; no local gate log at 6dbb81d is recorded (work/gates holds scn1.log, scn2.log only). Stale SHA on a proof. Fix: say "at the pre-rebase head <sha>" or rerun and cite 6dbb81d.
NOT VERIFIED (description only)

## Description pass (re-check)
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body; gh pr checks 233
Output: Local gates line now cites f263b56 (before the clean rebase); other SHAs (6dbb81d evidence, CI, scenario; f263b56 review) right; 5 checks pass. Prior failure fixed.
VERIFIED

## Description pass 2
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body; gh pr checks 233; git diff origin/main -- commands/driver.py orders.py release.py
Output: body unchanged since the re-check; check-point table matches the diff (take/take stack, round, order qa and own add --fix-for, release go); f263b56 (local gates, review) exists, 6dbb81d (evidence, CI, scenario) is the head; 5 checks pass; Known gaps consistent with the diff and this file.
VERIFIED

## Description pass 3
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body,headRefOid; gh pr checks 233; grep -rn "307\|59\.9" work/measure.md work/verifier
Output: head matches; 5 checks pass; runs 1.45/1.37/1.50 s and median 1.45 s match measure.md; SHAs f263b56/6dbb81d right; Known gaps no longer lists the measure, consistent. Failure: the body states "307 transcript files totalling 59.9 MB" as fact, but measure.md says "see counts below" and holds no count (grep finds 307 and 59.9 only in pr-body.md); no proof in verify.md, gates or evidence. Fix: add the count command and output to measure.md, or narrow the claim.
NOT VERIFIED (description only)

## Description pass 4
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body,headRefOid; grep -n "47\|21 MB" 03-change-spec.md; grep -n "count" work/measure.md
Output: head matches; runs 1.45/1.37/1.50 s and median 1.45 s match measure.md. Failure: the body says the set is "larger than the eval run the specification names (47 files, 21 MB)", but 03-change-spec.md names no 47 files or 21 MB (grep finds none), and measure.md gives no count of the measured set ("see counts below", none below); the 47/21 MB figure is only in measure.md's own text. The "larger" claim has no counted proof. Fix: add the file count and size of the measured set to measure.md, and cite the eval report (not the specification) as the source of 47 files / 21 MB, or drop the comparison.
NOT VERIFIED (description only)

## Description pass 5
Head: 6dbb81d012f5939a0ac60a5f5a3ade50e92428f9
Command: gh pr view 233 --json body,headRefOid; gh pr checks 233; git diff --stat origin/main; read work/measure.md
Output: head matches; the cost line claims only the median 1.45 s (runs 1.45/1.37/1.50 s), Windows, at 6dbb81d, interpreter start excluded, on a long batch's own steering transcripts, and that the eval run's record is archived: all in measure.md. No size comparison or file count is claimed any more. Check-point table, Changes list and Known gaps match the diff; SHAs f263b56/6dbb81d right; 5 checks pass. No failure.
VERIFIED (description only)
