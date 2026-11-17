# Report — strict-requirement-schemas

Status: **done** (2026-10-28, branch `change-requests/122-strict-requirement-schemas`, PR [#179](https://github.com/gsemet/markdown-okf-schema-studio/pull/179), head
`95bb63a6`, merged as `ae999b1e` + `b9bd1d8d`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 r1 | Scripted change of 656 files on `okf-schema>=0.16.0` (recipe unchanged from 0.15.0): base schema gains `superseded_by`, `supersedes`, `relates_to` and drops `additionalProperties: true`; StRS/SwRS schemas get `unevaluatedProperties: false`; 508 scalar `superseded_by` → lists; 142 generated `supersedes`; 53 StRS exemption fields removed; `supersedes` in `generated_fields`. No approved requirement touched. | `ae999b1e` |
| T1 r2 | `test/core/frontmatter/requirementSchemas.test.ts`: StRS and SwRS cases reject an unknown key and a scalar `superseded_by` (0/2 on the old schemas, 2/2 after); optional `REQUIREMENT_SCHEMA_DIR` hook | `b9bd1d8d` |

## Proof of completion

- Two rounds, Inspector (Opus) APPROVE both. `just check` green (unit 3133); `okfreq validate
  --check-links` 1064 requirements, 0 errors; `lint --check --check-links` and
  `update-coverage --check` clean.
- CI: normal [40732634099](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732634099) (r1) and
  [40735726022](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40735726022) (r2) pass. Heavy deferred: the post-CR-168 heavy
  gate on main serves as its heavy proof.

## Open items

- Heavy proof: the 1.0.0 heavy gate on main after CR 168.
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-122` and its branch.
