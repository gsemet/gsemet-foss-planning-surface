## Summary

Requirement pages of the published site were shared on X with a generic picture, a statistics sentence or raw Markdown as text, and `/requirements` (no trailing slash) served a redirect stub with no tags at all, which X does not follow. This change gives every requirement page a share card that says what the page is: one picture per feature category (a feature category is an "area" of the viewer, one of the 16 groups of the extension), a share title with the full requirement ID, and a description without inline-code backticks or link syntax. The stub now carries the index's tags.

## Deliverables

- One picture for the index (`requirements/og/areas-card.png`, renamed so X sees a fresh URL) and one per category (`requirements/og/area-<areaId>.png`, eyebrow "Feature category", the category title, the category colour). A category's page, use cases and behaviours share it. The four per-level pictures are no longer drawn.
- Share texts, with the visible pages and tab titles unchanged:

| Page | Share title | Description |
| --- | --- | --- |
| Index | `Requirements of Markdown OKF-Schema Studio` | unchanged |
| Category | `<Category>: a feature category of Markdown OKF-Schema Studio` | `A feature category of Markdown OKF-Schema Studio: <scope>` |
| Use case | `<title> (<full ID>)` | the whole user need |
| Behaviour | `<title> (<full ID>)` | the rule, backticks and link syntax removed, cut at a word with `…` at 200 characters at most |

- New helpers in `test/site/socialCard.ts`: `plainText(text)` and `shareDescription(text, max = 200)`.
- Screenshots of the new pictures are in Impacts.

## Blast radius

Grade: 1. The change is confined to the site build (`test/site/`), the requirements bundle and the glossary; the extension is untouched. A `git revert` restores the previous pictures and texts.

## Autonomous decisions

- The word check over the shipped requirements also strips backticks from the expected text, so that a word followed by a backticked suffix (for example `` `$ref`s ``) compares as the plain text does; the strict reading failed on one real requirement.

## Known gaps

- No before picture was captured; the old per-level pictures are removed by the diff, and the three after pictures are at this head.
- `just site-assemble` stops at its gallery step on Windows (no end-to-end reports there, CI only); the site was built with `npm run site`, which does not involve the gallery.
- The unit test "a page refresh inside the join window renders again instead of joining the shared render" failed once in a full run and passed on re-run: a timing flake unrelated to this change.

<details>
<summary>Details</summary>

## Changes

- `socialCard.ts`: `plainText`, `shareDescription`.
- `requirementsViewer/cards.ts`: `viewerCards` (index card plus one card per category) and `categoryCardBody` replace the level cards.
- `requirementsViewer/shell.ts`: `PageSpec.shareTitle` and `PageSpec.area`; `shareCard(spec)` picks the picture and the texts.
- `requirementsViewer/pages.ts`, `home.ts`, `layout.ts`: share titles and descriptions; the statistics sentence is removed from the use case description.
- `requirementsViewer/write.ts`: the `/requirements` stub carries the index's social tags.
- Requirements: SwRS-MDOKFSTUDIO-CORE-085 updated in place, scenario wording of SwRS-MDOKFSTUDIO-CORE-086, log entry. Glossary: "Area" and "Social card".

## Impacts

Social previews of every requirement page show the page's own title and text and its category's picture. After deploy, links must be reshared with `?v=2` so X fetches the new cards. No change to the visible pages.

The index picture, the "MyST syntax" category picture and the "Edition palette and slash menu" category picture, as built at this head:

![Index share card](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/02bff1514d62b0d27cc3f9462aef2a86d18006a7/after-areas-card.png)

![MyST syntax category card](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/02bff1514d62b0d27cc3f9462aef2a86d18006a7/after-area-myst.png)

![Edition palette and slash menu category card](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/02bff1514d62b0d27cc3f9462aef2a86d18006a7/after-area-palette-slash.png)

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: SwRS updated, markers in code and tests, `just requirements-update`
- [x] Changelog: No user-facing change (published site only)
- [x] Local gates: `just check` pass, `just preflight` pass (second run, see Known gaps), `just requirements-lint` pass, all at 726b41d
- [x] Review: approved at 726b41d (round 1, move 78ad518..726b41d)
- [x] CI green at 726b41d

## Internal references

CR-443 share-cards (requirements-share-cards).

</details>
