# Spec CR 090

## README outline (target 100-150 lines)
1. Title, logo, badges, links row (Marketplace, gallery, reports, requirements) - kept.
2. Pitch (3 lines) + hero screenshot (Cream, polished demo doc, edit mode showing MyST grid + admonition).
3. "Why Studio": one subsection each, 2-3 lines + one Cream screenshot:
   a. Edit MyST visually (grids, admonitions, figures, list-table) - strongest, verified
   b. Schema-aware OKF properties - verified
   c. Wide tables and text: Auto width (margin-break) - visual, low evidence
   d. See what changed since the last commit - claim specific form only
   e. Mermaid and PlantUML, no Java - verified (the pair)
   f. Themes: Cream default; one small row of 3 themes
   g. Others as a bullet list: review comment threads, slash menu, block selection, rich paste,
      Sphinx conf.py check, raw-source-preserving edits.
4. Comparison table (4 verified rows) with "checked on 2026-10-25" + wording "no equivalent found".
   Sources in docs/user/comparison.md.
5. Install, Open Studio (2 lines).
6. Documentation links to docs/user/*.md, CONTRIBUTING.

## Docs plan (nothing lost; text moved verbatim, headings kept)
docs/user/README.md (index), editing.md (inline editing, slash menu, toolbar? no -> toolbar.md),
toolbar.md, slash-menu.md, themes-and-motion.md, wide-tables.md, plantuml.md,
review-comments.md, okf.md (OKF + linked-file annotations), sphinx.md, settings.md,
comparison.md (matrix summary + sources, from research).
README's old screenshots move with their sections.

## Screenshots (images/readme/, Cream, simulated visual suite via README_BY_ID)
New demo fixture + scenarios: hero, myst-edit (grid/admonition/figure), schema-properties-cream,
diff-since-commit, diagrams (mermaid + plantuml), themes row. Reuse margin-break-cream.
