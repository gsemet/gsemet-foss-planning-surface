# Batch 2 hand-off (orchestrator I, 2026-10-24, partial)

Batch 2 is NOT finished. No commits, no PR. Worktree
`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-059`, branch
`changes-requests/059-requirements-batch2` from origin/main; all work uncommitted.

## Done

| Scope | StRS | SwRS |
| --- | --- | --- |
| diagrams | 14 | 111 |
| frontmatter-schema | 18 | 74 |
| frontmatter-editing | 11 | 71 |
| layout-width | 9 | 35 |

- layout-width also covers F-GFM-037 → SwRS-LAYOUT-001 (gfm inventory row points to it); visual
  scenarios gfm/v02..v04 need `@tests_req` for LAYOUT-001 in the marker step (P10.4).
- Removed 17 duplicate FMSCHEMA StRS (019-035) created by the fmedit analyst with the wrong
  script (never committed, no SwRS derived). `<word>` → `{word}` in 6 FMSCHEMA StRS.
- Last full gate before critics: `validate --prose --check-links` 607 requirements, 0 errors,
  0 warnings; `lint --check` and `update-coverage --check` clean.
- 4 critics: `reviews/<scope>-swrs.md`, all REVISE (diagrams 12, frontmatter-schema 25,
  frontmatter-editing 14, layout-width 14 defects: false or overclaimed Known issues, bundled
  SHALLs, wrong StRS wording, some missing SwRS).
- The one revision pass was sent to the original SwRS analysts (resumed in background):
  ad354bed60f788cb0 (diagrams), a0cc38a63528e2a0e (frontmatter-schema), ac8990527d6756f77
  (frontmatter-editing), a992e17f2e4578ae3 (layout-width). Completion not seen.

## Remaining, in order

1. Wait for the 4 revision analysts; re-run `validate --prose --check-links`, `lint --check`,
   `update-coverage requirements` then `--check`.
2. 4 critic re-checks: each appends "Re-check" with `Verdict: APPROVE` or `Verdict: FIX-REQUIRED`;
   on FIX-REQUIRED one more fix.
3. Follow-up (Sonnet analysts):
   - "Known issue" on CODE-026 and CODE-027 (page shows "Copied" though the host refused or
     dropped the copy) → backlog copy-button-false-copied.
   - New SwRS F-MYST-044 (label starting with `_`, `.`, `-`: anchor icon, click swallowed in edit
     mode), Known issue → backlog label-rename-dead-click.
   - New SwRS F-CODE-028 (copy button revealed by pointer only), Known issue → backlog
     copy-button-keyboard.
   - New SwRS F-MYST-018 (`{doc}`, `{numref}`, `{download}` have no preview-side resolution),
     verification pending (P10.5 test gap).
   - gfm checkbox SwRS (F-GFM-027 and neighbours): Known issue for tooltip-only refusal, box left
     busy after a malformed toggle, misleading standalone message → backlog
     P3/checkbox-refusal-feedback (user decision g).
   - Re-read every "skip" entry in the batch-1 inventories (code-blocks, gfm, myst,
     rendering-core) and specify them, except genuine composites and F-CORE-040..046 legacy
     tooling. List what was added.
   - STATE.md: F-CODE-029 (palette language list) goes to palette-slash in a later batch.
4. Commits: one per scope plus the follow-up, explicit paths, `docs:` messages, trailer
   `Assisted-by: Claude:Sonnet-5.5`. Push, ONE PR against main from the template (external-reader
   body, "How it works" with counts table + StRS→SwRS flowchart, "Autonomous decisions", Claude
   Code line). Wait for checks green and mergeable. Never merge.
5. STATE.md: header lines, per-scope cells, journal.

## Known issues found so far

- diagrams: empty Mermaid/PlantUML source skipped silently; wide Mermaid scaled down with no
  minimum and no zoom; Mermaid error has no Problems/status entry and source shows twice;
  renderer `executablePath` fed by no setting; missing Java gives a misleading hint; Graphviz
  never checked; many diagrams start many JVMs; hidden Mermaid under edit redrawn on theme
  change; Windows drive path in a PlantUML include refused as not local; `useJar` setting text
  stale; PlantUML syntax error kept by the page result cache.
