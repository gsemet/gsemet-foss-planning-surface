# 265: comment editor position, scroll and dismissal

Owner's report: `01-intent.md`. Behaviour: `02-answers.md`.

## Done means

Each of the four bugs is reproduced by a test that fails on the unchanged code, and passes after. Code
starts in `src/page/modules/commentCompose.ts`, `commentThreads.ts` and
`src/core/preview/styles/commentStyles.ts`; `commentThreads.ts` is close to the 800-line limit.
Update or add REVIEW SwRS. Approved requirements stay unchanged: the owner cannot agree tonight; if a fix
needs one changed, stop and return blocked with the question.
