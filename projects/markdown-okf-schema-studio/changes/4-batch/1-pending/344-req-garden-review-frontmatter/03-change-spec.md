---
type: cr-change-spec
description: Garden the okfreq requirements of the review-annotations, frontmatter-editing and frontmatter-schema scopes (StRS text, parents, SwRS merges, markers, validation tests, use-case diagrams), with no product behaviour change.
---

# Change Specification: garden the requirements of review-annotations, frontmatter-editing, frontmatter-schema

## Goal

A human reviewer understands each use case of these three scopes by reading its StRS, and each
SwRS is one observable behaviour, traced by `@implements_req` on the code that does it and
`@tests_req` on each test that checks its scenarios. The source of every finding and mapping below
is the audit `requirements-gardening/evidence/audit-review-frontmatter.md` (finding names X1-X5 are
its own); the systemic direction is `audit-synthesis.md`.

This CR changes requirement files, markers, tests and comment placement in `src/`. It changes no
product behaviour: no rendered output, message, setting or command changes. A `src/` edit is only a
marker move or a refactor that keeps the output byte-identical (section 6).

Repository: `C:/Users/gaeta/Projets/markdown-okf-schema-studio` (paths below are relative to it).
Rules that rank above this specification and that the Driver reads first: `.agents/constitution.md`
(section 1), `requirements/guidelines/requirements.guidelines.md`,
`requirements/guidelines/project.guidelines.md` ("Main paths of a StRS", "During a change",
"Approved requirements"). okfreq runs as `uv run --no-sync --group requirements okfreq`.

## Dependencies

- `req-use-case-diagrams` lands first: it adds to `requirements/guidelines/project.guidelines.md` the
  rule for an authored `### Use case diagram` section (one Mermaid fence: sequence, actors or state,
  placed before `### Main paths`). Section 9 follows that rule as landed; where the landed text
  differs from this specification, the landed rule wins.
- `req-marker-gate` lands first: `just check` then fails on an in-force non-exempt SwRS without
  `@implements_req`, on a marker comment that names more than 3 IDs, and on a companion file that
  does not name a scenario for each ID, except for the offenders in its baseline (a ratchet that
  only shrinks). This CR removes from that baseline every entry it fixes (section 7) and adds none.
- Sibling restructure CRs (`req-garden-block-table`, `req-garden-toolbar-lifecycle`,
  `req-garden-core-diagrams-trust`, `req-garden-palette-theme-layout`, `req-garden-myst-code-gfm`)
  edit some of the same files (`test/integration/realInput/markers.ts`,
  `test/integration/previewEditing.test.ts`, `test/page/modules/editActions.test.ts`,
  `test/core/protocol/pageStateMessages.test.ts`, and the `derives_from` of shared SwRS). This CR
  touches in those files only the IDs of its three scopes and the entries naming its StRS; it leaves
  the other IDs where they are. When a sibling already moved or removed one of them, there is
  nothing to do for it.

## Decisions carried from `02-answers.md`

- **Published requirements are never deleted.** Every merge, fold or split retires the old
  requirement with `okfreq supersede OLD NEW [NEW...] --path requirements --yes` (or
  `okfreq archive` when nothing replaces it). No `git rm`, no `okfreq retire` (all in-force SwRS of
  these scopes are `proposed`, none is a draft).
- **The split into this CR and its siblings is approved;** this CR follows the audit report of its
  group. Where the report offers two ways, this specification names the one taken and why.
- **Decisions the owner keeps**, which the Driver brings back and never takes alone:
  1. the re-approval of any approved StRS whose text changes (section 1);
  2. a change of lifecycle `draft` -> `proposed` (none is planned: these scopes have no draft;
     requirements created by this CR are created `proposed`, as the project guideline requires,
     which is not such a change);
  3. a merge or split of this specification that the Driver doubts once it reads the code and the
     tests (it stops that item and asks; the rest goes on).
- **No spec critic** for this CR.

## 1. The approved StRS: one owner package, before any of their changes

REVIEW-001, REVIEW-003, REVIEW-012 and REVIEW-015 are `approved` (owner `gaetan@xeberon.net`).
Before it changes any of these four files, the Driver writes the exact proposed text of each (a
diff of the authored sections) and brings it to the owner through its Foreman, in one package. It
applies only what the owner agrees to; the agreement and its date are recorded in this CR (a dated
section appended to `02-answers.md`, as the Foreman records owner answers), then the Driver sets
`approved_by: gaetan@xeberon.net` and `approved_at` to the time of the agreement with its UTC
offset. The PR body lists them under "Approved requirements changed" and requests the owner's
review.