- frontmatter-schema: Names/Values vs Name/Value header wording; BOM not stripped; empty
  frontmatter shows "Frontmatter is not a mapping." though StRS-001 says empty is valid; `$ref`
  with JSON-pointer fragment drops the property; missing `$ref` target or second ref to an
  inlined file becomes a ref to the root; `$ref` can read outside the schema folder; YAML schema
  syntax error silent; `anyOf`/`oneOf` merged; `type: object` labelled "(unknown)"; badge does
  nothing when only info rows have issues; editing a schema does not refresh previews; bundle
  root outside the workspace not watched; standalone file in a trusted workspace told it needs a
  trusted workspace; `formatValue` dead code.
- frontmatter-editing: editor in error state blocks other field editors; leaving edit mode
  discards an unsaved value; schema `minimum`/`maximum`/`pattern` not applied; boolean without
  schema edited as text, date-time as plain text; list items saved as strings; enum select saves
  on blur/Enter, not on change; save pin is the whole properties section; adding an existing key
  gets the generic stale-field message; a content patch closes an open field editor and drops its
  text.
- layout-width: at width 0 README says the three modes look the same but they keep different
  gutters; Width button row 3 in code/README but row 2 in a file header and CHANGELOG
  (Unreleased); CHANGELOG quotes old 56/24 px margins; short-identifier cell marks never removed;
  480 px limit only in visual tests; v05/v06 titles say "full" but assert only the 960 px column.

## Open questions

- F-DIAG-014 (click "Diagram source" opens the inline editor) has no code in `src/page`: owned by
  block-editing?
- DIAG analyst's `update-coverage` reported "360 files updated" with no tracked diff seen; not
  checked in depth.
- F-DIAG-017/018 (Mermaid insert) overlap palette-slash; F-DIAG-019/020 (comment quotes in
  diagrams) overlap review-annotations: batch 3/4 analysts cite these SwRS, not restate them.
- Inventory facts found wrong: Auto-width breakout list includes PlantUML; enum select does not
  save at once.

## Next batches

Batch 3: theme-zoom, toolbar-navigation, table-editing, block-editing. Batch 4: palette-slash
(with F-CODE-029), review-annotations, lifecycle-sync, trust-security.

## Process notes

- One scratch directory per parallel analyst (a shared one caused the duplicate-StRS accident),
  inside the session scratchpad, not `/tmp`.

## Update (orchestrator I, later)

- layout-width revision done: all 14 critic defects fixed, 40 SwRS (new LAYOUT-036..040), ids and
  uuids unchanged. `validate --prose --check-links`: 647 requirements, 0 errors, 0 warnings;
  `update-coverage --check`: 0 changes; `lint --check` to re-run once the others are idle.
  Settled: non-interactive first elements are never pushed down (the code never does it).
- Still running at that time: diagrams, frontmatter-schema, frontmatter-editing revisions.
- frontmatter-editing revision done: 14 defects fixed; new FMEDIT-072..079, 082..085 (085 =
  pagehide/hidden-page flush, 084 = 520 px wrap). FMEDIT-080/081 created by mistake and archived
  with `okfreq archive`; still in `derived_by` of StRS-002 and StRS-011: check the validator
  accepts it. The scroll part of F-FMEDIT-065 has no SwRS: layout-width should take it.
- diagrams revision done: 12 defects addressed; DIAG-021 archived (duplicate of LAYOUT-023); new
  DIAG-112..119; DIAG-005 rebuilt with a new uuid (nothing committed). The "Diagram source" click
  half of F-DIAG-014 is a coverage gap in the inventory, no SwRS. Reported gates: 646 requirements,
  0 errors, 0 warnings; lint and update-coverage --check clean.
- Still running: frontmatter-schema revision (a0cc38a63528e2a0e).
- frontmatter-schema revision done (last one): 25 defects addressed; new FMSCHEMA-075..087; 34
  SwRS rewritten (ids/uuids kept); StRS 001, 002, 005-008, 010, 014, 016, 017 reworded. New Known
  issue: an empty YAML schema file makes the analysis throw a TypeError. Open point: the "section
  flag / no custom key" part was dropped from FMSCHEMA-041: check frontmatter-editing covers it.
- All 4 revisions done. Sizes (StRS / SwRS): diagrams 14 / ~118, frontmatter-schema 18 / 87,
  frontmatter-editing 11 / 85, layout-width 9 / 40. Next: gates once, then critic re-checks.
