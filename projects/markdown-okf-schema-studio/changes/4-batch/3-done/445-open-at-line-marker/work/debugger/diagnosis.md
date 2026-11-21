# CR-445: why the line-marker visual scenarios are red (ci run 44857022866)

Reproduced locally on Windows (the visual harness runs here, Playwright Chromium):

    just compile  (or: npm run visual:render)
    uv run --no-sync --group docs python test/visual/capture.py --scenario lifecycle-sync/v04-line-marker-code-line-light-900 --workers 1

It fails exactly as in CI ("one marker is drawn: expected 1, found 0"). Probes in this folder
(run from the worktree after `npm run visual:render`): `trace_run.py <scenario id>` (timeline of the
marker through the real `run_scenario`), `prove_fix.py` (the scenarios with the fix below, simulated
by a monkeypatch), `probe_rest.py`, `probe_v07.py`, `probe_v11.py`. Raw timeline: `trace_v04.log`.

There are FOUR independent causes. Cause 1 hides the others: it explains all "no marker" lines
(v04..v12). Once it is fixed, v07, v10, v11 and v12 still fail for causes 2 to 5 (v04, v05, v06,
v08, v09 pass; proven with `prove_fix.py`).

## Cause 1 (all scenarios): the harness clears the marker before the assertions run

The page code is right: the marker IS drawn. `trace_v04.log`:

    120ms previewRevealLine received      (hostMessages delayMs 50, sent at page load)
    121ms marker added
    859ms focusin INPUT                   (find bar of check_find_bar)
    1274ms marker REMOVED                 stack: lineMarker.clear <- runtime.ts:123 postMessage wrapper

`run_scenario` (test/visual/capture.py) first runs the pre-scroll checks (`check_preview_toolbar` ->
`check_find_bar`, test/visual/capture_find_checks.py:15-70), which press Ctrl+F, type "the", open the
replace row and click "Replace all" (line 61). That posts `previewFindReplace`, which is in
`SOURCE_EDIT_TYPES` (src/page/features/lineMarker.ts:35), so `runtime.ts:123`
(`if (postsASourceEdit(message)) rt.lineMarker?.clear()`) removes the marker by design (spec 4.7:
an edit removes it). Then `apply_scroll(top)` and the assertions run on a page without marker.
Other `hostMessages` scenarios (`sourceScroll`, threads) survive the checks; this one does not
because it is the only message that a harness check cancels. `v09` has the same cause in another
form (delayMs 2500, then the fold click and the checks run after it).

The scenario's `delayMs` cannot fix it (the checks last 1 to 6 s and click, type and post edits).

### Fix 1 (test harness)

1. `test/visual/capture_final_checks.py`, `check_page_actions` (the loop at line 613): add a branch
   before the `press` branch:

   ```python
   if "hostMessage" in action:
       page.evaluate("""(data) => { const root = document.documentElement; window.dispatchEvent(new MessageEvent("message", { data: { ...data,
         documentId: root.getAttribute("data-sphinx-preview-document-id"),
         revision: Number(root.getAttribute("data-sphinx-preview-document-version")),
         requestId: Number(root.getAttribute("data-sphinx-preview-request-id")) } })); }""", action["hostMessage"])
       page.wait_for_timeout(action.get("waitMs", 300))
       continue
   ```
   (same context attributes the harness already uses for `previewEditCommand`,
   renderFixtures.ts:266-271.) It runs after `apply_scroll` and after every pre-check, before
   `check_content_assertions`.
2. `test/visual/scenarios.ts`: extend the `PageAction` type with
   `{ hostMessage: Record<string, unknown>; waitMs?: number }` (look at the type next to line 106).
3. `test/visual/lineMarkerScenarios.ts`: replace `render: { hostMessages: [...] }` by a page action.
   `reveal(line)` becomes `({ pageActions: [{ hostMessage: { type: "previewRevealLine", line } }] })`.
   v09: `pageActions: [{ click: "h2:has-text('Folded section') [data-okf-fold-toggle]", waitMs: 300 }, { hostMessage: { type: "previewRevealLine", line: 54 } }]`
   and drop its `render` line (the fold click must come first: a pointer press clears the marker).
   (Update the doc comment of `check_page_actions` and the header of lineMarkerScenarios.ts.)

Proof: `prove_fix.py` dispatches the message at that point (monkeypatching `check_page_actions`,
blocking the early message): v04, v05, v06, v08, v09 PASS.

## Cause 2 (v07): the assertion is wrong, the product is right

After fix 1, v07 fails "the marker sits on the top of the wrapped paragraph". The spec (03-change-spec
section 6.3 step 3) says a paragraph gets the measured top of the exact wrapped source line
(`measureLineTops`), and `lineMarker.ts` does that. Measured (`probe_v07.py`): paragraph top 101,
text "The third source line" top 147, marker top 146.97 (on line 5, correct).