| StRS | Authored change proposed | Why | If the owner refuses |
| --- | --- | --- | --- |
| REVIEW-001 | Add the `### Use case diagram` (section 9). | Every StRS gets a diagram. | No diagram on REVIEW-001. |
| REVIEW-003 | Diagram; in Main paths, the step backed by SwRS-REVIEW-081 cites SwRS-REVIEW-044 instead (081 is folded into 044, section 4). | A Main path may cite only an active SwRS. | Diagram dropped; REVIEW-081 is not folded into 044 (both stay as they are). |
| REVIEW-012 | Normative text: "toggle a TODO comment around the current or selected lines **from the edition palette or the slash menu** in a block editor" instead of "from the keyboard"; rationale line "The TODO shortcut action is also offered by the edition palette and the slash menu" becomes "The TODO action has no shortcut; Ctrl+/ toggles a plain comment"; Main paths reshaped as below; diagram. | The text contradicts SwRS-REVIEW-160 and the code (`The TODO action has no shortcut`, PALETTE-266). The requirement states what the code does; adding a shortcut would be a product change, out of scope. | REVIEW-012 unchanged; LIFE-170 keeps REVIEW-012 in its `derives_from`; the contradiction is reported in the PR and in `log.md` as an open finding. |
| REVIEW-015 | Diagram; in Path 2, the `Option SwRS-MDOKFSTUDIO-BLOCK-058 (nominal): the edit is one undo step` bullet is removed (BLOCK-058 is cited by `depends_on`, section 3); the undo-step outcome stays visible through SwRS-REVIEW-192, which depends on BLOCK-058. | Shared rule cited, not derived. | Diagram dropped; BLOCK-058 keeps REVIEW-015 in its `derives_from`. |

REVIEW-012's Main paths, proposed (the project guideline allows at most two paths, so the audit's
"Path 3" is not added; the Comments button becomes an option of Path 1):

- Path 1 "Open a comment chip": as today, plus at state "A chip stands in the text" an
  `Option SwRS-MDOKFSTUDIO-REVIEW-152 (nominal): the reader presses the Comments button and the gray
  and thread chips are hidden while the TODO chips stay`.
- Path 2 "Mark a line as TODO": 1. "A block editor is open on some lines" - SwRS-REVIEW-160: the
  writer runs the TODO action from the edition palette or the slash menu and the touched lines are
  wrapped in a TODO comment, one undo step; Option SwRS-REVIEW-160 (boundary): the same action on
  wrapped lines unwraps them; Option SwRS-REVIEW-160 (refusal): a line holding `-->` is left
  unchanged. 2. "The lines are marked as TODO". (Today's Path 2 step backed by LIFE-170 goes, as
  LIFE-170 no longer derives from REVIEW-012.)

Changes to the generated `derived_by` and Links block of these four StRS (an SwRS folded or
reparented) are listed in the package for information; they are not authored text.

Everything else in this specification proceeds while the owner's answer is pending; the items of the
"If the owner refuses" column wait for it.

## 2. StRS text of the proposed StRS

No approval is needed (lifecycle `proposed`). For each, keep the title, normative statement and user
need unless named here; cut the `### Rationale and constraints` to the constraints a stakeholder
cares about: remove the bullets that restate an SwRS or repeat an SwRS "Known issue" (X5). The
known issues stay in their SwRS.

| StRS | Change |
| --- | --- |
| FMEDIT-001 | Rationale from 15 bullets to the stakeholder constraints (the 5 known-issue bullets and the control-kind bullets go). Main paths: drop the steps backed by BLOCK-041 if section 3 removes FMEDIT-001 from BLOCK-041's parents (it does); keep BLOCK-228 (not a shared rule). |
| FMEDIT-005 | No text change besides the diagram. |
| FMEDIT-008 | Keep it for preservation, refusal and flush. Remove `#### Path 2: Remove a field` (it repeats FMEDIT-005); its normative text no longer lists field removal if it does today. Main paths: replace the BLOCK-058 bullet by the SwRS of this scope that carries the one-undo-step scenario (FMEDIT-043), or drop it. Rationale trimmed. |
| FMSCHEMA-001 | Rationale from 13 bullets to the stakeholder constraints; the fence and invalid-YAML text that duplicates FMSCHEMA-002 is kept here (it becomes the only home). Main paths: at the first state of Path 1, add `Option SwRS-MDOKFSTUDIO-FMSCHEMA-001 (refusal): YAML that does not parse shows one error row "Invalid frontmatter YAML" with the parser message, and the body still renders` and `Option SwRS-MDOKFSTUDIO-FMSCHEMA-001 (refusal): an opening fence without a closing fence` (the content of FMSCHEMA-002's only path; the audit's "Path 3" would break the two-path rule). Normative text gains "and when the frontmatter is invalid, explains why while the body still renders". |
| FMSCHEMA-002 | Superseded: `okfreq supersede StRS-MDOKFSTUDIO-FMSCHEMA-002 StRS-MDOKFSTUDIO-FMSCHEMA-001`. Before it, remove `StRS-MDOKFSTUDIO-FMSCHEMA-002` from SwRS-FMSCHEMA-001's `derives_from`. No diagram. |
| FMSCHEMA-006 | Rationale from 16 bullets to the stakeholder constraints (5 known issues go). |
| FMSCHEMA-010 | No text change besides the diagram. |
| FMSCHEMA-014 | Rationale from about 20 bullets to the user need, the link roots and the refusal rule. Main paths: the step backed by FMSCHEMA-060 cites FMSCHEMA-050 (060 folded, section 4). |
| REVIEW-008 | Main paths: the steps backed by REVIEW-100 and REVIEW-101 cite REVIEW-100 (merged, section 4). |
| REVIEW-017 | Normative text and user need speak of the change bars only (as today); Main paths: the step or option backed by REVIEW-208 cites REVIEW-207 (folded). Its derived side-by-side SwRS move to the new StRS below. |

