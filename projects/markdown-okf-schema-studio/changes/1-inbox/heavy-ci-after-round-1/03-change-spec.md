# Heavy CI after round 1 of a CR adding visual or real-window tests

The CR has no tracker issue (origin: the batch-07 retro, 2026-11-21).

## Goal

In batch 07, CR-439 needed 5 rounds, CR-445 6 and CR-441 4. The extra rounds were visual and
integration tests that failed only in CI: on Windows, `just preflight` runs only the static stage
and skips the visual, integration, report and gallery stages (justfile, `preflight` recipe: "visual,
integration, report and gallery stages skipped on Windows; CI runs them"). The Driver saw those
failures only at the end, when the pull request was opened.

After this change, a CR that adds or changes visual, integration or stress scenarios pushes its
branch as a draft pull request after round 1 and dispatches the heavy CI, so round 2 starts
with the real CI result instead of finding it in the last round.

## What changes

One file changes, in the Studio repository:
`.agents/guidelines/change-requests-lifecycle.guidelines.md` (the process guideline, which the
Driver reads) (hc-Q1). Nothing else changes: not chantier's `chantier.yaml` or cards (hc-Q1: the
rule is specific to Studio), not `.github/workflows/ci.yml`, not the `justfile`, not
`ci.guidelines.md`.

### New bullet in "Project rules on top of chantier's steps"

Add one bullet, **Early heavy CI**, in the section "Project rules on top of chantier's steps",
between the **Pull request** and **CI** bullets. Its content, in the guideline's style (short
sentences, plain English, no CR numbers, no batch names):

1. Scope (hc-Q2): a change request that adds or changes visual, integration or stress scenarios.
   In practice its round 1 diff touches `test/visual/`, `test/integration/` or the stress list
   `test/shared/stressPlan.ts`, or its `03-change-spec.md` asks for such scenarios. Other change
   requests keep the current steps.
2. Step (hc-Q2): after round 1's commit, whatever the round's review verdict, the Driver rebases
   on `origin/main`, pushes the branch and opens the draft pull request as the **Pull request**
   bullet says, then dispatches the heavy run in its own command:
   `gh workflow run ci.yml --ref <branch> -f heavy=true`.
3. Stack mode (hc-Q4): for a change request in a stack, the stack driver does this step after
   round 1. It pushes that change request's branch, opens its draft pull request against the
   branch below, and dispatches the heavy run on that branch. The bullet says that this is the one
   exception to "coder and review stop at the commit" of "Parallel Change Requests Orchestration",
   which stays unchanged. Later restacks push with `--force-with-lease` as today and do not dispatch
   the heavy run again (hc-Q3).
4. Reason, in one sentence: on Windows `just preflight` runs only the static stage, so visual
   and real VS Code window failures appear only in CI.
5. Reading (hc-Q2): round 2 starts by reading that run (`gh run list --workflow ci.yml --branch
   <branch> --event workflow_dispatch`, then `gh run view <id> --log-failed` for a red job).
   A failure goes into round 2 as the **CI** bullet says (a product or test failure becomes part
   of the round with the log excerpt; an infra failure is re-run once; a flake is named and filed).
   A red `stress` job is advisory (ci.guidelines.md, rule 12) but counts as a flake to fix.
6. Cost (hc-Q3): one early heavy run per such change request. Later rounds do not dispatch the
   heavy run again. Each push to the draft pull request still runs the pull request CI (static
   and visual jobs, `report` with the real VS Code stage skipped), as it does today.
7. Nothing else changes: the round limit (3, all causes together) still applies, and the early
   push does not mark the pull request ready; **Verify** still comes before ready. Rule 13 of
   [ci.guidelines.md](ci.guidelines.md) still holds: a change to the extension host, the webview or
   the real-window tests still gets a heavy run before merging.

### The environment the heavy run uses (no change to the workflow)

The step uses the existing `workflow_dispatch` input `heavy` of `.github/workflows/ci.yml`. On a
branch dispatch:

- Jobs: `static` (ubuntu-latest), `static-windows` (windows-latest), `visual` (ubuntu-latest,
  Playwright Chromium against the mock host, `just dev-ci visual`), `integration` (ubuntu-latest,
  a real VS Code window under `xvfb-run -s "-screen 0 2600x1440x24"`, `just ci-integration`, job
  timeout 30 min, test step 20 min, then `just ci-hang-dump`), `stress` (ubuntu-latest, real
  windows, `just ci-stress`, 12 rounds by default, advisory), `report` (`just ci-report all`),
  `gallery` (runs only when `integration` and `report` succeed; the default `gallery=true` is kept),
  `checks`. `release-check`, `tag-release`, `release` and `pages` do not run (they are `main` push
  only).
