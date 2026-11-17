Verdict: APPROVE

# S8a, round 1: page runtime split (REVIEWER)

Reviewed the round diff on `changes-requests/056-refactor-host-neutral-core` (HEAD `0d94248` = S7,
`git diff HEAD -M` plus the untracked `src/page/features/*` and `test/page/runtime*.ts` files).
The review was read-only, and only this file was written.

## Gates (re-run by the reviewer, in the worktree, Node 24 via `fnm exec --`)

| Gate | Result |
|------|--------|
| `npx tsc -p .` | exit 0, clean |
| `npm run test:unit` | 2 302 / 2 302 pass |
| `UV_NO_CONFIG=1 UV_OFFLINE=1 just check` | exit 0: boundaries passed (223 modules), check-limits passed (560 files, 9 on the baseline), check-settings 18, unit 2 302, contracts 2, security 28, release-tests 31 |
| `npm run bundle` | `out/bundle/preview.js` is 287.9 kB. A HEAD build of the same file is 275.3 kB, so the bundle grows by 12.6 kB (+4.6 %). The `rt.*` property accesses do not minify; see I3 |

Process note: my first gate attempt was a background command that lost its `cd` and ran in the main
checkout. It only rebuilt that checkout's gitignored `out/` from its own sources, and
`git status` there is clean. Every result above comes from foreground runs in the worktree.

## 1. Behaviour equivalence: OK, checked at runtime and not only by reading

I instrumented both shipped bundles, HEAD's (built from `git archive HEAD` in the scratchpad) and
this round's, in the unchanged `test/page/runtimeHarness.ts`, using four boot variants: default,
`commentsEnabled`, `editingEnabled: false`, and saved `editMode: true`.

- **Listener order.** I grouped every `addEventListener` on `document`, `window` and harness
  elements by (target, event type) and compared the order inside each group, with the capture flag
  and a signature made of the listener's string literals. There are 26–31 groups per variant, and
  every group has the same order in both bundles. The overall cross-type order differs (for
  example, a capture `pointerdown` is now added after a `keydown`). That cannot be observed, since
  dispatch order only depends on the order within the same target and type.
- **Elements, timers and queries.** I recorded the calls to `document.createElement`,
  `setTimeout` (with its delay), `requestAnimationFrame`, `querySelector` and `getElementById`, and
  the posted message types, through load, flushed frames, an edit-mode toggle and a block click.
  The sequences are identical (276–293 calls, 37–50 of them at init). Element creation order is
  therefore preserved.
- **`EXPECTED_TRACE`.** `test/page/runtimeBundle.test.ts` is unchanged (`git diff HEAD` is empty).
  It still drives the shipped minified `out/bundle/preview.js`, so the path users run stays
  covered after the `vm` change.
- **Shared state.** Every closure `let` of the old file is now either on `rt.state` (the
  variables shared across features) or a local `let` of the one feature that uses it. I checked
  each one against the old usages: `layout`, `anchorMap`, `expectedScroll`, `lastPostedLine`,
  `frame`, `sourceScrollSequence` stay in scrollCore; `lastPointerDownAt` in tableCellEditor;
  `editHoverElement` in editMode; the selection and move timers in their own features;
  `pendingEditorOpen` in frontmatterEditor; the WeakSets in contentPatch. tsc strict proves there
  is no other reference to them. No feature copies a mutable value at install: the top-level
  destructurings only take stable objects (`document`, `state`, `tools`, `diagnostics`). The
  insertion points are exposed as a getter (`points: () => insertPoints`) and not as the array,
  which gets reassigned. `rt.parts` is only read lazily (`scrollCore.ts:23-24`) or after it is
  filled (`hostHandlers.ts:12`, called after `rt.parts = …`).
- **Late binding.** The `keepReadingLine` and `flushOpenEditorsThen` callbacks handed to the page
  modules now resolve `rt.scroll` and `rt.blockEditor` when they are called. In the old file,
  calling them during install would already have hit the TDZ of `layout` and `widthMode`, so no
  module calls them at install. The order is the same.
- **Host handlers.** The 19 `hostMessages.on` registrations keep their order and their return
  forms (the expression arrows of `labelRename.receive` and `plantUmlFileRequests.receive`). They
  are still registered after the window scroll and resize listeners.
- **Regex quirk (S5 N3).** `scrollCore.ts:483` keeps `/%[da-f]{2}/iu`, with a comment explaining
  why.
