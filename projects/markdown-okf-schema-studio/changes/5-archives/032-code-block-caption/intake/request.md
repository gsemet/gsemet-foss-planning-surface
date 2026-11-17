# 032 — code-block-caption

From backlog `P3/bug-code-block` (files copied here as `backlog-*` / images).

## Problem

A MyST ```{code-block} renders its code centered and its :caption: as a floating centered italic line.

## Decisions (user grill, 2026-10-22 night plan)

1. Code inside {code-block} is left-aligned like a plain fenced block (find the centering rule: likely a figure/caption container style).
2. Decision: the :caption: becomes a title bar attached to the top of the code block: left-aligned, light monospace, same width and border as the block, square top joint (like the file name header on GitHub or Sphinx Book), readable in light, dark, cream and current theme.
3. Keep line numbers, emphasize-lines and the copy button working; plain fences unchanged (byte-identical PNGs for existing scenarios that have no {code-block}).

Night rules: blocked on a real product decision → apply the driver's recommendation and list it in the PR under "Décisions prises en autonomie" (Autonomous decisions).
