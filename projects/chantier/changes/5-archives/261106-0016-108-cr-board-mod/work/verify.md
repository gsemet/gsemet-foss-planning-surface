# CR-108 verify, head 88bff7535f0eb3bc78445438324608ea9793058f

Worktree `C:\Users\gaeta\Projets\chantier.worktrees\cr-board-CR-108`. Proof in `../evidence/`.

## Done when, item 1: `just check` and `just scenario`
- `just check` run by me at the head: exit 0, `26 passed in 4.07s` (evidence/just-check.txt).
- `just scenario`: not rerun; I read the coder's gate log (work/gates/20261106-010646.log) at the same head:
  github 172/172 and gitlab 172/172. The transcript has the checks: the index gives each batch `heartbeat` and
  `orders_pending` and each row `blocked`, `silent_minutes`, `folder`; the index lists landed CRs with state, batch, PR,
  cost, time, folder; the trashed CR with a total; "keeps the last 50 landed CRs, newest first, and counts them all".
- Own run of the worktree CLI on a throwaway repository (scratchpad `throw`, not the main checkout): 55 archive
  folders, 1 trashed. Index (evidence/throwaway-index.json): schema 2, `landed` 50 entries, `landed_total` 55,
  newest first (CR-55 ... CR-6), `trashed` 1 / `trashed_total` 1. A full entry: cr, title, state, batch, pr, cost_usd,
  when `2026-11-28T10:00:00Z`, path `../4-archives/...`. A folder with no STATUS.json gives `null` fields and a title
  (folder name for an archive, `_title` for the abandoned inbox item "Add csv export"). Not shown by me: real
  `batches` entries and row fields (no batch in the throwaway); the scenario covers them.
  Note: a STATUS.json with a UTF-8 BOM reads as empty (nulls); my first seeding hit it. Not a defect (the CLI writes none).

## Item 2: plugin tools and mod tests
- `claude plugin validate .` (binary `(Get-Process -Id $env:CLAUDE_PID).Path`, 2.1.309): exit 0, "Validation passed with warnings"
  (evidence/plugin-validate.txt).
- `claude plugin test .`: exit 0, 17 pass, 0 fail (evidence/plugin-test.txt). Tests cover: opening from the skill with
  prompt unchanged, the toggle, worktree path, outside git, unchanged mtime not reread, no timer after close, missing
  index, bad file / other schema, path leaving the checkout as plain text, plus folding, silent Foreman, sheets,
  size/UTF-8, links.
- Type-check: real `tsc` 5.9.3 with the engine's d.ts, command in work/coder/r2.md, rerun by me: exit 0, no output (evidence/tsc.txt).

## Item 3: run in the desktop app on this repository: NOT RUN
Reason: the plugin loads from the main checkout, and the mod is in the worktree/PR only; it loads once merged
(or with the branch checked out in the main checkout, which I must not do). I did not simulate it, and nothing above is
proof of it. What a person does: after merge, `/reload-plugins` in Claude Desktop in this repository, open the chantier
skill (pane opens) or run `/chantier-board`; check the board shows the real state; run `$CHANTIER file "x"` and see it
within 15 seconds; press a CR, then a document, and go back.

## Not checked
- "Copilot ignores the `hooks/` folder": not exercised by me (no Copilot host here).

## Verdict
VERIFIED for items 1 and 2 (check, plugin validate/test, type-check, index on a throwaway repository; scenario by log at
the same head). Item 3 NOT RUN.
