# CR-517 investigation: a comment updates only its highlights and does not wait for Git

Base: `aeefa1b00c5a6bb0cfbc64e67de3994c3e904053` (CR-516 head, no CR-517 commit yet). All paths are
relative to the worktree. "Read in code" means not executed. No build, test or install was run
here (a parallel `just dev` was announced).

## 1. Files and entry points

### Page: highlights, badges, orphan list, popover

`src/page/modules/commentThreads.ts` (`installCommentThreads`):

- `setThreads` (l.781) stores the sanitized list and calls `apply` (l.496-530): remember open
  popover, draft, delete confirmation and discard question; `close()`; `clear()` (l.298-308, unwraps
  every mark and merges text nodes, removes badges and the orphan box); for each thread in order
  `orphaned === true || (!attach && !badge)` goes to the orphan box; reopen the popover.
- `blockFor` (l.327-341) runs `querySelectorAll("[data-line]")` once per call, so once or twice per
  thread, plus one more in `attach` (l.368) for a moved quote.
- `attach` (l.359-431): first occurrence in ONE text node. Text inside earlier marks is skipped
  (`SKIP`, l.80-84) and a mark splits its text node, so overlapping placement depends on thread
  order. A moved quote (no block at the line) needs 12 characters and exactly one occurrence.
- `badge` (l.435-454): appended inside the block in thread order, or for `NEXT_TO`/`SKIP` blocks
  inserted right after the block (several end up in reverse thread order), marked
  `data-okf-comment-badge-after`.
- `renderOrphans` (l.460-494): box after `#sphinx-myst-preview-content`, entries in thread order.
- Other callers: `features/contentPatch.ts:143` (`apply()` after a patch and at startup),
  `features/hostHandlers.ts:51` (`visibilityChanged`), `:55` (`result`), `:58` (`setThreads`),
  `runtime.ts:189`, `:204`, `:303`.

`features/hostHandlers.ts` l.57-60: `setThreads(message.threads); rt.scroll.measure();`.
`features/scrollCore.ts` l.330-340 `measure()` rebuilds the mapping table (rectangles and line tops
of every mapped block), the anchor map and the sticky reading offset. A `ResizeObserver` on the
content (l.580-585) calls `stabilizeLayout`, which measures too.

Styles (`src/core/preview/styles/commentStyles.ts`, read in code): marks are paint only (l.402-413),
the inner badge is absolute (l.415-431), the popover fixed, the orphan box adds no scroll height
before the content end (l.650-657), hidden comments hide badges and box (l.735-749). The only
thread element that moves content blocks is the after-block badge (l.433-437, `display: block`).

### Host: author name and thread index

`src/session/features/comments.ts`:

- `writeComment` (l.469-499): `resolveAuthor({setting, gitName: () => host.vcs.userName(documentId),
  osUserName})` (l.488-492), then `store.update`, `hintHash`, `await this.post(preview)`. The page
  gets the threads before the command result.
- `core/comments/author.ts` `resolveAuthor`: setting, Git name, OS name, "Anonymous"; Git is not
  asked when the setting is set. Port `host-api/vcsInfo.ts:22`, adapter
  `host-vscode/headBaseline.ts` l.84-98: activates `vscode.git`, `getRepository(uri)`,
  `getConfig("user.name")`, no cache.
- Another Git name reader, `session/features/workspaceChoices.ts` l.99-107 (`refreshThreadAuthor`,
  on every render and at activation), belongs to inline source threads. Its cache can be older than
  the preview session: do not use it for a write. `sourceEdits.ts:252-256` is out of scope.

`createDocumentIndex` (`core/comments/anchoring.ts:158`) and `reanchorThreads` (`:494`, builds the
index when given a string) are called only from `comments.ts`: l.197, l.219, l.326, l.333.

User actions that run them (read in code):

