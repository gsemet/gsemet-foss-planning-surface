Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: trust-security StRS and SwRS

Scope `trust-security`: 14 StRS, 78 SwRS (TRUST-001..078), reviewed against `inventory/trust-security.md`, the
sources and tests of `markdown-okf-schema-studio-wt-059-b3`, the installed VS Code 1.143.1 (workbench and extension
host bundles, for the two claims that depend on VS Code), and the defect classes of the earlier reviews. Read-only
review: no lint, no build, no test run.

Verdict: REVISE

## What passed

- Structure: heading equals title and description equals the Normative behavior paragraph in all 92 files (two
  apparent differences, SwRS-043 and 057, come from YAML quoting only); no leftover placeholder; no backlog id, UX id
  or inventory id in any normative sentence or scenario (PERF-11, T34, CR 025, CR 050, STAB-03 appear only inside
  quoted test titles of Verification notes, where they are real). `derived_by` and `derives_from` are consistent.
- Numbers and texts verified against code: nonce 18 bytes = 24 base64url characters; 4096 document id; 17 render-gated
  types (exactly those of `PAGE_MESSAGE_GATES`; 41 types in all); 100 000 pin bound; afterField 1..1024; four decode
  rounds; 20 MiB, 500 and 20 000 patch bounds; six patch statuses; 18 settings; `@plantuml/core` 1.2026.9; Node 24;
  logo.png 256 x 256; the 12 CSP directives; all diagnostic codes named in 011, 025..034, 036..046 and 051.
- Known issues confirmed true in the code: SwRS-002 (`buildPreviewWebviewHtml` calls `renderPropertiesTable` with the
  default `editingEnabled = true`; only `patchPropertiesTable` passes `!preview.readOnly`, after the debounced link
  pass), 041 (diagnostic code reused), 045 (`webview.ts:processStylesheet` records "Ignored a linked stylesheet" but the
  sanitizer keeps the link; comment says "Refuses ... outright"), 048 (`rewriteNode` is a deny-list; `base` and unknown
  attributes pass), 060 (`hostTransport.ts:onMessage` does not look at `event.origin` or `event.source`), 071 (see defect 1:
  true, and checked in the VS Code source).
- Verification notes: all ~45 test titles named were grepped and exist (html-policy, resource-policy, userFacingText,
  package-contract, pageToHost, pageStateMessages, hostToPage, hostMessages, contentPatch T34, previewRuntimeFile PERF-11,
  previewManager "every page message type has one handler"); the scenario ids v01..v03 and r01 exist. "Untested" claims
  sampled (CSP font/media/connect/base directives, createNonce, missing-root, blocked-srcset, blocked-script-resource,
  blocked-active-element, dispatcher gates) are all true: no test asserts them.
- Owner-scope claim of F-TRUST-062 holds for 36 of the 41 page message types: each has a bound and a refusal in an
  owner SwRS (CODE-026, TOOLBAR-013/058/083/126/135, THEME-013/052, PALETTE-009/172/194..202, MYST-051, REVIEW-069..071/178,
  BLOCK-236/240..245, DIAG-050, GFM-027). Read-only refusals exist for every message that must refuse (BLOCK-121/181/224,
  FMEDIT-051, GFM-026, MYST-042, REVIEW-132/180, PALETTE-187/191/194/200); the host's silent ignore of
  `previewPaletteModeChanged` and `previewEditModeChanged` in `viewState.ts` is implied by the conditional "writable"
  wording of PALETTE-009 and BLOCK-011. Message types without an owner bound: only `previewWarningBannerClosed` (defect 9);
  `previewShowProblems` carries no payload.
- Spot-check of cited external ids (31 distinct ids checked against their description): all exist, all are `draft`
  (none archived or deprecated), 30 say what is claimed (LIFE-155, 030, 072, 093, 116, 163; BLOCK-008/013/017/121/181/
  223/224/244/245; FMEDIT-001/051/052; GFM-026/027/032/033/034/036/038; CODE-025/026; TOOLBAR-002/016/076/083/085/093/
  097/115/116; THEME-015/054; REVIEW-130/132/180; MYST-025/032/042/051; DIAG-024/026/050/091; CORE-003/004/018/041/044/056).
  One gloss is imprecise (defect 13).
- CORE-066 is cited (052, 065), not restated. 065's scenario line "dropped, with no answer and no change" is the stale
  case, which CORE-066 does not cover; acceptable.

## Defects (13)

