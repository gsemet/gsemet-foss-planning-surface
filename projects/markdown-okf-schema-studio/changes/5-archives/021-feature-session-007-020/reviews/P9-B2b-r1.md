Verdict: APPROVE

Reviewer re-derived from `p9-baseline/run-manifest-b2a.json` + `png-sha256-b2a.txt` and the current `out/reports/e2e/screenshots`. No gate re-run; nothing running.

## Verified
- A rows: 104 planned A rows (`old_to_new.json` action A) = `ASSERTION_ONLY_IDS`; in the manifest 103 have no PNG and the 104th (`frontmatter-schema/v02-okf-schema-narrow-hidden-description-dark-460`) is the `okf-schema-narrow` alias-of-screenshot that never had one. 241 scenarios, passed, 0 failures, `duplicateImages` empty, 167 PNG = 137 primary + 30 step.
- Checks: same 241 ids; executed pairs 1308 before and after; per-check interaction counts: 0 differences over all entries. `capture:false` goes through `save_step`'s early return, which still bumps the trace, and the final-frame checks run (trace equal).
- PNG diff vs B2a: 0 added; removed = 103 primaries (all A rows, none else) + 46 steps; 7 changed hashes: orphan box, TOC v22/v23/v24/v27/v28 (30-toc), and `frontmatter-schema/v03-links-loading-dark-900` (known flake). All other 160 kept PNGs byte-identical.
- Kept step lists in `STEPS_BY_ID` match `old_to_new.json` kept/dropped lists for all 29 scenarios (30 kept steps in the manifest). Steps removed from non-A scenarios are exactly the dropped lists.
- Orphan box: `make(1)` is added at the very end of the same `evaluate`, after `after = height()` is read and all return values are computed; assertions run afterwards on the returned numbers only, so it hides nothing. Later checks (final frame, tooltip, page checks) still pass with the box present and trace counts are unchanged.
- `30-toc.md`: used by exactly one scenario template (`scenarios.ts:1776`, the 8 TOC scenarios); no integration test or src file references it. `check_toc_column` code is unchanged; its table loops iterate over all `:scope > table`, so the added top table is checked for overlap and (Auto) centring too: coverage grew, semantics did not change. The heading list/index (`.nth(8)`) is unaffected, no new headings.
- Alias redirect: the 4 old alias ids map to the scenario they mirrored with a stderr note; ok.
- README `--check`: 9 identical, 0 differences; `git status images/` empty; README/CHANGELOG untouched.

## Product-owner view of changed PNGs
- v22 (Margin) vs v23 (Auto): now visibly different (Auto lets the 10-column table extend left of the TOC, Margin clips it at the text column). Good evidence. v24/v27 (Full) and v28 (hidden, 460) show the table clipped with the scroll fade; fine. In v28 the floating toolbar covers the page title (existing behaviour, not B2b).
- Orphan box: poor evidence. The box is only a sliver at the bottom edge (title row top cut at y~790 of 800 px); the old PNG showed empty padding, the new one shows a divider and the clipped "Orphaned comments" title. It proves nothing a reader can see.

## Findings
1. MEDIUM-LOW, `test/visual/capture.py` `check_orphan_box` (the `make(1)` re-add): the capture does not show the box. Fix (B2c or a follow-up, after all asserts): after `make(1)` scroll so the box is fully visible, e.g. `window.scrollTo(0, Math.max(0, document.documentElement.scrollHeight - innerHeight))` is already the position; instead raise the scenario `height` from 400 to ~560 or scroll by the box height, then re-verify the PNG shows the title and the one entry under the last table. Not a check loss, so not blocking.
2. LOW: `v28-toc-hidden-narrow-light-460` and the other TOC baselines are new baselines; confirm in B3 gallery that "toc-hidden-narrow" lock text mentions the table (no README use, fine).
3. INFO: `scenarioIds.ts` has 128 distinct STEPS/A entries parsed by my regex only because of a comment mention; the data is correct, but consider a one-line unit test that `ASSERTION_ONLY_IDS.size === 104` and every `STEPS_BY_ID` key is a scenario id with a `steps` name in the registry (B2c planned).
4. INFO: step sidecars and descriptions still mention dropped step PNGs (already noted for B2c).
