---
title: Grill answers
date: 2026-11-11
---

# Grill answers

- Run now (owner, 2026-11-11: "Export single html et les findings"), as one stack of six PRs, bottom to top: 290, 289, 293, 292, 291, 288. The owner merges the stack.
- No GitHub issue (`issue: none`).

- Export a single page as one self-contained `.html` file: the current preview theme and width, its CSS inline; local images as data URIs; Mermaid, PlantUML and Vega diagrams frozen as inline SVG; no JavaScript at all (tabs and dropdowns in plain HTML/CSS). URL links kept; relative links to other files removed, with a warning listing them before the export. Front matter properties table collapsed by default; when expanded, the field descriptions (from the OKF schema, when available) are shown. Review comments (TODO and THREAD chips) and all editing chrome excluded. Entry points: a command "Export to HTML" and a toolbar button; a save dialog that defaults next to the `.md` file. A new rendered output: the Inspector uses Opus (blast radius 2).

## Answers to the spec's questions (2026-11-11)

- Q1 toolbar button: in the main row, "for now": Refresh, Edit, Export, then the collapse button (the main row holds four buttons; TOOLBAR-001 is amended for that row, the other rows keep at most three).
- Q2 zoom: not kept; the file is at 100 %, the width mode and max width are kept.
- Q3 Restricted Mode: export allowed.
