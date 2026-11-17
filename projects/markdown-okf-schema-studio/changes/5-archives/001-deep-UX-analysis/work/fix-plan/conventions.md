# Conventions and pitfalls

Read this whole file before writing code. Every item below has already broken a build or a test in
this codebase.

All paths are relative to `` unless they start with `.agents/` or
the repository root is named.

## 1. Where code lives

| Concern | File | Notes |
| --- | --- | --- |
| Extension host: preview lifecycle, messages, edits | `src/extension.ts` | Not unit-testable (imports `vscode`); covered by integration tests |
| Webview runtime (all preview interactivity) | `src/webview/scrollSync.ts` → `createScrollSyncScript()` | **One big template literal**, see §2 |
| Pure helpers injected into the runtime | `src/webview/markdownTable.ts`, `anchorPolicy.ts`, `linkNavigation.ts` | Stringified with `.toString()`, see §3 |
| Webview HTML assembly, status pages | `src/preview/webview.ts` | |
| All preview CSS | `src/preview/previewStyles.ts` | Tested by regex in `test/webview/previewStyles.test.ts` |
| Toolbar markup | `src/preview/previewToolbar.ts` | |
| Frontmatter parse, validation, YAML patches | `src/frontmatter/okfFrontmatter.ts` | Uses the `yaml` package (`parseDocument`, `keepSourceTokens`) |
| Properties table markup | `src/frontmatter/propertiesTable.ts` | All values through `escapeHtml` |
| x-okf-link resolution | `src/frontmatter/fileLinks.ts`, `stemIndex.ts` | **Do not change resolution rules (UX-22 frozen)** |
| Markdown → HTML | `src/render/mystRenderer.ts`, `checkboxMarkers.ts` | |

Line numbers in the bug sheets refer to commit `e1b4ad0` and drift. Locate code by **function
name or quoted anchor string** (`rg -n "function postBlockEditSave" src`), never by line number.

## 2. The webview runtime is a template literal

`createScrollSyncScript(context)` returns one string: `` `(function () { … })();` ``. Inside it:

- **Never write a backtick or `${`** in runtime code. Build strings with `+`.
- **Double every backslash.** `"\\n"` in the TypeScript source becomes `"\n"` in the webview.
  `/\\r?\\n/u` becomes `/\r?\n/u`. A single `\n` in the TS source becomes a real line break inside
  a JS string literal: a syntax error at runtime that `tsc` does not catch.
- Runtime code is plain JavaScript. TypeScript types, `as`, `!`, `?:` in parameters, and `import`
  are not allowed there.
- Use `window.setTimeout` / `window.clearTimeout`, never the bare globals: the unit-test harness
  provides a fake `window` (§6).
- Guard browser APIs the harness lacks: `document.execCommand`, `caretRangeFromPoint`,
  `caretPositionFromPoint`, `createTreeWalker`, `createRange`. Use
  `typeof document.execCommand === "function"` and similar checks.
- The test `runtime script cannot terminate its containing script element` and every
  `scrollSync.test.ts` test evaluate the generated script in `node:vm`. A syntax error fails all
  of them at once. If ~60 tests fail together, suspect quoting.

**Prefer putting new logic in a separate pure module** (§3) and keep the runtime change to a few
lines of wiring.

## 3. Pure helpers injected with `.toString()`

Pattern (copy it exactly):

```ts
// src/webview/textEditing.ts
export interface TextEdit { start: number; end: number; text: string; caret: number }
export function createTextEditingTools() {
  function continueOnEnter(value: string, selectionStart: number, selectionEnd: number): TextEdit | undefined { … }
  return { continueOnEnter };
}
```

```ts
// src/webview/scrollSync.ts, next to `const tableTools = (${createMarkdownTableTools.toString()})();`
import { createTextEditingTools } from "./textEditing";
…
  const textEditing = (${createTextEditingTools.toString()})();
```

Rules for the factory body:

- Self-contained. No reference to imports, module constants, or other top-level functions; declare
  helpers **inside** the factory.
- No TypeScript-only runtime constructs: `enum`, `namespace`, parameter properties.
- Regular TS source. No backslash doubling here: tsc compiles the file normally and `.toString()`
  returns the compiled JS.
- Unit-test it by importing the factory directly in Node (`createTextEditingTools().continueOnEnter(…)`).
- The esbuild bundle minifies these functions. That is fine as long as they are self-contained.

## 4. Messages between webview and host

- Every new message **type** or **field** sent by the webview must be added to `PreviewSyncMessage`
  and validated in `isPreviewSyncMessage` (`src/extension.ts`): type checks, safe integers, string
  length limits.
- Every edit-like request must go through `matchesCurrentPreview` and, for document edits,
  `currentPreviewDocument` (version check), as existing handlers do.
- Host → webview messages carry `documentId`, `documentVersion`, `requestId`. The runtime ignores
  them unless `sameContext(message)` holds.
- Never trust webview-provided text offsets without re-checking them against the current document
  text (see `drainActiveBlockEdit`, `handleCheckboxToggle`).

## 5. Text, line endings, offsets

