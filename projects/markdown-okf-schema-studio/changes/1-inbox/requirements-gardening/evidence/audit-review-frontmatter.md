# Audit: review-annotations, frontmatter-editing, frontmatter-schema

Read-only audit (gardening phases 4, 6, 6b) of `markdown-okf-schema-studio` at `main` (dedbdb2a),
2026-11-17. Sources: `okfreq trace requirements --json` (no missing IDs, no non-leaf, no warnings),
the requirement files, and every `@implements_req` / `@tests_req` location with its surrounding code.
Paths are relative to the repository root. Severity: **H** misleading traceability or missing
behaviour, **M** split or marker placement to fix, **L** wording.

Scope inventory: 14 StRS in force (FMEDIT 3, FMSCHEMA 5, REVIEW 6, of which REVIEW-001/003/012/015
are `approved`); 21 superseded StRS (FMEDIT 8, FMSCHEMA 13). 87 SwRS in force in the three scopes
(REVIEW 53, FMSCHEMA 21, FMEDIT 13), 141 superseded, 5 deprecated, no draft. 10 SwRS of other scopes
are derived by these StRS (BLOCK-041/058/109/193/228, TRUST-001/005/065, TOOLBAR-113, LIFE-170): their
relation was checked, their markers are left to their scope's audit. No in-force StRS cites a
superseded or deprecated SwRS in its Main paths. Every StRS has a Main paths section.

## Summary

| StRS | Title (short) | #SwRS | Relevance | Split OK? | Markers OK? | Tests OK? | Validation test? | Diagram |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FMEDIT-001 | Edit metadata values in place | 9 | Real; rationale too long | Mostly | Partial | Partial | Indirect (companion file) | Sequence |
| FMEDIT-005 | Add, rename, remove fields | 6 | Real, clear | Mostly | Partial | Partial | Indirect (companion file) | Sequence |
| FMEDIT-008 | Edits keep source intact | 12 | Real; overlaps 001/005 | Partial | Partial | Partial | Indirect (companion file) | State |
| FMSCHEMA-001 | Readable, configurable table | 7 | Real; rationale restates SwRS | OK | No (central blocks) | Partial | Yes | Sequence |
| FMSCHEMA-002 | Invalid frontmatter explained | 1 | Thin, duplicate of 001 | n/a (merge) | as 001 | OK | Visual only | Fold into 001 |
| FMSCHEMA-006 | Find the schema, report problems | 4 | Real; rationale long | OK | OK | Partial | Visual only | Activity |
| FMSCHEMA-010 | Fields follow the schema | 3 | Real | OK | No (central blocks) | Partial (misattributed) | Visual only | Sequence |
| FMSCHEMA-014 | Link fields resolve and open | 9 | Real; rationale ~20 bullets | Partial | Partial | Partial | Yes | Sequence |
| REVIEW-001 | Read threads, keep orphans | 13 | Real, clear | Partial | Mostly | Partial | Yes | Sequence |
| REVIEW-003 | Comment, reply, resolve, delete | 21 | Real; large | Partial | Partial | Partial | Yes | Sequence |
| REVIEW-008 | Threads follow edits, renames | 8 | Real, clear | Partial | Partial | Partial | Yes | State |
| REVIEW-012 | Comment and TODO chips | 8 | Real; contradicts REVIEW-160 | Mostly | OK | No (REVIEW-160) | Visual only | Sequence |
| REVIEW-015 | Inline thread in the source | 7 | Real, clear | Mostly | OK | Partial | Yes | Sequence |
| REVIEW-017 | Changed blocks since commit | 13 | Text omits side-by-side | No | Partial | Good | Yes | Sequence |

## Cross-cutting findings

- **X1 (M, systemic) One marker per SwRS, on the first test only.** The SwRS verification notes
  name several tests, but `@tests_req` sits on one of them. Examples: REVIEW-171 names 7 tests in
  `test/page/modules/inlineThread.test.ts`, only line 74 is marked; REVIEW-100/101/107 have one
  marker each (`test/core/comments/anchoring.test.ts:67,74,138`) while about 30 tests of that file
  check their scenarios (lines 81-261, unmarked); REVIEW-004 scenarios "one bad thread", "limits"
  are tested at `test/core/comments/commentModel.test.ts:55,74`, unmarked; REVIEW-074 resolve and
  delete are tested at `test/core/comments/commentEditing.test.ts:185,198`, unmarked. About 26 SwRS
  of these scopes have exactly one focused test marker. The scenarios are mostly checked; the
  traceability does not show it.
