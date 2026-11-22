# Web board History page: what was done, per day, week or month

The user, 2026-11-13: "le bilan du jour oui dans une page dédiée, genre historique, avec une vue
par jour et tous les CR / PR et release faites. un peu comme la page energie de home assistant,
avec possibilité de faire avant/apres, selectionner semaine etc."

The board has no page that answers "what was done today, this week, this month". The closed
batches' records (`5-archives/batches/`), the archived CRs and the running batch hold it, but only
batch by batch (Costs, the Batch page's navigator, Home's five last batches).

Wanted: a read-only History page on the web board, in the spirit of Home Assistant's Energy page:
a period selector (day, week, month), previous and next arrows and a "today" button; for the
period, a few totals (CRs merged, CRs dropped, PRs opened, releases, cost of the CRs ended) and the
list of what happened, grouped by day, each line opening its CR or its PR.

History is the list; the charts (productivity and spending per day) belong to the Dashboard pages
CR of the same batch, and History draws none.
