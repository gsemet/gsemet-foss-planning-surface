# The Batch page's central view gets tabs: graph, Gantt, time cards

The user (2026-11-17), on the board's Batch page:

- The central view goes under tabs, placed under the "States and arrows, hover for the legend"
  line (`batch.legend_hint`, `js/views/batch-graph.js:48`). The current tab is today's
  dependency graph. The other views are loaded lazily (on first opening of their tab).
- **Gantt tab.** Each CR on its own line, with its start and end shown; dashes or hatching while
  it is not finished; a cross stuck to the right edge for a CR not started yet; the
  interdependencies drawn as vertical arrows between lines.
- **The graph tab:** a card that just changed state carries a small burst or an icon showing it
  was updated.
- **Time cards tab.** The time card visualisation (prototype 1 of `board-paper-visualizations`,
  copied into `intake/`): one paper time card per CR, one stamped line per round. A card gets a
  stamp when its CR needed several reworks (round 3 or more).

Data: the batch's `events.jsonl` holds timestamped `take`, `round`, `phase`, `verdict`,
`ship`, `handback` and `order` events, enough for start, end and per-round times.