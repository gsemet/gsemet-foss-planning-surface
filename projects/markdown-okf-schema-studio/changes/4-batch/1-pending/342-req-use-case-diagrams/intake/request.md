# Show a use-case diagram on each StRS, on GitHub and on the requirements site

From the requirements gardening audit, CR requirements-gardening (projects/markdown-okf-schema-studio/changes, evidence/audit-synthesis.md), section "Diagrams on the GitHub Pages site" and evidence/audit-crosscutting.md section B.

- Rule in requirements/guidelines/project.guidelines.md: a StRS may carry an authored `### Use case diagram` section with one Mermaid fence (sequence, actors or state), placed before `### Main paths`.
- The requirements viewer (test/site/requirementsViewer/) pre-renders that fence to inline SVG at site build time, with the Chromium and mermaid already in the repo (pattern of test/site/socialCard.ts:130), and shows it on the use-case page; a page without the section is unchanged.
- PlantUML is out: GitHub does not render it.
- Writing the diagrams of the 80 StRS is not in this CR: each restructure CR writes the diagrams of its StRS.
