# UX-25 — Focusing any non-Markdown editor wipes the side preview

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced |
| Area | Side preview "follow active editor" |
| Evidence | [r3-link-click.jpg](../../evidence/r3-link-click.jpg) |

## Use case

An author reviews a requirement in the side preview and clicks its `implemented_in_files` link to
check the code, or simply clicks a `.py`, `.yml`, or `.json` tab for a moment, then comes back.

## Steps to reproduce

1. Side preview on `SwRS-CORE-001.md` (with `projectRoot` set, see
   [UX-22](../04-okf-links-and-diagnostics/UX-22-project-root-ignores-bundle.md)).
2. Click the `src/export.py` value in the properties table.

## Observed

- Good: `export.py` opens in the source group with the `@implements_req SwRS-CORE-001` line
  selected.
- Then the side preview follows the new active editor and replaces the rendered requirement with
  a status page: **"Preview source missingOpen a Markdown file to use the Sphinx preview."** The
  panel title becomes "Markdown OKF-Schema Studio: export.py".
- Returning to the Markdown tab triggers a full re-render from scratch.

The same happens for any non-Markdown editor that becomes active, which in practice means
settings JSON, a YAML schema, a code file opened from a link, or a diff editor.

## Expected

Like VS Code's built-in Markdown preview, the side preview keeps showing the last Markdown document
when the active editor is not Markdown, and switches only when another Markdown editor becomes
active.

## Impact

Following the extension's own navigation (x-okf-link to code, `@tests_req` markers) destroys the
context the author came from. Schema authors who alternate between `*.schema.yaml` and a document
see the preview blank on every switch.

## Where it comes from

`src/extension.ts` `followActiveEditor` (L2222-L2237) calls `showUnavailableDocument` for any
ineligible document; `showUnavailableDocument` (L1706-L1732) discards the stage and sets the
missing-source page.

## Suggested direction

Ignore ineligible active editors in `followActiveEditor` (keep the current document), and use the
"missing source" page only when the previewed file itself disappears.

## Test to add

E2E: side preview on a Markdown file, open a `.py` file in the source group, assert the preview
still shows the Markdown content and its title.

## Done when

The side preview only changes document when another Markdown editor becomes active.
