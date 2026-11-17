# The x-okf-link list editor says a sibling file is not found

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-FMSCHEMA-050, SwRS-MDOKFSTUDIO-FMSCHEMA-063 · Area OKF links (frontmatter) · Side preview · QA210-07 · Replay `scenarios/c6-2-link-hint-ignores-document-folder.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![List editor hint says the file was not found](evidence/currently.jpg) | ![Expected: no not-found hint (annotated copy)](evidence/expected.jpg) |
| *Currently: the hint reads `No Markdown file named "related-target.md" was found` while the table row above resolves it (replay `c6-2` on b9118506).* | *Expected (annotated copy of the before-shot, same view without the hint): no not-found hint, suggestions from the document's folder.* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author edits the `related` list of a note whose targets sit next to it. The properties table
shows `related-target` as a resolved link, yet the editor warns that no Markdown file by that name
exists and offers only the chapters of another folder as suggestions. The product contradicts
itself: the same value is valid in the table and "not found" in the editor, so a valid link looks
broken on every edit and siblings of the document cannot be completed. FMSCHEMA-050 resolves a
document-relative link from the document's folder and FMSCHEMA-063 shows whether a value resolves.

## Steps to reproduce

1. Fixture `synth/frontmatter-edge.md` (with `synth/related-target.md` next to it, both in
   `assets/synth/`); open the preview to the side, edit mode on.
2. Click the `related` value, click "List item 1" (`related-target`), type a letter then Backspace.
3. The status line reads `No Markdown file named "related-target.md" was found. It will be saved
   as typed.` Other values give the same message (`zzz.md`, `related-target.md.md`).

## Impact

A false warning on every edit of a valid link and no completion for the document's siblings.

## Where it comes from

The hint looks files up from a root other than the one the table uses to resolve the link. Not read
in depth.

## Suggested direction

One resolver for the table and the editor hint, and suggestions taken from the resolved root. Done when: the editor hint and suggestions use the same resolution as the table; replay `c6-2` passes.

Uncheck to disagree: [x]

## Test to add

No test: once the table and the editor share one resolver the two cannot diverge, and the replay `c6-2` stays as the manual check.

Uncheck to disagree: [x]

Sources: sheet [c6-2](../../../4-archives/210-qa-campaign-2026-10-31/06-frontmatter/c6-2-link-hint-says-not-found.md),
replay [c6-2](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c6-2-link-hint-ignores-document-folder.json),
[campaign index](../../../4-archives/210-qa-campaign-2026-10-31/00-index.md).
