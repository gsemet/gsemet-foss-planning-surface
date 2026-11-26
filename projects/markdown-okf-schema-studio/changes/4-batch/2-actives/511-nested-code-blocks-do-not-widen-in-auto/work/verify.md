# CR-511 verification

Head: abfa71e58f2f150d028781beaeecc2bede4c8182

Base: 2fb89df9c1d19c9e882702f7b2f8328ccc105ae8. First verification of this CR; every claim below was
judged at `abfa71e` (nothing carried).

**Verdict: NOT VERIFIED**, on one claim of the posted description (claim 12). The specification's
items, both mutations and the gates are VERIFIED. The `STALE` marks of the description are expected
by the brief (rewritten after this verdict) and are not counted as a failure; the facts to replace
them are in claim 13.

Paths below are relative to the CR worktree. Logs are in `work/gates/`.

## 1. Scope of the change: VERIFIED

`git diff --numstat 2fb89df abfa71e`

    5   0   requirements/tiers/log.md
    26  12  requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md
    1   1   requirements/tiers/swrs/layout-width/index.md
    6   0   test/page/codeBlockBreakout.test.ts
    21  1   test/page/runtimePageControls.test.ts

One commit (`abfa71e5 docs: say only top-level blocks widen in the Auto width mode`), clean tree.
`git diff --stat 2fb89df..abfa71e -- requirements/tiers/stakeholder requirements/tiers/strs src/`
prints nothing. `git diff origin/main --stat -- src/` (origin/main `b9a1abd`) prints nothing (spec
item 6).

## 2. Requirement text (spec and plan item 9): VERIFIED

`git diff 2fb89df..abfa71e -- requirements`, and a script comparing `description:` with the
normative paragraph at both SHAs:

- `description:` equals the normative text at base and at head; the head text holds the top-level
  and nested clauses worded as in the specification; `req_lifecycle: proposed`.
- S9 "(refusal): Nested blocks keep their Margin layout" is declared and has its heading; the
  list-item row left S8 and is in S9.
- The nested-blocks known issue is gone, the other two are kept, one known issue on images in a
  top-level paragraph is added.
- `requirements/tiers/log.md` has the entry "Auto width: only top-level blocks widen (CR-511)"
  under `## 2026-11-26`. No stakeholder requirement file changed (claim 1).

## 3. okfreq validate (spec item 1): VERIFIED

`uv run --no-sync --group requirements okfreq validate --check-links --project-root .`, exit 0:
"1228 requirements, 0 errors, 26 warnings" (broken cross-link warnings, none on LAYOUT-023).
Log `verifier-okfreq-validate-abfa71e.log`.

## 4. Markers (spec item 2): VERIFIED

`just check-markers`:
`check-markers: 11 companion file(s), 459 in-force SwRS marked, 12 files on the marker baseline`

## 5. Requirements lint and update (spec item 3): VERIFIED

`just requirements-lint` exit 0 ("94 StRS checked, all parse"). `just requirements-update` exit 0
("0 indexes updated", "0 requirement OKF projections updated"); `git status --porcelain` empty
after it. `uv run --no-sync --group requirements okfreq trace requirements --json`: scenario
markers of S9 are `test/page/codeBlockBreakout.test.ts:373` and
`test/page/runtimePageControls.test.ts:596` (first per file); S8 keeps both files.
Logs `verifier-requirements-lint-abfa71e.log`, `verifier-requirements-update-abfa71e.log`.

## 6. Tests pass (spec items 4 and 5): VERIFIED

`fnm exec -- npm.cmd run compile` exit 0, then
`STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node scripts/node-test.mjs breakout out/test/page/runtimePageControls.test.js out/test/page/codeBlockBreakout.test.js`:
`tests 56, pass 56, fail 0, skipped 0`, with the six "Auto ..." real-browser cells,
"T10b: a code block inside a list item is not measured" and "T10b: a wide block nested in a
container is not measured". Log `verifier-tests-abfa71e.log`.
`git diff 2fb89df..abfa71e -- test/page/codeBlockBreakout.test.ts`: six added
`// @tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S9` lines, no assertion changed.

