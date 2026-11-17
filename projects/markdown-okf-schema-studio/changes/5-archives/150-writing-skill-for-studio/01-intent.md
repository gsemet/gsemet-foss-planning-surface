# A self-contained agent skill: writing Markdown for Studio

Type: feat · Priority: P1 · Requested 2026-10-27 by the user

## Intent (user, translated)

Create `skills/writing-for-markdown-okf-schema-studio/SKILL.md` in this repository: a skill that
teaches an agent how to write Markdown for Studio, with everything Studio can render. Example use:
"/writing-for-markdown-okf-schema-studio generate the implementation plan in XXX.md", and the
agent knows which syntax is available and writes a very good-looking document.

- **Strict minimum**: agents already know MyST, GFM, Mermaid, PlantUML, SVG and Vega-Lite; the
  skill only says **what is available in Studio** (and what is not), with the shortest examples
  where Studio differs or adds something. An agent must understand it instantly.
- **Raw SVG** is very effective to show an idea visually: say so.
- The agent gets a **palette of choices** (PlantUML, Mermaid, raw SVG, Vega-Lite, cards, tabs,
  admonitions, tables, math …) and must show **taste**: pick what carries the idea best, not
  everything at once.
- **Self-contained**: it is installed on machines that do not have Studio's code, only the
  extension. No link into this repository's sources; everything the agent needs is in the skill
  folder.
- **Maintenance**: `AGENTS.md` and the constitution state the maintenance rules clearly, backed by
  a maintenance guideline.

## Expected

- `skills/writing-for-markdown-okf-schema-studio/SKILL.md` with standard skill front matter
  (`name`, `description` that triggers on "write / generate a Markdown document, plan, report for
  Studio"), usable by Claude Code and GitHub Copilot (Agent Skills format). Short: a capability
  table (syntax family → what Studio renders → one-line example), the palette modes (Strict, GFM,
  MyST, Full) and what each enables, the "taste" rules (one visual per idea, SVG for concepts,
  Mermaid/PlantUML for flows and sequences, Vega-Lite for numbers, admonitions sparingly, tables
  for comparisons, front matter / OKF properties when relevant), and limits (what does not render,
  Restricted Mode, no remote resources). Optional `references/` files only if SKILL.md would exceed
  about 150 lines (progressive disclosure).
- It covers everything the stack delivers: MyST directives and roles Studio supports (including
  cards, tabs, `versionadded` from CR 148), GitHub alerts, math, Mermaid, PlantUML (built-in, no
  Java), Vega-Lite and Vega (CR 149), `[TOC]` / `[[_TOC_]]` (CR 142), README HTML (CR 141), comment threads,
  OKF front matter, tables and list tables, figures.
- **Maintenance guideline** `.agents/guidelines/writing-skill-maintenance.guideline.md`: any PR that
  adds, removes or changes a rendered syntax updates the skill in the same PR; the skill stays
  self-contained and minimal; how to check it.
- `AGENTS.md` (Quick Navigation and a rule line) and `.agents/constitution.md` (one short rule:
  the writing skill is part of the product and kept in sync) point to that guideline.
- **A check**: a unit test (or `just check` step) renders every example of the skill through the
  real pipeline and fails on any render error or unknown directive, so the skill cannot drift.
- Optional, decide in the CR: the skill folder is shipped in the VSIX and a command "Install the
  writing skill" copies it to the user's skills folder. Record the decision; do not build it unless
  it is trivial.

## Proof

The check above; a demo: ask a fresh agent with only the skill to write a sample implementation
plan, render it in Studio, real-window screenshots of the result (cream + dark) in the PR.
