# Agent visual review — summary (T40 step 3)

Inputs, all captured on 50cd143:
- the visual campaign of the PHASE5 checkpoint, `logs/visual-PHASE5/` (96 PNGs);
- the real-input captures of the PHASE5 full run, `logs/real-input-PHASE5/` (47 PNGs).

Seven Opus reviewers ran the protocol in `../visual-review.md`. The merged results are in
`review.json`.

| Set | Images | Pass | Fail |
| --- | --- | --- | --- |
| Visual campaign | 96 | 77 | 19 |
| Real-input | 47 | 35 | 12 |
| **Total** | **143** | **112** | **31** |

## Triage by the orchestrator

**Regressions of an approved fix: none found.**

For each of the 19 visual-campaign failures, the orchestrator compared the PHASE5 image with the
same capture from T00, before the plan (`logs/visual-T00/`), pixel by pixel.

- **13 are unchanged since T00**, apart from rows 47–76 (the T38 anchor icon). They are
  pre-existing, or the note's expectation is outdated:
  - `chapter-dark-top`: the note expects no figure number, but the caption is numbered;
  - `frontmatter-dark`, `frontmatter-light`: header and Name column shading;
  - `frontmatter-forced-white`: values in black;
  - `frontmatter-link-details-dark-460`, `frontmatter-link-details-white-460`: the hover tooltip
    of Refresh covers the Value header;
  - `handbook-dark-third`: the line cut under the sticky band;
  - `handbook-narrow-top`, `preview-sticky-headings-natural-growth`, `syntax-narrow-python`: the
    toolbar covers the end of a long sticky H1. This is part-2 UX-44, which is not approved;
  - `preview-sticky-headings-1`: the band is shorter than the toolbar;
  - `schema-validation-error-narrow`: a path breaks mid-word;
  - `handbook-narrow-table`: 0.28 % changed (the table scroll shadow, UX-15); the toolbar overlap
    is the same as at T00.
- **6 changed, as intended:**
  - `edit-table-wrapped-dark-460`, `edit-table-wrapped-light-460`: the table toolbar moved above
    the table (UX-14). The flagged `pedal_position` wrap inside a 460 px wrapped cell, and the
    missing " updated" text, are the same at T00.
  - `edit-table-wrapped-dark-900`, `edit-table-wrapped-light-900`: the table toolbar moved above
    the table, with labels (UX-14). The reviewer flags the floating preview toolbar at the edge of
    the short sticky band. That predates the plan and is UX-44.
  - `edit-frontmatter-list-dark`, `edit-frontmatter-list-light`: the field actions no longer cover
    the date value (UX-20 / UX-21), and the paragraph no longer reflows (UX-09). The reviewer's
    S2 point, that the pending save is not visible, applies to T00 as well.

**Real-input failures (12).** These scenarios were created during the plan, so no T00 image exists.
Each behaviour is asserted in the DOM or the host by its RI scenario, and the full gate passes.
- Cross-checked by the bug replay (`../replay/`):
  - `21-edit-hover`: UX-07, outline not visible in the capture;
  - `29-list-link-warning`: UX-19, the datalist is not shown, and `StRS-` / `BX.md` is split;
  - `32-save-keeps-list-in-place`, `33-save-keeps-table-in-place`: UX-11, the view does not
    match the note's measurements;
  - `30-frontmatter-actions-value`, `31-frontmatter-actions-picker`: UX-21;
  - `34-link-diagnostic-tooltip`: UX-23, the tooltip covers the end of a heading;
  - `26-focus-change-still`, `27-hidden-preview-catches-up`: UX-25 / UX-29, the view does not
    match the note.
- Known, and blocked with UX-28: `38-anchor-disabled` (G6). The pending banner reads
  "Preview pendingWaiting for the latest edit." This is the pending-banner layout question of
  T29.
- Minor, for follow-up:
  - `12-frontmatter-title-multiline`: a two-line title is shown on one line;
  - `24-start-writing-open`: the floating toolbar sits over the empty editor's top-right corner
    (UX-44 family).

Harness finding: in many images where the reviewer sees no collision, the visual campaign's machine
check reports "sticky heading overlaps the reserved toolbar row". Its geometry rule is stricter
than what is visible. This is logged in `../followups.md`.
