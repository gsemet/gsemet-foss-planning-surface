# 158 — Writing skill: correct product name, OKF and OKF-Schema defined

Type: docs · Priority: P2 · From the user via main, 2026-10-28

## Intent (user)

`skills/writing-for-markdown-okf-schema-studio/SKILL.md` must:

1. name the extension "Markdown OKF Schema Studio" everywhere (no "Studio" alone, no
   "OKF-Schema Studio");
2. define OKF, the Open Knowledge Format: a folder with sub-folders of Markdown files with front matter;
3. define OKF-Schema right after OKF: a separate tool that provides JSON Schemas for OKF bundles,
   https://github.com/gsemet/okf-schema. It gives validation to Markdown front matter; full
   validation needs that tool installed with uv: `uv tool install okf-schema` (from the okf-schema
   README; installs `okf-schema`, `okfkb`, `okfreq`). The extension only helps visualise (field
   descriptions, enum values, ...) and does not replace the validator;
4. state that OKF-Schema and the VS Code extension have the same author.

Short, in the skill's register. Keep the `@implements_req SwRS-MDOKFSTUDIO-CORE-073` anchor and
`test/core/render/writingSkill.test.ts` green (it asserts the description matches /Studio/);
refresh any installed copy of the skill.