- What the local Windows machine has that this run does not: the Windows display and the user's
  VS Code, a warm `node_modules`, `.vscode-test` and Playwright cache (CI installs from the lock
  files and the archive caches), and the local `gh` login (the workflow uses its own
  `contents: read` token). What the run has that `just preflight` on Windows does not: Linux, Xvfb
  and the visual, integration, stress, report and gallery stages.
- Healthy duration: about 10 min for `integration` and 16 min for `stress` (the input's
  description); the Driver reads the run when round 2 starts or when the run ends, whichever is
  later.

## Decisions carried

- hc-Q1 (confirmed by the owner, "Studio's CR guideline"): the rule goes in Studio's process guideline
  `.agents/guidelines/change-requests-lifecycle.guidelines.md`, not in `chantier.yaml`: it is
  specific to Studio (Windows preflight skips visual, integration and report).
- hc-Q2: a CR that adds or changes visual, integration or stress scenarios pushes its branch
  (draft PR) after round 1 and dispatches `gh workflow run ci.yml --ref <branch> -f heavy=true`;
  the next round reads that run. Other CRs keep the current steps.
- hc-Q3: one early heavy run per such CR; no extra run on every round.
- hc-Q4 (owner, "Push, draft PR and heavy run"): in a stack, the stack driver pushes that CR's
  branch after round 1, opens its draft PR against the branch below, and dispatches the heavy run.

## Out of scope

- Any change to `.github/workflows/ci.yml`, the `justfile`, `ci.guidelines.md` or the other project
  guidelines. In particular no role name and no link to the process guideline may go in a project
  guideline: `test/build/test_guideline_isolation.py` refuses both.
- Any change to chantier (its cards, `chantier.yaml`, the Driver card).
- Running visual or integration stages locally on Windows, or changing what `just preflight` skips.
- Automating the dispatch (a hook, a CLI command): the Driver runs the command.
- Changing the round limit.

## Commit and pull request

- One commit, type `docs`, no scope (scopes apply only to `fix` and `feat`,
  `git-commit-allowed-scopes.md`), for example `docs: dispatch the heavy CI after round 1 of a
  change request adding real-window tests`. The commit names explicit paths.
- No `CHANGELOG.md` line (not `feat` or `fix`); the pull request's Changelog checkbox says "No
  user-facing change". No SwRS is touched: the requirements check finds no requirement (process
  text only, no `src/` or test change).
- The pull request body keeps to [pull-request.guidelines.md](pull-request.guidelines.md): no
  internal IDs (no CR numbers, no batch, no planning link). Impacts: "No visible change: process
  documentation only".

## Evidence

The check reads the shipped guideline from the repository at the head under test, not a copy.

1. `git diff --stat origin/main...HEAD` lists only
   `.agents/guidelines/change-requests-lifecycle.guidelines.md`.
2. `grep -n "Early heavy CI" .agents/guidelines/change-requests-lifecycle.guidelines.md` finds the
   bullet inside "Project rules on top of chantier's steps", between **Pull request** and **CI**.
3. In the same file at the head, the bullet contains the exact command
   `gh workflow run ci.yml --ref <branch> -f heavy=true`, the three paths `test/visual/`,
   `test/integration/` and `test/shared/stressPlan.ts`, the words "draft", "round 1" and
   "round 2", and says that later rounds do not dispatch the heavy run again. It also has the
   stack sentence: the stack driver pushes the branch after round 1, opens the draft pull request
   against the branch below, and dispatches the heavy run.
4. Each decision hc-Q1..hc-Q4 maps to a sentence of the bullet (the Verifier quotes it).
5. `uv run --group docs --group release --group requirements pytest test/build/test_guideline_isolation.py`
   passes (no project guideline gained a role name or a link to the process guideline).
6. `just preflight` passes (on Windows, the static stage: `just ci-static`).
7. The command in the bullet is valid against the workflow at the head:
   `grep -n "heavy:" .github/workflows/ci.yml` shows the `workflow_dispatch` input `heavy`
   (boolean). No dispatch is needed to prove this CR, which changes no workflow and no test.

No host or default matrix: the change is process text and does not depend on a host or a setting.