1. SwRS-071, StRS-001, SwRS-001, SwRS-007, SwRS-011: Restricted Mode is claimed beyond the evidence; the Known issue is
   true but under-reported. Evidence: `package.json` has `"main": "./out/bundle/extension.js"` and no `capabilities`;
   VS Code 1.143.1 `getExtensionUntrustedWorkspaceSupportType` returns `false` for such a manifest (checked in
   `workbench.desktop.main.js`: `!e.main` is the only `true` path, then configured, product override, the manifest
   value, product default, else `false`). A packaged Studio is therefore disabled in Restricted Mode unless the user or
   product overrides it. Yet StRS-001 (title, user_need), SwRS-001 and 007 (scenarios "Restricted Mode"), 011, README:203,
   CHANGELOG:82 and `package.json:232` (useJar text "it also works in Restricted Mode") state it as working. No
   test or doc says otherwise: `untrusted-suite.ts` loads from the development path, `package-contract.test.ts` never reads
   `capabilities`, `docs/security-evidence.md` is silent. Further faults of 071: (a) the Known issue sentence "the read-only
   preview of this scope is reached only through that override" is too wide, a standalone file in a trusted window does not
   need it; (b) the SHALL "declare no capabilities entry" freezes the cause and is not a use case; (c) scenario 2 specifies
   VS Code's behaviour ("VS Code applies its default"), not the product; (d) derives_from StRS-001 although it contradicts
   it. Fix: keep the SHALL (current state) but drop scenario 2 for "GIVEN package.json / WHEN read / THEN no capabilities
   key"; narrow the Known issue to "the Restricted Mode case"; add a one-line Known issue to SwRS-001, SwRS-007 and the StRS-001
   rationale ("with a packaged VSIX, VS Code disables the extension in Restricted Mode unless overridden, see SwRS-071");
   list README:203, CHANGELOG:82 and `package.json:232` as unsupported statements in 071 (backlog: decide the capability
   declaration).

2. SwRS-019 (and StRS-006 rationale): false in the real product. The SHALL "SHALL NOT put a wildcard source ... in any
   directive" and the Criteria "The policy text holds no asterisk" are only true for the fake `cspSource`
   (`vscode-webview://unit`) of `html-policy.test.ts:186`. `vscodeHost.ts:assets` passes `webview.cspSource` through, and the
   VS Code 1.143.1 extension host defines it as `'self' https://*.vscode-cdn.net` (`extensionHostProcess.js`), so
   img-src, style-src, font-src, media-src and script-src of every real page contain an asterisk host wildcard.
   `trusted-suite.ts:83` only forbids `unsafe-inline` and `default-src *`. Fix: SHALL "... SHALL NOT put a bare wildcard
   source, unsafe-inline or unsafe-eval in any directive"; scenario 1 keeps the fake source; add a Known issue: "the
   webview source VS Code supplies is `'self' https://*.vscode-cdn.net`, a subdomain wildcard of the webview origin; the
   policy text of a real page therefore holds an asterisk (deduced from VS Code 1.143.1)"; Criteria "no source `*`".

3. SwRS-069: incomplete exception list. `pageMessages.ts:handlePageState` handles a `previewReady` before the render check
   (`reportsReloadedDocument`: reload of the current document with a fresh nonce; and `armContentPatchFallback` for an
   older request of a patch chain) and only then calls `matchesCurrent`. The SHALL "drop it, except the save or cancel of
   the block editor ..." is false for these two `previewReady` reports. LIFE-092 owns the reload but 069 does not cite it.
   Fix: "... SHALL drop it, except the ready reports of SwRS-MDOKFSTUDIO-LIFE-092 and the save or cancel of ...", add LIFE-092
   to Related requirements, and add the patch-chain case to LIFE-092 or to a note here.

4. SwRS-048, Criteria: wrong cross-reference. "removed or rewritten only by a rule named in SwRS-036 to SwRS-050" omits
   rules of this scope that are outside the range (033 src/poster/data, 034 srcset, 035 alt) and rules of other scopes
   (directive attribute rules `data-okf-width`: LAYOUT-026/027, MYST-033; `data-okf-color` and span style: GFM-034;
   table style: GFM-032). Fix: "... only by a rule of SwRS-033 to SwRS-047 or by SwRS-GFM-032, SwRS-GFM-034, SwRS-LAYOUT-026
   or SwRS-LAYOUT-027" (049 and 050 add attributes and remove nothing).

