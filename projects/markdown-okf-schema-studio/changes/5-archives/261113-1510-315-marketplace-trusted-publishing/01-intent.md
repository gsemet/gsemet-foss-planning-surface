# Publish to the VS Code Marketplace with trusted publishing

Type: ci. Filed 2026-11-13 by the Chief of Staff on the owner's request.

## Owner's words

> passons maintenant a la publication sur vs code marketplace qui apparament a changé avec un
> trusted publisher aussi

## Why

The release job publishes to the Marketplace with `VSCE_PAT`, an Azure DevOps personal access
token stored in the `release` environment. The Marketplace now offers Trusted Publishing: a
GitHub Actions workflow proves its identity with an OIDC token and gets a Marketplace credential
valid 15 minutes, so no long-lived secret is stored. Azure DevOps global PATs are reported to retire
on 2026-12-01 (community report, not confirmed by Microsoft).

## Scope

- `.github/workflows/release.yml`, job `package`: `permissions` gains `id-token: write`; the
  publish step runs `vsce publish --oidc --skip-duplicate --packagePath <vsix>` with no `VSCE_PAT`;
  the "Verify Marketplace token" step goes.
- `@vscode/vsce` from 4.0.0 (no `--oidc`) to a 4.1.x release, lock file updated.
- CONTRIBUTING ("How to Release", "GitHub Configuration") and the release-process guideline name
  the policy instead of the secret, and say `VSCE_PAT` is deleted once an OIDC release succeeded.

Out of scope: Open VSX (backlog item `publish-to-open-vsx`, parked until Eclipse grants the
namespace); deleting `VSCE_PAT` (the owner, after the first OIDC release).

## Already done by the owner

The Marketplace policy exists and is Active (see `02-answers.md`).

## Sources

- https://code.visualstudio.com/api/working-with-extensions/publishing-extension
- https://developer.microsoft.com/blog/trusted-publishing-visual-studio-marketplace/
- https://github.com/microsoft/vscode-vsce/pull/1291
