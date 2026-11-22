## Summary

The web board gets a read-only Dashboard view for one project, with two tabs. Productivity shows, per closed batch, the change requests held and merged, the mean rounds per merged one, the batch's duration and the model calls by part. Spending shows the cost per merged change request, the spend per batch stacked by part or by model, the cost outside the batches as one line, and the ten most expensive change requests. One point per closed batch.

The figures are computed on the server from the closed batch records it already reads and served by one new read-only op, `dashboard.get`; the web client only draws them, with a new chart component (inline SVG, no library).

## Deliverables

- Sidebar: Dashboard sits after Costs and before Configuration. The tab and the range ("last 10", "last 20", "all") are in the address, so a reload, a shared link and Back give the same view.
- Each tile is the board's figure card with a headline, a chart, a legend in words and a coverage line ("n of N batches"). A figure a record lacks is a gap (a cut line, an empty bar slot), never a zero. A chart's value is read on hover, keyboard focus and tap.
- Words exist in English and French.
- **UNVERIFIED:** no screenshot of the page from the PR's head is attached yet.

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

- **UNVERIFIED:** no screenshot of the page from a real board on the real planning surface, and the French view, ten-point charts, the unpriced badge and the PR links of the ranking were not seen live (only checked on a demo copy).
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

A new page for board users; nothing else changes. No screenshot yet (see Known gaps).

## Test plan

- Lint and the board, code-targets, server and dashboard test files passed at the working tree before commit (SHA to be named at the head).
- Browser check on a demo copy at both widths: no console errors.

## Internal references

- CR-448 `448-dashboard-pages`, batch-30.

</details>
