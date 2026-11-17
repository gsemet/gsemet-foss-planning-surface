Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: rendering-core StRS and SwRS (P10.3)

Verdict: REVISE

Scope: 5 StRS, 66 SwRS in `requirements/tiers/{strs,swrs}/rendering-core/`. `okfreq validate` and
`lint` (with `--prose --check-links`) report 0 errors, 0 warnings. No placeholders (the `<img>`,
`<pre>`, `<kbd>` hits are literal text), every SwRS title equals its first `##` heading, every
SwRS has a nominal and a boundary scenario, no duplicate titles or ids.

## Checks that pass

1. Coverage: every F-CORE-001..058 maps to an SwRS or has a valid skip (029, 031 composite visual
   scenarios; 040..046 tooling, UC-CORE-5 n/a). UC mapping in the inventory matches StRS 001..005.
2. StRS: no message names, file names or pixel values (the "document folder or workspace root"
   in StRS-002 is user-level, acceptable).
3. Spot check (about 30 of 66: 004, 012, 013, 014, 016, 018, 020, 021, 026, 027, 029, 037, 044,
   048..050, 054..058, 063..066 against the inventory rows and sources): limits 2000 / 10 Mi, 200 / 400 / 8,
   skipped dirs, 40 blocks / 50 ranges, 5 MiB, allow-list tags all match.

## Defects

1. SwRS-MDOKFSTUDIO-CORE-013, scenario 1 is wrong. `mystRenderer.ts:196` expands only while
   `includeStack.size < MAX_INCLUDE_DEPTH (8)` and the stack contains the root document, so the
   8th include in a chain is the first placeholder (7 nested includes expand), not the ninth.
   Fix: state the depth precisely in the description ("a chain deeper than 7 nested includes /
   the 8th include level") and rewrite the scenario to a chain of eight includes, the eighth
   staying a placeholder. Also bounded-ness: three independent triggers (depth, cycle, 5 MiB
   size) in one SwRS, the oversize file has no scenario. Split the 5 MiB limit into its own SwRS
   (derive CORE-002, CORE-003) or add a boundary scenario for it.
2. SwRS-MDOKFSTUDIO-CORE-066 derives_from CORE-005 (render failure), which is the wrong topic:
   page-message validation is a trust/security behaviour (the inventory says trust-security may
   take it). Fix: derive from the trust-security StRS for message validation (create it in that
   scope, or move this SwRS there at the cross-scope merge); do not leave it under CORE-005.
3. SwRS-MDOKFSTUDIO-CORE-027 (engine warm-up at activation) derives_from CORE-005 (failed or
   superseded render): wrong topic, it is a latency property of the first render. Fix: derive
   from CORE-001.
4. SwRS-MDOKFSTUDIO-CORE-021 (trust refusal message) derives_from CORE-005 only: the refusal is
   about trust, not a failed or superseded render. Fix: derive from CORE-001 and the
   trust-security StRS (or keep CORE-005 plus the trust one); and note in Rationale/Verification
   that production always passes `allowUntrusted` (inventory: possible dead code), so the test is
   at pipeline level.
5. SwRS-MDOKFSTUDIO-CORE-051 bundles two behaviours (no appearance animation before the first
   input; a content patch takes it back) and overlaps 050/052 on reduced motion. Fix: split into
   "enable soft appearance after the first pointer or key" and "disable it again after a content
   patch", one nominal and one boundary scenario each.
6. SwRS-MDOKFSTUDIO-CORE-012, scenario 2 (GitHub alert in an included file) duplicates
   SwRS-045 and is a different behaviour from "expand an include". Fix: replace it with a
   boundary of the include itself (include with an optional `:class:` still expands; included
   file with frontmatter is shown without it, or a missing file leaves the directive in place).
7. SwRS-MDOKFSTUDIO-CORE-046 nominal scenario is not testable as stated ("it yields an HTML
   result"). Fix: GIVEN one document, WHEN rendered once per palette mode (Strict, GFM, MyST),
   THEN the three HTML outputs are byte-identical; keep the second scenario as the boundary
   (a mode-specific button set does not alter the content HTML).
8. SwRS-MDOKFSTUDIO-CORE-034 boundary scenario ("short identifier at 460 px is not wrapped")
   contradicts nothing but does not test the boundary of the rule (an identifier exactly as wide
   as the viewport). Fix: boundary = identifier exactly the viewport width does not overflow
   and does not wrap needlessly. Minor.
9. SwRS-MDOKFSTUDIO-CORE-062: grammar in scenario 1 ("a open details" -> "an open details");
   description needs a line break fix ("block (with ... summary) or kbd block" is fine, but the
   details form is covered only through gfm/myst tests per the inventory, so add the
   Verification note naming that test path). Minor.
10. StRS-MDOKFSTUDIO-CORE-005 states two outcomes (render failure, supersession by a newer edit)
    in one SHALL; the supersession part ("keep last good page marked as outdated") conflates
    with failure. Fix: reword to "When a render fails, ... ; when a newer edit supersedes a
    render, the Studio SHALL keep showing the previous page until the newer render is ready",
    or split into two StRS. Minor.

Count: 10 defects (1 and 2 are the blocking ones; 8 to 10 are minor).

## Re-check

Verdict: APPROVE

`okfreq validate --prose --check-links`: 264 requirements, 0 errors, 0 warnings. 5 StRS, 68 SwRS.

1. CORE-013: fixed (8th level wording, 8-include chain scenario, cycle boundary; 5 MiB moved out).
2. CORE-066: derives_from CORE-001 with an explicit Gap note, re-link at the cross-scope merge (no
   trust-security StRS exists yet; inventory F-CORE-058 says the same). Accepted as a tracked deferral.
3. CORE-027: derives from CORE-001. Fixed.
4. CORE-021: derives from CORE-001, guard/dead-code note and pipeline-level test added. Fixed.
5. CORE-051 split into 051 (enable after first input) and 068 (disable after a content patch), each
   with two scenarios; inventory F-CORE-048 lists 051 and 068. Fixed.
6. CORE-012: scenario 2 is now an include boundary (`:class:` still expands, missing file stays a
   placeholder). Fixed.
7. CORE-046: byte-identical outputs across the three modes. Fixed.
8. CORE-034: boundary is an identifier exactly viewport wide. Fixed.
9. CORE-062: grammar fixed, Evidence line names the gfm/myst tests. Fixed.
10. StRS-005: two clauses now explicit (failure; supersession); acceptable.
New CORE-067 (5 MiB inclusive boundary, 2 scenarios, derives CORE-002 and CORE-003, inventory F-CORE-009
column lists it) and CORE-068 (2 scenarios, derives CORE-001) are bounded and correct. Spot-checked 12,
13, 21, 27, 34, 46, 51, 62, 66, 67, 68 and StRS-005: no new defects.