New StRS, created with `okfreq new` (StRS tier, scope `review-annotations`, `--lifecycle proposed`),
title "A writer compares each changed block with its last-commit version side by side",
`--description` a `SHALL` statement of the side-by-side diff (Side-by-side button, a card per
changed block with the HEAD version left and the current block right, added and removed words
marked, the button disabled in edit mode), `--user-need` in the writer's words. It gets a Main path
(Side-by-side on, cards with word marks, Side-by-side off restores the blocks) backed by REVIEW-008
and REVIEW-009 (and REVIEW-006 for the host posting the baseline), and a diagram. REVIEW-006, 008
and 009 change their `derives_from` from StRS-REVIEW-017 to the new StRS.

## 3. Reparenting: shared rules cited with `depends_on`, not derived

Shared rules are cited by `depends_on` in the SwRS that rely on them; they are not derived by the
StRS of these scopes. In each file below, remove from `derives_from` only the entries naming a StRS
of review-annotations, frontmatter-editing or frontmatter-schema; each keeps parents of its own
scope. Then check that each SwRS of these three scopes that relies on the rule cites it in
`depends_on` (most already do: see the in-force list in the audit); add the citation where missing.

| Shared SwRS | Entries removed from its `derives_from` |
| --- | --- |
| BLOCK-041 (one edit at a time) | FMEDIT-001, FMEDIT-008, REVIEW-008 |
| BLOCK-058 (one undo step, one render) | FMEDIT-001, FMEDIT-008, REVIEW-015 (waits for the owner, section 1) |
| BLOCK-109 (insert-point arrows; marginal to FMEDIT-008) | FMEDIT-008; add `relates_to: StRS-MDOKFSTUDIO-FMEDIT-008` only if the refusal scenario about the properties bar is kept in BLOCK-109 |
| TRUST-001 (editable whatever the trust) | REVIEW-001 |
| TRUST-005 (host handles write requests) | FMEDIT-008 |
| TRUST-065 (page message gate) | FMEDIT-008, REVIEW-015 |
| LIFE-170 (new page starts from stored choices) | REVIEW-012 (waits for the owner, section 1) |

Kept as they are (behaviours of these use cases, not shared rules): BLOCK-193, BLOCK-228.
TOOLBAR-113 (a link message shape, X4) is left to `req-garden-toolbar-lifecycle`, which folds the
TOOLBAR message SwRS; this CR does not edit it.

Within these scopes:

- SwRS-FMSCHEMA-084: remove `StRS-MDOKFSTUDIO-FMEDIT-005` from `derives_from` (the required-field
  refusal is FMEDIT-029's); add `relates_to: StRS-MDOKFSTUDIO-FMEDIT-005`. It keeps FMSCHEMA-010.
- SwRS-FMSCHEMA-091 (exported properties table opens on a click, derived only by TOOLBAR-014): add
  `relates_to: StRS-MDOKFSTUDIO-FMSCHEMA-001`; its scope stays (open question 1).
- A Main path that cited a removed derivation drops that bullet or step (the guideline requires the
  StRS in the cited SwRS's `derives_from`); section 1 and 2 name the cases.

## 4. SwRS merges and folds

Rule used for every row (requirements guideline, "preserve the identity when refining the same
contract"): the survivor keeps its ID and absorbs the scenarios, verification notes and
`depends_on` of the absorbed SwRS; its title and description widen to cover them; then
`okfreq supersede <absorbed> <survivor...> --path requirements --yes`. Every `@implements_req` and
`@tests_req` naming an absorbed ID is renamed to its survivor in the same commit (respecting the
3-ID cap; a duplicate marker at the same place is dropped). After the CR, no marker in `src/` or
`test/` names a superseded or deprecated ID of these scopes.

Message-validation SwRS (X4): the synthesis direction is taken (fold into the behaviour they guard,
citing the shared rule) rather than the audit's alternative of one "comment messages are validated"
SwRS, because that alternative would keep an SwRS no user can observe. The malformed-message case
becomes a refusal scenario of the survivor ("a malformed message is dropped, see
SwRS-MDOKFSTUDIO-TRUST-052" or TRUST-059 for host-to-page), and the survivor's `depends_on` cites
TRUST-052 / TRUST-059 / TRUST-065 as the absorbed one did.

| Absorbed | Survivor(s) | What moves |
| --- | --- | --- |
| REVIEW-069 (create message) | REVIEW-054 | Refusal scenarios of a malformed create message; markers `src/core/protocol/pageToHost.ts:316`, `src/session/features/comments.ts:543`, `test/core/protocol/pageToHost.test.ts:240`, `test/core/comments/commentEditing.test.ts:61`, `test/integration/commentWrite.test.ts:44`. |
| REVIEW-070 (reply message) | REVIEW-074 | Refusal scenarios; markers `pageToHost.ts:320`, `comments.ts:556`, `pageToHost.test.ts:241`. |
| REVIEW-071 (resolve and delete messages) | REVIEW-074 | Refusal scenarios; markers `pageToHost.ts:323`, `comments.ts:569`, `pageToHost.test.ts:264`. |
| REVIEW-081 (reply box of the popover) | REVIEW-044 | 044 becomes "a comment editor sends its text on Save or Cmd+Enter and keeps it until the host accepts", with a scenario table per editor (comment box, reply box). Waits for the owner (REVIEW-003 Main paths, section 1). |
| REVIEW-101 (orphaned, keeps its lines) | REVIEW-100 | 100 becomes "a thread follows its quote, or is orphaned keeping its lines"; marker `src/core/comments/anchoring.ts:444` and `test/core/comments/anchoring.test.ts:74`. REVIEW-107 (fuzzy) and REVIEW-219 (placed again) stay. |
| REVIEW-216 (quote over a wrapped line) | REVIEW-017 (SwRS) | A boundary scenario of the highlight; markers `src/page/modules/commentThreadData.ts:70`, `test/page/modules/commentThreadsLongDocument.test.ts:175,187,203,221`. |
| REVIEW-156 (show-comments message of another render) | REVIEW-152 | Refusal scenario citing TRUST-059; markers `src/page/features/hostHandlers.ts:47`, `test/page/runtimePageControls.test.ts:533`. |
| REVIEW-178 (inline thread change message) | REVIEW-186, REVIEW-192 | Refusal scenarios in both (reply and delete); markers `pageToHost.ts:268`, `pageToHost.test.ts:303`. |
| REVIEW-007 (side-by-side messages validated and gated) | REVIEW-006, REVIEW-009 | Page-to-host part to 006, host-to-page part to 009; markers `src/core/protocol/pageToHost.ts:258` (006), `src/core/protocol/hostToPage.ts:400` (009), `test/core/protocol/pageToHost.test.ts:378` (006), `test/core/protocol/hostToPage.test.ts:137` (009). |
| REVIEW-005 (word diff) | REVIEW-009 | The word marks become scenarios of the card; markers `src/core/mapping/wordDiff.ts:53,125`, `test/core/mapping/wordDiff.test.ts` (all). |
| REVIEW-010 (line hunks) | REVIEW-009 | Hunks with both sides become scenarios of the card; markers `src/core/mapping/lineDiff.ts:119,183,215,227`, `test/core/mapping/lineHunks.test.ts` (all). |
| REVIEW-200 (added and modified lines) | REVIEW-195 | Boundary scenarios of the posted lines; markers `lineDiff.ts:73`, `test/core/mapping/lineDiff.test.ts:6`. |
| REVIEW-203 (HEAD text from the Git extension, small files) | REVIEW-195 | Boundary scenarios (no Git, file over 1 MiB); markers `src/host-vscode/headBaseline.ts:43`, `test/host-vscode/headBaseline.test.ts:36`. |
| REVIEW-208 (malformed incoming-change ranges) | REVIEW-207 | Refusal scenario citing TRUST-059; markers `src/page/modules/incomingChanges.ts:73`, `test/page/modules/incomingChanges.test.ts:102`. |
| FMEDIT-054 (save message names editor and field) | FMEDIT-016 | Refusal scenario citing TRUST-052; marker `src/core/protocol/pageToHost.ts:232`; the test marker in the 9-ID block of `test/core/protocol/pageStateMessages.test.ts:220-228` goes onto a focused test (section 7). FMEDIT-016 gains FMEDIT-054's parent TRUST-009 only if TRUST-009 is a use case this behaviour serves; else it is not carried (FMEDIT-016 keeps FMEDIT-001 and FMEDIT-008). |
| FMSCHEMA-060 (bundleRoot, projectRoot, allowOutsideWorkspaceLinks) | FMSCHEMA-050 | 050 becomes "links resolve from the configured or default root and stay inside"; the settings are its scenarios; markers `src/core/configuration/settingsRegistry.ts:284`, `src/core/frontmatter/fileLinks.ts:105`, `test/core/configuration/frontmatterConfiguration.test.ts:10`, `test/core/frontmatter/fileLinks.test.ts:151`, `test/core/frontmatter/okfFrontmatter.test.ts:41`. |

SwRS text fixes (no merge):

- REVIEW-081 is folded; if the owner refuses the fold, its normative text is widened to its title
  and scenarios (sending and keeping the reply).
- REVIEW-086: normative text covers Delete (with its confirmation) as its title and scenarios do.
- REVIEW-094 / REVIEW-119: move the scenarios "Typing writes nothing" and "Change of a clean
  document" from REVIEW-119 to REVIEW-094; move the marker `src/session/features/comments.ts:272`
  (inside `shiftForEdits`) from REVIEW-119 to REVIEW-094; REVIEW-119 keeps the save-time write
  (`persistAnchors`, marker at line 294). Their test markers follow the scenarios.
- REVIEW-133: add the scenario "an HTML comment inside a tab item keeps its own source lines" (the
  behaviour `unmapPlainBlocks` in `src/core/render/mystGridToctree.ts:462` gives today) with a unit
  test; if the Driver finds the code does not do it, remove the REVIEW-133 marker there instead.
  Same check for REVIEW-167 at line 463.

## 5. What is not merged

REVIEW-002 (contrast on every theme) stays under REVIEW-003 (low finding; moving it under a theme
StRS belongs to the theme scope). REVIEW-044 and the FMEDIT-019 bundle of 10 scenarios stay one
SwRS each (the audit finds them one behaviour). FMEDIT-003 stays one SwRS.

## 6. Implementation markers (X3 and missing parts)

Each marker goes to the branch, helper or declaration that does the behaviour; a marker comment
names at most 3 IDs. Markers never go inside a generated HTML or CSS string. Where a marker block
sits on a whole function or constant, the Driver moves each ID onto the branch that produces it; when
the behaviour lives in one string constant, the constant is split into named constants joined in
the same order (output byte-identical, checked by the existing tests and a snapshot assertion of
the joined string if none exists), each with its marker.

| Site | Today | After |
| --- | --- | --- |
| `src/core/frontmatter/propertiesTable.ts:191-198`, `renderPropertiesTable` | 8 IDs (FMSCHEMA-084/004/005/006/014/039, TRUST-001, REVIEW-215) | FMSCHEMA-004 on the "table off" branch; 005 on the no-schema key listing; 006 on the value formatting; 014 on the Description toggle markup; 039 on the badge markup; 084 on the issue rows; REVIEW-215 on the frontmatter change-bar markup; TRUST-001 kept in its own comment on the code it names. |
| `src/core/frontmatter/okfFrontmatter.ts:323-326`, `analyzeFrontmatterCore` | FMSCHEMA-001/084/039/005 | 001 on fence detection and YAML parse; 084 and 039 on the validation call and issue count; 005 on the no-schema path. |
| `src/core/edits/frontmatterEdit.ts:79-82`, `planFrontmatterSave` | FMEDIT-016/024/037/067 | 016 on the YAML/type/schema checks; 024 on the rename branch; 037 on the add branch; 067 on the flush branch. |
| `src/core/frontmatter/frontmatterValidate.ts:319-321`, `fieldsFromYaml` | FMSCHEMA-029/084/039 | 029 on schema-ordered field listing with types; 084 on attaching violations to fields; 039 on the count that feeds the badge (or removed here if the badge marker in `propertiesTable.ts` covers it). |
| `src/core/preview/styles/commentStyles.ts:3-7`, `COMMENT_CSS` | REVIEW-028/143/152/002 (+1) | Split into named constants (orphan box: 028; chip box: 143; hidden review marks: 152; theme contrast: 002), each marked. |
| `src/core/render/mystGridToctree.ts:462-463` | REVIEW-133/167 | Kept only with the scenario of section 4. |
| `src/node-services/schemaFiles.ts:27` | FMSCHEMA-019 on `MAX_LISTED_DIRECTORIES` | On the listing cache function. |
| `src/page/features/frontmatterValueEditor.ts` | FMEDIT-003 only at the enum branch (line 87) | Also on the boolean toggle, the native number/date inputs and Set to null. |
| `src/core/comments/commentModel.ts:263,274` (`setResolved`, `deleteThread`), `src/session/features/comments.ts:570,580` (`handleResolve`, `handleDelete`) | no REVIEW-074 | `@implements_req SwRS-MDOKFSTUDIO-REVIEW-074` on each. |

## 7. Test markers (X1, X2, misattributed)

Every test cited in an SwRS's verification notes, and every test that checks a scenario of an SwRS,
carries `@tests_req` of that SwRS. File-level marker blocks are dissolved onto the tests. The
verification notes name the tests after the change.

File-level blocks of these scopes (the IDs of other scopes in the same block stay for their CR):

- `test/core/frontmatter/okfFrontmatter.test.ts:29-43` (15 IDs): move each onto its tests; for
  example FMSCHEMA-019 at about line 226 and 257 (nearest folder, case-insensitive, no lookup in
  Restricted Mode), FMSCHEMA-023 at 277 and 970 (JSON pointer fragment, extension fallback),
  FMSCHEMA-029 at 309 (schema order) and 85 (`fieldIconType`), FMSCHEMA-039 at 943, FMEDIT-037 at
  1339-1428, FMSCHEMA-055 at 830 and 877 (ambiguous or unknown stem, unreadable candidate), FMEDIT-004
  on the multi-line literal block and trailing line breaks tests. The block is removed.
- `test/integration/previewEditing.test.ts:242-258` (17 IDs on `run()`): the steps of `run()` that
  check FMEDIT-016, FMSCHEMA-014/084/063/067/073 and the StRS FMSCHEMA-001/014 are extracted into
  named step functions (assertions unchanged), each with at most 3 markers. The other IDs stay for
  their CR, in blocks of at most 3 or on extracted steps.
- `test/page/modules/editActions.test.ts` header (around line 44): REVIEW-160 goes onto the
  `todoCases` loop (line 181), `the todo toggle is its own inverse` (187), the registry test (195)
  and `a line containing --> is never wrapped in a TODO comment`; also on T21 in
  `test/page/runtimeEditPalette.test.ts`.
- `test/integration/realInput/markers.ts`: lines 29-32 (FMEDIT-019, FMSCHEMA-039/043/063) and 51-55
  (StRS FMEDIT-001/005/008, FMSCHEMA-001/014) are removed; the markers go onto the scenario
  functions that check them (section 8 for the StRS).
- `test/core/protocol/pageStateMessages.test.ts:220-228`: FMEDIT-054 is folded (section 4); its
  check goes onto a focused test of FMEDIT-016's malformed-save-message refusal (in
  `test/core/protocol/pageToHost.test.ts` if one exists, else a new one there).

Single focused marker for several scenarios (X1): mark each test of the listed lines.

| SwRS | Tests to mark |
| --- | --- |
| REVIEW-004 | `test/core/comments/commentModel.test.ts:55,74` |
| REVIEW-074 (with 070, 071 folded) | `test/core/comments/commentEditing.test.ts:185,198` |
| REVIEW-100 (with 101), REVIEW-107 | the tests of `test/core/comments/anchoring.test.ts:81-261` by the scenario each checks |
| REVIEW-094 | `anchoring.test.ts:38,55,61,166` |
| REVIEW-017 | `test/page/modules/commentThreads.test.ts:155-216,292` |
| REVIEW-028 | `commentThreads.test.ts:791-812` |
| REVIEW-044 (with 081) | `test/page/modules/commentCompose.test.ts:262,283,296`; `commentThreads.test.ts:375,394` |
| REVIEW-086 | `commentThreads.test.ts:510-581,744` |
| REVIEW-049 | `commentCompose.test.ts:80,108` |
| REVIEW-171 | the 7 tests its verification notes name in `test/page/modules/inlineThread.test.ts` |
| REVIEW-125 | a focused test of the nominal rename and move (`test/session/reviewReqComments.requirements.test.ts`), added if none exists |
| REVIEW-133 | the tests of `test/core/comments/commentMarkers.test.ts` that check its scenarios |
| REVIEW-195 (with 200, 203) | the other tests of `lineDiff.test.ts` and `headBaseline.test.ts` |
| FMEDIT-016 | `test/core/edits/frontmatterEdit.test.ts:93` (schema error, only errors of the edited field) |
| FMEDIT-028 | the tests of Custom-key refusals and the narrow-preview boundary (`test/page/runtimeFrontmatterEditor.test.ts`, `runtimeFrontmatterFields.test.ts`), added if none exists |
| FMSCHEMA-006 | unit tests for the list limit and lean frame if they exist; the contrast and narrow scenarios stay visual (`test/visual/scenarioDefinitions1.ts:770`), which carries the marker |
| FMSCHEMA-043 | the "page not ready" refusal test in `runtimeFrontmatterFields.test.ts` |
| FMSCHEMA-046 | the tests of its 7 scenarios in `test/core/frontmatter/fileLinks.test.ts` |
| FMSCHEMA-073 | `test/session/diagReq.links.requirements.test.ts:12` (unusable link warning) |
| FMSCHEMA-084 | the tests of 2020-12 keywords, closed schema and the strict setting |

Misattributed:

- `test/core/frontmatter/propertiesTable.test.ts:368` ("error rows carry the red underline class")
  is marked FMSCHEMA-029 and checks FMSCHEMA-084: re-mark it FMSCHEMA-084. FMSCHEMA-029 goes onto
  `okfFrontmatter.test.ts:309`, `propertiesTable.test.ts:695` (type icons) and
  `okfFrontmatter.test.ts:85`.
- `test/core/edits/frontmatterEdit.test.ts:56` (FMEDIT-067) mostly checks the stale and bad-key
  refusals: add FMEDIT-016 and FMEDIT-024 to it; keep FMEDIT-067 there for its last assertion; add a
  focused unit test of the flush (written as typed, unchecked) marked FMEDIT-067.

The `req-marker-gate` baseline: remove each entry these moves fix. After this CR, the baseline holds
no file or ID of these three scopes.

## 8. StRS validation tests

Each in-force StRS carries `@tests_req StRS-...` on a real scenario that walks its use case (never
the companion list).

| StRS | Validation scenario |
| --- | --- |
| FMEDIT-001 | `scenarioEnterCommitsTextField` (`test/integration/realInput/textEditing.ts:189`), `scenarioListEditorClickAndKeys` (`test/integration/realInput/frontmatterFields.ts:142`) |
| FMEDIT-005 | `scenarioCustomKeyAndOpenNewField`, `scenarioAddFieldPositionAndEscape` (`frontmatterFields.ts:415,501`) |
| FMEDIT-008 | `scenarioFrontmatterValueMinimalPatch`, `scenarioFrontmatterStructuralMinimalPatch` (`textEditing.ts:83,124`), `scenarioFlushFrontmatterKeptAsTyped` (`test/integration/realInput/flushBeforeNavigate.ts:389`) |
| FMSCHEMA-001 | the extracted step of `test/integration/previewEditing.test.ts` that renders the table; plus a unit scenario of the invalid-YAML refusal (`test/core/frontmatter/diagReq.frontmatter.requirements.test.ts:50`) for the former FMSCHEMA-002 path |
| FMSCHEMA-006 | new extracted step in `previewEditing.test.ts` on its `_schema/finding.schema.yaml` bundle: the typed document finds the schema (schema fields render), and a schema problem is reported |
| FMSCHEMA-010 | same bundle: fields in schema order with their types, the `legacy_summary` violation shown on its field, the badge count; the badge press scrolls to the first issue |
| FMSCHEMA-014 | the extracted link step of `previewEditing.test.ts` |
| REVIEW-001, 003, 008, 015 | unchanged (`reviewComments.test.ts:38`, `commentAnchors.test.ts:32-33`, `commentWrite.test.ts:37-38`, `inlineThread.test.ts:100`) |
| REVIEW-012 | `scenarioHiddenReviewMarks` (`test/integration/realInput/blockKeys.ts:140`) and a new real-window scenario `scenarioTodoToggle`: open a block editor, run the TODO action from the edition palette, the source holds the TODO comment around the lines, one undo restores them |
| REVIEW-017 | `scenarioIncomingChanges` (`test/integration/realWindowGaps.ts:187`, unchanged) |
| new side-by-side StRS | `sideBySideSteps` (`realWindowGaps.ts:~108`) |

New scenarios are registered in the suite that already runs their neighbours (`trusted-suite.ts` /
the realInput list).

## 9. Use-case diagrams

Each in-force StRS of these scopes (14 after the change: 13 kept plus the new one; FMSCHEMA-002 is
superseded) gets one `### Use case diagram` section per the rule of `req-use-case-diagrams`. The
diagram shows only behaviour that a derived SwRS specifies. Kinds and content, from the audit:

| StRS | Kind | Content |
| --- | --- | --- |
| FMEDIT-001 | sequence | Writer, Page (properties table), Field editor, Host, VS Code document: click cell, editor of the type, type and Enter, `previewFrontmatterSave`, plan and check, one edit, table re-rendered in place; refusal shown in the editor |
| FMEDIT-005 | sequence | Writer, Field action menu, Host, Document: Add field, schema field or custom key, one inserted line, re-render, new field's editor opens; Remove branch (disabled when required) |
| FMEDIT-008 | state | field editor: Open, Saving, Saved (one undo step, only the field lines changed), Refused (reason shown, text kept), Flushed (navigation, written as typed); other edits blocked while open |
| FMSCHEMA-001 | sequence | Writer, VS Code document, Host (analyse), Page: extract the block, parse YAML, render table and body (or the invalid-frontmatter row), edit, re-analyse after 300 ms, patch in place (held while a field editor is open) |
| FMSCHEMA-006 | state (the audit proposes an activity diagram; the rule allows sequence, actors or state) | document type, walk up to `_schema`, match `{type}.schema.*`, parse, inline `$ref`, compile; exits: no folder, no file, parse error, compile error, untrusted |
| FMSCHEMA-010 | sequence | Host, Validator, Page, Writer: order by schema, validate (2020-12), issues on rows, badge and missing-required line, badge press focuses the first issue |
| FMSCHEMA-014 | sequence | Writer, Page, Host, file system / stem index, VS Code editor: pending first paint, resolve after 150 ms, status patch, tooltip, click or Enter opens the target (or a warning) |
| REVIEW-001 | sequence | Reviewer, VS Code (document and `.comments.json`), Host comments feature, Page: read and validate (invalid: one warning, no threads), post threads with orphan verdicts, highlight or Orphaned comments, click opens the popover |
| REVIEW-003 | sequence | Reviewer, Page, Host, comment store (per-file queue), file system: create lane and a reply / resolve / delete lane, refusal keeps the text |
| REVIEW-008 | state | one thread: Anchored, Shifted (in memory), Saved lines; re-anchor to Moved or Orphaned (lines kept); back to Anchored when the quote returns; rename moves the file unless the target exists |
| REVIEW-012 | sequence | Writer, Renderer, Page, Host: gray and green chips, toggle the box, Comments button hides gray and thread chips, TODO action wraps the lines in one undo step |
| REVIEW-015 | sequence | Writer, Page (thread chip), Host, VS Code document: reply, exactly-one-thread check, insert above `-->` in one undo step; Delete branch; refusal while an editor is open |
| REVIEW-017 | sequence | Writer, document, Git extension, Host, Page: HEAD (at most 1 MiB), line diff, ranges, innermost blocks marked, Diff button hides the bars |
| new side-by-side StRS | sequence | Side-by-side on, host renders and posts HEAD, cards with word marks, off restores |

The four approved StRS get theirs only with the owner's agreement (section 1).

## 10. Log and generated files

- `just requirements-update` after the requirement edits; generated fields, indexes and Links blocks
  committed, never hand-edited.
- One dated entry in `requirements/tiers/log.md` (under `## 2026-MM-DD`, a `### Gardening of
  review-annotations, frontmatter-editing, frontmatter-schema` sub-heading): the old-to-new mapping
  of section 4, the supersession of StRS-FMSCHEMA-002, the new StRS, the reparenting, the owner's
  re-approval (or refusal) of the approved StRS, and the verification results actually run.

## Out of scope

- Any product behaviour change (for example adding a TODO shortcut; fixing a "Known issue").
- Deleting requirement files (owner decision).
- Markers and parents of other scopes, beyond removing this CR's StRS from shared SwRS parents
  (section 3); TOOLBAR-113.
- Rewriting the "Known issue" lines of the SwRS (X5 is handled on the StRS side only).
- Making the diagram section mandatory with a check (a later step after the six restructure CRs).
- Lifecycle changes `draft` -> `proposed` (none in these scopes).

## Evidence

Checks, in the worktree after `just dev`:

1. `uv run --no-sync --group requirements okfreq validate requirements --check-links --project-root .`
   and `just requirements-lint` pass; `scripts/check_main_paths.py` reports every cited SwRS valid.
2. `uv run --no-sync --group requirements okfreq update-coverage requirements --check` and
   `okfreq lint requirements --check` are clean after `just requirements-update`.
3. `uv run --no-sync --group requirements okfreq trace requirements --json`: each in-force SwRS of
   the three scopes has at least one `@implements_req` and one focused `@tests_req` (not in a block
   of more than 3); no marker names a superseded or deprecated ID of these scopes; each in-force StRS
   of these scopes has a `@tests_req` on a real scenario, none in `realInput/markers.ts`.
4. `just check` passes, including the `req-marker-gate` check, with this CR's entries removed from
   its baseline (the baseline file's diff shows only removals).
5. The split CSS constants and the refactored `src/` functions: `just check` unit tests pass, and
   the joined `COMMENT_CSS` (and any other split string) is asserted equal to its value before the
   change.
6. New and re-marked unit tests run in `just check`; a new test is shown failing when its assertion
   is broken (constitution 3, for the tests added for unchecked scenarios).
7. The new integration scenarios (`scenarioTodoToggle`, the `previewEditing.test.ts` schema steps)
   and the extracted steps: `just e2e` on an unlocked screen, or, since `just preflight` on Windows
   runs the static stage only, the heavy CI run on the branch:
   `gh workflow run ci.yml --ref <branch> -f heavy=true`, green.
8. `just preflight` passes.

Scenario steps a reviewer can follow:

- Open `requirements/tiers/strs/review-annotations/StRS-MDOKFSTUDIO-REVIEW-012.md` (if re-approved):
  the text says the TODO action comes from the edition palette or the slash menu, matching
  SwRS-REVIEW-160; the diagram renders on GitHub.
- Open StRS-FMSCHEMA-002: `req_lifecycle: superseded`, `superseded_by` StRS-FMSCHEMA-001; FMSCHEMA-001
  shows the invalid-YAML option in Path 1.
- `okfreq trace` for SwRS-REVIEW-160: focused tests in `editActions.test.ts` and
  `runtimeEditPalette.test.ts`, no header block.
- The PR body lists the IDs added, changed and superseded with their source and test files, and
  the approved StRS changed with the owner's review requested.

## Open questions for the user

1. SwRS-FMSCHEMA-091 (the exported properties table opens on a click) is an export behaviour filed
   in frontmatter-schema and derived only by StRS-TOOLBAR-014. Default applied: it stays in
   frontmatter-schema with `relates_to: StRS-MDOKFSTUDIO-FMSCHEMA-001`. Moving it to
   toolbar-navigation would mean a new TOOLBAR SwRS and superseding FMSCHEMA-091. Keep the default?
2. Does a change limited to the generated `derived_by` / Links block of an approved StRS (an SwRS
   folded into another, a shared rule reparented) need re-approval? This specification treats it as
   not authored text and lists it in the owner package for information only.
