# Protected features

These behaviours work today and the user relies on them. A task may change one **only** when the
task file names it under "Intended behaviour changes". Otherwise any change is a regression and the
reviewer must reject the task.

The "Covered by" column lists the automated checks. When a task touches an area whose coverage is
marked *manual*, the reviewer performs the manual check described, or asks the orchestrator to run
the QA skill.

## Rendering

| ID | Behaviour | Covered by |
| --- | --- | --- |
| P-R1 | MyST rendering in process: headings, paragraphs, lists, tables, admonitions (all kinds, titled, nested), figures, footnotes, citations, context tags, GitHub alerts, `diff`/`patch` tinting, syntax highlighting | `test/rendering/mystFeatures.test.ts`, `renderPipeline.test.ts`, `sphinxFeatures.contract.ts`, visual campaign |
| P-R2 | Math with bundled KaTeX, typeset before display; invalid LaTeX stays readable | `mathRenderer` tests in `test/rendering/`, trusted suite (KaTeX stylesheet assertion), visual `check_math_rendering` |
| P-R3 | Mermaid rendered in the webview (`out/bundle/mermaidPreview.js`), source kept on error | visual `06-mermaid-map`, `mystFeatures.test.ts` |
| P-R4 | PlantUML via `plantuml` executable or JAR, injected after render, diagnostic when missing | `test/rendering/plantUmlRenderer.test.ts`, visual `12-`/`13-` fixtures |
| P-R5 | Checkbox markers `[ ]`/`[x]`/`[X]`: interactive in task lists, paragraphs, table cells; literal in code, math, diagrams, link text, headings; toggled by a one-character edit (one undo step); disabled when untrusted | `test/rendering/checkbox*.test.ts`, `scrollSync.test.ts` checkbox tests, `test/integration/checkboxToggle.test.ts` |
| P-R6 | Sticky heading band: `#`-prefixed lines, depth from `stickyHeadingDepth` (**UX-34 frozen**) | `scrollSync.test.ts` sticky tests, visual `check_sticky_headings` |
| P-R7 | Properties table: schema resolution, type icons and labels, enum list, validation classes and badge, missing-required summary, description column collapse (persisted per document), `preview_shows_fields` excerpts, `tooltip_shows_fields`, marker line annotation, YAML-style value display (**UX-24 frozen**) | `test/frontmatter/propertiesTable.test.ts`, `okfFrontmatter.test.ts`, `previewEditing.test.ts`, visual `08-`/`09-`/`10-`/`14-` |

## Navigation and scroll

| ID | Behaviour | Covered by |
| --- | --- | --- |
| P-N1 | Scroll anchoring rules R1–R9 of `docs/scroll-anchoring.md` (fractional source-line anchor, reading line below the sticky band, owner leads, silent programmatic scrolls, anchor persists across renders, R7 edited element stays fixed, text edits shift the anchor) | `test/webview/anchorPolicy.test.ts`, `scrollSync.test.ts`, `test/integration/scroll-sync-suite.ts` |
| P-N2 | Anchor toggle in the toolbar disables both directions without changing the reverse-scroll preference | `scrollSync.test.ts`, scroll suite |
| P-N3 | Click in reading mode reveals the source line; double-click reveal when `doubleClickToSwitchToEditor`; `markEditorSelection` marker | `scrollSync.test.ts`, `test/integration/sourceMapping.test.ts` |
| P-N4 | Links: relative Markdown links open through VS Code, `#heading` and `#L42` select lines, same-document anchors scroll, external links use `openExternal`, unavailable links never fall back to a browser URL | `test/navigation/previewNavigation.test.ts`, `test/webview/linkNavigation.test.ts`, trusted suite |
| P-N5 | Wikilinks `[[Note]]`, `[[folder/Note]]`, `[[Note#Heading\|Label]]`; resolution beside the file, then the workspace folder; ambiguity requires a path; discovery in bounded batches when links enter the viewport; hover shows the path or the reason | `previewNavigation.test.ts`, `linkNavigation.test.ts`, `mystFeatures.test.ts` |
| P-N6 | x-okf-link navigation from the properties table, including the `@implements_req`/`@tests_req` marker line selection; project root behaviour (**UX-22 frozen**) | `test/frontmatter/fileLinks.test.ts`, `previewEditing.test.ts` |

## Editing