5. SwRS-078, StRS-014: title and parent overclaim. Title "The packaged extension ships the webview bundles" and StRS-014
   "SHALL ship the bundles the preview loads", but the SHALL covers only `plantumlPreview.js`, and the test
   (`package-contract.test.ts`, last test) checks `esbuild.mjs` text and that no `.vscodeignore` line starts with `out/bundle`
   or `out/**`. `preview.js`, `preview.css`, KaTeX and Mermaid bundles are not asserted (the note admits it; LIFE-162 only
   requires the page to load them). The SHALL also bundles two obligations (build writes; package does not exclude) and
   specifies a build script path. Fix: one SHALL "The package SHALL NOT exclude the folder out/bundle", title "The package
   keeps the out/bundle folder", drop the esbuild scenario (or move it to Verification), and reword StRS-014 accordingly
   (single SHALL, see defect 6).

6. Bundled SHALLs. (a) StRS-014 has two SHALL ("SHALL use the pinned ... and SHALL ship"); (b) SwRS-051 has two ("SHALL record"
   and "SHALL NOT show"); (c) SwRS-074 two (declares icon; file is a PNG 256 x 256); (d) SwRS-073 bundles "limit to 700" and
   "no plain description"; (e) SwRS-057 lists 12 field/type pairs in one SHALL (478 characters) and SwRS-058 five types with
   two target forms; (f) SwRS-011, 033, 034, 036..040, 044..046 each add "and record the diagnostic <code>", a second
   obligation observable only through `testHooks.ts` (SwRS-051 itself says the user never sees it). Fix: split (a) (b) (c)
   (d) into one SwRS each (or one SHALL each in the StRS); split 057 per type family (pin pair; insertAfterLine; the
   frontmatter-save fields; checkbox fields; flush/final/blockEditOpen), 058 into block edit and frontmatter save; for
   (f) keep the removal in the SHALL and move the code to the Criteria line (or to one SwRS "each removal is recorded with
   its code" derived from 051).

7. SwRS-055: circular and mechanism-level. "SHALL accept it only if the validator registered for its type accepts the message"
   specifies the table, not a behaviour; its only scenario (previewHistoryGo direction) duplicates TOOLBAR-058, and the
   per-type bounds are in the owner SwRS. Fix: either delete 055 (move the sentence to the StRS-009 rationale, which already
   says "the bounds of each message kind are specified with the feature that sends it") or restate as "When the host
   receives a page message with a field outside the bounds of its type, it SHALL drop it" with the owner ids in Related.

8. Cross-scope duplicates and misplacement (brief: lifecycle-sync, rendering-core). (a) SwRS-072 (no language, grammar or
   editors contribution) derives from StRS-LIFE-016, belongs with LIFE-018/148/149 and the same package-contract test:
   move to lifecycle-sync; its subject is wrong ("VS Code ... SHALL find no contribution"; the extension is the subject) and
   scenario 2 (search for `markdown.` in all contributes values) is stronger than the SHALL (LIFE-148 covers command ids only).
   (b) SwRS-073 derives from StRS-LIFE-021 and duplicates LIFE-157 (same test "every contributed setting is explained with a
   markdownDescription and a unique order"): keep in lifecycle-sync, merge the 700 limit into LIFE-157, delete 073 here
   (inventory F-TRUST-073 itself says so). (c) CORE-020 ("read-only with the resource root reduced to the document's folder")
   restates TRUST-001 and 007: keep TRUST-001/007 in trust-security and reduce CORE-020 to the render-succeeds half; its
   own note says trust belongs to a trust-security StRS. (d) TRUST-011 cites CORE-021 as "the render refusal when trust is
   required"; production always passes `allowUntrusted: true` (`previewManager.ts:296`), so that guard is unreachable (CORE-021
   says so): drop the cite. No duplicates found with the other three batch-4 scopes beyond these (LIFE-072/093/116/155/163,
   DIAG-002/028/050/091, MYST-086, REVIEW-130/132 are cited complements, not copies).

9. Missing coverage. (a) `previewWarningBannerClosed`: the host accepts it only with `key` of at most 32 characters matching
   `^[0-9a-z]+-[0-9a-f]{8}$` (`pageToHost.ts`); MYST-084 only says the key is sent and TRUST-067 only gates the document. No
   SwRS states the bound. Add it to MYST-084 or to a new SwRS here. (b) F-TRUST-040 and F-TRUST-016, `{include}` half: the shared
   reader `readBoundedText` refuses a Markdown `{include}` over 5 MiB (`too-large`) or unreadable (`renderPipeline.ts:195`);
   only the PlantUML half exists (DIAG-059, DIAG-070). CORE-012 says "a trusted document" while the code also reads includes in
   Restricted Mode from the document's folder, and `docs/known-limitations.md:37` says "only when the workspace is trusted": a doc/code
   disagreement recorded in the inventory notes but in no SwRS or Known issue. Add one SwRS (rendering-core or here) for the
   5 MiB / unreadable refusal and a Known issue on CORE-012 or TRUST-007. (c) SwRS-061 states 5 bounds but not the
   diagnostics array it validates (`isValidContentPatch`: at most 500 entries, severity at most 50, text at most 20 000, code at
   most 100 when present); LIFE-074 omits the `code` bound. Add "diagnostics" to 061 or complete LIFE-074. Also 061's
   "a finite initialAnchor and initialPin" is loose: initialPin needs finite `line` and `viewportTop`.

10. Known issue hygiene. SwRS-041: the Known issue concerns a diagnostic code visible to the test hook only (the Known issue
    says so; SwRS-051 says the reader never sees it): that is an internal wart, not a behaviour defect; fold it into
    Verification notes. SwRS-060: true, but states no consequence or mitigation; add "the page then accepts a message posted by
    any script of the page window; the content security policy (script-src with nonce, frame-src none) leaves no other
    sender (deduced)", cite `hostTransport.ts:createVsCodeTransport`. SwRS-002 Verification notes say "the Known issue below"
    but the Known issues section is above them.

11. SwRS-020: (a) "remove every Content-Security-Policy meta element the page already has" is wider than the code: it filters
    the direct children of `head` only (`injectContentSecurityPolicy`); write "of the head". (b) Scenario 2 ("No head") tests
    a branch the Verification note itself calls unreachable ("cannot arise after parsing"; parse5 always builds a head); remove
    the scenario.

12. StRS leaks and non-use-cases. StRS-009 and 010: user_need "As a security reviewer, I rely on the extension to act only on
    known, well-formed ... requests of its own preview page" and the normative text speak of messages, kinds and bounds
    (protocol internals), and no reader or writer sees them. Reword at user level ("what the preview page asks of the
    extension is checked before anything changes", "an answer meant for another document or an older page never reaches my
    page") and keep message vocabulary in the SwRS. StRS-012 rationale "The check scans the string literals of three source
    locations only" is test detail; move to SwRS-070 (where it already is). StRS-014 "pinned Node.js version", "official npm
    registry" are implementation terms; acceptable only as maintainer need, but see defect 6(a).

13. SwRS-042, Related requirements: the gloss of TOOLBAR-090 "an anchor is a hash followed by non-space characters" differs
    from the text of TOOLBAR-090 ("at least one character and no space, # or ?"). Use the TOOLBAR-090 wording. Same SwRS: the
    Criteria sentence on `xlink:href` is a different rule than the SHALL (which says `href`); say `href` in the SHALL and
    keep xlink in a separate sentence or in 044.

## Re-check

Scope re-checked in `markdown-okf-schema-studio-wt-059-b3`: 14 StRS, 88 SwRS (TRUST-001..088; 050, 055, 072 and 073
archived, `lifecycle: deprecated`). Read-only: no lint, build or test run.

Verdict: FIX-REQUIRED

### Earlier 13 defects

Fixed and verified against src/ and test/: 1 (071 narrowed, Known issue added to 001, 007, 011 and StRS-001; claims
README:203, CHANGELOG:82 and package.json:232 listed), 2 (019 now "bare wildcard", Known issue on the
`'self' https://*.vscode-cdn.net` source), 4, 5 (078 is one SHALL), 6 (b, c, e, f; 057 split into 081..085; 051/079 and
074/080 split), 7 (055 archived), 9 (086, 087, 088, 061 now holds the diagnostics bounds, which I checked against
`isValidContentPatch`: 500 entries, severity 50, text 20 000, code 100, label 500, message 20 000), 10, 11, 12 (StRS-009,
010 and 012 reworded), 13. Partly fixed: 3 (see defect 4), 6(a) (see defect 7), 8 (a, b: archived but the behaviour
is lost, defects 1 and 2; c: defect 6; d done: TRUST-011 no longer cites CORE-021).

Checks that passed in the revision: heading = title and description = normative sentence in all 102 files; one SHALL per
SwRS and StRS; `derives_from` and `derived_by` consistent in both directions for all 14 StRS and 88 SwRS; no active
trust-security requirement cites an archived id in its own text (only the StRS-TRUST-008 and 009 `derived_by` lists name
050 and 055, which is the convention used by the other archived ids, for example LIFE-048); no cited external id is
archived (LIFE-092 and LIFE-072 are draft); the new 079..088 match the code (`pageToHost.ts:hasValidStateFields`,
`isEditRequest`, `previewWarningBannerClosed` regex and `MAX_WARNING_KEY_LENGTH` 32, `readBoundedText` refusals
`too-large` and `unreadable`, `resolveInclude` returning undefined).

Known issues checked: 088 is TRUE. `previewManager.ts:246` sets `resourceRoot = readOnly ? documentDirectory : workspaceFolder`,
`renderPreviewDocument` is called with `allowUntrusted: true` (line 296) and builds the include policy from
`path.dirname(document)` and that root, so includes are read in Restricted Mode and for a file outside the workspace;
CORE-012 ("a trusted document") and `docs/known-limitations.md` ("supported only when the workspace is trusted") say the
opposite. It is a real doc/code disagreement, correctly worded, no change needed. 019 (cspSource), 071, 002, 045, 048,
060 are true. No test-gap item is labelled Known issue.

### Defects

1. LIFE-157 / StRS-LIFE-021 (lifecycle-sync must hold it): the 700-character limit of a setting description and "no
   plain description" are now specified nowhere. TRUST-073 is archived and LIFE-157 only requires a non-empty
   markdownDescription and a unique order. The behaviour is enforced and tested:
   `test/security/package-contract.test.ts:221` (`length <= 700`) and `:223` (`property.description` undefined);
   DIAG-076 and DIAG-077 repeat the 700 only for their own settings. Fix: add to lifecycle-sync one SwRS "A setting
   description has at most 700 characters" (SHALL: every contributed setting's markdownDescription has at most 700
   characters; second SwRS or scenario for "no plain description", one SHALL each), derived from StRS-LIFE-021, with the
   test "every contributed setting is explained with a markdownDescription and a unique order" in Verification notes.

2. StRS-LIFE-016 (lifecycle-sync must hold it): "the package contributes no language, grammar or editors entry" (TRUST-072,
   archived) is specified nowhere: LIFE-148 covers command identifiers only, LIFE-018 the custom editor, LIFE-149
   settings. Tested in `package-contract.test.ts:190-192` (`contributes.languages`, `.grammars`, `.editors` undefined).
   Fix: one SwRS in lifecycle-sync, "The extension SHALL contribute no language, grammar or editors entry", derived from
   StRS-LIFE-016, scenario GIVEN package.json / WHEN contributes is read / THEN none of the three keys exists. Then
   StRS-LIFE-016 and 021 `derived_by` stop pointing at TRUST-072 and 073 only (they may keep them as archived).

3. TRUST-022/024 (trust-security must hold it): "a record of a patched page gets a fresh nonce when it is loaded as a new
   document" is specified nowhere. LIFE-093 (archived) said "Covered by TRUST-022, 023 and 024", which is false:
   022 says a nonce is drawn "for every page it builds", 024 says a patch keeps the loaded nonce. The reload of the record
   is `rendering.ts:freshNonceRecord` (called from `setPanelHtml` and from `pageMessages.ts:handlePageState` when a
   re-created webview reports ready), which gives the record a new nonce so that no document reuses the nonce of an
   earlier one; it is a security rule. Tests: `contentPatch.test.ts` "T34: the record of a patched page carries the nonce of
   the loaded page and keeps its shell" and "T34: reuseNonce swaps every occurrence". Fix: new SwRS in trust-security
   (derived from StRS-TRUST-006): "When the extension loads the record of a patched page as a new document, it SHALL
   replace the nonce of the record by a fresh one first", scenario 1 reload of a patched record (THEN the nonce differs
   from every earlier nonce), scenario 2 a record with its own nonce keeps it; add it to 022's Related requirements.

