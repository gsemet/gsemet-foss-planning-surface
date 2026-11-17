# batch-05

Opened 2026-11-17T09:59:18Z, closed 2026-11-17T12:38:01Z, parallel, steered by Foreman, no budget, final cost $11.97. [batch-05.json](batch-05.json)

## Completion

| CR | Subject | Result | PR | Rounds | Cost |
| --- | --- | --- | --- | ---: | ---: |
| [CR-336](../261117-1038-336-check-against-minimum-vscode-types/) | Nothing protects the engines.vscode ^1.95.0 minimum: the lock file resolves @types/vscode to 1.140.0, so a change could use a newer API without any check failing. Add a just check step that type-checks src/ against @types/vscode 1.95. Found by the cursor-compatibility spec-writer, 2026-11-14. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/406 | 2 | $1.90 |
| [CR-337](../../6-trash/261117-1018-337-stress-incoming-changes-wait-timeout/) | Stress flake: the incoming-changes scenario timed out once in frame.waitForFunction (30 s) in round 2 of a scoped stress run on CR-328's branch (PR #402). The step was not touched by that CR. Seen once; find the run, the condition it waited for, and whether it repeats. | dropped | - | 0 | $0.61 |
| [CR-338](../261117-1222-338-remove-agents-changes-refs/) | Remove the Studio repository's remaining references to `.agents/changes/`, now that its change requests live in the planning surface. One PR, draft until CI is green; the owner merges by rebase. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/408 | 2 | $2.59 |
| [CR-339](../261117-1057-339-windows-table-breakout-resize-test/) | On Windows, the unit test "Auto measures a table again on a real resize while a cell is edited" (test/page/tableBreakout.test.ts:398) fails, also on origin/main 16105e0f (3 of 3 runs on a fresh install), so `just preflight`'s Windows static stage is red for every change. Found by CR-336's debugger in batch-05 (diagnosis in the planning folder: 4-batch/2-actives/336-check-against-minimum-vscode-types/work/diagnosis.md). Cause undetermined; looks like a Playwright/Chromium layout difference on Windows. Find the cause and fix it so the test passes on Windows and Linux. The owner asked for the fix on 2026-11-17 (« 1. oui fix »); it is the follow-up that runs the long gate after CR-336's waiver. | merged | https://github.com/gsemet/markdown-okf-schema-studio/pull/407 | 1 | $1.87 |

## Cost

- Total: $11.97, no budget
- Chief of Staff, steering the batch and Foreman $5.00 (42%), Drivers $4.60 (38%), workers $2.37 (20%)
- Most: CR-338 $2.59, CR-336 $1.90, CR-339 $1.87
- Chief of Staff, steering the batch and Foreman: 34 wakes, context 170,602 tokens on average, 251,903 at its peak
- Driver chantier:cr-driver with its workers: $6.97 (380 calls)
- Chief of Staff, steering the batch (outside the budget): $2.63 since the batch opened (72 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $1.80 since the batch opened (34 calls, 0 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $12.52 ($4.34 of it in the batch's spend), context 131,187 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)

## Retro

## 2026-11-17 · CR-336, CR-338, CR-339 (batch-05)

- [project] tableBreakout.test.ts:398 asserted a layout that depends on the page font's natural table width (705 px with Segoe UI vs the 727 px a 760 px pane allows), so it was red on Windows on main and made `just preflight` fail for every change until CR-339: long-term fix: tests do not assert font-dependent layout, or pin the font.
- [chantier] `take` and `ship` expect the CR's archive in the PR (`archive missing from the PR` on every CR) although the project gitignores .agents/changes, so each Driver was told by hand not to add one: long-term fix: set `Repo.archive_in_pr` from the project's settings so take and ship skip the archive.

(critic: kept 2, dropped 1)
