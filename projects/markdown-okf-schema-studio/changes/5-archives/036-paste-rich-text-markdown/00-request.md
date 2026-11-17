# 036 — paste-rich-text-markdown

From backlog `P3/paste-html-or-image` (files copied here as `backlog-*` / images).

## Problem

Pasting rich text (HTML clipboard) in edit mode inserts raw text; images already paste (CR 018).

## Decisions (user grill, 2026-10-22 night plan)

1. Decision: convert `text/html` clipboard content to Markdown with an in-repo converter based on parse5 (already a dependency; NO new dependency): headings, bold, italic, strikethrough, links, nested lists, inline code, code blocks (language from class when present), blockquotes, simple tables (GFM pipe), images as links. Everything else becomes plain text. Sanitize: drop scripts/styles/comments/event attributes.
2. Decision: Cmd/Ctrl+Shift+V pastes plain text unchanged. Image paste (CR 018) unchanged.
3. Unit tests: a table of HTML inputs (Google Docs, Word, a web page snippet, VS Code copy) → expected Markdown; undo is one step.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
