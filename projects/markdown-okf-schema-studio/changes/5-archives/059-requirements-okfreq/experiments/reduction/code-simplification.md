# Code simplifications revealed by the requirement overlap

These are the places where the overlap in the requirements points at duplicated code. Every
candidate below was checked in the worktree (head `ccdd039`).

Rules for every item:

- **No feature loss and no behaviour change.** Reason texts, check order, timeouts and answer
  shapes stay byte for byte. The existing tests guard each change, and no assertion changes
  (constitution 3).
- Known issues stay as they are. If a merge would naturally fix one, it is flagged below and done
  only as a separate fix commit: code, test and SwRS together, with its backlog item closed. It is
  not counted as a goal of this work.
- Layers (CONTRIBUTING.md "Architecture"): helpers go in the lowest layer that may hold them.
  Session helpers go in `src/session/`, protocol helpers in `src/core/protocol/`, page helpers in
  `src/page/modules/`. No new dependency-cruiser exception.
- 800-line ratchet: every touched file shrinks. `commentThreads.ts` (773 lines) and
  `editPalette.ts` (766) gain headroom.
- Each item is a separate commit in a **follow-up PR after PR #62 merges** (decision D4). Markers
  move with the code in the same commit. See "Follow-up PR plan" at the end.

## Summary

| # | Candidate | Files | Lines today in the duplicated parts | Estimated saving | Risk | Recommended |
| --- | --- | --- | ---: | ---: | --- | --- |
| S1 | Guarded source edit in the host: read-only, open edit, stale, plan, apply, report | `src/session/features/sourceEdits.ts` (460) | ~190 | **110–130** | Low | Yes |
| S2 | Writable-document guard for host requests | `src/session/features/hostRequests.ts` (302) | ~40 | 20–25 | Low | Yes (with S1) |
| S3 | Reply envelope helper (`documentId`, `revision`, `requestId`, `editId` echo) | `blockEdits.ts` (536), `frontmatter.ts` (382), `sourceEdits.ts`, `hostRequests.ts` | ~13 blocks × 6 | 30–40 | Low | Yes |
| S4 | Percent decoding of a path, written three times | `core/navigation/previewNavigation.ts`, `core/security/resource-policy.ts`, `page/features/scrollCore.ts` | 3 × 17 | 17 (host copies); page copy kept | Low (host); **a naive merge would fix a known issue** (page) | Host copies only |
| S5 | Boolean view preference toggles on the page | `page/modules/incomingToggle.ts` (62), `commentsToggle.ts` (65), `toolbarCollapse.ts` (70), parts of `tocColumn.ts`, `anchorMode.ts`, `themeMode.ts`, `widthMode.ts`, `viewControls.ts` | ~260 | **90–120** | Low to medium | Yes |
| S6 | Page round trips that rebuild their own pending map and timer next to `installHostRequests` | `page/modules/labelRename.ts`, `commentCompose.ts` (398), `commentThreads.ts` (773) | ~110 | 50–70 | Medium | Yes, one module per commit |
| S7 | Read-only refusal moved into the dispatcher gate | `src/session/pageMessages.ts` + handlers | ~30 | 20–30 | Medium | Optional, after S1 |
| S8 | Status line show and hide helper on the page | 12 page files, 13 sites | ~30 | 10–15 | Low | Optional |
| | **Total (S1–S6)** | | | **≈ 320–400** | | |

What the requirement overlap did **not** turn up as duplicated code, though I checked:

- Table cell refusal (TABLE-034) against the block editor refusal (BLOCK-222). The cell editor
  already runs through `blockSourceEditor.ts`; the overlap is only in the requirements.
- `PAGE_TO_HOST_VALIDATORS` and `PAGE_MESSAGE_GATES` are already single tables. The requirement
  side keeps one SwRS per message type (D1) but writes the shared envelope and gate rules once.
  Nothing to change in the code.
- The page `hostRequests` correlation (`installHostRequests`) is already shared by the pickers,
  the image and HTML paste and the PlantUML includes. Only the modules of S6 bypass it.

## S1. Guarded source edit in the host (`sourceEdits.ts`)

The duplication, confirmed in the source: five handlers repeat the same preamble and epilogue.
They are `handleCheckboxToggle`, `handleLabelRename`, `handleThreadChange`, `handleBlockMove` and
`blocksDocument` (copy, cut, paste). Each one does this:

1. `if (preview.readOnly) post({ ok:false, reason:"<verb> needs a trusted workspace." })`. The
   checkbox is the exception: its read-only check is in the dispatcher.
2. `if (preview.edits.active) post({ …"Save or cancel the open Markdown edit …" })`.
3. `currentPreviewDocument(preview, message) ?? post("The preview is out of date. Try again once
   it has refreshed.")`.
