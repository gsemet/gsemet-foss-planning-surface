# Review round 2 — CR 225 (Replace all skips blocks with a link URL match)

Verdict: APPROVE

Reviewed: the whole uncommitted change in `markdown-okf-schema-studio-wt-225` on top of origin/main
0b4ede78 (src, tests, requirements, the new TOOLBAR-131), against the owner-approved behaviour note
(choices A–D) and the round-1 findings. `just unit`: 3335 pass, 0 fail. Visual, integration and
real-window tests not run (per brief); the real-window scenario was traced by hand.

## Round-1 findings

1. **Closed** — `test/integration/findInPreview.test.ts`. Traced the Replace all step (match case on,
   query `studio`, replacement `atelier`) over the SOURCE, occurrence by occurrence:
   - `# Studio field notes`, `The Studio preview`, the admonition's `the Studio`, `about the Studio`:
     capital S, not matched with match case on. The admonition has no title (`Note`).
   - `and the studio keeps`: block source has 1 occurrence (case-sensitive, the planner regex has no
     `i` flag) = page 1, replaced.
   - `the studio table cell`: TD mapped to its row line, 1 = 1, replaced (unchanged from before).
   - `[studio link](https://example.com/studio)`: the target is now a hidden span, 1 = 1, label
     replaced, URL kept (checked with the bundled planner: `[PIN link](https://example.com/studio)`).
   - `$studio + 1$`: KaTeX always sets `aria-hidden="true"` on `.katex-html`
     (node_modules/katex/dist/katex.mjs:5724) and `.katex-mathml` is in `SKIPPED_SELECTOR`
     (src/page/modules/findIndex.ts:49); `typeset` throws instead of falling back to raw text, and
     the formula is valid. Not a page match, nothing sent.
   - New `A st**udio** split by markup...`: the find index joins the text nodes of a block, so the
     page has one match `studio` (occurrence 0 of 1); the source block has 0 occurrences, so the
     host skips it. Checked with the bundled planner (no edit).
   Result: host answers replaced 3, skipped 1; the page sends every match (all blocks mapped), so
   `pageSkipped` = 0 and the note is exactly `Replaced 3 matches; 1 match cannot be replaced from the
   preview` (src/page/modules/findBar.ts:439-440). The `message` survives the post-edit `refresh()`
   (it only resets on find/replace input and option toggles), so the exact-equality assertion is not
   racy. The expected string is SOURCE with the three replacements; `.replace` hits the first
   occurrence, which is the only one in each case.
   Other assertions: the case-insensitive total is read from the page (`1 of \d+`, `>= 7`): it is now
   8 (7 before), still `>= 7`; "a narrower count" holds (8 → 4); `hidden gem` is still `1 of 1`; the
   dark part only fills the field and closes. No screenshot is compared to a baseline (the shots are
   only written); `test/shared/stressPlan.ts` and `test/integration/realInput/run.ts` only name and
   call the scenario. No other scenario uses this SOURCE.
2. **Closed** — fenced code. `fencedCode` finds ``` / ~~~ fences (also behind `>` and list markers),
   the scanner jumps over them and definitions overlapping code are dropped; the definition regex
   allows 0–3 spaces only. Round-1 repro now skips (no wrong edit) for backtick, tilde, quoted,
   listed and CRLF fences; a link inside a fence is counted and the visible one replaced. Over-detecting
   a fence (e.g. an indented ``` line) only stops hiding, which can only add source occurrences, so it
   ends in a skip, never a wrong edit. Remaining false hiding (a link inside a 4-space indented code
   block) lowers the source count of a block whose text is all visible, so it also ends in a skip.
3. **Closed** — `test/visual/capture_find_checks.py:64` filters `!item.dryRun`. In the read-only page
   no dry run is sent at all (`replaceBlockedReason()` is set).
4. **Closed** — the dry run sends `replacement: ""` (`itemsFor(matches, false)`), accepted by
   `isFindReplaceItem` (length <= max, empty allowed), and the host returns before `apply` when
   `dryRun === true`; the replacement text is never used for the counts. No length gate left.
5. **Closed** — "no link inside a link": `[a [b](needle) d](needle)` now replaces the visible outer
   `needle` and keeps the inner target (CommonMark renders the outer one as text).

## Other checks

- Tests fail before: on origin/main the planner refuses the list-with-link case, `[a](needle) needle`
  and the link-in-link case (bundled HEAD planner); the dry-run, validator and session tests assert
  behaviour HEAD does not have.
- Requirements: TOOLBAR-012 and StRS TOOLBAR-003 are `req_lifecycle: draft` (draft on origin/main
  too); TOOLBAR-131 is `req_lifecycle: proposed` (`status: stable`, like the 40 other proposed SwRS).
  No approved requirement edited. Log entry, index row and StRS link present. Markers
  `@implements_req` / `@tests_req` TOOLBAR-131 present in code and tests.
- File sizes: findBar.ts 672, findReplace.ts 237, sourceEdits.ts 507, findBar.test.ts 551 (< 800).

## Findings

1. **nit (no action required)** — `test/integration/findInPreview.test.ts:276`. The comment above the
   count still reads "Headline, paragraph x2, admonition, table, link, math, last words": the math is
   not searchable and the new split paragraph is. Suggest "Headline, paragraph x2, admonition,
   table, link, the split word, last words". The assertion (`total >= 7`) is right either way.
