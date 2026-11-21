# Web board History page: CRs, PRs and releases per day, week or month

A dedicated History page on the board: what was done, per day, with every CR merged or dropped, every PR opened, made ready and merged, and every release.

The user (2026-11-13): "le bilan du jour oui dans une page dédiée, genre historique, avec une vue par jour et tous les CR / PR et release faites. un peu comme la page energie de home assistant, avec possibilité de faire avant/apres, selectionner semaine etc."

As in Home Assistant's Energy page:
- a period selector: day, week, month (and maybe year);
- previous and next arrows to move by one period, and a "today" button;
- for the period: the totals (CRs merged, PRs, releases, cost) and the list of items, grouped by day.

Open points for the grill:
- Source: the batch records of `5-archives/batches/` (CR-224, merged) and the archived CRs; what a record lacks (a PR's ready time, a release's date).
- The cost per period, from the priced record.
- Runs after CR-225 (board-read-views).
