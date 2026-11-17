Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: lifecycle-sync StRS and SwRS

Scope `lifecycle-sync`: 21 StRS (LIFE-001..021) and 165 SwRS (LIFE-001..165), reviewed against
`inventory/lifecycle-sync.md`, the sources and tests of `markdown-okf-schema-studio-wt-059-b3`, the
requirements guidelines, and the trust-security, toolbar-navigation, theme-zoom, block-editing, rendering-core, myst
and review-annotations requirements of the same worktree. Read-only review: no lint, no build, no test run.

Verdict: REVISE

## What passed

- Structure, mechanical pass over all 186 files: heading equals title everywhere; description equals the Normative
  behavior paragraph everywhere; exactly one SHALL each; at least two scenarios in every SwRS; no placeholder;
  every `derives_from` resolves to an existing StRS; every StRS has at least 3 SwRS (019 has 3, 016 has 3, 009 has 3);
  `derived_by` matches except StRS-016 and StRS-021, whose extra entry is the legitimate cross-scope derivation of
  TRUST-072 and TRUST-073. No backlog id, UX id, inventory id or `F-LIFE` id in a normative sentence. StRS texts carry no
  path, message name, ms or px value.
- Numbers, defaults and texts verified in code: four activation events and `^1.95.0`; the two commands, the
  `$(book)` icon, `resourceExtname == .md` enablement, the palette / Explorer / editor-title entries, the
  `ctrl+k shift+v` / `cmd+k shift+v` keybinding, the custom editor (`*.md`, priority `option`); all six status labels and
  every message text of 006, 010, 013, 022, 026, 051, 063..066, 128..131; 40 ms debounce; 1.5 s overlay delay;
  2 s patch acknowledgement wait; 20 MiB / 500 / 20 000 / 50 bounds; the overlay CSS (fixed, 14 px right, 128 px / 62 px
  top, `pointer-events: none`); 100 ms state throttle; 500 ms echo window with 2 px target tolerance; 50 ranges; 600 ms
  glow with 24 percent wash and 4 px shadow; saved-state bounds (100 indexes, 0..9999, 200, 4096); 200 remembered
  states and 200 Description choices; the group-lock rules (only a group holding the panel only, about 250 ms wait,
  focus commands 1..8, never past the last group); five setting groups and their `order` values (10, 11, 20..22,
  30..33); all setting defaults (incrementalUpdates, scrollPreviewWithEditor, scrollEditorWithPreview on;
  markEditorSelection, doubleClickToSwitchToEditor off).
- Known issues confirmed true in code: LIFE-045 (`isIgnoredWatchPath` splits the whole absolute path,
  `src/session/hostEvents.ts`), LIFE-094 (`isOutsideChange`: a change of the active text editor's document counts as
  typing, `src/core/preview/updatedRanges.ts`), LIFE-099 (the page posts `previewReveal` with activation `click` on a
  single click, `pageInput.ts`; the host gates only `double-click` on the setting, `scrollSync.ts:revealFromPage`),
  LIFE-155 (`session.readOnly` is set once in `createSession`/`switchDocument`; `onTrustGranted` only schedules the
  incoming marks). None is a test gap or a stale description in disguise. No other Known issue is needed in the
  checked behaviours except the one in defect 1.
- Cross-scope citations verified to say what is claimed: BLOCK-206 (flush before an own switch), BLOCK-198 (Refresh
  over an open editor), BLOCK-200 (refresh refused over a block editor), BLOCK-194 (newest waiting render when the
  editor closes), CORE-048/049/050 (glow, skipped glow, reduced motion), CORE-003/004 (source line, end line),
  TOOLBAR-120/121 (Anchor button pairing), TOOLBAR-025 (sticky band), THEME-022 (theme answer to the ready report). None of
  these is archived or deprecated. The ids named in the brief but absent from the files (TOOLBAR-122..133/147..149,
  GFM-028, DIAG-075, MYST-080, FMSCHEMA-059) are not cited by any lifecycle-sync file; MYST-080 (conf.py changes
  refresh the previews they govern), THEME-019/020 (theme change) and TOOLBAR-128..131 (editor-selection mark)
  already cover inventory lines F-LIFE-038, 039 and 068.
- Test names: all 142 quoted test titles and every `test/...` path in the SwRS exist in `test/`
  (`T34`, `PERF-05`, `PERF-11`, `CR 046`, `CR 050`, `STAB-02`, `T43`, `T08` are real titles).
- About 115 of 165 SwRS (70 percent) were read against source or tests; all 4 Known issues and every claim of
  "Untested" in the 076..115 and 134..165 ranges were sampled.

## Defects (24)

