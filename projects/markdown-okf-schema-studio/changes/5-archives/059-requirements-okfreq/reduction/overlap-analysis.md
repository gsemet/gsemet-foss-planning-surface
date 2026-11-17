# Overlap analysis of the okfreq baseline

Read-only audit of worktree `markdown-okf-schema-studio-wt-059-b3`, branch
`changes-requests/059-requirements-batch3`, head `ccdd039`. Inputs: the 2144 requirement files under
`requirements/tiers/`, `okfreq trace requirements --json`, and the code under `src/`.

Active means a lifecycle other than `deprecated`: **1863 SwRS and 228 StRS** (53 deprecated files
are left out). The scripts and their raw output are in `tools/` (raw outputs in the scratch folder
`/private/tmp/claude-502/-Users-az02065-Projects-Nestor-agentic-coding-white-paper/dd375646-4450-4e52-a643-89ff1d9e405a/scratchpad/059-reduction/`):
`parse.py` (requirements to `reqs.json`), `sim.py` (similarity pass, `sim-pairs.tsv`,
`sim-summary.json`), `build_mapping.py` (mapping and counts), `patterns.py`, `markers.py`.

## 1. Headline

The overlap is real, but it is **structural, not textual**. Almost no two SwRS say the same thing
in the same words. What happened is that one behaviour was cut into many SwRS:

- **1841 of 1863 SwRS (98.8 %) have exactly two scenarios.** The guideline asks for "two
  GIVEN-WHEN-THEN scenarios (nominal and boundary/refusal)". In practice that rule cut every
  behaviour with more than two cases into several SwRS, each with the same two-scenario shape.
- **Cross-cutting rules are written once per message, button or handler**. Examples are the
  read-only refusal, the stale-render gate, the open-edit refusal, message shape validation,
  answer correlation, and how view choices are stored and restored.
- **The refusal SwRS repeats the nominal of its sibling.** 84 SwRS have a second scenario named
  "Writable preview", "Trusted", "Valid" and so on, and 70 have a THEN such as "the move is
  planned" or "the dialog opens". That is the nominal case of another SwRS
  (`SwRS-MDOKFSTUDIO-BLOCK-121`, `-BLOCK-181`, `-PALETTE-191`, `-BLOCK-240`).

When every SwRS is mapped to a tile (one observable behaviour with its scenarios), 1863 SwRS fit
in **311 tiles** and 228 StRS fit in **76 use cases**. No behaviour is lost and no code changes.
Decision D1 then kept one SwRS per palette action and per page↔host message type, which gives
**364 tiles**: that is what `mapping.csv` now implements. The analysis below describes the overlap
itself and keeps the 311 figures.
See `mapping.csv`, `tiles.csv` and `mapping-summary.md`.

## 2. Scripted similarity pass (titles and normative sentences)

Method (`sim.py`): TF-IDF over the title and normative sentence of each active SwRS, with stop
words removed and ids stripped. I took the cosine of every pair through an inverted index and left
out terms that occur in more than 150 SwRS. Then I took the connected components at 0.55.

| Cosine band | Pairs in the same scope | Pairs across scopes |
| --- | ---: | ---: |
| ≥ 0.75 | 5 | 6 |
| 0.65 – 0.75 | 41 | 10 |
| 0.55 – 0.65 | 81 | 19 |
| 0.45 – 0.55 | 288 | 90 |

- Only **285 SwRS (15 %)** have a lexical neighbour at or above 0.55. They form 126 small
  components; the largest has 6 members.
- **The text pass alone explains about 160 of the 1552 removals** (285 SwRS in 126 components). The rest comes from the
  structural patterns below. These were found by reading every title in its scope, grouped by
  implementation file and parent StRS, and confirmed on the code.
- Structural signal: the 1863 SwRS sit in only **682 distinct (primary implementation file,
  parent StRS) pairs**, an average of 2.7 SwRS for each behaviour location. The 311-tile proposal
  is then 46 % of that natural clustering.

Near-duplicates across scopes found by the pass. Each one is merged in the mapping:

| Score | Pair | Note |
| --- | --- | --- |
| 0.90 | CORE-061 / MYST-011 | Version admonitions, written twice |
| 0.81 | BLOCK-055 / TABLE-029 | Escape during an IME composition |
| 0.77 | BLOCK-047 / TABLE-019 | Done posts the final save |
| 0.76 | BLOCK-209 / FMEDIT-069 | A refused flush warns that the text was lost |
| 0.76 | CODE-038 / THEME-033 | Link colour for code in White and Cream |
| 0.75 | DIAG-079 / TRUST-077 | PlantUML engine pinned to an exact version |
| 0.72 | CORE-054 / MYST-059 | Toctree glob |
| 0.66 | BLOCK-247 / TRUST-064 | Flush and watch messages addressed by their own id |
| 0.65 | BLOCK-223 / FMEDIT-052 | A save from an older render is answered with an error |
| 0.65 | FMEDIT-059 / GFM-025 | A checkbox is refused while an edit is open |
| 0.59 | TOOLBAR-093 / TRUST-026 | Percent decoding of a path, at most four rounds (same code, see code-simplification.md) |
| 0.57 | LAYOUT-020 / TOOLBAR-135 | Width mode values |
| 0.57 | CORE-035 / LAYOUT-032 | A wide table scrolls in its box |

