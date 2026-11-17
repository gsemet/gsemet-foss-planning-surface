# batch-01 progress report (before the release)

batch-01, stack, 4 of 4 change CRs merged, $21.14 spent, no budget.

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| CR-300 gallery-page-social-card | share picture card of site pages | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/371 | 1/3 | $1.58 |
| CR-301 strs-main-paths | Main paths of every StRS | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/372 | 2/3 | $5.04 |
| CR-302 requirements-viewer | requirements viewer on the site | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/373 | 3/3 | $7.02 |
| CR-303 site-one-cream-theme | one cream look for the site | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/374 | 2/3 | $3.70 |

- `main` HEAD `cf51f12f`: CI run 43262188098 fully green, `integration` and `stress` included.
- Not proved by the batch: the local `ci-integration` real-window step failed for CR-301 and CR-302
  (green on `main` CI); the SwRS count of the viewer (473 against 439 expected) is unexplained;
  TRUST-012 and TRUST-014 have no Main paths; Lighthouse was not measured.
- CR-303 was merged with its PR checks still running; the `main` run above covers it.

# Release v1.7.1

- Tag: `v1.7.1` at `cb96829955f3fce096fcb56147a6ca8a7f5c313d` (`chore: version 1.7.1`, PR
  https://github.com/gsemet/markdown-okf-schema-studio/pull/375, merged by the owner by rebase).
- GitHub release: https://github.com/gsemet/markdown-okf-schema-studio/releases/tag/v1.7.1,
  published 2026-11-12T19:47:14Z, not a draft, assets `markdown-okf-schema-studio.vsix`,
  `requirements-viewer-map.png`, `share-card-gallery.png`; both image links in the notes answer 200.
  Header count "27 changes since 1.7.0" matches
  `git rev-list --no-merges --grep='^chore: version' --invert-grep --count v1.7.0..v1.7.1^` (27).
- Marketplace: `vsce publish` logged "Published GaetanSemet.markdown-okf-schema-studio v1.7.1." at
  19:47:10Z; the gallery API serves the 1.7.1 VSIX (HTTP 200); the listing still showed 1.7.0 at
  19:50Z, during the Marketplace's verification of the new version.
- Pages: deployment 7747907634 of `cb968299`, success, https://gsemet.github.io/markdown-okf-schema-studio/
  and `/requirements/` answer 200.

## CI runs

| Run | Commit | Event | Result |
| --- | --- | --- | --- |
| [43262188098](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43262188098) | `cf51f12f` (`main` before the version) | push | success, `integration` and `stress` green |
| [43275294730](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43275294730) | `786fe7b0` (version PR branch) | heavy dispatch | success |
| [43289640826](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/43289640826) | `cb968299` (version push) | push | success: static, static-windows, visual, integration, stress, report, checks, tag-release, release / package, pages / build-site, pages / deploy-pages |

## Issues closed

None. No PR of `v1.7.0..v1.7.1` (#368 to #375) has a closing reference
(`gh pr view <n> --json closingIssuesReferences`), and the batch's changes carry no issue
(`issue: none` on CR-302 requirements-viewer, no `issue:` line elsewhere). Step 8 has no
comment to draft.