1. **SwRS-138, 139, 140, 030 and StRS-018: the claimed restoration of the reading state is dead code.**
   `previewManager.ts:switchDocument` sets `session.state = session.states.get(documentUri)` and then calls
   `rendering.showPending(session, true, ...)`, whose `clearContent` branch runs `preview.state = undefined`
   (`features/rendering.ts:265`). The next `updatePreview` builds its context from `preview.state` (line 381), so the
   state of the document the reader returns to is never applied. `session.states` is read nowhere else
   (`grep states` in `src/session`), so the 200-entry map of SwRS-139 is write-only. The same clearing means the stored
   Description choice (SwRS-140) is applied only when a session is created (`createSession`, line 239), not after a
   switch, and SwRS-030 hides that a replaced session starts with an empty `states` map. SwRS-138's verification note
   even admits the round trip is untested. Fix: rewrite SwRS-138 to the observed behaviour ("When the preview switches
   to a document, the page starts without the reading state it had there; the editor's first visible line is the anchor
   when the preview follows the editor"), add `Known issue: the state remembered for the document is cleared by the
   pending page before the render uses it, so a document the reader returns to does not get its scroll position, focused
   block, selection, open sections or Description state back`, keep SwRS-139/141/142 as the storage contract with a
   Known issue "the remembered states are never read", state in SwRS-140 that the stored choice is read only when a
   session is created, and weaken StRS-018 ("bring back the reading state it had there") to what is true for a restored
   panel and a reopened document, or list the gap as a Known issue in its Rationale. Re-check with one integration test
   (A to line 80, B, back to A) before choosing between "Known issue" and "supersede after fix".

2. **SwRS-099 and SwRS-112 are duplicates.** 099 ("While preview.doubleClickToSwitchToEditor ... is on, SHALL reveal the
   source line of a block that the reader double-clicks outside edit mode") and 112 ("When the reader double-clicks a
   rendered block that is not a link outside edit mode and doubleClickToSwitchToEditor is on, SHALL reveal the source
   line") state the same behaviour with the same gate (`pageInput.ts` `dblclick` handler and `revealFromPage`), the same
   "no reveal in edit mode, not on a link" scenarios. Fix: keep 099 (it owns default, Known issue and the setting
   contract); delete 112 (`okfreq archive`), move its "Setting off: host refuses a previewReveal with activation
   double-click" scenario into 099 or into SwRS-098, and drop 112 from StRS-011 and StRS-013 `derived_by`.

3. **Wrong "untested" claims, SwRS-099, 110, 111, 112.** `test/page/runtimeScroll.test.ts` "executes source and
   preview synchronization across layout changes" (line 662) dispatches a click on a mapped block and asserts a
   `previewReveal` with line 50 and activation `click` (line 741), dispatches `dblclick` with the setting off and asserts
   the activation stays `click` (line 744), builds a harness with `doubleClickToSwitchToEditor: true` and asserts
   `double-click` (line 748), and dispatches `Enter` and asserts activation `keyboard` (line 751). Fixes:
   099 "No test dispatches a dblclick with the setting on" -> "the page gesture is covered by runtimeScroll.test.ts
   'executes source and preview synchronization across layout changes'"; 110 "the page half has no unit test of the
   click" -> same test; 111 "Untested: no test dispatches the key" -> same test (the exclusion list of buttons, inputs,
   links, chips and insert points stays untested); 112 "the gesture is untested" -> same test (if 112 survives).

4. **SwRS-048, 069, 071, 076: four overlapping "patch or whole page" requirements.** 048 (a changed startup setting
   loads a new page document) is the "startup settings" branch of 076 ("other startup settings than the loaded page ->
   new page document", verified by the same test `runtimeContextKey covers the startup settings`). 069 ("same shell,
   document, source file, resource folders and startup settings -> content patch") is the logical complement of 071 and
   076, and its own wording duplicates their conditions. Fix: merge 048 into 076 (add the five setting names and the
   live `showComments` boundary to 076, keep `StRS-013` in its `derives_from`), then keep 069 as the single positive
   statement ("typing ... sends only the new content") that cites 071/072/073/075/076 for the exceptions instead of
   repeating them in its description; or drop 069 and fold its "Typing" scenario into 071. Net: -1 or -2 SwRS.

5. **StRS-LIFE-019 duplicates StRS-TRUST-001 / TRUST-004; the two scopes disagree on whether the behaviour is intended.**
   StRS-LIFE-019 ("A preview outside a trusted workspace is safe to read") is the same use case as StRS-TRUST-001 (read-only
   preview in Restricted Mode or outside every folder) and the read-beyond-the-folder clause is StRS-TRUST-004. Worse,
   StRS-LIFE-019 presents "Granting trust later does not make an already open preview writable" as a design
   rationale, while StRS-TRUST-001 records the same fact as a "Known issue". Decision: trust-security owns the use case.
   Fix: archive StRS-LIFE-019; re-derive SwRS-155 and SwRS-030 from StRS-TRUST-001 and keep them in lifecycle-sync
   (they are session lifecycle, and TRUST-001's Related list already points at them), re-derive SwRS-067 from
   StRS-LIFE-007 and StRS-TRUST-004. In SwRS-155 state the SHALL as the observed behaviour and keep the Known issue
   there only (not also in a StRS). Note: TRUST-007 (resource root of a read-only preview) and CORE-020 are not cited from
   this scope and need no change here; SwRS-127's second scenario ("file outside a folder -> read-only preview rooted in
   its folder") restates TRUST-001/007 and should only cite them.

6. **Message-envelope SwRS that belong to trust-security: SwRS-116, 117, 082, 074, 081 (and 093).**
   TRUST-065 (render-gated page message must name the render the host holds) and TRUST-069 (page-state message must
   name the render) already specify what SwRS-116 specifies ("previewScroll or previewReveal ... does not name the
   document, revision and request the host holds -> SHALL NOT move the editor"); TRUST-060 (page accepts a host message
   only if addressed to it) covers SwRS-117 (stale `sourceScroll`) and SwRS-081 (old identifiers refused after a
   patch); TRUST-061 and TRUST-060 cover SwRS-082 ("patch with stale or malformed fields is ignored") and, for the
   status-line bounds, SwRS-074 (TRUST-061 lists the same limits in its own Criteria note). SwRS-093 (fresh nonce for a
   document loaded from a patched record) is the sibling of TRUST-022/023/024. The lifecycle analyst already wrote
   "The envelope belongs to trust-security" in 074, 082 and 116 and then specified it anyway. Decision: trust-security
   keeps the envelope and the nonce; lifecycle-sync keeps only what changes the lifecycle. Fix: archive 116 and 117
   (cite TRUST-065/069/060 in the scenarios that remain, e.g. SwRS-109 and 100); archive 082 and 074 after adding the
   status-line bounds (500 lines, 20 000 characters, 50 characters severity) to TRUST-061's normative sentence;
   SwRS-081 stays only if reworded as "after a patch the page's identity is the next render's" (a lifecycle fact, one
   scenario) and cites TRUST-060; move SwRS-093 to trust-security. Net: about -5 SwRS.

7. **SwRS-164 duplicates SwRS TRUST-050.** TRUST-050 ("the sanitizer adds source-mapping attributes to mapped
   elements": source file, line, end line, document id, block id, tabindex) and LIFE-164 ("every block with a source
   line carries its source file, line, document id and a block id `source-block-N` ... for every positive integer
   line") describe the same attributes written by `html-sanitizer.ts` (and `mapping/sourceMapping.ts`). TRUST-050
   derives from StRS-TRUST-008 (unsafe HTML), which source mapping is not; LIFE-164 derives from StRS-011/012, which
   is the right use case. Decision: lifecycle-sync keeps the requirement. Fix: add the end line and `tabindex 0` to
   LIFE-164's scenarios (not to the sentence), archive TRUST-050 (or make it a one-line cross-reference), keep
   CORE-003/004 as the source of `data-line`.

8. **SwRS-163 is a security property derived from the wrong StRS.** "Context travels as inert JSON that cannot close
   its script element" (less-than signs escaped, `application/json`) is injection hardening; TRUST-023 explicitly carves
   it out of the nonce rule and points back to LIFE-163, and nothing in trust-security states it. It derives only from
   StRS-LIFE-008 (updates without losing the reader's place), which it does not serve except through its second scenario
   (equal shell keys). CSP itself (script-src, nonce) is TRUST-013..020 and does not conflict. Fix: keep one
   requirement (owner trust-security, derive from StRS-TRUST-006 and 008) for the escaping and the first scenario; keep
   the "two renders share the page shell" scenario in SwRS-162 or 071 where it serves StRS-008.

9. **SwRS-096 duplicates CORE-048 and CORE-050 and bundles five assertions.** The 600 ms single glow is CORE-048,
   "nothing glows under reduced motion" is CORE-050 (SwRS-096's own Scenario 2 only points to it). What is unique is
   the readability check of the visual scenarios v01..v03 (`check_update_glow`): wash, contrast 4.5:1, nothing moves,
   no sideways scroll. Fix: retitle "The update glow keeps the text readable and moves nothing", description "When
   blocks glow after an outside change, the extension SHALL keep the text contrast at 4.5:1 or more, move no element
   and cause no sideways scroll", drop the 600 ms and reduced-motion words (CORE-048/050 own them), keep the three
   visual scenarios as evidence. Note SwRS-095 already cites CORE-048..050; keep that.

10. **SwRS-030: the statement is not what the code does.** `switchDocument` compares `resourceRoot` and `readOnly`,
    not the workspace folder: two read-only previews of files in different directories (no workspace folder at all) also
    get a new session, and two documents of one folder with a different trust outcome do too. The scenario "Other
    folder" is right, the SHALL is too narrow. Fix: "When the preview switches to a document whose resource folder or
    read-only state differs from the session's, ..."; add the scenario "two files outside every workspace folder in
    different directories"; add the Known issue of defect 1 (the replaced session starts with no remembered states).

11. **SwRS-045 (Known issue true, but the scenarios and the Known issue are incomplete).** (a) Scenario "Whole path
    read" says "no render starts for any file of the workspace". Typing in the shown document, its deletion and its
    creation are handled outside `refreshReferencedPath` (`refreshPreview`, `onDidDelete`, `recoverMissingSource`), so
    they still work below a `tmp` folder; only dependency, include, image and sibling events are lost. (b) The ignore
    check sits at the top of `refreshReferencedPath`, so it also skips the linked-target enrichment and the PlantUML
    include notification below it, and `onConfFileEvent` applies it to `conf.py` (MYST-080). The Known issue names none of
    this. (c) Title "below build and tool folders" suggests a relative check; the sentence itself says "a path with one
    of the segments", which is right. Fix: change the THEN to "no render starts for an included file of the
    workspace; the shown document itself still renders when it is edited", extend the Known issue with "link
    enrichment, PlantUML include updates and conf.py changes are skipped the same way", and say "absolute path" in the
    normative sentence. Verification note: "refreshReferencedPath returns before any render" -> "before any
    dependency, enrichment or include handling".

12. **SwRS-121 cites a test that does not cover the claim.** "refresh preserves viewport state while reverse
    synchronization stays disabled" tests the Refresh button message (`previewRefresh` scroll fields), not that the page
    applies `initialAnchor` before first paint. The page half is `test/page/runtimeContentPatch.test.ts`
    (harness `createRuntimeHarness({ initialAnchor: 50 })`, line 954) and the host half `initialAnchorLine` is untested.
    Fix: Method "Unit test test/page/runtimeContentPatch.test.ts (a boot context with initialAnchor 50) covers the page
    half; the host rule (stored anchor, then the editor's first visible line, then none) is untested".

13. **SwRS-036: verification overclaims.** Criteria "The posted message holds the state fields of the snapshot", but
    the cited test "refresh preserves viewport state while reverse synchronization stays disabled" asserts only
    `type`, `scrollTop` and that `sourceLine` is a number. anchorLine, focused block, selected text, open sections and
    Description state are untested; the closing of the link tooltip (`rt.parts.linkTooltip.close()` before the
    check) is unspecified. Fix: say which fields are asserted and which are not; add "and close any link tooltip" or
    state it in a scenario.

14. **Internal ids and non-title labels in scenarios.** SwRS-011 scenario cites "T36" and SwRS-132 cites "STAB-05":
    both are code comments, not test titles, and are internal tags. SwRS-151 ("scenarioPreviewGroupLock, case A")
    cites a case label that does not exist in that function (it has "(a) Leak canary" etc.). Fix: name the test file and
    a real assertion text ("the passed Uri is the active text editor", "two restored panels coexist") and drop the tags.
    (Real test titles with `T34`, `PERF-05`, `CR 046` in 060..095 and 162/163 may stay: they are the exact titles.)

15. **SwRS-088..091: the DOM-morph internals are specified as four products.** 089 (equal blocks pair in document order,
    each kept node once), 090 (page-added nodes and text nodes are never kept) and 091 (a link block has the same key on
    first load and after a patch) specify `contentMorph.ts` mechanics (key function, pairing order); the observable
    behaviour is 088 ("unchanged blocks stay in place with focus, selection, images, diagrams"). 091 is a regression
    guard for a key function. Fix: keep 088 with scenarios "one changed block", "repeated identical blocks (pair in
    document order)", "a link block"; fold 089..091 into it (or keep 090 only if the page-added controls staying out is
    user-visible); `derives_from` StRS-008 unchanged. Net: -2 or -3 SwRS.

16. **SwRS-102, 103, 104 specify one property, "no scroll feedback", three times.** 102 (the page does not report its own
    programmatic scroll), 103 (the host ignores the editor scroll its own reveal caused) and 104 ("the pane the reader moved
    owns the anchor and never receives a scroll back") are the two halves and the umbrella of the same loop breaker. 104's
    SHALL is "never"-shaped and not testable on its own; its second scenario (revisit a line) is another behaviour.
    Fix: keep 102 and 103 (distinct code paths, distinct tests); rewrite 104 as the ownership rule only
    ("When the reader scrolls one pane, the extension SHALL record that pane as the owner of the anchor") with the
    revisit scenario, and drop the "never receives a scroll back" clause that 102/103 already carry. Also SwRS-118
    ("scroll sync works in every mode") restates 100/108/109/113 as a campaign (12 scenarios of
    `scroll-sync-suite.ts`); keep it as the E2E anchor but make its sentence the matrix ("in reading, edit and block
    mode, paired or solo, anchored or independent") and remove the second SHALL (leave the other pane still).

17. **Bundled SHALLs that should be split or trimmed.** (each needs one sentence in `okfreq` terms)
    - SwRS-054: fixed position, polite live region, pointer pass-through and two offsets (128 px / 62 px) in one
      sentence; the live-region half duplicates the pattern of SwRS-059. Keep "fixed, below the toolbar, moves
      nothing"; make the polite announcement a scenario of 059 or 052.
    - SwRS-061: "standalone status page" + "body carries the marker attribute" + "style reads the editor colours
      through neutral tokens" (+ the nonce scenario, which is TRUST-021). Keep the marker and the neutral tokens; cite
      TRUST-021 for the nonce.
    - SwRS-062: replace the page, cancel the queue, keep nothing of the previous document (three effects, one trigger).
    - SwRS-011: open the file as a permanent tab, in another group, and preview it. The group rule holds only when a side
      preview exists (the verification note admits it); put the condition in the sentence.
    - SwRS-119: defines the anchor (editor top line, preview reading line below the band, page top = line 1) in one
      sentence. Keep the definition as is but remove the band geometry that TOOLBAR-025 owns.
    - SwRS-125: 100 ms write limit + "never hold back previewScroll" + flush when hidden.
    - SwRS-153: focus by current position + restore the focus + no command past the last or eighth group. The
      third is a helper guard (`focusGroupCommand`); the product requirement is "unlocking a group never creates a
      group" (already SwRS-152's boundary).
    - SwRS-141: cap of 200 + ignore a malformed stored value.
    - SwRS-134..137 are four SwRS for one parser (`parsePreviewPanelState`); 135..137 are one family of
      "a saved field is kept only inside its bound" and may be one SwRS with three scenarios (guideline: families
      of equivalent assertions map to one SwRS).

18. **SwRS-110 omits a gate, SwRS-098 inverts polarity.** `revealFromPage` requires `scrollEditorWithPreview` for a
    click reveal; 110's sentence ("When the reader clicks a rendered block outside edit mode, SHALL reveal ...") does
    not say so (only 098 does, indirectly). SwRS-098's title ("... is on by default and makes the editor follow the
    preview") describes the on state while its sentence describes the off state ("While ..., is off, SHALL never move the
    text editor"). Fix: 110 "While scrollEditorWithPreview is on, when the reader clicks ..."; 098 title "preview.scrollEditorWithPreview
    is on by default and, when off, the preview never moves the editor" with the sentence unchanged.

19. **SwRS-009 / SwRS-010 / SwRS-019: the Open With tab and the command.** SwRS-009's scenario "Only an Open With tab ->
    reader runs Open Preview to Side on a.md" is reachable from the Explorer (URI argument) but not from the Command
    Palette or the keybinding: with a custom editor active `vscode.window.activeTextEditor` is undefined and
    `openPreview` shows "Open a Markdown file to use Markdown OKF-Schema Studio." (SwRS-010). That is a user-visible
    refusal that neither SwRS records. Fix: in 009 say "from the Explorer menu" in the GIVEN/WHEN; add to 010 a scenario
    "the active tab is a Studio Open With editor: the command from the Command Palette is refused" or record it as a
    Known issue on 010 (if intended as a limitation, say so; the code shows no check for a custom editor).

20. **SwRS-026 and SwRS-050 verification: the pending message is not asserted.** 026's THEN quotes "Following the active
    Markdown editor." and cites lifecycle.test.ts and sourceMapping.test.ts; neither asserts the text (no test contains
    it). 006's note says so; 026's does not. Fix: add "the message text is untested" to 026's Method, as in 006.

21. **StRS-LIFE-006 overclaims the trust and colour-theme clauses.** "When a file, a setting, the colour theme or the
    trust of the workspace ... changes, the Studio SHALL bring that preview up to date" is backed in this scope only by
    files (044, 046), settings (047, 048) and the ignore list (045). Theme is SwRS THEME-019/020/022 (not derived from
    StRS-LIFE-006); trust has no lifecycle SwRS and SwRS-155 says a trust grant changes nothing visible. The
    incoming-change marks that do follow a trust grant are review-annotations SwRS (not derived from StRS-LIFE-006). Fix:
    either narrow the StRS to "a file or a setting" and let theme and trust stay with theme-zoom and
    review-annotations, or add cross-scope `derives_from` to THEME-019/020 and the review-annotations marks SwRS, and
    keep the trust clause as "the incoming-change marks follow".

22. **Other StRS quality items.** StRS-LIFE-013 Rationale "The settings are read when a page loads, so a change
    replaces the page" is implementation (SwRS-048/076); say "A change of these settings reloads the preview page" or
    drop it. StRS-LIFE-012 Rationale "The block that was just edited stays at the same place on the screen after its
    save" has no SwRS in this scope (the pin is BLOCK-228..243); cite it or drop it. StRS-LIFE-016 Rationale ("contributes
    no command with a built-in identifier") is a SwRS (148); StRS-LIFE-015 "Problems entry" and "watcher" are
    implementation words in the Preserved intent ("no render, watcher or Problems entry lingers"): rewrite as "no
    work or warning of that preview lingers".

23. **StRS-LIFE-007 (28 SwRS) and StRS-LIFE-008 (30 SwRS) are too broad; StRS-LIFE-001 (17) and 010 (14) are borderline.**
    007 carries three use cases: render state labels and pending notice (006, 023, 049..061, 085, 087), missing or
    unusable source explained (062..068, 128..131), and the accessibility/markup of the status region (059..061). 008
    carries the in-place update (069..091), its safety fallbacks (072..078, 092, 093) and the page bundle (162, 163).
    Fix: split 007 into "The reader knows the render state of the preview" (SwRS 006, 023, 049..061, 085, 087) and "The
    reader is told why a preview has no source" (062..068, 128..131); split 008 into "The preview updates in place"
    (069..071, 079..091) and "A preview that cannot update in place loads again without losing the place" (072..078,
    092..093) and move 162/163 to a performance or trust StRS. Splitting also removes the need for SwRS that
    carry two StRS only to be reachable (067, 085, 087 each derive from 2 StRS for this reason).

24. **Near-duplicate pairs left after the merges above (keep one).**
    - SwRS-006 (scenario "Source missing", message *The active Markdown source is unavailable.*) and SwRS-063 (default
      reason): the 006 scenario is 063's first scenario. Remove it from 006.
    - SwRS-056 (a new page document removes the pending notice) and SwRS-085 (a patch removes the pending notice):
      different branches of one rule "the notice never survives the update that ends it"; keep both only if the
      sentences name the branch ("whole document" / "patch"); today 056's title omits the branch.
    - SwRS-022 (Open With editor given a document that is not a saved .md) and SwRS-064 ("The restored or active source is
      not a Markdown file"): different message texts, same eligibility test; fine, but state the shared rule once.
    - SwRS-105 / 106 (pairing on visible-editor change / on ready): distinct triggers, keep, cross-reference each
      other.
    - SwRS-160 / 161 (boot context and page defaults) overlap review-annotations' "the host tells the page the
      show-comments value on load" for the comment chip setting; keep one owner for `showComments` (review-annotations)
      and remove it from 160's scenario.

## Inventory F lines not mapped to any SwRS

- F-LIFE-081..084 (host-neutral ports of document store, editor port, panel port, settings and workspace ports) and
  F-LIFE-086 (`*ForTests` hooks): port contracts and test hooks, correctly not requirements; the inventory itself says
  "port contract only". Confirm that `okfreq` exempts them in the coverage report.
- F-LIFE-038 (conf.py refresh), F-LIFE-039 (theme), F-LIFE-047 (patch closes editors, drops deferred updates),
  F-LIFE-048 (render waits for an open editor), F-LIFE-056/057 (Anchor button), F-LIFE-063 (pin after a final save),
  F-LIFE-068 (selection mark), F-LIFE-085 (read-only creation): mapped to other scopes (MYST-080, THEME-019/020,
  BLOCK-148/204/FMEDIT-061, BLOCK-194, TOOLBAR-120..127, BLOCK-228..243, TOOLBAR-128..131, TRUST-001). Not defects; the only
  gap is that StRS-LIFE-006/012 do not list them (defects 21 and 22).
- F-LIFE-016 (flush before a switch, 1.5 s, warning "could not save the text you typed"): BLOCK-206 owns the post
  and the wait; the warning text and the 1.5 s bound are not in any lifecycle SwRS (SwRS-029 cites only the latest-wins
  rule). Add one SwRS "A save the host refuses during a switch shows a warning and the switch goes on" or confirm that
  block-editing already has it (`flushRefusalMessage`).
- F-LIFE-066/067 default-on settings are covered (097, 098); F-LIFE-073 (bundle as resource root) is covered by 162's
  second scenario, which is untested.

## Re-check list for the fixes

- Defect 1 needs an integration or unit check that fixes the truth before the SwRS changes direction.
- After merges, re-run `okfreq update-coverage` and verify that no remaining SwRS lost its only `@tests_req`
  (tests of 112, 082, 116, 117, 074 must move to 099, TRUST-061, TRUST-065/060).
- Expected count after the merges and moves of defects 2, 4, 6, 7, 8, 15 and 16: about 165 - 17 = 148 SwRS in
  lifecycle-sync (+1 for the F-LIFE-016 warning if added), 20 StRS before the split of defect 23 (-1 for StRS-019), 22 after.

## Re-check

Worktree `markdown-okf-schema-studio-wt-059-b3`; read-only; no lint, build or test run. Scope now 22 active StRS
(LIFE-019 archived, LIFE-022 and 023 new) and 154 active SwRS (12 archived; SwRS-166 new).

Verdict: FIX-REQUIRED

### Earlier defects, status

Fixed and checked against the files, `src/` and `test/`: 2 (112 archived into 099), 3 (tests named; the page test
`runtimeScroll.test.ts` "executes source and preview synchronization across layout changes" does dispatch click, dblclick
with the setting off and on, and Enter), 4 (048 into 076, 069 now cites 071..076), 5 (StRS-019 archived; 155 and 030
derive from StRS-TRUST-001; 067 from StRS-022 and StRS-TRUST-004), 7 (164 has end line and tabindex 0 in its scenario;
TRUST-050 archived), 8 (163 and 162 re-derived from StRS-TRUST-006/008, shell scenario in 162), 9, 10, 11, 12, 13, 14,
15 (089..091 folded into 088), 16, 18, 19 (LIFE-010 Known issue, but see defect 6), 20, 21, 22, 23 (StRS-022 and 023
split out), 24. Mechanical pass over the 176 active files: heading equals title, description equals the Normative
paragraph, one SHALL, at least two scenarios, every `derives_from` resolves and is reciprocal, no relative link, no
active requirement of any scope cites an archived LIFE id, every quoted test title and `test/` path exists. As in the
other scopes, active StRS keep archived SwRS in `derived_by` (convention, not a defect). Defect 1 and 6 of the first
round are only partly fixed (below).

### Special checks

- Restore of the reading state, A to B to A, by reading `previewManager.switchDocument` (lines 456..493),
  `rendering.showPending` (265) and `viewState.recordPreviewState` (62..92): CONFIRMED for the remembered state. The
  state of A is stored (481), `session.state` is set from the map (490), then `showPending(session, true, ...)` sets
  `preview.state = undefined` and `preview.stage = undefined`; a late report of the old page is dropped because
  `recordPreviewState` returns when `stage` is undefined; `runtimeContext` takes `preview.state` (rendering.ts 381). No
  other reader of `states` exists. So focused block, selection, open sections and Description state do not come back,
  and the Known issues of 138, 139 and 140 are true for them. NOT confirmed for the scroll position: see defect 1.
- New StRS-022 and StRS-023: the SwRS lists are right and reciprocal; texts carry no implementation. See defect 2 for
  StRS-018.
- SwRS-166: sentence, scenarios and the test "loading ignores a malformed stored value" are right.
- LIFE-074 against TRUST-061: duplicate, see defect 3.
- Fresh nonce for a record loaded as a new document: lost, see defect 4.

### Defects (8)

1. **SwRS-138, 139 (Known issue), 140 (Known issue), 030 (Known issue), StRS-018 Rationale: the Known issue overclaims the
   loss of the scroll position.** `switchDocument` never clears `session.scroll.anchor`. `initialAnchorLine`
   (`features/scrollSync.ts` 207..216) returns the stored anchor first when `anchor.documentId === preview.documentUri`,
   and only then the editor's first visible line. The anchor of A (set by `pageMessages.ts:193` on any scroll, refresh
   or save report, or by an editor scroll at `scrollSync.ts:143`) stays until another document reports its own. So in
   A (line 80), B (no scroll reported by B's page), back to A, the render of A gets `initialAnchor` 80 and the page
   applies it before the first paint (LIFE-121). Only the focused block, the selection, the open sections and the
   Description state are certainly lost; the scroll position is lost only when B reported an anchor in between. The
   normative sentence of 138 and its scenario "Back to A" state it unconditionally, and 030 says "the reading state of
   the documents shown before is lost" although the replaced session reads the stored Description choice in
   `createSession` (previewManager 239). Fix: 138 sentence "When the preview switches to a document, the extension
   SHALL start the render of that document without a remembered focused block, selection, open sections or Description
   state, anchored at the stored scroll anchor of that document when it still has one, else at the editor's first
   visible line when the preview follows the editor"; scenario "Back to A" THEN "the page keeps its scroll line when
   no other document reported an anchor meanwhile, and starts without focused block, selection, open sections and
   Description state"; add scenario "B scrolled in between" (scroll line not kept); Known issue limited to the four
   dropped items; same trim in 139, 140, 030 and in the StRS-018 Rationale; keep the full Known-issue text in 138 only and
   let 139, 140, 030 say "see SwRS-MDOKFSTUDIO-LIFE-138". The integration test A to line 80, B, back to A named in the
   Method is still the right way to settle the scroll half.

2. **StRS-018 no longer matches the SwRS it is derived by.** Its normative sentence now reads "a document that a preview
   showed before the window was reloaded", but SwRS 138, 139, 140 and 141 describe switching documents inside one
   session (and the Known issue in the Rationale does too), and the 200-document map of 139 is not used by a reload at
   all (a restored panel uses its saved state). Fix: either widen the sentence to "When a reader returns to a document
   that a preview showed before, whether after switching documents or after a window reload, the Studio SHALL bring
   back the reading state it had there", or derive 138 and 139 from StRS-LIFE-003 only and keep StRS-018 for 125, 126,
   127-related storage (135, 140, 141, 142, 166).

3. **SwRS-074 duplicates SwRS TRUST-061; decision: trust-security owns it.** TRUST-061 already states, as acceptance
   conditions of `previewContentPatch`, at most 500 diagnostics, a severity of 50, a text of 20 000, a label of 500 and
   a message of 20 000 characters, with "Out of bounds" scenarios; its Related list even points to LIFE-074. LIFE-074
   repeats the 500 / 20 000 / 50 bounds and adds only the code attribute scenario. LIFE-073 (the host does not send a
   patch beyond those bounds, so the whole page loads) is a different behaviour and stays. Fix: archive LIFE-074 with
   "Covered by SwRS-MDOKFSTUDIO-TRUST-061"; add its test `runtimeContentPatch.test.ts` "CR 050: a patch keeps the code of
   each status line and refuses a malformed one" to the Method of TRUST-061; move the scenario "each line keeps its
   code attribute" to SwRS-087; replace the "Related requirements" line of TRUST-061 by a pointer to LIFE-073.

4. **Lost behaviour: a patched record that is loaded as a new document gets a fresh nonce.** SwRS LIFE-093 was archived
   with "Covered by TRUST-022, 023 and 024", but TRUST-022 (a nonce per page it builds) and TRUST-024 (a patch keeps the
   loaded page's nonce in the record) say nothing about the next step: when the record of a patched page is assigned as
   a whole document (2 s fallback of LIFE-077, the recreated webview of LIFE-092), `freshNonceRecord` replaces the
   retained nonce by a new one (`rendering.ts` 206..231, `pageMessages.ts:171`); without it two documents would share a
   nonce. Nobody specifies it. Owner: trust-security (nonce family TRUST-022..024). Fix: new SwRS or a second sentence
   in a new requirement next to TRUST-024: "When the extension loads the record of a patched page as a new document, it
   SHALL give that document a fresh nonce", scenarios "Reload of a patched record" and "Own nonce" of the archived 093,
   test `contentPatch.test.ts` "T34: the record of a patched page carries the nonce of the loaded page and keeps its
   shell". The other three named behaviours are held: a patch with stale or malformed fields is ignored (TRUST-060
   "Older render" and TRUST-061 bounds, the stale-patch test of 082 should join their Method), a stale `sourceScroll` is
   ignored (TRUST-060), a scroll report not naming the current render is dropped (TRUST-069 "Older scroll report");
   a `previewReveal` naming another file stays in LIFE-114.

5. **Lost behaviours of archived TRUST-072 and TRUST-073: nobody specifies them.** TRUST-072 ("no language, grammar or
   editors entry in the manifest") and TRUST-073 ("markdownDescription of at most 700 characters, no plain
   description") are deprecated without an Archived note, while LIFE-148 only states "no command id starting with
   markdown." and LIFE-157 only "a markdownDescription and a unique order". The test
   `test/security/package-contract.test.ts` asserts `contributes.languages` and `contributes.grammars` undefined (lines
   190..191) and `length <= 700` and no `description` (221..223). StRS-016 and StRS-021 still list the two in
   `derived_by`. Owner: lifecycle-sync (StRS-016, StRS-021, package contract LIFE-148/157). Fix: add SwRS-167 "The
   extension contributes no language and no grammar" (derives from StRS-016, scenarios "keys of contributes" and
   "built-in Markdown language untouched", test as named) and SwRS-168 "A setting description has at most 700
   characters and is a markdown description" (derives from StRS-021); give TRUST-072 and TRUST-073 an Archived note
   naming them; remove the deprecated ids from `derived_by` of StRS-016 and StRS-021 if the project drops archived
   entries elsewhere.

6. **SwRS-010: the keybinding cannot reach the refusal.** The scenario "Studio Open With tab active" and the Known issue
   say the command is refused "from the Command Palette or the keybinding". The keybinding (SwRS-017, `when`
   `editorTextFocus && resourceExtname == .md`) does not fire while a custom editor has the focus, and the editor-title
   button is absent (SwRS-016). Only the Command Palette (when `resourceExtname == .md`) reaches `openPreview` with no
   active text editor. Fix: delete "or the keybinding" in the WHEN, THEN and Known issue of 010.

7. **SwRS-054: the title still promises what the sentence dropped.** Title "The pending notice is fixed, announced
   politely and never blocks the page"; the sentence (fixed box, top right below the toolbar, moves nothing, pointer
   pass-through) no longer mentions the polite announcement, which now lives in SwRS-059 scenario 2. Fix: title "The
   pending notice is a fixed box that moves nothing and lets the pointer through".

8. **Duplicate Known issue across scopes (low).** StRS-MDOKFSTUDIO-TRUST-001 Rationale and SwRS-LIFE-155 both record
   "a preview open when trust is granted stays read-only". The first review asked for it in the SwRS only. Fix (trust
   scope file): drop the first bullet of the StRS-TRUST-001 Rationale or replace it by "see SwRS-MDOKFSTUDIO-LIFE-155".

### Cross-scope handoff summary

- Specified nowhere: "a patched record loaded as a new document gets a fresh nonce" (defect 4, trust-security);
  "no languages or grammars contribution" and "setting description at most 700 characters, no plain description"
  (defect 5, lifecycle-sync).
- Held by the receiving scope: stale or malformed patch (TRUST-060, 061), stale `sourceScroll` (TRUST-060), scroll report
  not naming the current render (TRUST-069), source-mapping attributes (LIFE-164 with end line and tabindex),
  flush-refusal warning (BLOCK-209, FMEDIT-069), double-click reveal (LIFE-099).
