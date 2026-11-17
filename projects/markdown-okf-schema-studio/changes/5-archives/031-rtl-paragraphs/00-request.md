# 031 — rtl-paragraphs

From backlog `P3/rtl-paragraphs` (files copied here as `backlog-*` / images).

## Problem

K2: plain Hebrew/Arabic paragraphs are left-aligned; raw `dir` is stripped by the sanitizer.

## Decisions (user grill, 2026-10-22 night plan)

1. Emit `dir="auto"` on block elements (paragraphs, headings, list items, blockquotes, table cells) so RTL text right-aligns like GitHub.
2. Allow the `dir` attribute in the sanitizer allow-list (values `ltr`, `rtl`, `auto` only).
3. Remove `knownIssue: "P9-B4-K2"` from rendering-core/v17, v18 (fixture 35-cjk-rtl) and add content assertions: RTL paragraphs right-aligned, LTR unchanged, no horizontal scroll.

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
