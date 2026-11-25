# Verify CR-500 (judge + conflicts)

Head: d05934da38e5cf43bee59c586121e687a493165e

All claims judged at d05934da (git 2.56.0.windows.4, worktree of the CR).

1. New tests green. Command: `uv run --no-sync --project . python -m pytest skills/chantier/scripts/cli/tests/test_judge.py .../test_conflicts.py .../test_scenario_coverage.py -q`
   Output: `48 passed in 20.79s`. Collected: test_judge 26, test_conflicts 21 (47 together): matches the PR body.
2. `judge` for real (scenario unit parallel, `just scenario --unit parallel`, log work/verifier/scenario-parallel.log): `294/294 checks`. Transcript shows:
   - `judge CR-101 --epoch 1` exit 0: `ask: ready-to-merge CR-101 fix-login-timeout <pr link>`, then the `handed back:` line, then `decide: send it with ... the merge is the user's`; asks unchanged (scenario check passed).
   - `judge CR-101 --record "scenario: one sentence" --epoch 1` exit 0: `[foreman->chief-of-staff] ask A-1: <ask> | note: scenario: one sentence`; status/asks checks passed.
   - `judge CR-103 --epoch 1` (queued) exit 2: `judge CR-103: CR-103 is queued, not handed back; nothing to word yet; `status` shows the batch`.
3. `conflicts` for real (`just scenario --unit series-deps`, log work/verifier/scenario-series-deps.log): `85/85 checks`. Transcript shows exit 0 with `1 in conflict`, `CR-106 x CR-105: conflict in shared.py; noted`, `next: asks "conflict CR-106 early-cmd-second with CR-105 early-cmd-first: shared.py; switch to a stack?"`; second run `skipped: already noted`, no next line; in the stack batch `conflicts: not run: batch-10 is a stack batch ...`, no note; no ref moved, no ask recorded (scenario checks).
4. Epoch checks (missing exit 2, stale exit 3), blocked and in-stack no-ask, `--record` refusals with unchanged bytes, old/unparseable git refusal (`2.37.1`, `2.37.1.windows.1`, unparsed) and `2.56.0.windows.4` parsing to (2,56,0): covered by the passing tests of claim 1 (read in commands/judge.py, commands/conflicts.py, core/git.py: refusals precede any write; git version checked before the mode).
5. Review box: `$CHANTIER log CR-500` holds the Driver note `r2 approved at d05934da`.
6. PR 483 description (work/pr-body.md): consistent with the diff (judge, conflicts, git helpers, public gaps/owed, scenario steps, AGENTS.md). Autonomous decisions and Known gaps name the deviations (`--record` prints only asks' lines; missing-ref exit 1 as not run; merge-tree unproved on CI runners). `just test` seconds stated (base 154.6 s, head ~172 s). No images.
7. Unproved, as the spec said: the merge-tree form on the CI runners' git (only local 2.56.0 run). CI and the long gate are the Driver's.
Note (not a failure): test_conflicts runs ~19 s alone against the spec's estimate of +1.5 to +3 s; the PR states the measured whole-suite figures.

VERIFIED