4. `plan…()`, then `"refused" in plan` posts `plan.refused`.
5. `this.apply(document, [edit]).then(applied ? ok : "VS Code could not apply the <noun>.",
   error => error.message)`.
6. A private `post…Result` that echoes the message identity, once per handler: 5 copies of about
   14 lines.

The requirements copied this exactly: BLOCK-121/122/123/128, BLOCK-181/182/183/188,
REVIEW-180/181/182/184, MYST-042/043/044, GFM-022/024/025.

Proposed helper: `src/session/features/guardedEdit.ts`, in the session layer, with no new import
direction.

```ts
interface GuardSpec<M> {
  post(result: { ok: false; reason: string }): void;   // the handler's own answer shape
  trustReason?: string;          // omitted = read-only checked elsewhere (checkbox)
  busyReason: string;
  staleReason?: string;          // default "The preview is out of date. Try again once it has refreshed."
  order?: "trust-busy-stale" | "stale-busy";           // checkbox keeps its current order
}
function guardedDocument<M>(preview, message: M, spec: GuardSpec<M>): HostDocument | undefined;
function applyAndReport(apply: PromiseLike<boolean>, ok: () => void, fail: (reason: string) => void, noun: string): PromiseLike<void>;
function replyTo(message, type, result): HostToPageMessage;   // S3
```

- Each handler keeps its own reason texts, passed in. `order` keeps the checkbox order: stale,
  then busy, with no read-only check.
- Lines: about 190 duplicated lines become about 60 lines of helper plus about 4 lines per call
  site. **Saving 110 to 130 lines.** `sourceEdits.ts` drops from 460 to about 340.
- Risk: low. The order and the exact texts are parameters. The risk is to swap the checkbox
  order. The `stale-busy` order and a test for it guard against that.
- Guarding tests: `test/session/blockReq.requirements.test.ts` (18 tests),
  `test/session/reviewReqThreads.requirements.test.ts`,
  `test/session/renderReq.labelRename.requirements.test.ts`,
  `test/session/trustReq.requirements.test.ts`, `test/integration/blockMove.test.ts`,
  `test/integration/blockClipboard.test.ts`, `test/integration/labelRename.test.ts`,
  `test/integration/checkboxToggle.test.ts`, `test/core/protocol/pageStateMessages.test.ts`.
- Markers: the cross-cutting markers (`TRUST.readonly-request-refusal`, `BLOCK.edit-exclusivity`,
  `TRUST.page-message-gates`, `BLOCK.source-edit-outcome`) move to the helper, once each. The
  feature markers (`BLOCK.move-host`, `MYST.label-rename-host`, …) stay on the handlers.

## S2. Writable-document guard for host requests (`hostRequests.ts`)

`handleListCitations`, `handlePickDocument`, `handlePickImage` and `handlePasteImage` repeat the
same steps: `readOnly` refuses with a reason, then `currentPreviewDocument` (or `preview.document`
with an id check) refuses as "out of date, or not a file". `handleListTargets` does the stale part
only.

- Fix: reuse `guardedDocument` from S1 (no busy check: these requests edit no document), with a
  `requireFile` option.
- Saving: 20 to 25 lines.
- Risk: low. `handlePasteImage` uses `preview.document` and the id check rather than
  `currentPreviewDocument`, because the editor's autosaves move the revision (documented in its
  comment). It must keep that. Pass a `match: "document"` mode, or leave that handler as it is.
- Guarding tests: `test/session/paletteReq.requirements.test.ts` (13),
  `test/session/pasteImageWrite.test.ts`, `test/integration/` picker suites.

## S3. Reply envelope helper

`documentId: message.documentId, revision: message.revision, requestId: message.requestId,
editId: message.editId` is written by hand in 13 answer builders:

- `blockEdits.ts` ×5
- `frontmatter.ts` ×2
- `sourceEdits.ts` ×5
- `hostRequests.ts` ×1, already shared there as `postHostResult`

Fix: `replyEnvelope(message)` in `src/core/protocol/` (pure; next to `envelope.ts`), returning the
four fields. Saving: 30 to 40 lines. Risk: low (TypeScript checks the shape). Guards:
`test/core/protocol/hostToPage.test.ts` and every session suite above.

## S4. Percent decoding of a path, written three times

`decodePath` (at most four decoding rounds, then refuse any leftover escape) exists three times:

- `src/core/navigation/previewNavigation.ts` (TOOLBAR-093), using `/%[\da-f]{2}/iu`
- `src/core/security/resource-policy.ts` (TRUST-026), using `/%[\da-f]{2}/i`, the same result
- `src/page/features/scrollCore.ts` `navigateToAnchor` (TOOLBAR-119), using `/%[da-f]{2}/iu`
  (the class lost `\d`). A comment there says it is kept on purpose; it is a recorded Known issue.

