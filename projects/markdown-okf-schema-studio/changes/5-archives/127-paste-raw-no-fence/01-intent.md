# Pasting a large document in edit mode wraps it in a quadruple-backtick fence

Type: fix · Priority: P1 · Reported 2026-10-27 after the demo tour of the P1 stack

## Intent (user)

- Open an empty Markdown file, switch to edit mode.
- Paste a very large document: it is pasted inside a ```` (quadruple-backtick) fence.

## Expected

Pasting into a block editor inserts the clipboard text as is (raw Markdown), whatever its size and
content. No fence is added around it.

## Before starting the CR

Reproduce it in a real VS Code window: find the size or content (code fences inside the pasted text,
front matter, length) that triggers the fence, and which paste path adds it. The e2e pastes a large
document containing fenced code blocks into an empty file and must fail on the current code.