| Path to the call | User action | What runs |
| --- | --- | --- |
| `rendering.ts:336` `schedule` after a render, `post` l.208/219 | first preview of a document that has comments; a following preview switching document | index + re-anchor all (same sidecar and view: nothing) |
| `rendering.ts:605-606` page ready | page reload or restore | re-posts; re-anchors only if there is no view for that file text |
| `writeComment` l.497, `post` | create, reply, resolve, delete | sidecar hash changes: index + re-anchor all, once per write |
| sidecar watcher l.427-435 (150 ms) | the comments file created or changed outside | index + re-anchor all |
| `hostEvents.ts:266` `shiftForEdits`, `post` | clean change (reload, revert, clean undo) | view dropped: index + re-anchor all |
| same, dirty undo or redo | undo, redo | `recheck`: index + re-anchor all (l.197) |
| same, an orphan exists and the text changed | typing while a thread is orphaned | index + re-anchor of the orphans (l.197) |
| `hostEvents.ts:373` `persistAnchors` l.304-361 | **every save of a previewed document** | l.326 index, even with no comments file (skipped only with no preview or a comments file dirty in an editor); l.333 re-anchor when the file is valid (zero threads when missing) |

Plain typing with no orphan does not re-index. `moveSidecars` does not index.

### Real-window scenario, report, job

- `test/integration/perf547.ts`: removes the old report, `createFixture("perf-547",
  perf547Document())`, side preview, `measurePerf547`, writes `out/reports/probe/perf-547.json`
  and prints it after `PERF-547`. One run makes 12 comment writes (9 create + 3 restyle samples,
  `test/probe/perf547Measure.ts`).
- Probe route for a host figure: `session/previewSession.ts` l.59-62 and l.167 (`preview.probe`),
  `host-vscode/testHooks.ts:206`, read as `getActivePreviewForTests()?.comments` (see
  `test/integration/commentWrite.test.ts`). The fake in
  `test/session/reviewReqComments.requirements.test.ts` l.135 has only `probe.commentPosts`: a new
  probe field must be added there too or be written defensively.
- `justfile` l.470-484 `ci-perf-547`; `test:integration` compiles `test/**` to `out/test/**`.
- `.github/workflows/ci.yml`: boolean input `perf_547` (l.41-44), job `perf-547` (about l.545-588),
  job timeout 5 min, step 4 min, artifact `perf-547-attempt-<n>` holding `out/reports/` (report at
  `probe/perf-547.json`). `test/build/test_workflows.py` l.1352-1390 pins command, env, timeouts,
  artifact and recipe.
- Dispatch (branch pushed first):
  `gh workflow run ci.yml --ref chantier/batch-09/cr-517-a-comment-updates-only-its-highlights-an -f perf_547=true`
  then `gh run download <run-id> --name perf-547-attempt-1 --dir <new empty folder>`.
- Report described in `CONTRIBUTING.md` l.441-454, `.agents/guidelines/ci.guidelines.md` l.114-120,
  `docs/how-we-test.md` l.196-199.

### Tests, requirements, changelog

- Page: `test/page/commentRestyle.test.ts` (CR-516, real Chromium with the perf-547 document, limit
  100 restyled elements, skipped without Chromium unless `STUDIO_REQUIRE_CHROMIUM=1`, run by
  `just ci-visual 1`; in `test:breakout`); `test/page/modules/commentThreads.test.ts` (938 lines,
  own fake DOM: tag, class and bare attribute selectors only, no `isConnected`),
  `commentThreadsLongDocument`, `reviewReq.requirements`, `runtimeCommentsHidden`,
  `runtimeContentPatch`.
- Host: `test/session/reviewReqComments` and `reviewReqThreads`, `commentAuthorResource`
  (REVIEW-065 S6), `test/host-vscode/headBaselineUserName`, `test/core/comments/*`,
  `test/integration/commentWrite.test.ts` l.203-214.
- SwRS in `requirements/tiers/swrs/review-annotations/`: REVIEW-012 (posting), 017 (highlight once;
  S7: applying again leaves the same DOM), 028 (orphan box), 021, 044, 086, 152, 217, 218
  (popover), 065 (author order: setting, repository Git `user.name`, OS, Anonymous), 219, 223
  (CR-516 restyle). Markers `@implements_req` / `@tests_req` move with code. Numbers go up to 223.
- `CHANGELOG.md` `## Unreleased`: one user line appended at the END, ending
  `(CR-517 <short name>, PR #n, issue #547)`. `docs/releases-notes/` is written only by the version
  PR. `requirements/tiers/log.md`: newest first, dated, `Reason: CR-517, issue 547...`.
- File size ratchet: `src` 800 lines. `commentThreads.ts` is exactly 800.

