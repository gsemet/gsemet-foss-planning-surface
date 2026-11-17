# T36 implementation — round 1

> Transcribed by the orchestrator from the implementer's hand-back message (2026-10-11 02:11):
> the implementer replied with the report text instead of writing this file. Content unchanged.

STATUS: DONE

## Summary
The Studio preview can now be opened from the editor title bar, the Explorer context menu, and `Cmd+K Shift+V` / `Ctrl+K Shift+V`. `openPreview` accepts an optional resource URI from menus. It opens that file first if the file is a `file:`-scheme URI and is not the active editor. Non-`Uri` arguments are ignored. `markdown.*` settings and the built-in preview commands are untouched.

## Files changed
- `package.json` — added `icon: "$(book)"` on openPreview, `menus["editor/title"]`, `menus["explorer/context"]` and `keybindings`, exactly as in the task. The command palette entries, activation events and customEditors are unchanged.
- `src/extension.ts` — `openPreview(uri?: unknown)`. If `uri instanceof vscode.Uri`, its scheme is `file` and it differs from the active text editor's document, it calls `openTextDocument` and then `showTextDocument(doc, { preview: false })`. A failure there shows an error message and returns. With no argument, behaviour is unchanged.
- `README.md` — "Use the Preview" lists the title-bar button, the Explorer entry and the keybinding.
- `test/security/package-contract.test.ts` — see the existing-assertion change below.
- `test/integration/lifecycle.test.ts` — new URI integration check.
- `test/integration/realInput.test.ts` — new scenario RI-T36.

## Tests written first (failing before the fix)
- "contributes only opt-in Markdown OKF-Schema Studio commands" (package-contract) — failure excerpt: `Expected values to be strictly deep-equal` on the commands array (missing icon). The log is `fix-plan/logs/T36-impl-pre-unit.log`.
- The lifecycle URI check and RI-T36 were written before the implementation, but I did not run them against the unchanged code. The `trusted` gate was run only once, after the fix. Without the fix, RI-T36 would find no `.codicon-book` action, since `package.json` had no `editor/title` entry.

## Tests added or changed
- `lifecycle.test.ts`: with another document active, `executeCommand(COMMAND_ID, secondDocument.uri)` makes the preview show that URI and makes it the active text editor. A following `executeCommand(COMMAND_ID, { not: "a uri" })` leaves the preview unchanged.
- `realInput.test.ts`, `scenarioTitleBarButton` (RI-T36): with a Markdown file active and no preview, a real click on `.editor-actions .codicon-book` opens the side preview. It uses `page.locator` and `.click()` only. The evidence screenshot is `36-title-bar-button`.

## Existing assertions changed
- `package-contract.test.ts`, "contributes only opt-in …":
  - The openPreview entry gains `icon: "$(book)"` (and the type gains `icon?`). It is required by the new title-bar icon.
  - Old `assert.equal(menus["editor/title"], undefined)` is replaced by deepEqual on the exact `editor/title` entry. Required by the new title-bar button.
  - New deepEqual assertions cover `explorer/context` and `keybindings`. They are additions, not replacements.
  - `assert.doesNotMatch(serialized, /markdown\./u)` and every other assertion are kept.

## Verification
- `PLAN/scripts/gate.sh T36-impl unit types contracts trusted` → PASS on all four (compile, unit, types, contracts-compile, contracts, trusted-build, trusted). Logs are `fix-plan/logs/T36-impl-*.log`.
- The screen was unlocked: the `ioreg` lock check printed nothing, and `trusted` passed.
- The `trusted` log shows `PASS real-input screenshot: 36-title-bar-button`. That is the only line in the log mentioning RI-T36 or the lifecycle URI check, so the lifecycle check passing is inferred from the suite passing overall.

## Evidence for reviewers
- Screenshot `36-title-bar-button`, produced by the real-input evidence helper in the `trusted` run.

## Open points / STOP reason
- The Explorer entry uses the command's full title ("Markdown OKF-Schema Studio: Open Preview to Side"). The task specifies no separate menu title, so I did not add one.
