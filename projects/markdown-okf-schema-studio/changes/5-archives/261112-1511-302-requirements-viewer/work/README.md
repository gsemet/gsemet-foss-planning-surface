# Requirements viewer: working folder

Everything about the requirements viewer for the published site, kept for a later change.

| File | What it holds |
| --- | --- |
| `01-intent.md` | What the owner wants and the state of the work |
| `02-answers.md` | Every decision of the owner, dated (2026-10-25 wait, superseded on 2026-11-12) |
| `03-change-spec.md` | Draft spec, with the open questions to grill when the CR is opened |
| `main-paths/FORMAT.md` | The `### Main paths` format for a StRS (owner's decision of 2026-11-12) |
| `main-paths/StRS-MDOKFSTUDIO-DIAG-001.md` | The format written for one real use case (Mermaid) |
| `prototype-02/` | **Latest**: simpler static pages on one real vertical slice (Diagrams, DIAG-001); see its README |
| `prototypes/journey/` | First journey series, one prototype per step (below) |
| `prototypes/explorations/` | Earlier explorations: A Atlas (columns), B Constellation (rejected: flashy, unusable), C Strata (Sankey), D first metro, E first 4-view journey |

## The step prototypes (`prototypes/journey/`)

Each file is standalone (data inlined, about 1.6 MB) and opens on its step; the bar at the bottom
moves between steps, and every page also works as the full viewer.

| Step | File | What it shows |
| --- | --- | --- |
| 0 | `00-design-system.html` | Principles (do / don't), line colours, themes, type, components, motion |
| 1 | `01-areas.html` | The 16 areas as line cards, and the network ribbon (width = behaviours) |
| 2 | `02-area.html` | One area as a vertical line of use cases; transfers to other areas; lifecycle bar |
| 3 | `03-use-case.html` | The metro map from Main paths, Play per path, pick panel, combinatorics |
| 4 | `04-behaviour.html` | Rule, its place on the path, scenarios (GIVEN/WHEN/THEN), code and tests with kinds |
| 5 | `05-search.html` | The search sheet, results grouped by areas, use cases, behaviours, files |

Checked in the in-app browser at 1440 px and 375 px; not on a real phone nor in Safari.

## Rebuild the prototypes

From a scratch folder holding `site.html`, `ds.html` and the build scripts of `prototypes/journey/`:

```bash
git archive origin/main | tar -x -C src
(cd src && ../.venv-okfreq/bin/okfreq generate-report requirements --output-json ../report.json --output-summary-md ../report.md)
python3 build_data.py "$(git rev-parse origin/main)"
python3 build_journey.py src <this folder>/main-paths
python3 build_steps.py <this folder>/prototypes/journey --inline
```

`okfreq` is the one of the project's uv environment (`uv run --no-sync --group requirements okfreq`).
`build_data.py` reads `report.json` and writes `data.js`; `build_journey.py` adds the area titles
and the Main paths into `journey-data.js`; `build_steps.py` writes the step files from
`site.html` (the viewer) and `ds.html` (the design system page).
