# Run brief addendum (2026-10-27, run 5) — CRs 137–147 on the same stack as CR 135

Read with [RUN-BRIEF.md](RUN-BRIEF.md) (run 4, CR 135); its run rules, cost rules and return format
apply. The user asked: every P1 and P2 item, plus the P3 items `external-edit-glow` and
`plantuml-jar-include-confinement`, "sur la stack en cours, dans des nouvelles PR", organised to
optimise delivery when changes overlap.

## Stack (bottom → top), base main

135 (one PR, 26 tasks) → **137** plantuml-jar-include-confinement → **138** table-column-min-width
→ **139** external-edit-glow → **140** edit-mode-tag-in-block-title → **141** readme-html-guaranteed
→ **142** toc-marker → **143** heading-folding → **144** find-and-replace-in-preview (two backlog
items, one PR) → **145** paste-url-as-link → **146** drop-file-as-link → **147** rich-diff-side-by-side → **148** myst-cards-tabs-version-directives (added 2026-10-27 late) → **149** vega-lite-charts-full-mode (adds dependencies, own `npm ci`) → **150** writing-skill-for-studio (documents everything below) → **151** dependency-update-security-floors (top of the stack; own `npm ci`, lock files change last).

## Scheduling

- Slots: up to 4 task drivers for CR 135 as today, **plus up to 2 CR drivers** for 137–147, started
  in stack order. Window tests stay serialised by `WINDOW-TESTS.lock`.
- A CR driver creates its worktree `../markdown-okf-schema-studio-wt-NNN` (branch
  `change-requests/NNN-<slug>`) from the **current tip of the CR 135 integration branch** (or of the
  ready CR just below it, when that one touches the same files: 140 → 141 → 142, 143 → 144,
  145 → 146), with a `node_modules` symlink to the main checkout.
- Drivers stop at step 7 + push, as in run 3 (`reports/PR-BODY.md`, no PR).
- **Stack driver**, once CR 135's PR is open and each CR is ready or blocked: rebase each branch
  onto the one below (first onto CR 135's branch), resolve conflicts (Opus for a hard one, in
  particular against CR 135's T26 module split), `just check` on each, open the PRs ready,
  `gh stack link --base main <135's PR> <137 …147>` (bottom → top), CI in ≤5-minute slices,
  heavy CI on the top branch at the end. A red CR goes back to its driver as a new round.
  Keep `STACK-STATE.md` current (create it).
- Blocked CR (round 3 failed): out of the stack, listed with a question and a recommended answer;
  the others continue.

## When CR 135 lands (after the user merges)

Archive the audit folder `02-backlog/P3/audit-performance-security-maintainability/` with CR 135
(its report is closed by CRs 132, 133, 135 and 137).
