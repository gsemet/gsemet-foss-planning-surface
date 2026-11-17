Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: SwRS of scope `diagrams` (P10.3, Sonnet critic)

Reviewed: 14 StRS and 111 SwRS in the worktree `markdown-okf-schema-studio-wt-059`, against `src/` and
`test/`, the inventory (`inventory/diagrams.md`, 55 F-DIAG rows) and the defect classes of
`reviews/{code-blocks,gfm,myst}-swrs.md`.

## What was checked

- Mechanical (all 125 files): frontmatter description equals the Normative behavior text (no
  glued/stale split: OK); first `##` heading equals the title (OK); derived_by of every StRS equals the
  derives_from of the SwRS (consistent); every SwRS has at least two scenarios (OK); no placeholders.
- Inventory: all 55 F-DIAG rows carry requirement ids, no SwRS is unreferenced and no cited id is
  missing (OK). Coverage gap: none substantive.
- Source read in full for `plantumlDiagram.ts`, `plantumlPreview.ts`, `plantumlFileRequests.ts`,
  `mermaidPreview.ts`, `mermaidCache.ts`, `mermaidError.ts`, `plantUmlRenderer.ts`,
  `plantUmlIncludes.ts`, `plantUmlLimits.ts`, `plantUmlConfiguration.ts`, `session/features/plantUml.ts`,
  `mystNormalize.ts` (diagram rules), `mystRenderer.ts:resolvePlantUmlFile`, the diagram CSS,
  `widthMode.ts`, `package.json` settings. About 65 of the 111 SwRS (about 58 %) were compared with
  that code, with weight on the Known-issue claims and the boundary scenarios (1 MiB / 5 MiB / 8 MiB,
  8 deep, 64 files, 65th result, 4096 / 4097 characters, exactly-at-limit cases, 10 s, 30 s, order 79/80).
  The boundary scenarios of 038, 050, 059, 061, 062, 063, 066, 097, 098, 099, 100 are true versus the code.
  Known issues verified true: 001, 002, 015, 022, 026, 032, 037, 041, 054, 085, 092, 093, 076.
  Test titles cited in Verification notes exist (a few are quoted loosely, see 12).
- Anchored-to-code: the "Known issue" lines are present for the real oddities (empty diagram blank,
  CSP untested, UX-46 no minimum scale, UX-36 no live preview, plain engine errors cached, drive-letter
  paths refused, Smetana differences, stale useJar text, executablePath fed by no setting, hint
  about jarPath on a missing Java). Nothing is skipped as "looks like a bug".

## Defects (REVISE)

1. StRS-MDOKFSTUDIO-DIAG-010 (rationale) is false versus the code and contradicts SwRS-041: it says
   "failed, unsupported and include-refused results are not kept". `plantumlDiagram.ts:outcome` caches a
   plain engine failure (`cacheable` is false only when an include failed or an included file holds an
   unsupported directive); an up-front unsupported directive never reaches the cache at all. Fix: "include-refused
   results (and results with an unsupported directive in an included file) are not kept; a plain engine
   failure is kept until the source or variant changes (Known issue)". Same slip in SwRS-039: "an earlier
   successful result" must read "an earlier result" (errors are kept too, per 041 scenario 2).
2. SwRS-006 is not true as written: "SHALL draw every Mermaid diagram again" on an observed attribute change, but
   `mermaidCache.plan` returns `keep` when the theme colours are unchanged (the behaviour 009 itself states, and its
   scenario "a theme attribute change that leaves the colours as they were draws nothing"). Fix: "SHALL check
   every Mermaid diagram and draw again each one whose theme colours differ from those it was drawn with,
   keeping the labels"; add the same-colours scenario to 006 or point to 009.
