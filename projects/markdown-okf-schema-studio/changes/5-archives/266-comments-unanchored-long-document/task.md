# Task

Specification: `03-change-spec.md`, with `02-answers.md`. Stack mode: commit, never push. The base is
`origin/main`; the stack driver places the branch above CR 264 later, which also changes comment and
read-only code. Do not depend on 264 here.

Tests first. Gates: `just check`, and the e2e groups of comments through `just e2e` as far as the machine
allows. Only one CR runs app-window tests at a time. Before and after screenshots, light and dark, for any
visible change, in `out/`, named in the report.
