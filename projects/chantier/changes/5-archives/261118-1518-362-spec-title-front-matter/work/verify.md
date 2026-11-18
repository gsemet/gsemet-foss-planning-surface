# Verify CR-362

Head: f1792cd79ce23802e6b7213eb7fbc8477bdf5f87

## Claims (all judged at f1792cd)

1. Shipped markdown.js hides the front matter. Command: `uvx --from nodejs-wheel==24.19.0 node verifier/probe.mjs <worktree>/.../board/web/js/panel/markdown.js` (log: verifier/evidence/node-after.log). Output:
   - plain: `<h3 class="md-h1">Title</h3><p>Text.</p>` (no type, cr-spec, description, `<dl`, `---`)
   - bom: same; crlf: same
   - empty (`---\n---\n# T\n`): `<h3 class="md-h1">T</h3>`
   - unclosed: `<p>--- type: x</p><h3 class="md-h1">Heading</h3>`
   - none: `<h3 class="md-h1">Title</h3><p>Text.</p>`
   Same probe at base 5717626d (node-before.log): plain/bom/crlf drew `<dl class="fm">...`; empty, unclosed and none identical to the after. Proved.
2. Python tests: `pytest skills/chantier/scripts/cli/tests/test_titles.py skills/chantier/scripts/cli/tests/test_board_description.py -q` -> `19 passed`. Proved. Diff touches only markdown.js and panel.css (`git diff --stat origin/main...HEAD`), tests unchanged.
3. No leftover `.fm` use: grep of board/web for `.fm` / `"fm"` finds nothing; DESIGN.md names no front matter style. No other title reader: grep `lstrip("#")|startswith("#")` in src finds only driver_prompt.py's concepts.md table parser (not a CR title). Proved.
4. PR 326 description: matches the diff (Summary, Deliverables, Changes: markdown.js skip, three .fm rules removed); renders; no images. Known gaps names the missing screenshot. Review box `approved at f1792cd` matches the log note "r1 approved at 5717626d, committed as f1792cd7". Proved.
5. CI green at f1792cd: Driver's note (gh pr checks 326, all 5 jobs pass); head of PR is f1792cd (`gh pr view 326`).
6. Board by hand with a screenshot: NOT CAPTURED. Serving `chantier board` needs a long-running server beside a browser capture, and my card forbids background shells. Not claimed; see verifier/evidence/before-after.md. The PR's Known gaps names it.

## Description-only pass, head f1792cd (PR 326 body re-read)

7. Before/after table values match node-before.log and node-after.log (plain/bom/crlf: dl+heading+paragraph before, heading+paragraph after; empty, unclosed, none identical). Proved.
8. Rendering: FAILED. `gh pr view 326 --json body -q .body | grep -n 'BOM or' | od -c` shows the first table row ends at "BOM or `" followed by a raw newline (the text "`
`" was posted as a real line break). The row is split in two, so the GFM table breaks. Fix: write the escape as `\r\n`-style text on one line (e.g. "plain, BOM or CRLF").
9. Test plan: first box "No behaviour change in Python" left unchecked with no reason; check it (tests 19 passed, claim 2) or drop it.

Superseded by the pass below.

## Description-only pass 2, head f1792cd79ce23802e6b7213eb7fbc8477bdf5f87 (PR 326 body re-read via `gh pr view 326 --json body`)

9. Rendering: table row now reads "plain, BOM or CRLF" on one line; the table has 4 rows, sections and the fold are intact; no image. Proved.
10. Test plan: all six boxes checked; first box cites 19 passing tests (claim 2). Proved.
11. Consistency: the quoted readFrontMatter equals the diff at f1792cd (`git diff 5717626d HEAD`: regexes `[^\S
]*`, returns 0 or end+1); Changes (markdown.js skip, three .fm rules removed) matches the 2-file diff stat; Autonomous decision matches the regex. Known gaps names the missing screenshot. Template audit: Summary, Deliverables, Blast radius, Autonomous decisions, Known gaps, fold with Changes, Impacts, Test plan, Internal references. Review box matches log note "r1 approved at 5717626d, committed as f1792cd7". Proved.

VERIFIED
