# Report — 273-frontmatter-this-field

Status: **done** (2026-11-10, branch `change-requests/273-frontmatter-this-field`, PR #341, merge commit `ecb368e9`, fixes GitHub #334).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A front matter value can be shown in the body with inline code `= this.field`: a pure core pass `src/core/render/frontmatterValues.ts` shows the value as plain text, before the table-of-contents markers so the TOC entry and heading anchor use it; a missing key keeps the raw code with a warning style and a diagnostic (capped at 20 per render); new SwRS-MDOKFSTUDIO-CORE-079 (proposed), requirements log, CHANGELOG, writing-skill update | `ecb368e9` |

## Proof of completion

- Three rounds, Inspector on Opus each time: r1 FIX-REQUIRED (the TOC showed the raw expression), r2 FIX-REQUIRED (the double-backtick escape did not work; a wrong sentence about the heading anchor in the SwRS), r3 APPROVE (coder on Opus).
- 21 new unit tests; visual scenarios v32 and v33 (light and dark). `just check` passed locally (3691 unit, 93 security); the headless capture of 72 scenarios passed.
- CI at head `bf6d8249`: PR run 42855525413 green; heavy run 42854789775 green (integration and stress included).
- Before and after screenshots are on branch `change-requests/273-frontmatter-this-field-assets`.

## Open items

- Owner decision: `null`, an empty string, `[]`, `{}` and a key with no value show the warning style; the owner keeps it as is.
- Known limitation: an included file reads the including document's front matter, and its missing-key warning carries the included file's line number.
- Dotted paths (`this.a.b`) follow own properties of objects only, not array indexes. To show the expression literally, keep a backtick inside the code; more backticks do not escape it.
- No edit-mode visual scenario: a unit test that renders twice covers the refresh path.
