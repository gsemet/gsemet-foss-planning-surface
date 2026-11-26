# Web board: root Dashboard graphs and chart hover fix

Web board: Dashboard graphs on the root (all projects), and fix the hover bug on the dashboard's line charts.

From the user, 2026-11-24, as the follow-up of `web-board-menu-home-history` (CR-482, which adds the multi-project home, its feed and History): put "Dashboard" graphs in the root section, for all projects, and fix a bug seen when the mouse hovers a graph.

Hover bug, reproduced on the real board (read-only link, project chantier, page Tableau de bord, chart "CRs pris en charge et mergés"): hovering a point at batch 24 draws a pale vertical band over the chart that is opaque and sits above the lines, so the curve vanishes behind it (the peak of the line at batch 24 is hidden; the lines show again on each side). The caption above the chart updates correctly ("Batch 24, 2026-11-18: pris en charge 29, mergés 29"). The other charts were not hovered; check them all (the bar chart "Appels de modèle par partie" uses `chart-bar` rects). Expected: the band stays behind the lines, or is a translucent highlight, and the lines and points stay visible.

Wanted: a Dashboard section at the root level (all projects) built from the same graphs as a project's dashboard, with a choice of what to aggregate (to grill); the per-project dashboard keeps working. A change under clients/web/ reads DESIGN.md first and keeps it true (AGENTS.md); the root page is CR-482's, so this CR comes after it.
