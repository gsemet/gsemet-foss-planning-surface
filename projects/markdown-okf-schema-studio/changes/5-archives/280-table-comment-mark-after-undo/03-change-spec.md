---
title: Change spec, comment mark restored with an undone row delete
cr: 280
slug: table-comment-mark-after-undo
source: QA271-03 (Medium, P2)
issue: none
date: 2026-11-10
base: origin/main (c478278d line, release/1.6.0)
---

# Change spec: comment mark restored with an undone row delete

## Problem

Fixture `synth/anchors-tables.md` with `anchors-tables.comments.json` (thread `t1` quotes "beta"
on line 13, thread `t2` "retry budget" on line 27). In edit mode, Row - on the beta row, Escape,
then Meta+1, Meta+z: the buffer equals the baseline and the row is back, but the page shows only
the `t2` mark. A webview reload does not bring `t1` back; only closing and reopening the preview
does. The sidecar on disk is unchanged. So the host keeps a wrong in-memory view of the threads,
not the page (a webview reload re-posts the host's view, see "Why the host" below).

## Root cause hypothesis

Code anchors (all on `origin/main`):

- `src/session/features/comments.ts`, `CommentsController.shiftForEdits`: picks between "shift the
  lines in memory" (`event.document.isDirty` true) and "drop the view, check every anchor again"
  (false). The comment says the second branch is for "a reload from disk, a revert or an undo to
  the saved text".
- `src/session/hostEvents.ts`, `onDocumentChanged`: returns early when `event.changes.length === 0`.
- `src/host-vscode/documents.ts`, `onDidChange`: forwards `event.document` (its `isDirty`) and
  `event.reason` (undo / redo) as `DocumentChange`.
- `src/session/features/comments.ts`, `post`: uses `state.view` as it is while `view.diskHash`
  equals the sidecar hash; a thread in `view.orphaned` stays orphaned until the view is dropped.
- `src/session/features/rendering.ts` (around line 546): on every `previewReady` (page load and
  after each content patch) `comments.posted` and `textHash` are reset and the view is re-posted.
- `src/page/modules/commentThreads.ts`, `apply`: a thread posted with `orphaned: true` goes to the
  "Orphaned comments" box, never to a mark.

Hypothesis. In VS Code the `onDidChangeTextDocument` event that carries the content changes reports
`document.isDirty` as it was before the change; the dirty flip arrives as a second event without
content changes, which `onDocumentChanged` drops. With the replay's steps:

1. Revert File: document clean, view rebuilt, `t1` anchored on 13.
2. Row - (minimal diff from `planBlockTextEdit`: delete from line 13 col 2 to line 14 col 2): the
   event says `isDirty: false`, so the view is dropped and the next `post` re-anchors against the
   text without "beta". "beta" is a short quote (< 12 characters), absent: `t1` is orphaned
   (`reanchorWith`, `src/core/comments/anchoring.ts`). Correct at that moment.
3. Meta+z back to the saved text: the event says `isDirty: true`, so `shiftThreadLines` only moves
   lines; `view.orphaned` still holds `t1`. Every later post, a webview reload included, sends
   `t1` with `orphaned: true`. A new preview session starts without a view and re-anchors: fixed.

Why the host and not the page: a webview reload re-posts `state.view` (rendering.ts resets
`posted`), and the mark is still missing; the page would place `t1` on line 13 if it were posted
with `orphaned: false`.

The hypothesis also explains the mirror case on a dirty document (shifted, never re-checked) but
not by itself: even with a correct dirty flag, an orphan stays orphaned while the document stays
dirty, whatever text returns (cut then paste the row, retype the word). The sheet's chosen direction
is "re-anchor threads whose quote reappears after a text change", which covers both.

First step of the developer (before the fix): confirm the stale `isDirty` with a probe in
`test/integration/commentAnchors.test.ts` (real VS Code: first edit of a clean document, then an
undo back to the saved text; record `isDirty` seen by `shiftForEdits` and the `orphaned` flags in
`preview.probe.lastComments`). The fix below does not depend on the answer, but the SwRS wording and
the code comment of `shiftForEdits` must state the observed behaviour.

## Change

1. `shiftForEdits`: an undo or a redo (`event.reason`) drops the view like a clean change does
   (checked again against the text, starting from the stored lines), whatever `isDirty` says. The
   code comment is corrected (the dirty flag of the event is the state before the change).
2. `post`: when the view is reused and holds orphaned threads, and the document text changed since
   the view was built (record the document revision in the view), the orphaned threads only are
   checked again against the current text with `reanchorThreads` (shifted lines as the start, D25
   rules unchanged: short quotes only inside the window, context first). A thread found again
   leaves `orphaned` and takes the found lines; the others are untouched. Anchored threads keep the
   shift-only path (no per-keystroke re-anchoring of every thread; REVIEW-094 and REVIEW-119
   unchanged for them). Cost: one `createDocumentIndex` per debounced post, only while an orphan
   exists.
3. Nothing is written: the sidecar still changes only on save (`persistAnchors`, REVIEW-119).

Not in scope: where an anchored thread whose line was deleted is shown while dirty (badge on the
next row), the revert of a dirty document (no `reason`; covered for orphans by point 2 only).

## Requirements (okfreq)

All in scope `review-annotations`, owner `default_owner_email`. None is `approved`: no owner
agreement needed.

| ID | Action | Lifecycle |
| --- | --- | --- |
| SwRS-MDOKFSTUDIO-REVIEW-119 | Amend the boundary scenario "Change of a clean document": add the row "An undo or a redo, whatever unsaved state the editor reports: the lines followed in memory are dropped and the threads are checked again"; add the test name to the verification notes. | proposed (stays) |
| SwRS-MDOKFSTUDIO-REVIEW-219 (next free number on origin/main; re-check at rebase, the stack may take it) | New: "An orphaned thread whose quote returns is placed again". When the document text changes while a thread is orphaned and its quote is found again under the re-anchoring rules, the extension SHALL post the thread on the found lines with orphaned false, without writing the comments file. Scenarios: nominal (row deleted then undone: mark back, sidecar unchanged); nominal (quote retyped in a dirty document); refusal (a short quote reappearing outside the 50-line window stays orphaned); boundary (no orphan: no extra check). Derives from StRS-MDOKFSTUDIO-REVIEW-008 and StRS-MDOKFSTUDIO-REVIEW-001. | proposed (`okfreq new ... --lifecycle proposed`) |

Markers: `@implements_req SwRS-MDOKFSTUDIO-REVIEW-219` on the orphan re-check in `post` (or the
helper it calls); `@implements_req SwRS-MDOKFSTUDIO-REVIEW-119` already on `persistAnchors`, add it
on `shiftForEdits`. `@tests_req` on each new test. Then `just requirements-update` and a dated entry
in `requirements/tiers/log.md`.

## Tests first (each fails on origin/main)

Unit / session (`test/session/reviewReqComments.requirements.test.ts`, memory host):

- "an undo or a redo drops the followed lines even when the document reports unsaved changes":
  change event with `isDirty: true` and `reason: "undo"` (then `"redo"`): `comments.view` is
  undefined. The existing test "a document without unsaved changes that changes drops the followed
  lines, a dirty one shifts them" keeps its assertions (a dirty change without a reason shifts).
- "an orphaned thread whose quote returns is posted again on its lines": view with `t1` orphaned,
  document text gains the quote back (dirty, no reason), schedule, post: `probe.lastComments` has
  `t1` with `orphaned: false` on the found line; the sidecar text is unchanged (no write).
- Refusal: short quote back but outside the window stays orphaned; no orphan: `createDocumentIndex`
  not called (spy or call count), so typing costs nothing extra.

Pure (`test/core/comments/anchoring.test.ts`): only if a helper is added to `anchoring.ts`
(for example re-checking a subset); otherwise none.

Integration (`test/integration/commentAnchors.test.ts`, real VS Code): row line deleted with a
`WorkspaceEdit`, then `undo`: `probe.lastComments` holds `t1` with `orphaned: false` on line 13.

Real-input (promoted replay): new `test/integration/realInput/tableCommentUndo.ts`,
`scenarioUndoRestoresCommentMark`, header naming the replay
`scenarios/271-c1b-3-undo-row-delete-keeps-comment-mark.json`. Inline document and sidecar (the
fixture `anchors-tables.md` table and its two threads, written by the scenario like
`tableEscape.ts` does with `withDocument`), side preview, edit mode, click cell "2" of the beta row,
toolbar Row -, Escape, focus the editor, Meta+z; assert the buffer equals the original and the page
has `mark[data-okf-comment-thread]` for `t1` and `t2`, and no `[data-okf-comment-orphan="t1"]`;
the sidecar bytes are unchanged. Register it in `test/integration/realInput/run.ts` (full run and
the `single` map, key `table-comment-undo`).

Replay promoted: `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1b-3-undo-row-delete-keeps-comment-mark.json`
with its fixtures `assets/synth/anchors-tables.md` and `assets/synth/anchors-tables.comments.json`,
taken from local branch `qa/271-table-campaign-replays` (87307e8f) with
`git checkout 87307e8f -- <those three paths>` (the fixtures are shared with QA271-02 and QA271-10
replays: whichever CR of the stack lands first adds them, later ones skip them).

## Files expected to change

- `src/session/features/comments.ts` (shiftForEdits, post, CommentsState.view gets the revision)
- `src/core/comments/anchoring.ts` (only if a subset helper is added)
- `test/session/reviewReqComments.requirements.test.ts`
- `test/integration/commentAnchors.test.ts`
- `test/integration/realInput/tableCommentUndo.ts` (new), `test/integration/realInput/run.ts`
- `requirements/tiers/swrs/review-annotations/SwRS-MDOKFSTUDIO-REVIEW-119.md`,
  `.../SwRS-MDOKFSTUDIO-REVIEW-219.md` (new), generated okfreq indexes and coverage files,
  `requirements/tiers/log.md`
- `.agents/skills/markdown-studio-exploratory-qa-claude/scenarios/271-c1b-3-undo-row-delete-keeps-comment-mark.json`,
  `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/anchors-tables.md`,
  `.agents/skills/markdown-studio-exploratory-qa-claude/assets/synth/anchors-tables.comments.json`
- `docs/releases-notes/` entry if the release-notes check asks for one.

No page code, no rendered syntax: the writing skill is untouched.

## Blast radius and stack order

Behaviour: only review-thread placement after edits (scope review-annotations). No table, front
matter or rendering code changes, so CRs 277-279 and 281-282 do not touch the same source files.
Shared files with the stack: `test/integration/realInput/run.ts` (every CR that promotes a
real-input replay adds a line), `requirements/tiers/log.md` and the generated requirements files
(always conflict, resolved by re-running `just requirements-update`), the shared QA fixtures above,
and the next free SwRS number. CR 277 (preview stale after undo or revert) also reacts to undo
events; if it changes `src/session/hostEvents.ts` `onDocumentChanged` (for example the empty-changes
guard), put 280 on top of it and re-run the session tests. Otherwise 280 can sit anywhere in the
stack.

Risk: point 2 re-checks orphans after any text change, so an orphan may re-attach while the user
types a short quote back near its old place; that is the intended direction and still follows D25.
`comments.ts` stays under the 800-line ratchet (about 560 lines now).

## Gates

- `just check` (types, boundaries, file size, unit, contract, requirements lint through it).
- Headless visual and e2e of the group: `review-annotations` (and `table-editing` as a smoke, the
  replay runs a table edit); real-input single scenario
  `STUDIO_REAL_INPUT_SCENARIO=table-comment-undo`.
- `okfreq validate --check-links --project-root .` and coverage as CI runs them.
- Heavy CI on the branch: `gh workflow run ci.yml --ref <branch> -f heavy=true` (integration and
  real-input jobs run in real VS Code; the stale-dirty-flag behaviour only shows there).
- `just preflight` before the PR is ready.

## Open questions

None for the owner.
