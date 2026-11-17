# batch-05: running

Updated 2026-11-17T10:07:27Z · steered by the Chief of Staff (direct mode) · independent PRs (parallel) · spent $0.89 as of 2026-11-17T10:00:39Z · 1 asks unread · 0 orders pending

[All change requests](../STATUS.md)

| CR | Subject | Status | Step | Branch | PR/MR | Long gate | Cost |
| --- | --- | --- | --- | --- | --- | --- | ---: |
| [336](2-actives/336-check-against-minimum-vscode-types/intake/request.md) | Nothing protects the engines.vscode ^1.95.0 minimum: the lock file resolves @types/vscode to 1.140.0, so a change could use a newer API without any check failing. Add a just check step that type-checks src/ against @types/vscode 1.95. Found by the cursor-compatibility spec-writer, 2026-11-14. | [🟡 working Round 2/3](2-actives/336-check-against-minimum-vscode-types/STATUS.md) | coder r2 | `chantier/batch-05/cr-336-nothing-protects-the-engines-vscode-1-95` | - | - | $0.16 |
| [337](2-actives/337-stress-incoming-changes-wait-timeout/intake/request.md) | Stress flake: the incoming-changes scenario timed out once in frame.waitForFunction (30 s) in round 2 of a scoped stress run on CR-328's branch (PR #402). The step was not touched by that CR. Seen once; find the run, the condition it waited for, and whether it repeats. | [🔴 blocked Question 1/3](2-actives/337-stress-incoming-changes-wait-timeout/STATUS.md) | waits for the user | `chantier/batch-05/cr-337-stress-flake-the-incoming-changes-scenar` | - | - | $0.15 |