4. SwRS-TRUST-069, SHALL: two inaccuracies. (a) The exception list names only LIFE-092; `handlePageState` also handles,
   before the render check, a `previewReady` for an earlier request of a patch chain (`armContentPatchFallback`), which is
   specified in LIFE-078, not LIFE-092. (b) "SHALL drop it" is false for a stale previewEditSave, previewEditCancel and
   previewFrontmatterSave: `reportStaleEdit` answers them with an error (the Criteria line and BLOCK-223/FMEDIT-052 say so,
   the SHALL contradicts them). Fix: "... SHALL drop it without changing anything, except the ready reports of
   SwRS-MDOKFSTUDIO-LIFE-078 and SwRS-MDOKFSTUDIO-LIFE-092, the save or cancel of the block editor the host has open for
   exactly the render that message names, and the stale save, cancel or frontmatter save that BLOCK-223 and FMEDIT-052
   answer with an error"; add LIFE-078 to Related requirements and drop the patch-chain sentence from the Verification
   note (it stays as the Method).

5. LIFE-164 (lifecycle-sync must hold it): the sanitizer behaviour of the archived TRUST-050 is only partly kept.
   `html-sanitizer.ts:injectSourceMappings` gives every mapped element that is not naturally focusable and has no
   tabindex `tabindex="0"` (tested for h1 and p: `html-policy.test.ts:106-107`, `sourceMapping.test.ts:53,58`), and sets the
   end line to the line when `data-end-line` is absent, smaller than the line or not a positive integer
   (`html-policy.test.ts:107`). LIFE-164 says the keyboard access applies to "a figure directive" only and names the end line
   for an admonition only. Fix: change the LIFE-164 SHALL or add a second SwRS: "every mapped element that is not naturally
   focusable SHALL be keyboard-focusable (tabindex 0)" and "the end line of a mapped element SHALL equal its line unless a
   valid end line not before the line is given", with the two tests above.