| ID | Behaviour | Covered by |
| --- | --- | --- |
| P-E1 | Edit mode toggle (pencil) exists only when editing is allowed (trusted workspace) | `scrollSync.test.ts`, untrusted suite |
| P-E2 | Clicking a mapped block in edit mode opens its exact source range: paragraph, heading, whole list, whole directive (from its title), fenced code (editor outside the `<pre>`), figure, `$$` math, Mermaid fence | `scrollSync.test.ts` ("edit mode opens mapped figures and admonition titles…", "fenced Markdown editors…"), `previewEditing.test.ts`, visual `check_preview_edit_mode` |
| P-E3 | The raw-Markdown editor preserves the block's line breaks and its trailing line ending, autosaves to the same VS Code buffer, commits on blur and Cmd/Ctrl+Enter, and the result re-renders | `scrollSync.test.ts` ("raw Markdown block edits autosave…", "edit mode loads raw Markdown…"), `previewEditing.test.ts` |
| P-E4 | Arrow keys at the start/end of an editor move editing to the previous/next top-level block; the pending navigation survives the re-render | `scrollSync.test.ts` ("arrow boundaries transfer block editing…") |
| P-E5 | Table cell editor: edits one cell; toolbar inserts/deletes rows and columns; the header row and the last body row cannot be deleted; switching cells keeps changes; leaving the table finalizes | `scrollSync.test.ts` table tests, `test/webview/markdownTable.test.ts`, `previewEditing.test.ts` |
| P-E6 | Host-side safety: stale versions and stale requests are rejected; a block that changed in the source while being edited is not overwritten; one inline edit at a time; checkbox toggles refused while a block editor is open | `previewEditing.test.ts`, `checkboxToggle.test.ts`, `scrollSync.test.ts` |
| P-E7 | Frontmatter editing: type-aware controls (enum select, date/time/number inputs, checkbox, text textarea, list editor with drag and keyboard reorder, YAML editor for objects/unknown), key rename with schema suggestions, add/remove field, "Set to null", validation before apply, error state stays open, Escape cancels, **YAML comments preserved** | `scrollSync.test.ts` frontmatter tests, `okfFrontmatter.test.ts`, `previewEditing.test.ts`, visual frontmatter scenarios |
| P-E8 | Read-only (untrusted or standalone) previews never edit, never spawn processes, show the trust notice | `test/integration/untrusted-suite.ts`, `standalone-suite.ts` |

## Lifecycle and chrome

| ID | Behaviour | Covered by |
| --- | --- | --- |
| P-L1 | "Open Preview to Side" creates or reveals one side preview that follows the active **Markdown** editor | `test/integration/lifecycle.test.ts` |
| P-L2 | Open With custom editor (`priority: option`; Text Editor stays the default), stays on its file | `stockCoexistence.test.ts`, `lifecycle.test.ts` |
| P-L3 | Reload Window restores the side preview, its scroll position and edit mode; close/reopen persistence | `test/integration/reload-suite.ts`, `serializer.test.ts` |
| P-L4 | The previewed file deleted or renamed → "missing source" page; recovery when it comes back | `lifecycle.test.ts`, *manual*: QA skill part-2 scenario "external rename" |
| P-L5 | Dirty (unsaved) buffer content is what renders; the production `_build/` is never touched | trusted suite, `dirtySnapshots.test.ts` |
| P-L6 | Live settings (`preview.*`, `frontmatter.*`, `plantuml.*`) apply without reload | `test/configuration/*.test.ts`, *manual*: QA skill part-2 "live settings" |
| P-L7 | Theme modes current/dark/white, persisted per workspace; follows VS Code theme changes | `scrollSync.test.ts`, visual themes |
| P-L8 | Find widget in the preview (`enableFindWidget`), `retainContextWhenHidden` | trusted suite (`findWidgetEnabled`) |
| P-L9 | The extension never edits `markdown.*` settings, never replaces stock preview commands, and coexists with the built-in Markdown preview and editor | `test/security/package-contract.test.ts`, `stockCoexistence.test.ts` |

## Security boundary

| ID | Behaviour | Covered by |
| --- | --- | --- |
| P-S1 | Webview CSP with per-render nonce; no `unsafe-inline`; no remote resources; hostile HTML, event handlers, unsafe schemes, encoded traversal, unsafe CSS URLs removed | `test/security/html-policy.test.ts`, `resource-policy.test.ts`, trusted suite CSP assertions |
| P-S2 | Every message from the webview is validated by `isPreviewSyncMessage` and matched to the current render (`matchesCurrentPreview`); new message types and fields must be validated the same way | `previewEditing.test.ts`, review |
| P-S3 | Local resources canonicalized and symlink-checked within the workspace | `resource-policy.test.ts`, `fileLinks.test.ts` |
| P-S4 | Data from documents reaches the webview only escaped (`escapeHtml`) or through `textContent`/attributes, never through `innerHTML` of unescaped data | review |

## Performance budgets (must not get worse)

| ID | Budget | Covered by |
| --- | --- | --- |
| P-P1 | Render debounce 40 ms; an in-flight render is never killed; finished renders are never discarded as stale | `test/build/buildQueue.test.ts` |
| P-P2 | No extra full webview reloads per keystroke compared with the previous task (UX-28 tasks must reduce them) | T02 navigation counter (added by T29) |
| P-P3 | Sticky heading convergence capped at three passes; frontmatter list previews capped at 50 items | `scrollSync.test.ts`, `propertiesTable.test.ts` |
