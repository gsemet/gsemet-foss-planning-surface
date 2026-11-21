## Summary

The published requirements viewer named a requirement by its short ID (`BLOCK-003`) in its page headings, tab titles and breadcrumb, and its search could not find a requirement from its full ID (`StRS-MDOKFSTUDIO-BLOCK-014` answered "Nothing matches"). This change makes the full ID the name of a requirement everywhere on the viewer, and makes the search find a requirement from its full ID, its short ID, in any case, from a number without its leading zeros, and from a bare number.

## Deliverables

Where a use case or behaviour page now shows the full ID:

| Place | Before | After |
|---|---|---|
| Eyebrow | `Use case BLOCK-003` | `Use case StRS-MDOKFSTUDIO-BLOCK-003` |
| Tab title | `Use case BLOCK-003: <title> \| Studio requirements` | `Use case StRS-MDOKFSTUDIO-BLOCK-003: <title> \| Studio requirements` |
| Share title (og/twitter) | `<title> (StRS-MDOKFSTUDIO-BLOCK-003)` | `Use case StRS-MDOKFSTUDIO-BLOCK-003: <title>` |
| Breadcrumb | `Areas / Block editing / BLOCK-003` | `Areas / Block editing / StRS-MDOKFSTUDIO-BLOCK-003` |
| Pager links | `← <title>` | `← <full ID>: <title>` |

Search: `StRS-MDOKFSTUDIO-BLOCK-014`, `BLOCK-014`, `block-014` and `block-14` find the page, the exact ID match comes first and Enter opens it. A short ID shared by a use case and a behaviour lists the use case first, the behaviour right under it. A bare number (`14`) lists every requirement numbered 14 first.

## Changes

- `pages.ts`: full ID in the eyebrow, titles, crumbs, pager name and pager links.
- `searchIndex.ts`: entries start their search text with the full ID and carry a new optional `i` field.
- `viewer.js`: ID matching (ID parts rule, bare-number rule), ID matches first, capped list counts them first, new hint.
- Tests: page texts, share titles, index fields, a new search test that runs the shipped `viewer.js`, and a Chromium check of the breadcrumb, eyebrow and pager at 1280, 800 and 390 px.
- Requirements: two new SwRS (CORE-092 search by ID, CORE-093 full IDs on pages), CORE-084 and CORE-085 updated, glossary entries Full ID and Short ID.

## Impacts

User-visible on the published requirements viewer (text of headings, titles, links and search). The share title of a use case or behaviour changes from `<title> (<full ID>)` to `Use case <full ID>: <title>`, as asked by the owner; the two assertions that pinned the old form changed for that reason. No screenshots yet: see Known gaps.

## Blast radius

Grade: 1. The change is confined to the requirements viewer and its tests; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [ ] Local gates: `just check`, `just requirements-lint`, `just requirements-update` (no diff on a second run), `okfreq validate --check-links --project-root .` and `just ci-viewer-graph` (6 tests, 2 new in Chromium) passed on the round's tree; `just preflight` not yet run (the long gate follows)
- [ ] Review
- [ ] CI green

## Autonomous decisions

- Two new SwRS (CORE-092 search by ID, CORE-093 full IDs on pages) instead of extending CORE-080 and CORE-082: the change adds two behaviours that can be tested on their own, and the existing ones keep their statements.
- A full-ID query (for example `StRS-MDOKFSTUDIO-GFM-014`) lists its own tier only, as the specification's matching rules say (`StRS-…-14` matches the StRS, never the SwRS of the same number). The shorter forms (`GFM-014`, `gfm-14`) list the use case, then the behaviour under it.

## Known gaps

- Scenario captures are pending the verification run.
