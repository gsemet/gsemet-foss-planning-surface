# Eval kit: an end-to-end dry run as evidence

## Goal

The batch-13 retro (2026-11-12) found that four blockers of the `full` campaign got past CR-189
reproducible-evals' Inspector and Verifier. An independent review found them only after the
merge. Each checker had judged one piece alone (the judge, the setup, the audit), and no one had
run the pieces together the way a campaign does. The four blockers:

1. The audit counted the merged release PR as a stray merge (C12). The CLI clears a release's
   `pr` when it merges.
2. The reset's verify failed on `refs/pull/*`, which GitHub keeps forever.
3. The operator merged with a raw `gh pr merge`, which the host may refuse.
4. The release CRs did not name `uv.lock`, so the version bump left the lock stale and
   `uv run --locked pytest -q` failed.

This CR gives the eval kit a **dry run**: one campaign run end to end with no model call and no
write to GitHub. It covers the reset, the setup, a staged run of what a campaign leaves behind,
then `audit.py --sandbox` and the judge on that result. The dry run passes on a run that follows
the rules. On each planted fault it fails and names the criterion. It is the evidence every
eval-kit change carries. The project's rules require it, together with an independent review
before the merge.

No `issue:` line: the CR comes from a retro, not from a tracker issue.

## Base

Work from `origin/main` (d6271d4 or later), not from the main checkout's working tree, which is
behind. The kit as it stands there: `evals/kit/setup.py`, `sandbox.py` (`build`, `reset`,
`merge`, the constants `REPO` and `URL`), `audit.py` (`--sandbox`, `batch_prs`,
`sandbox_checks`, `judge_rows`), `judge.py` (`feature`, `release`), `forge.py` (claude-planted's
local forge), `sandbox-crs/`, `sandbox-judge/` and `sandbox.json`.

## What changes

### 1. The dry run: `evals/kit/dry_run.py`

```text
uv run --no-project python evals/kit/dry_run.py [--case <name>] [--keep]
```

