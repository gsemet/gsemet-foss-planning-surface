# E - Incoming diff, local comments, MyST autodetect, TODO comments (Sonnet deep analysis)

Status: analysis only, nothing implemented. Grounded in the code read on branch dev/gsemet.
Items marked (verify) are inferences from library sources that were not executed (no builds/tests run).

## 0. Facts about the code base that all four features share

- Parser: the JS `myst-parser@^1.7.4` (mystmd), not Python MyST. `src/render/mystRenderer.ts:70-80` loads
  `mystParse` and `mystToHtml` via dynamic import; `renderMyst()` (line ~1462) calls `mystParse(...)` with NO options
  (`:1473`, also `:342`, `:745`, `:1229`). Defaults come from `node_modules/myst-parser/dist/myst.js:12-30`:
  smartquotes, colonFences, frontmatter, math, footnotes, citations, deflist, tasklist, tables, blocks = ON;
  strikethrough = OFF; markdown-it `html: true` (`dist/config.js`), `linkify` off. Directives and roles are always on.
  So today EVERY optional MyST syntax is always on and there is no per-file gate.
- Nothing in `src/` reads `conf.py`. `sphinx/conf.py` is only the standalone contract build config
  (`myst_enable_extensions` there is a fixed list). `src/build/sphinxBuild.ts` and `snapshotWorkspace.ts` are the
  separate build path and are not used by the live preview (`renderPreviewDocument` is in-process, `renderPipeline.ts:117`).
- Render flow: host `renderPreviewDocument` (`renderPipeline.ts:117-236`) -> `renderMyst` -> HTML with `data-line` /
  `data-end-line` (`sourcePositionProperties`, `mystRenderer.ts:481`) -> `rewriteSphinxHtml`
  (`security/html-sanitizer.ts:354`, renames to `data-sphinx-source-line` / `data-sphinx-source-end-line`, `:334-337`)
  -> `annotateSourceMappings` (`mapping/sourceMapping.ts:82`) -> webview. The webview selects mapped blocks with
  `[data-sphinx-source-file][data-sphinx-source-line]` (`scrollSync.ts:124`).
- Diagnostics: `renderMyst` returns `RenderDiagnostic {message,line?,severity}`; `renderPipeline.ts:156-158` wraps them as
  `PreviewDiagnostic` with `code: "myst-diagnostic"`. They reach the user ONLY through the preview status `<aside
  data-sphinx-preview-status>` list (`preview/webview.ts:84-103`, `formatStatusDiagnostic`) and the in-place patch
  (`extension.ts:970-1008`, `diagnosticsFitPatch`). There is NO `vscode.languages.createDiagnosticCollection` anywhere
  in `src/` (grep: no hit), so nothing appears in the Problems panel today.
- Host to webview side channels already exist and are the right pattern for new data that must not go through sanitized
  HTML: `previewPropertiesTable` (`extension.ts:748`), `previewCheckboxResult` (`:1586`), `previewContentPatch` (`:862`),
  `previewPairing` (`:2700`). The host validates inbound messages in a whitelist (`extension.ts:412-510`,
  `type` union at `:112`); new inbound types (comment save) must be added there.
- Edit mode is a webview flag (`scrollSync.ts:105`, `applyEditMode` `:2870`): the rendered blocks become click-to-edit;
  there is no second DOM. So "preview mode" and "edit mode" share the same block elements with `data-sphinx-source-line`.
- Editor changes: `onDidChangeTextDocument` (`extension.ts:3263`) calls `shiftAnchorsForEdits` and `refreshPreview`
  (`:3199`); there is already line shifting logic `shiftLineForEdits` that can be reused for comment anchors.
- No `capabilities` block in `package.json` (untrusted/virtual workspace behavior is therefore the VS Code default:
  extension disabled in untrusted unless declared; preview additionally throws `WorkspaceTrustError` at
  `renderPipeline.ts:118`). Settings live under `markdownOkfSchemaStudio.*` (`package.json:88-160`).
  `extensionDependencies` absent.
- `src/mapping/textDiff.ts` only exports `minimalReplacement` (single prefix/suffix replacement). There is no line diff.

---

## 1. show-incoming-diff (green bar for added/modified lines vs git)

Intent image: native editor gutter, a green vertical bar in a framed region on added/modified lines (a whole fenced block
lines 17-27 is green). Wanted: the same green status in the Studio, for added and modified lines.

### 1.1 Getting the base text (HEAD content)

Option A (recommended): built-in git extension API, soft dependency.
```ts
const gitExt = vscode.extensions.getExtension<GitExtension>("vscode.git");
if (!gitExt) return undefined;               // git disabled/not installed: feature silently off
const git = (gitExt.isActive ? gitExt.exports : await gitExt.activate()).getAPI(1);
const repo = git.getRepository(uri);         // null: not in a repo (outside repo, or git.enabled=false)
const base = await repo.show("HEAD", uri.fsPath);   // string; throws if the file is not in HEAD
```
- No `extensionDependencies` needed; `vscode.git` ships with VS Code. Soft-handle absence (remote/web, git disabled,
  Cursor/VSCodium forks). Types: copy a minimal local interface (`Repository.show(ref, path)`, `state.onDidChange`,
  `state.HEAD`, `getRepository`) instead of importing `git.d.ts` (not published to npm, avoid vendoring the whole file).