Proposal:

- Export one `decodePercentPath` from `resource-policy.ts`. `previewNavigation.ts` already imports
  from `../security/resource-policy`, so this adds no new edge. Delete the second host copy:
  **saves 17 lines, no behaviour change.**
- **Do not** point the page copy at it in this work. That would turn `[da-f]` into `[\da-f]` and
  fix the Known issue of TOOLBAR-119, so it would be a behaviour change. Flagged: if the
  maintainer wants that fix, it is its own commit with the test, the SwRS update
  (`TOOLBAR.anchor-jump`) and the backlog item (`P3/link-navigation-fixes`).
- Guards: `test/core/navigation/previewNavigation.test.ts`,
  `test/security/resource-policy.test.ts`, `test/session/previewNavigator.test.ts`,
  `test/session/toolbarReq.requirements.test.ts`.

## S5. Boolean view preference toggles on the page

The view-choice SwRS (37 of them, now `LIFE.view-choice-store` and `LIFE.view-choice-start`) come
from one pattern written once per choice. `incomingToggle.ts`, `commentsToggle.ts` and
`toolbarCollapse.ts` are almost the same file. Each one:

- reads `getState()[key]`, else `initialViewPreferences[pref] !== false` (or `=== true`), else
  the default;
- applies a root attribute and the `aria-pressed`, `aria-label`, `title` and `data-tooltip` of
  one button;
- on click, toggles, applies, merges `setState({...state, key})` and posts
  `previewViewPreferenceChanged`.

`tocColumn.ts`, `anchorMode.ts`, `themeMode.ts`, `widthMode.ts` and `viewControls.ts` repeat the
read-state, merge-state and post part with non-boolean values.

- Proposed helper: `src/page/modules/viewPreference.ts`, with
  `installViewPreference({ stateKey, preference, read(initial), post })` returning
  `{ value, set(value) }`, plus `installBooleanToggle({ button, rootAttribute, labels, … })` on
  top of it.
- The three boolean modules become about 15 lines each. The others call the helper for their
  state part.
- Saving: **90 to 120 lines.**
- Risk: low for the three toggles. Their tests compare exact labels and attributes. Medium for
  the five others: default precedence differs per choice. For example, the zoom saved with the
  panel wins over the stored zoom (THEME-049), while the theme starts from the stored value
  first (THEME-007). Keep the precedence per call site; do not unify it.
- Guards: `test/page/runtimePageControls.test.ts` (39 tests),
  `test/page/modules/commentsToggle.test.ts`, `test/core/state/previewViewPreferences.test.ts`,
  `test/integration/storedChoices.ts`, visual scenarios toolbar-navigation and theme-zoom.

## S6. Page round trips outside `installHostRequests`

`installHostRequests` (`src/page/modules/hostRequests.ts`, 87 lines) already does the edit id,
the `<type>Result` match, the timeout, the dialog state and `cancelAll`. Three modules rebuild it
by hand:

- `labelRename.ts`: `pending = { editId, timer }`, 6 s timeout, its own match in `receive`.
- `commentCompose.ts`: `sending` timer, 15 s, "no answer" text.
- `commentThreads.ts`: an `act` map per thread for reply, resolve and delete, 15 s each.

To migrate them without a behaviour change, `installHostRequests` needs two options:

- `timeoutReason`: today the text is fixed, "The editor did not answer. Try again."; the comment
  modules show their own text;
- `timeoutMs: undefined` means "no timeout". `checkboxes.ts` has no timeout today, so it is
  **not** migrated unless that option exists.

Also out of scope:

- `blockMoves.ts` and `blockSelectionView.ts`: their answers are matched by render, not by edit
  id (`previewBlockMoveResult`, `previewBlocksResult`), and their 5 s timer only forgets the
  flight.
- `inlineThread.ts` already uses `deps.ask`.

Saving: 50 to 70 lines, which also gives `commentThreads.ts` room under 800. Risk: medium. These
are timing paths, and the comment answers may be matched by request rather than by edit id, so
check each `receive` before the switch. Do one module per commit.

Guards:

- `test/page/modules/labelRename.test.ts` (7), `renderReq.labelRename.requirements.test.ts`;
- `commentCompose.test.ts` (14), `commentThreads.test.ts` (37), `hostRequests.test.ts`;
- `test/integration/labelRename.test.ts` and the comments integration suite.

## S7. Read-only refusal in the dispatcher gate (optional)

After S1, the read-only check is still made in 9 handlers. `PageMessageDispatcher.handlePageState`
already refuses `EDIT_REQUEST_TYPES` for the page-state family.

