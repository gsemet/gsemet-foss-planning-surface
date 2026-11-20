# Dashboard pages: productivity and spending charts per day

Priority P2, later.

Depends on: the studio project (`projects/markdown-okf-schema-studio`): not before its batch-06 is closed. (The owner, 2026-11-20: the dependency is the studio.)

Owner idea (2026-11-20): dashboard pages for chantier, in the spirit of an example screenshot the owner shared. Tabs "Productivity", "Spending", "Scorers". Productivity shows, per day over a date range:
- human interactions per PR (a single number plus a line chart);
- median cycle time: kickoff -> merge, kickoff -> PR, PR -> first human review, first human review -> merge;
- pull requests opened vs merged (line chart, with totals);
- total agent runs stacked by agent type (Foreman, Code, Review, Triage, Spec, Custom), with the count of top-level runs.

Nothing decided yet: where it lives (forge hub page, artifact, status report), which data chantier already records (orders, asks, costs, PR times), and what "Spending" and "Scorers" show. To grill later.

Second example from the owner (same day), the "Spending" tab (screenshot dashboard-example-spending.png; the first one is now dashboard-example-productivity.png):
- cost per PR: one number (with the total and PR count) and a line chart per day, split into a cost breakdown (compute, platform, inference), plus a "most expensive PRs" list (top 20 by attributed cost);
- spend by source: total and average per source, a stacked area chart per day by source (for chantier this could be by role or agent type, by batch, or by project).
