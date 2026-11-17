# Report: CR 213

PR [#239](https://github.com/gsemet/markdown-okf-schema-studio/pull/239), merged by the user 2026-10-31 into #237's branch, landed on main with #237 (rebase, commit f54a9ee4, same tree as 04b71f01). Normal CI runs 41189049030 and 41190530197 green; no heavy. Opus Inspector APPROVE in round 4 (owner-granted, doc only).

- `q shot --annotate/--note/--color`: outlines and labels drawn on QA screenshots; 34 px clip padding when annotating.
- Every finding has "Why this is wrong", a Verdict (Bug, Gap, Decision) and its requirements; Decisions go to the owner.
- `references/qa-bug-template.md` is the single template for sheets and backlog items, with "Uncheck to disagree" proposals.
- Screenshots: branch `screenshots/cr213-qa-annotate`. Details: reports/report.md. Follow-up in P3: qa-annotate-followups.
