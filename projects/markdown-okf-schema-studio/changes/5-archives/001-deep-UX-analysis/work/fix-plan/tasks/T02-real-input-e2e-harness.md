# T02 — Real-input E2E harness and smoke scenarios

| Field | Value |
| --- | --- |
| Fixes | [QA-02](../../08-test-campaign-gaps/QA-02-e2e-injects-messages-instead-of-typing.md) (foundation; each later fix task adds its own failing real-input scenario) |
| Depends on | T00 |
| Gate | `unit trusted` |
| Risk | Low (tests only) |
| Commit message | `test(vscode): add a real-input E2E harness for preview editing` |

## Goal

Create the harness that every interaction fix (T07–T28) uses to prove its bug with **real mouse and
keyboard events**, then add smoke scenarios for behaviour that already works. The smoke scenarios
protect P-E2, P-E3, P-E4 and P-E5 from regressions in later tasks.

## Context to read first

- `test/integration/checkboxToggle.test.ts`. It is the model to follow: CDP connection, the
  `currentPreviewFrame` lookup by document version and request id, real `locator.click()`,
  screenshots and notes, and the `INDEX.md` and `*-LATEST.md` files. **Do not modify it.**
- `test/integration/trusted-suite.ts`: how suites are registered.
- `test/integration/previewEditing.test.ts`, around `const schemaDirectory`: how a schema bundle
  fixture is built (`_schema/<type>.schema.yaml`, matched by the document's `type`).
- `test/integration/review-index.ts`: item list of the stakeholder review index.
- `conventions.md` §6.

## Allowed files

- `test/integration/realInput/harness.ts` (new)
- `test/integration/realInput.test.ts` (new)
- `test/integration/trusted-suite.ts` (register the suite)
- `test/integration/review-index.ts` (add one index item)

## Harness API (`test/integration/realInput/harness.ts`)

Implement and export these functions. Copy the logic from `checkboxToggle.test.ts` where it exists.

```ts
export const MOD: "Meta" | "Control";                 // process.platform === "darwin" ? "Meta" : "Control"
export async function connectWorkbench(): Promise<{ browser: Browser; page: Page }>;  // STUDIO_CDP_PORT, workbench page
export async function waitFor(description: string, predicate: () => boolean | Promise<boolean>, timeoutMs?: number): Promise<void>;
export function createFixture(prefix: string, files: Record<string, string>): { directory: string; path(relative: string): string; dispose(): void };
//   mkdtemp under test/integration/fixtures/<prefix>-*, writes every file (creating folders), dispose() removes the directory
export async function openSidePreview(document: vscode.TextDocument): Promise<void>;  // show in column One, run COMMAND_ID
export async function openStudioEditor(uri: vscode.Uri): Promise<void>;              // vscode.openWith(uri, EDITOR_VIEW_TYPE)
export async function waitForRender(document: vscode.TextDocument, extra?: (html: string) => boolean): Promise<void>;
//   preview.documentUri === document uri, phase "ready", documentVersion === document.version, extra(html) if given
export async function currentPreviewFrame(page: Page): Promise<Frame>;               // visible frame whose html carries the host's current version and requestId
export async function setEditMode(page: Page, on: boolean): Promise<Frame>;          // clicks [data-sphinx-preview-edit-toggle] until data-sphinx-preview-edit-mode matches; returns the current frame
export async function blockEditor(frame: Frame): Promise<Locator>;                   // the open raw-Markdown textarea: [data-sphinx-preview-block-editor] textarea
export async function typeText(page: Page, text: string, delayMs?: number): Promise<void>; // page.keyboard.type(text, { delay: delayMs ?? 25 })
export async function press(page: Page, key: string): Promise<void>;                 // page.keyboard.press
export function bufferText(document: vscode.TextDocument): string;                   // document.getText()
export function lines(text: string): string[];                                       // split on \n
export interface Evidence { directory: string; capture(page: Page, frame: Frame, name: string, note: string): Promise<void>; finish(passed: boolean): void }
export function createEvidence(label: string): Evidence;
//   .artifacts/<label>-* directory with INDEX.md; capture() writes <name>.png and <name>.md (note + current buffer excerpt);
//   finish() writes .artifacts/<LABEL>-LATEST.md with "Suite: **passed|failed**" and a link to INDEX.md
export function writeSchema(directory: string, typeName: string, schemaYaml: string): void; // <directory>/_schema/<typeName>.schema.yaml
export async function closeAllEditors(): Promise<void>;                              // disposeActivePreviewForTests(); workbench.action.revertAndCloseActiveEditor for the fixture; closeAllEditors
```

Rules:

- **Actions** use `page.mouse`, `page.keyboard`, `locator.click()` or `locator.press()` only.
  **Reads** may use `getActivePreviewForTests`, `vscode.workspace` and `frame.evaluate` (reading the
  DOM).
- Never call `sendPreviewMessageForTests` or `locator.fill` in this harness or its suites.
- Import `COMMAND_ID`, `EDITOR_VIEW_TYPE`, `getActivePreviewForTests` and
  `disposeActivePreviewForTests` from `../extensionApi`.
- Every scenario cleans up in `finally`: dispose the preview, revert and close the fixture editor,
  dispose the fixture.

## Smoke scenarios (`test/integration/realInput.test.ts`)

Export `run()`. It connects once and runs the scenarios below in sequence, each in its own function
with its own fixture. Viewport: `page.setViewportSize({ width: 1400, height: 900 })`; close the
sidebar and the auxiliary bar first, as `checkboxToggle.test.ts` does.

Fixture `smoke.md` (exact content):

```markdown
# Smoke document

First paragraph line one
continues on line two.

Second paragraph.

| Name | Value |
|------|-------|
| alpha | one |
| beta | two |

- item one
- item two
```

| ID | Steps (real input only) | Assertions |
| --- | --- | --- |
| RI-S1 paragraph blur commit | Side preview; edit mode on; click the text "Second paragraph."; `End` key; type ` Added.`; click the heading "Smoke document" (moves focus out) | The buffer line `Second paragraph. Added.` exists; the rest of the buffer is unchanged except that line |
| RI-S2 Cmd/Ctrl+Enter | Click "First paragraph"; press `${MOD}+End`; type ` X`; press `${MOD}+Enter` | Buffer line 4 is `continues on line two. X`; no `[data-sphinx-preview-block-editor]` remains after the re-render |
| RI-S3 arrow navigation | Click "Second paragraph."; press `${MOD}+End`; press `ArrowDown` | After the re-render, a block editor is open whose textarea value starts with `\| Name \| Value \|` |
| RI-S4 table cell Enter | Click the cell `one`; press `End`; type `1`; press `Enter` | Buffer contains `\| alpha \| one1 \|` (whole-table formatting may still change before T04; assert only that this row text appears and the row count is unchanged) |
| RI-S5 Open With editor | `openStudioEditor` on the same file; edit mode on; click "Second paragraph."; `End`; type ` Z`; `${MOD}+Enter` | Buffer contains `Second paragraph. Z` |

Capture a screenshot after each scenario's final action, with a short note.

Before writing assertions, check that every scenario works **today**. These are smoke tests of
existing behaviour. If one fails, read the code to see whether your steps or selector are wrong, and
fix the test. If the product is really broken, STOP and report.

## Registration

In `trusted-suite.ts`, import `run as runRealInput` from `./realInput.test`. Call it right after the
checkbox toggle block, in the same try/catch logging pattern:
`console.error("Real-input integration failed:", error); throw error;`.

In `review-index.ts`, add an item "Real-input editing" linking to `REAL-INPUT-LATEST.md`. Copy the
format of the checkbox item.

## Expected changes to existing tests

None. `trusted-suite.ts` and `review-index.ts` gain lines; no existing line changes except
renumbering in the review index, if the list is numbered.

## Must not change

- `checkboxToggle.test.ts`, `previewEditing.test.ts`, and any `src/` file.

## Done when

- The `trusted` gate passes with the new suite included, and its log shows the five scenario names.
- `.artifacts/REAL-INPUT-LATEST.md` says passed, and `INDEX.md` lists five captures.
- `rg -n "sendPreviewMessageForTests|\.fill\(" test/integration/realInput*` finds nothing.
