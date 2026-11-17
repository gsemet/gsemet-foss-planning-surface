# T35 — No user-facing "Sphinx"; status pages read as two lines

| Field | Value |
| --- | --- |
| Fixes | [UX-26](../../05-preview-lifecycle/UX-26-status-page-text-and-stale-naming.md) |
| Depends on | T34 |
| Gate | `unit contracts trusted visual` |
| Risk | Low |
| Commit message | `fix(vscode): reword user-facing messages and separate status titles` |

## Goal

- No string a user can see mentions "Sphinx": notifications, status pages, status messages, and
  render errors shown in the preview. Internal identifiers (`data-sphinx-*`, `sphinx-preview-*`,
  `sphinx-myst-*`, function names) do not change.
- Status pages show the title and the message on separate lines.

## Context to read first

- `src/extension.ts`: the `showWarningMessage` / `showInformationMessage` / `showErrorMessage`
  calls, and the messages passed to `setStatus`, `setMissingSource`, `showPending` and
  `buildStatusWebviewHtml`. T13 already removed "Open a Markdown file to use the Sphinx preview."
- `src/preview/webview.ts`: `statusMarkup`, `PREVIEW_STATUS_LABELS`, `buildStatusWebviewHtml`.
- `src/render/*.ts`: error messages that reach the status page (`RenderError`, PlantUML
  diagnostics).
- `src/preview/previewStyles.ts` → `PREVIEW_ACCESSIBILITY_CSS`. It is injected into status pages
  too.

## Allowed files

- `src/extension.ts`, `src/preview/webview.ts`, `src/preview/previewStyles.ts`,
  `src/render/*.ts` (message strings only)
- `test/security/userFacingText.test.ts` (new)
- `test/webview/previewStyles.test.ts`
- Existing tests that assert the old wording. List them; change only the expected strings.
- `test/integration/realInput.test.ts` (add RI-T35)
- `README.md` (only sentences that describe the preview as a Sphinx build to the user; keep the
  architecture notes accurate: rendering is in-process MyST)

## Steps

1. Inventory: `rg -n "Sphinx" src`. Classify each hit as user-facing (string literal shown to the
   user) or internal (identifier, comment, CSS class, attribute). Put the classification table in
   the report.
2. Reword each user-facing string. Use "Markdown OKF-Schema Studio" in notifications and "the
   preview" in in-preview text. Examples:
   - `Sphinx preview navigation blocked: <reason>` → `Markdown OKF-Schema Studio could not follow the link: <reason>`;
   - `Sphinx preview could not open <path>: <error>` → `Markdown OKF-Schema Studio could not open <path>: <error>`.
3. Status layout. In `PREVIEW_ACCESSIBILITY_CSS`, add:

   ```css
   [data-sphinx-preview-status] > strong,
   [data-sphinx-preview-status-message] { display: block; }
   ```

   Also add a small gap (`margin-block-start: 0.25em` on the message).
4. `test/security/userFacingText.test.ts` scans the sources of `src/extension.ts`,
   `src/preview/webview.ts` and `src/render/*.ts` for **string and template literals** containing
   the capitalized word `Sphinx`, and fails on any. The regex must skip comments; a simple
   tokenizer over quotes is enough. An explicit allowlist array is permitted, but each entry needs
   a comment explaining why it is not user-facing.
5. Real-input E2E, scenario **RI-T35**:
   - side preview on a fixture, then delete the fixture file with `fs.rmSync`;
   - the missing-source page appears;
   - capture it with `required: ["status-two-lines"]`;
   - restore the file, and recovery follows (P-L4).

## Expected changes to existing tests

Tests asserting the old notification or status strings. List each one.

## Must not change

- Internal identifiers, CSS class names, message types, and status values.

## Done when

- All gates pass. `userFacingText.test.ts` passes. RI-T35 passes with `status-two-lines` required.

## Amendment before round 1 (orchestrator, 2026-10-11)

T29 and T34 are blocked (see `followups.md`). So the "Preview pending" banner still sits in flow
above the rendered content on every edit. It is one line, about 23 px high, and its height is the
open T29 design question. Step 3 as written would make that banner two lines (about 46 px) and
double the shift at the top of the page on each keystroke. Scope step 3 so it does not:

- In `buildStatusWebviewHtml` (`src/preview/webview.ts`), add the attribute
  `data-sphinx-preview-status-page` to `<body>`. No other markup change.
- The two-line rule (and its gap) applies:
  - on status pages: `[data-sphinx-preview-status-page] [data-sphinx-preview-status] > strong`
    and `[data-sphinx-preview-status-page] [data-sphinx-preview-status-message]`;
  - to every non-pending banner on rendered pages (stale, error, missing-source, recovery):
    `[data-sphinx-preview-status]:not([data-sphinx-preview-status="pending"]) > strong` and the
    same `:not(...)` form for `[data-sphinx-preview-status-message]`.
- A pending banner above rendered content keeps its current one-line layout. `success` stays
  visually hidden.
- Unit tests (`test/webview/previewStyles.test.ts`, and the `buildStatusWebviewHtml` tests if
  they exist):
  - the status page `<body>` carries `data-sphinx-preview-status-page`;
  - `PREVIEW_ACCESSIBILITY_CSS` has no unscoped `[data-sphinx-preview-status] > strong` rule with
    `display: block`. Every such selector carries either `[data-sphinx-preview-status-page]` or
    the `:not([data-sphinx-preview-status="pending"])` guard.
- Existing tests that compare the exact status page html may need the new body attribute. That
  is an expected change: list each one in the report and change only the expected html.
