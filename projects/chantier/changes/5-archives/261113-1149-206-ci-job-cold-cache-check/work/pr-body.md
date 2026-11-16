## Summary

A new CI job passed every local gate and was red at its first run: it reads uv's cache offline, the developer's cache was warm and the runner's was empty. A fault that one local run with an empty cache would have shown cost a whole fix cycle.

This PR writes the lesson down in two places: this repository's contributing rules (a change that adds a CI job or changes the steps of one runs that job once locally with an empty uv cache before the push, and quotes the output), and the guidance for writing a change specification, for any project (a specification that adds or changes a CI job names the environment the job runs in and the evidence that proves it before the push). Text only.

## Deliverables

What changes, by file:

| File | Addition |
| --- | --- |
| `CONTRIBUTING.md`, "Daily work" | The rule: who owes the cold-cache run, which steps run and which are skipped, a fresh `UV_CACHE_DIR`, the output kept as evidence |
| `evals/README.md`, "Changing the kit" | The same rule in short, pointing to `CONTRIBUTING.md` |
| `skills/chantier/references/spec-writer.md` | Input: read the CI files, read-only. Output: the job's environment, the proof before the push, what only the first CI run proves. No tool is named |

Choices: only the cache is made cold locally (a runner's system and installed tools stay proved by CI alone); the actions and the runner-setup steps are not repeated, above all the global git identity step, which must never touch a developer's own configuration; no recipe, no CLI tool, no test.

## Blast radius

Grade: **1**. Documentation and one card's text; a plain `git revert` restores the previous text.

## Autonomous decisions

- The new `CONTRIBUTING.md` text is a separate bullet with four sub-bullets rather than an extension of the eval-kit bullet: it applies to any CI job, not to the kit alone.

<details>
<summary>Details</summary>

## Changes

- `CONTRIBUTING.md`: one bullet and four sub-bullets in "Daily work".
- `evals/README.md`: one bullet in "Changing the kit".
- `skills/chantier/references/spec-writer.md`: two sentences in Input, one bullet in Output.

## Human decisions

- Any change that adds a CI job, or changes the steps of one, owes the cold-cache run, not eval-kit changes only; an ordinary change that touches no CI job does not.
- The run repeats the job's own steps in the workflow's order, in one fresh empty cache folder; a warm-up step is run too, and so proved. The actions and the runner-setup steps (the global git identity above all) are skipped.
- The output is kept as the verification evidence and quoted in the PR body.
- The rule lives in this repository's own rules, not in a card.
- The specification-writing guidance gains one generic line (the job's environment and the proof before the push), naming no tool, and reads the environment from the CI files, read-only; what it cannot find is an open question.
- The cold cache is the only local proof; other differences with the runner are proved by CI alone.
- No new recipe or tool, no structure test: text only.

## Impacts

No visual change. A contributor who touches a CI job's steps now owes one cold-cache local run; a specification for a CI change now states the job's environment.

## Test plan

- [x] New or changed tests: none, no behaviour change
- [x] Local gates at `f1fb10d`: `just check` passes; `just scenario` carried from `7d52066`: patch unchanged; the long gate runs once at the top of the stack, PR 152
- [x] Evidence at `f1fb10d`: `git diff --stat origin/main...HEAD` shows only the three files; no added line of the card names `uv`, `just` or GitHub Actions

  ```text
   CONTRIBUTING.md                           | 14 ++++++++++++++
   evals/README.md                           |  4 ++++
   skills/chantier/references/spec-writer.md |  8 +++++++-
   3 files changed, 25 insertions(+), 1 deletion(-)
  ```

- [x] Review: approved at `7d52066` (carried to `f1fb10d`: patch unchanged by the restack, apart from one context line)
- [x] Verified at `f1fb10d`
- [x] CI green at `f1fb10d`

## Internal references

- CR-206 ci-job-cold-cache-check

</details>