6. CORE-020 duplicates TRUST-001 and TRUST-007 (decision: archive CORE-020). Its two halves are "read-only" (TRUST-001) and
   "resource root reduced to the document's folder" (TRUST-007); its boundary scenario (an include outside the folder is
   refused with a warning) is CORE-018 plus TRUST-088. Citations: TRUST-001 Related, TRUST-007 Related, StRS-CORE-001
   `derived_by`, rendering-core index; nothing else. Fix: archive CORE-020 (`lifecycle: deprecated`, "Archived: covered by
   SwRS-MDOKFSTUDIO-TRUST-001, TRUST-007 and TRUST-088"), remove its line from the Related requirements of TRUST-001 and
   TRUST-007 (leave StRS-CORE-001 `derived_by` as for the other archived ids), and add to TRUST-001 scenario 2 "THEN the
   preview is read-only and shows the rendered document", so the "still renders" half survives. CORE-021 (refusal of the
   render when trust is required) stays rendering-core's, its unreachable guard being its own Known issue.

7. StRS-TRUST-014 still bundles two obligations (earlier 6a): "SHALL be built from pinned, official dependencies and keep in
   its package the bundles the preview loads". Children 075..077 are the first, 078 the second. Fix: one SHALL; move 078
   under a separate StRS (new StRS-TRUST-015 "The package keeps what the preview loads") or under a lifecycle-sync package
   StRS, and give StRS-TRUST-014 only the pinned and official dependencies; adjust `derives_from` of 078 and `derived_by`
   of both.

