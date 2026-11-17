# 07 — Stability, Data Integrity, and Correctness

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers defects that corrupt documents, lose edits, leave the preview in a stuck state, or
raise uncaught errors in the extension host. Lines refer to `e1b4ad0`.

## Findings

### STAB-01 — Frontmatter fence detection truncates the block and table edits corrupt the file

- **Severity**: High (silent document corruption)
- **Confidence**: Confirmed by reproduction
- **Effort**: S
- **Location**:
  [okfFrontmatter.ts:264](../../../../src/frontmatter/okfFrontmatter.ts#L264),
  [okfFrontmatter.ts:277](../../../../src/frontmatter/okfFrontmatter.ts#L277),
  [okfFrontmatter.ts:354](../../../../src/frontmatter/okfFrontmatter.ts#L354),
  [mystRenderer.ts:1263-1270](../../../../src/render/mystRenderer.ts#L1263)

**What happens.**
All four fence patterns have the shape `^---\r?\n([\s\S]*?)(?:\r?\n)?(?:---|\.\.\.)…`.
Because the newline before the closing fence is *optional*, the lazy body stops at the first `---`
or `...` found anywhere, including at the end of a value. A title such as `To be continued...` or a
value ending in `---` closes the frontmatter in the middle of a line.

**Evidence.**
Source document:

```markdown
---
title: To be continued...
author: Ada
status: draft
---
# Body
```

`extractFrontmatter` returns only `{ title: "To be continued" }`; the remaining lines render as
Markdown body (with `---` turning `status: draft` into a setext heading). Editing `status` from the
properties table then writes this file:

```markdown
---
title: To be continued
status: done...
author: Ada
status: draft
---
# Body
```

The title lost its ellipsis, `status` is duplicated, and the new value absorbed the stray `...`.
The schema validation of the candidate patch passes, because it is computed on the same truncated
parse, so no guard stops the write.

**Fix.**
Require the closing fence on its own line, and share one implementation between extraction,
patching, and body stripping:

```typescript
const FRONTMATTER = /^---[ \t]*\r?\n(?:([\s\S]*?)\r?\n)?(?:---|\.\.\.)[ \t]*(?:\r?\n|$)/u;
```

The optional group keeps the empty block (`---\n---`) valid. Export it from one module and use it in
`extractFrontmatter`, `createFrontmatterDocumentPatch`, `createFrontmatterFieldPatch`,
`stripFrontmatter`, and `linkedFileDetails` (which already uses a stricter but different pattern).
As a second guard, refuse to apply a frontmatter patch whose re-parse of the *patched document* does
not contain every key of the original block.

**Tests to add.**
Regression fixtures for values ending in `...`, `---`, `....`, a block containing `---` inside a
quoted string, an empty block, CRLF line endings, and a document without a closing fence.
For each, extraction returns every key and a table edit changes exactly one line.

**Done when.**
No frontmatter edit can change a key other than the edited one.

### STAB-02 — The inline-edit lock survives a webview reload

- **Severity**: High (editing becomes impossible until an unrelated action)
- **Confidence**: Confirmed by code path; not reproduced in a running VS Code
- **Effort**: S
- **Location**:
  [extension.ts:1055-1059](../../../../src/extension.ts#L1055),
  [extension.ts:1158-1205](../../../../src/extension.ts#L1158),
  [extension.ts:2201-2209](../../../../src/extension.ts#L2201),
  [extension.ts:512-591](../../../../src/extension.ts#L512)

**What happens.**
The host records `preview.activeBlockEdit` on the first autosave of an inline block edit and clears
it only on a final save, a cancel, an apply failure, or a text change made *outside* the inline
editor. Any webview document replacement destroys the inline editor without sending a cancel: a save
or autosave (PERF-06), a PlantUML injection, a link-enrichment pass, a theme change, or a settings
change. After the reload, every click on a block posts `previewEditOpen` and receives "Another
Markdown block is already being edited." In the custom editor there is often no text editor on the
same document, so nothing clears the lock until the tab is closed.

**Fix.**
Release a lock whose `requestId` differs from the current stage when a new page reports
`previewReady`, and release it on `onDidDispose`. Additionally, defer non-essential reloads while
`activeBlockEdit` is set (STAB-03). Add a 30 s idle timeout as a last resort.

**Tests to add.**
Integration test: open a block, autosave once, force `updatePreview` (simulate a save), then open
another block; expect success.

**Done when.**
No sequence of reloads leaves the preview unable to open an editor.

### STAB-03 — Any reload destroys an open inline editor

- **Severity**: Medium
- **Confidence**: Confirmed by code path
- **Effort**: S (deferral) to L (with PERF-05 content patching)
- **Location**:
  [extension.ts:1801-1819](../../../../src/extension.ts#L1801),
  [extension.ts:646-675](../../../../src/extension.ts#L646),
  [scrollSync.ts:1657-1738](../../../../src/webview/scrollSync.ts#L1657)

**What happens.**
The inline editor lives in the webview DOM only. `pendingBlockNavigation` is persisted in webview
state, but the open editor, its caret, and any text typed after the last autosave message are not.
With autosave enabled, the user's own save reloads the page and closes the editor while they type.

**Fix.**
While an inline block or frontmatter edit is active, queue reloads (PlantUML injection, enrichment,
save-triggered renders) and apply them when the edit completes. Persist the open edit
(`editId`, block, caret, current text) in `setState` so a forced reload can reopen it.
PERF-05 step 2 removes the reloads entirely.

**Done when.**
Saving, theme changes, and diagram completion never close an open inline editor.

### STAB-04 — PlantUML child-process handling is fragile

- **Severity**: Medium
- **Confidence**: EPIPE confirmed by reproduction; other items by code reading
- **Effort**: S
- **Location**:
  [plantUmlRenderer.ts:162-243](../../../../src/render/plantUmlRenderer.ts#L162)

**What happens.**

- `child.stdin` has no `error` listener. When the process exits before reading its input (bad JVM
  flags, missing JAR inside a wrapper, crash), writing the diagram raises `EPIPE` as an **uncaught
  exception** in the extension host. Reproduced with a stub that exits immediately and a 900 KB
  diagram.
- `stdout += chunk.toString()` decodes each chunk independently, so a multi-byte UTF-8 character
  split across two chunks becomes two replacement characters; non-ASCII labels in large diagrams are
  corrupted.
- `stderr` is accumulated without a limit.
- There is no timeout; a hung process lives until the next render disposes the stage.
- `SIGTERM` targets the direct child only; a wrapper script may leave the JVM running.

**Fix.**
Add `child.stdin.on("error", …)` that settles the promise with a diagnostic; collect `Buffer` chunks
and decode once with `Buffer.concat(chunks).toString("utf8")`; cap `stderr` at 64 KiB; add a timeout
(for example 15 s) that kills the process group (`detached: true`, `process.kill(-child.pid)`).

**Tests to add.**
Spawner-hook tests for an early-exit child (no uncaught exception), a two-chunk split of `é`
(decoded correctly), and a hung child (killed at the timeout).

**Done when.**
No PlantUML failure mode produces an uncaught exception or an orphaned process.

### STAB-05 — Restoring a serialised panel orphans the previous side preview

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:2146-2199](../../../../src/extension.ts#L2146),
  [extension.ts:1896-1922](../../../../src/extension.ts#L1896)

**What happens.**
`deserializePreviewPanel` calls `disposePreview(existingSidePreview, false)` before creating the
restored preview. That disposes the subscriptions of the previous preview (message handler,
`onDidDispose`, watchers) but leaves its *panel* open. When VS Code restores two preview panels
after a reload, the first one stays on screen with frozen content and no handlers; clicks and
scrolls do nothing.

**Fix.**
Either dispose the previous panel too, or let restored panels coexist and give only the most recent
one the `followsActiveEditor` role (the other becomes a fixed preview of its document).

**Done when.**
Every visible preview panel has a live `ActivePreview` behind it.

### STAB-06 — Inline block edits rely on absolute offsets and can be dropped silently

- **Severity**: Medium
- **Confidence**: Plausible (race between two editing surfaces; not reproduced)
- **Effort**: M
- **Location**:
  [extension.ts:1078-1097](../../../../src/extension.ts#L1078),
  [extension.ts:1109-1156](../../../../src/extension.ts#L1109),
  [extension.ts:431-450](../../../../src/extension.ts#L431),
  [extension.ts:913-1038](../../../../src/extension.ts#L913)

**What happens.**
The block's position is a character offset captured at the first save. Any change above the block
(typing in the text editor, a formatter, a frontmatter edit from the table, which is not blocked
while a block edit is open) shifts the text, and the next autosave fails with "The source block
changed". Typing in the text editor also clears the host lock (`refreshPreview`) while the webview
editor stays open; the webview's next autosave then carries a stale `documentVersion` and
`requestId`, `matchesCurrentPreview` rejects it, and the handler returns **without sending an
error**. Text typed in the webview between those two events is lost without notice.

**Fix.**
Track the block as a range and update it from `TextDocumentChangeEvent.contentChanges` (the same
shifting already done for anchors in `shiftAnchorsForEdits`). When an edit message is rejected for
staleness, reply with `previewEditSource` and an explicit error instead of returning silently.
Refuse `previewFrontmatterSave` while a block edit is active, or rebase the block range after it.

**Done when.**
Concurrent edits either rebase the block or surface an error; no edit is dropped silently.

### STAB-07 — GitHub alerts are not recognised in CRLF documents

- **Severity**: Low
- **Confidence**: Confirmed by reproduction
- **Effort**: XS
- **Location**:
  [mystRenderer.ts:122](../../../../src/render/mystRenderer.ts#L122),
  [mystRenderer.ts:386-438](../../../../src/render/mystRenderer.ts#L386)

**What happens.**
`expandGithubAlerts` splits on `\n` only, and `ALERT_MARKER` ends with `[ \t]*$`, so the trailing
`\r` of a CRLF line never matches. `> [!NOTE]` renders as an admonition with LF endings and as a
plain quote with CRLF endings, which is the default on Windows checkouts with `core.autocrlf=true`.

**Fix.**
Split on `/\r?\n/u` and rejoin with the detected line ending, or strip a trailing `\r` before
matching. Audit the other line-based helpers (`openingFence`, `closesFence`) for the same
assumption.

**Done when.**
The rendered HTML of a fixture is identical for its LF and CRLF variants.

### STAB-08 — Inherited object keys are treated as frontmatter fields

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: XS
- **Location**:
  [okfFrontmatter.ts:921](../../../../src/frontmatter/okfFrontmatter.ts#L921),
  [okfFrontmatter.ts:1071-1081](../../../../src/frontmatter/okfFrontmatter.ts#L1071),
  [fileLinks.ts:206-214](../../../../src/frontmatter/fileLinks.ts#L206)

**What happens.**
`name in frontmatter` and `name in value` are true for `constructor`, `toString`, and other
`Object.prototype` members. A schema that declares such a property name reports it as present (never
"missing required") and renders its value as the inherited function.

**Fix.**
Use `Object.hasOwn` everywhere a frontmatter or schema record is probed by name.

### STAB-09 — Per-document state grows without bound

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: XS
- **Location**:
  [extension.ts:814-819](../../../../src/extension.ts#L814),
  [extension.ts:1767-1774](../../../../src/extension.ts#L1767)

**What happens.**
`workspaceState` receives one `descriptionsCollapsed:<uri>` key per document ever previewed, and the
side preview's `states` map keeps one entry per document it has followed. Neither is ever pruned.
The growth is small per entry but permanent for `workspaceState`.

**Fix.**
Store a single bounded map (for example the 200 most recent URIs) under one key, and cap `states`
with the same LRU policy.
