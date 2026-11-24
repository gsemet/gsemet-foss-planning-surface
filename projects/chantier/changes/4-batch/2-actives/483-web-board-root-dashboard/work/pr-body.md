## Summary

The web board's Dashboard was only available inside a project, and hovering or focusing a point on any chart laid an opaque band over the lines, marks and bars of that slot, hiding them. This PR shows the Dashboard on "All projects" too, with one summed curve per graph, and draws the hover band behind the series.

## Deliverables

- **Hover band.** In the shared chart component the drawing (`.chart-svg`) is now stacked above the columns (`.chart-cols`) that catch the pointer, focus and taps; the band keeps its `--accent-tint` token. Lines, marks and stacked bars stay visible on the hovered or focused slot, for every Dashboard chart.
- **Dashboard on All projects.** The `dashboard` registry entry gains an `overview`, so the All-projects menu reads Home, Notifications, History, Dashboard, Help. The page has the same tabs (Productivity, Spending) and range (last 10, last 20, all) as a project's, one curve or stack per graph, one link per project to its own Dashboard, a live line naming each project with a running or paused batch, and the project mark on the most expensive CRs.

```text
point = a batch number; value = sum over the projects that closed it
counts, costs ........ summed
rounds / merged CR ... pooled (mean over all merged CRs)
cost / merged CR ..... summed cost / summed merged CRs
duration ............. point: mean of the projects; headline: median of all batches
readout .............. "Batch 24, 3 projects: held 41, merged 38"
```

- `dashboard.get` answers for all projects with the same shape plus `projects` per point and `project` per top row; read-only, no forge call, still readable with the public key.
- No new token, colour or component.
- **UNVERIFIED:** no screenshots of a real board at this head (see Known gaps).

## Blast radius

Grade: **1**. A change to one shared chart sheet and one read-only server answer; a `git revert` restores the previous board. A project's own Dashboard answer is unchanged.

## Autonomous decisions

- The all-projects answer is the same `dashboard.get` op with the value `"*"`, as the history topic does, rather than a sibling op, so the protocol and the public-key allow-list are unchanged.
- The feed's refresh signal on All projects is a `closed_rev` field added to the `board` topic's project line.

## Known gaps

- **UNVERIFIED:** screenshots of the hovered charts and of the All-projects Dashboard on each tab: Playwright is not installed on the build machine, so no screenshot of a real board was taken.

<details>
<summary>Details</summary>

## Changes

- `css/components/chart.css`, `js/ui/chart.js`: the drawing above the hover band; readout names the batch and project count.
- `board/dashboard_page.py`, `board/dashboard_spend.py`, `board/api/ops.py`, `board/state.py`: grouping by batch number, `answer_all`, pooled ratios, union model rank.
- `js/views/registry.js`, `dashboard.js`, `dashboard-spend.js`, `dashboard-feed.js`, `css/views/dashboard.css`, `en/fr-dashboard.js`, `en/fr-help.js`: the page on All projects.
- `DESIGN.md`, `docs/web-board.md`: the Dashboard sections.
- Tests: `test_board_dashboard.py`, `test_board_dashboard_all.py`, `test_board_dashboard_client.py`, `test_board_design.py`, `test_board_read_key.py`.

## Human decisions

- One curve per graph, summed over the projects per batch; per-project detail one click away.
- Points are aligned by batch number (a time axis is left for later), and a readout names how many projects a point covers.
- A batch's duration is the mean across projects at a point and the median for the headline, never a sum.

## Impacts

All-projects users get a Dashboard menu entry and page; chart hover no longer hides the series. No screenshot yet.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates: `just check`, `just eval-dry-run`
- [ ] Evidence: none yet (no Playwright)
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-483 web-board-root-dashboard (batch 31).

</details>