8. Hygiene in the revision. (a) SwRS-TRUST-019 Known issues entry has no "Known issue:" prefix (all others have it), so a
   grep or lint for the label misses it: start the line with "Known issue:". (b) SwRS-TRUST-071 scenario "Top-level keys" is the
   same test as scenario "Manifest" (no capabilities key): delete it. (c) SwRS-TRUST-057 Verification Criteria still lists
   insertAfterLine and afterField bounds, which now belong to 081 and 082: cut the sentence after "100000 in absolute
   value".

### Behaviour now specified nowhere, by scope

- lifecycle-sync: 700-character setting description and no plain description (defect 1); no languages, grammars or editors
  contribution (defect 2); tabindex 0 of every mapped element and the end-line default (defect 5).
- trust-security: fresh nonce of a patched record loaded as a new document (defect 3).
- Checked and held elsewhere: "a patched page's identity is the next render's" (TRUST-060 scenario 2), "patch with stale
  or malformed fields ignored" (TRUST-060 for the addressing, TRUST-061 for the fields; scenario of 060 uses themeChanged,
  not a patch, acceptable), "scroll report not naming the current render ignored" (TRUST-069 scenario 1, previewReveal
  of another document falls under the same sentence), "source scroll for another render ignored by the page" (TRUST-060).

