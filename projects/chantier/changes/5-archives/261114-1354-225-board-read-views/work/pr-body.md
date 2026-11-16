## Summary

`chantier board` served a page frame with empty views. This PR draws the prototype's reading views from the live record of the planning folder: Home, Kanban, Batch (dependency graph, mode band, PRs to review and drafts, merged PRs), Costs, a CR's file panel, the project picker with "All projects", and the phone layout with its bottom bar. The views only read; the one non-GET request is the Costs view's "Recompute".

The page is hand-written HTML, CSS and native ES modules, one module per view, with no compiler and no bundler, in English and French from one word file per language.

This PR sits on the summaries CR's branch and holds only the board's reading views; it is a draft until that branch merges.

## Deliverables

- The views, in `skills/chantier/scripts/cli/src/chantier/board/web/`: `js/core` (api, store, router, dom with the escaping `html` tag, refresh, format), `js/model` (semantics, grill, events, words), `js/ui` (icons, parts, sidebar, picker, bottom bar, header), `js/views` (registry, home, overview, kanban, batch, batch-graph, batch-prs, costs), `js/panel` (panel, tree, markdown, file view), and `css/` per layer and per view.
- Prototype views reproduced: project picker (v6-01, v6-03), All projects (v6-16, v6-17), Home (v6-07, v6-09, v6-15), Kanban (v6-10, v6-13, kanban phone v6-11), Batch (v6-06, v6-12, v6-14), Costs (layout of v2-04), the file panel (layout of v3-06), phone layout (v6-08).
- Side-by-side comparison images (prototype left, board right, PC 1400x860 and phone 375x812): see the Verifier's evidence; the screenshots are attached below once the Verifier has left them.
- Targets enforced by `just check`: Biome (format, lint, 300 lines per JS file, 50 per function, at most 5 parameters, cognitive complexity 10) and one structure test for what Biome cannot see (links and imports stay inside the folder, no other origin, no inline script, style or `on...=`, no id selector, no `!important`, CSS nesting, colours through tokens, `innerHTML` in `dom.js` only).
- Server additions, from the record only: per CR `updated` and `branch`; per project line `asks_unread` and `last_event_at`. `STATUS.json` and the pane are untouched.

## Blast radius

Grade: 2. The page and the board's read data change; the CLI's other commands do not. Reverting the commits restores the empty frame.

## Autonomous decisions

- The static folder is `board/web/` (where the server's frame lives), not `static/`.
- JavaScript files are capped at 300 lines (the repository's existing cap), under the specification's 400.
- Biome (already pinned for the board frame) replaces ESLint, Stylelint and Prettier; it has no cyclomatic or nesting rule, so cognitive complexity 10 and the structure test stand in the repository's own checks.
- A stack's PRs stay drafts, because the record holds no "stack verified on the forge" fact; no field was invented.
- A file too large to show as text (the server cuts at 1 MB) is listed by size and never fetched as text; an SVG or HTML file is offered as a download, never run.

## Known gaps

- Evidence E7 is partial: there is no fix-CR card shot and no series-CR "draft until it merges" shot.
- Two comparisons are board-only, with no prototype image to put beside them: the All projects bottom bar and the phone's swiped Kanban column.
- Linux and macOS CI, a cold fetch there and a real phone are unproved; the emulated phone (375x812) is compared, and the user is to try the board's URL over the local network.
- Stack-verified is not readable from the record, so a stack's PRs always show as drafts.
- A `[l](javascript:...)` link in a file renders as text, not as a link.
- No screenshot of the pane from a real session is needed: this PR does not change what the CR board pane draws.

<details>
<summary>Details</summary>

## Changes

- Server: `board/crs.py`, `board/state.py` (fields above); scenario step 16c checks every static module answers 200 with a JavaScript or CSS type and the `'self'`-only policy.
- Lint and tests: `biome.json`, `tests/test_code_targets.py`, `CONTRIBUTING.md` "Code standards".
- Page: as listed in Deliverables.

## Human decisions

- The page is in English and French, from one word file per language, open to more.
- The lint tool is Biome through `uvx` (pinned Node.js wheel), run by `just check`.
- The final comparison with the prototype is on PC (1400x860) and phone (375x812).

## Impacts

The board shows Home, Kanban, Batch, Costs, the file panel and the picker from the live record. Developers get JS and CSS targets in `just check`.

## Test plan

- [ ] New or changed tests (they fail on the previous code): the structure test in `test_code_targets.py`, the board tests, scenario step 16c
- [ ] Local gates at `<sha7>`: `just check`, `just scenario`
- [ ] Evidence: before at `<sha7>`, after at `<sha7>`
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-225 board-read-views, on CR-223 cr-summaries' branch. Work files: `work/investigation.md`, `work/r1.md` to `r4.md`, `work/qa/`.

</details>
