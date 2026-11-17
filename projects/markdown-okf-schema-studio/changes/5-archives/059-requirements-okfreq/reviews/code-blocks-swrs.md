Ids in this file predate the reduction; see `reduction/mapping.csv`.

# Critic review: code-blocks SwRS (P10.3)

Verdict: REVISE

Scope: 4 StRS, 30 SwRS in the worktree `markdown-okf-schema-studio-wt-059`. `okfreq validate --prose
--check-links`: 246 requirements, 0 errors, 0 warnings. Titles are the first `##` heading, no
placeholders, no duplicate ids, `derives_from` targets exist and fit the subject (CODE-005 derives
from StRS-001 and StRS-003, which is right). Spot-check against `src/` of the worktree: 12 of 30
SwRS (40%): 003, 005, 006, 007, 009, 011-fallbacks (by inventory), 016, 018, 020, 026, 030 and the
alias list of 002. Most match; the defects are below.

## (1) Coverage of F-CODE

All 33 F-CODE rows map to a SwRS or a skip (F-CODE-001/002 to CODE-001; 003 to 002; 004 to 003;
005 to 004; 032 to 005; 030 to 028; 031 to 029; 033 to 030; the others one to one).

- F-CODE-028 skip (no keyboard path): accepted. It documents an absent behaviour, a SHALL would
  describe something that does not exist. StRS-004 rationale records it ("revealed by pointing
  only"), which is enough as a finding.
- F-CODE-029 skip (palette language list): reason is valid in principle, but there is no
  `swrs/palette-slash` yet in this worktree, so it cannot be confirmed here. Condition: the
  palette-slash critic must find a SwRS that owns `highlightLanguageNames` (the language list
  of the edition palette). If it does not, CODE needs one.

## (2) Defects (SwRS, bounded / testable / scenarios)

1. **SwRS-MDOKFSTUDIO-CODE-007, boundary scenario is false.** The CSS fallbacks are fixed hex
   colours (`var(--studio-charts-blue, #3794ff)` and so on; comments use
   `--studio-descriptionForeground, #808080`), not "the editor foreground colour". Fix: GIVEN a
   theme that defines no chart colours / THEN each token class uses its built-in default colour
   and comments stay italic. Also fix the verification criterion accordingly.
2. **SwRS-MDOKFSTUDIO-CODE-013, boundary scenario is vague and not a boundary.** "The page layout
   rules of Auto width apply" is untestable and sits in layout-width, and the inventory notes Auto
   width lets wide code break out, which contradicts "SHALL NOT widen the page" as written. Fix:
   either scope the SHALL ("outside Auto width mode") with a boundary of a line exactly as wide as
   the block (no scrollbar, no overflow), or turn the Auto case into an explicit exception
   stated in the normative text.
3. **SwRS-MDOKFSTUDIO-CODE-018, bundles four behaviours** (hide under 30 px, show again on return,
   hide when scrolling stops outside, follow resize), and the boundary scenario mixes two
   WHEN/THEN pairs in one line. Fix: split into (a) 30 px visibility threshold hide/show and
   (b) hide when scrolling stops with the pointer outside the block (and the resize repositioning
   as its own SwRS or dropped). Each with one GIVEN-WHEN-THEN per scenario.
4. **SwRS-MDOKFSTUDIO-CODE-017, bundles** shape/position (26 px, 6 px corner), avoiding the
   sticky band and floating toolbar, and lazy creation. Fix: split placement avoidance (below
   band/toolbar) from the basic position, or reduce the SHALL to one behaviour and move the
   rest to its own SwRS; keep the "no button before first hover" boundary.
5. **SwRS-MDOKFSTUDIO-CODE-020, bundles** the 1.5 s Copied state and the reset on hovering
   another block. Also "When a copy completes" is wrong: the page shows Copied on click, the
   host gives no acknowledgement (see suspected bug in F-CODE-026/027). Fix: trigger "When the
   reader clicks the copy button"; move the reset-on-other-block to its own SwRS or keep only
   as a boundary of a single SHALL ("returns to Copy code after 1.5 s or on hovering another
   block" is still two triggers: prefer the split).
6. **SwRS-MDOKFSTUDIO-CODE-008, bundles** line marking with the panel look (full width, square
   corners, no border). Fix: keep marking in 008 and put the panel style in its own SwRS (or in
   012's family) with its own scenarios.
7. **SwRS-MDOKFSTUDIO-CODE-005, bundles** the unknown-language wrap and the throwing-grammar
   fallback. The nominal and boundary scenarios cover both but the SHALL has two conditions
   joined by "or". Acceptable only if the description is reduced to the wrapped-block fallback;
   suggest keeping as is only if the critic lead accepts the pairing. Minimum fix: state the
   escaped-text result as the boundary only, and the nominal as the one SHALL.
8. **SwRS-MDOKFSTUDIO-CODE-029, bundles** hide on `mouseout` and "never for blocks outside the
   preview content". Fix: split into two SwRS or merge the second rule into CODE-022
   (excluded blocks) and keep 029 as the mouseout hide.
9. **SwRS-MDOKFSTUDIO-CODE-016, bundles** soft background/readable text and YAML link colour.
   Fix: split the YAML colour into its own SwRS (the white-theme Python boundary then belongs to
   the first one). Lower priority than 1-8.
10. **SwRS-MDOKFSTUDIO-CODE-001, bundles** literal display (incl. inner fences in a markdown
    fence) and token colouring, and its boundary is the same as CODE-004. Fix: keep CODE-001 on
    the highlighting of supported languages, add the literal-text rule (inner fences, table,
    link inside a `markdown` fence) as its own SwRS, and give CODE-001 a boundary of its own
    (for example a supported language with an empty block).

## (3) StRS

No implementation detail found (no message names, pixel values or file names). Two soft points,
not blocking: StRS-004 rationale cites the "button" and "pointing only", and StRS-001 rationale
mentions the README; both are in the Rationale section, not in the SHALL.

## (4) Links and form

Correct. No duplicates, no placeholders. The generated `## User Need` heading inside the StRS
body comes from the okfreq template and is the same in every scope: leave it.

## Notes

- SwRS-025, 024, 027, 031-type rows are flagged untested in the inventory; their verification
  notes name tests that do not exist yet (integration suites for untrusted/standalone copy).
  That is a plan, not a defect, but the implementation step must add them or set
  `annotation_exemption`.

## Re-check

Verdict: APPROVE

`okfreq validate --prose --check-links`: 264 requirements, 0 errors, 0 warnings. All 10 first-review
defects are fixed: 007 uses the built-in default colours; 013 is scoped "outside Auto width mode"
with an exact-fit boundary; 018 is reduced to the 30 px threshold (hide/show), with 032 (scroll stops
outside) and 033 (resize) split out; 017 is position only, with 034 (clear of band/toolbar); 020 is
triggered by the click, with 035 (reset on another block); 008 is marking only, with 036 (diff panel
look); 005 is wrapping only, with 037 (throwing grammar); 029 is mouseout only, the excluded blocks
live in 022; 016 and 038 (YAML link colour) are split; 001 has its own empty-block boundary, with 031
(literal fenced text). New CODE-031..038: each has one SHALL, 2 scenarios, a fitting derives_from
(001 for 031/037/038, 004 for 032-035, 002 for 036), and the inventory last column maps them
(F-CODE-001/008/016/017/018/020/031/032 all updated; every non-skipped F-CODE row has a SwRS).
Spot-checked 15+ SwRS (001, 005, 007, 013, 016-018, 020, 022, 029, 031-038): no new defects.

Non-blocking notes: (a) CODE-005 boundary wording ("a diff block with no language other than diff")
is vague; (b) CODE-037 boundary adds the unwrapped-block case as a second outcome; (c) the F-CODE-029
skip stays conditional: no palette-slash SwRS exists yet in this worktree, so the palette-slash
critic must confirm one owns `highlightLanguageNames`.