## 2. Smallest change

1. **Measure first (host figures, own commit).**
   - `writeComment`: time the Git name wait as the write sees it (wrap `gitName`), append to an
     array on `preview.probe`, expose it in `testHooks.ts`. A cached answer then records near 0.
   - `perf547.ts`: before opening the document, `git init` in the fixture folder and set a LOCAL
     `user.name` (a fixed invented one), **no commit**: with no HEAD commit `headText` answers
     nothing (`headBaseline.ts` l.66-68), so no incoming-change marks alter the measured DOM. Wait
     until `getAPI(1).getRepository(uri)` has the fixture folder as root (the outer checkout is also
     a repository; do not reuse `waitForGitRepository` of `realWindowGaps.ts`, it waits for a HEAD
     commit). Assert a stored author equals that name. Report `authorWait` (unit, samples, median)
     and a field saying the folder is a Git repository with `user.name`.
   - `threadIndex`: give the generator a scale argument (default 1, output unchanged); add
     `test/probe/perf547ThreadIndex.ts`, plain Node, importing `anchoring.ts` and `parseSidecar`,
     run by `ci-perf-547` after the window run (`node out/test/probe/perf547ThreadIndex.js`), adding
     `threadIndex` to the report: per document lines, bytes, threads, samples and median of
     `createDocumentIndex(text)` and of `reanchorThreads(text, threads)` (string form, as `post`
     calls it); one discarded warm-up; assert no orphan. Update `test_workflows.py` and the three
     report descriptions. (Calling it from the scenario would avoid the recipe change, but a plain
     Node step follows the wording and runs locally without a window.)
2. **Page.** New module beside `commentThreads.ts` (ratchet) for the incremental update; `setThreads`
   uses it, `apply()` stays the full anchoring for patch, startup and visibility. One lazy
   `[data-line]` snapshot per update, shared by `blockFor` and the moved-quote search.
   - Added thread at the end of the list (how the host adds): earlier placements cannot change.
   - Resolved only: toggle the attribute on the same element and orphan text. Reply: badge
     `aria-label`, orphan meta, popover.
   - Removed, re-anchored (`anchor.line`, `quote`, `orphaned`) or inserted elsewhere: that thread,
     plus every thread whose placement can depend on it (same or nested block, split text node,
     badge or orphan that could now get a mark, moved-quote threads whose uniqueness count changes),
     unwrapped and placed again in thread order.
   - Return whether an after-block badge was inserted, removed or moved while comments are shown;
     `hostHandlers.ts` measures only then.
3. **Author, only if the CI median of `authorWait` is above 10 ms.** Per preview session, per
   document: remember a non-empty name; a write with one uses it and starts a background read; no
   name, `undefined` (none or failure) or another document waits as today; the setting never reads
   Git; keep the newest read when two overlap; nothing survives the session. Amend REVIEW-065 to say
   an earlier read of the same session may be used. Otherwise change nothing and report figures.
4. Requirements: a new SwRS (next free number, REVIEW-224 at this base) for "an update touches only
   changed threads", markers, `just requirements-update`, log entry; CHANGELOG line.

## 3. Risks

Values derived from what the change alters:

- **Scroll measure skipped.** Derived from `measure()`: the mapping table, anchor map and reading
  offset (scroll sync, line marker, sticky band). Today every `previewComments` refreshes them, also
  hiding any earlier stale state. After the change only after-badge changes (and the
  `ResizeObserver` on size changes) refresh them. A badge moved without a height change needs the
  explicit measure. Marks splitting text nodes are assumed not to move line tops (CSS read only).
- **Same result, thread order.** Re-placing one thread while later marks exist differs from a full
  apply. Compare in-place against from-nothing for: two threads in one block, overlapping quotes,
  nested blocks, first of two deleted, orphan becoming anchored after a delete, several after-badges
  on one block, last badge removed (`data-okf-comment-badged` goes), orphan box order and removal,
  empty list, hidden comments, resolve of an orphan.
- **Full apply repairs DOM drift today.** A holder can be disconnected, or its block ineligible or
  eligible again (open block editor, patched content): check unchanged holders and retry threads that
  are a badge or an orphan without a host verdict.
