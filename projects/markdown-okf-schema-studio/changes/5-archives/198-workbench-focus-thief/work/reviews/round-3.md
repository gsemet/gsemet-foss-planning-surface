# Review round 3 — workbench focus thief (test environment only)

Inspector, 2026-10-29. Worktree `markdown-okf-schema-studio-wt-198`, uncommitted work (6 modified,
7 new files, all under `test/`). Follow-up of the three recommendations of round 2.

## Verdict: APPROVE

All three round-2 recommendations are addressed. No new finding.

## Checks

| Check | Result |
| --- | --- |
| 1. No internal CR id in added lines | OK: `git diff` added lines and the 7 new files contain no `CR NNN` and no `#NNN`. `realInput/run.ts` now reads "Does a user's alert type pick (keyboard, real mouse press) reach the file? …" and `stressPlan.ts` "The alert type pick with the keyboard and a real mouse press, logged per pick." |
| 2. `testProfile.ts` header accurate | OK: the header now says the settings are written by `run-tests.ts` and `reload-suite.ts`, and the flags are passed only by `run-tests.ts` ("the reload window gets the settings alone"). Matches the code: `testProfileLaunchArgs` is called only at `run-tests.ts:51` (untrusted) and `:104` (runTests); `reload-suite.ts` calls `writeTestProfileSettings` only. The table row of the flag ("the test windows the launcher starts directly or through runTests") is consistent with that |
| 3. Untrusted launch uses the helper | OK: `run-tests.ts:44` calls `writeTestProfileSettings(userDataDirectory)`; the inline `mkdirSync` / `writeFileSync` is gone. The profile still contains `security.workspace.trust.startupPrompt: "never"` |
| Untrusted window stays untrusted | OK: untrusted args have no `--disable-workspace-trust`; the profile sets no `security.workspace.trust.enabled` (and the unit test forbids it) |
| Unused imports | OK: `fs` and `path` stay used elsewhere in `run-tests.ts` (`existsSync`, `mkdtempSync`, `mkdirSync`, `path.join`); `testProfileUserSettings` is no longer imported there; both imported helpers are used. `tsc` in `just check` passes |
| Gates | `just check`: exit 0 (node tests 3183/3183 + 69/69, pytest 80 passed, `1067 requirements, 0 errors, 0 warnings`). Worktree unchanged afterwards (13 entries, same as before) |

## Notes for the Driver

- Round-2 notes still apply: real proof is the heavy run (alert-dropdown and review-threads green,
  `ALERT-PICK-PROBE` lines in the stress log); keep both `toc` and `alert-type-pick-probe` when
  stacking above #205; no internal ids in the PR body.
