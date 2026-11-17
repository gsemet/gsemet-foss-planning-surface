# T37 — A distinct editor name and short tab titles

| Field | Value |
| --- | --- |
| Fixes | [UX-31](../../07-discoverability-and-chrome/UX-31-open-with-label-and-builtin-competitor.md), [UX-32](../../07-discoverability-and-chrome/UX-32-long-tab-titles.md) |
| Decisions | D-14, D-15 |
| Depends on | T36 |
| Gate | `unit full` |
| Risk | Low–medium (reload campaign locates tabs by title) |
| Commit message | `feat(vscode): shorten preview tab titles and rename the Studio editor entry` |

## Goal

- **Open With picker.** The row reads `MyST + OKF Studio   Markdown OKF-Schema Studio`: one
  distinct choice, with the provider shown by VS Code. The extension's own `displayName` does not
  change.
- **Side preview tab:** `Studio · <file name>`. **Open With editor tab:** `<file name>`.

## Context to read first

- `package.json` → `contributes.customEditors[0].displayName`.
- `src/extension.ts`: every `panel.title =` assignment (`updatePreview`, `switchPreviewDocument`,
  `createPreview`), and the `createWebviewPanel` initial title in `openPreview`.
- `test/integration/reload-suite.ts`: it finds the tab by
  `aria-label="Markdown OKF-Schema Studio: reload-evidence.md"`.
- `README.md` → "Use the Preview", the paragraph about the duplicated label in the picker.
- The repository root `AGENTS.md`, "VS Code Extension — Markdown OKF-Schema Studio" → "Identity"
  bullet.

## Allowed files

- `package.json`
- `src/extension.ts`
- `test/security/package-contract.test.ts`
- `test/integration/reload-suite.ts`, and any integration test asserting a panel title
- `README.md`
- `../../AGENTS.md`, i.e. the repository root `AGENTS.md`: the Identity bullet only

## Steps

1. `package.json`: `customEditors[0].displayName = "MyST + OKF Studio"`.
2. `src/extension.ts`:
   - add `function previewTitle(preview: { followsActiveEditor: boolean }, filePath: string): string`.
     It returns `"Studio · " + basename` for side previews, and the basename for Open With
     editors;
   - use it for every title assignment;
   - the initial `createWebviewPanel` title becomes `"Studio"`.
3. Tests: update the expected `displayName` in the contract test and the reload-suite tab locator
   (`Studio · reload-evidence.md`). Run `rg -n "Markdown OKF-Schema Studio:" test` and update every
   title expectation.
4. `README.md`: replace the paragraph explaining
   "Markdown OKF-Schema Studio - Markdown OKF-Schema Studio" with the new picker label and tab
   titles. Add one sentence explaining what Studio adds compared with the built-in Markdown
   Preview and Editor: MyST directives, the OKF properties table and schema validation,
   x-okf-link navigation, inline editing.
5. `AGENTS.md`, Identity bullet: "the extension display name is `Markdown OKF-Schema Studio`; the
   custom editor's display name is `MyST + OKF Studio`; side preview tabs read `Studio · <file>`".

## Tests

- The contract test and title assertions, updated as above.
- An integration assertion: after opening the side preview, `getActivePreviewPanelForTests()?.title === "Studio · <file>"`;
  for an Open With editor, the title is the basename.

## Expected changes to existing tests

- `package-contract.test.ts`: the custom editor `displayName`.
- `reload-suite.ts`: the tab locator.
- Any assertion of `Markdown OKF-Schema Studio: <file>` titles. List each one.

## Must not change

- The extension `displayName`, command titles in the palette, `viewType`s, and the configuration
  title.

## Done when

- The `unit` and `full` gates pass (`full` includes the reload campaign).