- `repo.show('HEAD', path)` needs the path relative-or-absolute accepted (absolute fsPath works in the API) and
  throws for untracked / newly added files: catch, then treat as "no base".
- Alternative B: `repo.diffWithHEAD(path)` returns a unified diff string; parsing hunks `@@ -a,b +c,d @@` gives added/modified
  ranges directly for the SAVED file only. Cannot represent the dirty buffer. Use only as fallback; prefer A with our own diff.
- Alternative C: `git show HEAD:path` via `child_process`: works without the extension but needs trust and a binary; avoid in v1.
- What does the VS Code gutter compare against? The index/HEAD (SCM quick diff, "working tree vs HEAD" incl. staged
  state through the quick-diff provider). `repo.show('HEAD')` equals the common expectation ("incoming" in the intent =
  changed since last commit). Offer a later option `base: HEAD | index` (`repo.show(":0", path)`? use `repo.show("", path)`
  semantics are version dependent) - not v1.

### 1.2 Computing changed lines vs the dirty buffer

Add `src/mapping/lineDiff.ts` (pure, no vscode import, node:test friendly like `textDiff.ts`):
```ts
export interface LineChange { kind: "added" | "modified"; startLine: number; endLine: number } // 1-based, in the NEW text
export interface DeletedMarker { afterLine: number; count: number }
export function diffLines(base: string, current: string): { changes: LineChange[]; deleted: DeletedMarker[] }
```
- Split on `/\r\n|\n|\r/` (same rule as `sourceRangeForLines`, `sourceMapping.ts:44`). Normalize EOL differences: compare lines
  without the terminator so CRLF vs LF (Windows autocrlf) does not mark the file all green. Hash lines (Map<string,int[]>).
- Algorithm: strip common prefix/suffix (cheap, same trick as `minimalReplacement`), then Myers O(ND) on the middle with a
  cap (e.g. D <= 2000 or middle > 20k lines: degrade to "whole middle = modified"). A hunk with both removed and added
  lines = `modified` for the added lines; hunk with only added = `added`; hunk with only removed = `deleted` marker.
  Alternatively use the `diff` npm package (`diffLines`), but a 120-line Myers is dependency-free and testable; the repo
  already avoids dependencies for small helpers (`textDiff.ts`).
- Cost: typical doc < 5k lines, diff after prefix/suffix strip is ~O(N + ND). Dirty-buffer diff on every keystroke is fine
  if debounced; cap guards pathological files. Cache base text per (repo, path, HEAD sha) in a `Map`; invalidate on
  `repo.state.onDidChange` when `repo.state.HEAD?.commit` changes.
- Frontmatter: the renderer shifts positions by the stripped frontmatter lines (`mystRenderer.ts:1466-1474`
  `lineOffset`); data-line values are already in full-file line numbers, so the diff on the raw buffer lines matches directly.

### 1.3 Marking rendered blocks

- Do NOT bake diff state into the sanitized HTML (it changes on each keystroke and defeats `previewContentPatch` keying and
  caching). Send ranges through a side channel: host posts `{type:"previewDiffMarks", documentId, version, changes, deleted}`
  after each render/patch, mirroring `previewPropertiesTable`. The webview applies a class on elements:
  for every `[data-sphinx-source-line]` element compute `[line, endLine]` (`data-sphinx-source-end-line`, fallback line) and
  toggle `data-diff="added|modified"` when the interval intersects a change. Reapply after each content patch (hook where the
  webview re-annotates after `previewContentPatch`; find via `scrollSync.ts` patch handler) - it must be idempotent and clear
  stale attributes first.
- Granularity problem: a block (paragraph, list, fenced code) can span many lines; per-block marking is coarser than the
  gutter. For fenced code and lists, children carry their own data-line only for `listItem`; code blocks are one element,
  so the whole block turns green when any line changes (the image shows exactly a whole fenced block green, so acceptable).
  Nested blocks: mark only the innermost elements (leaf-most), skip an ancestor if a descendant mapped element already
  carries the mark, otherwise a whole list/blockquote lights up for one changed item.
- Style in `previewStyles.ts` (add near the selection-mark rules): `[data-diff]{box-shadow: inset 3px 0 0 var(--okf-diff-added)}`
  with `modified` slightly different (VS Code uses `editorGutter.modifiedBackground` blue and `addedBackground` green; the intent
  asks green for both: use one green token, expose CSS variable
  `--vscode-editorGutter-addedBackground` fallback `#2ea043`). Prefer `box-shadow` or `border-left` on a pseudo-element
  so layout does not shift; check `max-width` margins (`maxContentWidth` setting) so the bar sits on the block edge, or
  position it in the left margin like a gutter. Respect `test/webview/previewStyles.test.ts` / `creamTheme.test.ts` color checks.
- Edit mode: same elements, same CSS; make sure the active block edit textarea/overlay (`activeBlockEdit`) keeps the bar.
  Frontmatter rows: map changed lines in the frontmatter range to the properties-table block (`data-sphinx-...` of the
  table) or skip in v1.
- Deleted lines: render a small red triangle/notch (as VS Code does) as a pseudo-element at the top of the block that follows
  `afterLine` (`[data-diff-deleted-before]`). v1: skip deleted, or notch only. Clicking could expand the removed text (v2).