- **X2 (M) File-level marker blocks in tests.** `test/core/frontmatter/okfFrontmatter.test.ts:29-43`
  (15 IDs over 63 tests); `test/integration/previewEditing.test.ts:242-258` (17 IDs on `run()`);
  `test/page/modules/editActions.test.ts:~31-50` (43 IDs); `test/integration/realInput/markers.ts`
  (64 IDs, a companion file with no test code); `test/core/protocol/pageStateMessages.test.ts:220-228`
  (9 IDs on one oracle test). They link IDs to a file, not to the test of a scenario. For the
  okfFrontmatter block, focused tests exist and should carry the markers (for example FMSCHEMA-019
  at line 226, FMSCHEMA-023 at 277 and 970, FMSCHEMA-029 at 309, FMSCHEMA-039 at 943, FMEDIT-037 at
  1339-1428).
- **X3 (M) Central implementation marker blocks.** `src/core/frontmatter/propertiesTable.ts:191-198`
  puts 8 IDs (FMSCHEMA-084/004/005/006/014/039, TRUST-001, REVIEW-215) on `renderPropertiesTable`;
  `src/core/frontmatter/okfFrontmatter.ts:323-326` (4 IDs on `analyzeFrontmatterCore`);
  `src/core/edits/frontmatterEdit.ts:79-82` (FMEDIT-016/024/037/067 on `planFrontmatterSave`);
  `src/core/preview/styles/commentStyles.ts:3-7` (5 IDs on the whole `COMMENT_CSS` string);
  `src/core/frontmatter/frontmatterValidate.ts:319-321` (3 IDs on `fieldsFromYaml`). Each marker
  should go to the branch or helper that does the behaviour (for example the Description toggle
  markup for FMSCHEMA-014, the badge markup for FMSCHEMA-039, the `data-okf-orphans` rule for
  REVIEW-028).
- **X4 (M) The message-validation rule is repeated for each feature.** REVIEW-069, 070, 071, 178,
  007, 156, 208 and FMEDIT-054 each specify "a malformed message is dropped", which TRUST-052,
  TRUST-059 and TRUST-065 already state and which they cite in `depends_on`. The shared-rule clause of
  the granularity rule applies.
- **X5 (L) Many known issues in FMSCHEMA and FMEDIT.** Most in-force FMSCHEMA and FMEDIT SwRS carry
  a "Known issue" (for example FMSCHEMA-006 names a helper that is never called, an internal detail;
  FMSCHEMA-004: the frontmatter is validated while the table is off). They are listed again in the
  StRS rationales, so each one is written twice.

## FMEDIT-001: A writer edits metadata values in place with fitting controls

- Relevance (L): a real use case. The rationale has 15 bullets, 5 of them known issues that repeat
  SwRS text (control kinds, list editing). Cut it to the constraints a stakeholder cares about.
