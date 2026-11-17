# Release report: v1.8.1

Released 2026-11-13. A patch release with no change to the extension: the first publication to
the VS Code Marketplace with Trusted Publishing (GitHub OIDC), no stored token.

| Item | Value |
| --- | --- |
| Tag | `v1.8.1` on 0253426a (`chore: version 1.8.1`), made by `tag-release` of the version push run |
| GitHub release | https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.8.1 (published 16:37:45Z, asset `markdown-okf-schema-studio.vsix`) |
| Version PR | https://github.com/gsemet/markdown-okf-schema-studio/pull/388, merged by rebase 16:14Z |
| Change in the release | https://github.com/gsemet/markdown-okf-schema-studio/pull/387 (b1907e9f), and fd8adb9e (docs) |
| Heavy run of `main` HEAD before the version commit | 43450028473 on b1907e9f: integration success, stress success |
| Branch heavy run of the version PR | 43456982844 on 08e3c0f8: success |
| Version push run | 43460632277 on 0253426a: static, static-windows, visual, integration, stress, report, checks, tag-release, release / package, pages / build-site, pages / deploy-pages all success |
| Marketplace | gallery `vspackage` 1.8.1: HTTP 200 |
| Pages | deployment 7770803614 on 0253426a, state success, https://gsemet.github.io/markdown-okf-schema-studio/ (HTTP 200) |

## Check of record

- The release job (`release / package`, job 132019872135) ran
  `npx --no-install vsce publish --oidc --skip-duplicate --packagePath out/reports/package/markdown-okf-schema-studio.vsix`;
  the step's environment holds only `RELEASE_TAG` and `UV_CACHE_DIR` (no `VSCE_PAT`). Output:
  `Published GaetanSemet.markdown-okf-schema-studio v1.8.1.` The step succeeded, then the GitHub
  release was written.
- The Marketplace serves 1.8.1: HTTP 200 on the gallery `vspackage` URL.
- Which policy shows "Last used": not seen from here (the Marketplace page needs the owner's
  sign-in). The job runs in `release.yml`, called by the `release` job of `ci.yml`, environment
  `release`: the OIDC token carries both workflows (`job_workflow_ref` `release.yml`,
  `workflow_ref` `ci.yml`), so either policy may be the one that matched. The Chief of Staff
  checks the publisher's Trusted Publishing page.
- `VSCE_PAT` can now be deleted by the owner (CONTRIBUTING, "GitHub Configuration").

## Issues closed

No issue closed by this release (PRs 387 and 388 have no closing references; no `issue:` line in
the changes).

## Notes

- No hero image, no `tweet.md` (owner's exception for this release). The release job logs
  "Pattern '.../release-assets/*' does not match any files": expected, the notes have no image.