- Edge cases: untracked/new file -> `show` throws -> base undefined -> either no marks (recommended, noise) or all added;
  intent says "incoming"; VS Code itself shows full green bar for untracked after `git add -N` only. Recommend no marks for
  untracked, all-added for "added to index but not in HEAD" (when `repo.state.indexChanges` shows status INDEX_ADDED).
  No git extension / no repo / file outside repo / virtual doc scheme != `file`: feature off, no error.
  Renamed files: `show('HEAD', newPath)` throws; ignore (v2: use `repo.getObjectDetails`/log --follow).
  Merge conflict / binary / huge (> 1 MB) docs: skip.

### 1.4 Refresh triggers

- Typing: after `refreshPreview` (debounced render already) recompute diff against the cached base (cheap) and post marks.
  Use `document.getText()` of the buffer, not the file, so unsaved edits count (VS Code quick diff does the same).
- Save: no extra work (buffer already used); only needed if base changes.
- Git state: `repo.state.onDidChange` (commit, checkout, stage, reset): refetch `show('HEAD')` when HEAD commit id changed, repost marks.
  Debounce 300 ms; this event fires very often (every status refresh), compare commit sha before refetching.
- Toggle: `markdownOkfSchemaStudio.preview.showIncomingDiff` boolean, default recommended `true` (matches editor behavior) or
  `false` for first release (see ambiguities); plus a toolbar button later (toolbar work belongs to group D). Setting change
  handled in the existing `onDidChangeConfiguration` block (`extension.ts:3270`): add the setting to
  `readPreviewConfiguration` (`src/configuration/...`, mimic `test/configuration/previewConfiguration.test.ts`).
- Untrusted workspace: base text is just git content, safe; still skip when `!vscode.workspace.isTrusted` to stay consistent.

### 1.5 Files touched, size, tests, risks

Files: new `src/mapping/lineDiff.ts`; new `src/git/baseText.ts` (git API adapter, cache, event wiring); `src/extension.ts`
(post message after render, config, dispose listeners; message type union); `src/webview/scrollSync.ts` (apply marks; keep
in a small new module like `webview/linkNavigation.ts` to avoid growing the 3.6k-line file, but the runtime is bundled
as a string in `scrollSync.ts`, see how `linkNavigation.ts` is wired); `src/preview/previewStyles.ts`; `package.json`
(setting); `src/configuration/previewConfiguration.ts` (setting read).
Size: M (S for the pure diff + styles, M due to git adapter + patch reapply).
Tests: `test/mapping/lineDiff.test.ts` (mimic `test/mapping/textDiff.test.ts`: identical, added, modified, deleted, CRLF vs LF,
cap fallback); `test/webview/` marks test mimicking `contentPatch.test.ts` / `scrollSync.test.ts` DOM harness
(`test/rendering/dom.ts`) to check class application with nested blocks; `previewConfiguration.test.ts` for the setting;
`test/security/package-contract.test.ts` for the new setting contract; adapter with a fake `getAPI` object.
Risks: coarse block granularity vs gutter expectation; reapply after patch causing flicker/layout shift; git event storm;
CRLF false positives; huge diff cost; the patch comparison key (`contentPatch.ts` shell key) must not include marks.

---

## 2. local-comment-mode (Confluence-like threaded comments, sidecar JSON)

### 2.1 Selection to anchor

