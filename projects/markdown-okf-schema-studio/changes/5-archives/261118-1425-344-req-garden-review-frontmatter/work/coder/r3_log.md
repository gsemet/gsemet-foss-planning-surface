### Gardening of review-annotations, frontmatter-editing, frontmatter-schema

- Merged (the survivor keeps its ID and takes the scenarios, verification notes and `depends_on` of the absorbed
  SwRS; the absorbed one is `superseded`): REVIEW-069 into REVIEW-054; REVIEW-070 and REVIEW-071 into REVIEW-074;
  REVIEW-081 folded into REVIEW-044 (now "a comment editor sends its text on Save or Cmd+Enter and keeps it until the
  host accepts it", with a comment-box and a reply-box scenario table); REVIEW-101 into REVIEW-100; REVIEW-216 into
  REVIEW-017; REVIEW-156 into REVIEW-152; REVIEW-178 into REVIEW-186 and REVIEW-192; REVIEW-007 into REVIEW-006
  and REVIEW-009; REVIEW-005 and REVIEW-010 into REVIEW-009; REVIEW-200 and REVIEW-203 into REVIEW-195; REVIEW-208
  into REVIEW-207; FMEDIT-054 into FMEDIT-016 (it did not take FMEDIT-054's parent TRUST-009); FMSCHEMA-060 into
  FMSCHEMA-050. Markers naming an absorbed ID were renamed to the survivor; no marker in `src/` or `test/` names a
  superseded or deprecated SwRS of these scopes.
- Text fixes without a merge: REVIEW-086 (Delete with its confirmation), REVIEW-094 and REVIEW-119 (the scenarios
  "Typing writes nothing" and "Change of a clean document" and the `shiftForEdits` marker move to REVIEW-094),
  REVIEW-133 and REVIEW-167 (a comment and a thread in a tab item keep their own source lines).
- Superseded: StRS-MDOKFSTUDIO-FMSCHEMA-002 by StRS-MDOKFSTUDIO-FMSCHEMA-001; SwRS FMSCHEMA-017, 018 and 076 now
  derive from StRS FMSCHEMA-001.
- Added: StRS-MDOKFSTUDIO-REVIEW-018 (a writer compares each changed block with its last-commit version side by
  side); SwRS REVIEW-006, 008 and 009 derive from it, no longer from REVIEW-008 and REVIEW-017 only. Use case diagrams
  added to StRS FMEDIT-001, 005, 008, FMSCHEMA-001, 006, 010, 014, REVIEW-008, 017 and 018.
- Reparenting: shared rules are cited by `depends_on` instead of derived. Removed from `derives_from`: FMEDIT-001,
  FMEDIT-008 and REVIEW-008 from BLOCK-041; FMEDIT-001, FMEDIT-008 and REVIEW-015 from BLOCK-058; FMEDIT-008 from
  BLOCK-109 and TRUST-005; FMEDIT-008 and REVIEW-015 from TRUST-065; REVIEW-001 from TRUST-001; REVIEW-012 from
  LIFE-170; FMEDIT-005 from FMSCHEMA-084 (now `relates_to`); FMSCHEMA-091 gains `relates_to` StRS FMSCHEMA-001.
- Owner approval: the approved StRS REVIEW-001, 003, 012 and 015 were re-approved by the owner on 2026-11-17
  (`approved_at` 2026-11-17T22:55:00+01:00). Commits: "docs: add a use case diagram to the comments file StRS",
  "docs: add a use case diagram to the comment write StRS and cite the merged reply SwRS", "docs: state that the TODO
  action comes from the palette or the slash menu", "docs: add a use case diagram to the thread reply StRS, undo step
  cited not derived". REVIEW-012 now says the TODO action comes from the palette or the slash menu (it has no
  shortcut).
- Markers: the 14-ID file-level blocks of `okfFrontmatter.test.ts` and `previewEditing.test.ts` are split onto their
  tests and steps (at most 3 per marker block); `realInput/markers.ts` lost the FMEDIT-019, FMSCHEMA-039, 043, 063
  lines and the StRS FMEDIT-001, 005, 008, FMSCHEMA-001, 014 lines, which now sit on their scenarios; the
  FMEDIT-054 check moved onto a focused FMEDIT-016 test in `pageToHost.test.ts`; `propertiesTable.ts`,
  `okfFrontmatter.ts`, `frontmatterEdit.ts` and `commentStyles.ts` carry one marker per branch (the comment
  stylesheet is split into named parts, same bytes); `scripts/marker-baseline.json` only shrank.
- New tests: `okfFrontmatter.test.ts` and `previewEditing.test.ts` keep their assertions (the patch tests moved to
  `okfFrontmatterPatches.test.ts`, the step helpers to `previewEditingHelpers.ts`, for the 1500-line limit); a flush
  test (FMEDIT-067) in `frontmatterEdit.test.ts`; a comments-file rename test (REVIEW-125) in
  `reviewReqComments.requirements.test.ts`; a refusal test of the frontmatter save message (FMEDIT-016) in
  `pageToHost.test.ts`; `commentStyles.test.ts` is marked; two real-window steps in `previewEditing.test.ts`
  (schema order and badge, schema problem row) and the real-window scenario `scenarioTodoToggle`
  (`realInput/blockKeys.ts`, REVIEW-012), type-checked only. Each new unit test was shown failing once with a
  broken assertion.
- No product behaviour change.
- Verified: `just requirements-update` and `just requirements-lint` pass (0 files would change after the update);
  `okfreq trace requirements --json` shows each in-force SwRS of the three scopes with an `@implements_req` and a
  focused `@tests_req`, and a validation test on each in-force StRS; `just check` and
  `just check-settings unit` pass; the real-window suites (`just e2e`) were not run.
