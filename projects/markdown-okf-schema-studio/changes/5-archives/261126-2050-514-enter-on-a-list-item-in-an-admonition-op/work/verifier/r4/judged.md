# CR-514 verification

Head: f9dc2c630b852635e8bffcd0b00b42cc886b293c

Base of every "before": `5f0746d79ca28e564841daa19288075aa7823776` (`origin/main`). Fourth
verification, a short pass on the posted description of pull request 540. The first verdict at this
head is kept as `verify-f9dc2c6-first.md` (NOT VERIFIED on its claim C, the card sentence of Known
gaps). The code did not change since; the description did. Verdict at the end: VERIFIED.

Placeholders: `<wt>` the CR worktree; `<r3>`, `<r4>` = the folders `verifier/r3`, `verifier/r4`
beside this file; `<node>` = `fnm exec -- node --import ./scripts/register-myst-patches.mjs`, run
from `<wt>`; `<chantier>` the CLI of the brief with `--batch batch-09`; the other placeholders of the
carried claims are `<base>` = a detached base worktree used by the first verdict (since removed),
`<repro>` and `<r2>` = `verifier/repro` and `verifier/r2`.

## Judged in this pass

### D0. Only three Known gaps bullets changed: VERIFIED (f9dc2c6)

- Command: `gh pr view 540 --json number,headRefOid,isDraft,title,body,updatedAt,state,baseRefName`
  (saved as `verifier/pr-540-f9dc2c6-second.json`); `git rev-parse HEAD`
- Output: head `f9dc2c630b852635e8bffcd0b00b42cc886b293c` on both, draft, OPEN, base `main`, same
  title, updated `2026-11-26T19:39:07Z`.
- Command: `python -I verifier/desc-diff.py <work>` (the body judged by the first verdict,
  `pr-540-f9dc2c6-end.json`, against the one posted now; log `verifier/desc-diff-f9dc2c6.log`)
- Output: `old chars 14243 new chars 14542 local chars 14542`,
  `posted equals pr-body.md (trailing newline ignored): True`, and three `replace` hunks only: the
  bullets "Clicking the first paragraph of a tight list item", "Emptying the first block of a box
  body" and "A card of a box". Nothing else is new.

### D1. The card bullet (failed before as claim C): VERIFIED (f9dc2c6)

Posted: "A card of a box loses words of its body when a `---` line that no second `---` line closes
stands right under the card's opening line (it is read as the start of a block of options), and a
`{div}` that is not shown as a box (the callout class written as its argument) and starts with `---`
stops the preview (both as before this change); the move chord does not refuse to write that in such a
`{div}`."

- Command: `<node> <r4>/three.js <wt> C` (log `r4/three-C-f9dc2c6.log`)
- Output: with the unclosed line right under the opening line, all 7 body shapes in all 4 card
  spellings lose a word (`missing=Beta`, and `missing=Alpha` for the one-word body); the DOM shows the
  lines read as options (`<code .shiki.language-yaml>`). A closed block and a `---` after a blank line
  show every word (`missing=-`). The three `{div}` callout-argument spellings throw
  (`THROWS Cannot read properties of undefined (reading 'length')`) for every body that starts with
  `---`, blank line first or not; a closed options block draws.
- Command: `<node> <r3>/cards2.js <wt>`, then `cmp` with `r3/cards2-5f0746d.log` (base)
- Output: `cards2-same-as-base`: 315 pages, byte-identical to the base ("as before this change").
- Command: `diff` of the "cards and divs with dashes" section of `r3/gapsC-f9dc2c6.log` and
  `r3/gapsC-5f0746d.log`
- Output: `cards-and-divs-section-same-as-base` (the `{div}` throws on the base too).
- Command: `<node> <r2>/calloutdiv.js <wt>`, then `cmp` with the first verdict's log
- Output: `calloutdiv-same`: in `{div} with class argument, ---` the chord answers `ok=true`, writes
  the `---` first and the page `THROWS`; the `:class:` spelling and the fence div are refused.

### D2. "Emptying the first block of a box body": VERIFIED (f9dc2c6)

- Command: `<node> <r4>/three.js <wt> B` (log `r4/three-B-f9dc2c6.log`: click the first paragraph,
  empty the editor through `PreviewManager`, render again; every case keeps `Lastword kept=true`)
- Output: `{admonition}` with a title, 10 spellings (colon and backtick fence, `:class: dropdown`,
  also with `:open:`, `:class: tip`, `:class: tip dropdown`, `:name:`, a title with markup): title
  "Admonition", its own title as a body paragraph, nothing else of the box. `{note}`, `{tip}`,
  `{warning}`, alert, callout, callout with a `title` attribute: the title only. `{dropdown}`: no box.
  `{dropdown}` with `:open:`: `after THROWS value.replace is not a function`.
- The heading half of the first sentence is unchanged: carried from f9dc2c6 (`gapsC-f9dc2c6.log`:
  `note|heading` after shows "Headword" as the title).

### D3. "Clicking the first paragraph of a tight list item": VERIFIED (f9dc2c6)

- Command: `<node> <r4>/three.js <wt> A` (log `r4/three-A-f9dc2c6.log`: 8 following contents in a
  note, a dropdown and an alert; the arrows walked with the real `structuralMove`; each editor emptied)
- Output: "click on first paragraph" opens the `<li>` with the following content in all 24 cases and
  `after emptying, content left=false`. "Enter on the item" (`block 1, Right, Right`) does the same in
  all 12 HTML comment and HTML cases.
- Observation, not counted: Enter on the whole item takes the hidden content for the other listed
  kinds too. What differs by kind is Enter on the item's first paragraph (one Right further): of the
  listed contents it takes only an HTML comment or HTML written with no blank line before it. The
  sentence is true as written and does not say otherwise.

### D4. The posted description renders, with no new claim, name or mark: VERIFIED (f9dc2c6)

- Command: `gh api repos/gsemet/markdown-okf-schema-studio/pulls/540 -H "Accept: application/vnd.github.html+json" --jq .body_html`,
  then `python -I <r4>/rendered.py <r4>/pr-540-body.html` (log `r4/rendered-f9dc2c6.log`)
- Output: headings `Summary, Deliverables, Changes, Impacts, Blast radius, Autonomous decisions,
  Known gaps, Test plan, Internal references`; each of the three bullets renders as one list item with
  its whole text. Their text (D0) names no role as a doer, no person and no path, and adds no mark.
- Command: `gh pr checks 540`; `git ls-remote origin refs/heads/main <branch>`; first and last lines
  of `work/gates/prepush-f9dc2c6-preflight.log`; `<chantier> handoff CR-514`
- Output: `checks`, `report`, `static`, `static-windows`, `viewer-graph`, `visual`, `visual-2` pass,
  the others skipping; branch `f9dc2c63...`, main `5f0746d7...`;
  `head f9dc2c630b852635e8bffcd0b00b42cc886b293c base 5f0746d...: just preflight`, `exit 0`,
  `tree checked`; handoff: rounds 6 of 6, head f9dc2c6.
