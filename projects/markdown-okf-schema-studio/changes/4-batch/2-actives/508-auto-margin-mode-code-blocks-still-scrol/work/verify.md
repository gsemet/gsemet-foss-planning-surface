# CR-508 verification

Head: 09e8acf1a1581cb3803ad5f99b31a5c650f601cf

Base: 4a47151e8d055b7f096b69b1fca2d9bf9636f863 (origin/main). `<worktree>` is the CR worktree,
`<base>` a detached worktree of the base (removed). Logs are in `work/gates/`.

Verdict: NOT VERIFIED, for the pull request description only (claim 13). Every code, test, host and
evidence claim (1 to 12) is VERIFIED.

Gate pass cited (no long gate in `chantier.yaml`): `work/gates/preflight-final.log`, first line
`09e8acf1a1581cb3803ad5f99b31a5c650f601cf`.

## 1. Pushed head: VERIFIED (09e8acf)

- `git rev-parse HEAD` -> `09e8acf1a1581cb3803ad5f99b31a5c650f601cf`; `git status --porcelain` -> empty
  (also after all runs below).
- `gh pr view 525 --json headRefOid,isDraft,state,mergeable` ->
  `09e8acf1... draft=true OPEN MERGEABLE`. Checks static, static-windows, visual, viewer-graph,
  report, checks: SUCCESS; the others skipped.

## 2. Unit tests of the measure fail before, pass after (Evidence 1): VERIFIED (09e8acf)

Command, in `<worktree>` and in `<base>` with the head's test file, after `npm run compile`:
`node --import ./scripts/register-myst-patches.mjs --test --test-reporter=spec --test-name-pattern="code block|Mermaid figure" out/test/page/runtimePageControls.test.js`

- Head: `tests 7, pass 7, fail 0, skipped 0`.
- Base (`verify-unit-base.log`): `tests 7, pass 4, fail 3`. Failing: "widened by its border too"
  (`'60px' !== '62px'`), "captioned code block breaks out through its inner code" (`null !== ''`),
  "overflows by 1 px still breaks out" (`null !== ''`). Passing on both: fits at a fractional
  width, capped, inside a list item, Mermaid figure.

## 3. Real browser test fails before, passes after (Evidence 2): VERIFIED (09e8acf)

`env STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- npm run test:breakout` at head, on Windows ->
`tests 14, pass 14, fail 0, skipped 0` (6 code block, 8 table). Defaults, Auto:
`plain097 688.0s 686/686; plain100 691.0W 689/689; python097 698.0W 696/696; captioned103 711.0W 709/709; listed100 660.0s 658/689; huge300 1068.0W 1066/2041`.

Base source, head test (`verify-breakout-base.log`): `tests 6, pass 0, fail 6, skipped 0`; e.g.
`a scroll bar stays (2 px): needs 698.0, Auto python097 696.0W 694/696`,
`a block wider than the column is not marked: needs 691.0, Auto plain100 688.0s 686/689`,
`a block wider than the column is not marked: needs 711.0, Auto captioned103 688.0s 686/709`.

CI visual job at the head (`ci-visual-139401739913.log`): checkout `Merge 09e8acf... into
4a47151e...`; `tests 14, pass 14, fail 0, skipped 0`; `ci-visual: passed`. Linux numbers logged:
plain097 694.0W 692/692, plain100 715.0W 713/713, python097 722.0W 720/720, captioned103 736.0W
734/734, listed100 660.0s 658/713, huge300 1068.0W 1066/2113.

## 4. Table breakout unchanged and passing (Evidence 3): VERIFIED (09e8acf)

`git diff --stat 4a47151e...HEAD -- test/page/tableBreakout.test.ts src/core src/page/features/scrollCore.ts skills justfile .github package-lock.json requirements/tiers/strs`
-> empty. Its 8 tests pass in claim 3.

## 5. Overflow of 1 to 3 px, and the 2 px short breakout: VERIFIED (09e8acf)

`probe.js` (`verify-probe-head.log`, `verify-probe-base.log`): one 100-character plain fence, Auto,
column widened one pixel at a time (wrapper width, `pre` client/scroll).

| Column | Overflow | Base 4a47151 | Head 09e8acf |
| --- | --- | --- | --- |
| 687 | 4 px | 689.0 wide, 687/689 (scrolls 2 px) | 691.0 wide, 689/689 |
| 688 | 3 px | 688.0 not wide, 686/689 | 691.0 wide, 689/689 |
| 689 | 2 px | 689.0 not wide, 687/689 | 691.0 wide, 689/689 |
| 690 | 1 px | 690.0 not wide, 688/689 | 691.0 wide, 689/689 |
| 691 | 0 | 691.0 not wide, 689/689 | 691.0 not wide, 689/689 |

## 6. Code inside admonition, quote, tab, card, list is unchanged and scrolls: VERIFIED (09e8acf)

Same probe, containers page, column 688: Margin and Auto, base and head give the same figures, no
block marked wide: admonition 653/689, quote 654/689, tab 656/689, card 656/689, list 658/689.

## 7. Capped at the area left of the table of contents, unchanged: VERIFIED (09e8acf)

"TOC open auto", huge300: base `812.0W 810/2041` (`verify-breakout-base.log`), head
`812.0W 810/2041` (claim 3).

