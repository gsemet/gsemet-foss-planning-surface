Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: code-blocks inventory

## Missing rows

Scripted: 26 checklist rows carry scope `code-blocks` or `code-blocks?` (CL 7, CTL 2, MSG 1, VIS 16).

- **C-CL-092** (MyST `{grid}`/`{toctree}` now render) is cited nowhere in the inventory
  and not listed in "Checklist corrections". It must be moved (to myst) or kept.
- **Moved rows not handled by the target scope**: C-CL-032 and C-CL-039 (to layout-width) and
  C-CL-057 (to theme-zoom) appear in no cell of `inventory/layout-width.md` or
  `inventory/theme-zoom.md` (grep of the id finds only code-blocks.md). The rule says a moved
  row counts only if the target cites it. Only C-CL-033 is OK (myst cites it, and its Checklist
  corrections table lists it).
- All other rows (CL-045, CL-096, CTL-001/002, MSG-001, VIS-035..038, 052..060, 256..258) are cited.

## Missing behaviours

None of substance. Minor, optional additions:

- The copy button hides when the pointer leaves the block (`mouseout`), and only blocks inside
  `#sphinx-myst-preview-content` get one (`blockOf` content check); neither is stated.
- A numbered/emphasized block in an unknown language is still line-wrapped without the `hljs`
  class (`shouldWrapLines` path, `highlight.ts`); and a grammar that throws falls back to escaped
  text when lines are wrapped (F-CODE-005 only mentions the unwrapped fallback).
- Inline `<code>` outside `<pre>` is never highlighted (regex needs `<pre><code>`).

## Wrong/unverifiable evidence

Spot-checked 45+ claims by grep in the refactored worktree: all test names (highlight, codeCopy,
previewStyles, mystFeatures, pageToHost), symbols (`LANGUAGE_ALIASES`, `resolveLanguage`,
`classifyDiffLines`, `wrapCodeLines`, `decodeEntities`, `highlightLanguageNames`,
`MAX_COPY_TEXT_LENGTH`, `isBoundedString`, `EDIT_REQUEST_TYPES`, `matchesCurrent`,
`PAGE_MESSAGE_GATES.previewCopyText: "render"`, `router.on("previewCopyText")`,
`codeCopy.hide` in contentPatch, `clipboard.writeText`), CSS hooks and `data-myst-*` attributes
exist. Coverage states look right (F-CODE-024/025/027/028 have no tests; F-CODE-029 is consumed
and tested in `test/page/runtimeEditPalette.test.ts`, which the row could cite). No false
evidence found.

## Count check

Behaviours 30 / tested 22 / untested 8 match the table; the Untested list matches. Checklist
total is wrong: the table says 25 (17 + 4 moved + 4 new) but there are 26 rows (C-CL-092 is
missing). After moving C-CL-092 the total must be restated.

## Verdict

Fixes: (1) place C-CL-092 (move to myst, add to Checklist corrections, check myst cites it);
(2) make layout-width cite C-CL-032 and C-CL-039 and theme-zoom cite C-CL-057, or keep them
here with a reason; (3) fix the Counts row to 26 rows; (4) optionally add the minor behaviours.

Verdict: REVISE

## Re-check

- Fixes (1)-(3): C-CL-032/033/039/092 are cited by layout-width (F-LAYOUT-016/024) and myst (F-MYST-045..050, 055..067), and C-CL-057 is kept and cited (F-CODE-007/016; theme-zoom does not cite it). Counts row says 28, correct.
- DEFECT 1: `inventory/code-blocks.md` is corrupted. Lines 49-118 are a stale duplicate: a second "Checklist corrections" (old text, says C-CL-057 moves to theme-zoom, contradicting lines 50-66), a second copy of F-CODE-002..033 (lines 69-100) and a truncated line 68. Each F-id appears twice.
- DEFECT 2: Counts lists 17 undocumented, but only 16 F-rows say `undocumented`. F-CODE-026 is in the Counts list yet its Cov. says nothing of it. Evidence spot-checks (MAX_COPY_TEXT_LENGTH, mouseout, shouldWrapLines, CODE_BLOCK regex, others) were OK.
Re-check verdict: REVISE

Orchestrator note: the corrupted file (stale duplicate section) was repaired by an analyst and verified: each F-id once, 33 behaviours, 22 tested, 11 untested, 17 undocumented. Re-check verdict: APPROVE (fixed)
