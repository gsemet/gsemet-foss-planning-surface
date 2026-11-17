# Round 1 review: alert palette after a lazy continuation line

Verdict: **CHANGES REQUESTED**

Reviewed worktree `markdown-okf-schema-studio-wt-223`: uncommitted changes on top of `origin/main`
0b4ede78. Nothing in the worktree was modified. The two `src` files were swapped to their
originals to run the new tests, then restored. The checksum of `git diff` plus the untracked files
is the same before and after (`62c42884…`), and `out/` was recompiled from the restored sources.

The core design is sound. One pure function (`blockQuoteEnd` / `blockQuoteAround`) is shared by
the render pass and the palette, the line mapping is right, and the palette caret and selection
math is right. Most of the GitHub table matches GitHub. Three inputs still render differently from
GitHub (all compared with `gh api markdown -f mode=gfm`), and two of them break inputs that
rendered correctly before this change.

## Blocking

### 1. Lazy setext-like lines become a heading, and the heading is used as the alert title

- Where: `src/core/render/mystGithubAlerts.ts:111`. Lazy lines are pushed raw into the MyST
  directive body.
- Cause: `blockQuoteEnd` is right to keep `===`, `--` (and `=`) as lazy text, as GitHub does.
  Inside the rewritten body, though, `a\n===` is a setext heading. The admonition then takes that
  heading as its title, and the body is left empty.
- Repro: `> [!NOTE]\n> a\n===\n` renders `<aside … data-line="1" data-end-line="3"><p
  class="admonition-title">a</p></aside>`. No "Note" title, no body. `> [!NOTE]\n> a\n--\n` gives
  the same result.
- GitHub renders the title "Note" and the body `<p>a<br>===</p>`.
- This is a regression. Before the change, the alert rendered correctly and `===` was a paragraph
  outside it.
- Fix: write lazy lines into the body so they cannot change its block structure. For example,
  escape a leading setext underline character (`\===`). The rewrite is render-only, so the
  document is not touched. Add these rows to `GITHUB_CASES`.

### 2. A list item that cannot interrupt a paragraph still ends the alert on GitHub

- Where: `src/core/syntax/blockQuoteRange.ts:28` (`INTERRUPTING_ITEM`) and `:72`.
- Cause: on a lazy line the block quote does not match, so the open container is the document,
  not the paragraph. The CommonMark rule "only `1.` or a non-empty item interrupts a paragraph"
  therefore does not apply. cmark-gfm and commonmark.js behave this way.
- Repro: `> [!NOTE]\n> a\n2. x\n`.
  - Ours: one alert on lines 1 to 3 holding "a 2. x".
  - GitHub: the alert holds "a", then `<ol start="2"><li>x</li></ol>`.
- Repro: `> [!NOTE]\n> a\n-\n`.
  - GitHub: the alert holds "a", then an empty `<ul><li></li></ul>`.
  - Ours: the `-` hits finding 1, and the alert title becomes "a".
- The palette has the same error. With `> [!TIP]\n> a\n2. x`, the caret on `2. x` and WARNING, the
  TIP head is rewritten.
- This refutes the Coder's open point (a). The owner's spec says that a list item ends the alert,
  as on GitHub.
- Fix: on a lazy line, any list marker starts a block (`^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:[ \t]|$)`).
  Keep the stricter rule only for quoted lines inside an open paragraph (`> a\n> 2. x` stays text,
  which is correct). Add rows for `2. x`, `-`, `+ b` and `1) b` (GitHub ends the alert on the last
  two as well).

### 3. A table in the alert keeps the paragraph open, so the next unquoted line joins the table

- Where: `src/core/syntax/blockQuoteRange.ts:87-93`. Quoted table rows are treated as paragraph
  text, so `paragraphOpen` stays true.
- Repro: `> [!NOTE]\n> | a | b |\n> | - | - |\n> | 1 | 2 |\nfoo\n`.
  - Ours: `foo` becomes a table row (`<td>foo</td>`) and the alert ends on line 5.
  - GitHub: the alert holds the table, then `<p>foo</p>` follows outside it.
- Before the change, `foo` rendered outside the alert, so this is a regression.
- A related case: in `> [!NOTE]\n> | a | b |\n| - | - |\n`, the lazy delimiter row turns the body
  into a table. GitHub renders it as text (`| a | b |<br>| - | - |`).
- Fix:
  - A quoted delimiter row after a quoted header row closes the paragraph, because a table is
    open.
  - A lazy delimiter row must be written so it stays text, using the same escaping as finding 1.

## Non-blocking

### 4. HTML block state differs from GitHub

- Where: `src/core/syntax/blockQuoteRange.ts:65-96`.
- `htmlBlock` stays set until a blank quoted line, but HTML block kinds 1 to 5 end on their end
  marker.
  - Repro: `> [!NOTE]\n> <!-- c -->\n> text\nlazy`. GitHub puts "lazy" in the alert; ours puts it
    outside.