3. SwRS-021 (Auto-width breakout) restates the owned requirement SwRS-LAYOUT-023 ("widen a table, figure,
   image, code block or Mermaid diagram ...", edited element exempt in `widthMode.ts`). It has no
   diagram behaviour of its own, its scenarios have no numbers ("marked wide with a breakout size"), the
   phrase "a Mermaid diagram or a diagram figure" is unclear, and its Known issue says both engines qualify while
   inventory F-DIAG-013 says only Mermaid is in the list (the code supports 021: the selector is
   `table, figure, img, pre, .myst-mermaid-diagram`, so a `.myst-plantuml-figure` qualifies through `figure`).
   Fix: delete 021 (and its derives_from LAYOUT-007 and the StRS-001 derived_by entry) and cite LAYOUT-023
   from the diagram StRS-001 rationale; keep the "PlantUML qualifies via the generic figure selector, not by its own
   entry" fact as a Known issue in LAYOUT-023 or in the diagrams rationale. If kept, give it a measured scenario and say
   "see LAYOUT-023".
4. Wrong derives_from: SwRS-019 and 020 (comment quote / compose skip) and 022 (diagram under edit hidden) apply
   to Mermaid and PlantUML figures but derive only from the Mermaid StRS (001 and 003). 022 sits under
   "Mermaid diagrams stay in place while typing", which is not its subject (an open block editor). PlantUML
   readers have no parent for them. Fix: add StRS-006 to derives_from of 019, 020, 022 (and to its derived_by), or
   create one StRS "Diagrams are left alone by page-wide tools" and move 019, 020, 022 there; remove 022 from
   StRS-003.
5. Bundled SHALLs (one SwRS = one bounded SHALL), real second behaviours:
   a. SwRS-032: three SHALLs (message with directive and line; engine not run and host not asked; state
      unavailable). Split "shows the message and sets unavailable" from "does not run the engine and does not ask
      the host".
   b. SwRS-048: three triggers (host refusal, 10 s silence, malformed answer) plus "the diagram SHALL show it".
      Split the host refusal (reason passed once) from the page-side timeout and malformed-answer reasons; the
      showing is already 037/041.
   c. SwRS-049: "ignore a malformed request" and "send from as null for a non-string from" are two behaviours.
   d. SwRS-030: variant decision (dark below luminance 0.18, transparent is light) and redraw on a variant switch.
   e. SwRS-014: keep the late drawing in the cache / show only the current key / no late error. Split the late
      picture from the late error.
   f. SwRS-105: order matching with the source line and isolation of a failing diagram.
   g. SwRS-101: group kill with fallback, and the "canceled" message on the diagram.
   h. SwRS-036 (refuse the include AND show the unavailable message) and SwRS-081 (contain AND centre) are
      minor two-part SHALLs; split or reduce to the observable outcome.
6. SwRS-005 is vague and under-tested by its scenarios: the SHALL names five variables as "node, text, border, line and
   background" colours, but the code maps them to primaryColor, primaryTextColor / lineColor, primaryBorderColor,
   secondaryColor (`--studio-textBlockQuote-background`) and tertiaryColor (`--studio-editor-background`), and
   `--studio-editor-background` is not the diagram background (that is `transparent`). Scenarios check only the node fill, text and
   line. Fix: restate the mapping with the real roles and add a scenario for the border colour and the font.
7. Redundant warning statements: SwRS-107 (every JAR failure also a `plantuml-render` warning with the document
   path) repeats "and a warning" already stated in 089, 091, 092, 094, 095, 096. Fix: keep the warning in one
   owner (107, with scenarios per failure kind) and remove it from the message requirements, or drop 107 and add the
   `plantuml-render` code to one of them.
8. Misused "Known issue" lines that describe correct behaviour: SwRS-068 ("With useJar the JAR receives the file
   text (unit test)") and SwRS-091 ("The built-in engine is never swapped in behind the user's back"). Move them
   to the body or scenarios. Conversely a real missing Known issue: SwRS-111 (and 084-086) never say that the
   JAR/PATH pipeline draws the same SVG in light and dark (no dark variant is asked), while the built-in engine does
   (030). 111's title and scenarios ("both themes") promise more than the code does; reword to what is verified
   (a loaded picture, no error, source kept) and add that Known issue.
9. SwRS-108 omits conditions of the real code path: the content patch is sent only if incremental updates are on,
   the page is ready for the stage, `diagnosticsFitPatch(statusLines)` holds and `planContentPatch` returns a plan; otherwise
   `setPanelHtml`. Scenario "Ready page" is false when the diagnostics do not fit a patch. Add the two conditions to
   the SHALL and a "diagnostics too long" scenario (or a Known issue).
10. SwRS-072 wording: "in place of each remaining {uml} diagram" but `resolvePlantUmlFile` also applies to a
    body-less `{plantuml}` file; say "{uml} or body-less {plantuml}". StRS-011 rationale lists "an include cycle"
    among the unreadable-file cases with "one warning in the status line": a cycle is an engine-side include message
    (SwRS-064, no host warning); remove it from that bullet.
11. Open question, F-DIAG-014 second half ("in edit mode a click on the Diagram source disclosure opens the inline
    editor") has no SwRS and no diagram code that implements it (no `details`/summary handling found in
    `src/page/features/blockEditor.ts`). Confirm it belongs to block-editing (the inventory says so) and drop it from
    the diagrams inventory note, or add a Known issue to 022 pointing at the owner.
12. Verification notes quote test titles loosely for 058, 059, 060 (the real test is "a missing file is refused and
    watched, a too large file and a symlink escape are refused" in `plantUmlIncludes.test.ts`) and 011 cites
    "RI-T34" (it is in `test/integration/realInput.test.ts`). Quote the real titles/paths so the later
    `tested_in_files` mapping finds them.

## Overlaps checked

- CODE-022 (copy button): correctly not re-specified; 019/020 cover only comments. OK.
- palette-slash / review-annotations: 017/018 (Mermaid insertion, GFM-only) and 019/020 (comment skip) are
  diagram-specific and the generic palette / comment rules are not duplicated here. Batch 2 scopes for those
  are not in the worktree yet; the palette-slash and review-annotations analysts must cite 017/018/019/020, not
  restate them.
- layout-width: see defect 3.
- Over-splitting: acceptable except 107 (defect 7). 087/088 and 076-078 are small but each bounded.

Verdict: REVISE

## Re-check

Re-read against the worktree (14 StRS, 119 SwRS files of which DIAG-021 is deprecated) and the code
(`mermaidPreview.ts`, `plantumlDiagram.ts`, `plantUmlRenderer.ts`, `session/features/plantUml.ts`,
`widthMode.ts`). Mechanical: every description equals the Normative text (the 5 raw differences are
YAML escaping only); every title equals the first `##` heading; derived_by of every StRS matches the
derives_from of the SwRS (DIAG-021 aside); no dangling id.

Defects 1-12: all fixed and true to the code. 1 (StRS-010 and 039/041 now say plain engine failures
are kept; `cacheable` matches), 2 (006 plus a same-colours scenario, matches `plan` keep), 3 (021
deprecated, LAYOUT-023 cited with the generic `figure` selector Known issue, true), 4 (019/020/022
derive from StRS-001 and StRS-006 on both sides), 5 (splits 112-119 exist; the remaining two-SHALL
descriptions are positive/negative pairs, acceptable), 6 (005 matches the seven theme variables at
lines 67-73), 7 (warning owned by 107; 089-096 no longer repeat it), 8 (111/084 Known issue added),
9 (108 matches the `incrementalUpdates` / `readyRequestId` / `diagnosticsFitPatch` / `planContentPatch`
path), 10, 11 (gap noted in the inventory), 12 (real titles and paths).

Remaining defects:

1. StRS-MDOKFSTUDIO-DIAG-001 (`derived_by` line 24) and StRS-MDOKFSTUDIO-LAYOUT-007 (`derived_by`
   line 18) still list the deprecated SwRS-MDOKFSTUDIO-DIAG-021, and `swrs/diagrams/index.md` line 26
   still lists it as a live entry. Fix: remove DIAG-021 from both `derived_by` lists (a deprecated
   requirement is not a child) and regenerate the index; if okfreq keeps archived ids by design,
   state it in STATE.md instead.
2. SwRS-MDOKFSTUDIO-DIAG-086 bundles three behaviours in one SHALL (write the text to standard input;
   run in the workspace folder; take the first svg start to the last svg end tag), with scenarios for
   only the third and for split characters. Fix: split the SVG extraction (with the log-lines and
   split-character scenarios) from "stdin plus cwd = workspace folder" (scenarios: stdin holds the
   text, cwd is the workspace root).
3. Inventory row F-DIAG-013 (main repo `inventory/diagrams.md` line 50) still says only Mermaid is in
   the breakout list and "inconsistency"; the code selector includes `figure`, so a PlantUML figure
   qualifies. Fix: align the note with SwRS-LAYOUT-023 Known issue (cosmetic, outside the requirement
   files).

Verdict: FIX-REQUIRED

## Re-check 2

Checked against the worktree `markdown-okf-schema-studio-wt-059` (656 requirements, `okfreq validate --prose --check-links`: 0 errors, 0 warnings) and the code (`src/core/render/plantUmlRenderer.ts`, `test/core/render/plantUmlRenderer.test.ts`).

Re-check 1 defects:

1. DIAG-021 in `derived_by` of StRS-DIAG-001 (line 24) and StRS-LAYOUT-007 (line 18) and as a live line in `swrs/diagrams/index.md` (line 26): NOT fixed, and the fallback (a statement in STATE.md) is not there either. Cause: `okfreq archive` sets `lifecycle: deprecated` and `derives_from: []` but does not prune the parent's `derived_by` nor the index. Fix: add one line to STATE.md (and to the `requirements/tiers/log.md` entry) saying that deprecated requirements stay listed in `derived_by` and in the generated index by okfreq design (applies to DIAG-021, FMEDIT-080, FMEDIT-081). No requirement edit needed.
2. DIAG-086 split: fixed. DIAG-086 is now only the SVG extraction (first svg start to last svg end tag; log-lines and split-character scenarios; matches `svgOutput` lines 180-186 and the tests "renders PlantUML through the configured external JAR" and "decodes a multibyte character split across stdout chunks"). The new DIAG-120 holds "text on stdin" and "cwd = workspace root" with one scenario each; the cited test asserts `child.input === source` and `cwd: workspace.root`. One SHALL each.
3. Inventory F-DIAG-013 and UC-DIAG-1: fixed (the note says both diagram kinds qualify through the generic `figure` selector and points to the LAYOUT-023 Known issue).

New defect found while re-reading:

4. SwRS-MDOKFSTUDIO-DIAG-004, Known issue ("... (UX-46, not fixed, absent from docs/known-limitations.md)"): names an internal finding id, which the new guideline rule (no backlog reference in requirement text) rules out. Fix: delete the parenthesis, keep "There is no minimum scale and no zoom: a very wide diagram is scaled until its labels become small."

Verdict: FIX-REQUIRED

Fixed after Re-check 2 (one pass): DIAG-004 parenthesis removed, inventory row F-FMSCHEMA-023 mapped to FMEDIT-086/035, deprecated-in-index noted in STATE.md. Verdict after fix: APPROVE
