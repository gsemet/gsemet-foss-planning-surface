# Heavy CI after round 1 of a CR adding visual or real-window tests

The CR has no tracker issue (origin: the batch-07 retro, 2026-11-21).

## Goal

In batch 07, CR-439 needed 5 rounds, CR-445 6 and CR-441 4. The extra rounds came from visual and
integration tests that failed only in CI. On Windows, `just preflight` runs only the static
stage. The `preflight` recipe of the `justfile` on `origin/main` says: "visual, viewer-graph,
integration, report and gallery stages skipped on Windows; CI runs them". The Driver saw those
failures only at the end, when the pull request was opened.

After this change, a CR that adds or changes visual, integration or stress scenarios does three
things after round 1: it pushes its branch, opens a draft pull request with a provisional body,
and dispatches the heavy CI. Round 2 then starts with the real CI result instead of finding it in
the last round.

## What changes

One file changes, in the Studio repository:
`.agents/guidelines/change-requests-lifecycle.guidelines.md`, the process guideline the Driver
reads (hc-Q1). Nothing else changes: not chantier's `chantier.yaml` or cards (hc-Q1: the rule is
specific to Studio), not `.github/workflows/ci.yml`, not the `justfile`, not `ci.guidelines.md`.

### New bullet in "Project rules on top of chantier's steps"

Add one bullet, **Early heavy CI**, to the section "Project rules on top of chantier's steps",
between the **Pull request** and **CI** bullets. Write it in the guideline's style: short
sentences, plain English, no CR numbers, no batch names. It may be split into sub-items. It says
the following.

1. **Scope (hc-Q2).** The rule applies to a change request that adds or changes visual,
   integration or stress scenarios. In practice, its round 1 diff touches `test/visual/`,
   `test/integration/` or the stress list `test/shared/stressPlan.ts`, or its
   `03-change-spec.md` asks for such scenarios. Other change requests keep the current steps.
2. **Reason (one sentence).** On Windows, `just preflight` runs only the static stage, so visual
   and real VS Code window failures show up only in CI.
3. **Early push (hc-Q5).** After round 1, whatever the round's review verdict, the change
   request's own Driver does these steps in order:
   - **Checkpoint commit.** It makes a checkpoint commit of round 1's state (explicit paths,
     project commit format).
   - **Rebase and fast gate.** It rebases on its base, then runs the project's fast gate at the
     rebased head, as the rules name it.
   - **Push.** It pushes the branch without the long gate (`just preflight`).
   - **Draft pull request.** It opens the pull request as a draft with a provisional body: the
     template's sections, with what is not known yet marked as provisional.
   - **Dispatch.** In its own command, it runs `gh workflow run ci.yml --ref <branch> -f heavy=true`.

   The requirements check and `just preflight` keep their places: the requirements check stays
   before the pull request leaves draft, as the **Pull request** bullet says, and `just preflight`
   stays a long gate before ready.

   The bullet states that this overrides the chantier Driver card's "gate before the first push"
   for these change requests. In `driver.md`, "CR driver: ship and proof" runs the long gate
   before the push and the PR, and the **Early push** bullet keeps "a PR that does not exist yet
   still waits for its gate before its first push".
4. **Stack (hc-Q4, revised).** A change request in a stack follows the same steps. Its own Driver
   pushes and opens the draft pull request against the base that `take` printed. The stack driver
   only restacks later, as "Parallel Change Requests Orchestration" says. That section stays
   unchanged and the stack driver's role has no exception.
5. **Open-PR cap (hc-Q6).** The early draft pull request counts in the user's cap of open pull
   requests (default 4). When the cap is reached, the Driver pushes the branch and dispatches the
   heavy run without opening the pull request. It opens the pull request when a slot frees up, by
   the usual steps.
6. **Reading the run (fix 6).**
   - **Find the run.** The Driver finds the run with
     `gh run list --workflow ci.yml --branch <branch> --event workflow_dispatch --json databaseId,headSha,status,conclusion`.
     It checks that the run's `headSha` is the head it pushed; a run at another head is not this
     run.
   - **Read a red job.** For a red job, `gh run view <id> --log-failed` gives the log.
   - **What the run is for.** The run is input to the next round. It never proves a later head
     green.
   - **Failures.** A failure goes into the next round as the **CI** bullet says: a product or
     test failure with the log excerpt; an infra failure is re-run once; a flake is named and
     filed. A red `stress` job is advisory (`ci.guidelines.md`, rule 12) but still a flake to fix.
   - **Round 1 approved.** When round 1 was approved and no round 2 follows, the Driver reads the
     run before **Verify**.
