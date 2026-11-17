Ids in this file predate the reduction; see `reduction/mapping.csv`.

# P10.3 critic review: myst SwRS (and StRS)

Scope `myst` (14 StRS, 87 SwRS) in `markdown-okf-schema-studio-wt-059`, against `inventory/myst.md`.

## Mechanical checks (scripted)

- `okfreq validate requirements --prose --check-links --project-root .`: 246 requirements, 0 errors, 0 warnings.
- All 101 files: first `##` heading equals frontmatter `title`; no duplicate titles; no placeholders; every SwRS has
  exactly two scenarios (Nominal, Boundary or refusal), at least one `derives_from`, and every link resolves to an existing StRS.
- Description equals "Normative behavior" text in all files except SwRS-MYST-077 (see D4).

## Coverage of F-MYST (73 rows)

Every F-row maps to at least one SwRS except the two skips.
- F-MYST-018 (`{doc}`/`{numref}`/`{download}`): skip is valid, there is no defined or tested behaviour to state. But
  StRS-MYST-004 promises links to a "document" that no SwRS verifies (D5).
- F-MYST-044 (rename dead click for labels starting `_ . -`): skip is valid, a suspected bug must not become a requirement.
  Advisory: record it in `docs/known-limitations.md` or the requirements log so it is not lost.

## Spot-check against inventory evidence (about 40 of 87)

Checked 001-005, 009-010, 013, 019-020, 025-029, 036-056, 057-062, 066-068, 070-072, 075, 078-086 against the F-row text and
code (`src/session/webview.ts` for the KaTeX-missing boundary of 025). Messages, thresholds (100 chars, 6 s, 5 s, 500, 8 levels,
10 warnings, 2 s), refusal texts and Restricted Mode behaviour all match. No false statement found.

## Defects (blocking)

- D1 SwRS-MYST-065: two behaviours (`{table}` and `{csv-table}`) plus raw HTML table alignment and GFM alignment. Split into
  one SwRS for `{table}` (caption, `:label:` id, `:align:`, GFM alignment, raw HTML table under it) and one for `{csv-table}`
  (`:header:`, quoted multi-line cells, caption, `:align:`), each with its own nominal and boundary scenario (use `okfreq new`).
- D2 SwRS-MYST-069: bundles literal list syntax (quotes, prefixes, comments, continuations, CRLF) with mutation forms
  (`=`, `+=`, `.append`, `.extend`, list addition). Split into two; the boundary scenario today (CRLF, prefixes) does not
  test the mutation clause at all.
- D3 SwRS-MYST-047: two clauses, the remaining-use message and the 5 s auto-close, and the 5 s clause has no scenario.
  Keep the message (counting `{ref}` forms only) in 047 and move the auto-close to its own SwRS with nominal (closes at 5 s)
  and boundary (a new rename or Escape before 5 s) scenarios.
- D4 SwRS-MYST-077: the description was hand-edited and now differs from the body; it leaks the internal id "U17"
  (also in the verification criteria "Wording U17") and never states the actual wording. Put the exact sentence
  ("`<syntax>` is used but this needs the MyST extension `<ext>`, which is not enabled in your conf.py. Add "<ext>" to
  `myst_enable_extensions`.") in the statement, make description and body identical, drop "U17".
- D5 StRS-MYST-004: "label, figure, table or document" but document references are unverified (F-MYST-018 skipped).
  Reword to "heading, figure, table, equation or label" (and keep the SwRS-019 link), or add a testable SwRS for `{doc}`.
- D6 SwRS-MYST-087: implementation detail ("registry", "fail the build", "sanitizer rules", "data attributes"), method
  inspection, and derives only from StRS-001 (admonitions) although it also governs figures and tables. Either rephrase to the
  observable outcome (each directive family renders, styles and offers palette actions under its own name; a duplicate name
  is refused) and add StRS-008 and StRS-013 to `derives_from`, or split per family; do not leave it as an admonition-only link.

## Advisory (non-blocking, fix if cheap)

- SwRS-MYST-071: cache lifetime (2 s, mtime and size recheck) and invalidation on conf.py events are two behaviours.
- SwRS-MYST-058: `:caption:` and `:hidden:` are two behaviours; SwRS-MYST-057 also holds web addresses and file extension
  lookup that appear only in the scenarios, not in the SHALL.
- SwRS-MYST-082 (six banner layout properties) and 081 (content plus Tab order and polite status) are broad; acceptable as
  page-wide families only if the verification notes list each property.
- SwRS-MYST-044: boundary scenario tests the render-gate drop, a different behaviour from the refusal text.

Verdict: REVISE

## Re-check

Verdict: FIX-REQUIRED

- okfreq validate (prose, links): 264 requirements, 0 errors, 0 warnings (the validator does not catch the defects below).
- D1 (065/088), D2 (069/089), D3 (047/090), D4 (077: description identical to body, no "U17" anywhere), D5 (StRS-004 body and
  description both read "heading, figure, table, equation or label", consistent), D6 (087 rephrased, 091/092/093 added, 093 derives
  from StRS-001/008/013): fixed in content. Spot-checked 019, 033, 052, 060, 066, 071, 075, 082 and 088-093: faithful, two scenarios each.

Defects (blocking, file corruption):
- SwRS-MDOKFSTUDIO-MYST-065.md line 27: the normative sentence is truncated at "its `:align:`, k" and the heading `### Scenario: Nominal`
  is glued onto the same line (no blank line, no heading). Frontmatter description is complete ("keeping GFM column alignment on
  every cell"), so body and description differ. Restore "eeping GFM column alignment on every cell." and put a blank line plus
  `### Scenario: Nominal` on its own line.
- SwRS-MDOKFSTUDIO-MYST-069.md line 27: sentence ends "...line ending.### Scenario: Nominal" on one line; heading not on its
  own line. Insert a blank line and a separate `### Scenario: Nominal` heading.
- Re-run a scan for `.+### ` in tiers/*/myst/*.md after the fix (only 005 line 37 is legitimate).
