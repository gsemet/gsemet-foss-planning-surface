## Summary

Adds a self-contained agent skill, `writing-for-markdown-okf-schema-studio`, that tells an agent what Studio
can render and how to choose among it with taste: a capability table, the palette modes (Strict, GFM, MyST,
Full), selection rules (one visual per idea, raw SVG for concepts, Mermaid/PlantUML for flows, Vega-Lite for
numbers, sparing admonitions) and the limits. A test renders every example of the skill through the real
pipeline, so the skill cannot drift from the product.

## Deliverables

A sample implementation plan written from the skill alone (headless Chromium capture; the real-window render
is pending because the screen was locked during the run):

![Demo plan, cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/aeb6d312ebabfd11aa88d63a0a048ef0bf48b87f/demo-plan-cream.png)
![Demo plan, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/aeb6d312ebabfd11aa88d63a0a048ef0bf48b87f/demo-plan-dark.png)

```text
skills/writing-for-markdown-okf-schema-studio/
├── SKILL.md              (134 lines)
└── references/examples.md
```

- Maintenance guideline `.agents/guidelines/writing-skill-maintenance.guideline.md`; `AGENTS.md` and the
  constitution (new section 6) state that the skill is part of the product and is updated in any PR that
  changes a rendered syntax.
- `test/core/render/writingSkill.test.ts`: skill shape (no link out of the folder), zero diagnostics and no
  unresolved directive for every example, 20 syntax families each rendered as its own element. Without the
  skill folder, 3 of the 4 tests fail.
- The folder is not excluded by `.vscodeignore`, so the VSIX already carries it.

## Impacts

Docs and agent tooling only; no runtime change. Blast radius: 1.

## Test plan

- `just check`: unit 2922, contracts 2, release tests 45, requirements 1040 with 0 errors.
- Real-window render of the demo: pending (screen locked); run the heavy CI job.

### Requirements traceability

- SwRS-MDOKFSTUDIO-CORE-073 (the writing skill and its render check): source
  `skills/writing-for-markdown-okf-schema-studio/SKILL.md`; test `test/core/render/writingSkill.test.ts`.
- StRS CORE-001 `derived_by` and the rendering-core index regenerated; `skills` added to the rendering-core
  `source_dirs`.

## Autonomous decisions

- Top of the stack (above the Vega-Lite CR), so the skill documents everything the stack adds.
- Maintenance guideline name `writing-skill-maintenance.guideline.md`; the skill's examples are rendered by a test.
- The TOC marker documented is `[TOC]` / `[[_TOC_]]` and `{contents}`; `[[toc]]` is literal text and listed as a limit.
- Raw SVG is documented as a file shown with `{figure}` or an image, because inline `<svg>` in Markdown is dropped.
- A bare `:::{dropdown}` renders an empty `<details>` (body lost); the skill uses `:class: dropdown`. Known issue, to file as a backlog item.
- An "Install the writing skill" command is not built; recorded in the guideline as a separate change.

## Internal references

CR 150 (writing skill for Studio), stacked above CR 149.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
