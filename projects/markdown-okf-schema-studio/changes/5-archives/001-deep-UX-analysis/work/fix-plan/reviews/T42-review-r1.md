# T42 review — round 1

Base: 50cd143. Diff: `scripts/diff.sh 50cd143`.

## A. Scope
- Changed files: `package.json` (`contributes.commands` only) and
  `test/security/package-contract.test.ts` (commands entries + `category?` in the type). Both allowed.
- No frozen behaviour touched, no unrelated churn.

## B. Correctness (D-20, D-13)
- Both commands have `"category": "Markdown OKF-Schema Studio"` and short titles
  "Open Preview to Side" / "Refresh Preview".
- Unchanged: command IDs, `icon` (`$(book)`), `enablement`, `menus`, `keybindings` (no hunks outside
  the two `title` lines and the added `category` lines).
- Palette text: VS Code renders "Category: Title", so the palette still reads
  "Markdown OKF-Schema Studio: Open Preview to Side".
- (Note: the D-20 row in the decisions table describes UX-10. The task uses the D-20 entry in the
  Details section, "Command category", and the implementation follows it.)

## C. Tests
- The expected `commands` deepEqual in "contributes only opt-in …" was updated as the task lists.
  It is still an exact deepEqual and was not weakened. The report says it failed before the
  `package.json` change.

## D. Regressions
- Orchestrator: unit, types and contracts logs show `fail 0`, and tsc ran clean.
- `logs/T42-impl-full.log`: every listed E2E line is PASS. The reload campaign
  (`runReloadCampaign`, which `run-tests.ts` calls last) starts the third VS Code session
  (log lines ~1089–1370). That session ends with `Exit code: 0`, and the log has no "Timed out" or
  error. `reload-suite.ts` is unchanged, and it calls
  `command(page, "Markdown OKF-Schema Studio: Open Preview to Side")` and then waits for the first
  palette row to contain that label (lines 60, 103). A timeout there throws, so a clean exit shows
  that the palette text still matches.
- Protected features: the area is the command and menu contribution, and the entry points are
  covered by `36-title-bar-button`, `05-open-with-editor` and the reload campaign (all pass).
- Items 14–16 (webview, protocol, read-only) do not apply.

## Docs
- `README.md:138` already names the Explorer entry
  "**Open Preview to Side**". Line 140 keeps the palette full title, which is correct. The root
  `README.md` mentions neither title. No doc change is needed.

## Findings
None.

VERDICT: PASS
