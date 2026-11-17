# c3-1 — A lazy continuation line of a GitHub alert renders outside the alert and is not editable with it

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Rendering, inline editing (alerts) |
| Modes | Side preview |
| Evidence | [c3-1-alert-lazy-line.jpg](../../evidence/c3-1-alert-lazy-line.jpg) |
| Related | none |
| Replay | `scenarios/c3-1-alert-lazy-continuation-outside.json` |

## Use case

An author writes an alert and wraps the text without a leading `>` on the second line, which is
valid CommonMark and GitHub renders it inside the alert.

## Steps to reproduce

Fixture (synthetic) `synth/admon.md`:

```markdown
> [!NOTE]
> Line one of a note.
lazy continuation line of the note.
```

1. Open the file, open the side preview, switch edit mode on.
2. Look at the alert, then click "Line one of a note." to open its block editor.

## Expected

The lazy line is part of the alert body (as on GitHub and as a plain `>` quote renders it in the
same preview), and the block editor holds all three lines.

## Observed

The alert box ends after "Line one of a note."; the lazy line renders as a normal paragraph
below it. The block editor covers "Lines 5-6" only. A plain blockquote with a lazy line renders
correctly. Editing and committing the alert (type change or text) leaves the lazy line untouched
in the buffer (diff stays one line), so no data is lost.

## Impact

The preview misrepresents the document, and the lazy line cannot be edited together with its alert.

## Where it comes from

`src/core/render/mystGithubAlerts.ts` (alert block range and body split); not read in depth.

## Suggested direction

Take the alert's end line from the blockquote token map, not from the last `>`-prefixed line.

## Test to add

Render test: `> [!NOTE]\n> a\nb` gives one alert whose body contains `b`.

## Done when

The replay scenario passes both checks.
