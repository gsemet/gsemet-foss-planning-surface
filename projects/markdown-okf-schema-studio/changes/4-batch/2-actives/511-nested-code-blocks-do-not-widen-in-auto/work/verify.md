# CR-511 verification

Head: abfa71e58f2f150d028781beaeecc2bede4c8182

Base: 2fb89df9c1d19c9e882702f7b2f8328ccc105ae8. Second pass, at the same head, on the posted
description alone. Claims 1 to 11 are carried from the first pass
(`work/verifier/verify-first-pass.md`); claims 12 and 13 are judged again at `abfa71e`. No gate,
test or worktree was run in this pass.

**Verdict: VERIFIED**

Paths below are relative to the CR worktree. Logs are in `work/gates/`.

## 1. Scope of the change: VERIFIED

carried from abfa71e: same head; the evidence it rests on did not change.

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

carried from abfa71e: same head; the evidence it rests on did not change.

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

carried from abfa71e: same head; the evidence it rests on did not change.

`uv run --no-sync --group requirements okfreq validate --check-links --project-root .`, exit 0:
"1228 requirements, 0 errors, 26 warnings" (broken cross-link warnings, none on LAYOUT-023).
Log `verifier-okfreq-validate-abfa71e.log`.

## 4. Markers (spec item 2): VERIFIED

carried from abfa71e: same head; the evidence it rests on did not change.

`just check-markers`:
`check-markers: 11 companion file(s), 459 in-force SwRS marked, 12 files on the marker baseline`

## 5. Requirements lint and update (spec item 3): VERIFIED

carried from abfa71e: same head; the evidence it rests on did not change.

`just requirements-lint` exit 0 ("94 StRS checked, all parse"). `just requirements-update` exit 0
("0 indexes updated", "0 requirement OKF projections updated"); `git status --porcelain` empty
after it. `uv run --no-sync --group requirements okfreq trace requirements --json`: scenario
markers of S9 are `test/page/codeBlockBreakout.test.ts:373` and
`test/page/runtimePageControls.test.ts:596` (first per file); S8 keeps both files.
Logs `verifier-requirements-lint-abfa71e.log`, `verifier-requirements-update-abfa71e.log`.

## 6. Tests pass (spec items 4 and 5): VERIFIED

carried from abfa71e: same head; the evidence it rests on did not change.

`fnm exec -- npm.cmd run compile` exit 0, then
`STUDIO_REQUIRE_CHROMIUM=1 fnm exec -- node scripts/node-test.mjs breakout out/test/page/runtimePageControls.test.js out/test/page/codeBlockBreakout.test.js`:
`tests 56, pass 56, fail 0, skipped 0`, with the six "Auto ..." real-browser cells,
"T10b: a code block inside a list item is not measured" and "T10b: a wide block nested in a
container is not measured". Log `verifier-tests-abfa71e.log`.
`git diff 2fb89df..abfa71e -- test/page/codeBlockBreakout.test.ts`: six added
`// @tests_req SwRS-MDOKFSTUDIO-LAYOUT-023#S9` lines, no assertion changed.

## 7. Mutations of the widening rule (spec item 4, description's Test plan): VERIFIED

carried from abfa71e: same head; the evidence it rests on did not change.

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

carried from abfa71e: same head; of the body it quotes, only the parts in claims 12 and 13 changed (diff there).

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

carried from abfa71e: same head; of the body it quotes, only the parts in claims 12 and 13 changed (diff there).

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

carried from abfa71e: same head; of the body it quotes, only the parts in claims 12 and 13 changed (diff there).

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

carried from abfa71e: same head; the evidence it rests on did not change.

First line of `work/gates/preflight-abfa71e.log`:
`CR-511 chantier/batch-09/cr-511-requirements-only-top-level-blocks-widen abfa71e58f2f150d028781beaeecc2bede4c8182`
Same log: unit group `tests 5367, pass 5359, fail 0, skipped 8`; other groups `56/56` and
`116/116`; `ci-static: passed`;
`preflight: visual, viewer-graph, integration, acceptance, report and gallery stages skipped on Windows; CI runs them`;
`result: exit 0`. Run before this verification and judged from the log, as the brief allows.
`chantier handoff CR-511` names no long gate for the project (`none in chantier.yaml`).

## 12. Description, posted body, Known gaps and Deliverables row 1: VERIFIED (judged at abfa71e)

