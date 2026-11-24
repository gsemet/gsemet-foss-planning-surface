# Verify CR-483 searched-line

Head: 9d956eaafe0addcef4e57abb032ab33be81923f5

Judged at 9d956ea (pushed head, rebased on origin/main: `git merge-base --is-ancestor origin/main HEAD` -> rebased).

## Claims

1. Command `openInStudioAtLine`: declared, palette `when` `resourceExtname == .md && !activeCustomEditorId`, editor/title entry, no keybinding. Proof: `package.json` lines 127, 188-189, 207-209; `keybindings` has no such entry; `node --test out/test/security/package-contract.test.js` -> 14 pass, 0 fail. Host tests `studioLine.test.js` (22 pass with `studioTabNavigation` and `pendingLine`): "Open in Studio at This Line opens the Studio view type in the text editor's group at the caret's line and closes no tab", "... reveals the Studio tab of the file already open in another group", "... tells the reader and opens nothing on a Studio tab, with no editor and on a file that is not Markdown". VERIFIED at 9d956ea.
2. Real window, command associated and default (text tab stays, Studio tab in the same group, marked at 42): `test/integration/openAtLineStudio.test.ts` lines 99-114; step `open-at-line-studio` `STEP done (16546 ms)` in heavy run 45444316305 (headSha 9d956ea, conclusion success, integration/stress/visual/static/static-windows/viewer-graph success). VERIFIED.
3. Link `#heading`, Studio Back/Next, VS Code Go Back/Go Forward, Reopen With Text Editor and `openWith default` stay text, default link opens text with history unchanged, reveal in another group with no second tab, its own history kept: rows at test lines 128-197, same step green on Linux. Unit: `studioTabNavigation.test.js` ("a link that opens a new Studio tab records the move, and the new tab shares the source's history", "a link to a Studio tab that is already open keeps its own history and appends the move to it", "a link from a Studio tab that opens as text records nothing", Back/Next reveal elsewhere), `toolbarReq` amended test "a fixed preview that is not a Studio tab records anchor jumps only; a Studio tab records a link only when it opens in a Studio tab" pass. VERIFIED.
4. Raw-text requests never replaced / no closing code: `grep tabGroups.close` in `src/host-vscode/studioTabs.ts`, `openInStudioAtLine.ts` -> none; only `activation.ts:297` (Open as Text, not in this diff's added lines). Host tests assert no tab closed; real-window rows assert Reopen With Text Editor and `openWith default` stay. Explorer-style opening: `openAtLine.test.ts` step green (`[open-at-line] jump under the association: studio=1 text=0 marks=0`). VERIFIED.
5. Pending line taken once (`pendingLine.test.js` 5 tests; host test "a line delivered to the live Studio tab ... is gone afterwards"). VERIFIED.
6. Probe table: Linux CI log lines `[open-at-line:probe]` (heavy run) show in every associated row `tabUri=-/-`, `selections=none`, `textEditorSeen=false`: no signal, so no automatic signal built (consistent with body). Header comment of `openAtLineProbe.test.ts` matches the body table. The Windows measurement itself was not re-run: UNVERIFIED, added to Known gaps of pr-body.md together with the two Linux default rows that differ (Go to Symbol and Quick Open opened nothing).
7. Requirements: `okfreq lint` reports only W2 broken-link warnings in untouched PALETTE-264, 0 indexes/projections to update; LIFE-196..198 added, LIFE-181, TOOLBAR-059, StRS LIFE-023 amended, log entry present (diff of `requirements/tiers/log.md`). VERIFIED.
8. CHANGELOG line under `## Unreleased` ends `(CR-483 searched-line, PR #500)`; docs `open-studio.md`, `known-limitations.md`, glossary "Line hand-off" updated (git diff). VERIFIED.
9. Gates: `npm run compile` clean at head; `gh pr checks 500` at 9d956ea: static, static-windows, visual, viewer-graph, report pass.
10. PR description: posted body equals `work/pr-body.md` (apart from the Known gaps bullet I added); Summary/Deliverables/Changes match the 61-file diff; no images; Known gaps lists the UNVERIFIED claims (posted body to be refreshed by the Driver with the new bullet).

Out of scope not claimed: 5.1 (not built, justified by the probe).

Verdict: VERIFIED