- Proposal: a `READ_ONLY_REFUSALS: Partial<Record<PageToHostType, { reason, post }>>` table,
  applied after the render gate for every gated type.
- The outcome is the same: today the handler's read-only check also runs only after the render
  gate passes.
- Saving: 20 to 30 lines, and the cross-cutting SwRS gets one implementation point.
- Risk: medium. The `post` of each type must keep its answer shape (`error` for checkbox, `ok`
  plus `reason` for the others), and the trust text differs per type. Do it only if S1 leaves
  the handlers still noisy.

## S8. Status line helper (optional)

There are 13 sites in 12 page files that set `textContent` and toggle `data-visible`. A
`showStatus(element, text)` in `src/page/modules/` saves 10 to 15 lines. Low value, low risk.
Fold it into S6 where the same modules are touched.

## Expected effect on the 800-line ratchet

| File | Now | After |
| --- | ---: | ---: |
| `src/session/features/sourceEdits.ts` | 460 | ~340 (S1, S3) |
| `src/session/features/hostRequests.ts` | 302 | ~275 (S2, S3) |
| `src/page/modules/commentThreads.ts` | 773 | ~730 (S6) |
| `src/page/modules/editPalette.ts` | 766 | ~781 with 15 markers folded back from the companion; under 800 |
| New helpers | | ~60 (`guardedEdit.ts`) + ~50 (`viewPreference.ts`) + ~10 (`replyEnvelope`) |

Net change in `src/`: about **−320 to −400 lines** (S1 to S6). That is less than 1 % of the 51 000
lines. The gain is mainly one place per rule, which matches the cross-cutting SwRS.

## Follow-up PR plan

Runs after PR #62 is merged into `master`, on a new branch from `master`, for example
`refactor/059-shared-guards`. It changes code only; requirement text changes only where a marker
moves with its code. The tile ids come from the reduced baseline of PR #62.

### Preconditions

- PR #62 merged; `just preflight` green on `master`.
- Read `.agents/constitution.md`, `CONTRIBUTING.md` ("Architecture", file size ratchet) and this
  document's item before each commit.
- Record the line counts of the touched files (`wc -l`) in the PR description, before and after.

### Commits, in order

| Order | Item | Commit message | Suites to run besides `just check` |
| --- | --- | --- | --- |
| d1 | S3 reply envelope | `refactor(session): one reply envelope for page answers` | `test/session/**`, `test/core/protocol/**` |
| d2 | S1 guarded source edit | `refactor(session): guard source edits in one place` | blockReq, reviewReqThreads, labelRename and trustReq session suites; integration blockMove, blockClipboard, labelRename, checkboxToggle |
| d3 | S2 host request guard | `refactor(session): share the host request guard` | paletteReq, pasteImageWrite; picker integration |
| d4 | S4 host decode helper (host copies only) | `refactor(core): one percent decoder for links and resources` | previewNavigation, resource-policy, previewNavigator |
| d5 | S5 view preference helper | `refactor(page): one view preference helper` | runtimePageControls, commentsToggle, previewViewPreferences, storedChoices; visual groups toolbar-navigation and theme-zoom |
| d6 | S6 page round trips, one commit per module (labelRename, commentCompose, commentThreads) | `refactor(page): route <module> through host requests` | labelRename, commentCompose, commentThreads, hostRequests; comments integration |

S7 and S8 are optional. Do them only if d1 to d6 are green and the maintainer asks.

### Rules per commit

- No assertion changes. Reason texts, check order, timeouts and answer shapes stay byte for byte.
  An item that cannot keep them is dropped, not bent.
- Markers move with the code: the `@implements_req` of a tile goes to the new helper when the
  helper now produces the behaviour, and stays at each caller that still has its own part. Run
  `okfreq update-coverage requirements` and commit the regenerated coverage fields with the code.
- Known issues stay. S4 keeps the page copy of `decodePath` because merging it would fix the
  TOOLBAR-119 known issue silently. Fixing it is a separate `fix:` commit with code, test, SwRS
  update and backlog item together, not part of this PR.
- No new dependency-cruiser exception; helpers go in the lowest layer that may hold them.
- Every touched file shrinks or stays the same (800-line ratchet).

### Gates

| When | Gate |
| --- | --- |
| Every commit | `just check`, plus the suites of the row above |
| Every commit | `okfreq update-coverage requirements --check`, `okfreq trace requirements --json` (`missing_ids` = 0, `duplicates` = 0) |
| After d2, d5 and d6 (timing-sensitive) | `just preflight` |
| End of PR | `just preflight` (allow up to 3 runs for the known VS Code focus timeouts; report them separately) |

### Effort

About 15 agent-hours: d2 and d5 about 4 h each, d6 about 4 h for the three modules, the others
about 1 h each.