`gh pr view 537 -R gsemet/markdown-okf-schema-studio --json body,headRefOid,baseRefName,title,isDraft,updatedAt`:
head `abfa71e58f2f150d028781beaeecc2bede4c8182`, base the CR-515 branch, draft, updated
`2026-11-26T14:07:23Z`. `diff --strip-trailing-cr -B <posted body> work/pr-body.md`: exit 0.
`diff --strip-trailing-cr work/scratch/pr-537-body-forge.md work/pr-body.md` (the copy taken before
the proofs were rewritten): the only differences are Deliverables row 1, Known gaps bullet 1, the
Test plan proofs and boxes of claim 13, and one trailing blank line. Sections and the table are
well formed.

Known gaps bullet 1, rewritten:

- "only the list-item case of a nested block is checked" in a real browser: carried from abfa71e
  (first pass, claim 12: the only real-browser assertions on a nested block are the list-item blocks
  of `codeBlockBreakout.test.ts`). `grep -nE "tab-set|tab-item|dropdown|\{card\}|admonition|\{note\}|^>|<details"`
  on the width fixtures 29, 34 and 63 of `test/visual/fixtures/`: no match (exit 1).
- "fakes an admonition, a block quote and a card by their element tags": carried from abfa71e (a
  `div` for the admonition and the card, a `blockquote` for the quote,
  `test/page/runtimePageControls.test.ts:608-626`).
- "no test of this rule puts a block in a tab set or a dropdown": the files of `test/` naming a tab
  set or dropdown, searched for `data-sphinx-preview-wide|data-width-mode|widthMode|[Bb]reakout|LAYOUT-023|"auto"`:
  the hits in `runtimePageControls.test.ts` build no tab set or dropdown (its S9 containers are
  those above; its one `details`, line 631, is the source disclosure inside a Mermaid figure in
  `T10b: a Mermaid figure is not a code block`, `sed -n 628,640p`), and the others assert width preferences, handles or the first-element gap, not a
  block widened inside such a container. Agrees with the first pass.
- "the rule does not depend on the kind of container": `sed -n 88,96p src/page/modules/widthMode.ts`:
  `wrapperOf` tests only that the block's parent is the page content, or that an `IMG` is in a `P`
  with no text whose parent is the page content; no container kind is read. Behaviour: claim 9.

Deliverables row 1, "top level not stated in the rule": `git show 2fb89df:requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md`:
the normative text reads "SHALL widen a table, figure, image, code block or Mermaid diagram that is
wider than the text column ...", with no top-level limit.

Bullets 2 and 3: unchanged, carried from abfa71e (first pass, claims 9 and 12).
`grep -niE "STALE|UNVERIFIED" <posted body>`: no match (exit 1). `work/verifier/evidence/before-after.md`:
"Every planned pair is captured." No claim was accepted as failed.

## 13. Description, Test plan proofs and boxes: VERIFIED (judged at abfa71e)

- New or changed tests box: `grep -n AssertionError work/gates/verifier-mutation-{any,paragraph}-abfa71e.log`
  matches both logs; messages `TABLE` and `P` as read in the first pass (claim 7, carried from
  abfa71e). The new test passes on the head: claim 6, carried from abfa71e.
- Requirements box: `work/gates/verifier-requirements-update-abfa71e.log` ("0 files updated"); empty
  `git status --porcelain` after it and the one added scenario: claims 2 and 5, carried from abfa71e.
- Changelog box: claim 1, carried from abfa71e.
- Local gates box: `head -n 1 work/gates/preflight-abfa71e.log`:
  `CR-511 chantier/batch-09/cr-511-requirements-only-top-level-blocks-widen abfa71e58f2f150d028781beaeecc2bede4c8182`;
  lines 5621-5626 `tests 5367`, `pass 5359`, `skipped 8`, line 5624 `fail 0`; line 5892
  `ci-static: passed`; line 5894 `result: exit 0`.
- Review box: `chantier handoff CR-511`, note
  `move 5f7658a..abfa71e (conflict) inspector approved at abfa71e58f2f150d028781beaeecc2bede4c8182`.
- CI box: `gh pr checks 537 -R gsemet/markdown-okf-schema-studio` (run 45828706682): `checks`,
  `report`, `static`, `static-windows`, `viewer-graph`, `visual`, `visual-2` pass; `gallery`,
  `toc-loop`, `pages`, `tag-release`, `acceptance`, `integration`, `release`, `release-check`,
  `stress` skipping. No other check.

## Notes on this run

- `git rev-parse HEAD` in the CR worktree: `abfa71e58f2f150d028781beaeecc2bede4c8182`;
  `git status --short`: empty.
- The notes of the first pass on its own run are kept in `work/verifier/verify-first-pass.md`.

VERIFIED
