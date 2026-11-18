# Intent: rework the eval campaigns

The campaigns get names that say their host:

- `full` becomes `claude-full`;
- `real-foreman` becomes `claude-real-foreman`;
- `real-direct` becomes `claude-real-direct`.

`ticket-summary` goes. The one-CR `copilot` campaign gives way to `copilot-real-foreman` and
`copilot-real-direct`, the Copilot counterparts of the two quick Claude campaigns. They are ready
to launch, and the user runs them later in the Copilot app.

The reports in `evals/results/` are named by date and time first
(`2026-11-12-19-41-real-direct-run1.md`), so the folder lists in the order the runs happened.

On the way, the evals' docs lose what is wrong today:

- campaign lists written by hand that disagree;
- steps that are Claude Desktop's only but do not say so;
- old report names that the new names would make misleading.

The release notes already published (v0.9.0, v0.10.0) are history and keep the old names.