## 7. Mutations of the widening rule (spec item 4, description's Test plan): VERIFIED

Detached worktree of `abfa71e` under `work/scratch/vwt`, one edit of
`src/page/modules/widthMode.ts` at a time (the harness bundles the source at test time), restored
after each, worktree removed at the end.

a. `if (element.parentElement === content) return element;` changed to
`if (element) return element;`, `node --test --test-name-pattern "T10b: (a wide block nested|a code block inside a list item)" out/test/page/runtimePageControls.test.js`:
exit 1, `fail 2`; "a wide block nested in a container is not measured":
`AssertionError [ERR_ASSERTION]: TABLE` (the list-item test fails too, `AssertionError: PRE`).
Log `verifier-mutation-any-abfa71e.log`.

b. Only `&& parent.parentElement === content` removed, whole file:
exit 1, `tests 50, pass 49, fail 1`; the new test: `AssertionError [ERR_ASSERTION]: P`.
Log `verifier-mutation-paragraph-abfa71e.log`.

## 8. Description, Autonomous decisions: VERIFIED

- Fake image members: with line 618 (`Object.assign(image, ...)`) removed in the throwaway
  worktree and recompiled, mutation a fails with
  `TypeError [Error]: image?.hasAttribute is not a function` instead of the `TABLE` assertion
  (mutation b still fails with `AssertionError: P`). Logs
  `verifier-mutation-any-nomembers-abfa71e.log`,
  `verifier-mutation-paragraph-nomembers-abfa71e.log`.
- No changelog line: no changelog or release note file in claim 1.
- Rule wording unchanged by the known issue: the normative text matches the specification
  (claim 2).

## 9. Description, Summary and the cases of Known gaps 2 and 3: VERIFIED

Throwaway real-browser probe (source kept as `work/verifier/auto-width-probe.ts.txt`; copy it to
`test/page/zzVerifierProbe.test.ts` in a throwaway worktree, compile, run
`node scripts/node-test.mjs breakout out/test/page/zzVerifierProbe.test.js`): rendered page,
shipped stylesheet, column 688 px, pane 1100 px, Margin compared with Auto. 1 pass.
Log `verifier-probe-abfa71e.log`.

- Widened: top-level code block (1068 px), table (1010 px), image alone in a paragraph (1000 px).
- Same as Margin: list item (code, table), admonition (code, table), block quote (image, code),
  card (code, table), tab set (code, image), dropdown (code, table).
- Same as Margin: a linked image alone in a paragraph; an emphasised one; narrow then wide image in
  one paragraph.
- Paragraph widened to 1000 px from its first image: wide then narrow; linked wide then plain
  narrow.

