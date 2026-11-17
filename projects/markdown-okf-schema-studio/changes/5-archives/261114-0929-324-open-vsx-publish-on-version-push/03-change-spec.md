# Change Specification: publish to Open VSX on the version push

Type: ci (plus docs and one SwRS wording). Automatable: no user impact (the extension, its
settings and its users are untouched; only the release wiring changes). Priority P1, batch-04,
before the v1.9.1 release CR.
Sources: `01-intent.md`, `02-answers.md` (2026-11-14), `intake/request.md`, the v1.9.0 retro
(`4-archives/261114-0709-323-release-v1-9-0/retro.md` and `04-report.md`), the CR-322 archive
(`4-archives/261114-0013-322-publish-to-open-vsx/03-change-spec.md`, open question 1). Code read at
`origin/main` `4b45b45e` (version 1.9.0).

## Goal

The version push publishes to Open VSX without a recovery dispatch. The Open VSX trusted publisher
(registered for workflow `release.yml`, environment `release`, one per extension) stays as it is,
so the publish must run in a run whose OIDC token names `release.yml` as the workflow, not
`ci.yml`.

## Facts checked for this specification

- `ci.yml` job `release` calls `./.github/workflows/release.yml` with `workflow_call`
  (`permissions: contents: write, id-token: write`, `secrets: inherit`). In a called workflow the
  token's `workflow_ref` names the caller (`ci.yml`); only `job_workflow_ref` names `release.yml`.
  The Marketplace policy matched (its step was green on v1.9.0); Open VSX did not ("No trusted
  publisher matches the presented token").
- The v1.9.0 recovery, run 43569382533: event `workflow_dispatch`, branch `main`, input
  `tag=v1.9.0`, green on all three publication steps (Marketplace skipped the duplicate, GitHub
  release rewritten, Open VSX published). This is the only proven Open VSX path.
- `GITHUB_TOKEN` events start no new run, **except** `workflow_dispatch` and
  `repository_dispatch`. A job with `permissions: actions: write` can dispatch `release.yml`
  with `gh workflow run`, and that run is a top-level run of `release.yml`: its token names
  `release.yml` in both claims, as the recovery did.
- Nothing in `ci.yml` needs the `release` job: `pages` needs `tag-release`, `integration`,
  `stress` and `report`, and calls `pages.yml` itself (its own permissions, unchanged; its
  `deploy-pages` OIDC worked on v1.9.0 through `workflow_call`). No job reads an output of
  `release`.
- Nothing else calls `release.yml` (`grep -rn "workflows/release.yml" .github/` shows only
  `ci.yml`).
- `release.yml` already accepts `workflow_dispatch` with `tag` (required) and `notes` (default
  `reviewed`); its concurrency group is `release-<tag>`. The `release` environment allows the
  default branch and `v*` tags.
- A dispatched run takes the "workflow ref script" branch of the notes steps
  (`github.event_name == 'workflow_dispatch'`): it loads `scripts/release_notes.py` from the
  dispatch ref's head (`GITHUB_SHA`) and prepares the notes folder of the checked-out tag. That is
  exactly the v1.9.0 recovery path. Checkout, packaging and publishing stay on the tag.

## Decisions

1. **The `release` job of `ci.yml` dispatches `release.yml` instead of calling it** (the
   direction preferred in `02-answers.md`). Same job name, same `needs` and same `if`, so the
   truth tables and `test_release_and_pages_run_when_a_tag_was_created` stay valid.
2. **Dispatch ref: the default branch** (`github.event.repository.default_branch`, that is
   `main`), as the proven recovery. Judgment against `--ref <tag>`: a tag ref would pin the notes
   script to the tag too, but neither registry's trusted-publisher check has been seen on a
   tag-ref run, and v1.9.1 must not be the experiment. If `main` moved since the tag (a merge
   during the heavy run), the run uses the newer notes script on the tag's notes folder, the
   same behaviour as every manual recovery.
3. **The dispatching job does not wait for the release run.** The release is its own run of
   **Release VSIX** (event `workflow_dispatch`, branch `main`); its failure turns that run red and
   GitHub notifies as for any failed run. The CI run of the version push stays green once the tag,
   the dispatch and Pages succeed. Judgment: waiting would mean finding the dispatched run id and
   polling for up to the release job's length inside a 15-minute CI job, for a result the release
   process already watches (step 6 of the release guideline). The job summary links the Release
   VSIX runs page.
4. **Remove `workflow_call` from `release.yml`.** With no caller left, keeping it invites the same
   mistake again. The triggers become `push: tags` (a hand-pushed tag) and `workflow_dispatch`
   (the version push and the recovery). The recovery command is unchanged.
5. **Least privilege on the caller**: the `release` job gets `permissions: actions: write` only.
   `contents: write`, `id-token: write` and `secrets: inherit` go away (they were only there to be
   passed down to the called workflow). The `package` job of `release.yml` keeps
   `environment: release`, `contents: write`, `id-token: write`, unchanged.
6. **open-vsx.org and the Marketplace policy stay as registered** (`release.yml`, environment
   `release`). The owner changes nothing outside the repository.

## What changes

### 1. `.github/workflows/ci.yml`, job `release`

Replace the reusable-workflow call with a normal job. Keep the comment line above it about the
skipped heavy ancestors, and add one comment saying why it dispatches. Shape (the coder may adjust
the comment wording, not the values):

```yaml
  # A dispatch, not a workflow_call: the Open VSX trusted publisher matches the token's workflow,
  # which must be release.yml (a called workflow's token names ci.yml). A workflow_dispatch made
  # with GITHUB_TOKEN starts a run, unlike a tag pushed with it. The same dispatch is the recovery.
  release:
    needs: tag-release
    # Same reason as tag-release: do not inherit success() from the skipped heavy ancestors.
    if: ${{ !cancelled() && needs.tag-release.result == 'success' && needs.tag-release.outputs.tag != '' }}
    runs-on: ubuntu-latest
    timeout-minutes: 5
    permissions:
      actions: write
    steps:
      - name: Dispatch Release VSIX with the tag
        env:
          GH_TOKEN: ${{ github.token }}
          GH_REPO: ${{ github.repository }}
          TAG: ${{ needs.tag-release.outputs.tag }}
          DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
        run: |
          gh workflow run release.yml --ref "$DEFAULT_BRANCH" -f tag="$TAG"
          {
            echo "## Release dispatched"
            echo
            echo "Release VSIX runs for $TAG on $DEFAULT_BRANCH (event workflow_dispatch):"
            echo "$GITHUB_SERVER_URL/$GH_REPO/actions/workflows/release.yml"
          } >> "$GITHUB_STEP_SUMMARY"
```

- Exact step name "Dispatch Release VSIX with the tag" (the test finds it by name).
- No checkout (`gh` uses `GH_REPO`). No `${{ }}` inside `run`: every value goes through `env`.
- `notes` is not passed: its default `reviewed` applies.
- Nothing else in `ci.yml` changes; `pages` stays a `workflow_call` of `pages.yml`.

### 2. `.github/workflows/release.yml`

- Delete the `workflow_call:` trigger block (with its `tag` input). `push: tags` and
  `workflow_dispatch` stay as they are.
- Update the comment above "Load the release notes script of the workflow ref": drop "Only
  workflow_dispatch: inside workflow_call, github.event_name is the caller's event". Say instead
  that every dispatch (the version push from CI and a manual recovery) runs the notes script of
  the workflow ref, and a hand-pushed tag runs the tag's.
- `inputs.tag || github.ref_name` expressions stay (dispatch sets `inputs.tag`; a tag push uses
  `github.ref_name`).
- Nothing else: steps, their order, the job's environment and permissions.

### 3. `test/build/test_workflows.py`

- `test_release_publishes_to_the_marketplace_with_trusted_publishing`: drop the last assert
  (`_ci_jobs()["release"]["permissions"]["id-token"] == "write"`), now false by design.
- New test, next to the Open VSX test, without `@tests_req` (same reason as CR-315 and CR-322:
  release wiring, no SwRS covers publication), for example
  `test_the_version_push_dispatches_release_yml_so_its_token_names_release_yml`:
  - `_ci_jobs()["release"]` has no `uses`, no `with`, no `secrets`;
  - its `permissions == {"actions": "write"}`;
  - exactly one step named "Dispatch Release VSIX with the tag"; its `run` contains
    `gh workflow run release.yml`, `--ref "$DEFAULT_BRANCH"` and `-f tag="$TAG"`, and no `${{`;
  - its `env` maps `TAG` to `${{ needs.tag-release.outputs.tag }}`, `DEFAULT_BRANCH` to
    `${{ github.event.repository.default_branch }}`, `GH_TOKEN` to `${{ github.token }}`,
    `GH_REPO` to `${{ github.repository }}`;
  - `_release()[True]` (PyYAML reads `on` as `True`) has no `workflow_call` key, has
    `workflow_dispatch` with a required `tag` input, and keeps `push`;
  - no file in `WORKFLOWS` contains `uses: ./.github/workflows/release.yml`;
  - `_release()["jobs"]["package"]["environment"] == "release"` and its `id-token` is `write`
    (already in the Open VSX test; repeat or reference, the coder's choice).
- Rename `test_release_tag_and_call_run_the_notes_script_of_the_tag` to
  `test_release_tag_push_runs_the_notes_script_of_the_tag` (keep its `@tests_req
  SwRS-MDOKFSTUDIO-CORE-078` marker and body), and reword the comment above `RELEASE =` ("tag
  pushes and workflow_call keep the tag's" becomes "a tag push keeps the tag's; the version push
  is a dispatch").
- The existing generic tests must still pass: every job declares its permissions, `!cancelled()`
  with an explicit `needs.<job>.result` below skippable jobs, every `needs.<job>` reference names
  a needed job.

### 4. `requirements/`

`SwRS-MDOKFSTUDIO-CORE-076`, nominal scenario "Version change on main with a green heavy run": the
THEN becomes "`tag-release` tags the commit, `release` dispatches the **Release VSIX** workflow
with the tag on the default branch, and `pages` builds the site ...". Nothing else in the SwRS
(its tables say "`release` and `pages` are skipped", still true). CORE-078 stays true (the dispatch
path prepares the reviewed notes before the Marketplace step). Then `just requirements-update` and
a dated entry in `requirements/tiers/log.md` (per the requirements guidelines, "During a change").

### 5. `CONTRIBUTING.md`, "How to Release"

- Step 6: "CI calls **Release VSIX** explicitly with that tag. A tag pushed by `GITHUB_TOKEN` does
  not trigger another push workflow, so this call is required." becomes: CI **dispatches**
  **Release VSIX** with that tag on the default branch, as a run of its own. A tag pushed by
  `GITHUB_TOKEN` starts no workflow, but a dispatch does; and a dispatch (not a reusable-workflow
  call) is needed so that the OIDC token names `release.yml`, the workflow both trusted publishers
  are registered for. Watch that **Release VSIX** run (`gh run list --workflow release.yml
  --limit 3`), not only the CI run.
- "GitHub Configuration": replace the bullet "The `package` job of `release.yml` and its caller
  job `release` in `ci.yml` both grant `id-token: write` (...)" with: the `package` job of
  `release.yml` grants `id-token: write`; the `release` job of `ci.yml` only dispatches it
  (`actions: write`). Add to the renaming bullet: calling `release.yml` as a reusable workflow
  breaks the Open VSX publication (the token would name the caller).
- "Recovery and Release Notes": "rerun the failed release job" becomes "re-run the failed job of
  the **Release VSIX** run"; the rest (dispatch with the existing tag) stays.
- "Recovering from a red heavy job", item 3: after `tag-release`, `release` dispatches Release
  VSIX (a separate run) and `pages` runs. Item 5: a failed publication is re-run in the Release
  VSIX run; in the CI run re-run only `release` (if the dispatch itself failed) or `pages`.

### 6. `.agents/guidelines/ci.guidelines.md`

- "Recovering from a red heavy job on a release push", items 3 and 5: the same two edits as in
  CONTRIBUTING (no role names in guidelines).
- Add one rule after rule 14 (numbered next, wording the coder's): a job that publishes with OIDC
  trusted publishing runs in a top-level run of the workflow file the registry knows
  (`release.yml`), started by a dispatch, never through `workflow_call`; a change to that wiring is
  proven by the next version push, not only by a manual dispatch.

### 7. `.agents/guidelines/release-process.guidelines.md`, step 6

Name where the release job is: the version push dispatches a separate **Release VSIX** run
(event `workflow_dispatch`, branch `main`, found with `gh run list --workflow release.yml
--limit 3`); watch it with `gh run watch <run-id>`. Its Open VSX step must be green without a
recovery dispatch; a recovery dispatch is still allowed, and its use is reported as a failure of
the version-push path. No role names (`test_guideline_isolation.py`).

## Out of scope

- The open-vsx.org and Marketplace registrations (unchanged, decision 6).
- `pages.yml` and its call from `ci.yml`.
- The other two v1.9.0 retro items (integration flakes, registry indexing delay) and the v1.9.1
  release itself (its own CR).
- Waiting on the dispatched run from CI (decision 3).
- `CHANGELOG.md`: no line (a `ci` change).

## Commits

Per [git-commit-message.guidelines.md](../../../guidelines/git-commit-message.guidelines.md) and
[git-commit-allowed-scopes.md](../../../guidelines/git-commit-allowed-scopes.md): one commit,
`ci: dispatch the release workflow from the version push`, with every file above. Never `feat:` or
`fix:` on the extension (no user-facing change). Pull request per
[pull-request.guidelines.md](../../../guidelines/pull-request.guidelines.md); the body says no
registry setting changes and the proof is the v1.9.1 version push. `requirements/tiers/log.md`
conflicts with the other batch-04 changes are expected (stacked PRs).

## Evidence

Local, in the worktree (cut from `origin/main`):

1. `uv run pytest test/build/test_workflows.py` passes, the new test included.
2. `grep -rn "workflow_call" .github/workflows/release.yml` prints nothing;
   `grep -rn "workflows/release.yml" .github/` prints nothing.
3. `just requirements-lint` and `just requirements-update` pass.
4. `just check`, then `just preflight` (completion gate, constitution section 4).

No dispatch of `release.yml` before merge: `release.yml` is unchanged except for the removed
trigger, the manual dispatch path is already proven (v1.9.0 recovery), and the new `release` job
of `ci.yml` only runs on a version push to `main`.

Scenario of record (the v1.9.1 release CR checks it, not runnable before merge):

1. The v1.9.1 version push runs `ci.yml`; `tag-release` tags `v1.9.1`; job `release` is green and
   its summary says "Release dispatched".
2. A **Release VSIX** run appears with event `workflow_dispatch`, branch `main`, input
   `tag=v1.9.1`, started by `github-actions[bot]`, with no manual dispatch before it.
3. In that run: "Publish to VS Code Marketplace", "Attach VSIX and images to GitHub release" and
   "Publish to Open VSX" are green, with no recovery dispatch.
4. Within 15 minutes both checks of record of the release guideline answer HTTP 200.
5. If the Open VSX step fails anyway: recovery by dispatch as in CONTRIBUTING, and the release
   report records the version-push path as not proven.

## Open questions

None with a user impact. Decisions 2 (dispatch on `main`, not on the tag) and 3 (CI does not wait
for the release run) are judgment calls the Chief of Staff may revisit; neither changes what users
get.
