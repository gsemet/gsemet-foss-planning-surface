# Tile model for the okfreq requirements

A tile is the new unit of the requirements. At the SwRS level it is one observable behaviour with
all its scenarios. At the StRS level it is one user use case. This document defines both levels,
how cross-cutting rules are written once, and the target count per scope. The complete
assignment of the old ids is in `mapping.csv`. The list of tiles, with the survivor id and a
proposed title for each, is in `tiles.csv`.

## 1. What one SwRS is

One SwRS = **one observable behaviour** of the extension, meaning one thing a user, the page or
VS Code can see happen. That behaviour has one trigger family and one outcome rule. Its scenarios
cover every case of that rule.

| Part | Rule |
| --- | --- |
| Title | The behaviour in one sentence, in the shared vocabulary (palette, insert point, block editor…). No message type, no file name. |
| Normative behavior | One `SHALL` sentence that states the rule, not one case of it. Example: "When the host receives a write request from a read-only preview, it SHALL refuse it with a reason the page shows and change nothing." |
| Scenarios | **Named by kind**: `Scenario (nominal): …`, `Scenario (refusal): …`, `Scenario (boundary): …`. At least one nominal and one refusal or boundary. **At most about 8.** Above that, the tile holds two behaviours and is split. Equivalent cases go in **one scenario with a table** (inputs, outcome) rather than in several scenarios. Examples: the five gates of the page message gate rule, the 12 HTML-to-Markdown element mappings, the alias table of the slash menu. |
| Known issues | A `### Known issues` section with notes (`- Known issue: …`), written as the code behaves (constitution 1). Only real behaviour defects go there. Documentation gaps and missing tests go to the backlog, not into the SwRS. |
| Depends on | A feature tile that relies on a cross-cutting rule lists it in the authored `depends_on` field (base schema; filename-stem link). It says "see SwRS-…" in its body instead of repeating the gate. |
| Verification notes | Method and criteria. One line per test file. Each scenario names the test (or visual scenario) that checks it. |
| Markers | One `@implements_req` for each implementation point (each file that produces the behaviour, at the function, not at the file head). One `@tests_req` for each test file, above the first test of the tile. Every scenario names its test in the verification notes. |

What is **not** a tile:

- An internal mechanism the user cannot observe: a cache size, frame scheduling, "reads no
  geometry", "rebuilt not patched". The test may stay as a plain unit test without a marker.
  13 SwRS are dropped on this ground (`drop-implementation-detail`).
- One input, button, mode or limit of a behaviour that already has a tile. That becomes a
  scenario or a table row.
- The case of a cross-cutting rule for one message type, when that case adds nothing to the rule
  (for example "a stale save is refused" for one request type). That becomes a row of the
  cross-cutting tile.

What **is** always its own tile, even when the code drives it from a table (decision D1):

- Each **palette action** (Bold and Italic share one tile because they share the asterisk
  markers; Strikethrough, Checkbox, Footnote… each have their own).
- Each **page↔host message type**: the accepted shape and what happens to a malformed one. A
  `msg-` tile may cover two types that share one shape (Resolve and Delete of a comment). A type
  that already has a feature SwRS stating its accepted shape needs no separate `msg-` tile.

### Tile body template

```markdown
## <title>

### Normative behavior

When <trigger family>, the extension SHALL <one outcome rule>.

### Scenario (nominal): <name>
- GIVEN … - WHEN … - THEN …

### Scenario (refusal): <name>
- GIVEN … - WHEN … - THEN …

### Scenario (boundary): <name>
| Input | Outcome |
| --- | --- |
| … | … |

### Known issues
- Known issue: <as the code behaves>.

### Verification notes
- Method: <test file> (scenarios nominal, refusal), <visual scenario id> (boundary)
- Criteria: …
```

## 2. Cross-cutting rules are written once

A rule that every message, button or handler applies is one SwRS family. A feature tile lists it
in `depends_on` and repeats none of its scenarios. The proposal has 13 cross-cutting tiles,
placed in the scope that owns their subject:

| Family | Tile key | Scope | Survivor id | What it states once |
| --- | --- | --- | --- | --- |
| Host request gate: envelope | `TRUST.page-message-envelope` | trust-security | TRUST-052 | Every page message has a registered type and a valid envelope (identity fields, size bound) before any handler runs (`PAGE_TO_HOST_VALIDATORS`). The accepted fields of each type are in that type's own `msg-` SwRS, which lists this tile in `depends_on`. |
| Host request gate: freshness | `TRUST.page-message-gates` | trust-security | TRUST-065 | A message passes the gate of its type: `render`, `comment`, `document`, `own-id` or `page-state`. A stale write is answered "out of date" or with a reopen hint. A row per gate. |
| Host request gate: trust | `TRUST.readonly-request-refusal` | trust-security | TRUST-005 | A write request of a read-only preview is refused with a reason before any change. A row per request type with its reason text. |
| Host request gate: answer | `TRUST.request-answer-correlation` | trust-security | **new id** | Each request carries an edit id. It is answered once with `<type>Result` and the same identity, or it ends with a readable error after its timeout. A late answer is dropped. A row per request type with its timeout. |
| Page acceptance | `TRUST.host-message-acceptance` | trust-security | TRUST-059 | The page accepts only registered host messages addressed to its render. Per-type bounds are in each type's `msg-` SwRS or feature SwRS. |
| Read-only affordances | `TRUST.readonly-no-edit-affordance` | trust-security | TRUST-001 | A read-only preview shows no Edit button, palette, reply box or edit target. |
| Read-only viewing | `TRUST.readonly-keeps-viewing` | trust-security | TRUST-006 | Theme, zoom, view preferences, links, discovery, copy and lists still work. |
| One edit at a time | `BLOCK.edit-exclusivity` | block-editing | BLOCK-041 | An open block, cell or field editor blocks other edits, moves, renames, thread changes, checkbox toggles and refreshes. A row per blocked action with its reason. |
| Source edit outcome | `BLOCK.source-edit-outcome` | block-editing | BLOCK-058 | Every host source edit is one undo step and renders once. A failed apply is answered "VS Code could not apply …". |
| View choice store | `LIFE.view-choice-store` | lifecycle-sync | **new id** | A view choice made on the page (edit mode, palette mode, theme, zoom, toolbar, TOC, width, anchor, comments, changes) is posted, validated and stored for the workspace. A failed write is only logged (Known issue). |
| View choice start | `LIFE.view-choice-start` | lifecycle-sync | **new id** | A new page starts each choice from the panel state, the stored value or the default. The precedence and the rounding of each choice are given in a table. |
| Palette popovers | `PALETTE.popover-focus-contract` | palette-slash | PALETTE-031 | Popovers open inside the frame, one at a time. Escape or typing closes only them and gives the focus back. |
| Palette leave saves | `PALETTE.popover-leave-saves` | palette-slash | PALETTE-036 | Leaving the frame from any palette control saves once. A press keeps the text box focus. |

Why trust-security and lifecycle-sync:

- trust-security already owns the StRS "What the preview page asks of the extension is checked
  first", "ignores answers not meant for it" and "never applied to a newer version". The gate
  code (`src/session/pageMessages.ts`, `src/core/protocol/*.ts`) is the security boundary.
- The view choices are a lifecycle concern: workspace state and panel state across reloads.
- Editing exclusivity and the edit outcome stay in block-editing, because the block edit lock is
  the source of the rule.

## 3. What one StRS is

One StRS = **one user use case** that a writer, reader, reviewer or maintainer can do and see in
VS Code. It is broad enough to have 3 to 8 SwRS under it. It names no message, file or pixel
value.

- **About 5 per scope** (2 to 8). A scope with a narrow subject such as code-blocks or gfm needs
  2. An editing scope needs 7 or 8.
- The old facet StRS merge into the use case as constraints. Example: "Using the palette never
  closes or saves the editor by accident" and "The palette and its menus appear softly" become
  the constraints of "The palette stays in reach".
- Read-only use cases exist once, in trust-security (`TRUST.uc-readonly`).
- StRS test markers stay only on the integration, real-input and visual tests
  (`strs_test_coverage_mode: linked-swrs-and-validation-test`), deduplicated: one per StRS per
  file.

## 4. Target count per scope

**Proposed** is what `mapping.csv` implements (decision D1: about 370). The 311 column is the
earlier variant, which folded the message types and palette actions into tables; it is kept for
reference in `tools/tiles_swrs.311.txt`.

| Scope | SwRS now | **Proposed** | 311 variant | StRS now | **Proposed StRS** | Reasoning |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| rendering-core | 67 | 13 | 13 | 5 | 3 | Toctree, tables, figures, raw HTML and glow go to their subject scopes |
| code-blocks | 38 | 8 | 7 | 4 | 2 | Copy button visibility is one tile with 10 scenarios; `msg-previewCopyText` |
| gfm | 38 | 9 | 8 | 4 | 2 | Receives the raw-HTML SwRS from core; `msg-previewCheckboxToggle` |
| myst | 95 | 18 | 17 | 14 | 6 | Receives toctree, table and figure from core; `msg-previewLabelRename` |
| diagrams | 119 | 19 | 18 | 14 | 4 | JAR pipeline as 4 tiles instead of 37; `msg-previewPlantUmlInclude` |
| frontmatter-schema | 89 | 19 | 19 | 18 | 5 | Link resolution: 5 tiles |
| frontmatter-editing | 85 | 13 | 12 | 11 | 3 | Gate and isolation SwRS go to the cross-cutting tiles; `msg-previewFrontmatterSave` |
| layout-width | 42 | 9 | 9 | 9 | 3 | |
| theme-zoom | 54 | 8 | 7 | 13 | 3 | Persistence moves to `LIFE.view-choice-*`; `msg-previewThemeModeChanged` |
| toolbar-navigation | 146 | 30 | 23 | 14 | 6 | 7 `msg-` tiles (5 page-to-host, 2 host-to-page) |
| block-editing | 241 | 45 | 34 | 25 | 8 | 11 `msg-` tiles (10 edit and block messages, the move result) |
| palette-slash | 272 | 59 | 43 | 27 | 7 | One tile per palette action (+15); `msg-previewPaletteModeChanged` |
| table-editing | 122 | 23 | 22 | 15 | 5 | List table and Pipe table actions split |
| review-annotations | 215 | 40 | 34 | 18 | 6 | 6 `msg-` tiles (4 comment messages, show comments, incoming changes) |
| lifecycle-sync | 155 | 29 | 28 | 22 | 7 | Gains the 2 view choice tiles; `msg-previewPendingOverlay` |
| trust-security | 85 | 22 | 17 | 15 | 6 | Envelope and acceptance stay general; 5 `msg-` tiles |
| **Total** | **1863** | **364** | **311** | **228** | **76** | |

