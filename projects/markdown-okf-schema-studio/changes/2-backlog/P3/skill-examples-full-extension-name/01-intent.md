# Writing skill references and docs: full extension name

From CR 158 (landed in #168), 2026-10-28.

## Intent

Rename "Studio" used alone to "Markdown OKF Schema Studio" (or "the extension" where repetition is
heavy), as SKILL.md now does, in:

- `skills/writing-for-markdown-okf-schema-studio/references/examples.md` (title, line 3, the
  PlantUML sample); every example must still render (`test/core/render/writingSkill.test.ts`);
- `.agents/guidelines/writing-skill-maintenance.guideline.md`;
- `AGENTS.md` (also its "Markdown OKF-Schema Studio" title and intro).

Docs only; no behaviour change.
