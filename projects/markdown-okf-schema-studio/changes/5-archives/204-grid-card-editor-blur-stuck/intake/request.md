# 204 — Grid card block editor stuck after blur (#227)

P1 batch 2026-10-31 (user request via the Chief of Staff). Stack of 2 ready PRs: CR 203 (base main) then CR 204 (base CR 203). Never merge.

Backlog intent (verbatim):

> # Block editor in a grid card sometimes does not close on blur; the page stays stuck
> 
> GitHub issue #227 (filed 2026-10-31). While editing a card of the #225 grid, clicking outside the
> block editor did not save and close it; the page stayed in edit mode, Done/Cancel partly hidden by
> the palette. Not reproduced deterministically.
> 
> Suspects: focus moving into the palette that overlaps the text box (#225), or the blur commit
> suspension.
> 
> Owner decisions (2026-10-31):
> - Reproduce first, in a real window (heavy CI) and headless, on the issue's grid document.
> - Blur outside the editor (text box AND palette) must always save and close it.
> - BLOCK-047 stays: a whole-window blur commits and closes (owner decision 2026-10-29).
> - If not reproducible once the #225/#226 layout fix is in, report the attempts; no speculative fix.

## Delivery

- Stacked on CR 203 (`change-requests/203-grid-card-block-editor-layout`). Work from origin/main for
  the reproduction; before your first push, rebase locally onto the pushed 203 branch (never pushed
  yet, so no force needed) and open the PR with base = the 203 branch.
- Reproduce FIRST, on the issue's grid document (#225), both headless (page runtime / visual) and in
  a real window (integration scenario run by heavy CI; no local real-window tests). Try at least:
  click outside after typing; click in the palette then outside; Done/Cancel partly covered; focus
  moves into the palette; the blur commit suspension window.
- If reproduced: fix so that a blur outside the editor (text box AND palette) always saves and
  closes it; regression test that fails without the fix. BLOCK-047 stays as is (whole-window blur
  commits and closes).
- If NOT reproducible on top of CR 203: no speculative fix. Keep the repro tests if useful
  (they guard the behaviour), and write the attempts in the PR body / report; tell the Foreman.
- PR body: "Closes #227" only if fixed or the tests prove the behaviour; otherwise "Refs #227".
- Before/after screenshots on the issue's document in cream and dark if there is a visible change.
- CI: normal CI, then ONE heavy on this top PR:
  `gh workflow run ci.yml --ref change-requests/204-grid-card-editor-blur-stuck -f heavy=true`.
