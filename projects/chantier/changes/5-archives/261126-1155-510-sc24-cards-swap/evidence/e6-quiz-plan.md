# Evidence 6: the situation quiz, free plan only

No quiz run was made: only `--plan`, which prints the plan and the estimate and stops before the
host check and any model call (`evals/kit/quiz.py`, `play`). Worktree `batch-31-CR-510`,
uncommitted tree (base `88d9ab40`), 2026-11-26, run from the worktree.

The 11 roles with cases under `evals/quiz/`. The three session roles have no shipped model, so
they take `--model` (here `claude-sonnet-5-5`).

## After the swap (the working tree: the boot is `brief`'s output, no manifest)

`just quiz coder conflict-resolver cr-driver debugger demo-explorer release-driver stack-driver
verifier --plan`, exit 0:

```text
plan: coder 3 cases x 3 runs on claude-sonnet-5-5 + 9 judge calls on claude-fable-5-2: ~$3.19
plan: conflict-resolver 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: cr-driver 18 cases x 3 runs on claude-sonnet-5-5 + 54 judge calls on claude-fable-5-2: ~$19.37
plan: debugger 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: demo-explorer 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.06
plan: release-driver 3 cases x 3 runs on claude-sonnet-5-5 + 9 judge calls on claude-fable-5-2: ~$3.23
plan: stack-driver 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.08
plan: verifier 2 cases x 3 runs on claude-sonnet-5-5 + 6 judge calls on claude-fable-5-2: ~$2.13
plan total: 90 runs, ~$32.19 (cap $10)
```

`just quiz chief-of-staff foreman griller --model claude-sonnet-5-5 --plan`, exit 0:

```text
plan: chief-of-staff 17 cases x 3 runs on claude-sonnet-5-5 + 51 judge calls on claude-fable-5-2: ~$19.00
plan: foreman 11 cases x 3 runs on claude-sonnet-5-5 + 33 judge calls on claude-fable-5-2: ~$12.22
plan: griller 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.07
plan total: 87 runs, ~$32.29 (cap $10)
```

## The pre-swap head (`--cards 88d9ab40`, walked by its start manifest)

The same two commands with `--cards 88d9ab40`, each exit 0:

```text
plan: coder 3 cases x 3 runs on claude-sonnet-5-5 + 9 judge calls on claude-fable-5-2: ~$3.27
plan: conflict-resolver 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.09
plan: cr-driver 18 cases x 3 runs on claude-sonnet-5-5 + 54 judge calls on claude-fable-5-2: ~$20.25
plan: debugger 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.09
plan: demo-explorer 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.09
plan: release-driver 3 cases x 3 runs on claude-sonnet-5-5 + 9 judge calls on claude-fable-5-2: ~$3.36
plan: stack-driver 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.14
plan: verifier 2 cases x 3 runs on claude-sonnet-5-5 + 6 judge calls on claude-fable-5-2: ~$2.23
plan total: 90 runs, ~$33.52 (cap $10)

plan: chief-of-staff 17 cases x 3 runs on claude-sonnet-5-5 + 51 judge calls on claude-fable-5-2: ~$26.56
plan: foreman 11 cases x 3 runs on claude-sonnet-5-5 + 33 judge calls on claude-fable-5-2: ~$14.13
plan: griller 1 cases x 3 runs on claude-sonnet-5-5 + 3 judge calls on claude-fable-5-2: ~$1.11
plan total: 87 runs, ~$41.80 (cap $10)
```

## What a real run needs

- Each total is above the default cap (`--max-usd 10`): a run needs a higher `--max-usd`, or one
  call per role. The `cr-driver`, `chief-of-staff` and `foreman` roles exceed $10 on their own.
- No quiz results file of the old cards exists: `git ls-files "evals/results/quiz*"` prints
  nothing at this head, and no `quiz-*.json` is in the surface's `changes/`. The `--against`
  baseline of the F4 gate (child 6's) has to be run too.
- Roles with no case under `evals/quiz/`: qa-driver, inspector, investigator, spec-writer,
  spec-critic, board-griller, retro-critic.
- Quiz under F4: not run (Known gaps).
