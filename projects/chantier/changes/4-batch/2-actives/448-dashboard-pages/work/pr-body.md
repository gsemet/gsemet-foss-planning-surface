## Summary

The web board gets a read-only Dashboard view for one project, with two tabs. Productivity shows, per closed batch, the change requests held and merged, the mean rounds per merged one, the batch's duration and the model calls by part. Spending shows the cost per merged change request, the spend per batch stacked by part or by model, the cost outside the batches as one line, and the ten most expensive change requests. One point per closed batch.

The figures are computed on the server from the closed batch records it already reads and served by one new read-only op, `dashboard.get`; the web client only draws them, with a new chart component (inline SVG, no library).

## Deliverables

- Sidebar: Dashboard sits after Costs and before Configuration. The tab and the range ("last 10", "last 20", "all") are in the address, so a reload, a shared link and Back give the same view.
- Each tile is the board's figure card with a headline, a chart, a legend in words and a coverage line ("n of N batches"). A figure a record lacks is a gap (a cut line, an empty bar slot), never a zero. A chart's value is read on hover, keyboard focus and tap.
- Words exist in English and French.

Screenshots from `chantier board` run at head 20cac21 on a copy of the real planning surface (project `chantier`, 28 closed batches; the board's own "writer blocked" badge is the copy having no remote).

![Productivity, English, last 20 batches, at 20cac21](./evidence/dashboard-productivity-en.png)
Productivity, English, last 20 batches, at 20cac21.

![Spending, English, by role, a batch read on hover, at 20cac21](./evidence/dashboard-spending-en-role.png)
Spending, English, by role, with the value of batch 26 read on hover, at 20cac21.

![Productivity, French, at 20cac21](./evidence/dashboard-productivity-fr.png)
Productivity, French, last 20 batches, at 20cac21.

![Spending, French, by model, all batches, at 20cac21](./evidence/dashboard-spending-fr-model.png)
Spending, French, by model, all batches, at 20cac21.

![Productivity at 375 px, at 20cac21](./evidence/dashboard-narrow-375.png)
Productivity at 375 px wide, at 20cac21.

```
GET api/v1/call/dashboard.get  {project, range: "10" | "20" | "all"}
-> {range, closed_total, total, points[], productivity{crs,rounds,duration,calls},
    spending{per_cr,spend{role,model},outside,top}, now}
```

## Blast radius

Low. One new op and three new Python modules, new client files and one component; the Costs page and the batch records are unchanged. Roll back by reverting the PR.

## Autonomous decisions

- The figures module is split in three files (`dashboard_records.py`, `dashboard_page.py`, `dashboard_spend.py`) to stay under the size limits of the code-targets test.
- Batch-29's record is kept as a JSON fixture file loaded by the test helper rather than a literal.

## Known gaps

- **UNVERIFIED:** the ten-point charts, the unpriced badge and the PR links of the ranking were not seen live (only checked on a demo copy and in tests).
- The whole view repaints on every push of the store, which may reset a hovered chart column.
- The word `dashboard.calls` is defined in both languages and not used by any view yet.
- The welcome of the server's API lists 21 ops with `dashboard.get`. Another open PR (the one adding `tzdata` to `uv.lock`) also adds an op: whichever lands second re-runs `uv lock` and recounts (22 ops once both land).
- Batch-01 to batch-16 hold no dates and no batch cost: they show only in the change-request and rounds tiles and in the ranking.
- A release alone records 0 rounds and lowers its batch's mean.
- A model's colour follows the project's all-time cost order, the Costs card's follows one batch's: they may differ.

<details><summary>Details</summary>

## Changes

- `board/dashboard_records.py`, `board/dashboard_page.py`, `board/dashboard_spend.py`: pure figures over closed batch records.
- `board/api/protocol.py`, `protocol.json`, `ops.py`, `docs/server-api.md`: the `dashboard.get` op (protocol 1 unchanged).
- Web client: views `dashboard*.js`, `ui/chart.js`, sheets `chart.css` and `dashboard.css`, router, store, api, registry, icon, French and English words, `DESIGN.md` (Components row, `--chart-height` token, Dashboard section).
- Tests: `test_board_dashboard.py`, `dashboard_world.py`, the every-op protocol call, and a design test on the registry order.

## Human decisions

- Closed batches only; the running batch has no point and a line links to Costs.
- Figures computed on the server and tested in pytest, not in the browser.
- Stacked bars for the stacked tiles, lines for the others; models coloured by all-time cost rank, up to eight, the rest folded.
- One project at a time; the switch by part or model is shared with Costs.

## Impacts

A new page for board users; nothing else changes.

## Test plan

- [x] `just check` passed at 9808e1d (1654 passed, 20 skipped).
- [ ] `just eval-dry-run` at 9808e1d: pending.
- [x] Browser check on a demo copy at phone and desktop widths, both tabs: no console errors, at the working tree of 9808e1d.
- [ ] Long gate at 9808e1d: pending.

## Internal references

- CR-448 `448-dashboard-pages`, batch-30.

</details>
