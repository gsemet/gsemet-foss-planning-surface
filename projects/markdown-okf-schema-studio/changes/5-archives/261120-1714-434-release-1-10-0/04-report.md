# Release 1.10.0: report

- Tag: `v1.10.0` on `dd89211d` (`chore: version 1.10.0`, version PR
  [#444](https://github.com/gsemet/markdown-okf-schema-studio/pull/444), merged by the owner by
  rebase at 16:52Z on 2026-11-20). The tag was made by CI's `tag-release` job; no agent pushed a
  tag.
- Release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.10.0, published
  17:11:11Z, not a draft. Assets: `markdown-okf-schema-studio.vsix`, `edit-one-list-item.png`,
  `list-item-handles-drag.png`, `list-items-in-toc.png`. The release body's image links point to
  `releases/download/v1.10.0/<file>`. The header reads "30 changes since 1.9.3".

## CI runs

| Run | What | Head | Result |
| --- | --- | --- | --- |
| [44764608171](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44764608171) | Heavy run on `main` before the version commit (step 4) | `049b543` | success; `integration` and `stress` each read as success |
| [44777704200](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44777704200) | Version push on `main` (step 6) | `dd89211` | success: static, static-windows, visual, release-check, integration, stress, report, checks, tag-release, release, pages / build-site, pages / deploy-pages success; toc-loop and gallery skipped |
| [44780688939](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/44780688939) | Release VSIX (`workflow_dispatch`, `main`) | tag `v1.10.0` | success in 54 s: Verify release tag, Prepare the reviewed release notes (workflow ref script), Publish to VS Code Marketplace, Attach VSIX and images to GitHub release, Publish to Open VSX, all success |

No job was re-run. Open VSX was published by the version-push path: no recovery dispatch was used.

## Registries

Checked at 17:13:39Z, about 2.5 minutes after the release run ended (17:11Z):

- VS Code Marketplace, `.../vsextensions/markdown-okf-schema-studio/1.10.0/vspackage`: HTTP 200,
  served at the first poll (minute 2-3 after the run).
- Open VSX, `https://open-vsx.org/api/GaetanSemet/markdown-okf-schema-studio/1.10.0`: HTTP 200,
  served at the first poll (minute 2-3 after the run).

The listing pages were not checked (not a gate).

## Pages

Deployed by the version push's own run: `pages / build-site` and `pages / deploy-pages` success in
run 44777704200.

## Issues closed

No issue closed by this release. The PRs of the release (#418, #419, #426, #428, #429, #431, #432,
#433, #434, #435, #436, #437, #439, #442, #443, #444) have no closing references
(`gh pr view <n> --json closingIssuesReferences`), and the batch's change requests all have a
verbal origin. Step 8 of the release guideline has nothing to post.

## Project inconsistency found

`CONTRIBUTING.md`, "How to Release", step 3 still amends the version commit with
`git commit --amend --no-edit -s CHANGELOG.md`, while
`.agents/guidelines/release-process.guidelines.md` step 5 says the version commit carries no
`Signed-off-by` trailer ("amend it without `-s`"). The guideline was followed. The fix (drop `-s`
from CONTRIBUTING.md) is already in the inbox as `1-inbox/contributing-release-signoff`.
