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

Captures of the viewer at 4e05f1e (before: the current main), on made-up titles. Use case page, before then after:

![Use case page before](./verifier/evidence/before-step1-use-case.png)
![Use case page after](./verifier/evidence/rebase/after-4e05f1e-step1-use-case.png)

Behaviour page, before then after:

![Behaviour page before](./verifier/evidence/before-step2-behaviour.png)
![Behaviour page after](./verifier/evidence/rebase/after-4e05f1e-step2-behaviour.png)

Search for `StRS-MDOKFSTUDIO-BLOCK-014`, before then after:

![Search before](./verifier/evidence/before-step3-search.png)
![Search after](./verifier/evidence/rebase/after-4e05f1e-step3-search.png)

Behaviour page at 390 px, before then after:

![390 px before](./verifier/evidence/before-step6-behaviour-390.png)
![390 px after](./verifier/evidence/rebase/after-4e05f1e-step6-behaviour-390.png)

## Changes

- `pages.ts`: full ID in the eyebrow, titles, crumbs, pager name and pager links.
- `searchIndex.ts`: entries start their search text with the full ID and carry a new optional `i` field.
- `viewer.js`: ID matching (ID parts rule, bare-number rule), ID matches first, capped list counts them first, new hint.
- Tests: page texts, share titles, index fields, a new search test that runs the shipped `viewer.js`, and a Chromium check of the breadcrumb, eyebrow and pager at 1280, 800 and 390 px.
- Requirements: two new SwRS (CORE-092 search by ID, CORE-093 full IDs on pages), CORE-084 and CORE-085 updated, glossary entries Full ID and Short ID.

## Impacts

User-visible on the published requirements viewer (text of headings, titles, links and search). The share title of a use case or behaviour changes from `<title> (<full ID>)` to `Use case <full ID>: <title>`, as asked by the owner; the two assertions that pinned the old form changed for that reason. Before and after captures of the scenario steps are in the verification evidence (see Known gaps for what they cover).

## Blast radius

Grade: 1. The change is confined to the requirements viewer and its tests; a plain `git revert` restores the previous behaviour.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated or added, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates at 4e05f1e (checks and review carried from 4ddd1de, patch unchanged by the rebase): `just check`, `just requirements-lint`, `just requirements-update` (no diff on a second run), `okfreq validate --check-links --project-root .` and `just ci-viewer-graph` (6 tests, 2 new in Chromium) passed; `just preflight` passed (on Windows its static stage only: the visual, viewer-graph, integration, report and gallery stages are CI's)
- [x] Review: approved at 4e05f1e (carried from 4ddd1de, patch unchanged by the rebase onto the current main)
- [x] CI green at 4e05f1e: static, static-windows, viewer-graph and visual pass; integration, stress, release-check and toc-loop are skipped on pull requests

## Autonomous decisions

- Two new SwRS (CORE-092 search by ID, CORE-093 full IDs on pages) instead of extending CORE-080 and CORE-082: the change adds two behaviours that can be tested on their own, and the existing ones keep their statements.
- A full-ID query (for example `StRS-MDOKFSTUDIO-GFM-014`) lists its own tier only, as the specification's matching rules say (`StRS-…-14` matches the StRS, never the SwRS of the same number). The shorter forms (`GFM-014`, `gfm-14`) list the use case, then the behaviour under it.

## Known gaps

- The scenario captures were taken on a site built from made-up requirement titles over the frozen use cases (`BLOCK-003`, `BLOCK-014`), not from the real report, at 4e05f1e (before: `9c70477a`). Step 3 differs from the specification's wording: `StRS-MDOKFSTUDIO-BLOCK-014` lists the use case only (see Autonomous decisions), and Enter opens it. Real report titles and the published site are not checked.
- The 800 px layout of the pager is not proved by the captures (they cover 1280 and 390 px); the Chromium check in the viewer-graph job covers it and passes.
- The new entry in the requirements log (`requirements/tiers/log.md`) has a heading suffix naming the change, kept because the log's earlier headings follow that convention.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
