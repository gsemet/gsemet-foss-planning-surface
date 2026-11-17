Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Review: trust-security inventory (P10.1 critic)

Scope `trust-security`, inventory `inventory/trust-security.md` (73 behaviours), code at `c166165`.

## Missing rows

22 checklist rows carry scope `trust-security` (scripted grep of `checklists/*.md`). All 22 ids appear
in the inventory. Handling check of the 7 rows listed in "Checklist corrections":

- C-CL-075, C-CL-087: `n/a` (tooling, CI process) with reasons; acceptable.
- C-CL-024 moved to `myst`: `inventory/myst.md` cites it. Handled.
- **C-CL-008, C-CL-009 moved to `review-annotations`: `inventory/review-annotations.md` does not cite
  them** (it cites C-CL-002, 007, 010, 015, 029-031, 034-036, 080, 089, 091, 095, 102 only).
- **C-CL-014, C-CL-020 moved to `palette-slash`: `inventory/palette-slash.md` does not cite them.**
- Kept rows C-CL-082, 083 and C-AR-138, 139 (PlantUML) are cited in `inventory/diagrams.md`. Handled.

Four rows are therefore handled by nobody (the checklist still labels them `trust-security?`).

## Missing behaviours

None of substance (fewer than 3). Minor, optional additions:

- `resource-policy.ts:relativeResourcePath` (posix separators for page URLs) and
  `resourcePathPart`/`resourceReferenceSuffix` trimming are not stated.
- Sanitizer: a kept `<script src>` is walked for children after getting nonce (no behaviour change).
- `hostMessages.ts` has no origin check: noted in F-TRUST-065. Restricted Mode, read-only,
  standalone, stale, CRLF-free scope: all present. CRLF and undo do not apply to this scope.

## Wrong/unverifiable evidence

31 claims spot-checked by grep in the code root; all exist: `readOnly =` in `previewManager.ts`,
`EDIT_REQUEST_TYPES`, `PAGE_MESSAGE_GATES`, `reportStaleEdit`, the seven refusal strings, `the
standalone document directory` (links.ts), `onDidGrantTrust`/`onTrustGranted`, `freshNonceRecord`,
`reuseNonce`, `sameResourceRoots`, `scenarioUntrustedReadOnly`, `READ_ONLY_NO_HOVER_ASSERTIONS`,
`ASSERTION_ONLY_IDS`, capture id `r01-untrusted-read-only`, `warningsInProblems`, `jar-untrusted`,
`allowSchemaResolution`, `allowExternalScripts`, and the tests `the trust gate prevents renderer
invocation...`, `canPatch refuses next content...`, `PERF-11...`, `every page message type has one
handler` (asserts 41 types), `removes refresh metadata...`, `CR 050 ... banner`, `no user-facing
string literal mentions Sphinx`. Coverage claims confirmed: `sanitizeCss`/`stylesheetRelativePath`
have no caller outside `html-sanitizer.ts` (F-050 dead code true); `webview.ts:186` says "Refuses
linked stylesheets outright" (F-049 true); `userFacingText` scans only `src/extension.ts`,
`src/session/webview.ts`, `src/core/render/*.ts` (F-068 true); `package.json` has no `capabilities`
(F-069 true); `mystDiagnostics.test.ts:runUntrusted` exists. No false evidence found.

## Count check

Table rows 73; by Cov. column: tested 58, untested 14, doc-only 1; "undocumented" in Notes: 34. Matches the
Counts table (73/58/14/1/34). Checklist "15 cited + 7 moved / 22": 15 kept-and-cited + 5 moved + 2 n/a;
the "7 moved" lumps the 2 `n/a` rows with the 5 moved ones (cosmetic).

## Verdict

Real gap: 4 rows (C-CL-008, C-CL-009, C-CL-014, C-CL-020) moved away but not cited by the target
inventories. Fixes (any one per row):

1. Have `review-annotations` cite C-CL-008, C-CL-009 and `palette-slash` cite C-CL-014, C-CL-020; or
2. keep them here: cite each in F-TRUST-008 (and F-TRUST-006 for C-CL-009) and drop them from "Checklist
   corrections".
3. Optionally reword the Counts cell to "15 cited + 5 moved + 2 n/a / 22".

Verdict: REVISE

## Re-check

- Fixes: C-CL-008/009 are now kept and cited in F-TRUST-008 (and F-TRUST-006 for 009); C-CL-014/020 are cited in `inventory/palette-slash.md` (F-PALETTE-093/096, 039/064); C-CL-024 in `inventory/myst.md`; Counts cell reworded to "17 cited + 3 moved + 2 n/a / 22".
- Checklist: all 22 ids with scope trust-security are cited in an `| F-` row or listed in Checklist corrections (C-CL-075, 087 n/a; 014, 020, 024 moved and cited by target F-rows).
- Spot-check of 8 evidence claims by grep (readOnly =, EDIT_REQUEST_TYPES, reportStaleEdit, onDidGrantTrust, freshNonceRecord, scenarioUntrustedReadOnly, allowExternalScripts, no `capabilities` in package.json) and every cited src/test path exists (only globs unmatched, by design).
- Counts: 73 rows = 58 tested + 14 untested + 1 doc-only; 34 undocumented; all match the table.

Re-check verdict: APPROVE