7. **Re-dispatch (hc-Q3, revised).** The change request's own Driver dispatches a heavy run:
   - **When.** Once after round 1, then once after each round that fixes a red `integration` or
     `stress` job of the early heavy run. It pushes that round, then dispatches the same command.
   - **When not.** Never when the last heavy run is green.
   - **Rule 13.** Rule 13 of [ci.guidelines.md](ci.guidelines.md) asks for a heavy run before
     merging a change to the extension host, the webview or the real-window tests. That run is
     the last green heavy run when the head has not changed since it ran. Otherwise the Driver
     dispatches one more run before ready.
   - **Pull request CI.** Each push to the draft pull request still runs the pull request CI, as
     it does today: static, visual and viewer-graph jobs, then `report` with the real VS Code stage
     skipped.
8. **Unchanged.** The round limit (3, all causes together) still applies. The early push does not
   make the pull request ready: **Verify** still comes before ready.

### The environment the heavy run uses (no change to the workflow)

The step uses the existing `workflow_dispatch` input `heavy` of `.github/workflows/ci.yml` (as on
`origin/main`).

Jobs that run on a branch dispatch:

| Job | System | What it runs |
| --- | --- | --- |
| `static` | ubuntu-latest | static checks |
| `static-windows` | windows-latest | static checks |
| `visual` | ubuntu-latest | Playwright Chromium against the mock host, `just dev-ci visual` |
| `viewer-graph` | ubuntu-latest | `just dev-ci visual`, then `just ci-viewer-graph` (job timeout 15 min) |
| `integration` | ubuntu-latest | a real VS Code window under `xvfb-run -s "-screen 0 2600x1440x24"`, `just ci-integration` (job timeout 30 min, test step 20 min), then `just ci-hang-dump` |
| `stress` | ubuntu-latest | real windows, `just ci-stress`, 12 rounds by default; advisory |
| `report` | ubuntu-latest | `just ci-report all` |
| `gallery` | ubuntu-latest | only when `integration` and `report` succeed; the default `gallery=true` is kept |
| `checks` | ubuntu-latest | the aggregate job |

`release-check`, `tag-release`, `release` and `pages` do not run: they run only on a push to `main`.

What differs from the local machine:

- **The local Windows machine has, and the run does not:**
  - the Windows display and the user's VS Code;
  - a warm `node_modules`, `.vscode-test` and Playwright cache (CI installs from the lock files and
    the archive caches);
  - the local `gh` login (the workflow uses its own `contents: read` token).
- **The run has, and `just preflight` on Windows does not:** Linux, Xvfb, and the visual,
  viewer-graph, integration, stress, report and gallery stages.

Healthy duration: about 10 min for `integration` and 16 min for `stress` (from the input's
description). The Driver reads the run when the next round starts or when the run ends, whichever
comes later.

## Decisions carried

- **hc-Q1** (confirmed by the owner, "Studio's CR guideline"): the rule goes in Studio's process
  guideline `.agents/guidelines/change-requests-lifecycle.guidelines.md`, not in `chantier.yaml`,
  because it is specific to Studio (the Windows preflight skips the visual, integration and
  report stages).
- **hc-Q2:** a CR that adds or changes visual, integration or stress scenarios pushes its branch
  as a draft PR after round 1 and dispatches `gh workflow run ci.yml --ref <branch> -f heavy=true`;
  the next round reads that run. Other CRs keep the current steps.
- **hc-Q3 revised** ("Only after such a fix"): a heavy run once after round 1, then once after each
  round that fixes a red integration or stress job of the early heavy run, and never when the last
  heavy run is green. Rule 13's pre-merge run is that last green run if the head is unchanged.
  The CR's own Driver dispatches (bullet item 7).
- **hc-Q4 revised** ("The CR's own Driver"): in a stack, the CR's own Driver pushes and opens the
  draft against the base `take` gave, as outside a stack. The stack driver only restacks later,
  with no exception to its role. This replaces the stack-driver exception of the previous version
  of this spec.
