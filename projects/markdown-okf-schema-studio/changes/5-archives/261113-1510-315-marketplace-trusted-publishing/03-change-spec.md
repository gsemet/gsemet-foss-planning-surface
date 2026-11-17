# Change Specification: publish to the VS Code Marketplace with trusted publishing

Type: ci. Automatable: the owner does not review this specification (02-answers.md, "go").
Sources: `01-intent.md`, `02-answers.md`, `intake/request.md`.

## Goal

The owner's words: « passons maintenant a la publication sur vs code marketplace qui apparament a
changé avec un trusted publisher aussi ».

The release job publishes to the VS Code Marketplace with GitHub Actions OIDC (Marketplace
Trusted Publishing) instead of the `VSCE_PAT` secret. The workflow proves its identity with an
OIDC token and receives a Marketplace credential valid 15 minutes; no long-lived secret is read
by the workflow. Azure DevOps global PATs are reported to retire on 2026-12-01 (community report,
not confirmed by Microsoft).

## Already in place (owner, 2026-11-13)

A Trusted Publishing policy exists on the `GaetanSemet` publisher
(marketplace.visualstudio.com/manage/publishers/gaetansemet/trustedpublishing):

| Field | Value |
| --- | --- |
| Name | Release workflow |
| Provider | GitHub Actions |
| Repository owner | `gsemet` (#133498) |
| Repository | `markdown-okf-schema-studio` (#1418546863) |
| Workflow | `release.yml` |
| Environment | `release` |
| State | Active, last used Never |

The policy binds the file name `.github/workflows/release.yml` and the environment `release`:
neither may be renamed, and the job `package` keeps `environment: release`.

## Decisions carried from 02-answers.md

1. `@vscode/vsce` goes to 4.1.0, not 4.1.1 (4.1.1 was a day old). 4.0.0 has no `--oidc`.
2. No automatic fallback to `VSCE_PAT` when OIDC fails at release time. The Marketplace step runs
   before the GitHub release step, so a failed exchange fails the job before the GitHub release
   is written. Recovery: a fix, then a `workflow_dispatch` of `release.yml` with the tag (the
   existing path); in an emergency, a local `vsce publish` with the PAT the owner keeps. (vsce
   4.1 itself never falls back to a PAT when `--oidc` fails.)
3. `VSCE_PAT` stays in the `release` environment until the first release published with `--oidc`
   succeeds; then the owner deletes it (Microsoft's migration advice). This CR does not delete it.
4. The proof is a 1.8.1 maintenance release, a separate release CR run right after this one merges
   (same batch, stacked). Not part of this CR.

## What changes

### 1. `.github/workflows/release.yml`, job `package`

- `permissions` becomes `contents: write` and `id-token: write`. The workflow-level
  `permissions: contents: read` stays as is (a test forbids `write` there).
- Delete the step "Verify Marketplace token" entirely.
- Step "Publish to VS Code Marketplace" (keep this exact name: tests look it up by name):
  - `run: npx --no-install vsce publish --oidc --skip-duplicate --packagePath out/reports/package/markdown-okf-schema-studio.vsix`
  - no `env:` block; no `VSCE_PAT` anywhere in the file. A `VSCE_PAT` in the environment
    together with `--oidc` would be a conflicting authentication method for vsce 4.1.
- Keep the order: "Publish to VS Code Marketplace" before "Attach VSIX and images to GitHub
  release" (decision 2 relies on it).
- Everything else in the job is unchanged (`npm ci --ignore-scripts`, tag checks, notes steps,
  the GitHub release step).

### 2. `.github/workflows/ci.yml`, job `release` (required consequence)

The normal release path calls `release.yml` from `ci.yml` (job `release`,
`uses: ./.github/workflows/release.yml`). A called workflow cannot get more permissions than its
caller job grants; without this change GitHub rejects the nested `id-token: write` and the CI
workflow fails. So the caller job `release` gets:

```yaml
    permissions:
      contents: write
      id-token: write
```

`secrets: inherit` and the rest of the job stay unchanged. This file is not named in the intent's
scope list, but the intent's goal cannot work without it; follow
[ci.guidelines.md](../../../guidelines/ci.guidelines.md) (rule 3: permissions belong in the
workflow).

### 3. `package.json` and `package-lock.json`

- `devDependencies`: `"@vscode/vsce": "^4.1.0"` (the repository's caret convention; the lock
  file is what pins, constitution section 5), with the lock file resolving exactly 4.1.0:
  `fnm exec -- npm install --save-dev @vscode/vsce@4.1.0`, then check
  `node_modules/@vscode/vsce/package.json` and the `node_modules/@vscode/vsce` entry of
  `package-lock.json` both say `4.1.0`.
- vsce 4.1.0 needs Node `>= 22`; `.nvmrc` is 24.
- Keep the `overrides` and the `//overrides` note (`@azure/msal-node`, `qs` floors reached
  through `@vscode/vsce`); if the new tree no longer reaches one of them, say so in the PR body,
  do not remove it.
- `scripts/package-extension.mjs` calls `node_modules/@vscode/vsce/vsce`; check packaging still
  works (`just package`).

### 4. `CONTRIBUTING.md`, "How to Release"

- "GitHub Configuration": replace the `VSCE_PAT` secret bullet with the trusted publishing
  policy: the `release` environment, the Marketplace Trusted Publishing policy "Release workflow"
  on the `GaetanSemet` publisher (repository owner `gsemet`, repository
  `markdown-okf-schema-studio`, workflow `release.yml`, environment `release`), and the
  `id-token: write` permission of the `package` job and of its caller job `release` in `ci.yml`.
  Say `VSCE_PAT` is no longer used by the workflow, stays in the `release` environment until a
  release published with `--oidc` succeeds, and is then deleted by the owner. Say that renaming
  `release.yml` or the `release` environment breaks publication until the policy is updated.
- Step 6 ("publishes to Marketplace"): may say "publishes to Marketplace with trusted
  publishing (OIDC)"; no other change.
- "Recovery and Release Notes": add the OIDC failure case of decision 2: a failed token exchange
  fails the job before the GitHub release; fix the cause, then dispatch **Release VSIX** with the
  existing tag; in an emergency the owner publishes locally with `vsce publish` and the PAT they
  keep. There is no automatic fallback to the PAT.

### 5. `.agents/guidelines/release-process.guidelines.md`

Name the policy instead of the secret, briefly (the mechanics stay in CONTRIBUTING): in step 6
(monitoring the Marketplace publication), say the publication uses the Marketplace Trusted
Publishing policy "Release workflow" (no stored token), that a failed OIDC exchange is recovered
as in "Recovery and Release Notes" of CONTRIBUTING.md, and that `VSCE_PAT` is deleted by the owner
once a release published with `--oidc` succeeded.

### 6. Test: `test/build/test_workflows.py`

Add one test, without a `@tests_req` marker (like
`test_release_job_keeps_dependency_install_scripts_off`: this is release hardening, not an
extension behaviour, and no SwRS covers publication authentication), for example
`test_release_publishes_to_the_marketplace_with_trusted_publishing`, asserting:

- `_release()["jobs"]["package"]["permissions"]["id-token"] == "write"`;
- the "Publish to VS Code Marketplace" step's `run` contains `--oidc`, `--skip-duplicate` and
  `--packagePath out/reports/package/markdown-okf-schema-studio.vsix`, and the step has no `env`;
- `"VSCE_PAT" not in RELEASE.read_text()` and no step is named "Verify Marketplace token";
- the publish step comes before "Attach VSIX and images to GitHub release";
- the `ci.yml` job `release` (`_ci_jobs()["release"]`) has `permissions["id-token"] == "write"`.

## Out of scope

- Open VSX (backlog item `publish-to-open-vsx`, parked until Eclipse grants the namespace).
- Deleting `VSCE_PAT` from the `release` environment (the owner, after the first OIDC release).
- The 1.8.1 release itself (its own release CR, after this one merges).
- Any change to the Marketplace policy, the `release` environment or repository settings.
- Requirements: no SwRS changes (CI only; CORE-078 is about release notes and is untouched).
- `CHANGELOG.md`: no line (CI and build commits get none, CONTRIBUTING "How to Release" step 2).

## Commit

One commit, `ci: publish to the Marketplace with trusted publishing`, per
[git-commit-message.guidelines.md](../../../guidelines/git-commit-message.guidelines.md) (no scope
for `ci`). Pull request per
[pull-request.guidelines.md](../../../guidelines/pull-request.guidelines.md); the body says the
first proof is the 1.8.1 release and that `VSCE_PAT` stays until then.

## Evidence

Checks (local, in the worktree):

1. `npx --no-install vsce --version` prints `4.1.0`, and
   `npx --no-install vsce publish --help` lists `--oidc`.
2. `git grep -n VSCE_PAT -- .github/` prints nothing.
3. `just package` builds `out/reports/package/markdown-okf-schema-studio.vsix`.
4. `just check` passes (includes the workflow tests, `npm audit` floors and the release tests).
5. `just preflight` passes (completion gate, constitution section 4).

Scenario (not runnable before merge; recorded for the 1.8.1 release CR):

1. The 1.8.1 version push runs `ci.yml`; `tag-release` tags; job `release` calls `release.yml`.
2. "Publish to VS Code Marketplace" logs a successful publish with `--oidc` and no token
   step exists; the Marketplace policy shows "last used" set.
3. "Attach VSIX and images to GitHub release" runs after it.
4. On failure, the GitHub release is not written; recovery follows decision 2.

## Open questions

1. Reusable-workflow identity. The normal release path is `ci.yml` calling `release.yml` through
   `workflow_call`. In such a run GitHub's OIDC token names the caller in `workflow_ref`
   (`ci.yml`) and the called file in `job_workflow_ref` (`release.yml`). Neither the Marketplace
   documentation nor the vsce README says which claim the policy's "Workflow" field matches (npm's
   trusted publishing, for instance, matches the caller). If the Marketplace matches the caller,
   the 1.8.1 publish through CI fails, and only a `workflow_dispatch` of `release.yml` with the
   tag succeeds. Recommendation: the owner adds a second policy on the same publisher, identical
   but with workflow `ci.yml` (environment `release`), before the 1.8.1 release; it costs one form
   and is removed later if unused. Alternative: run 1.8.1 as is and recover with
   `workflow_dispatch` if it fails (decision 2's path). This does not block implementing this CR.
