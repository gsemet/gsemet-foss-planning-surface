# 044 — flaky-linked-target-watcher (P1)

From backlog `P1/flaky-linked-target-watcher` (`01-intent.md` here).

## Problem

"Preview editing integration failed: Error: Timed out waiting for the linked-target watcher to
deliver the event of the save." (PR #21, run 39848594435, docs-only change, so a flake.)

## Decisions (user grill, 2026-10-23)

1. Find the root cause (watcher event ordering / latency under xvfb, or a race in the product),
   fix it at the cause. Never raise the timeout, never retry (CI rule 12).
2. Proof: 20 repetitions locally with a real VS Code (`just ci-stress`, add the scenario to the
   stress plan) under `requests/WINDOW-TESTS.lock`, one window run at a time across CRs (CR 043
   also uses it), plus one run of the manual heavy CI job once CR 043 has landed it (before that:
   the current CI integration job). If CR 041 already fixed it and it does not reproduce: prove it
   (20 green rounds + reasoning on the code path) and close with that evidence.
3. Speed: driver, coders, reviewers on Opus; reviewer checks the round diff; ready as soon as the
   required `checks` job is green and the PR is mergeable. Rounds: 3.
4. PR written for an external reader (prd-workflow "PR body for an external reader").

## Decision 5 (main session, 2026-10-23 16:40)

Coder r1: root cause already fixed by d53b756 (direct watch of the linked target; all 5 failures
ran without it, 13+ integration jobs with it passed). r1 adds a readiness wait + diagnostics;
stress `linked-target-save` 20/20 locally. The full local suite stops earlier on two unrelated
failures (checkboxToggle undo, slash-menu after line break): those belong to CR 048, not 044.
Proof for 044 = local stress 20/20 + one manual heavy CI run green (integration + stress). Go on
with review r1, commit, PR (explain in the PR that the cause was fixed earlier and this PR makes the
test wait on a readiness signal and print diagnostics).