Top pairs in the same scope show the split-by-scenario pattern. Examples: TABLE-075/124 (0.89),
TABLE-073/074, LAYOUT-007/008 (40 px gap in read mode and in edit mode), THEME-038/039 (Zoom in /
Zoom out), REVIEW-021/022 (click / Enter opens the popover), TOOLBAR-077/078, DIAG-001/023
(Mermaid / PlantUML fences), PALETTE-181/188 and PALETTE-195/271.

## 3. Pattern 1: cross-cutting rules repeated per message or button (144 SwRS, 17 families)

Each family below becomes one SwRS: a rule with a table of the message types or buttons it
covers. Its own-scope members fold in as scenarios, and the members from other scopes are marked
`replace-by-crosscutting`.

| Family (new tile) | Members | Scopes involved | Example ids | Code that implements it |
| --- | ---: | --- | --- | --- |
| Page message validation (`TRUST.page-message-validation`) | 41 | 13 scopes | BLOCK-236…245, REVIEW-069/070/071/178, TOOLBAR-013/058/083/126/135, THEME-013/052, PALETTE-010, CODE-026, GFM-027, FMEDIT-054, DIAG-050, MYST-051, CORE-066 | One table: `PAGE_TO_HOST_VALIDATORS` in `src/core/protocol/pageToHost.ts` |
| Page message gates, render or document (`TRUST.page-message-gates`) | 19 | 9 | BLOCK-248/223/123/183, PALETTE-181/188/195/271, CODE-027, DIAG-051, TOOLBAR-112, FMEDIT-052, MYST-044, REVIEW-182 | One table: `PAGE_MESSAGE_GATES` in `src/session/pageMessages.ts`, plus `currentPreviewDocument` in each handler |
| Read-only refusal of write requests (`TRUST.readonly-request-refusal`) | 15 | 7 | BLOCK-121/181/224/210, REVIEW-132/180/122, PALETTE-187/191/194/200, MYST-042, GFM-026, FMEDIT-051 | `EDIT_REQUEST_TYPES` gate plus 9 copies of `if (preview.readOnly)` in `sourceEdits.ts` and `hostRequests.ts` |
| Host-to-page acceptance (`TRUST.host-message-acceptance`) | 14 | 5 | BLOCK-129/246/247, TOOLBAR-056/089/122, REVIEW-156, LIFE-055 | `src/core/protocol/hostToPage.ts` |
| Read-only: no editing affordance (`TRUST.readonly-no-edit-affordance`) | 11 | 6 | TOOLBAR-002, PALETTE-015, REVIEW-130/131, BLOCK-013, LIFE-155 | Page runtime `editable` flag |
| Read-only keeps viewing (`TRUST.readonly-keeps-viewing`) | 9 | 5 | THEME-015/054, TOOLBAR-016/076/115/116, CODE-025, PALETTE-182 | Gate table (read-only rejects only `EDIT_REQUEST_TYPES`) |
| Answer correlation and no-answer timeout (`TRUST.request-answer-correlation`, new id) | 11 | 3 | PALETTE-172/173/175/177/145/208/216, REVIEW-185/056, DIAG-047/052 | `installHostRequests` (`src/page/modules/hostRequests.ts`) and `postHostResult` |
| One edit at a time (`BLOCK.edit-exclusivity`) | 17 | 5 | BLOCK-041/217/122/182/198/199/200, REVIEW-181/176, MYST-043/050, GFM-025, FMEDIT-002/058/059/072/073 | `preview.edits.active` checks (5 copies in `sourceEdits.ts`) and page `openEdit()` guards |
| Source edit outcome: one undo step, failed apply reported (`BLOCK.source-edit-outcome`) | 12 | 4 | BLOCK-058/059/225/128/188, REVIEW-184/194, GFM-022, FMEDIT-053/055 | `this.apply(...).then(applied ? ok : "VS Code could not apply …")`, 6 copies |
| View choice stored for the workspace (`LIFE.view-choice-store`, new id) | 17 | 5 | THEME-010/011/012/014/046/047, TOOLBAR-010/014/015/035/125/127, PALETTE-008/009, BLOCK-010/011, LAYOUT-021 | `viewState.ts` plus one page module per choice |
| View choice start precedence (`LIFE.view-choice-start`, new id) | 20 | 6 | THEME-004…008/048/049/050/053, TOOLBAR-011/012/036/124/147, PALETTE-012/013, BLOCK-008/009, LAYOUT-038, REVIEW-159 | Same page modules (`getState() ?? initial ?? default`) |
| Palette popover open/close contract (`PALETTE.popover-focus-contract`) | 15 | 2 | PALETTE-031…035/037/062/076/082/100/107/156/169, TABLE-087/127 | `editPalette.ts`, `editPalettePopovers.ts` |
| Palette leave-frame saves once (`PALETTE.popover-leave-saves`) | 9 | 1 | PALETTE-019/020/024/036/063/103/104/105/171 | `editPalette.ts` focus handling |

