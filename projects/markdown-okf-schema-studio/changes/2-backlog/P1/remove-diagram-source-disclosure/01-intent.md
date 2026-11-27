# Remove the "Diagram source" disclosure under diagrams

## Intent

A reader of a page no longer sees the collapsed **Diagram source** disclosure under a diagram: the
owner finds it useless.

## Decided (owner, 2026-11-27)

- Priority P1.

## To grill

- Which surfaces: the preview only, as for **Chart source** since 1.13.0, or the HTML export too.
- A diagram that fails to render: does its source stay visible.

The code and requirement facts are in `intake/request.md`.