### Why 364

- **D1 keeps one SwRS per palette action and per message type.** Each is a thing a reviewer looks
  up by name, and each has its own test rows. The tile model still removes the scenario splits
  (nominal and refusal as two SwRS) and the repeated gate rules.
- **Below about 300 the tiles would start to hold two behaviours.** The current maximum is 9
  scenarios for a feature tile, plus the table-driven cross-cutting tiles. I split 12 tiles that
  had 11 to 14 members to stay under that bound.
- **No merge joins behaviours that are tested separately into one scenario.** Each old SwRS keeps
  its test as a named scenario. A merged tile only reduces the number of marker lines: one per
  tile per file. The test count stays the same.

## 5. Scope merges and splits

**No scope is merged or split.** The 16 scopes are the frozen e2e groups of
`test/shared/e2eGroups.ts` (requirements guideline, "Before editing"). Merging two scopes would
mean merging two e2e groups and moving their visual scenarios.

What does change is **where some SwRS live**: a SwRS moves to the scope of its subject. In the
main scopes the move is a supersede to a survivor in the other scope; in the PR #62 scopes it is
a merge.

| From | SwRS | To | Why |
| --- | --- | --- | --- |
| rendering-core | 054, 055 (toctree glob) | myst `MYST.toctree` | Toctree is a MyST directive; CORE-054 duplicates MYST-059 |
| rendering-core | 057, 058 (list-table) | myst `MYST.table-directives` | Duplicates MYST-063/064 |
| rendering-core | 059, 063 (figure) / 060 / 061 | myst `MYST.figures` / `MYST.reference-roles` / `MYST.admonitions` | CORE-061 duplicates MYST-011 |
| rendering-core | 044, 062, 056 (raw HTML) | gfm `GFM.raw-html`, `GFM.raw-tables` | Duplicate GFM-033 and GFM-029/030 |
| rendering-core | 035 | layout-width `LAYOUT.table-scroll` | Duplicates LAYOUT-032 |
| rendering-core | 048, 049 (glow) | lifecycle-sync `LIFE.outside-change-glow` | Same as LIFE-094/096 |
| myst | 020–023 | rendering-core `CORE.unresolved-placeholders` | Same rule as CORE-022/023/047 |
| diagrams | 019, 020 | review-annotations `REVIEW.highlight`, `REVIEW.comment-button` | Comment behaviour, tested by the comment tests |
| diagrams | 079, 080 | trust-security `TRUST.pinned-dependencies`, `TRUST.package-identity` | Supply chain and package rules |
| trust-security | 046, 047 (`dir`) | rendering-core `CORE.text-direction` | Same as CORE-041 |
| trust-security | 087 | rendering-core `CORE.include-limits` | An include rule |
| lifecycle-sync | 140–142, 166 | frontmatter-schema `FMSCHEMA.description-column` | The Description column choice |
| theme-zoom | 023, palette 038 | rendering-core `CORE.motion` | Reduced motion and soft appearance |
| theme-zoom | 033 | rendering-core `CORE.typography` (with CODE-038) | Code link colour in White and Cream |

## 6. Guideline changes needed

`requirements/guidelines/requirements.guidelines.md`, section "Levels", changes first, in its own
commit (`plan.md`, step 1). The exact replacement text is in `plan.md`. It replaces two rules:

- "two GIVEN-WHEN-THEN scenarios (nominal and boundary/refusal)" becomes "all the scenarios of
  one observable behaviour, named by kind, about 2 to 8".
- "Settings, commands, messages, palette actions, slash entries and toolbar buttons each need
  their SwRS" becomes: one SwRS per palette action and per page↔host message type; settings,
  commands, slash entries and toolbar buttons are scenarios of the feature SwRS they belong to;
  cross-cutting rules are written once and cited with `depends_on`.

It is a guideline, not the constitution, so it changes in PR #62. The maintainer approved the
direction (D1).
