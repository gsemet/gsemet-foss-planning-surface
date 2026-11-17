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