- Webview already reads selections (`scrollSync.ts:147`, `window.getSelection`) and maps blocks by line. On `selectionchange`
  / mouseup with a non-collapsed selection inside `#sphinx-myst-preview-content` (ignore selections inside code-edit
  textareas, mermaid, properties table):
  - Find the nearest ancestor `[data-sphinx-source-line]` for range start and end (as `scrollSync.ts:3128`) -> `startLine`,
    `endLine` (end ancestor's end-line).
  - `quote` = `selection.toString()` (collapse whitespace), plus `prefix` / `suffix` = up to 32 chars of the block's
    `textContent` before and after the selection (Hypothesis/W3C TextQuoteSelector pattern).
  - Because the rendered text differs from the Markdown source (markup chars), a more robust v1 anchor is the SOURCE text
    of the block: host receives `{startLine, endLine, quote, prefix, suffix}`, finds `quote` inside the source lines
    `[startLine, endLine]` (try exact, then after stripping common inline markup `*_\`[]`), and stores both `line`/`endLine`
    and `quote`. If the quote cannot be located in source, fall back to the block lines only (comment on the block).
- Floating button: absolutely positioned `<button>` near `range.getBoundingClientRect()`, hidden on collapse; in edit mode
  disable while a block edit is active.

### 2.2 Sidecar format `<name>.comments.json` (next to the document)

```json
{
  "version": 1,
  "document": "notes.md",
  "threads": [{
    "id": "t_8f3a",
    "anchor": { "line": 42, "endLine": 42, "quote": "selected text", "prefix": "...", "suffix": "...", "contentHash": "sha1-of-block-source" },
    "resolved": false,
    "createdAt": "2026-10-15T10:00:00Z",
    "comments": [{ "id": "c_1", "author": "Gaetan Semet", "createdAt": "...", "editedAt": null, "body": "markdown text" }]
  }]
}
```
- Name: `notes.md` -> `notes.comments.json` (intent). Deterministic path from the document path; do not store absolute paths.
- Author: `git config user.name` via the same git API (`repo.getConfig('user.name')`; `Repository.getGlobalConfig` fallback),
  override setting `markdownOkfSchemaStudio.comments.author` (string, empty = use git, final fallback OS user / "Anonymous").
- Stable JSON (sorted keys by construction, 2-space indent, trailing newline) to keep git diffs small.

### 2.3 Re-anchoring after edits

- While the doc is open: reuse `shiftLineForEdits` (`extension.ts` `shiftAnchorsForEdits` at `:2668`) to move `line/endLine`
  on each content change event, in memory; persist to sidecar only when threads are modified (not on every keystroke), or on
  save (`onDidSaveTextDocument`) so the sidecar does not churn.
- At load / when the doc changed externally: for each thread, check the quote at `line`; if absent, search the quote in a
  window (+-50 lines) then whole document: exact first, then normalized-whitespace, then fuzzy (Bitap/Levenshtein <= 20 %
  of quote length, prefix/suffix scoring). Result states: `anchored`, `moved` (update line), `orphaned` (keep thread, show
  in the panel's "Orphaned" section, never delete).
- Pure helper `src/comments/anchoring.ts` (testable).

### 2.4 Rendering

- Host sends `previewComments {threads with resolved anchors}` side channel (as for diff). Webview wraps the quote range
  in `<mark data-comment-thread="id">` by walking text nodes of the target block (must be reapplied after each content patch;
  skip code blocks/mermaid; if the quote cannot be found in rendered text, put a margin badge on the block instead). A
  highlight must not break `data-sphinx-source-*` mapping: wrap only inside the text, not around block elements.
- Thread UI: v1 right-side popover anchored to the highlight / badge (single thread, reply textarea, Resolve, Delete).
  Full: a collapsible side panel listing all threads, filter open/resolved, jump to anchor.
  All user text rendered with `textContent` (never innerHTML); comment bodies plain text in v1 (markdown later via the
  host renderer).
- Webview to host messages (add to the whitelist `extension.ts:412`): `commentCreate`, `commentReply`, `commentResolve`,
  `commentDelete`, `commentEdit`. Host owns the file; webview never writes.

### 2.5 Persistence, watcher, trust, git

- Write with `vscode.workspace.fs.writeFile(uri, TextEncoder)` (works for remote/virtual); read via `workspace.fs.readFile`.
  Serialize writes through a per-document promise queue; read-modify-write on the latest file (to merge with an external
  change) plus a content-hash check before overwriting; atomic enough via temp+rename is not available in `workspace.fs`
  (`rename` exists: write `.tmp` then `rename`, optional).
- Watcher: `createFileSystemWatcher(RelativePattern(dir, "<name>.comments.json"))` per open preview (existing watchers at
  `extension.ts:302,1057,2804` are the model); on change reload and repost, ignoring our own write (compare hash/mtime).
- Untrusted workspace: preview is already disabled until trusted (`WorkspaceTrustError`); comments are data only, JSON.parse
  with schema validation (`version`, array/length/string limits; mimic `frontmatter/schemaValidator.ts`); reject files > 2 MB.
- readOnly (document `isReadonly`, virtual fs, git-diff scheme): show threads, hide create/reply.
- The sidecar appears in git as an untracked file. This is by design (shared review). Offer
  `markdownOkfSchemaStudio.comments.sidecarLocation`? No: keep one rule. Mention in README; users can `.gitignore`
  `*.comments.json`. The file explorer will list it (consider `files.exclude` suggestion in docs only). Also the
  stem/frontmatter indexers (`stemIndex.ts`, watchers on `**/*.md`) are unaffected because it is `.json`.
- Renames: `onDidRenameFiles` handler exists (`handleRenames`): also rename the sidecar (`workspace.fs.rename`), update its
  `document` field.

### 2.6 v1 vs full

v1 (M-L): create thread from selection (quote + line), add reply, resolve/reopen, delete thread; author from git/setting;
highlight + popover; re-anchor by line shift while open plus quote search +-N lines on load; orphan list as a simple
section; sidecar read/write + watcher. Plain text bodies. Preview and edit mode both (selection works in both; button off
during an active block edit).
Full (L-XL): side panel with filters, fuzzy re-anchor with scoring, comment edit/delete per comment, markdown bodies,
mentions, @-notifications none, export of comments into the PDF/build, VS Code native Comments API in the text editor
(`vscode.comments.createCommentController`) sharing the same sidecar so threads appear in the source editor too, rename
handling, multi-window locking.

Files touched: new `src/comments/{model,sidecar,anchoring,author}.ts`; `src/extension.ts` (messages, watcher, config,
dispose); `src/webview/scrollSync.ts` (+ new `webview/commentsUi.ts`); `src/preview/previewStyles.ts`;
`package.json` (setting author, optional enable flag); README.
Size: L (v1 M-L). Tests: `test/comments/anchoring.test.ts`, `sidecar.test.ts` (schema validation, malformed JSON, size limit;
mimic `test/frontmatter/*` pure tests and `test/security/html-policy.test.ts` for hostile content), `test/webview/comments.test.ts`
(DOM harness like `scrollSync.test.ts`: selection to anchor, highlight idempotent after patch), `package-contract.test.ts`.
Risks: highlight wrapping breaks text editing / checkbox handlers / click-to-edit hit targets; re-anchoring wrongness
(silent mis-attachment is worse than orphaning, prefer orphan when score low); concurrent writers; the 158 KB scrollSync
runtime growth; XSS via comment text (use textContent; CSP already restrictive); sidecar noise in commits.

---

## 3. myst-autodetect (extension detection + warning; clickable URLs already done in 292b498)

### 3.1 Current state

See section 0: no extension flags are passed; defaults ON: smartquotes, colonFences, math (dollarmath), deflist,
tasklist, footnotes, citations, frontmatter, tables, blocks; OFF: strikethrough (`myst.js:26`). Because JS mystmd does not
implement all Sphinx myst extensions, a one-to-one mapping to Python `myst_enable_extensions` is partial:

| Python extension | JS parser today | AST signal for "used" |
| --- | --- | --- |
| `colon_fence` | `colonFences:true` (always) | `mystDirective` node whose source line starts with `:::` (check `position` + source line) |
| `dollarmath` | `math:true` (always) | node types `math`, `inlineMath` where source text has `$` delimiters (vs ```{math} directive) |
| `deflist` | on | `definitionList` |
| `tasklist` | on | `listItem` with `checked` != undefined / our checkbox nodes (`checkboxMarkers.ts`; note: `[ ]` markers are custom-handled, `mystRenderer.ts:1466`) |
| `strikethrough` | off | `delete` nodes (only if enabled) - or scan `~~x~~` outside code |
| `substitution` | not supported by parser (`{{ var }}` stays text/maybe role) (verify) | regex `\{\{[^}]+\}\}` in text nodes outside code/inlineCode |
| `fieldlist` | not supported (verify) | lines `^:name: value` at block start in paragraph text |
| `attrs_inline`/`attrs_block` | not supported | `{#id .class}` after inline / `{#id}` line above block |
| `html_admonition` / `html_image` | raw html handled separately | `html` nodes starting with `<div class="admonition">` / `<img` |
| `linkify` | off | bare URLs: handled by our own `autolinkBareUrls` (`mystRenderer.ts:1321`), NOT the extension: never warn |
| `replacements`, `smartquotes` | smartquotes on | skip detection (low value / noisy) |

Recommended v1 detection scope: `colon_fence`, `dollarmath`, `deflist`, `tasklist`, `substitution`, `fieldlist`,
`attrs_inline/attrs_block`, `strikethrough`, `html_admonition`, `html_image`. Skip `smartquotes`, `replacements`, `linkify`,
`amsmath`, `attrs_*` if too costly.

### 3.2 Finding and reading conf.py without executing it

- Resolution: start at `dirname(document)`, walk up to the workspace folder root (stop at it; at filesystem root if outside
  any workspace), first directory containing `conf.py` wins (also accept `docs/conf.py` / `source/conf.py` children of the
  root as a secondary lookup: Sphinx projects commonly keep `conf.py` in `docs/` or `source/`, and a doc in `docs/foo/x.md`
  finds `docs/conf.py` by walking up anyway; the sibling-lookup matters only for docs at repo root; v1: walk-up only).
  Use `vscode.workspace.fs` or `node:fs` like `stemIndex.ts` (the code mixes both); cache `Map<dir, {path|null, mtime}>`.
- Parser `src/sphinx/confParser.ts` (pure, no vscode import): a tiny tokenizer, NOT a Python evaluator.
  1. Strip comments (`#` to EOL outside strings) and keep string literals (single/double/triple quotes, prefixes r/u/f ignored).
  2. Find assignments at column 0: `^(extensions|myst_enable_extensions|myst_heading_anchors|...)\s*(\+?=)\s*` then read a bracketed
     list `[`...`]` or tuple `(`...`)` with bracket depth counting across lines, collecting string literals only; handle
     trailing commas, nested comments, implicit concatenation ("a" "b" -> ignore).
  3. `+=` and `x.append("a")` / `x.extend([...])` at column 0: union into the list. `myst_enable_extensions = ["a"] + [...]`:
     collect all literals in the expression.
  4. Anything non-literal (names, function calls, conditionals, `myst_enable_extensions = my_list`): mark result `uncertain`
     and degrade to "do not warn" (see 3.3).
  5. Also `myst_all_links_external`, `myst_enable_checkboxes`(old tasklist), `myst_heading_anchors` not needed.
- Result type: `{ found: true, mystEnabled: boolean (extensions includes "myst_parser" or "myst_nb"), extensions: Set<string>, certain: boolean }`.
  "myst_parser" absent from `extensions` -> the file is likely not MyST-processed at all (or uses `recommonmark`); then the
  gate is "all optional syntax unsupported" but only warn when `certain`.
- Never use `child_process`/python (untrusted workspaces, performance, the intent says "look if enabled and detect extension").

### 3.3 Semantics when there is no conf.py ("per-file feature gate")

The intent: "keep MyST features behind a feature gate per file". Recommend:
- no conf.py found: gate OPEN (all features on, no warnings). Rationale: the preview currently renders everything, users
  of Obsidian-style vaults have no Sphinx; warnings there would be pure noise. Optional setting
  `markdownOkfSchemaStudio.myst.extensions` (string[] | "auto") to force a list, default `"auto"`.
- conf.py found, parsed `certain`: gate per extension per the list. Gate means WARN, not disable rendering, in v1
  (rendering the construct as the editor shows it keeps the preview WYSIWYG; the warning explains why a Sphinx build will
  differ). Offering real disabling (pass options to `mystParse({extensions:{...}})`, `mystRenderer.ts:1473`) is feasible for
  `deflist`, `tasklist`, `math`, `colonFences`, `strikethrough` but changes output: v2, opt-in.
- conf.py found but uncertain: no warning (avoid false positives), maybe a single info line "conf.py could not be statically analyzed".
- Frontmatter-level override (per file): `myst:\n  enable_extensions: [...]` in YAML for files outside a Sphinx project (mystmd
  frontmatter is `project/myst` keys). Optional; ambiguity below.

### 3.4 Detecting usage and message

Emit from `renderMyst` (it has the AST and the source) a new pass `detectOptionalSyntax(ast, source) -> Usage[]` where
`Usage = {extension, label, line}`, one entry per extension (first use line, plus count), skipping `code`, `inlineCode`,
`html` nodes (reuse the skip list at `mystRenderer.ts:1292`). The gate (enabled set) must be passed in through
`MystRenderContext` (new optional `enabledExtensions?: ReadonlySet<string>`), computed in `renderPipeline.ts` next to
`resolveInclude`, so `renderMyst` stays pure/testable. Message exactly as the intent:
"Warning: `XXX` is used but this is behind the extension YYY, which does not seem enabled in your config.py. Please install
extension "YYY" and register in `myst_enable_extensions`". Note: "install" is wrong for built-in extensions (they are just enabled
in `myst_enable_extensions`); recommend rewording to "Please enable "YYY" in `myst_enable_extensions` (conf.py)" - ambiguity.
XXX = the syntax sample (e.g. `:::` fence, `$...$`), YYY = Python extension name. Severity "warning" with `line`.
Includes: diagnostics in included files should be attributed to the included file or skipped (include expansion at
`mystRenderer.ts:689`); v1 only analyze the active document's own AST before include expansion (call the detector right
after `mystParse`, before `expandIncludes`).

### 3.5 Where to show

- Preview banner: free, already works via `RenderDiagnostic` -> status `<aside>` (`preview/webview.ts:84`). Multiple items
  OK; the list is bounded by `MAX_PATCH_DIAGNOSTICS` (`scrollSync.ts:217`), so cap at ~10 and aggregate counts.
- Problems panel: add `vscode.languages.createDiagnosticCollection("markdownOkfSchemaStudio")` in `extension.ts`, set from
  `result.diagnostics` for entries with `line` (range = whole line, `DiagnosticSeverity.Warning`, code `myst-extension`),
  clear on dispose/close/doc change. This is also where the "error line" in the editor comes from (squiggle on the line),
  which matches the intent ("display an error line"). Recommended: do both; banner for preview-only users, collection for editor.
- Quick fix (v2): code action "Add `x` to myst_enable_extensions" editing conf.py.

### 3.6 Caching and invalidation

Cache per conf.py path keyed by mtime+size: `Map<confPath, {mtimeMs,size,parsed}>`; the nearest-conf lookup cached per directory
with negative caching (`null`) and invalidated when a `conf.py` is created/deleted: single watcher
`createFileSystemWatcher("**/conf.py")` (pattern excluded for `IGNORED_WATCH_SEGMENTS`, `extension.ts:2553`), on any event clear
caches and re-render active previews (`updatePreview`/`refreshPreviewDocument`, as the config-change handler at `:3270` does).
Render path must not do synchronous disk walks on every keystroke: resolve once per document open and on watcher events,
store on `ActivePreview`.

### 3.7 Files, size, tests, risks

Files: new `src/sphinx/confParser.ts`, `src/sphinx/confLocator.ts`; `src/render/mystSyntaxDetect.ts` (AST pass);
`src/render/mystRenderer.ts` (context option + hook); `src/render/renderPipeline.ts` (inject enabled set); `src/extension.ts`
(watcher, DiagnosticCollection, per-preview cache); `package.json` (setting `myst.extensions`/`myst.warnOnDisabledExtensions`).
Size: M (parser S, detection M because of per-syntax heuristics, UI S).
Tests: `test/rendering/confParser.test.ts` (multi-line, `+=`, append, comments, tuples, uncertain cases; mimic
`bareUrlAutolink.test.ts` pure style), `test/rendering/mystSyntaxDetect.test.ts` (each syntax, none inside code fences; mimic
`mystFeatures.test.ts` which uses `renderMyst` directly), a `renderPipeline.test.ts` case that diagnostics carry code
`myst-extension` and line, `test/security/userFacingText.test.ts` (checks user-facing text; the new message must pass it).
Regression risks: false positives on `$` (currency, prices) and `:::` inside blockquote/indented code; `{{ }}` in Jinja-like docs;
warning noise in non-Sphinx repos with a stray `conf.py` (e.g. pelican/other tools): mitigated by requiring `myst_parser`
in extensions; Windows paths; large `conf.py`.

---

## 4. todo-comments (HTML comments and TODO as inline chips)

### 4.1 Today's behavior

- Block `<!-- ... -->` (starting a line): markdown-it `html_block` -> mdast `html` node (`tokensToMyst.js` html_block map).
  `mystToHtml` has no `html` handler; the pipeline only special-cases raw `<table>` (`normalizeRawHtmlTable`, `mystRenderer.ts:1040`)
  and context-tag blocks (`:195`, `:321`). Raw html otherwise is dropped by mdast-util-to-hast (no `allowDangerousHtml`,
  `renderMdast.js:7-17`; verify by running `renderMyst("<!-- x -->")`) -> the comment disappears silently from the preview.
- Inline comments (`text <!-- c --> text`): markdown-it inline `html_inline` -> `html` inline node, also dropped.
- `% line comment` (MyST): `myst_line_comment` -> `comment` node -> hast `comment` (`schema.js:77`) -> serialized `<!-- -->`
  into the DOM, invisible. Not in the intent but treat like HTML comments (same chip, "%").
- The sanitizer (`html-sanitizer.ts`) is parse5-based: parse5 keeps comment nodes (nodeName `#comment`); nothing in the file
  matches `comment` (grep), so a comment would pass through unchanged; there is no stripping step. `rawHtmlChildren` drops
  `#comment` inside raw html tables (`mystRenderer.ts:567`).
- `TODO` is plain text: rendered as ordinary text, no special handling anywhere.
- Source mapping: dropped nodes produce no element, so there is nothing to click and no data-line for them.
- Fenced/indented code: parsed as `code` nodes, never `html`; comments inside are literal text and already safe.
- Frontmatter is stripped before parsing (`stripFrontmatter`), so `<!--` in YAML never reaches the parser.

### 4.2 Proposal

Preprocess in the AST (same stage as `autolinkBareUrls`, `mystRenderer.ts:1321`), converting `html` nodes whose value is a
comment into hast nodes, and splitting `TODO` out of text nodes:

1. Block comment (`html` node, `value` matches `^<!--[\s\S]*-->\s*$`, possibly multi-line; `position.start/end.line`
   give the span): `setHast(node, "div", {class:"okf-comment", "data-line": start, "data-end-line": end, "data-kind":"comment"},
   [chip, body])`, where chip = `<button class="okf-chip okf-chip-comment" aria-expanded="false">&lt;!--</button>` and body =
   `<div class="okf-comment-body" hidden role="note">` with the comment text (escaped through hast text, so it is safe).
   Multi-line comments: body keeps line breaks (`white-space: pre-wrap`).
   An `html` node holding comment PLUS other markup (e.g. `<!-- x --><div>`) -> leave as is (rare).
2. Inline comment (`html` child of paragraph/heading/listItem with a comment value): hast `span.okf-chip-inline` + hidden
   `span.okf-comment-body`; expansion shown as an inline-block admonition below the line (CSS `display:block` when expanded).
   Multi-line inline comments appear as a single html_block or as several `html` nodes: markdown-it only joins when `<!--`
   starts the line (block) or within one paragraph (inline); handle both.
3. TODO: in `text` nodes (outside `code`, `inlineCode`, `html`, `link`, `mystRole`, `math`: copy the skip set from
   `autolinkBareUrls`, `:1322-1330`) match `\bTODO\b(?:\([^)]*\))?:?\s*(.*)$` (case-sensitive; also optionally `FIXME`, `NOTE`?).
   Replace the match with `span.okf-chip.okf-chip-todo` "TODO" and, for the rest of the line, the text stays visible by
   default (since a TODO is usually inline prose: "TODO: write intro"). Clicking the chip toggles an admonition-like
   zone below the block showing the text; v1 simpler: chip is a styled badge only, click toggles a highlight of the sentence.
   Ambiguity below. Also a TODO inside an HTML comment (`<!-- TODO ... -->`): chip kind is `todo` (green) instead of
   gray, label "TODO".
4. Client behavior: webview delegate click on `.okf-chip` toggles `hidden`/`aria-expanded` on the sibling body; expansion
   state is kept per (line) in a Map saved in the existing webview state (`savedState`, `scrollSync.ts:106`) so it survives
   content patches (otherwise `previewContentPatch` collapses everything on each keystroke). Add keyboard (Enter/Space).
5. Styling in `previewStyles.ts`: gray chip `<!--`, green chip `TODO` (use theme variables like existing alerts/callouts; look at
   the admonition styles `aside.admonition` for the expanded zone: reuse `.admonition` classes: body is
   `div.admonition.okf-comment-note` with `p.admonition-title` "Comment"/"TODO"). Dark/cream theme checks in
   `test/webview/creamTheme.test.ts`.
6. Edit mode: block edit works by line range (`sourceRangeForLines`, `sourceMapping.ts:37`). A comment block now emits an element
   with data-line/end-line, so click-to-edit on the body (not the chip) opens the block editor with the raw `<!-- ... -->`
   source: round trip is exact since the editor replaces source lines, not rendered text. The chip click only toggles. Verify
   that the block editor does not treat `div.okf-comment` as non-editable (it currently ignores unmapped nodes, `scrollSync.ts:2547`).
   Inline chips inside paragraphs edit with the paragraph (existing behavior), the chip's rendered text must not leak back
   into saved source: the inline editor works from source lines, not DOM text, so safe; confirm in `textEditing.ts`.
7. Comments inside code blocks: untouched by construction (AST based; do not use regex on source). Also `% ` lines inside
   fenced directives: `code` nodes.
8. Sanitizer: new classes/attributes (`class`, `hidden`, `aria-expanded`, `role`, `button`) must survive `rewriteSphinxHtml`;
   `button` is not in `REMOVED_ELEMENTS` (`html-sanitizer.ts:55`) but check for `onclick` stripping policy and CSP (no inline
   handlers: use delegated listener). Prefer `span role="button" tabindex="0"` to avoid `<button>` inside `<a>`/headings oddities.
9. Printing/build: the Sphinx build path is separate; chips exist only in the live preview renderer. If PDF/HTML export of the
   preview reuses `renderMyst`, add an option `showComments` default true.
10. Setting: `markdownOkfSchemaStudio.preview.showComments` (default true) so people can hide chips; plumbed like other preview
   settings, read in `renderMyst` context or hidden by CSS class on body (cheaper, no re-render): recommend the CSS route.

### 4.3 Files, size, tests, risks

Files: `src/render/mystRenderer.ts` (new pass `markCommentsAndTodos`, ~100 lines; or new `src/render/commentMarkers.ts` mirroring
`checkboxMarkers.ts`, which is the closest precedent: pre/post AST handling); `src/preview/previewStyles.ts`;
`src/webview/scrollSync.ts` (click toggle, state); `package.json` (setting); `src/security/html-sanitizer.ts` only if attributes
are filtered.
Size: M (S for chips only without expansion state persistence).
Tests: `test/rendering/commentMarkers.test.ts` (mimic `checkboxMarkers.test.ts`/`checkboxRendering.test.ts`: block, inline,
multi-line, `<!-- TODO -->`, comment in fenced code and inline code untouched, `TODO` in link text skipped, data-line values with
frontmatter offset), `test/webview/previewStyles.test.ts` additions, `test/webview/scrollSync.test.ts` toggle + state survives
patch, `test/security/html-policy.test.ts` (malicious `<!-- --><script>` content stays text, `--!>` closers).
Regression risks: comments currently invisible are now visible: documents with many HTML comments (templates, markdownlint
`<!-- markdownlint-disable -->`, TOC markers `<!-- toc -->`, `<!-- prettier-ignore -->`) become noisy: provide the setting and an
ignore list of tool directive prefixes (`markdownlint-`, `prettier-ignore`, `toc`, `cspell:`, `vale `, `prettier-`); contextual
tags `<!-- ... -->` used by `repairGroupedContextTagHtml` / `CONTEXT_TAG_OPEN` (check this before converting, `:321-360`);
raw html table path (`normalizeRawHtmlTable`) must keep running first; scroll-sync height changes when expanding (layout cache
at `scrollSync.ts:360-371` must be recomputed on toggle); `data-line` collisions where the converted div shares a line with a
neighbor block; the incremental patch DOM-diff resets expansion state.

---

## 5. Cross-cutting recommendations

- Add a shared host-to-webview "decorations" message family (`previewDiffMarks`, `previewComments`) applied after every
  content patch via one `reapplyDecorations()` hook in the webview runtime to avoid the patch/flicker bug class.
- Sequence suggestion: todo-comments (S/M, self-contained) -> myst-autodetect (M) -> show-incoming-diff (M) -> local-comment-mode (L).
- Keep `scrollSync.ts` growth down: new webview logic in separate modules (see how `linkNavigation.ts`, `markdownTable.ts`,
  `textEditing.ts` are factored) and keep package-contract/userFacingText tests green for every new setting/message.

## 6. Numbered ambiguities and recommended defaults

1. Diff base: HEAD only, or index/merge-base like the editor gutter? Recommend HEAD, label "since last commit".
2. Diff default: on or off? Recommend on (intent wants it like the editor), setting `preview.showIncomingDiff`.
3. Untracked/new files: all green or nothing? Recommend nothing for untracked, all green only for staged-added.
4. Deleted lines: notch marker in v1? Recommend notch only (no expansion) in v2; skip in v1.
5. Modified vs added: same green (intent) or distinguish (blue like VS Code)? Recommend same green in v1.
6. Block granularity acceptable (whole fenced block / paragraph)? Recommend yes.
7. Comments: sidecar location always next to the document, named `<name>.comments.json`, committed to git by default? Recommend yes, document `.gitignore` option.
8. Comments v1 scope: threads + reply + resolve + delete, plain-text bodies, popover (no side panel)? Recommend yes.
9. Comment author fallback chain: setting -> `git config user.name` -> OS username -> "Anonymous". Recommend.
10. Orphaned threads: keep and list, never auto-delete. Recommend.
11. Also surface comments in the native text editor via the VS Code Comments API? Recommend not in v1.
12. Autodetect without conf.py: gate open (everything on, no warning). Recommend.
13. Gate meaning: warn only, or disable the syntax in rendering? Recommend warn only in v1; optionally disable later.
14. Warning wording: intent says "Please install extension YYY"; built-in extensions are enabled not installed. Recommend "Please enable `YYY` in `myst_enable_extensions`" (keep the intent wording if the user prefers verbatim).
15. Where displayed: both preview banner and Problems panel (DiagnosticCollection)? Recommend both.
16. Conf.py lookup: walk up from the document to the workspace root only; also check `docs/`/`source/`? Recommend walk-up only.
17. Syntax coverage for warnings: which extensions? Recommend colon_fence, dollarmath, deflist, tasklist, substitution, fieldlist, attrs_*, strikethrough, html_admonition, html_image; never linkify/smartquotes/replacements.
18. Per-file override via frontmatter (`myst.enable_extensions`)? Recommend defer.
19. Comments rendering: chips for block and inline `<!-- -->`, also `% ` MyST comments? Recommend yes for both with the same gray chip (`%`).
20. TODO: chip on the word only (text stays inline) or expandable text zone? Recommend chip + the rest of the line visible; expansion only for HTML comments, and for `<!-- TODO ... -->`.
21. Tool-directive comments (`markdownlint-*`, `prettier-ignore`, `toc`): hide by default. Recommend an ignore list plus `preview.showComments` setting (default true).
22. Also match `FIXME`/`XXX`/`NOTE`? Recommend TODO only (intent), regex configurable later.