- Standard library only. It runs on POSIX and on Windows, with UTF-8 everywhere, like the rest
  of the kit. Exit codes follow `judge.py`: 0 every case behaved as expected, 1 a case did not
  (named), 2 usage, 4 external (git or uv failed: the tool's own text is printed).
- Everything happens in one new temporary folder, which is removed at the end unless `--keep` is
  given (then its path is printed). That folder holds a local bare repository standing for the
  sandbox's origin, the workspace, its `.run.json`, the fake forge's state and the staged
  transcripts.
- **No GitHub, no model.** Before any call, the dry run:
  - rebinds `sandbox.URL` to the local bare repository, in its own process only. `sandbox.REPO`
    keeps its value, and no command-line argument or environment variable of `setup.py`,
    `sandbox.py`, `audit.py` or `judge.py` changes the repository. Their "the repository is a
    constant" rule stays true for every user.
  - puts the dry run's fake `gh` first on the `PATH` of its own environment and of every process
    it starts.
  - sets `GIT_ALLOW_PROTOCOL=file` in that environment, so that any git call that would reach
    a network URL fails instead.

  It never starts `claude` and never prices a real call.
- **Output:** one line per case (`ok <case>: <what was shown>`, or `FAIL <case>: <expected> /
  <got>` followed by the lines that matter from the tool, at most ten), then
  `dry run: <n> of <m> cases as expected`. With `--case <name>`, only that case runs, after the
  steps it needs.

### 2. The sandbox's GitHub, played locally: `evals/kit/sandbox_forge.py`

This is a fake `gh` for the dry run only. The dry run writes its launcher in its temporary
folder: `gh` with `exec python` on POSIX, `gh.cmd` on Windows, as `setup.py` already does for
`forge.py`. It answers what the kit asks of the real forge, with the JSON fields the kit reads:

- `auth status`: logged in, with a token-scopes line that holds `workflow`.
- `repo view --json defaultBranchRef`.
- `pr create`, `pr view` (`number,state,title,isDraft,baseRefName,autoMergeRequest,
  statusCheckRollup,headRefOid,mergedAt,headRefName`), `pr list --state open|merged|all`,
  `pr checks`, `pr merge --rebase --match-head-commit`, `pr close`.
- `release create|list|view|delete`.

Like GitHub, it writes `refs/pull/<n>/head` in the bare origin when a PR opens or its head moves,
and never deletes those refs. Its CI is real: the long gate `uv run --locked pytest -q` runs on
the PR's head in a fresh clone, once per commit, and gives a `statusCheckRollup` of `SUCCESS`
or `FAILURE`. The staged run can also mark a head's checks as pending. It refuses any `--repo`
other than `sandbox.REPO`.

`forge.py` (claude-planted's forge) does not change. It keeps refusing a close and anything else
it refuses today.

**Windows:** Python's `subprocess` finds only an `.exe` for a bare `gh`, so it does not see the
fake's `gh.cmd`. The kit therefore resolves the tool it runs with `shutil.which` (which honours
`PATHEXT`) wherever it calls `gh`: `sandbox.run` and `sandbox.gh`, `setup.py`'s `gh auth status`,
`audit.run_cmd` and `judge.run`. With the real `gh` the behaviour is unchanged. A tool that is
not found keeps today's message.

### 3. What the dry run plays: the clean run

The clean run is one case, `clean`. Its steps:

1. **Base.** `sandbox.build` into a temporary repository. Its SHA-1 must equal `sandbox.json`'s
   base. The base is pushed to the local origin's `main`.
2. **Leftovers of an earlier run, then the reset.** The dry run stages what a previous run
   leaves on the sandbox:
   - a merged PR, an open PR, a closed PR, a branch, a tag and a release, with PR titles starting
     `[eval 3 <date> full]`;
   - the `refs/pull/*/head` of each of those PRs.

   Then it runs `sandbox.py reset`, which must print a plan and change nothing, and `reset --yes`
   (in-process, through `sandbox.main([...])`). Expected: the reset ends with `sandbox reset:
   main at <base>`, while `refs/pull/*` are still on the origin. The preconditions of `reset` are
   met by the fake and by the run's environment, never skipped: `gh auth status` with the
   `workflow` scope, `gh repo view`, and a git credential helper set in that environment only
   (`GIT_CONFIG_COUNT`), never in the user's config.
3. **Setup.** `setup.sandbox_main("full", <workspace>)`, in-process. Expected:
   - the run number is 4, one more than the leftovers' 3, and the prefix is
     `[eval 4 <today> full]`;
   - the clone's HEAD is the base;
   - `chantier init` and `uv sync --locked` passed;
   - the frozen CRs of `full` are in `.agents/changes/3-ready/` with their "Eval run" section;
   - `<workspace>.run.json` is written;
   - `.claude/settings.local.json` holds an allow rule, in both `Bash(...)` and `PowerShell(...)`
     forms, that matches the exact merge line setup printed followed by a PR number (the
     Claude Code rule form `<prefix> *`). This check is the dry run's own.
4. **A staged batch.** Through the real CLI (`$CHANTIER` as setup prints it, run from the
   workspace), a scripted Foreman steers one parallel batch of two CRs:
   - **One frozen feature CR of `full`'s first batch**, implemented by a reference solution kept
     in the kit, `evals/kit/dry-run/<slug>.patch`, so that its hidden tests pass. Use
     `delete-item`, unless another frozen CR of that batch is clearly smaller to implement; the
     README names the one chosen. The patch stays in the kit like the hidden tests. It is never
     copied into a real campaign's workspace and never pushed to the real sandbox.
   - **The release `release-v0-2-0`**, made as its frozen CR says, `uv.lock` included.

   The scripted agents do what a rule-following agent does: `open` (`--release 2 --mode parallel
   --slots 2 --budget <n> --default-branch main`), `take` and `round` with their epoch, a
   worktree and branch per CR, an explicit `git add -- <paths>`, a first push with `-u` and a
   rewrite pushed with `--force-with-lease`, a PR whose title starts with the run's prefix, `gh pr
   checks`, `gate`, `verdict <cr> VERIFIED`, `ship` and `handback ready`. The release goes
   through `release go` (an `ask`, then a `go`), `note --draft` for its notes, the release PR,
   the tag pushed to the local origin and `gh release create`. Merges happen as in a campaign:
   - the operator merges the feature PR with `sandbox.py merge <n>` exactly as setup printed it,
     from the workspace, followed by `order merged`;
   - the Foreman merges the release PR (`gh pr merge --rebase`) and records it with
     `order merged --epoch`, so the CLI clears the release's `pr` the way it did in batch-13.

   Then the Foreman removes the merged worktrees and runs `pause`. `scenario/run_scenario.py`
   already scripts a Foreman and Drivers against the real CLI and is the model to follow. The
   dry run may take its approach but does not import from `scenario/`.
5. **Staged transcripts.** The staged batch leaves the Claude transcripts a Foreman batch leaves,
   in a temporary `--projects` folder: the Foreman's own (named by the batch's recorded Foreman
   transcript), and one agent per role the audit expects under it (a CR Driver with its workers,
   a Release driver), with the prompts and the tool calls of step 4. Each prompt starts with
   `chantier <role> for ...`, names its card and `$CHANTIER rules`, and a worker's prompt has a
   `writes:` line. With these, the audit's transcript checks run and pass. Nothing in them is a
   model's output.
6. **Audit and judge.** `audit.py <workspace> --sandbox --projects <staged>` runs as a separate
   process, with the fake `gh` on its `PATH`. Expected:
   - exit 0;
   - `[C12]` PASS, with the release PR counted as the batch's own;
   - `[J5]` PASS for each PR;
   - the judge: the feature CR `pass`, `main` `pass`, the release `pass`. The release judge's
     GitHub-release item says `not run: not the sandbox`, since the origin is a local path, and
     that is not a failure.

   `cost` may print `not measured`, which is not a failure.

### 4. The planted faults: one case each, at least the four of batch-13

Each case starts from the clean run's state (a copy of the workspace, the origin and the fake's
state, or a new staging; the Driver chooses) and plants one fault. It is as expected only when
the named tool fails **and** names the criterion given below. A failure for another reason is
`FAIL` in the dry run.

| Case | Blocker | The fault planted | Expected |
| --- | --- | --- | --- |
| `stray-merge` | 1 | A PR with the run's prefix, not recorded by the batch, merged on the forge after the batch opened | The audit exits 1 with a `FAIL [C12]` line naming that PR's number, while the release PR is still not counted as a stray |
| `reset-leftover` | 2 | After the reset, a branch and a tag pushed back to the origin (the `refs/pull/*` stay) | `setup.py full` exits 2 with "the sandbox is not at its base", naming the branch and the tag, and creates nothing; `reset` plans their deletion; once `reset --yes` has run, setup passes |
| `merge-refused` | 3 | `sandbox.py merge` on a PR with a failed check, on one with a pending check, and on one whose title lacks the prefix | Each exits 2 with `refused: ...; nothing merged`, naming the reason (`not all green`, `pending`, `prefix`), and the PR stays open on the forge |
| `stale-lock` | 4 | The release's head bumps the version in `pyproject.toml`, `shelf.__version__` and `CHANGELOG.md` but not in `uv.lock`, and the forge merges it anyway | The forge's CI on that head is `FAILURE`; `sandbox.py merge` refuses it; the audit exits 1 with a `FAIL [J5]` line on the release PR; and the judge's release row is `fail`, naming the stale lock |

The Driver may add cases. Each one names its criterion the same way.

**Where the kit does not fail as the table says, the kit is fixed in this CR.** One gap is
known: today a stale `uv.lock` makes `judge.pytest` raise `NotRun` (no pytest summary), and the
release judge's `uv run python scripts/release_check.py` may re-lock silently. The judge (feature
and release) must report a stale `uv.lock` at the ref it judges as `fail`, with an item that
names it (for example `FAIL: uv.lock is not up to date at <ref>`), never as `not run`. A stale
lock is the run's fault, not the judge's.

### 5. Proof the dry run catches what batch-13 missed

As one-time evidence in the PR (not a permanent case), the Driver runs the new dry run against
the kit as it was before the fix, `evals/kit/` at d72df44 (in a temporary worktree, with the
dry run and its fake copied in). The `clean` case must fail there at least on the C12 stray
(the release PR), on the reset's verify (`refs/pull/*`) and on the merge (no `sandbox.py merge`).
The PR body quotes those lines.

### 6. A structure assertion for blocker 4's own form

In `skills/chantier/scripts/cli/tests/test_structure.py`, add one assertion to the existing
`test_the_sandbox_campaigns_name_only_frozen_crs_with_hidden_tests`: each frozen release CR
(`evals/kit/sandbox-crs/release-*/03-change-spec.md`) names `uv.lock` in its "Files" list. It
takes no time and catches the text the dry run cannot see.

### 7. `just` and CI

- New recipe in `justfile`:

  ```text
  # The eval kit's dry run: reset, setup, a staged run, the audit and the judge, on a local sandbox; no model, no GitHub
  eval-dry-run:
      uv run --no-project python evals/kit/dry_run.py
  ```

- **`just check`:** the recipe joins `check` (`check: test release-notes eval-dry-run`) only if
  the whole dry run takes under 10 seconds on the Driver's machine and on CI. Otherwise it stays
  a separate recipe, and the PR body gives the measured time as the reason. The setup's
  `uv sync`, the forge's CI and the judge's clones make the separate recipe the likely outcome.
- **CI:** if the recipe stays separate, `.github/workflows/ci.yml` gets one job like `scenario`'s,
  `just eval-dry-run (ubuntu-latest)`, with the same steps (checkout, setup-uv, setup-just, the
  git identity), so the dry run cannot rot unseen. The Driver runs it on its own OS too (Windows
  for this project's main machine), and that output is the Verifier's evidence. If it joins
  `just check`, CI already runs it on the three OSes and no job is added.

### 8. The project's rules

- **`evals/README.md`**, section "The kit":
  - rows for `kit/dry_run.py` (the dry run: reset, setup, a staged run, audit and judge, on a
    local sandbox, with its planted faults; no model, no GitHub), `kit/sandbox_forge.py` (the
    sandbox's GitHub played locally, for the dry run only) and `kit/dry-run/` (the reference
    solution of the staged CR);
  - a new subsection **"Changing the kit"** that states:
    - A change to `evals/kit/` passes `just eval-dry-run` at its pushed head. Its output is the
      Verifier's evidence (`work/verifier/evidence/`), quoted in the PR body.
    - A new campaign behaviour, or a fault a run found, gets its case in the dry run in the same
      PR.
    - One line of guidance: an eval-kit change gets an independent review of the whole campaign
      path (setup, a run, the audit, the judge) before its merge, by a reviewer that did not
      write it. The dry run does not replace it.
- **`CONTRIBUTING.md`**, "Daily work":
  - in the recipe block, `just eval-dry-run   # the eval kit's dry run: no model, no GitHub`;
  - in the bullet on the eval campaigns, a sentence: a change to the eval kit passes `just
    eval-dry-run` (see [evals/README.md](https://github.com/gsemet/chantier/blob/main/evals/README.md#changing-the-kit));
  - if a CI job is added, the closing bullet's CI list names it.
- `AGENTS.md` does not change. Its line "a change to the docs or the eval kit alone needs none"
  is about `just scenario` and stays true.

## Out of scope

- Any write to the real sandbox (https://github.com/gsemet/chantier-eval-sandbox), any call to
  GitHub, any paid campaign or model call.
- A new review role, a new gate, or a mandatory second-model review before every merge. "The
  independent review runs before the merge" is one line of guidance for eval-kit changes.
- The release judge's GitHub-release item against the real GitHub (`judge.is_sandbox`), Copilot's
  audit, direct mode, a series, a stack, a second batch and `claude-planted`: the dry run stages
  one Foreman-steered parallel batch of `full`'s shape.
- `forge.py`, the runbooks' prompts, `SCORECARD.md` and its rails, the CLI and the cards.

## Evidence

- `just eval-dry-run` at the pushed head, on the Driver's OS (Windows here): every case `ok`,
  ending with `dry run: <n> of <n> cases as expected`. Its output goes in
  `work/verifier/evidence/` and is quoted in the PR body. The Verifier runs it itself.
- `just check` passes on Linux, macOS and Windows (CI), the new structure assertion included.
- If a CI job is added, it is green on the PR.
- §5's run against d72df44's kit, failing on the three named criteria, quoted in the PR body.
- The measured duration of the dry run, and with it the decision on `just check` (§7).
- During the whole run, no network call to github.com from the dry run. The PR body says how it
  was checked: `GIT_ALLOW_PROTOCOL=file`, the fake first on the `PATH`, and the fake refusing
  any other `--repo`.
- `just scenario` is not required: the CLI, the cards and the scenario do not change.

## Decisions taken

Taken by the Chief of Staff's delegation, where `02-answers.md` left the point open:

1. The dry run reaches the local origin by rebinding `sandbox.URL` in its own process. No
   argument or variable of the kit's commands changes the repository.
2. A separate fake `gh` (`sandbox_forge.py`) plays the sandbox's GitHub. `forge.py` stays
   claude-planted's and keeps its refusals.
3. The kit resolves `gh` with `shutil.which`, so a `.cmd` fake is found on Windows. This is
   needed for the dry run to be portable.
4. The staged run is one Foreman-steered parallel batch: one frozen feature CR (`delete-item`
   unless another is clearly smaller) with a reference solution kept in the kit, plus
   `release-v0-2-0`. The staged transcripts let the audit's transcript checks run.
5. The four planted cases are `stray-merge`, `reset-leftover`, `merge-refused` and `stale-lock`.
   A case counts only when the failure names its criterion.
6. A stale `uv.lock` is a judge `fail`, not `not run`. The judge is fixed in this CR.
7. The threshold for "fast" is 10 seconds. Above it, the dry run is a separate `just
   eval-dry-run` recipe, run by its own CI job on Linux.
8. The rules live in `evals/README.md` ("Changing the kit") with a pointer in `CONTRIBUTING.md`,
   and `AGENTS.md` is unchanged.
9. One structure assertion checks that each frozen release CR names `uv.lock`.
10. The run against d72df44's kit is one-time evidence in the PR, not a permanent case.
