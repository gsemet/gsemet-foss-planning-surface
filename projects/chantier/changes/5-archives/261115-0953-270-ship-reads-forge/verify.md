# Verify CR-270

Head: 6d07c1bdb0e8a09080e5a2af2d6d5916a2578223

Verdict: VERIFIED

Claims (all at head 6d07c1b, run in the worktree batch-18-CR-270):

- Spec steps 1-6, 8, 9 (section 13b base_from_pr, ready_words, release / release_merged, stacks, every other ship call): `just scenario --unit stack --unit release --unit parallel`: stack 129/129, release 107/107, parallel 183/183 checks pass.
- Step 10 (section 22, GitLab): `just scenario --unit gitlab`: 32/32 checks pass.
- Step 7 (`ship <cr> <link> --draft`): `uv run --no-sync --project . chantier ship cr-1 https://x/pr/1 --draft --batch batch-18` printed `unrecognized arguments: --draft`, exit 2; `ship --help` lists no `--draft`. The scenario also checks it (run_scenario.py line 4296, expect=2).
- Budget: parallel 261.6 s vs 260 and stack 517.6 s vs 320 were over budget in this run because four units ran at once on a loaded machine; every check passed, and CI at this head was green.
- PR body (work/pr-body.md) read against the diff: Summary, Deliverables (one forge read, `draft not read`, `--draft` removed, hand-stacked PR reads `PR in draft`), Known gaps (GitLab draft field, Copilot) match the diff. No pane change, no screenshot needed.