- **hc-Q5** ("After round 1, any verdict"): checkpoint commit, fast gate, push without the long
  gate, and a draft PR with a provisional body. The requirements check and `just preflight` stay
  where they are. The bullet says it overrides the Driver card's "gate before the first push".
- **hc-Q6** ("Yes; at cap, no PR yet"): the early draft counts in the open-PR cap. At the cap, the
  Driver pushes the branch and dispatches the heavy run without opening the PR.
- **Spec critic, fix 5:** the facts are taken from `origin/main` (the `viewer-graph` job, the
  current wording of the `preflight` recipe).
- **Spec critic, fix 6:** the run's head SHA must be the pushed head. The run is input to the next
  round, never proof of green at a later head. With round 1 approved, it is read before Verify.

## Out of scope

- Any change to `.github/workflows/ci.yml`, the `justfile`, `ci.guidelines.md` or the other
  project guidelines. In particular, no role name and no link to the process guideline may go in
  a project guideline: `test/build/test_guideline_isolation.py` refuses both.
- Any change to chantier (its cards, `chantier.yaml`, the Driver card). The override of hc-Q5
  lives in Studio's process guideline only.
- Running the visual or integration stages locally on Windows, or changing what `just preflight`
  skips.
- Automating the dispatch (a hook, a CLI command): the Driver runs the command.
- Changing the round limit or the open-PR cap.

## Commit and pull request

- **Commit.** One commit, type `docs`, with no scope (scopes apply only to `fix` and `feat`, as
  `git-commit-allowed-scopes.md` says). For example: `docs: dispatch the heavy CI after round 1 of
  a change request adding real-window tests`. The commit names explicit paths.
- **Changelog and requirements.** No `CHANGELOG.md` line, since the change is not `feat` or `fix`;
  the pull request's Changelog checkbox says "No user-facing change". No SwRS is touched: the
  requirements check finds no requirement (process text only, no `src/` or test change).
- **Pull request body.** It follows [pull-request.guidelines.md](pull-request.guidelines.md): no
  internal IDs (no CR numbers, no batch, no planning link). Impacts: "No visible change: process
  documentation only".
- **Early push.** This CR changes no visual, integration or stress scenario, so the new rule does
  not apply to its own delivery.

## Evidence

Every check reads the shipped guideline from the repository at the head under test, not a copy.

1. `git diff --stat origin/main...HEAD` lists only
   `.agents/guidelines/change-requests-lifecycle.guidelines.md`.
2. `grep -n "Early heavy CI" .agents/guidelines/change-requests-lifecycle.guidelines.md` finds the
   bullet inside "Project rules on top of chantier's steps", between **Pull request** and **CI**.
3. In the same file at the head, the bullet contains:
   - the exact command `gh workflow run ci.yml --ref <branch> -f heavy=true`;
   - the three paths `test/visual/`, `test/integration/` and `test/shared/stressPlan.ts`;
   - the words "draft", "provisional", "round 1" and "fast gate";
   - the sentence that it overrides the Driver card's gate before the first push;
   - the stack sentence (the change request's own Driver pushes and opens the draft against the
     base `take` printed; the stack driver only restacks);
   - the cap sentence (at the cap, push and dispatch without opening the pull request);
   - the head SHA check;
   - the re-dispatch rule (after a round that fixes a red `integration` or `stress` job; never
     when the last heavy run is green; rule 13's run is the last green run at an unchanged head).
4. The "Parallel Change Requests Orchestration" section is unchanged
   (`git diff origin/main...HEAD` shows no line of it).
5. Each decision hc-Q1 to hc-Q6, and fixes 5 and 6, maps to a sentence of the bullet; the Verifier
   quotes each one.
6. `uv run --group docs --group release --group requirements pytest test/build/test_guideline_isolation.py`
   passes: no project guideline gained a role name or a link to the process guideline.
7. `just preflight` passes (on Windows, this is the static stage, `just ci-static`).
8. The command in the bullet is valid against the workflow at the head:
   `grep -n "heavy:" .github/workflows/ci.yml` shows the `workflow_dispatch` input `heavy`
   (boolean). No dispatch is needed to prove this CR, which changes no workflow and no test.

No host or default matrix: the change is process text and does not depend on a host or a setting.
