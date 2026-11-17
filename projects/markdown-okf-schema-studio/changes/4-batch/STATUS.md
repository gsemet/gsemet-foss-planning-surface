# batch-05: paused

Updated 2026-11-17T12:24:45Z · steered by a Foreman · independent PRs (parallel) · spent $11.87 as of 2026-11-17T12:24:44Z (to date) · 5 asks unread · 0 orders pending

[All change requests](../STATUS.md)

| CR | Subject | Status | Step | Branch | PR | Long gate | Cost |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| [336](3-done/336-check-against-minimum-vscode-types/intake/request.md) | Nothing protects the engines.vscode ^1.95.0 minimum: the lock file resolves @types/vscode to 1.140.0, so a change could use a newer API without any check failing. Add a just check step that type-checks src/ against @types/vscode 1.95. Found by the cursor-compatibility spec-writer, 2026-11-14. | [✅ merged](3-done/336-check-against-minimum-vscode-types/STATUS.md) | - | `chantier/batch-05/cr-336-nothing-protects-the-engines-vscode-1-95` | [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/406) | waived → follow-up windows-table-breakout-resize-test | $1.90 |
| [337](../6-trash/261117-1018-337-stress-incoming-changes-wait-timeout/intake/request.md) | Stress flake: the incoming-changes scenario timed out once in frame.waitForFunction (30 s) in round 2 of a scoped stress run on CR-328's branch (PR #402). The step was not touched by that CR. Seen once; find the run, the condition it waited for, and whether it repeats. | [⚪ dropped](../6-trash/261117-1018-337-stress-incoming-changes-wait-timeout/STATUS.md) | - | `chantier/batch-05/cr-337-stress-flake-the-incoming-changes-scenar` | - | - | $0.61 |
| [338](3-done/338-remove-agents-changes-refs/intake/request.md) | Remove the Studio repository's remaining references to `.agents/changes/`, now that its change requests live in the planning surface. One PR, draft until CI is green; the owner merges by rebase. | [✅ merged](3-done/338-remove-agents-changes-refs/STATUS.md) | - | `chantier/batch-05/cr-338-remove-the-studio-repository-s-remaining` | [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/408) | passed 884949f | $2.59 |
| [339](3-done/339-windows-table-breakout-resize-test/intake/request.md) | On Windows, the unit test "Auto measures a table again on a real resize while a cell is edited" (test/page/tableBreakout.test.ts:398) fails, also on origin/main 16105e0f (3 of 3 runs on a fresh install), so `just preflight`'s Windows static stage is red for every change. Found by CR-336's debugger in batch-05 (diagnosis in the planning folder: 4-batch/2-actives/336-check-against-minimum-vscode-types/work/diagnosis.md). Cause undetermined; looks like a Playwright/Chromium layout difference on Windows. Find the cause and fix it so the test passes on Windows and Linux. The owner asked for the fix on 2026-11-17 (« 1. oui fix »); it is the follow-up that runs the long gate after CR-336's waiver. | [✅ merged](3-done/339-windows-table-breakout-resize-test/STATUS.md) | - | `chantier/batch-05/cr-339-on-windows-the-unit-test-auto-measures-a` | [PR](https://github.com/gsemet/markdown-okf-schema-studio/pull/407) | carried from a18fc89 | $1.87 |

## Paused

- Paused: 2026-11-17T12:24:44Z

## Cost

- Total: $11.87, no budget
- Chief of Staff, steering the batch and Foreman $4.90 (41%), Drivers $4.60 (39%), workers $2.37 (20%)
- Most: CR-338 $2.59, CR-336 $1.90, CR-339 $1.87
- Chief of Staff, steering the batch and Foreman: 34 wakes, context 170,602 tokens on average, 251,903 at its peak
- Driver chantier:cr-driver with its workers: $6.97 (380 calls)
- Chief of Staff, steering the batch (outside the budget): $2.49 since the batch opened (69 calls)
- Chief of Staff, grill and specifications with the user (outside the budget): $1.80 since the batch opened (34 calls, 0 spec-writers, 0 spec critics)
- Chief of Staff, whole session: $12.38 ($4.34 of it in the batch's spend), context 128,186 tokens; not counted: 2 compactions since the batch opened, which leave no record (about $0.12 each)
- Not counted: compaction calls, which leave no record (about $0.12 each)
- To date: it grows if the batch runs again; `close` prices the final cost
