# 200 — Admonition body click opens the whole directive

Night batch 2026-10-28 (user request via the Chief of Staff). From origin/main, one PR.

Backlog intent (verbatim):

> # Backlog (P3, owner decision needed): should a click in an admonition body open the whole directive?
> 
> Found by CR 184 (2026-10-29, PR #198). Today a click in the BODY of a MyST admonition (`:::{note}` /
> ```` ```{note} ````) opens only the clicked paragraph; only a click on the title opens the whole
> directive. BLOCK-014 claimed the whole directive opens; CR 184 recorded the real behaviour as a
> Known issue in SwRS-MDOKFSTUDIO-BLOCK-014 and pinned it with a test.
> 
> GitHub alerts now open as a whole (CR 184), so alerts and admonitions differ.
> 
> - Option A: align admonitions with alerts (a body click opens the whole directive). Simple mental
>   model; large directives open a big editor for a one-word fix.
> - Option B: keep paragraph-level editing in admonition bodies and document it (update BLOCK-014).
> - Decision: owner. If A: same mechanism as `src/page/features/mappedBlocks.ts` alert rule; flip the
>   pinned known-issue test.
> 
> ## Decision (owner, 2026-10-29): decided A by the owner
> 
> Option A: a click in an admonition body opens the whole directive, like GitHub alerts. Moved from
> P3 to P2 and run as CR 200, stacked on the CR 199 v2 PR.

## Owner decisions (2026-10-29, via the Chief of Staff)

1. Option A: a click in an admonition BODY (`:::{note}` and the backtick fence form) opens the
   whole directive, as GitHub alerts already do (`src/page/features/mappedBlocks.ts` alert rule).
   Update SwRS-MDOKFSTUDIO-BLOCK-014 and remove its Known issue line; flip the pinned known-issue
   test.
2. BLOCK-047 stays as is: when the whole window loses focus, the block editor commits and closes.
   No code change. Add this decision to the rationale of SwRS-MDOKFSTUDIO-BLOCK-047 (separate
   commit, doc only).

Proof: unit test, headless visual test with a real click on an admonition body, before/after
screenshots in the PR body. Ready PR (not draft), stacked on the CR 199 v2 PR
(`change-requests/199-focus-studio-editor-group-v2`). Until that branch exists, work from
origin/main and do not push; once it exists, rebase onto it (local, before the first push) and
open the PR with that base.