- **`previewState` (Description toggle).** HEAD wrote `documentId: context.documentId` and then
  spread the snapshot, which overwrote that key in place. The new destructuring gives the same key
  order and the same value.

## 2. Typing: OK

- No `@ts-nocheck`, `@ts-ignore` or `@ts-expect-error` remains in `src/`. There is no `any` in
  `runtime.ts` or the features, and no `as unknown as`.
- The one structural cast, `as Partial<PageRuntime> as PageRuntime` at `runtime.ts:142`, is
  justified by the slot-filling order that `runtime.ts` documents.
- The remaining casts are narrow DOM casts, about 45 of them. There are 74 non-null assertions,
  mostly on table edit indices, which is acceptable for verbatim moves.
- Every exported feature symbol has TSDoc. Every feature file is at most 599 lines (≤ 800).

## 3. Tests: OK

- **`runtime.test.ts` split.** It has 450 `test(` titles before and after, and they are
  identical. Its 2 153 assertion lines form an identical multiset. The line-multiset comparison
  against `HEAD:test/page/runtime.test.ts` misses exactly 44 lines: the shared helpers, now with an
  `export` prefix in `runtimeTestSupport.ts`. The only non-trivial added line is an import
  specifier. Every file is at most 1 172 lines (≤ 1 500).
- **The 10 module tests.** The diff touches only the harness lines (`vm.runInNewContext(fn.toString())`
  → direct call with `as never` fakes, plus `provideGlobalElement`) and one comment path. No
  assertion changed.
- **What the `vm` sandboxes no longer check.** They used to check that a module is self-contained
  (a module could not reach a global missing from the sandbox). Since S5 the page is a bundle, so
  that property is no longer needed. The shipped bundle stays covered by `runtimeBundle.test.ts`:
  its two "reads no name it does not declare" tests and `EXPECTED_TRACE`.
- **`provideGlobalElement`.** It writes `globalThis.Element`. That is safe under node:test's
  per-file process isolation (the default), and each test sets it before its install.

## 4. Ratchet and guard: OK

- The baseline only loses `src/page/runtime.ts` and `test/page/runtime.test.ts`. Nothing is added
  or raised.
- `SUPPRESSION_ALLOWLIST` is removed, and the check now applies with no exception.
  CONTRIBUTING.md is updated to match.
- Boundaries are green, with no new exception.
- `chipToggle.ts:116` now uses `readPreviewBootSettings(context).showComments`, which is
  `bootFlag(true)`, so the same `!== false` rule as before.
- The stale `toString` comments are gone from `anchorPolicy.ts`, `spanColors.ts`, `chipToggle.ts`
  and the module headers. `grep` finds no "injected with `.toString()`" or "self-contained" text
  left in `src/`.

## Findings

None blocking.

- **I1 (info): the move is not fully verbatim.** The report says "bodies moved verbatim", but
  there are two small deduplications:
  - `blockSelectionView.ts:165` `ownsKeys(...)` replaces three inline
    `["INPUT","TEXTAREA","SELECT"]…closest(...)` guards. It is equivalent: `Boolean(closest())`
    matches the old truthiness, and the `isContentEditable` arm is only on the two handlers that
    had it.
  - `frontmatterListEditor.ts:54` `itemInput(row)` replaces nine
    `row.querySelector?.("[data-okf-list-item-input]")`. It adds `?.` on the row, which only
    differs where the old code would have thrown on an undefined row, and none of the call sites
    can get one.

  No fix needed. The final PR text should say "moved with two small helper extractions".
- **I2 (info, carried over): `hostToPage.ts`.** The coder's open point 2, the "every constant is
  declared in its body" comment on `createHostMessageFilter`, stays accurate while
  `test/core/protocol/hostToPage.test.ts` and `router.test.ts` still rebuild that function with
  `.toString()`. Move those two tests to direct imports in S8b, or as a follow-up, and drop the
  comment at the same time.
- **I3 (info): bundle size.** The minified page bundle grows by 12.6 kB (+4.6 %), because the
  `rt.state.*` and `rt.<feature>.*` accesses no longer minify into closure locals. This is
  acceptable for a webview loaded from disk. Mention it in the PR if size is ever discussed.
- **I4 (info): pre-existing pin, not touched.** The `[da-f]` regex (S5 N3) is still logged for a
  later CR.