- A `<textarea>` normalizes line breaks to `\n`. Documents may be CRLF. Do not "fix" CRLF handling
  (UX-35 is out of scope), but never make it worse. Any range computed on host text must not split
  a `\r\n` pair.
- VS Code offsets (`document.offsetAt`/`positionAt`) are UTF-16 string offsets on `getText()`.
- `previewEditSave` carries the full block text. Its `originalText` must equal the document text of
  the block (`handlePreviewEditSave` checks this).

## 6. Tests

| Kind | Location | Run |
| --- | --- | --- |
| Unit (Node, no VS Code) | `test/**/*.test.ts` except `test/integration` | `scripts/gate.sh <T> unit` |
| Webview runtime | `test/webview/scrollSync.test.ts`, which uses a hand-written fake DOM (`RuntimeElement`, `createRuntime`) | same |
| Contracts (real MyST/Sphinx env) | `test/rendering/*.contract.ts` | `gate.sh <T> contracts` |
| Integration (real VS Code, Playwright over CDP) | `test/integration/*.test.ts`, registered in `trusted-suite.ts` | `gate.sh <T> trusted` |
| Scroll campaign | `test/integration/scroll-sync-suite.ts` | `gate.sh <T> scroll` |
| Reload campaign | `test/integration/reload-suite.ts` | `gate.sh <T> reload` |
| All integration hosts | — | `gate.sh <T> full` |
| Visual (static pages, Python Playwright) | `test/visual/scenarios.ts`, `test/visual/capture.py` | `gate.sh <T> visual` |

Facts about the harnesses:

- The fake DOM in `scrollSync.test.ts` supports only the selectors it lists in `querySelector` and
  `querySelectorAll`. Extend those switch statements when your runtime code queries a new
  selector; do not rewrite the harness.
- The fake `window` has no `setTimeout`. T09 adds a fake timer queue (`window.setTimeout`,
  `window.clearTimeout`, harness `flushTimers()`); later tasks reuse it.
- Real-input E2E tests (added by T02) use `page.mouse` and `page.keyboard` only for **actions**.
  Test hooks (`getActivePreviewForTests`, `vscode.workspace` APIs) are allowed for **reading
  state**. Never use `sendPreviewMessageForTests` or `locator.fill` in a real-input scenario.
- The modifier key is `Meta` on macOS and `Control` elsewhere:
  `const mod = process.platform === "darwin" ? "Meta" : "Control"`.
- Tests that check bugs are written **first**. Run them, see them fail, record the failure excerpt
  in your report, then fix.
- Integration tests run against `out/bundle/extension.js`. The `trusted` gate compiles and bundles
  for you.
- **Locked screen (added by the orchestrator after T07).** The integration suites need an unlocked
  macOS screen. Before a `trusted`/`full` run, check
  `ioreg -n Root -d1 | rtk proxy rg -o '"CGSSessionScreenIsLocked"=\w+'`: `=Yes` means focus and
  undo steps time out (typically checkboxToggle "one undo"). Do not chase those failures and do
  not swap source files to bisect them: run `unit`/`types`, write the report, and state that
  `trusted` is pending on unlock. The orchestrator runs it before committing.
- **Known flake:** `previewEditing.test.ts` "Frame was detached" (about 1 run in 10). Rerun once.
- **Real-input pitfalls on macOS:** use the harness helpers (`withCurrentFrame` for frame access,
  `waitForRender` after a commit, `caretToEnd` instead of `${MOD}+End`). `ArrowDown` does not change
  a focused `<select>`; use type-ahead (press the first letter of the option).

### Changing an existing assertion

Allowed only when the task's **Expected changes to existing tests** lists it. For each one, the
report states the old assertion, the new assertion, and which intended behaviour change requires it.
**Deleting** an assertion is allowed only when the behaviour it checked is intentionally removed,
and the replacement assertion must check the new behaviour. Never weaken a regex to make it match
"anything", and never mark a test `skip`/`todo` to get green, except for the `todo` markers that T01
creates on purpose.

## 7. CSS

- Use VS Code theme variables with fallbacks, as existing rules do
  (`var(--vscode-focusBorder, Highlight)`).
- `test/webview/previewStyles.test.ts` matches declarations **in order inside one rule**. When you
  edit a rule it checks, update that test as listed in the task.
- Three themes must stay readable: current, dark, white (`data-sphinx-preview-theme-mode`).

## 8. Git hygiene

- Never commit. The orchestrator commits after review.
- Never touch files outside the task's **Allowed files**. If you must, STOP and report why.
- Never run repository-wide formatters, `npm audit fix`, or dependency upgrades. Never edit
  `package-lock.json` unless the task says so.
- Do not touch `book/`, `.agents/` (except your report), or anything else the user is editing.

## 9. STOP conditions

Stop and write the report with `STATUS: STOP` (do not try to work around it) when:

1. a required change touches a file not in **Allowed files**;
2. an existing test fails and the task's **Expected changes to existing tests** does not cover it;
3. the task's assumptions about the code are wrong (a function does not exist, a behaviour differs
   from the description);
4. a fix would change a frozen behaviour (UX-22, UX-24, UX-34) or a protected feature that the task
   does not list as an intended change;
5. a gate cannot run in your environment.
