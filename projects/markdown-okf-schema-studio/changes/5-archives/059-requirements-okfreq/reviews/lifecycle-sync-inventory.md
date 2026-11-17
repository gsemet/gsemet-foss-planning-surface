Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: inventory lifecycle-sync (LIFE)

Critic P10.1 (Sonnet). Read-only check of `inventory/lifecycle-sync.md` against the checklists,
`tools/scope-map.json` and the refactored code (`markdown-okf-schema-studio-wt-059`).

## Missing rows

Script: all `C-` ids whose scope column is `lifecycle-sync` or `lifecycle-sync?` (48) minus the ids cited in the
F-LIFE table. Uncited: C-PKG-032, C-AR-135, C-AR-149, C-CL-088, C-CL-099, C-CL-106. All six are listed as
moved out in "Checklist corrections", so the target scope must cite them:

- C-PKG-032 -> diagrams: cited by F-DIAG-017, F-DIAG-053 (also in its claimed table). OK.
- C-AR-135, C-AR-149 -> rendering-core: `inventory/rendering-core.md` does not cite them (grep: 0 hits).
- C-CL-088, C-CL-099, C-CL-106 -> frontmatter-schema: `inventory/frontmatter-schema.md` does not cite them (0 hits).

These five are handled only once their target inventory cites them (action on the rendering-core and
frontmatter-schema analysts, or at the P10 cross-scope merge; not a defect of this file). The 14 moved-in rows
are each cited by a named F-LIFE row (checked by grep).

## Missing behaviours

No gap of substance. Small, optional additions:

- `hostEvents.ts:watchStemRoot`: besides stopping on folder removal (F-LIFE-031), the stem watcher invalidates the
  filename-stem index when a `.md` file is created, deleted or renamed, so link resolution stays current
  (cross-scope, frontmatter-schema cites `invalidateStemIndex`).
- `hostEvents.ts:onDocumentClosed`: closing a document clears its Problems entries (F-LIFE-030 only mentions
  clearing on panel disposal).
- `hostEvents.ts:refreshPreview` with an open inline editor and an outside change (`trackOutsideChange`,
  STAB-03/06): block-editing owns it (cited there); F-LIFE-048 could cross-reference.
- `page/pageDiagnostics.ts` (Ctrl/Cmd+A kept in controls, editor keys kept in the page, `__studioDiagnostics`
  trace): cited by block-editing/table-editing, not here; fine, the scope-map lists the file under LIFE, so a
  one-line "owned by table-editing" note would help.
- Restricted Mode / read-only (F-LIFE-085), CRLF (F-LIFE-062 `\n` only), undo (F-LIFE-051), stale (F-LIFE-070)
  are all covered.

## Wrong/unverifiable evidence

Scripted: 361 backticked evidence tokens; all 174 `file:symbol` pairs resolve to an existing file and symbol
(src); 124 `file:test name` pairs checked by grep. 13 INT step labels checked
(`the second lifecycle render`, `the explicitly refreshed dirty render`, `the theme-triggered bounded render`,
`Open With stayed loading while MyST was rendering`, `opening the direct MyST editor disposed ...`, etc.): all exist
in the named suites. Also verified: `"Save or cancel this edit before refreshing."` (pageInput.ts:48),
`"Cannot open ..."` and `"Open a Markdown file ..."` (activation.ts:141/150), T36 and `{ not: "a uri" }`
(lifecycle.test.ts:217/232), `scenarioPreviewGroupLock` (realInput.test.ts), the 11 ignored watch segments
(hostEvents.ts:43), `PENDING_OVERLAY_DELAY_MS` 1500 and `CONTENT_PATCH_ACK_TIMEOUT_MS` 2000 (pageLoadState.ts).

One inexact name: F-LIFE-080 cites `settingsRegistry.test.ts:a setting with nothing stored reads as its default`;
the test is titled "a setting with nothing stored reads as its schema default". Fix the string.

Coverage states checked on the untested rows (F-LIFE-001, 004, 020, 025, 029, 037, 038, 077, 082, 083, 086):
consistent with the tests found.

## Count check

Script on the table: 86 rows F-LIFE-001..086 with no gaps; tested 74, untested 12 (the Counts line is right;
row 018 contains `||` inside backticks, a naive column split mis-reads it); 21 rows flagged `undocumented`;
checklist 48 - 6 + 14 = 56 matches. Counts table matches.

## Verdict

All in-scope rows are cited, evidence is genuine, counts are right. Optional polish: fix the F-LIFE-080 test
name; add the stem-index and document-closed notes; make sure rendering-core and frontmatter-schema cite the five
moved-out rows.

Verdict: APPROVE
