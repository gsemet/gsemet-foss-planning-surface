# Web board Dashboard page: productivity and spending charts

The user (2026-11-20, `intake/request.md`, with two example screenshots of another product) wants
dashboard pages for chantier: charts over time of what the team produced and of what it cost, in
the spirit of the examples' "Productivity" and "Spending" tabs.

Intent:

- A Dashboard page of the web board, with two tabs, Productivity and Spending, drawn from what
  chantier's records of closed batches already hold (CRs and their results, rounds, dates, costs,
  and the cost's split by part and by model).
- Charts only: the list of what was done per day, week or month is the History page's
  (`board-history`), with no overlap.
- No new data is recorded for it. A metric of the examples that chantier's records do not hold
  (human interactions per PR, review times, runs by agent type, a "Scorers" tab) is out of scope.

Both board languages (English, French). The board stays read-only on a batch. Destination:
batch-30.
