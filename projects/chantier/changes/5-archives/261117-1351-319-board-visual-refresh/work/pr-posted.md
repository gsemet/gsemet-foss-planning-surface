## Summary

The web board worked but felt heavy: a different font on every host, tinted borders and fills for every state, and a Batch page that spent its width on a legend, a merged section and state groups. This PR restyles every view of the board in one light, modern look (one font, one deep accent, white surfaces with hairlines, two-tone cards, states as small icons) and tidies the Batch view along the way.

## Deliverables

Before (the previous pictures, at b9daeff) and after (at 9bb941f), side by side:

| Before (b9daeff) | After (9bb941f) |
| --- | --- |
| ![Batch before](https://github.com/user-attachments/assets/400e332e-d0fe-4d3a-8fd5-1eb124493d91) | ![Batch after](https://github.com/user-attachments/assets/fc8cbee9-a95d-4195-8686-5b19af0ccad5) |
| ![Costs before](https://github.com/user-attachments/assets/180d37cb-f0b9-4d91-89bb-31a34dd60ae4) | ![Costs after](https://github.com/user-attachments/assets/b7bce151-e9cc-41ae-af92-70ef13351066) |
| ![Costs phone before](https://github.com/user-attachments/assets/9c4b3f40-6005-46ea-bceb-774c9e2902e4) | ![Costs phone after](https://github.com/user-attachments/assets/e0fa8031-4808-45c4-aaad-356fb6681a44) |
| ![Configuration before](https://github.com/user-attachments/assets/367fce5d-9c2a-49b9-93bf-2e8fa0c3454a) | ![Configuration after](https://github.com/user-attachments/assets/d9568951-17bd-456e-95a9-bc5f59d8a479) |

After, at 9bb941f: Home, Triage, Kanban; the picker with a long project name and its open menu; the project's new Project section; an arrowhead touching the end of a bent line.

![Home](https://github.com/user-attachments/assets/32fee78c-82f6-4d95-a395-d6174b1fc4d6) ![Triage](https://github.com/user-attachments/assets/00ab77eb-8fe7-48c7-a699-efdd751eff79) ![Kanban](https://github.com/user-attachments/assets/fc516109-81b6-4309-8d57-ff36aafb5362)

![Picker, long name](https://github.com/user-attachments/assets/d2ca126d-23ac-41a3-adc1-cb3c5eb60460) ![Picker menu](https://github.com/user-attachments/assets/13d3f6ee-50c0-4913-b0b5-2be4c58dd326) ![Project section](https://github.com/user-attachments/assets/455e787c-a598-4f03-8416-41778921d330) ![Arrowhead close-up](https://github.com/user-attachments/assets/21aa07a3-fc64-4106-88ef-e68a0c2a455b)

- **One font, shipped with the board.** Inter in two weights (regular and medium) loads from the board itself; the page policy gains `font-src 'self'` and nothing else.
- **A sticky breadcrumb bar** (project, view, and on Batch the batch with its state) that stays at the top with a light shadow once the page scrolls.
- **A lighter project picker.** The name ends in an ellipsis before a centred chevron; the open menu shows only each project's mark and name and, while a batch runs, `batch-N · P %`. The folder, repository path and upstream URL moved to the project's Home, in a new Project section.
- **Batch view.** Four figure cards, no "Batch" card, no merged section and no state groups: each CR keeps one place in its level for its whole life, its state a badge (icon and word in the state's colour) in the node's top right corner. Level heads read "No dependency", "Level 1", ... A "States and arrows" pill opens the legend in a tooltip. One PR column: PRs to review, then drafts. Each arrowhead now sits at the end of its line on the card and points along it.
- **Shared look:** one deep teal accent, grey chips, two-tone cards (white body, grey metadata band), state icons instead of tinted borders and fills, hairline tables.

```text
before: tinted card per state, groups per level and state, merged section, legend row
after : white card + state badge, one place per CR, drafts last, legend in a tooltip
```

## Blast radius

Grade: **2**. Every page of the board changes its CSS and several views change their markup; two read-only fields (the repository path and its upstream URL, credentials removed) are added to the served project data. The board is read-only for planning content as before; a `git revert` restores the old look.

## Autonomous decisions

- The two new served fields (`repo_path`, `origin`) come from a read-only `git remote get-url origin`, cached for 30 s: the Project section needs them and the board served neither.
- The picker's percent counts the batch's merged CRs over its CRs, as Home's batch meter does.
- The all-projects overview keeps its folder and repository lines.
- Inter's static v4.1 files (not the variable font) were taken.
- One line of the README's picture alt text was fixed along with the docs, as it named merged PRs.

## Known gaps

- `docs/web-board.md` still describes the picker's surface entry as showing its name and path (the menu now shows the name only), and does not mention the project Home's new Project section; the project Home picture does not show it. Left because the round limit was reached; a docs follow-up closes it.
- The PRs view was not captured live (no forge access in the sandbox), and the side by side with the four approved mock-up files is not included.
- When a CR goes from working to ready, the CRs below it in the same level move up about 19px, because its "CI" step row is no longer drawn; the CR keeps its level and order.
- At 1400px the Batch graph's own scroller clips Level 1's right edge, so a node's badge can be partly cut there.

<details>
<summary>Details</summary>

## Changes

- `board/web/fonts/` (two Inter `woff2` files and the OFL licence), `fonts.css`, `.gitattributes` (fonts binary), `reply.py` (`font-src 'self'`).
- `tokens.css` re-valued (accent and its shades, state colours, type, space, shadows); the old tint, tag, mode and ring tokens removed.
- Shell: `index.html`, `shell.css`, `sidebar.css`, `crumbs.css`, `picker.css`, `ui/header.js`, `ui/picker.js`, `ui/sidebar.js`; `nav.sync` key.
- Shared pieces: `stateIcon`, chips, two-tone cards, figure cards, meters, buttons.
- Views: Batch (`batch-graph.js`, `batch-prs.js`, `batch-pr-card.js`), Triage, Kanban, Home and overview (`home-project.js`), PRs, Costs, Configuration, panels and dialogs.
- Server: `state.py` serves `repo_path`, `origin` (userinfo stripped) and a top-level `served_origin`.
- Docs: `docs/web-board.md`, `CONTRIBUTING.md`, `README.md`, `scripts/docs_screenshots.py` and the retaken `docs/web-board/*.png`.

## Human decisions

- A light layout: white sidebar with a hairline, grey active pill, small grey section captions and a breadcrumb header.
- Comfortable spacing on an 8px rhythm, 14px text.
- One deep accent colour; states shown as small dots or icons, with the legend in a tooltip.
- Inter, shipped with the board (no network), in regular and medium only.
- Two-tone cards (white body, grey metadata band) with a diffuse shadow.
- Every view takes the style, and the documentation pictures are retaken.
- On Batch: no "Batch" figure card, no merged section, no earlier batches' CRs, one PR column, no state groups (each CR keeps one place, its state a badge in its top right corner) and level heads without "after level N".
- The breadcrumb bar stays at the top when the page scrolls.
- One change, not split.

## Impacts

The board looks different on every page; what it shows and does is unchanged except for the Batch changes and the Project section listed above. The screenshots in Deliverables show the result.

## Test plan

- [ ] New or changed tests: the shipped-frame test lists the fonts, one assertion on the page policy, a parametrized case for the new served fields
- [x] Local gates at `2a58e23`/`9bb941f`: `just check` passed, and `just docs-screenshots` passed
- [x] Evidence: before at `b9daeff`, after at `9bb941f`
- [x] Review: approved at `2a58e23` (code), `9bb941f` (docs, carried)
- [x] Verified at `9bb941f`
- [x] CI green at `9bb941f`: all five jobs, `just scenario (ubuntu-latest)` included

## Internal references

CR-319 "the web board, lighter and more elegant" (batch-23). Work files: `work/investigator/investigation.md`, `work/coder/r1.md`, `r2.md`, `r3.md`.

</details>
