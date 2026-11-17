# Answers

Short name: `win-breakout-test`

## 2026-11-17: triage

1. win-breakout-test-Q1: **Fix the pre-existing Windows test failure?** Owner, on CR-336's
   question (open the PR on Linux CI with a separate CR for this test, or fix it first): « 1. oui
   fix ». Filed as its own CR, added to batch-05, automatable (the Driver works from the request
   alone). It is the follow-up of CR-336's long-gate waiver: its own long gate runs
   `just preflight` on Windows with the test fixed.
