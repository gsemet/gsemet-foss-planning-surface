# Answers

Short name: `xstate6-inline-block`

## 2026-11-17: grill

1. xstate6-inline-block-Q1: **Block content: machine JSON or JS/TS source?** Owner: « Si json est
   possible, json se sera ». The block holds machine JSON (`machineToJSON` output); no code runs.
2. xstate6-inline-block-Q2: **Fence name.** Owner: « Appelle le block xstate-json ». The fence
   language is `xstate-json`.
3. xstate6-inline-block-Q3: **Renderer.** Owner: « le moteur doit être opensource en MIT ». Any
   rendering engine (and its runtime dependencies shipped in the VSIX) is open source under MIT.
4. xstate6-inline-block-Q4: **When, and how deep.** Owner: « Fait l'étude exhaustive ». The study
   runs now, exhaustive, before any specification; its report goes in `evidence/`.

## 2026-11-17: after the study (evidence/xstate6-renderer-study.md)

5. xstate6-inline-block-Q5: **Does the MIT rule cover what Studio already ships?** Owner: « tu
   peux répondre à la question sur les licences toi-même ». Decided by the Chief of Staff: the MIT
   rule applies to what this CR adds (the engine and every new runtime dependency it brings into
   the VSIX). Dependencies Studio already ships (Mermaid's d3, DOMPurify, elkjs) are not
   re-judged: reusing them adds no new license.
6. xstate6-inline-block-Q6: **Rendering.** Owner: « Il faudrait un rendu avec édition comme
   l'extension du fournisseur. Je veux le même rendu que sur leur site. » The block renders like
   Stately's own diagrams (stately.ai, the Stately Editor VS Code extension), and the diagram can
   be edited, writing back the block's JSON. A follow-up study checks which MIT pieces give that
   look and editing.
7. xstate6-inline-block-Q7: **Is xstate-viz's older look acceptable as "the same rendering"?**
   Owner, with a screenshot of today's Stately editor (`intake/target-look.png`): « je veux ».
   Target: that look and interaction, reimplemented in Studio (no Stately code, assets or
   branding): a light grid canvas; rounded state boxes, the initial state marked by a dot and an
   arrow, final states by a ringed dot; event labels as pills on orthogonal edges routed by ELK;
   guarded transitions as a card (diamond, name, `IF` condition, context assignments); dashed
   edges for re-entry; timeout labels with a clock icon; zoom level and fit-to-view control; a
   side panel "State details" (name, state type, initial state toggle, timeout, parent state,
   layout) to edit the selected state, writing back the block's JSON. xstate-viz (MIT) and elkjs
   remain the starting point for code and layout.
8. xstate6-inline-block-Q8: **Why the block, and is xstate-viz worth reusing?** Owner: « xstate-viz
   n'est plus maintenu je vois pas ce que ça apporterait à Studio. le but c'est de fournir une
   syntaxe de communication entre l'agent et l'humain efficace, en gros, faire ce que l'on ne peut
   pas en mermaid ou plantuml ». xstate-viz is dropped as a base. The block's purpose is an
   efficient agent-to-human channel for behaviour that Mermaid and PlantUML cannot carry; the
   Stately look is no longer the goal in itself.
9. xstate6-inline-block-Q9: **Keep the CR?** Owner, after the proposed scope (validation,
   simulation, scenarios, diff, editing): « ok, abandonne l'idée ». Abandoned; no PR was opened.
