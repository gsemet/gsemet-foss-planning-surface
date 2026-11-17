# Backlog (P3, owner decision needed): should a click in an admonition body open the whole directive?

Found by CR 184 (2026-10-29, PR #198). Today a click in the BODY of a MyST admonition (`:::{note}` /
```` ```{note} ````) opens only the clicked paragraph; only a click on the title opens the whole
directive. BLOCK-014 claimed the whole directive opens; CR 184 recorded the real behaviour as a
Known issue in SwRS-MDOKFSTUDIO-BLOCK-014 and pinned it with a test.

GitHub alerts now open as a whole (CR 184), so alerts and admonitions differ.

- Option A: align admonitions with alerts (a body click opens the whole directive). Simple mental
  model; large directives open a big editor for a one-word fix.
- Option B: keep paragraph-level editing in admonition bodies and document it (update BLOCK-014).
- Decision: owner. If A: same mechanism as `src/page/features/mappedBlocks.ts` alert rule; flip the
  pinned known-issue test.

## Decision (owner, 2026-10-29): decided A by the owner

Option A: a click in an admonition body opens the whole directive, like GitHub alerts. Moved from
P3 to P2 and run as CR 200, stacked on the CR 199 v2 PR.
