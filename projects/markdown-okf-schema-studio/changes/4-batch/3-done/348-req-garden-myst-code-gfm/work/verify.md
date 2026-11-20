# Verify CR-348, garden the requirements of myst, code-blocks, gfm

Head: 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa

Base of the diff: 3766a40e (PR 418's head). All claims below are judged at the head above, in the worktree
`markdown-okf-schema-studio.worktrees/batch-06-CR-348` (clean). First Verifier of this CR; nothing carried.
Rules read: `$CHANTIER rules` (project AGENTS.md, constitution, requirements guidelines, PR guidelines).

## Gate

- `just preflight` pass at the head: `work/gates/20261118-200106.log`, first line
  `gate CR-348 branch chantier/batch-06/cr-348-... head 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa`, last line
  `result: pass at 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa`. It holds: unit `tests 4070`, `pass 4055`, `fail 0`,
  `skipped 15`; security `tests 101`, `fail 0`; contracts `tests 0` (no contract file matched); build tests
  `175 passed`; Sphinx contract `4 passed`; `check-markers: ... 403 in-force SwRS marked, 25 files on the marker
  baseline`; `main paths: 92 StRS checked, 578 SwRS citations, all valid`; `ci-static: passed`. Windows static
  stage only (visual, integration, report, gallery skipped on Windows). Claim: VERIFIED.
- CI run 44377876071 (`gh run view`): headSha `2a6f4f10...`, conclusion `success`; jobs stress, static-windows,
  integration, report, checks, static, visual success; gallery, release-check, toc-loop, tag-release, pages,
  release skipped. The visual job log has `passed: myst/v47-maths-offline-light-900`. Claim: VERIFIED.

## Specification claims, run at 2a6f4f10

1. okfreq validate: `okfreq validate --check-links --project-root .` printed
   `1164 requirements, 0 errors, 26 warnings`, exit 0 (the 26 warnings are broken-link notes in PALETTE SwRS the CR
   does not touch). VERIFIED.
2. `just requirements-lint`: ended with `0 indexes would change`, `0 requirement OKF projections would change`,
   `0 files would change`, `main paths: 92 StRS checked, 578 SwRS citations, all valid`. VERIFIED.
3. No marker for the superseded IDs: `grep -rnE "(CODE-005|CODE-026|GFM-027|GFM-039|MYST-051|MYST-101)\b" src test
   sphinx` printed nothing. VERIFIED.
4. Marker baseline has no CODE, GFM or MYST entry: `grep -nE "CODE|GFM|MYST" scripts/marker-baseline.json` printed
   nothing; the diff removes 5 entries (codeBlockStyles.ts, contentBlockStyles.ts, mystRenderer.ts,
   labelRename.test.ts, mystBlocksWindow.ts), adds none. VERIFIED.
5. Supersessions (frontmatter `req_lifecycle: superseded`, `superseded_by`): CODE-005 -> CODE-039, CODE-001;
   CODE-026 -> CODE-019; GFM-027 -> GFM-021; GFM-039 -> GFM-040, GFM-041; MYST-051 -> MYST-045; MYST-101 ->
   MYST-096; StRS MYST-001 -> StRS MYST-015, 016, 017, 018. Nothing deleted: `git diff --name-status` of
   `requirements/` shows 8 `A` and 74 `M`, no `D`. VERIFIED.
6. Added: the 8 `A` files are StRS GFM-005, MYST-015..018 and SwRS GFM-040, GFM-041, MYST-102, as the body lists.
   VERIFIED.
7. Reparenting (`derives_from` read from the files): TRUST-005 has no GFM-003, MYST-009 or CODE-004; TRUST-065 has no
   CODE-004 or MYST-009; CORE-012 = CORE-002, CORE-003; MYST-019 = MYST-009; MYST-097 = StRS CORE-001; GFM-031 =
   GFM-002, MYST-017; BLOCK-041 = BLOCK-003, BLOCK-058 = BLOCK-025 (sibling work). TRUST-006 is superseded and still
   lists CODE-004 (spec asked to remove it; it is out of force, the sibling CR owns it; the Coder noted it). VERIFIED.
8. `depends_on`: CODE-017 = TRUST-005, TRUST-065; CODE-019 = TRUST-005, TRUST-052, TRUST-065; GFM-021 adds TRUST-052;
   GFM-041 = GFM-021, TRUST-005, TRUST-065, BLOCK-041, BLOCK-058; MYST-045 adds TRUST-052, TRUST-090; MYST-036,
   MYST-038 cite MYST-097; MYST-031 cites TRUST-025. GFM-040 (render only) has an empty `depends_on`; the spec
   names "the radio SwRS" for the shared rules, the log and body do not claim otherwise. VERIFIED, with that note.
9. Every StRS in force of the three groups has a `### Use case diagram` and a `@tests_req StRS-...` on a real
   scenario (grep over `test/`): CODE-001 scenarioDefinitions1.ts:704, CODE-004 :445, GFM-002 sD2:787, GFM-003
   checkboxToggle.test.ts:109, GFM-005 radioChoice.test.ts:187, MYST-005 sD1:1371, MYST-006 mathScenarios.ts:22,
   MYST-007, MYST-009 (labelRename.test.ts:35 and realInput/labelRenameAboveTable.ts:43), MYST-012, MYST-015 sD1:213,
   MYST-016 mystBlocksWindow.ts:150, MYST-017 sD2:698, MYST-018 sD2:798. Diagram count 14 of 14. VERIFIED.
   (The generated `requirements-report.md` lists every StRS test as "missing" because no execution evidence is
   attached on the Windows static stage; in-force SwRS of code-blocks, gfm and myst are all `covered`, only the
   superseded ones show missing. Base behaves the same.)
10. src/ is comments only: `git diff -U0 3766a40e..2a6f4f10 -- src` filtered for non-comment lines printed nothing
    (24 files, 30 insertions, 48 deletions). VERIFIED.
11. New tests exist with markers (`git diff -U0` on the test files): CODE-007 box/font (previewStyles.test.ts),
    CODE-019 second click (codeCopy.test.ts), GFM-008 footnote without definition, MYST-019 heading text
    (mystFeatures/mystPaletteRendering), MYST-024 missing KaTeX bundle (mathRenderer.test.ts), MYST-053 ninth grid
    level (gridToctree.test.ts), GFM-021 host refusals (test/session/radioChoice.test.ts: marker gone, open editor,
    apply refused, apply fails), documents.test.ts markers GFM-021/041, visual `mathScenarios.ts` + fixture
    `89-maths-offline.md`. They ran in the gate's unit run (4070, 0 fail) and, for the visual one, in CI. VERIFIED.
12. Approved StRS commits: `git show ed2032d8 --stat` = GFM-002 only (27+, 5-), `approved_at` moved to
    2026-11-18T18:51:15+01:00, rationale now "named, hex, rgb/rgba and hsl/hsla"; `git show 376912c5 --stat` =
    MYST-001 plus MYST-015..018. Matches the body's "Approved requirements changed". VERIFIED.
13. Not tested by design (declared): MYST-019 `{numref}` contradicts the code (log.md says so, no test added); the
    new MYST-006 gallery appearance is not proved because the gallery job was skipped (CI visual passed the scenario).

## PR description (work/pr-body.md, judged against the diff 3766a40e..2a6f4f10)

- The posted PR 419 body is the OLDER version (`gh pr view 419` diff against pr-body.md: its Known gaps say six
  visual scenarios failed locally, and its CI box is unchecked). The local `work/pr-body.md` is the one judged; it
  must be posted before ship.
- Summary, Deliverables, added, superseded, changed lists, New tests, Impacts, Changes: each sentence matched the
  diff (checks 3 to 12 above; `scripts/marker-baseline.json` and `unused-exports-allowlist.json` (clearMathCache)
  edits match; `scenarioIds.ts` lock texts of v35 and v36 and the v47 entry match).
- Numbers: unit 4070 tests, 0 failed; "contract and security 101 tests, 0 failed" (contract matched 0 files, security
  101); build 175; Sphinx 4: all in the gate log. Wording nit only.
- Review box: Driver note `r2 approved at 3766a40e... committed as ed2032d8, 376912c5, 2a6f4f10 (rest)` covers the head.
- Known gaps: MYST-019 numref, CODE-007 geometry, gallery skipped, Windows static only, "one or two edits" notes, CODE-001
  intent: each has its bullet. "Verified at the head" is left unchecked, as it should be.
- Role names: none outside "Internal references". No image attached (no images to look at). No STALE mark.

## Before/after evidence

None captured: the change is requirement text, marker comments and tests; no behaviour or screen changes (the one
new capture is a new scenario, not a changed one, and passed in CI at the head). No detached base worktree was
created, so none to remove.

## Verdict

VERIFIED at 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa (on the condition the Driver posts work/pr-body.md as the PR body).

## Description pass

Head: 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa

Judged the body posted on PR 419 (`gh pr view 419 -R gsemet/markdown-okf-schema-studio --json body,headRefOid`:
headRefOid 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa, isDraft true, base the branch of PR 418). It is the pr-body.md
judged above with one change, the Verified box now checked "at 2a6f4f1". Judged again at 2a6f4f10 against the diff
3766a40e..2a6f4f10 (148 files, 1846 insertions, 624 deletions) and the claims 1 to 13 above:
- Summary, Deliverables, Changes, Impacts match the diff; the older version's stale Known gaps are gone.
- Test plan SHAs are all 2a6f4f1; CI 44377876071 at 2a6f4f1 success (stress re-run, gallery skipped) matches the CI box.
- Review box: Driver note `r2 approved ... committed as ed2032d8, 376912c5, 2a6f4f10 (rest)` covers 2a6f4f1.
- Known gaps: each declared limit (numref, CODE-007 geometry, gallery, Windows static, "one or two edits", CODE-001
  intent) has its bullet. Role names only in "Internal references". No image attached, so no username or home folder.
  No STALE mark. Draft, as expected.
Description: VERIFIED at 2a6f4f10ecff73a407c6eecbb751ada4f41fcafa.