- Split: FMEDIT-001, 003, 004, 010, 016, 019 plus BLOCK-041/058/228. FMEDIT-019 (10 scenarios)
  bundles save, Escape, refusal display and undo keys. It is one behaviour ("commit or cancel a field
  editor"), so it stays as it is. FMEDIT-003 merges the old per-type SwRS, which is fine.
- Markers (M): `src/page/features/pageInput.ts:223-224` puts FMEDIT-001 and 019 on one click
  listener, which is acceptable. FMEDIT-003 has one marker at `frontmatterValueEditor.ts:87` (the
  enum branch) for 9 scenarios: the boolean toggle, the native inputs and Set to null have no marker.
- Tests (M): FMEDIT-004 has one focused test (`runtimeFrontmatterEditor.test.ts:915`, Enter saves).
  The "multi-line literal block" and "trailing line breaks" scenarios are only traced through the
  okfFrontmatter block (X2). FMEDIT-016 has one focused test (`test/core/edits/frontmatterEdit.test.ts:40`).
  The schema-error and "only errors of the edited field" scenarios are at line 93 (unmarked).
- Validation (M): only `test/integration/realInput/markers.ts:51` (companion list). Put the StRS
  marker on `scenarioEnterCommitsTextField` (`test/integration/realInput/textEditing.ts:189`) and
  `scenarioListEditorClickAndKeys` (`frontmatterFields.ts:142`).
- Diagram: sequence of Writer, Page (properties table), Field editor, Host, VS Code document:
  click cell, open editor of the type, type and Enter, previewFrontmatterSave, plan and check, apply
  one edit, re-render the table in place (or a refusal shown in the editor).

## FMEDIT-005: A writer adds, renames and removes metadata fields

- Relevance: clear and well bounded.
- Split (L): FMEDIT-024, 028, 029, 037, 043 and FMSCHEMA-084. Deriving FMSCHEMA-084 (validation
  report) is weak; the required-field refusal is already in FMEDIT-029. Suggest dropping that link,
  or using `relates_to`.
- Markers (M): FMEDIT-024, 037 and 067 share `frontmatterEdit.ts:80-82` (X3). Put them on the
  rename branch, the add branch and the flush branch of `planFrontmatterSave`.
- Tests (M): FMEDIT-028 has 9 scenarios and two focused tests (`runtimeFrontmatterEditor.test.ts:595`,
  `runtimeFrontmatterFields.test.ts:299`). The Custom-key refusals and the narrow-preview boundary
  are not marked. They are probably covered by `realInput/frontmatterFields.ts:303,415`, which carry
  no marker.
- Validation (M): companion file only (`markers.ts:52`). Candidates are
  `scenarioCustomKeyAndOpenNewField` and `scenarioAddFieldPositionAndEscape`
  (`test/integration/realInput/frontmatterFields.ts:415,501`).
- Diagram: sequence of Writer, Field action menu, Host, Document: open the editor, Add field, pick a
  schema field or a custom key, insert one line, re-render, open the new field's editor; a second
  branch for Remove (disabled when required).

## FMEDIT-008: Metadata edits keep the source intact, follow the schema and never lose text

- Relevance (M): a real cross-cutting need (safety), but it overlaps FMEDIT-001 and 005. It shares
  FMEDIT-016, 024, 029 and 043, and its Path 2 "Remove a field" repeats FMEDIT-005. Keep this StRS
  for preservation, refusal and flush, and drop Path 2.
- Split: FMEDIT-043, 016, 054, 067 plus BLOCK-041/058/109/193 and TRUST-005/065. BLOCK-109 (insert
  point arrows) is linked only through one refusal scenario about the properties bar; it is marginal
  here (L). FMEDIT-054 is a protocol shape (X4).
- Markers (M): FMEDIT-067 is spread over 5 places, which is fine. The marker at
  `frontmatterEdit.ts:82` is in the X3 block.
- Tests: FMEDIT-067's unit marker is at `test/core/edits/frontmatterEdit.test.ts:56`. That test
  mostly checks stale and bad-key refusals (the FMEDIT-016 and 024 behaviours) and checks the flush
  only in its last assertion (L, misattributed). FMEDIT-054 is checked only by an oracle-equivalence
  test (`pageStateMessages.test.ts:229`) in a 9-ID block (M).
- Validation (M): companion file only (`markers.ts:53`). The real scenarios exist:
  `scenarioFrontmatterValueMinimalPatch`, `scenarioFrontmatterStructuralMinimalPatch`
  (`realInput/textEditing.ts:83,124`) and `scenarioFlushFrontmatterKeptAsTyped`
  (`realInput/flushBeforeNavigate.ts:389`).
- Diagram: state of the field editor: Open, then Saving (save posted), then Saved (one undo step,
  only the field lines changed), Refused (reason shown, text kept) or Flushed (navigation, written as
  typed); Open goes to Blocked-others while it is open.

## FMSCHEMA-001: Frontmatter appears as a readable, configurable properties table

- Relevance (M): a real use case. The rationale (13 bullets) restates SwRS 004, 005, 006, 014 and 043
  and their known issues. The fence and invalid-YAML text duplicates FMSCHEMA-002.
- Split: FMSCHEMA-001, 004, 005, 006, 014, 043, 090. This is good granularity. FMSCHEMA-004 is a
  settings-driven behaviour (hide the table), which is acceptable.
- Markers (M): X3. FMSCHEMA-004/005/006/014 are all on `renderPropertiesTable`
  (`propertiesTable.ts:192-195`); FMSCHEMA-001/005 are on `analyzeFrontmatterCore`
  (`okfFrontmatter.ts:323,326`); FMSCHEMA-005 is also in the `PROPERTIES_CSS` header
  (`propertiesStyles.ts:2`). FMSCHEMA-006 has a single marker for 5 scenarios, and that marker sits
  in the block.
- Tests (M): FMSCHEMA-006 has one focused test (`propertiesTable.test.ts:643`, nested objects). The
  list limit, lean frame, contrast and narrow scenarios are visual only (`scenarioDefinitions1.ts:770`).
  FMSCHEMA-043 has one focused test (`runtimeFrontmatterFields.test.ts:540`); the "page not ready"
  refusal is unmarked.
- Validation: yes (`test/integration/previewEditing.test.ts:242`, visual scenarios).
- Diagram: sequence of Writer, VS Code document, Host (analyse), Page: open the document, extract the
  block, parse YAML, render the table and body, edit the text, re-analyse after 300 ms, patch the
  table in place (held back while a field editor is open).

## FMSCHEMA-002: Invalid frontmatter is explained and the body still renders

- Relevance (M): thin. Its only SwRS is FMSCHEMA-001, which FMSCHEMA-001 (StRS) also derives and
  whose "Invalid YAML" scenarios and rationale already cover it. Proposal: supersede it by
  StRS-FMSCHEMA-001 and keep its Main path as Path 3 of FMSCHEMA-001. Validation today is the visual
  scenario `scenarioDefinitions2.ts:928` only; `test/core/frontmatter/diagReq.frontmatter.requirements.test.ts:50`
  is a unit test that could carry the scenario.
- Diagram: none (a refusal path of FMSCHEMA-001).

## FMSCHEMA-006: A document finds its schema and schema problems are reported

- Relevance (L): clear. The rationale has 16 bullets with 5 known issues; trim it to the
  stakeholder constraints.
- Split: FMSCHEMA-005 (shared with 001), 019, 023, 027. This is fine.
- Markers: correct places (`okfFrontmatter.ts:87` findSchemaDirectory, `:173` parseSchemaFile,
  `frontmatterParse.ts:145`, `schemaRegistry.ts:18`). `src/node-services/schemaFiles.ts:27` marks a
  constant (`MAX_LISTED_DIRECTORIES`) rather than the listing cache (L).
- Tests (M): FMSCHEMA-019 has focused markers only on the listing cache
  (`test/node-services/schemaFiles.test.ts:10,33`). Nearest-folder, case-insensitive match and "no
  lookup in Restricted Mode" are tested in `okfFrontmatter.test.ts:226,257` but traced only by the
  X2 block. For FMSCHEMA-023, the "JSON pointer fragment" and "Extension fallback" scenarios are at
  `okfFrontmatter.test.ts:277` (unmarked).
- Validation (M): visual only (`scenarioDefinitions1.ts:769`, `scenarioDefinitions2.ts:349`). No
  integration test opens a typed document with a real `_schema` folder; `previewEditing.test.ts`
  (fixture `08-okf-schema`) could carry it.
- Diagram: activity of document type, walk up to `_schema`, match `{type}.schema.*`, parse
  YAML/JSON/JSON5, inline `$ref`, compile. The exits are no folder (generic table), no file (info
  row), parse error (warning row), compile error (red row) and untrusted (info row).

## FMSCHEMA-010: Fields follow the schema and problems show on the field concerned

- Relevance: clear.
- Split: FMSCHEMA-029, 039, 084. This is fine. FMSCHEMA-084 carries the strict-setting scenario,
  which is consistent with the settings rule.
- Markers (M): all three share `fieldsFromYaml` (`frontmatterValidate.ts:319-321`) and the X3
  blocks. FMSCHEMA-084 also has `schemaValidator.ts:5`, which is correct.
- Tests (H, misattributed): FMSCHEMA-029's only focused unit test is
  `test/core/frontmatter/propertiesTable.test.ts:368` "error rows carry the red underline class",
  which tests FMSCHEMA-084 (and the tooltip). The schema-order test (`okfFrontmatter.test.ts:309`),
  the type icons (`propertiesTable.test.ts:695`) and `fieldIconType` (`okfFrontmatter.test.ts:85`)
  carry no marker. FMSCHEMA-084 has the same single unit test for 7 scenarios (2020-12 keywords,
  closed schema and strict setting are unmarked).
- Validation (M): visual only (`scenarioDefinitions2.ts:315`).
- Diagram: sequence of Host (analyse), Validator, Page, Writer: order the fields by schema, validate
  (2020-12), attach issues to rows, render the badge and the missing-required line, the writer
  presses the badge, the page scrolls to and focuses the first issue.

## FMSCHEMA-014: Frontmatter link fields resolve, show their status and can be followed

- Relevance (M): a real use case. The rationale (about 20 bullets) is a full specification; reduce
  it to the user need, the roots and the refusal rule.
- Split (M): FMSCHEMA-039, 046, 050, 055, 060, 063, 067, 073 and TOOLBAR-113. FMSCHEMA-060 is a
  settings SwRS ("bundleRoot, projectRoot, allowOutsideWorkspaceLinks set the roots"). Fold it into
  FMSCHEMA-050 as scenarios (old 050 + 060 becomes new 050 "links resolve from the configured or
  default root"). TOOLBAR-113 is a protocol shape (X4).
- Markers (M): FMSCHEMA-073 is at `src/session/features/links.ts:213`, inside a 5-ID block on
  `handleLink`, which is acceptable. FMSCHEMA-063/067 share `formatLinkedValue`
  (`propertiesTable.ts:62-63`).
- Tests (M): FMSCHEMA-046 has 7 scenarios and one focused test (`fileLinks.test.ts:65`, oneOf).
  FMSCHEMA-073 has one focused test (`test/session/links.test.ts:17`). The "unusable link warning"
  is in `diagReq.links.requirements.test.ts:12`, which is marked for TOOLBAR-113 only. FMSCHEMA-055:
  "ambiguous or unknown stem" and "unreadable candidate" are tested in
  `okfFrontmatter.test.ts:830,877` (X2 block).
- Validation: yes (`previewEditing.test.ts:243`, `scenarioDefinitions1.ts:808`, `markers.ts:55`).
- Diagram: sequence of Writer, Page, Host, File system/stem index, VS Code editor: first paint
  (pending), resolve after 150 ms (root and containment), patch the table with link status, hover
  for the tooltip with target fields, click or Enter sends previewLink, open the target at the marker
  line (or a warning for an unusable link).

## REVIEW-001: A reviewer reads review threads on the text, and unplaceable ones are kept (approved)

- Relevance: clear, good length, with a good Path 2 (re-placement after undo).
- Split (M): REVIEW-001, 004, 012, 017, 021, 028, 100, 101, 107, 119, 216, 219 and TRUST-001.
  REVIEW-100 and 101 are the two outcomes of one re-anchoring step and share one implementation
  marker (`src/core/comments/anchoring.ts:443-444` on `reanchorWith`). Mapping: 100 + 101 become one
  SwRS "a thread follows its quote, or is orphaned keeping its lines"; 107 (fuzzy) and 219 (placed
  again) stay separate. REVIEW-216 (quote over a wrapped line) is a boundary scenario of REVIEW-017
  (highlight) and could merge into it (L).
- Markers: well placed (`commentModel.ts:79,140`, `comments.ts:115,135,416`,
  `commentThreads.ts:358,456,621`, `commentThreadData.ts:32,70`). REVIEW-028 is also in the
  `COMMENT_CSS` header (`commentStyles.ts:4`, X3); point it at the orphan-box rule.
- Tests (M): X1. REVIEW-017 has 8 scenarios and one marker (`commentThreads.test.ts:143`); the
  boundary and refusal tests at lines 155-216 and 292 are unmarked. REVIEW-028's host-verdict
  scenarios are tested at `commentThreads.test.ts:791-812`, unmarked. REVIEW-012 is well covered
  (`test/session/reviewReqComments.requirements.test.ts:150-431`).
- Validation: yes (`test/integration/reviewComments.test.ts:38`, `commentAnchors.test.ts:33`,
  `commentWrite.test.ts:37`). None of them clicks a highlight in the real window; the popover
  opening is unit-tested only.
- Diagram: sequence of Reviewer, VS Code (document and `.comments.json`), Host comments feature,
  Page: show the document, read and validate the comments file (invalid: one warning, no threads),
  post the threads with orphan verdicts, highlight the quote or list it in Orphaned comments, the
  reviewer clicks the highlight, the popover opens.

## REVIEW-003: A reviewer comments, replies, resolves and deletes, and no comment is lost (approved)

- Relevance (L): clear, but the widest StRS (21 SwRS).
- Split (M):
  - REVIEW-069, 070 and 071 are three message-shape SwRS (X4): merge them into one "comment messages
    from the page are validated" SwRS, or into refusal scenarios of 054 and 074 that cite TRUST-052.
  - REVIEW-044 (comment box) and REVIEW-081 (reply box) specify the same behaviour, "send on Save or
    Cmd+Enter and keep the text until the host accepts", for two editors. They are candidates to
    merge into one SwRS with a table per editor (L).
  - REVIEW-081's normative text says only "show a reply text area and a Reply button", while its
    title and scenarios cover sending and keeping the reply (L).
  - REVIEW-086's normative text covers Resolve and Reopen only; its title and scenarios also cover
    Delete (L).
  - REVIEW-002 (contrast on every theme) is a theme rule; it fits better under a theme StRS or as
    `relates_to` (L).
- Markers (M): REVIEW-074 is marked only on `addReply` (`commentModel.ts:247`) and `handleReply`
  (`comments.ts:557`). The resolve and delete code (`setResolved`, `deleteThread`, `handleResolve`,
  the delete handler) carries no REVIEW-074 marker. REVIEW-044/054/069 share a 3-ID block on
  `handleCreate` (`comments.ts:542-544`), which is acceptable. REVIEW-054 at
  `src/host-vscode/vscodeHost.ts:80` (atomic rename) is correct.
- Tests (M): REVIEW-044 has 9 scenarios. Its two markers are on `normalizeBody`
  (`commentEditing.test.ts:78`) and on key isolation (`commentCompose.test.ts:234`). The refused
  save, the 15 s timeout and the late ok are tested at `commentCompose.test.ts:262,283,296`,
  unmarked. REVIEW-081's refusal and timeout tests are at `commentThreads.test.ts:375,394`,
  unmarked. REVIEW-086's refused resolve, delete question and "one action at a time" tests are at
  `commentThreads.test.ts:510-581,744`, unmarked. REVIEW-049 has one marker; the triple click and
  the 500-character cap are at `commentCompose.test.ts:80,108`, unmarked. REVIEW-217 and 218 are
  well marked (`commentEditorBehaviour.test.ts`).
- Validation: yes (`test/integration/commentWrite.test.ts:38`).
- Diagram: sequence of Reviewer, Page (Comment button, comment box, popover), Host, Comment store
  (per-file queue), File system: select text, Comment button, type and Save, previewCommentCreate,
  read latest, append and write atomically, ok, close the box, re-post the threads. A second lane
  for reply, resolve and delete, where a refusal keeps the text and shows the reason.

## REVIEW-008: Review threads follow edits and renames of the document

- Relevance: clear and short.
- Split (M): REVIEW-094 (shift in memory) and REVIEW-119 (write on save) overlap. REVIEW-119
  carries "Typing writes nothing" and "Change of a clean document", and its implementation marker
  at `src/session/features/comments.ts:272` sits inside `shiftForEdits`, the REVIEW-094 behaviour.
  Mapping: move the typing and dirty or clean change scenarios and the line-272 marker to REVIEW-094;
  REVIEW-119 keeps the save-time write (`persistAnchors`, line 294). REVIEW-100, 101, 107 and 219
  are shared with REVIEW-001 (see the merge there). BLOCK-041 is derived here with no visible role
  in this use case (L).
- Markers: REVIEW-125 at `moveSidecars` (`comments.ts:369`) and REVIEW-094 at `shiftThreadLines`
  (`anchoring.ts:71`) are correct.
- Tests (M): REVIEW-094 has one marker (`anchoring.test.ts:27`); lines 38, 55, 61 and 166 test its
  other scenarios, unmarked. REVIEW-125 has one focused marker (`reviewReqComments.requirements.test.ts:272`,
  the "names another document" refusal); the nominal rename and move are covered only by the
  integration `run()` block (`commentAnchors.test.ts:37`).
- Validation: yes (`test/integration/commentAnchors.test.ts:32`).
- Diagram: state of one thread: Anchored, then Shifted (dirty edits, in memory), then Saved lines
  (document save writes them). Re-anchor goes to Moved (exact or fuzzy match) or Orphaned (lines
  kept); Orphaned goes back to Anchored when the quote returns. Rename moves the file unless the
  target exists.

## REVIEW-012: A writer sees HTML comments and TODO notes as chips and toggles them (approved)

- Relevance (H): the normative text says the Studio lets the writer "toggle a TODO comment around
  the current or selected lines from the keyboard in a block editor". REVIEW-160 specifies "The TODO
  action has no shortcut" (Ctrl+/ toggles a plain comment, see PALETTE-266); the action is reached
  through the palette and the slash menu. Either the StRS wording ("from the edition palette or the
  slash menu") or the SwRS is wrong. This StRS is approved, so the fix needs the owner's agreement.
- Split: REVIEW-003, 133, 139, 143, 152, 156, 160 and LIFE-170. REVIEW-156 is a stale-message rule
  (X4). The TODO toggle (REVIEW-160) appears in no Main path; add a Path 3 "Mark a line as TODO".
- Markers (M): REVIEW-133 and 167 are also marked on `unmapPlainBlocks`
  (`src/core/render/mystGridToctree.ts:462-463`), a tab-item helper. It does serve the "comment keeps
  its own lines in a tab item" scenario, but REVIEW-133 has no such scenario. Keep the marker only if
  that scenario is added. REVIEW-143 and 152 are in the `COMMENT_CSS` header (X3).
- Tests (H): REVIEW-160 has 8 scenarios. Its only test marker is in the 43-ID header block of
  `test/page/modules/editActions.test.ts` (around line 44). Its real tests (`todoCases` loop at line
  181, "the todo toggle is its own inverse" at 187, registry aliases around 203-222) are unmarked,
  and `trace` lists no focused test for it. REVIEW-139 is marked at `commentMarkers.test.ts:72,112`
  (good). REVIEW-133 has one focused test (`commentMarkers.test.ts:19`) for 8 scenarios.
- Validation (M): visual only (`test/visual/scenarioDefinitions2.ts:648`, chips visible or hidden).
  The integration scenario `scenarioHiddenReviewMarks` (`test/integration/realInput/blockKeys.ts:139`)
  could carry the StRS marker; nothing validates the TODO toggle end to end.
- Diagram: sequence of Writer, Renderer, Page, Host: render the HTML comment as a gray chip and TODO
  as a green chip, click or Enter on the chip toggles its box, Comments button off hides the gray and
  thread chips (TODO stays), the TODO action in a block editor wraps the lines and saves one undo
  step.

## REVIEW-015: A writer keeps a discussion in the Markdown source and answers it from the preview (approved)

- Relevance: clear and well scoped.
- Split: REVIEW-167, 171, 178, 186, 192, BLOCK-058 and TRUST-065. REVIEW-178 is a message shape (X4).
  The refusal while an edit is open is specified in REVIEW-171 (scenario table, line 66) through
  `depends_on` BLOCK-041; that is good.
- Markers: correct (`src/core/comments/inlineThread.ts:38,123,152`, `src/page/modules/inlineThread.ts:33`,
  `src/session/features/sourceEdits.ts:204`). REVIEW-167 is also on `unmapPlainBlocks` (see
  REVIEW-012).
- Tests (M): REVIEW-171 lists 7 tests in its verification notes; one is marked
  (`test/page/modules/inlineThread.test.ts:74`). REVIEW-192 is marked at
  `test/core/comments/inlineThread.test.ts:96` and `test/core/edits/sourceEdits.test.ts:69`
  (adequate).
- Validation: yes (`test/integration/inlineThread.test.ts:100`).
- Diagram: sequence of Writer, Page (thread chip), Host, VS Code document: open the chip, type a
  reply, previewThreadReply with lines, check exactly one thread and that the document is unchanged,
  insert the message above `-->` as one undo step, re-render. A Delete branch removes the lines and
  one blank line. A refusal branch applies when an editor is open.

## REVIEW-017: A writer sees which blocks changed since the last commit

- Relevance (H): the normative text and user need speak of green bars only. Six derived SwRS
  (REVIEW-005, 006, 007, 008, 009, 010) specify the side-by-side diff (Side-by-side button, HEAD
  cards, word marks), a second use case that no StRS states and no Main path shows. Proposal: create
  a new StRS "A writer compares each changed block with its last-commit version side by side",
  derive 005-010 from it, and keep REVIEW-017 for the change bars (195, 200, 203, 207, 208, 214,
  215).
- Split (M):
  - Internals: REVIEW-005 (word diff), REVIEW-010 (line hunks), REVIEW-200 (line ranges) and
    REVIEW-203 (HEAD text via the Git extension) describe algorithms and adapters. REVIEW-010 and
    REVIEW-200 are near-duplicates (two line diffs).
  - Proposed mapping: 200 + 203 become boundary scenarios of 195 (host posts changed lines); 010 + 005
    become scenarios of 009 (cards); 007 and 208 become refusal scenarios citing TRUST-059 (X4).
  - Each of 005-010 has 2 scenarios only, which confirms they are fragments of 2-3 behaviours.
- Markers (L): `src/page/modules/incomingChanges.ts:71-73` puts REVIEW-207, 215 and 208 on one
  `apply`, which is acceptable. REVIEW-215 is spread over 6 places, including the X3 block of
  `renderPropertiesTable`.
- Tests: good for the diff units (`lineHunks.test.ts`, `wordDiff.test.ts`, `sideBySideCards.test.ts`,
  `frontmatterChanges.test.ts`, all marked per test). REVIEW-200 and 203 have one marker each
  (`lineDiff.test.ts:6`, `headBaseline.test.ts:36`); check the other tests of those files (X1).
- Validation: yes (`test/integration/realWindowGaps.ts:182`, `scenarioDefinitions2.ts:1153`).
- Diagram: sequence of Writer, VS Code document, Git extension, Host incoming-changes feature, Page:
  edit the document, read HEAD (at most 1 MiB), diff lines, post the ranges, mark the innermost blocks
  and draw the bars, Diff button off hides them. The second StRS gets its own sequence: Side-by-side
  on, render HEAD, post the baseline, cards with word marks.

## Orphan SwRS

- None: every in-force SwRS of the three scopes has an in-force StRS parent.
- FMSCHEMA-091 "The exported properties table opens on a click" (L) is derived only by
  StRS-TOOLBAR-014 (export). It is an export behaviour filed in frontmatter-schema; move it to the
  toolbar-navigation scope or keep it with `relates_to` StRS-FMSCHEMA-001. Its markers are fine
  (`src/core/export/exportContent.ts:103`, `test/core/export/htmlExport.test.ts:165,300,318`).

## Counts by category

| Category | Count | Examples |
| --- | --- | --- |
| StRS audited (in force) | 14 | FMEDIT 3, FMSCHEMA 5, REVIEW 6 |
| SwRS audited (in force, these scopes) | 87 | plus 10 of other scopes checked for relation only |
| H: StRS text missing or contradicting derived behaviour | 2 | REVIEW-017 (side-by-side), REVIEW-012 vs REVIEW-160 |
| H: SwRS traced only by a file-level block or a misattributed test | 2 | REVIEW-160, FMSCHEMA-029 |
| M: StRS duplicate or overlap | 2 | FMSCHEMA-002 into 001; FMEDIT-008 Path 2 repeats FMEDIT-005 |
| M: repeated message-validation rule (X4) | 8 | REVIEW-007/069/070/071/156/178/208, FMEDIT-054 |
| M: SwRS that are scenarios of one behaviour (merge) | 7 | 100+101; 010+200; 200+203 into 195; 005/010 into 009; FMSCHEMA-060 into 050; 044~081 |
| M: SwRS describing internals | 4 | REVIEW-005, 010, 200, 203 |
| M: overlap or misplaced marker between two SwRS | 2 | REVIEW-119 marker in `shiftForEdits` (094); FMEDIT-067 test checks 016 |
| M: central implementation marker blocks (X3) | 6 sites | `propertiesTable.ts:191`, `okfFrontmatter.ts:323`, `frontmatterEdit.ts:79`, `commentStyles.ts:3`, `frontmatterValidate.ts:319`, `mystGridToctree.ts:462` |
| M: file-level test marker blocks (X2) | 5 files | `okfFrontmatter.test.ts`, `previewEditing.test.ts`, `editActions.test.ts`, `realInput/markers.ts`, `pageStateMessages.test.ts` |
| M: SwRS with a single focused test marker (X1) | about 26 | REVIEW-017, 049, 086, 094, 100, 101, 107, 171; FMEDIT-004, 016; FMSCHEMA-006, 029, 043, 046, 073, 084 |
| M: missing implementation marker for a part of a behaviour | 2 | REVIEW-074 resolve and delete; FMEDIT-003 boolean, native inputs, null |
| M: StRS validation only visual or companion file | 7 | FMEDIT-001/005/008 (companion), FMSCHEMA-002/006/010, REVIEW-012 (visual) |
| StRS with a direct validation test in an integration run | 7 | FMSCHEMA-001/014, REVIEW-001/003/008/015/017 |
| L: wording (verbose rationale, description narrower than title) | 9 | FMEDIT-001/008, FMSCHEMA-001/006/010/014 rationale; REVIEW-081, 086 descriptions; REVIEW-002 placement |
| Orphan SwRS | 0 | FMSCHEMA-091 is cross-scope (L) |