The 144 `replace-by-crosscutting` SwRS by scope: block-editing 26, toolbar-navigation 26,
palette-slash 22, theme-zoom 19, review-annotations 18, frontmatter-editing 10, myst 5,
diagrams 4, gfm 4, code-blocks 3, layout-width 2, table-editing 2, rendering-core 1,
frontmatter-schema 1, lifecycle-sync 1. Members of a family that live in the family's own scope
are counted as `fold-as-scenario`.

Confirmed on the code. The read-only, open-edit and stale preamble is written again in each
handler of `src/session/features/sourceEdits.ts`: checkbox, label rename, inline thread, block
move, blocks copy, cut and paste. It is also in four handlers of
`src/session/features/hostRequests.ts`. Only the wording changes ("Moving a block needs a trusted
workspace.", "Renaming needs a trusted workspace.", …). The requirements copied that repetition:
one SwRS per handler for each gate.

## 4. Pattern 2: one SwRS per scenario (1372 SwRS fold into a sibling)

`fold-as-scenario` covers 1372 SwRS: 941 in the PR #62 scopes plus the main scopes' superseded
SwRS of the same kind. The classification is a heuristic on the old title:

| Kind of the folded SwRS | Count | Typical example |
| --- | ---: | --- |
| Nominal variant (a second input, button or mode of the same behaviour) | 691 | THEME-039 "Zoom out lowers the zoom by 10 points" folds into THEME-038; LAYOUT-008 (edit mode) into LAYOUT-007 (read mode) |
| Refusal (a refused or ignored input of the same behaviour) | 396 | PALETTE-191 "The document picker is refused in a read-only preview"; TABLE-079 "A table already in the target form is refused" |
| Boundary (a limit, an edge or an empty case) | 285 | REVIEW-006/007/008 (1000 threads, 200 comments, 10 000 characters) fold into one validity SwRS |

Per scope (folded / active): palette-slash 203/272, block-editing 179/241, review-annotations
162/215, lifecycle-sync 121/155, diagrams 93/119, table-editing 93/122, toolbar-navigation 92/146,
myst 70/95, frontmatter-schema 68/89, trust-security 65/85, frontmatter-editing 63/85,
rendering-core 52/67, layout-width 31/42, code-blocks 28/38, gfm 26/38, theme-zoom 26/54.

The biggest single sources:

- **Palette actions written field by field**. Colour picker: 9 SwRS (058–061, 064–068). Link
  panel and link writing: 15 (089–108). Figure form and writing: 15 (153–170). HTML to Markdown:
  12 (217–228).
- **Slash menu**: 28 SwRS (232–268), cut by key, by ranking rule and by alias category. The five
  alias SwRS 263–267 are one data table.
- **Host request handlers**. The image paste refusal alone is 7 SwRS (200, 201, 272, 273, 274 on
  the host, 205, 206 on the page).
- **Comment anchoring**: 24 SwRS (094–117), one per heuristic rule.
- **PlantUML JAR pipeline**: 37 SwRS (084–120), one per error string or limit.

## 5. Pattern 3: near-duplicates across scopes (26 merged, plus 35 lexical pairs)

`merge-into` covers 26 SwRS where the same behaviour is specified in two places. Examples:
TRUST-046/047 (`dir` attribute) into CORE-041 (right-to-left). TABLE-031/032/033 (cell flush) into
the block flush tile. TABLE-101 (CRLF) into the line-endings tile. PALETTE-139 (Column alignment
list) and PALETTE-269 (slash menu in a cell) into the table tiles. LIFE-140/141/142/166
(Description choice storage) into FMSCHEMA-014. TOOLBAR-073/114 (pending saves before history or
link) into the flush tile. THEME-023 and PALETTE-038 (motion) into CORE-050. DIAG-079 into
TRUST-075.

In the main scopes, SwRS that live in the wrong scope are superseded into the scope of their
subject:

- rendering-core: 054/055 (toctree) to myst, 057/058 (list-table) to myst, 059/063 (figure) to
  myst, 060 to myst, 061 to myst, 044/062/056 (raw HTML) to gfm, 035 to layout-width, 048/049
  (glow) to lifecycle-sync, 066 to trust-security.
- myst: 020–023 to rendering-core placeholders.
- diagrams: 019/020 (comments inside diagrams) to review-annotations, 079/080 to
  trust-security.

## 6. Pattern 4: implementation detail that is not observable behaviour

- **13 SwRS are dropped** (`drop-implementation-detail`). They describe caches, frame scheduling
  or internal invariants that a user cannot observe:
  - Caches: DIAG-010 (Mermaid cache of 64), DIAG-040 (built-in result cache of 64), FMSCHEMA-078
    (64 schemas), REVIEW-205 (HEAD cache), MYST-071 (conf.py lookup cache).
  - Scheduling: TOOLBAR-051 (TOC rebuilt once per frame), TOOLBAR-052 (scroll tracking reads no
    geometry), BLOCK-089 (insert points rebuilt, not patched), CORE-027 (engine warmed at
    activation).
  - Internals: MYST-034 (widths through the CSSOM), DIAG-013 (unique element ids), MYST-093
    (directive registry refuses duplicates), TRUST-049 (sanitizer marks its container).
- Their tests stay as plain unit tests. Only the `@tests_req` line goes away.
- **233 SwRS name code identifiers in their normative sentence**: message types such as
  `previewBlockMove`, `data-*` attributes, CSS variables, `px` values. They are kept: an SwRS may
  name the message it answers. In the new tiles that detail moves into the scenarios and the
  verification notes, so the normative sentence states the observable outcome.
- Main-scope "Known issues" mix real defects with documentation and test gaps, for example
  LAYOUT-007 ("CHANGELOG entry 0.2.1 still quotes superseded margins") and DIAG-003
  ("mermaidPreview.ts has no unit test"). That explains why layout-width shows 32 "Known issue"
  sections for 42 SwRS and diagrams shows 52 for 119. The tile model keeps behaviour defects as
  notes and sends documentation and test gaps to the backlog.

## 7. Counts per pattern and scope

The `keep` column counts surviving ids by old scope. 308 survivors and 3 new cross-cutting ids
make 311 tiles. This table is the 311 variant; the counts per scope of the 364 variant that
`mapping.csv` implements are in `mapping-summary.md`.

| Scope | Active SwRS | keep | fold-as-scenario | replace-by-crosscutting | merge-into | drop |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| block-editing | 241 | 34 | 179 | 26 | 1 | 1 |
| code-blocks | 38 | 7 | 28 | 3 | 0 | 0 |
| diagrams | 119 | 18 | 93 | 4 | 1 | 3 |
| frontmatter-editing | 85 | 12 | 63 | 10 | 0 | 0 |
| frontmatter-schema | 89 | 19 | 68 | 1 | 0 | 1 |
| gfm | 38 | 8 | 26 | 4 | 0 | 0 |
| layout-width | 42 | 9 | 31 | 2 | 0 | 0 |
| lifecycle-sync | 155 | 26 | 121 | 1 | 7 | 0 |
| myst | 95 | 17 | 70 | 5 | 0 | 3 |
| palette-slash | 272 | 43 | 203 | 22 | 4 | 0 |
| rendering-core | 67 | 13 | 52 | 1 | 0 | 1 |
| review-annotations | 215 | 34 | 162 | 18 | 0 | 1 |
| table-editing | 122 | 22 | 93 | 2 | 5 | 0 |
| theme-zoom | 54 | 7 | 26 | 19 | 2 | 0 |
| toolbar-navigation | 146 | 23 | 92 | 26 | 3 | 2 |
| trust-security | 85 | 16 | 65 | 0 | 3 | 1 |
| **Total** | **1863** | **308** | **1372** | **144** | **26** | **13** |

In the main scopes, every non-keep row is an `okfreq supersede` (462) or an `okfreq archive` (8
drops) in `mapping.csv`. The reason column keeps the underlying kind.

## 8. StRS overlap

228 StRS become 76 use cases.

- In the PR #62 scopes the StRS were written per feature facet: palette-slash 27, block-editing
  25, lifecycle-sync 22. Example: "A writer colours text and inserts emoji from pickers" and "A
  writer inserts a table of a chosen size from a grid" are one use case, "insert through
  pickers".
- Three read-only StRS outside trust-security (THEME-005, PALETTE-023, REVIEW-011) restate
  TRUST-001/003 and merge there.
- StRS-BLOCK-010 (paste) merges into the palette paste use case.
