# Prototype: the visualization backend's pages

A throw-away mockup for the grill of `visualization-backend`, not code to ship. Every action
is simulated: nothing is sent or written anywhere but the browser's local storage.

- `index.html`: prototype 6 (the project picker at the top left, Home, Triage, Kanban, Batch
  with its mode and PR columns, Costs, the CR folder's sliding panel). Only `chantier` has a
  snapshot; the other projects of the picker are examples.
- `compare.html`: `index.html` on a PC and on a phone, side by side.
- `data.js`: a snapshot of the planning folder, written by `snapshot.py`.
- `v1/`: prototype 1 (Board, Asks and Chief of Staff, Costs), with its own snapshot script.
- Screenshots of each version: `../evidence/prototype/` (`v1-*`, `v2-*`, `v3-*`).

## Run it

A page that loads `data.js` must be served over HTTP (a `file://` page in the Browser pane
cannot load it). From the repository's root:

```bash
python -I .agents/changes/1-inbox/visualization-backend/prototype/snapshot.py .agents/changes .agents/changes/1-inbox/visualization-backend/prototype/data.js
```

```bash
python -I -m http.server 8790 --bind 127.0.0.1 --directory .agents/changes/1-inbox/visualization-backend/prototype
```

Then open `http://127.0.0.1:8790/` (or `compare.html`). `?v=triage|kanban|batch|costs` opens a
view. "Tout annuler (prototype)" in the drafts list resets the simulated triage.

The paths above are this CR's while it sits in `1-inbox/`; the folder moves with the CR.
