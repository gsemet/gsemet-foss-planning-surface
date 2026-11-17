# Round 2 Inspector (Opus) — CHANGES REQUIRED

Not run by the Inspector (timeout): compile + the two new tests, and the revert check on
`src/session/features/comments.ts`. Must be run by the next round:
`npx tsc -p . && node --import ./scripts/register-myst-patches.mjs --test out/test/session/reviewReqComments.requirements.test.js`,
then again with only comments.ts reverted from a copy (restore exactly).

1. BLOCKING (likely the real cause of the reported bug): dropping `view` does nothing if the next
   `post()` returns early on the text hash (`hash === state.textHash && state.posted !== undefined`
   returns before `view` is checked). With `view` undefined and `textHash` equal to the sidecar hash,
   the view is never rebuilt; `shiftForEdits` then skips the preview on every later edit
   (`if (!view ...) continue`) and highlights stay on old lines until the sidecar changes or a reload.
   Happens today on the clean-document path (`shiftForEdits` sets `view = undefined`, schedules a post
   that reads the same sidecar text and returns). Can also defeat fix 2 when the file-watcher post of
   the write runs first.
   Fix: the early return also needs a view (`... && (state.view !== undefined || no stored threads)`),
   or clear `state.textHash` wherever `view` is dropped (`shiftForEdits` clean branch, `persistAnchors`
   revision-changed branch). Test: post, clean-document change, post again with the same sidecar text
   and a shifted document → expect the new line. REVIEW-119 verification line only holds when
   textHash differs; adjust.
2. Fix 1 (textHash after last staleness check): correct.
3. Fix 2 (revision captured before getText, drop view if changed): logically right; depends on 1.
4. Test 2 is a weak proof (hook runs at the read inside store.update, before the write). Test 1's
   design is right. Old-code failure of both unconfirmed.
5. Docs/markers OK; CHANGELOG overstates "checked again against the current text" given finding 1.
