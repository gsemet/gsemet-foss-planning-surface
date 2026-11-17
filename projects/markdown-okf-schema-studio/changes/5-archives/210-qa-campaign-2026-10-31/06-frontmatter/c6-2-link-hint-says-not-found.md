# c6-2 — The x-okf-link editor hint says "No Markdown file named related-target.md" for a link the table resolves

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (typed, completed, and `.md` variants in one session) |
| Area | OKF links (frontmatter) |
| Modes | Side preview |
| Evidence | DOM text of the status line (replay check) |
| Related | none |
| Replay | `scenarios/c6-2-link-hint-ignores-document-folder.json` |

## Use case

An author edits the `related` list of a note whose targets sit next to it.

## Steps to reproduce

1. Open `synth/frontmatter-edge.md` (a `synth/related-target.md` exists), preview to the side, edit mode.
2. Click the `related` value, click "List item 1" (`related-target`), type a letter then Backspace.

## Expected

No warning: the table shows `related-target` as a resolved link, and the file exists.

## Observed

The status line reads `No Markdown file named "related-target.md" was found. It will be saved as
typed.` Typing any value gives the same message (`zzz.md`, `related-target.md.md`). The suggestion
list offers only the bundle's chapters (book/), none of the files next to the document.

## Impact

A false warning on every edit of a valid link, and no completion for siblings of the document.

## Where it comes from

Not read; the hint looks up files from a root other than the one the table uses to resolve the link.

## Suggested direction

Use one resolver for the table and the editor hint, and offer files of the resolved root.

## Test to add

Real-input E2E on `synth/frontmatter-edge.md`: editing a resolved link shows no "not found" status.

## Done when

The replay scenario passes.
