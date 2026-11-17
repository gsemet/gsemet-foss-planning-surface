# Review: PR #192 (3d65a586, 0203bfef): Pages site from the CI end-to-end reports

Reviewed in the detached worktree `markdown-okf-schema-studio-wt-review179` at main `cb1f2adc`. Nothing
was committed or pushed.

## Verdict: FINDINGS

The automatic path is sound. With no `run_id`, the selector only accepts a `workflow_dispatch` run of
`ci.yml` on the exact HEAD sha that finished green, whose `integration` job succeeded and whose three
artifacts have not expired. A dry run can never deploy. Tag verification cannot be skipped on a real
deploy. `id-token: write` and `pages: write` are confined to the `deploy-pages` job, which runs no
repository code.

There is one major gap: the manual `run_id` input skips every one of those checks.

## Findings

### F1 (major): `run_id` input bypasses the sha, event, conclusion and integration checks on a real deploy

- Where: `.github/workflows/pages.yml:85-92` (`REQUESTED_RUN_ID` is used as-is) and `:96-112`.
- Scenario: a maintainer dispatches `tag=v1.4.0` and pastes a `run_id`. That run might belong to
  another commit, have failed, be a `pull_request` run (possibly from a fork, so its HTML reports were
  produced by untrusted code), have skipped `integration`, or come from another workflow. Tag
  verification passes because it checks the checkout, not the reports. The build then downloads that
  run's artifacts and deploys them to Pages as the v1.4.0 site, with nothing in the log flagging the
  mismatch. If the run is partial, the `e2e-*` pattern download matches only what exists. A missing
  `e2e-integration` artifact is skipped silently, so the gallery ships without the real-window
  captures. Only a missing `studio-reports` artifact fails the step.
- Fix: validate an explicit run id with the same rules. For example, add `--run-id` to
  `select_e2e_run.py`. It would fetch `runs/{id}` and require `path == .github/workflows/ci.yml`,
  `head_sha == HEAD`, `event == workflow_dispatch` and `conclusion == success`, then run
  `integration_succeeded` and `has_artifacts`, and exit non-zero on a mismatch. Alternatively, honour
  `run_id` only when `dry_run` is true.

### F2 (minor): on the automatic release path the reuse almost never kicks in

- Where: `.github/workflows/ci.yml:331-342` together with `scripts/select_e2e_run.py:81`.
- Scenario: heavy runs are dispatched on change-request branches. PRs land on main under a new sha,
  for example branch `90bfb7a4` became main `768a04dc`. `tag-release` then calls `pages.yml` in the same
  push run, so a heavy run of the release sha cannot exist yet. The selector returns nothing, and the
  build falls back to running the full suite as it did before. The behaviour is correct, but the
  speed-up only applies to a later manual dispatch after someone runs heavy on main.
- Fix: none needed for correctness. Document it in the workflow comment, or accept a run on a tree-equal
  commit (compare `git rev-parse <sha>^{tree}`). If you add that, keep the check strict.

### F3 (minor): selector or download failures abort the deploy instead of falling back

- Where: `scripts/select_e2e_run.py:59` (`check_output` raises), and `pages.yml:96-112`.
- Scenario: a `gh api` error (rate limit, 5xx, or a missing `actions: read` grant) fails the step under
  `set -e`. An artifact can also expire between selection and download (retention edge). Either way the
  release deploy fails, even though the fallback could have built the site.
- Fix: decide on the policy explicitly. One option is to catch `CalledProcessError` in `main()`, log a
  warning and print nothing so the fallback runs. Another is to keep failing closed and say so in the
  docstring. The selection-to-download race is narrow and acceptable.

### F4 (minor): `GH_TOKEN` is exported to every step of `build-site`

- Where: `.github/workflows/pages.yml:42`.
- Scenario: `npm ci` lifecycle scripts, `uv sync`, `just site-assemble` and the fallback suite all see
  the token. Its scope is only `contents: read` and `actions: read`, and `actions/checkout` already
  persists a token in `.git/config`, so the impact is low.
- Fix: move `GH_TOKEN` into the `env:` of the "Find the end-to-end reports" step, the only step that
  uses `gh`. Optionally also set `persist-credentials: false` on checkout.

### F5 (minor): `just site-from-run` hides failed downloads and mixes in stale local reports

- Where: `justfile` `site-from-run` recipe (around lines 208-213).
- Scenario: the `for ...; do gh run download ... && cp ...; done` line returns only the status of the
  last iteration. A failed `e2e-visual` or `e2e-integration` download is silently skipped, and the site
  is assembled from whatever `out/reports` already holds, including leftovers from earlier local runs.
- Fix: use a shebang recipe with `set -euo pipefail`, and run `rm -rf out/reports out/reports-download`
  before downloading.

