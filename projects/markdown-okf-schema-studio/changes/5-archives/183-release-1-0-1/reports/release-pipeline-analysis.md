# 183 — Release pipeline on merge to main: analysis for 1.0.1

Scope: what happens when the stack whose top PR is #197 (branch `change-requests/183-release-1-0-1`,
version 1.0.1; GitHub stack 217) is merged to `main`. Read from the code of that branch after its
rebase onto the whole stack (so it includes #207, "require a green heavy run before tagging a
version change", and #209, "make re-run artifacts unique per attempt"), and from GitHub settings
read with `gh api`. Nothing was tagged or published.

## Verdict on the manual tag

**No manual tag push.** Since #207, CI tags `v1.0.1` itself, and only after the heavy real-window
jobs (integration and stress) of the merge push and the `checks` are green. A red job does not call
for a manual tag but for a re-run of the same CI run (recovery steps below). Expect it on this
release: the stress job is blocking on the version push and still fails now and then (see the
risks). Pushing `v1.0.1` by
hand would bypass that gate: a pushed `v*.*.*` tag starts `release.yml` and `pages.yml` through
their `push: tags` triggers, which do not look at the heavy results.

The only case left for a hand-pushed tag: `tag-release` passed its green-run check (checks,
integration and stress all `success`) but the "Tag a committed version bump" step itself failed
(for example the first real tag push by `GITHUB_TOKEN` is refused). Then
`git tag v1.0.1 <tip sha of the push> && git push origin v1.0.1` is consistent with the rule. Pages
then looks for a green heavy run of that commit; the CI run concluded red (its `tag-release`
failed), so the selector finds none and Pages runs the suite itself, which is slower but correct.

Fallbacks for the publication, none needing a new bump: re-run the failed `release` job; or
`gh workflow run release.yml --ref main -f tag=v1.0.1 -f notes=placeholder` (then paste
`reports/release-notes.md` into the GitHub release by hand).

## Merge method and merge order

- **Repository settings** (`gh repo view`, branch protection of `main`): only **rebase merge** is
  allowed (squash merge and merge commits are disabled), linear history is required, and the
  required status check is `checks` with "up to date" (`strict: true`).
- **The stack is landed atomically with GitHub's stack merge.** #197 is not based on `main`: its
  base is `change-requests/181-readme-reports-link-and-tiers-link` (#195), and only the bottom PR
  of the stack targets `main`. The command, rebase being the only allowed method:

  ```bash
  gh pr ready 197
  gh stack merge 217 --rebase --yes
  ```

  #197 must leave draft first (`gh pr ready 197`), because stack merge refuses draft PRs. Pass the
  stack id 217, never a bare 197: a number is resolved first as a stack number.
  GitHub merges every PR of the stack into `main` in one all-or-nothing operation: if one PR cannot
  be merged (branch protection, a red `checks`), none is. So the bump can never reach `main` before
  the fixes it announces, and no PR is left half-landed.
- **What it produces on `main`.** The commits of all the stack PRs, replayed by the rebase merge
  with new SHAs, in stack order, in one push. The bump commit `chore: version 1.0.1` is the last
  commit of #197, so it is the new tip. `github.event.before` is the previous tip of `main` (1.0.0
  in `package.json`); the CI run is for the new tip (1.0.1). `release-check` runs
  `scripts/version.py --bump-since "$BEFORE_SHA"`, compares the two ends of the push, sees
  1.0.0 → 1.0.1 and outputs `bump=true`. The intermediate commits get no CI run of their own
  (GitHub runs a push workflow for the pushed tip only).
- **The throwaway proof workflow.** The branch of #207 (`change-requests/195-require-green-heavy-
  before-tagging`) carries "chore: throwaway rerun proof workflow (removed before merge)" and, right
  after it, "chore: remove the throwaway rerun proof workflow". Both land on `main` with the rebase
  merge; the workflow file exists in no pushed tip, so it never runs on `main` and leaves no file.
  Harmless, only two extra commits in the history.
- **Does `tag-release` find a green heavy run for the merge commit?** It does not search for one:
  the merge push runs the heavy jobs itself in the same CI run, and `tag-release` reads their
  results through `needs`. Heavy runs made on the PR branch are never reused for tagging (the merged
  commits have new SHAs anyway). So the green heavy run of the merge commit exists exactly when the
  heavy jobs of the merge push pass.
- **Other PRs of the stack.** The stack merge marks every PR of the stack merged. Merging them one
  by one from the bottom is not a shortcut: `delete_branch_on_merge` is false, so GitHub does not
  retarget the next PR to `main`, and `checks` is required with `strict: true`. Each step would need
  a retarget to `main`, a rebase onto the new `main` and a new green `checks`, 18 times. Use the
  stack merge.

## Chain on the merge push (after the rebase onto the stack)

1. **Push event on `main`.** Tip `T` (the bump commit) on top of the previous tip `P`.
   `github.event.before` = `P`, a real 40-hex SHA.
2. **`release-check`** (push to `main` only): `version.py --bump-since P` → `bump=true`.
3. **Jobs.** `static`, `visual`, and, because `bump=true`, `integration` and `stress`
   (`needs: release-check`, `if: !cancelled() && (manual heavy dispatch || bump == 'true')`).
   `stress` is blocking on a version change (`continue-on-error` is off when `bump=true`; advisory
   everywhere else). `report` (`needs: [release-check, visual, integration]`) merges the stages with
   `just ci-report all`, then `checks` gates `static`, `visual` and `report`. `gallery` stays manual
   and is skipped. Heavy time: integration about 10 minutes; the stack's stress job about 22.5 to
   23.5 minutes against its 30-minute job timeout (#203, Find in preview, adds about 0.9 minute and
   #205, the `toc` scenario, about 1.6 minutes over the 20 rounds). The trusted window runs under a
   26-minute launch deadline (`STUDIO_LAUNCH_TIMEOUT_MS=1560000` in `just ci-stress`). The margin
   is enough: no sharding is needed. Nit: the `justfile` comment above `ci-stress` (about line 287)
   still says 20 rounds take about 18 minutes in the trusted window; left as is.
4. **`tag-release`** (`needs: [checks, release-check, integration, stress]`). It runs on a push to
   `main` when `release-check` succeeded and either `checks` is green or `bump=true` (so an untagged
   version change always explains itself). Steps:
   - "Refuse to tag a version change without a green heavy run": when `bump=true` and not all of
     `checks`, `integration`, `stress` are `success`, it writes the "Release not tagged" summary
     (each result and the re-run command) and fails the job. No tag, and `release` and `pages` are
     skipped.
   - "Tag a committed version bump" (only when checks are green and, on a version change, both heavy
     jobs too): `version.py --tag-before P` checks that the version increased, that
     `package-lock.json` agrees, that `v1.0.1` does not exist on the remote and is above the highest
     merged tag, then `git push origin HEAD:refs/tags/v1.0.1` with the job token and outputs
     `tag=v1.0.1`. No ruleset blocks a tag push.
5. **`release`** (`needs: tag-release`, runs when the tag output is set): `release.yml` with
   `tag: v1.0.1` and `secrets: inherit`; the called job selects the `release` environment
   (`COPILOT_GITHUB_TOKEN`, `VSCE_PAT`; no approval rule). It checks out the tag, verifies the tag
   (format, `HEAD` = tag commit, ancestor of `origin/main`, equal to `package.json` and lock
   versions), generates the notes with `scripts/release_notes.py --to-ref v1.0.1` (range
   `v1.0.0..v1.0.1`, context passed through a file, so the 1.0.0 argv failure cannot recur; output
   validated, three attempts), packages, publishes with `vsce publish --skip-duplicate` and creates
   the GitHub release with the VSIX and the notes.
6. **`pages`** (`needs: [tag-release, integration, stress, report]`, runs when the tag output is set): calls
   `pages.yml` with `tag: v1.0.1`, `reports_from_caller: true` (both heavy jobs green) and
   `reports_artifact` = the name the `report` job announced in its `artifact` output
   (`studio-reports-attempt-<n>`). Pages downloads that artifact of the calling run and builds the
   site from it, without running the suite again; on a download failure, or an empty name, it falls
   back to the suite. It runs in parallel
   with `release`. The token-pushed tag does not start the `push: tags` workflows, so nothing runs
   twice.

## Recovering from a red heavy job on the merge push (from #209)

Copied from the pull request of #209, "Recovery steps for a red heavy job on the version push":

1. Open the run of the version commit on `main` (workflow **CI**); the `tag-release` summary says
   "Release not tagged".
2. Run `gh run rerun <run-id> --failed`, then `gh run watch <run-id>`.
3. The failed jobs and their dependents re-run (`report`, `checks`, `tag-release`, `release`,
   `pages`); passed jobs keep their results.
4. Each attempt uploads `-attempt-<n>` artifacts; `report` merges the attempt-1 visual stage with
   the re-run integration stage and Pages uses the newest merged reports. The 2-hour stage gap no
   longer applies within one CI run, so a later re-run still works. To fetch reports by hand:
   `just site-from-run <run-id>`.
5. Once the tag exists, only re-run the failed jobs.

If the same job fails again, fix the cause in a new pull request and release a new version
(`just version`).

Checked against `.github/workflows/ci.yml` and `pages.yml` of this branch: every uploaded artifact
is named `<stage>-attempt-${{ github.run_attempt }}`; `visual`, `integration` and `report` announce
that name in an `artifact` output; `report` downloads each stage by the name its producer announced
(a job that was not re-run keeps its attempt-1 output, so its attempt-1 artifact is used, and the
re-run job's new one); `pages` receives `reports_artifact: needs.report.outputs.artifact` and
downloads exactly that name. After a stress-only failure, `report` is not re-run and its attempt-1
artifact (which already holds both stages) is the one Pages takes, which is correct. GitHub allows
re-runs for 30 days and at most 50 attempts per run (CONTRIBUTING). A later push without a version
change never tags 1.0.1.

## The 1.0.0 failures, one by one

| 1.0.0 failure | Fix | On this branch | Can it hit 1.0.1? |
| --- | --- | --- | --- |
| `tag-release`, `release`, `pages` skipped on the 1.0.0 merge push: the implicit `success()` is false when an ancestor (`integration`) is skipped | `!cancelled()` plus explicit `needs.<job>.result` in the three `if`s (on `main` since 1.0.0), kept by #207 | Yes, see the chain above; `test/build/test_workflows.py` evaluates the conditions over truth tables | No. On a version change the heavy jobs now run, so they are not skipped; if one is red, `tag-release` still runs and says why. |
| Release VSIX: `OSError: Argument list too long: 'gh'` while generating notes | Context written to a file and a short prompt; `notes=generated\|placeholder` dispatch input (on `main` since 1.0.0) | Yes: `scripts/release_notes.py`, `release.yml`, tests in `test_release.py` | The argv failure cannot. The Copilot call itself has not run in production since the fix. |

## Remaining risks (none known to fail, all unproven in production)

- **Expect "Release not tagged" on the merge push.** The alert-dropdown stress scenario still
  failed in about 4 of the 17 recent heavy runs ("Timed out waiting for Warning to change the
  type": runs 40802940246, 40800284527, 40796963673, 40793505712), and stress blocks tagging on
  the version push. If it happens, follow the recovery steps above (re-run the failed jobs of the
  same run); do not push a tag.
- **The release waits for the heavy jobs** (stress about 23 minutes, the longest), and a flake in
  integration or stress blocks the tag until it is re-run.
- **Reports after a re-run: fixed by #209.** The earlier known limit (a download by a fixed name
  returned the attempt-1 artifact, so Pages could build from stale first-attempt reports after
  "Re-run failed jobs") no longer applies: artifacts are named per attempt and each consumer reads
  the name its producer announced. Like the rest of the chain, not yet exercised on `main`.
- **Notes generation is the first real exercise of the file-based prompt.** If it fails, `package`
  fails before `vsce`, nothing is published and the tag stays. Recovery: re-run `release`, or
  dispatch `release.yml` with `notes=placeholder` and paste `reports/release-notes.md`. The
  validity of `COPILOT_GITHUB_TOKEN` cannot be checked from here.
- **First CI-created tag and first real run of `release-check` and of the green-run gate** on a
  push to `main`: the workflow tests cover the conditions, but no real push to `main` has run them.
- **Marketplace publish** needs a valid `VSCE_PAT` for publisher `GaetanSemet`;
  `--skip-duplicate` makes a re-run safe.

## Checklist after the merge (in order)

0. Before the merge: #197 is out of draft (`gh pr ready 197`), then `gh stack merge 217 --rebase
   --yes`.
1. The push run of `ci.yml` on `main`: `release-check` logs "Version change in this push: true";
   `integration` and `stress` run (not skipped).
2. `checks`, `integration`, `stress` green, then `tag-release` green, and
   `git ls-remote --tags origin v1.0.1` lists the tag at the merge tip. If the summary says
   "Release not tagged": follow the recovery steps above, do not push a tag.
3. `release` runs (not skipped): notes step green, Marketplace shows 1.0.1 with the new categories
   and keywords, GitHub release `v1.0.1` has the VSIX and the notes.
4. `pages` green, its log says "Reports from the calling run", and the site is deployed from
   `v1.0.1`.
5. Every PR of stack 217 shows as merged (the stack merge is all-or-nothing).
