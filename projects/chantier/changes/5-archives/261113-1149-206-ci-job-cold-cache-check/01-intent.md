# A change that adds a CI job proves it once with a cold uv cache before the push

## The request

Batch-14's retro: CR-191 added the CI job `just eval-dry-run`. Its long gate passed on the
Driver's machine, and the job was red on `ubuntu-latest`: the dry run calls `uv lock --offline`
(`evals/kit/dry_run.py`), which reads the registry from uv's cache, and the runner's cache was
empty. One round was spent on it (the fix is commit `27c1539`: a "warm the uv cache" step in
`.github/workflows/ci.yml`). The request asks for two things: an eval-kit change that adds a CI
job runs its recipe once locally with an empty uv cache (`UV_CACHE_DIR` set to a fresh folder)
before the push, and the Spec-writer names the CI environment when a specification adds a job.

## The problem

- A developer's machine and a CI runner differ in state, not only in system: the local uv cache
  is warm after months of work, the runner's is empty at each run. A recipe that depends on that
  state passes every local gate and fails at its first CI run.
- Nothing asks for the difference to be looked at. `evals/README.md`, "Changing the kit", asks
  for `just eval-dry-run` at the pushed head, which runs with the warm cache. A specification
  that adds a job says what the job runs, not where: the Spec-writer card
  (`skills/chantier/references/spec-writer.md`) has no line about a CI job.
- The cost is a full round and a CI cycle each time, for a fault one local run would show.

## What would fix it

1. A project rule of this repository, where its contributors and agents read it
   (`CONTRIBUTING.md` and `evals/README.md`, "Changing the kit"): a change that adds a CI job
   runs that job's steps once, in the workflow's order, with `UV_CACHE_DIR` set to a fresh empty
   folder, before the push; the output is evidence.
2. A line in the Spec-writer card, for every project: a specification that adds or changes a CI
   job names the environment the job runs in (the system, and what is absent there: caches,
   tools, credentials, network state) and the evidence that proves the job before the push.

## Out of scope

- A new `just` recipe or CLI tool that empties the cache: one measured case does not justify one.
- Emulating the runner (a container, `act`): only the cache is cold.
- Differences of system (Linux on CI, Windows locally): CI stays the proof for those; the
  specification names them so the Driver knows what a local run cannot prove.
- Changing how `dry_run.py` or the CI job works today: the warm step of `27c1539` stays.
