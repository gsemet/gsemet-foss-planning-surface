### Garden the requirements of palette-slash, theme-zoom and layout-width (CR-345)

- Added (proposed): StRS-MDOKFSTUDIO-PALETTE-019, 020 and 021 replace the umbrella StRS-MDOKFSTUDIO-PALETTE-001
  (formatting buttons and shortcuts; GitHub Flavored Markdown constructs; MyST constructs), and SwRS-MDOKFSTUDIO-PALETTE-276
  to 280.
- Superseded, old to new:
  - StRS-PALETTE-001 to StRS-PALETTE-019, 020, 021;
  - SwRS-PALETTE-045, 048, 135, 138, 126 to PALETTE-276 (inline marker buttons);
  - SwRS-PALETTE-049, 052, 053, 123, 267 to PALETTE-277 (line-prefix buttons);
  - SwRS-PALETTE-265, 273, 274 to PALETTE-278 (starter blocks) and PALETTE-001 (mode membership);
  - SwRS-PALETTE-130, 137 to PALETTE-127; SwRS-PALETTE-268 to PALETTE-238;
  - SwRS-PALETTE-010 and SwRS-THEME-013 to SwRS-LIFE-169; SwRS-LAYOUT-018 to SwRS-LAYOUT-011.
- Split out: the scroll-follow scenario of PALETTE-021 became PALETTE-279 (derived from StRS-PALETTE-005), the rule
  icon of PALETTE-002 became PALETTE-280 (derived from StRS-PALETTE-019).
- Reparented: the SwRS that derived from StRS-PALETTE-001 now derive from 019, 020 or 021 (or from StRS-PALETTE-002,
  007, 013, 015 or 018 where they belong there); PALETTE-114 derives from StRS-REVIEW-015 and PALETTE-275 from
  StRS-PALETTE-015; TABLE-085 and TABLE-111, CORE-028, TRUST-001, 005, 006 and 065 moved to the palette StRS they
  serve. SwRS-LIFE-169 and LIFE-170 are cited by StRS LAYOUT-003, PALETTE-002, THEME-004 and THEME-011 through
  `depends_on`. Main paths that cited a superseded SwRS now cite the merged one.
- Changed text: StRS PALETTE-002 (four nested modes), PALETTE-005 (one use case), PALETTE-018 (Explorer drops, pasted
  URL), LAYOUT-004 and THEME-002 (history removed); a `### Use case diagram` on all 15 in-force StRS of the scope.
- Approved StRS: the owner agreed in advance (CR-345 `02-answers.md`) to the corrections of StRS-LAYOUT-001,
  StRS-LAYOUT-003 and the diagram of StRS-PALETTE-015; their `approved_by` and `approved_at` are set again and the
  Driver records the re-approval.
- Checks run: `just requirements-update`, `just requirements-lint`, `just check-markers` and
  `okfreq validate --check-links`.

