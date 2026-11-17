# T37 implementation — round 1

STATUS: DONE

## Summary
The custom editor display name is now `MyST + OKF Studio`; the extension display name is unchanged.
A new `previewTitle()` helper in `src/extension.ts` titles side previews `Studio · <file>` and Open
With editors `<file>`. It is used at all three title assignments. The initial
`createWebviewPanel` title is `Studio`. README and root AGENTS.md (Identity bullet only) are updated.

## Files changed
- package.json — customEditors[0].displayName
- src/extension.ts — `previewTitle`, three title assignments, initial title
- README.md — picker/tab-title paragraph, one sentence on what Studio adds
- AGENTS.md — Identity bullet
- test/security/package-contract.test.ts, test/integration/reload-suite.ts, test/integration/lifecycle.test.ts

## Tests written first (failing before the fix)
- package-contract "contributes only opt-in ... commands" — `displayName: 'Markdown OKF-Schema Studio'` vs expected `'MyST + OKF Studio'` (unit log T37-red-unit.log)
- lifecycle.test.ts new title assertion — actual title differed from `'Studio · preview.md'` (T37-red-trusted.log). The trusted suite stops at its first failure, so later checks did not run in the red state.

## Tests added or changed
- lifecycle.test.ts — after the side preview opens, `getActivePreviewPanelForTests()?.title === "Studio · preview.md"`.

## Existing assertions changed
- package-contract.test.ts:"contributes only opt-in ..." — old: customEditors displayName `Markdown OKF-Schema Studio` → new: `MyST + OKF Studio` — required by: D-14
- reload-suite.ts (tab locator) — old: `aria-label="Markdown OKF-Schema Studio: reload-evidence.md"` → new: `aria-label="Studio · reload-evidence.md"` — required by: D-15
- No other test asserted a `Markdown OKF-Schema Studio: <file>` title (rg checked; the remaining matches are command titles, fixture text and the aria-label of the preview content).

## Verification
- `PLAN/scripts/gate.sh T37-impl unit types contracts full` → PASS (logs/T37-impl-*.log, full: logs/T37-impl-full.log)

## Evidence for reviewers
- Red-run logs: logs/T37-red-unit.log, logs/T37-red-trusted.log

## Open points
- No integration assertion for the Open With editor title (basename): that panel is owned by the custom editor and no test hook exercises it. The code path is `previewTitle` with `followsActiveEditor === false`.
