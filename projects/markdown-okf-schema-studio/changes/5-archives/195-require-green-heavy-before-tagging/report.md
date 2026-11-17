# 195 — Require a green heavy run before tagging — report

Landed 2026-10-29. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/207 merged 2026-10-29 06:02Z with stack 217 (stack head `95598afa`; this PR's merge commit `6607285b`).

- Delivered: CI refuses to tag a version change without a green heavy run.
- CI on the final head: [40800375179](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40800375179).
- Stack heavy run (top of the stack): [40811480230](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40811480230).
- Open items: Possible follow-up: relax the gap check when both stages carry the same CI run id. Follow-up CR 197 landed with it.
