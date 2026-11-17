# UX-38 — A field editor left in error silently blocks every other field

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced |
| Area | Frontmatter properties table editing |
| Evidence | [p2-fm-object-after.jpg](../evidence/p2-fm-object-after.jpg) |

## Use case

An author enters an invalid value (a number out of range, a YAML mistake), sees the red message,
and clicks another field to fix something else first.

## Steps to reproduce

1. `synth/frontmatter-edge.md`, edit mode on, click `priority`, type `9`, press Enter.
   The message "Schema validation failed: must be <= 5" appears.
2. Click the `reviewed_on` value, then the `owner` value.

## Observed

- Neither click opens an editor; nothing visible happens. The `priority` editor stays open with
  its error, possibly scrolled out of view.
- The only exit is to scroll back, click inside the invalid control, and press Escape. There is no
  Cancel button and no hint.
- When the invalid editor is scrolled above the viewport, a user can believe edit mode is broken.

## Where it comes from

`src/webview/scrollSync.ts`: openers return early while `activeFrontmatterEdit` or
`activeBlockEdit` exists (for example `openFrontmatterKeyEditor`, L853-L855, and the value opener);
the blur handler retries the save but never closes an invalid editor.

## Suggested direction

When another field is clicked while an editor is invalid, either revert the invalid editor
(with a toast "Change to priority discarded: must be <= 5") or scroll to it and flash it with an
explicit "Fix or cancel this value first" message. Add a visible Cancel control to every editor.

## Done when

Clicking a field always produces a visible response.