Mermaid and captioned figures were not in the probe; their top-level cases are the existing tests
(claim 6) and `test/page/widthModeScenarios.test.ts` (run in claim 11's gate).

## 10. Description, Deliverables, Changes, Impacts, Blast radius, Requirements and Changelog boxes, Internal references: VERIFIED

`gh pr view 537 -R gsemet/markdown-okf-schema-studio --json headRefOid,baseRefName,isDraft,title,body`:
head `abfa71e58f2f150d028781beaeecc2bede4c8182`, base the CR-515 branch, draft, body the same text
as `work/pr-body.md`; sections and the table are well formed, no image, no username or home folder,
no role name or CR number outside Internal references.

- Changes: the four bullets match the five files of claim 1 and their diffs; the new test holds a
  table, an image in a paragraph and a code block, each in a container
  (`test/page/runtimePageControls.test.ts:608-626`).
- Deliverables: rows match the diff. Minor wording, not failed: row 1 "top level not stated" is
  true of the old normative text only (the old known issue already said "Only top-level blocks");
  the old known issue did not name the dropdown.
- Impacts: no `src/` change (claim 1). Blast radius: `.vscodeignore` excludes `requirements/**`
  and `test/**`, so nothing shipped changes.
- Test plan, Requirements box: claims 1, 2, 5. Changelog box: claim 1.
- Internal references: S9 added, list-item row moved from S8 to S9 (claim 2).

## 11. Gate at the head (spec item 7): VERIFIED

First line of `work/gates/preflight-abfa71e.log`:
`CR-511 chantier/batch-09/cr-511-requirements-only-top-level-blocks-widen abfa71e58f2f150d028781beaeecc2bede4c8182`
Same log: unit group `tests 5367, pass 5359, fail 0, skipped 8`; other groups `56/56` and
`116/116`; `ci-static: passed`;
`preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
`result: exit 0`. Run before this verification and judged from the log, as the brief allows.
`chantier handoff CR-511` names no long gate for the project (`none in chantier.yaml`).

## 12. Description, Known gaps: NOT VERIFIED (first bullet)

Bullet 1: "... The new unit test fakes an admonition, a block quote and a card by their element
tags, and **no test builds a tab set or a dropdown**; the widening rule **looks only at a block's
parent**."

- "no test builds a tab set or a dropdown" is false as written. A search for
  `\{tab-set\}|\{dropdown\}` in `test/**/*.test.ts` gives 26 matches in 10 files (for
  example `test/core/render/cardsTabs.test.ts`, 8). What is true: no test of the Auto width rule
  puts a wide block in a tab set or a dropdown (no width mode term in the tab and card tests;
  `codeBlockBreakout`, `tableBreakout` and `svgBreakout` hold no such container).
- "looks only at a block's parent" is wrong for an image: `wrapperOf`
  (`src/page/modules/widthMode.ts:88-96`) also reads the paragraph's parent and its text. What is
  true: the rule does not look at which kind of container holds a block.
- Rest of the bullet VERIFIED: the only real-browser assertions on a nested block are the
  list-item blocks of `codeBlockBreakout.test.ts` (the admonition case of `tableBreakout.test.ts`
  asserts the top-level table); the new test fakes the admonition and card with a `div` and the
  quote with a `blockquote`.

Suggested replacement: "..., and no test of this rule puts a block in a tab set or a dropdown; the
rule does not depend on the kind of container."

Bullets 2 and 3 VERIFIED: behaviour by claim 9; "no test checks them": the only two-image
paragraph in the width tests (`widthModeScenarios.test.ts:88`) asserts the figure mark in the
default mode, and no width test holds a linked image; the known issue and criteria text by claim 2
(criteria: "a paragraph only when it holds no text and an image is its direct child").

No `UNVERIFIED` claim and no uncaptured evidence pair (`verifier/evidence/before-after.md`).

## 13. Facts for the STALE proofs (to be rewritten, not counted)

- Unit-test mutations: both messages hold at `abfa71e` (claim 7).
- Local gates: claim 11 (5367 unit tests, 5359 pass, 0 fail, 8 skipped).
- Review: `chantier log` / `handoff` note
  `move 5f7658a..abfa71e (conflict) inspector approved at abfa71e58f2f150d028781beaeecc2bede4c8182`
  proves "approved at abfa71e".
- CI: `gh pr checks 537 -R gsemet/markdown-okf-schema-studio` (run 45828706682, attempt 1, head
  `abfa71e`, conclusion success): `checks`, `report`, `static`, `static-windows`, `viewer-graph`,
  `visual` (7m24s), `visual-2` (8m26s) pass; `acceptance`, `gallery`, `integration`, `pages`,
  `release`, `release-check`, `stress`, `tag-release`, `toc-loop` skipped.

## Notes on this run

- Two earlier shell calls and the first mutation call changed folder into the throwaway worktree,
  which is under the CR folder; the startup core forbids that. Nothing was written outside the
  `writes:` folders by them.
- The Edit tool is not available to this session: the throwaway files were mutated with `sed`.
- The throwaway worktree used a junction to the CR worktree's `node_modules`; the junction was
  removed first, then the worktree. The CR worktree is clean at `abfa71e`.
