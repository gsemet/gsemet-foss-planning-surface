# Answers

The QA report: `intake/ux-qa.md` (with its screenshots); the user's screenshots: `intake/borders.png`,
`intake/kanban-priorities.png`, `intake/detail-drawer.png`.

- design-Q1 (split): two CRs. The quick fixes go first, in their own CR `board-design-bugs`: the
  drawer's file list (the `.nm` class collision with the card band rule, the `.ind` collision
  with Triage's pill), the Kanban priority chips (browser button border, the meaningless grey
  square), the front matter rendered as a paragraph in `panel/markdown.js`, and the "---" titles
  from `status/views.py` `_title()`. This CR then does the full realignment.
- design-Q2 (rules): the report's proposed rules, as they stand: one white card with a hairline and
  a shadow only on what floats; never a box in a box (lists are rows with dividers, as the PRs
  page); no side bars; one chip, one filter chip, one segmented control; a type scale 11/12/14/16/24
  and radii 6/10/full; the front matter as a muted key/value list; the file list as a grid (icon,
  name, size right-aligned). The report's other findings (the Batch PR card's clipped gate line,
  the Costs KPI tiles teal against Home's white, Configuration's value shown three times, about 15
  font sizes, 12 radii, 7 chip styles) are realigned here too.
- design-Q3 (language): every user-facing string of the board goes through its translations (all
  French when the board is in French). The user (2026-11-17): "tout traduire et mettre une
  guideline qui s'active quand on touche à l'interface qui dit qu'il faut tout traduire": the
  project gets a rule, read whenever a change touches the board's web files, saying every string
  goes through the translations.
- The user put both CRs in the running batch (batch-24), 2026-11-17.

## Settled by the Chief of Staff

Choices the specification needed that the answers leave to the agents (2026-11-17, by the
Spec-writer on the Chief of Staff's brief); none changes a decision above.

- S1 (where the translation rule lives): one conditional line in the root `AGENTS.md`, with its
  detail in `CONTRIBUTING.md` ("Words"), enforced by a test in `just check`. Reason: `AGENTS.md`
  is what every session of this repository loads (Claude Code and Copilot alike) and the root that
  `chantier rules` lists for every role before its card; the repository has no folder-scoped rule
  mechanism (no nested `AGENTS.md`/`CLAUDE.md`, no `.github/instructions/`), and one added would
  serve one host only and would not be listed by `chantier rules`, which follows links from the
  root file only.
- S2 (what "every string" covers): every word the board composes (text, `title`, `aria-label`,
  `placeholder`, `alt`, toasts, dialogs, empty and loading states) goes through `t()`/`tn()`. A
  value the server sends as a fixed code (a configuration layer's name, a PR state, a check state)
  is mapped through `t()` by its code. Free text that is data is shown as it is, inside a
  translated frame: file contents, titles, slugs, role descriptions from the shipped defaults, a
  CLI refusal or diagnostic, a waiver's rule quoted from `AGENTS.md`.
- S3 (glossary): a French value equal to its English one is allowed only for a key the test lists
  by name, and only for a chantier name (CR, PR, batch, round, slot, worker, Driver, Foreman, Chief
  of Staff, CoS, Inbox, Backlog, Grill, 3-ready, Stack, Kanban, Triage), a word that is the same in
  French (Configuration, Total, Budget, Mode, Agent, OK, Pipeline) or a format with no word
  (`{n} s`, `{batch} · {state}`, `Ctrl+S`). Anything else is translated (for instance Steering:
  Pilotage; automatable: automatisable; Label: Étiquette).
- S4 (priority chip): the neutral chip, a 6 px dot in the priority's ramp colour, the word in
  `--ink2`: the ramp's pale end (P4) is unreadable as text on the chip's grey.
- S5 (swatches): a label's or priority's swatch is a 6 px dot (`--radius-full`), as a radius of 2 px
  is not on the scale.
- S6 (fixed component sizes): the chip's 20 px height and 6 px inline padding, and the file row's
  32/16/56 px, are component tokens in `tokens.css`, not spacing; spacing is the 4/8/12/16/24/32
  scale.
- S7 (sizes inside the drawer): the drawer's title and a rendered document's `h1` take the 16 px
  heading step (not the report's 18 px, which is off the scale); `h2`/`h3` 14 px/500.
- S8 (lists): every list of PRs is the PRs page's row with a divider: Home's open PRs and the Batch
  page's PR column included; the Costs tables stay tables, unboxed, rows with dividers.
- S9 (Kanban and Triage groupings): a Kanban column keeps a `--col-fill` field without a line (the
  columns sit side by side and take drops); a Triage lane is an unboxed section, a heading and a
  top hairline, as the report's table says.
- S10 (Costs receipt): on screen the receipt is a flat card on the board's type scale; the paper
  ticket (grain, scissors, perforation, its large figures as `--ticket-*` tokens) is drawn only in
  the "Copy as image" export.
- S11 (PR state chip): draft, merged and closed keep their state's tint and icon; an open PR, which
  is no chantier state, shows the neutral chip with no icon.
- S12 (phone bar): four views and More (Home, Triage, Kanban, Batch; More opens PRs, Costs and
  Configuration).
- S13 (the sticky header): its shadow becomes a bottom hairline; a selection or focus ring
  (`0 0 0 Npx`, no blur) is not a shadow and stays.
- S14 (evidence): the before/after screenshots come from `scripts/docs_screenshots.py`, extended
  with `--lang`, `--out` and `--root` and a PRs step, in French (the user's language), at
  1400x860 and 375x812; the docs screenshots are refreshed in English as today.

- realign-Q1 (the user, 2026-11-17, overrules S10): the Costs receipt stays a paper ticket on screen
  (with the red "PAS FINI" stamp of costs-receipt-not-finished-stamp on it); only what surrounds it
  is realigned.
- realign-Q2 (the user, 2026-11-17, confirms S3): chantier's own names stay English in the French
  board (CR, PR, batch, round, slot, worker, Driver, Foreman, Chief of Staff, Inbox, Backlog, Grill,
  Stack, Kanban, Triage); everything else is translated.