### F6 (nit): the stage downloads are redundant

- Where: `.github/workflows/pages.yml:96-104`.
- Detail: `studio-reports` is uploaded by the `report` job after it has merged `e2e-*` into
  `out/reports`, so it is a superset of both stage artifacts. In run 40781647461 it was 85.9 MB, against
  72.0 + 13.7 MB for the two stages. The ordering in 0203bfef is correct, and `download-artifact` v4
  overwrites files on extraction. Downloading `studio-reports` alone gives the same result with about
  86 MB less transfer. That requires `has_artifacts` to keep requiring the stage names, or the switch
  becomes a design change.

## Checks that passed (review questions)

- **Different commit (automatic path):** `head_sha` is both the API filter and re-checked in
  `is_candidate`. The event must be `workflow_dispatch`, the conclusion `success` and the status
  `completed`. The `integration` job must have conclusion `success`; a skipped job, as in a non-heavy
  dispatch, is rejected. Expired artifacts are rejected. All of these are unit-tested.
- **Live check:** `select_e2e_run.py` returned run 40781647461 for sha `90bfb7a4`, and printed nothing
  (exit 0) for an unknown sha. Its artifacts include `e2e-visual`, `e2e-integration` and
  `studio-reports`, none expired.
- **Dry run:** `deploy-pages` has `needs: build-site` and `if: !inputs.dry_run`, with an implicit
  `success()`. For push and `workflow_call`, `inputs.dry_run` is null, so the deploy runs. A dispatch
  with `dry_run=true` never deploys. A dispatch with `dry_run=false`, no tag and a branch ref skips
  `build-site`, so the deploy is skipped as well.
- **Tag verification:** `build-site` only runs without `dry_run` if `inputs.tag` is set or the ref is a
  tag, and in both cases `DEPLOYMENT_TAG` is non-empty. A whitespace tag fails the regex. The tag goes
  through `env` (no injection), and the step checks that HEAD is the tag commit, is an ancestor of the
  default branch and matches the `package.json` version.
- **Permissions:** the workflow and `build-site` have `contents: read` and `actions: read`.
  `pages: write` and `id-token: write` are granted only to `deploy-pages`, which runs only
  `deploy-pages`. The `ci.yml` `pages` caller grants a superset, `actions: read` included, so
  `workflow_call` stays valid.
- **Overlapping files:** see F6. Ordering and overwrite are correct.
- **Fallback:** PlantUML and Graphviz, Playwright, then `xvfb-run just site`. These are the same steps
  as before, moved after `npm ci` and `uv sync`, which is fine.
- **`just site` locally:** `site: e2e site-assemble` resolves to e2e, requirements-report, compile,
  site:gallery, then site. That matches the old order plus a harmless `compile`. `site-assemble`
  mirrors `ci-gallery`, which already runs on a runner without PlantUML.
- **`workflow_call` after a release:** this path works, but in practice it always takes the fallback
  (F2).
- **Several heavy runs on one commit:** the newest by `created_at` that qualifies wins, and an older
  complete run is used when the newest lacks artifacts (tested).
- **Partial artifacts:** rejected by `has_artifacts` on the automatic path; the manual path has the gap
  described in F1.
- **Re-run attempts:** the runs list and the jobs endpoint (default `filter=latest`) reflect the latest
  attempt. `download-artifact` v4 resolves names to the latest artifact.
- **Pagination:** `gh api --paginate` with `per_page=100`. The concatenated JSON pages are parsed
  correctly with `raw_decode`.

## Gates (main cb1f2adc)

| Gate | Result |
|---|---|
| `just check` on a fresh venv (after `npm ci` only) | FAIL at `release-tests`: `ModuleNotFoundError: No module named 'jsonschema'` while collecting `test/build/test_plugin_manifests.py`. This environment failure predates the PR (the file comes from 2017e39d, an ancestor of 3d65a586). `release-tests` runs with `--group docs --group release`, and `jsonschema` only arrives through the `requirements` group (okf-schema). |
| `just check` after `uv sync --group docs --group requirements` | PASS, exit 0. 80 pytest passed, among them the new `test_select_e2e_run.py` and `test_workflows.py`; okfreq: 1067 requirements, 0 errors, 0 warnings; lint 0 changes; coverage 0 changes. |
| `uv run --group requirements okfreq validate --check-links --project-root .` | PASS, exit 0: `1067 requirements, 0 errors, 0 warnings`. |

Fix for the pre-existing failure: run `uv sync --group docs --group requirements` first, or make the
recipe `release-tests` use `uv run --group docs --group release --group requirements pytest ...`.

actionlint is not installed locally, so it was not run.
