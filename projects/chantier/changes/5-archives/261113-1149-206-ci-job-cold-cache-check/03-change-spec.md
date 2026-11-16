# A change that adds or changes a CI job proves it once with a cold uv cache before the push

## Goal

Batch-14's retro: CR-191 added the CI job `eval-dry-run` (`.github/workflows/ci.yml`). Its long
gate passed on the Driver's machine, and the job was red at its first run on `ubuntu-latest`:
`evals/kit/dry_run.py` calls `uv lock --offline`, which reads the registry from uv's cache, and the
runner's cache was empty. A full round and a CI cycle were spent on a fault one local run would
have shown (the fix is commit `27c1539`, the step "Warm the uv cache with the sandbox's registry
packages" before `just eval-dry-run`).

A developer's machine and a CI runner differ in state, not only in system: the local uv cache is
warm, the runner's is empty at each run. This CR makes that difference looked at, in two places:

1. **This repository's rules** (not a card): a change that adds a CI job, or changes the steps of
   one, runs that job's work steps once locally, in the workflow's order, with a fresh empty uv
   cache, before the push; the output is the Verifier's evidence, quoted in the PR body.
2. **The Spec-writer card**, for every project, naming no tool: a specification that adds or
   changes a CI job names the environment the job runs in and the evidence that proves the job
   before the push.

Text only: no recipe, no CLI change, no test.

## What changes

### 1. `CONTRIBUTING.md`, section "Daily work"

In the bullet list after the `just mod` / `tsc` paragraphs, next to the bullet that ends
"A change to the eval kit (`evals/kit/`) runs `just eval-dry-run`, as
[Changing the kit](evals/README.md#changing-the-kit) says.", add one bullet (or extend that one;
the Driver chooses, in the style of the surrounding text) that says:

- A change that adds a CI job to `.github/workflows/`, or changes the steps of one, runs that
  job's steps once on the local machine before the push, in the workflow's order, with
  `UV_CACHE_DIR` set to a new empty folder (the same folder for every step of that run; outside
  the repository). A runner's uv cache is empty at each run and the local one is warm: a step that
  reads the cache passes every local gate and fails at its first CI run.
- The steps repeated are the job's `run:` steps that do the job's work, a warm-up step included
  (such as the one before `just eval-dry-run`), which is so proved. The actions
  (`actions/checkout`, `astral-sh/setup-uv`, `extractions/setup-just`) and the steps that only set
  up the runner's machine are not repeated: above all the git identity step, whose
  `git config --global` must never touch the developer's own configuration.
- The output is the Verifier's evidence (`work/verifier/evidence/`), quoted in the PR body.
- A change that touches no CI job's steps does not owe it: a cold run downloads everything again.
- The cold cache is the only local proof. Other differences with the runner (its system, the tools
  installed there) are proved by CI alone; the specification names them.

### 2. `evals/README.md`, section "Changing the kit"

Add one bullet to the list, after the first one ("A change to `evals/kit/` passes
`just eval-dry-run` at its pushed head…"), that states the same rule in short and points to
`CONTRIBUTING.md` ("Daily work") for the full text: a kit change that adds a CI job or changes the
steps of one also runs that job's work steps once with `UV_CACHE_DIR` set to a new empty folder,
before the push, its output kept as the Verifier's evidence and quoted in the PR body. The
existing bullets are unchanged.

### 3. The Spec-writer card, `skills/chantier/references/spec-writer.md`

Generic text, for any project: it names no tool (no `uv`, no `just`, no GitHub Actions).

- **Input**, after "Read the code the CR touches, read-only, to name real files, functions and
  commands.": when the CR adds or changes a CI job, read the project's CI files too, read-only, to
  name the environment the job runs in. What the CI files and the answers do not give goes in the
  list of open questions (the card's last paragraph already says a point left open is not the
  Spec-writer's to decide).
- **Output**, a new bullet in the list "A rich specification holds:", before "The evidence that
  proves it": when the CR adds or changes a CI job, the environment that job runs in (its system,
  and what is absent there that the local machine has: caches, tools, credentials, network
  state), the evidence that proves the job before the push as the project's rules ask for it, and
  which of those differences only the job's first CI run can prove.

The agent files `agents/spec-writer.md` and `com.github.copilot/agents/chantier-spec-writer.agent.md`
are not changed: the contract lives in the card.

## Decisions carried from `02-answers.md`

| Answer | Where it lands |
| --- | --- |
| Any change that adds a CI job, or changes the steps of one, owes the cold-cache run (not eval-kit changes only) | §1, §2 |
| An ordinary change (no CI job touched) does not owe it | §1 |
| What runs: the job's own steps, in the workflow's order, in one fresh empty `UV_CACHE_DIR`; a warm-up step is run too, and proved | §1, §2 |
| Which steps: the `run:` steps that do the job's work, warm-up included, in order; the actions and the runner-setup steps (the global git identity above all) are skipped | §1 |
| The output is the Verifier's evidence and the PR body quotes it | §1, §2 |
| The rule lives in this project's rules (`CONTRIBUTING.md` "Daily work", `evals/README.md` "Changing the kit"), not in a card | §1, §2 |
| The Spec-writer card gains one generic line (environment: system, what is absent; the evidence before the push), naming no tool | §3, Output |
| The Spec-writer reads the environment from the CI files, read-only; what it cannot find is an open question | §3, Input |
| The local proof is the cold cache only; other differences are named so the Driver knows CI is their only proof | §1, §3 |
| No recipe (`just ci-cold …`), no structure test: text only | Out of scope |
| Gates: `just check` and `just scenario` (for the card's line) | Evidence |

## The environment of this repository's CI (for reference)

Read from `.github/workflows/ci.yml` at this specification's writing: three jobs, each starting
with `actions/checkout@v4`, `astral-sh/setup-uv@v6`, `extractions/setup-just@v3` and a step
"Git identity for the test repositories" (`git config --global user.name/user.email`):

- `check`: `just check` on `ubuntu-latest`, `macos-latest` (runner `macos-15-intel`,
  `continue-on-error`) and `windows-latest`.
- `scenario`: `just scenario` on `ubuntu-latest`.
- `eval-dry-run`: the warm step `uv lock --refresh --dry-run --directory evals/kit/sandbox`, then
  `just eval-dry-run`, on `ubuntu-latest`.

On each runner the uv cache is empty at the start; the local cache is warm. This CR changes none of
them.

## Out of scope

- A new `just` recipe or CLI tool that empties the cache: one measured case does not justify one
  (AGENTS.md: a new tool comes from measured cost).
- A structure test for the new text.
- Emulating the runner (a container, `act`): only the cache is cold.
- Differences of system (Linux on CI, Windows locally) and of installed tools: CI stays their
  proof; a specification names them.
- Changing `evals/kit/dry_run.py` or the CI jobs: the warm step of `27c1539` stays.
- The Driver, worker, Inspector or Verifier cards: the rule is this project's, read through
  `$CHANTIER rules`; only the Spec-writer card changes.
- The agent files of either host.

## Evidence

This CR adds or changes no CI job, so it does not owe the cold-cache run itself.

- `just check` at the pushed head, passing (Linux, macOS and Windows in CI).
- `just scenario` at the pushed head, passing: AGENTS.md asks for it on a change to the cards.
- The diff touches only `CONTRIBUTING.md`, `evals/README.md` and
  `skills/chantier/references/spec-writer.md`: `git diff --stat origin/main...HEAD` at the pushed
  head, quoted in the PR body.
- A read of the three new passages, quoted in the PR body: the rule (who owes it, which steps run
  and which are skipped, the fresh `UV_CACHE_DIR`, the evidence), and the card's two additions,
  with no tool name in the card (`rg -n "uv|just|GitHub Actions"
  skills/chantier/references/spec-writer.md` prints no new line).