- HTML block kind 7 is not detected when no paragraph is open.
  - Repro: `> [!NOTE]\n> # h\n> <custom-x>\nlazy`. GitHub puts "lazy" outside; ours keeps it in
    the alert.
- Both cases are rare. Fix them or record them as a known issue.

### 5. The palette now finds alert heads inside fenced code through lazy lines

- Where: `blockQuoteAround`, `src/core/syntax/blockQuoteRange.ts:112`, which does not track
  fences.
- Repro: ```` ```\n> [!NOTE]\nfoo\n``` ````, caret on `foo`, argument TIP. The result is
  ```` ```\n> [!TIP]\nfoo\n``` ````: a literal inside the code block was rewritten.
- Quoted lines inside fences already had this problem before the change. The change extends it to
  unquoted lines.

### 6. A stale verification note contradicts the new normative text

- Where: `requirements/tiers/swrs/gfm/SwRS-MDOKFSTUDIO-GFM-009.md:159`.
- The note still says that `mystPaletteRendering.test.ts` covers "end at the first unquoted
  line". That wording now contradicts the normative text, and the test does not check it anyway.
  Reword the note.

### 7. A new comment sits between an existing comment and its code

- Where: `src/core/render/mystGithubAlerts.ts:91-96`.
- The new comment ("The alert runs over its quoted lines…") was added between the colon-container
  comment and the `let colons` line that comment explains. Move the colon comment back next to
  `let colons`.

### 8. For the owner: an alert inserted mid-paragraph absorbs the next line

- Inserting an alert on a middle line of a paragraph absorbs the next line.
- Repro: `Intro\nSecond\nThird`, caret on `Second`. The result is
  `Intro\n> [!NOTE]\n> Second\nThird`. `Third` is now, correctly, a lazy line of the new alert, so
  the preview pulls it into the alert.
- The text output is unchanged from before the change, and the spec only covers the line above.
  The owner may want the same blank line after the new alert as before it.

## What was checked and found correct

- Before the fix, the new tests fail. With the original `mystGithubAlerts.ts` and
  `blockEditActions.ts`, the three test files ran 25 tests with 9 failing. That matches the
  Coder's claim, and the failures are real behaviour assertions.
- The changed assertion in `alertSourceLines.test.ts` is the owner-approved change: the lazy line
  is now in the alert. The removed case (an alert followed by a list item) was re-added as a new
  test. No assertion was weakened.
- These inputs render as GitHub does or as CommonMark specifies, with the right `data-line` and
  `data-end-line`:
  - a lazy `---` is a thematic break that ends the quote (no setext heading; alert on lines 1-2,
    `<hr>` on line 3);
  - alert at EOF without a final newline (1-3);
  - lazy line, blank line, then a second alert with its own lazy line (1-3 and 5-7);
  - alert in a `:::{card}` with a lazy line, and the paragraph after the card (line 7);
  - `>\ta` with a lazy line;
  - a lazy continuation of a list item inside the alert;
  - CRLF;
  - an alert in a list item with an indented lazy line;
  - `> > [!NOTE]`, which is not an alert, as before.
- Palette:
  - The caret on a lazy line, or on a quoted line after lazy lines, is in the alert.
  - A selection keeps its range, and the caret follows the head-length change.
  - The blank line is added only when the line above is quoted or lazy, and the selection covers
    the quoted lines.
- Requirements:
  - GFM-009 and PALETTE-115 are both `proposed`.
  - In GFM-009, the frontmatter description is identical to the normative text, and the index is
    regenerated.
  - GFM-037 and all approved requirements are untouched.
  - The `@implements_req` / `@tests_req` markers are in place.
- Screenshots (`after-alert-lazy-{cream,dark}.png`): the lazy line is inside the Note in both
  themes. Before the change, it rendered as a separate paragraph. Plain quotes are unchanged.

## Gate results

- `just check`, first run: failed on one unrelated flaky test in
  `out/test/session/toolbarReq.requirements.test.js` ("one search per wikilink name runs at a
  time"). That file then passed 3 times out of 3 on its own.
- `just unit contracts security release-tests requirements-lint`, rerun: green. Unit 3329/3329,
  security 71/71, pytest 153 passed, requirements 1072 with 0 errors.
- `UV_NO_CONFIG=1 uv run --group requirements okfreq validate --check-links --project-root .`:
  1072 requirements, 0 errors, 21 warnings (the existing PALETTE-264 cross-link warnings).
- GitHub comparison: `gh api markdown -f mode=gfm` on every input quoted above.
- Probe scripts are in `/private/tmp/claude-502/cr223-driver/inspector/`.