## 8. Margin, Full width, tables, images, diagrams, settings unchanged: VERIFIED (09e8acf)

- Margin: probe figures identical base and head; the two Margin screenshots are byte identical.
- `src/page/modules/widthMode.ts`: `measureWide` returns before any breakout unless `mode === "auto"`
  (`if (mode !== "auto" || !wrappers) return;`), so Full width takes none of the changed measure.
- `codeOf` answers only for a `PRE` or a `FIGURE` with a direct `PRE` child: for tables, images and
  diagrams `codeNeed` is 0 and the 1 px tolerance is kept. Diagram error `pre` elements sit inside
  `details`, not directly in a figure. Mermaid unit test and the table tests pass.
- `git diff 4a47151e...HEAD -- package.json`: only the `test:breakout` script changes.

## 9. Requirements, docs, changelog, static checks (Evidence 4): VERIFIED (09e8acf)

- `okfreq validate requirements --check-links --project-root .` -> exit 0,
  `1226 requirements, 0 errors, 26 warnings` (`verify-okfreq-validate.log`).
- `okfreq update-coverage requirements --check` -> `0 files would change`.
- `just requirements-update` -> exit 0; `git status --porcelain` and `git diff --stat` empty
  (`verify-requirements-update.log`).
- `git diff --stat 4a47151e...HEAD` -> 10 files: CHANGELOG.md, docs/user/wide-tables.md,
  package.json, requirements/tiers/log.md, SwRS-MDOKFSTUDIO-LAYOUT-023.md, layout-width/index.md,
  widthMode.ts, test_workflows.py, codeBlockBreakout.test.ts, runtimePageControls.test.ts.
- LAYOUT-023 stays `proposed`; its implemented and tested file lists match the description's.
- `just check`: from the gate log at this head (claim 11), not rerun by me.

## 10. Screenshots (Evidence 5) and real VS Code preview (Evidence 6): VERIFIED (09e8acf)

Pairs, figures and reproduction: `work/verifier/evidence/before-after.md`. All six images opened:
they show what is claimed, no user name or home path.

- Auto, cream, 1100 px: base fence 742 px `pre` 740/742 (scrolls 2 px), captioned 688 px 686/742;
  head both 744 px, 742/742, centred.
- Margin: identical.
- Real VS Code 1.147.0, planning page copy, Auto: base `box 785.6875, client 784, scroll 785`
  (scroll bar visible); head `box 787.6875, client 786, scroll 786` (none)
  (`verify-e6-base.log`, `verify-e6-head.log`).

Host and default matrix: defaults, dark background off, line numbers off, both off and 125 %
scaling in claim 3; VS Code webview in a real window here. All cells VERIFIED.

How the window was run: the installed VS Code with its own user-data and extensions folders under
the scratch folder, driven over the debugging port, launched when the machine had had no input for
about 88 minutes; both windows exited by themselves after `Browser.close`; no process with those
profile paths remained. `~\.vscode-shared\sharedStorage\state.vscdb` (VS Code's per-user shared
storage) has a modification time inside the run; whether the test window or the owner's open VS Code
wrote it is not established.

## 11. Preflight, Windows static stage (Evidence 7): VERIFIED (09e8acf)

`work/gates/preflight-final.log` (the Driver's run, first line the head SHA): unit `tests 5242,
pass 5221, fail 0, skipped 21`; pytest `205 passed`; sphinx 4 passed; `ci-static: passed`; visual,
viewer-graph, integration, report and gallery skipped on Windows (CI runs visual and viewer-graph:
claim 1).

## 12. Description matches the diff and its figures are right: VERIFIED (09e8acf)

Posted body equals `work/pr-body.md` (only a trailing blank line differs). Summary, Deliverables,
Changes, Blast radius scope and Autonomous decisions match the diff; the unit failure output, the
browser table, the gate counts and the Known gaps bullet match claims 2, 3, 6 and 11. No internal
reference, no image yet, no user name. The unit output block is condensed (names cut, the four
passing tests on one line).

## 13. Description meets the rules: NOT VERIFIED (09e8acf)

- No proof names its SHA: none of the Test plan items, the unit output or the browser table carries
  `09e8acf` (or `4a47151` for the before figures). A search of `work/pr-body.md` for
  `\b[0-9a-f]{7,40}\b|!\[|No visual change` -> 0 matches. The card and chantier's pr-template require it; the project template and
  guideline are silent.
- Impacts holds text only: neither before/after images nor "No visual change", which the project's
  pull request guideline says the Verifier fails. The brief says the images are added after this
  pass; the six files are in `work/verifier/evidence/`.

To close: add the images to Impacts and name the SHAs, then a description-only pass.

## Observation (not a failed claim)

In a widened block the longest line ends flush against the right border (measured at head: text
right edge within 0.41 px of the `pre`'s inner right edge, computed `padding-right` 12.88px;
`verify-edge-head.log`), visible in both after screenshots. Chromium does not count that padding in
the `pre`'s `scrollWidth`, at base as at head (the same 100-character line needs 689 px of
`scrollWidth` in both), and the specification leaves the block's look unchanged. If it is accepted
as a cosmetic defect, it needs a Known gaps bullet.
