# 266: comments not shown on a very long document

Owner's report: `01-intent.md`.

## Done means

Reproduce first, on a copy of `README.md` in a test workspace with comments created through the preview,
and find the real cause. Length is the owner's observation, not a proven cause: `README.md` also holds raw
HTML (`<div align>`, `<picture>`), images and tables. Do not assume; trace the anchor through
`src/core/comments/anchoring.ts` (its limits `MAX_CANDIDATES`, `MAX_FUZZY_TEXT`), `src/core/render/commentMarkers.ts`
and `src/page/modules/commentThreads.ts`, including any deferred rendering of a long page. The report says
what the evidence shows.

A test fails on the unchanged code and passes after. Update or add REVIEW SwRS. Approved requirements stay
unchanged: the owner cannot agree tonight; if a fix needs one changed, stop and return blocked with the
question.
