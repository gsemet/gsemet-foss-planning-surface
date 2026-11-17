# Report: CR 214

PR [#240](https://github.com/gsemet/markdown-okf-schema-studio/pull/240), merged by auto-merge (enabled on the owner's account) 2026-10-31 10:51 (rebase, commit 1b731e66, tree b947fc07 = bab47cf7). Normal CI run 41193718394 green. Heavy: not run on #240 before the merge; the new real-input E2E runs in the heavy on #241 (tree c7da7d4e, includes this change). Opus Inspector APPROVE in rounds 2 and 3.

- Lists of `( )` / `(x)` items render as radio groups (2-item minimum, mixed lists, nested groups, label from the paragraph above); one click writes at most two lines, one undo step; keyboard per the radio pattern.
- Reuses the checkbox toggle path and host guards; the host refuses forged groups.
- README "Decide in the page" (Cream and Dark), demo fixture 74-radio-plan.md, visual v10/v11, writing skill "Choices" row and plan example, QA template radio rule, user docs, CHANGELOG.
- New SwRS-MDOKFSTUDIO-GFM-039 (proposed); GFM-027, CORE-073 edited; StRS GFM-003 generated lines only.
- Screenshots branch push denied ([Out-of-Place Publication]); orphan commit e7ceb521 local only, shots in /private/tmp/claude-502/cr214-driver/shots/.
- Follow-ups in P3: radio-choice-followups.
