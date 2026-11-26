# CR-512 reproduction runs (2026-11-26)

Head under test: `8df99ce17f42da9e12e9a1656fc70e780cc9ca16` (base branch head; `src/` unchanged in
every run). Windows 11. Before each real-window run and clip take, a process listing showed no
other test or clip VS Code instance.

**Outcome: 2c, cannot reproduce.** Every run below found the cell editor reopened on the header
cell "Task". No reopen failed, so there is no failure trace.

## Real-window scenario (VS Code 1.148.0)

Command (runs 1 to 7), from the worktree in Git Bash:
`env STUDIO_REAL_INPUT_SCENARIO=table-grid-paste [CR512_VARIANT=<names>] fnm exec -- npm run test:integration -- --trusted-only`
(`CR512_VARIANT` was read by temporary code, removed before run 7.)

| Run (log `runN-*.log`) | Condition | Result | Trace, ms from page start: patch/closed, reopened, focused |
| --- | --- | --- | --- |
| 1 header-base | first version of the header scenario, clipboard `writeText`, auto-save off | pass | not captured |
| 2 variant-base | same, sampled for 4 s | pass, editor open on TH row 0 column 0 | 381, 386, 392 |
| 3 variant-copy | clipboard filled by Ctrl+C in VS Code's text editor on `tasks.tsv` | pass, five rows, editor open | 1637, 1642, 1651 |
| 4 variant-autosave | `files.autoSave: afterDelay`, delay 200 ms | pass, five rows, editor open, saved | 419, 425, 432 |
| 5 variant-timing | clip timing: 250 ms, then the clip's table check | pass, open at the check (293 ms) and at 4 s | 823, 829, 839 |
| 6 variant-all | copy, auto-save and timing together | pass, open at the check (299 ms) and at 4 s | 1604, 1610, 1619 |
| 7 final-single | final test code: `scenarioTableGridPaste` then `scenarioTableGridPasteFromHeader` | pass (exit 0) | not captured |
| 8 stress20-header | final test code, 20 rounds in one window | 20/20 pass | not captured |

Run 8 command:
`env STUDIO_REAL_INPUT_SCENARIO=stress STUDIO_STRESS_SCENARIOS=table-grid-paste-header STUDIO_STRESS_REPEAT=20 fnm exec -- npm run test:integration -- --trusted-only`

Paste data types seen by the page: `["text/plain"]` with `writeText` (runs 2, 4, 5);
`["text/plain","application/vnd.code.copymetadata","vscode-editor-data"]` after the editor's own
Ctrl+C (runs 3, 6). No `text/html` in these runs, unlike the specification's table and the
`clip.md` note (inference, not checked: `.tsv` opens as plain text, so VS Code has no coloured
HTML to put).

## Clip takes (VS Code 1.147.0, pinned build; extension VSIX built from the branch)

Commands: `env [CLIP_KEY_COMMANDS=1] CLIP_SCRATCH=<scratch> DEMO_CODE=<pinned 1.147.0 Code.exe> just clip paste-spreadsheet-cells setup --vsix out/reports/package/markdown-okf-schema-studio.vsix`, then the same with `take`.
Records are in `take<N>/` (`verify.json`, `events.json`, `host.json`).

| Take | Setup | Key path | `cellEditorOpenAfterPaste` | `cellEditorOpen` (after Done) | Passed | Trace: patch/closed, reopened, focused |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | fresh | current (`keyboard.press`) | true | false | yes | 9762, 9768, 9775 |
| 2 | take 1's profile | `CLIP_KEY_COMMANDS=1` | true | false | yes | 14974, 14979, 14986 |
| 3 | fresh | current | true | false | yes | 13734, 13741, 13748 |
| 4 | fresh | `CLIP_KEY_COMMANDS=1` | true | false | yes | 17877, 17884, 17894 |
| 5 | take 4's profile | current, final `scenario.mjs` | true | false | yes | not captured |

Takes 1 to 4 ran the scenario with the new record plus a temporary trace record, reading the Done
button once at 4.0 s. Take 5 ran the final scenario (bounded wait, no trace).
`evidence/clip-take1-4.27s-editor-open-after-paste.jpg`: take 1, the editor open in "Task".

Event times from the start of the take (`scratch/take-times.cjs`): the Done click was at 4.44,
4.42, 4.47, 6.64 (take 4: a slow take, the copy already late at 4.12) and 4.61 s (take 5; zoom at
5.14 s against 4.82 s in takes 1 to 3, mark 1 on time at 5.42 s).

## The earlier miss (CR-489, read only)

- CR-489 round 1 (2026-11-25, about 02:13 to 02:19): the editor was not reopened in 3 of 3 runs
  (one take and two probes, one after Ctrl+A). `take1.log`: the table was right and the cell editor
  held "(no cell editor)"; an 8 s probe found no block editor, no edit status, focus on the body.
- CR-489 round 2, the same VSIX: the editor was open (take 3 failed on the header text
  "TaskDoneCancel"; takes 4 and 5 passed with the Done click). Hence the "may or may not" wording.
- `cellEditorOpen` is read after the Done click, so `false` there never showed the state after the
  paste; `cellEditorOpenAfterPaste` now does.
- `git log 3a82969d..HEAD -- src` (3a82969d: a commit adding the clip): 17b779d5, e09285ef
  (charts), 8f6eb3e5 (code width). None touches table editing.
- No page trace was captured at the time, so the cause of those three misses is not established. A
  rare intermittent loss of the pending navigation is not excluded by these runs.
