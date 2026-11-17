# 02 — Security: Webview, Content Handling, and Resource Exhaustion

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers what untrusted *document content* can make the extension do:
script and style policy in the webview, host-side message handling, file reads, and
content-driven denial of service. Paths are relative to the repository root; lines refer to
`e1b4ad0`.

## Context

The rendering chain is `myst-parser` → AST normalisation → `myst-to-html` → highlight.js →
parse5-based sanitizer → string injection of toolbar, properties table, scripts, and CSP.
`myst-to-html` is called without `allowDangerousHtml`, so raw HTML nodes are dropped;
raw HTML tables are rebuilt from an allowlist in
[mystRenderer.ts:551-598](../../../../src/render/mystRenderer.ts#L551).
This is the main reason the sanitizer is not exploitable today, and several findings below are
about removing the latent paths that would become exploitable if that single property changed.

The webview is a privileged surface. Its scripts can post `previewEditSave` and
`previewFrontmatterSave`, which apply `WorkspaceEdit`s to the active document, and `previewLink`,
which opens files and external URLs. Script execution in the webview is therefore equivalent to
"rewrite the open document and open links on the user's behalf".

## Controls that hold and must be kept

- CSP with `default-src 'none'`, `connect-src 'none'`, `frame-src 'none'`, `object-src 'none'`,
  `base-uri 'none'`, `form-action 'none'`, and a per-render nonce
  ([csp.ts](../../../../src/security/csp.ts)).
- Mermaid runs with `securityLevel: "strict"` and its SVG is shown through an `<img>` data URI;
  PlantUML SVG is shown the same way, so diagram scripts never execute.
- KaTeX runs with `trust: false`, `maxExpand: 1000`, `maxSize: 100`.
- YAML parsing uses `maxAliasCount: 100` (alias-bomb protection).
- Resource and navigation paths go through repeated decoding, scheme blocking, root containment, and
  `realpath` checks
  ([resource-policy.ts:123-188](../../../../src/security/resource-policy.ts#L123)).
- The properties table escapes every dynamic value before it is spliced after sanitisation
  ([propertiesTable.ts](../../../../src/frontmatter/propertiesTable.ts)).
- Host-side message validation checks types, integer ranges, and document/version/request identity
  ([extension.ts:307-395](../../../../src/extension.ts#L307)).

## Findings

### SEC-05 — Include expansion has no global budget (exponential fan-out)

- **Severity**: Medium (denial of service of the whole extension host)
- **Confidence**: Confirmed by reproduction
- **Effort**: S
- **Location**:
  [mystRenderer.ts:643-700](../../../../src/render/mystRenderer.ts#L643),
  [mystRenderer.ts:125](../../../../src/render/mystRenderer.ts#L125),
  [renderPipeline.ts:164-177](../../../../src/render/renderPipeline.ts#L164)

**What happens.**
`expandIncludes` limits *depth* (8) and rejects cycles on the current path, but it does not limit
the *number* of expansions. A file that includes the next level ten times, repeated over a few
levels, expands to `10^depth` synchronous `statSync` + `readFileSync` + `mystParse` calls on the
extension host thread, re-run on every keystroke.

**Evidence.**
Measured with `renderMyst` and ten includes per level:

| Depth | Include reads | Output | Wall time |
| --- | --- | --- | --- |
| 3 | 1,110 | 38 KB | 0.4 s |
| 4 | 11,110 | 376 KB | 1.9 s |
| 5 | 111,110 | 3.7 MB | 15.9 s |

The allowed depth of 8 implies about 10^8 expansions, which never completes.
Six ten-line files are enough, and the preview re-triggers on every edit and every save.

**Fix.**
Introduce a render budget shared across the whole expansion:
maximum total includes (for example 200), maximum total included bytes (for example 10 MiB),
and memoisation of `resolveInclude` + parse results per canonical path within one render.
When the budget is exceeded, stop expanding, keep the remaining directives as placeholders,
and emit one diagnostic. Moving the render off the main thread
([PERF-01](04-performance-render-pipeline.md#perf-01--the-whole-render-runs-on-the-extension-host-main-thread))
also prevents a single document from freezing other extensions.

**Tests to add.**
Unit test generating the fan-out fixture above at depth 5: the render completes in under 1 s,
produces a budget diagnostic, and performs at most the budgeted number of reads.

**Done when.**
No document can make one render perform more than the budgeted I/O and parsing work.

### SEC-06 — Script and stylesheet policy relies on a single layer

- **Severity**: Medium (defence in depth; not exploitable with the current MyST writer options)
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [csp.ts:13-16](../../../../src/security/csp.ts#L13),
  [html-sanitizer.ts:170-192](../../../../src/security/html-sanitizer.ts#L170),
  [html-sanitizer.ts:305-318](../../../../src/security/html-sanitizer.ts#L305),
  [webview.ts:210-227](../../../../src/preview/webview.ts#L210),
  [extension.ts:560-577](../../../../src/extension.ts#L560)

**What happens.**
Three properties combine:

1. `script-src` allows `${cspSource}` in addition to the nonce. `cspSource` covers every file under
   `localResourceRoots`, which is the whole workspace folder (or the document directory).
2. The sanitizer keeps `<script src="…">` whenever the path resolves inside the roots and **stamps
   it with the page nonce**. `allowExternalScripts` is `!preview.readOnly`, so this is the trusted
   default.
3. `<link rel="stylesheet">` pointing inside the roots is kept. The comment on `processStylesheet`
   says linked stylesheets are "refused outright", but the function only records a diagnostic and
   the element survives.

None of this is reachable from Markdown today because raw HTML never reaches the sanitizer.
The day someone enables `allowDangerousHtml`, adds a `{raw} html` handler, or widens the raw-table
allowlist, a committed `notes.js` becomes executable with full webview privileges.
The sanitizer is also a denylist (`REMOVED_ELEMENTS` lists five tags), which does not cover
`base`, `template` content, SVG animation elements, `meta` other than refresh, or form controls.

**Fix.**

1. CSP: `script-src 'nonce-…'` only. Mermaid and any future bundle are loaded with the nonce, so
   `cspSource` is not needed for scripts. Keep `cspSource` for `img-src`, `font-src`, `style-src`.
2. Sanitizer: remove every content `<script>` unconditionally; remove content
   `<link rel="stylesheet">` as the comment already promises; drop `allowExternalScripts`.
3. Replace the denylist with an allowlist of element and attribute names that matches what
   `myst-to-html`, highlight.js, and KaTeX actually emit, and route URL-bearing attributes through
   the existing resource and navigation policy.
4. Delete code that only served the retired Sphinx pipeline (`sanitizeCss`, external-script
   handling); see
   [SUP-04](03-security-supply-chain-and-packaging.md#sup-04--dead-sphinx-pipeline-code-and-stale-security-evidence).

**Tests to add.**
Sanitizer unit tests: a resolvable `<script src>` and a resolvable stylesheet are both removed;
`<base>`, `<template>`, `<svg><animate attributeName="href">`, and `<input formaction>` are removed.
CSP unit test: `script-src` contains no host source.

**Done when.**
A sanitizer bypass alone is no longer sufficient to run a script from the workspace.

### SEC-07 — Broad resource roots and recursive watching in standalone mode

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:529-559](../../../../src/extension.ts#L529),
  [extension.ts:1941-1966](../../../../src/extension.ts#L1941)

**What happens.**
In standalone mode the resource root is the document's directory. For a file opened from the home
directory, `localResourceRoots` is `~` and the dependency watcher is `~/**/*`.
Content can then reference any image, font, or stylesheet under `~` (displayed, not exfiltrated,
since `connect-src` is `'none'` and remote images are blocked). The watcher cost is covered in
[PERF-16](06-performance-frontmatter-and-filesystem.md#perf-16--recursive-file-watchers-and-per-event-realpath-calls).

**Fix.**
Use the document directory as the resource root only when it is not the home directory, a volume
root, or a system directory; otherwise restrict roots to the files actually referenced by the
render (`stage.dependencies` plus resolved image paths), which are already known after rendering.

**Done when.**
A standalone preview of `~/note.md` does not expose or watch the whole home directory.

### SEC-08 — Schema-supplied regular expressions can hang the extension host

- **Severity**: Low (requires a hostile schema in the workspace)
- **Confidence**: Plausible (standard ReDoS mechanics; not reproduced)
- **Effort**: M
- **Location**:
  [schemaValidator.ts:5-11](../../../../src/frontmatter/schemaValidator.ts#L5),
  [fileLinks.ts:217-233](../../../../src/frontmatter/fileLinks.ts#L217)

**What happens.**
OKF schemas come from `_schema/` in the workspace. Ajv compiles `pattern` and `patternProperties`
with the native `RegExp` engine, and `iterAnnotations` builds `new RegExp(pattern, "u")` for
property names. A pattern such as `^(a+)+$` against a long frontmatter value backtracks
exponentially, synchronously, on the extension host, three times per keystroke.

**Fix.**
Configure Ajv with `code: { regExp: re2 }` (the `re2` package, linear-time) or validate in the
worker introduced by PERF-01 with a time budget. Apply the same engine to `patternProperties`.

**Done when.**
A catastrophic pattern produces a validation diagnostic within a bounded time.

### SEC-09 — Unbounded synchronous file reads driven by content

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [fileLinks.ts:347-383](../../../../src/frontmatter/fileLinks.ts#L347),
  [okfFrontmatter.ts:507-565](../../../../src/frontmatter/okfFrontmatter.ts#L507),
  [okfFrontmatter.ts:600-645](../../../../src/frontmatter/okfFrontmatter.ts#L600)

**What happens.**
`linkedFileDetails` reads the *entire* linked target with `readFileSync` to extract a few
frontmatter fields, and the link target may be any file type. Schema files and every `$ref`
target are read and parsed without a size limit. Includes, by contrast, are capped at 5 MiB.
A frontmatter link to a multi-gigabyte file stalls or crashes the extension host.

**Fix.**
Apply the include cap (5 MiB) everywhere content can trigger a read; for linked targets read only
the first 64 KiB, which is enough for a frontmatter block, using a file handle.

**Done when.**
No content-triggered read exceeds a documented byte budget.

### SEC-10 — Host message handling: missing size caps and an unguarded `openExternal`

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:307-395](../../../../src/extension.ts#L307),
  [extension.ts:1535-1537](../../../../src/extension.ts#L1535),
  [previewNavigation.ts:118-122](../../../../src/navigation/previewNavigation.ts#L118)

**What happens.**
`isPreviewSyncMessage` bounds `requests` (64 × 4096) but not `editedText`, `originalText`,
`fieldName`, `newFieldName`, `fieldValue` depth, or the single `request` of `previewLink`.
For external links, the scheme is checked on the *decoded* value, while the *raw* value is passed
to `vscode.Uri.parse` and `vscode.env.openExternal` outside any `try/catch`, so a malformed value
produces an unhandled rejection, and the parsed scheme is never re-checked.

**Fix.**
Cap text payloads (for example 1 MiB for block edits, 256 characters for keys, 4096 for requests)
and frontmatter value depth. Parse once with `vscode.Uri.parse(value, true)`, re-check
`uri.scheme` against `http`/`https`/`mailto`, and wrap the call in the existing error handling.

**Done when.**
Every webview message field has an explicit bound, and external navigation re-validates the URI it
opens.

### SEC-11 — Absolute filesystem paths are exposed in the preview

- **Severity**: Info
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [linkNavigation.ts:64-75](../../../../src/webview/linkNavigation.ts#L64),
  [extension.ts:1480-1490](../../../../src/extension.ts#L1480),
  [webview.ts:74-89](../../../../src/preview/webview.ts#L74)

**What happens.**
`previewLinkTargets` returns the resolved real path, which the webview writes into each link's
`title`; diagnostics also print absolute file paths. Spec R4 already requires workspace-relative
tooltips for frontmatter links, but Markdown links were not aligned. Screenshots and screen sharing
leak user names and directory layouts.

**Fix.**
Send workspace-relative paths (the helper `workspaceRelativePath` in `fileLinks.ts` already exists)
for both link titles and diagnostics.

### SEC-12 — Generated CSS is not escaped

- **Severity**: Info (defence in depth)
- **Confidence**: Confirmed by code reading
- **Effort**: XS
- **Location**:
  [mathRenderer.ts:22-38](../../../../src/render/mathRenderer.ts#L22),
  [mathRenderer.ts:82-86](../../../../src/render/mathRenderer.ts#L82)

**What happens.**
KaTeX inline `style` values are moved verbatim into a nonce-bearing `<style>` element.
KaTeX validates colours and sizes today, so no `}` or `</style>` can appear, but the code does not
enforce it, and a future KaTeX option (or a different math engine) would make it a CSS or HTML
injection point inside a trusted element.

**Fix.**
Reject any declaration containing `{`, `}`, `<`, `@`, or `\`, and keep the original inline style
on that node instead (which the CSP would then block, degrading gracefully).