- Internal lists (`addedMarks`, `addedBadges`, `badgedBlocks`, `addedOrphans`) drive `clear`,
  `visibilityChanged`/`paintFocus` and the popover holder: keep them exact.
- Open popover: keep today's rebuild with draft, confirmation, discard question, `sent`/`act`
  states and the same trace messages. A repeated thread id only comes from a hostile message
  (`parseSidecar` refuses it): fall back to the full apply for it.
- **Comparability of the runs.** The fixture becomes a Git repository, which CR-516's runs did not
  have (Git status work after each sidecar write may add time or noise). Say so beside the table.
- **Generator bytes.** Baseline of the default output, computed here with `node` type stripping
  (v24.22.2, nothing written): 13 files, sha256 of `JSON.stringify(files)`
  `f1c010b1cce9f1a446f6812b2c764b69aa91320cf5f5e48a77dcb73c914b8ae9`; `report.md` 64579 bytes
  `bea73f28631d98b4fb0566055d6c17c954e2089ecc0126bfbcd22b91dc068289`; `report.comments.json` 7534
  bytes `df1f01f87008cf21443f122bee2150ee456dc61d587d989a749e22c4562c73f9`. Pin it in a test. The
  fourfold shape (1856 lines, 88 tables, 788 rows, 44 images, 36 threads) must also scale
  `BLOCKQUOTES` (21 to 84); assert all 36 threads anchor.
- CI step timeout 4 min (CR-516's healthy runs: under 2 min); one earlier dispatch of CR-516 failed
  on a network timeout while fetching VS Code.
- Order and rounds: the author decision needs a pushed measure commit and a dispatch before the
  author code; the page change can travel in the same push. Round limit 6; no heavy CI at this head.
- Parallel batch CRs may claim the same SwRS number.

Follow-ups, not in scope (read in code, not verified):

- `contentMorph.ts` `copyPositions` (l.118-131) stops where child counts differ, so a nested
  `data-line` under an element holding a mark or badge may stay stale after a patch.
- The locally installed VS Code's Git `getConfig` reads `git config --local` only, so a global-only
  `user.name` would not be used (falls to the OS name); not checked on the CI VS Code version.

Owner watch: read in code, the thread index is built on every save of a previewed document, even
with no comments file (`persistAnchors` l.326), and every create, reply, resolve or delete indexes
and re-anchors all threads. Its cost is not measured yet; nothing is to be disabled or changed here.

## 4. Questions only the user can answer

None.

## 5. Evidence plan

Kind: performance change in the page (and possibly the host), same visible result. No screenshot:
nothing visible changes.

| Claim | Shown by (kept in `<CR>/evidence/`) |
| --- | --- |
| Other highlights stay the same elements; `[data-line]` read once; measure only when a block can move | new page tests, run on the base sources (fail) and on the change (pass), both logs |
| Same result as from nothing, after create, reply, resolve, delete | a comparison test of both DOMs, best on the real preview in Chromium (base: `commentRestyle.test.ts`) |
| CR-516 restyle limit holds | `commentRestyle.test.ts` log with `STUDIO_REQUIRE_CHROMIUM=1` |
| Generator default unchanged | hash test against the values in section 3 |
| Author decision | one `perf-547` dispatch of the measure-first commit: report with `authorWait` samples and median, run id, head |
| Author behaviour, if changed | tests: setting, name read in the session, first write, changed Git name, no name |
| Timing | three `perf-547` dispatches at the final head: each run's raw report and a table of medians per interaction and `authorWait` samples against CR-516's "after" runs 45918715713, 45918718450, 45918721402 (`516-.../evidence/after/runs.md`: commentCreate 47.1, 45.9, 37.1 ms; selectionRelease 18.2, 17.65, 18.05 ms) |
| Thread index cost | `threadIndex` medians of both documents from the same three runs beside their `commentCreate` median, with the action table of section 1 (read in code) |
| Project gates | `just preflight` (on Windows the static stage only); heavy CI at the stack's last commit only (02-answers item 6) |

Cannot be shown: a gain above runner noise is not guaranteed ("Not separable from runner noise" is
accepted); skipping the scroll measure is shown by a test, not by the timings; the thread index is
timed in plain Node on the CI runner, not inside VS Code, and only with every thread anchoring
exactly (orphan and fuzzy search cost is not measured).
