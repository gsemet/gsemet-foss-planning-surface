# 06 — Performance: Frontmatter Analysis, Schema Validation, and Filesystem Access

Part of the [deep analysis review](00-index.md) of `src/markdown-okf-schema-studio`.
This file covers the OKF frontmatter path (`analyzeFrontmatter`, Ajv, link resolution, stem index)
and the synchronous filesystem work done on the extension host thread: watchers, `realpath`, and
directory walks. Lines refer to `e1b4ad0`.

## Context

`analyzeFrontmatter` runs at least three times per edit
([PERF-14](#perf-14--frontmatter-is-analysed-three-times-per-edit)), each time synchronously.
Each run discovers the schema directory, lists it, reads and parses the schema and its `$ref`
targets, compiles an Ajv validator, validates, and (for enrichment passes) resolves file links.
[spec.md](../../../../spec.md) requirement R3 asked for compiled
validators to be cached; the cache exists but never hits.

## Findings

### PERF-12 — The Ajv validator cache never hits, and every compile is retained (memory leak)

- **Severity**: High
- **Confidence**: Confirmed by reproduction
- **Effort**: S
- **Location**:
  [schemaValidator.ts:13-45](../../../../src/frontmatter/schemaValidator.ts#L13),
  [okfFrontmatter.ts:905-960](../../../../src/frontmatter/okfFrontmatter.ts#L905),
  [okfFrontmatter.ts:695-705](../../../../src/frontmatter/okfFrontmatter.ts#L695),
  [fileLinks.ts:129-170](../../../../src/frontmatter/fileLinks.ts#L129)

**What happens.**
`getCachedValidator` keys a `WeakMap` by the schema *object*. `analyzeFrontmatter` builds that
object fresh on every call (`resolveSchemaRefs(parseSchemaFile(...))`), so the lookup always misses
and Ajv compiles the schema again. The same applies to the `if` sub-schemas in `effectiveProperties`
and to the expanded branches in `valueMatchesSchema`. Ajv itself stores every compiled schema in its
private `_cache`, which is a `Map` keyed by the schema object (`node_modules/ajv/dist/core.js:100`).
The objects can never be collected, so memory grows with every analysis.

**Evidence.**
Probe with a 15-line OKF schema (`required`, `enum`, `if/then`, one `x-okf-link`), run from
`src/markdown-okf-schema-studio` after `npm run compile`:

```javascript
const { analyzeFrontmatter } = require("./out/src/frontmatter/okfFrontmatter.js");
const { sharedSchemaValidator } = require("./out/src/frontmatter/schemaValidator.js");
// ... call analyzeFrontmatter 505 times on the same document, with global.gc() before measuring
console.log(sharedSchemaValidator._cache.size, process.memoryUsage().heapUsed);
```

| Measure | Value |
| --- | --- |
| Ajv `_cache` entries after 505 analyses | 1,523 (three compiled schemas per analysis) |
| Heap retained after GC, per 500 analyses | +13.4 MB |
| Time per analysis (tiny schema, warm) | 0.83 ms |

At three analyses per edit, a working session of 10,000 edits retains on the order of 800 MB with
this small schema; real bundle schemas are larger, and each compile also costs more.
The extension host eventually slows down from GC pressure and can run out of memory.

**Fix.**

1. Cache the *resolved schema* per schema file, keyed by `(path, mtimeMs, size)` of the schema and
   of every `$ref` target it inlined, so the same object identity is reused until a file changes
   (this is also PERF-13).
2. Key the validator cache by that stable object, or by a content hash of the resolved schema.
3. When a schema entry is evicted or invalidated, call `sharedSchemaValidator.removeSchema(schema)`.
4. Cache `if` and branch validators under the same resolved-schema entry.

**Tests to add.**
Unit test: 100 analyses of an unchanged document leave `_cache.size` constant after the first one
and return the same validator instance; touching the schema file produces exactly one recompilation.

**Done when.**
Heap and Ajv cache size stay flat across repeated analyses of an unchanged schema.

### PERF-13 — Schema discovery and parsing are not cached

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: S (together with PERF-12)
- **Location**:
  [okfFrontmatter.ts:428-499](../../../../src/frontmatter/okfFrontmatter.ts#L428),
  [okfFrontmatter.ts:558-645](../../../../src/frontmatter/okfFrontmatter.ts#L558)

**What happens.**
Each analysis walks ancestor directories with `statSync` to find `_schema`/`_schemas`, lists the
schema directory with `readdirSync` plus one `statSync` per entry, then reads and parses the matched
schema and every relative `$ref` target with `readFileSync`. Nothing is memoised, so a bundle with a
large `_schema/` directory pays this I/O several times per keystroke, plus on every frontmatter save
and link click.

**Fix.**
Introduce a `SchemaRegistry` per workspace folder: schema directory per document directory,
directory listing, and parsed + resolved schema per file, invalidated by a
`FileSystemWatcher(RelativePattern(root, "**/_schema{,s}/**"))`. Return the same resolved object
until invalidation so PERF-12's validator cache is effective.

**Done when.**
An analysis of an unchanged document performs no filesystem call for schema discovery or parsing.

### PERF-14 — Frontmatter is analysed three times per edit

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: M
- **Location**:
  [extension.ts:534-552](../../../../src/extension.ts#L534),
  [extension.ts:691-747](../../../../src/extension.ts#L691),
  [extension.ts:2450-2492](../../../../src/extension.ts#L2450),
  [propertiesTable.ts:256-293](../../../../src/frontmatter/propertiesTable.ts#L256)

**What happens.**
For one edit: `updatePreview` analyses with `inspectLinks: false`; `refreshFrontmatter` analyses the
same version again 300 ms later with the same options; `scheduleLinkEnrichment` analyses a third
time with `inspectLinks: true`. The second and third passes each call
`replacePropertiesTableMarkup`, which parses the whole page with parse5 and
`sourceCodeLocationInfo: true`, then reassign the webview HTML (see
[PERF-05](05-performance-webview-lifecycle.md#perf-05--each-keystroke-replaces-the-webview-document-three-to-six-times)).
Link resolution results are discarded on every edit even when no link-bearing field changed.

**Fix.**
Memoise the analysis per `(document URI, version, options)`. Remove `refreshFrontmatter`'s timer for
edits that also trigger a render, since `updatePreview` already analyses that version. Run link
resolution only when the link-bearing values (the `x-okf-link` annotated fields) differ from the
previous resolved set, and reuse previous results otherwise. Deliver the table as a fragment by
`postMessage` instead of splicing the page.

**Done when.**
One edit performs at most one analysis without links and at most one link resolution, and only when
link inputs changed.

### PERF-15 — Any Markdown save invalidates the stem index and forces a synchronous rebuild

- **Severity**: Medium (High in large workspaces)
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:200-213](../../../../src/extension.ts#L200),
  [stemIndex.ts:84-147](../../../../src/frontmatter/stemIndex.ts#L84),
  [fileLinks.ts:542-565](../../../../src/frontmatter/fileLinks.ts#L542)

**What happens.**
`watchStemRoot` invalidates the index on `onDidChange` as well as create and delete. A content
change cannot change a filename stem, but it now discards the index for the whole workspace folder.
The next `filename-stem` link resolution rebuilds it with a recursive `readdirSync` over the entire
workspace on the extension host thread. With autosave, the active document's own save triggers this
about once per second during typing. `lookup` also performs `realpathSync` + `statSync` for every
candidate on every lookup.

**Fix.**
Invalidate only on create, delete, and rename (spec R1 already says so). Apply the change
incrementally (add or remove one path) instead of discarding the index. Build the initial index
asynchronously (`fs.promises.opendir` or `vscode.workspace.findFiles("**/*.md")`, which honours
`files.exclude`) and resolve links as "pending" until it is ready. Cache `realpath` results per
candidate until the next invalidation.

**Done when.**
Saving a Markdown file performs no directory walk, and the first index build does not block the
host.

### PERF-16 — Recursive file watchers and per-event `realpath` calls

- **Severity**: Medium
- **Confidence**: Confirmed by code reading
- **Effort**: M
- **Location**:
  [extension.ts:1964-1984](../../../../src/extension.ts#L1964),
  [extension.ts:1780-1819](../../../../src/extension.ts#L1780),
  [buildQueue.ts:104-112](../../../../src/build/buildQueue.ts#L104),
  [extension.ts:617-643](../../../../src/extension.ts#L617)

**What happens.**
Each preview creates a `**/*` watcher on its resource root. In standalone mode that root is the
document's directory, so previewing `~/note.md` installs a recursive watcher on the home directory.
Every event, including those caused by `git checkout`, builds, or `node_modules` installs outside
the ignored segment list, runs `refreshReferencedPath`, which calls `realpathSync` on the event path
and on the active document, then `queue.dependsOn`, which calls `realpathSync` on every dependency
of the last render. A checkout touching 5,000 files issues tens of thousands of synchronous
syscalls. The ignore list (`IGNORED_WATCH_SEGMENTS`) is applied after VS Code has already delivered
the event. Each linked frontmatter target adds one more watcher per preview.

**Fix.**
Watch only what the render depends on: the document, its includes, and its resolved images, with one
`RelativePattern` per directory and file glob, rebuilt when `stage.dependencies` changes. Store
dependencies as a pre-canonicalised `Set<string>` on the stage so `dependsOn` is a lookup.
Never create a recursive watcher outside a workspace folder. Coalesce bursts with a 100 ms debounce.

**Done when.**
A file event unrelated to the rendered document costs no syscall, and no recursive watcher exists
outside workspace folders.

### PERF-17 — Per-keystroke synchronous filesystem calls

- **Severity**: Low
- **Confidence**: Confirmed by code reading
- **Effort**: S
- **Location**:
  [extension.ts:299-305](../../../../src/extension.ts#L299),
  [extension.ts:2201-2220](../../../../src/extension.ts#L2201),
  [resource-policy.ts:105-121](../../../../src/security/resource-policy.ts#L105),
  [fileLinks.ts:422-430](../../../../src/frontmatter/fileLinks.ts#L422)

**What happens.**
`onDidChangeTextDocument` calls `refreshPreview` for *every* changed document in the window,
including other files, Git and output documents. For each preview it runs `sourceAvailable`
(two `realpathSync` and one `statSync`) or `refreshReferencedPath` (more `realpathSync`).
Each render then constructs two `ResourcePolicy` instances (pipeline and webview), each calling
`realpathSync` on its roots, and link enrichment walks to the filesystem root with `existsSync` to
find `.git`.

**Fix.**
Filter `onDidChangeTextDocument` to `file:` documents that are either an active preview document or
a known dependency. Cache canonical roots per preview (they only change on workspace-folder events),
and cache `gitRoot` per directory.

**Done when.**
Typing in an unrelated file performs no filesystem call on behalf of the preview.