Fix 2: `test/visual/lineMarkerScenarios.ts`, `SOFT_WRAP_ASSERTIONS`: replace `blockTopAssertion(...)`
by an assertion that the marker top is within 3 px of the top of the third source line, e.g.
`expr` using a Range on the text node that contains `The third source line` (first character's
`getBoundingClientRect().top`, as in `probe_v07.py`), and require the marker NOT to be at the paragraph top
(`Math.abs(marker.top - p.top) > 10`). Fix the v07 description ("marks the line", not "the top of the block")
and the comment above `SOFT_WRAP_ASSERTIONS` ("the renderer maps the block" is true, but the marker
uses the line tops). `blockTopAssertion` stays for the table.

## Cause 3 (v10): the fixture dropdown renders as an empty `<details></details>`

`:::{dropdown}` is not a directive of this renderer: the rendered page has `<details></details>` (no
body, no mapping), so there is nothing to open and the marker falls back to the previous H2.
A dropdown here is an admonition with the class (see fixture 38-myst-gallery lines 10-14, and
`paletteActions.ts` `dropdown`).

Fix 3: `test/visual/fixtures/91-line-marker.md`, replace lines 58-60 by

    :::{admonition} Closed by default
    :class: dropdown

    The searched line is inside this dropdown, which starts closed.
    :::

(the searched line is now 61) and in `lineMarkerScenarios.ts` v10: `reveal(61)`. Mechanism proven on the
gallery page (`probe_rest.py`, "gallery dropdown"): `previewRevealLine` on line 13 of a
`:class: dropdown` admonition gives `details[open]` = 1 and one marker. Re-run v10 after the fixture edit
(the other scenarios use lines before 58, unaffected; v09 uses line 54 - keep it).
The fixture header comment/description in lineMarkerScenarios.ts that quotes line numbers needs a check too.

## Cause 4 (v11): real product defect, the arrow touches the list item handle in edit mode

Measured (`probe_rest.py`, 900 px, edit mode on, line 47): arrow l=40..49, list item handle
(`.okf-list-item-handle`) l=47..68: 2 px overlap. In `src/core/preview/styles/lineMarkerStyles.ts` the
edit-mode rule is `inset-inline-start: max(1px, calc(var(--sphinx-preview-content-gutter, 16px) - 13px - 1.5em))`.
At 900 px the gutter is 72px, so inset = 38px (+2px marker border); the handle starts 4px before the text and is
1.5em wide, so it starts at 72 - 25 = 47 and the arrow (11 px with its border) must end before it.

Fix 4 (product): in that rule subtract 6px more:
`inset-inline-start: max(1px, calc(var(--sphinx-preview-content-gutter, 16px) - 13px - 1.5em - 6px));`
(update the comment above it). Proven with injected CSS: arrow l=34..43, no overlap (`probe_rest.py`). v06 (table
row handle) still passes as the arrow only moves 6px further left. Note for the Driver: in a narrow pane (gutter 16px)
the `max(1px, ...)` clamp still puts the arrow at 1px, over a handle that sits at negative x; that case has no
scenario, so a note in the requirement or a follow-up is enough.

## Cause 5 (v12): assertion too strict for forced colours

Chromium with `forced_colors: active` computes the band's `background-color` as `rgba(255, 255, 255, 0)`
(transparent but not black), and the arrow border as `rgb(55, 0, 110)` (a system colour). Measured with
`forced_colors="active"` (`probe_rest.py`): bg `rgba(255, 255, 255, 0)`, border `rgb(55, 0, 110)`.

Fix 5: `test/visual/lineMarkerScenarios.ts`, `HIGH_CONTRAST_ASSERTIONS`: replace
`marker.backgroundColor === 'rgba(0, 0, 0, 0)'` by a zero-alpha test, e.g.
`/, 0\)$/.test(marker.backgroundColor) || marker.backgroundColor === 'transparent'`. (In the harness
`forcedColors: true` is applied by capture.py:318 as `forced_colors="active"` on the context, as in my probe.)

## Order and check

Apply fixes 1-5, then run the whole group locally:

    uv run --no-sync --group docs python test/visual/capture.py --group lifecycle-sync --workers 1

(`npm run visual:render` first; fixture edit in fix 3 needs the render). The "unintended identical PNGs"
lines of the campaign (v04/v07, v05/v08/v10) disappear once the markers are drawn at different places;
if one pair remains, give the scenarios a different line. Fixes 1-3 and 5 touch only tests; fix 4 touches
`src/core/preview/styles/lineMarkerStyles.ts` (SwRS-MDOKFSTUDIO-LIFE-178/180 stay valid).

Optional product note (not needed for CI): `previewFindReplace` with `dryRun: true` is a read-only count request
but is in `SOURCE_EDIT_TYPES`, so it also clears the marker; `postsASourceEdit` could ignore messages with `dryRun === true`.
In this run the dry run was cancelled before posting; only the real "Replace all" cleared the marker.
