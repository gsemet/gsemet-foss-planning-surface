# Verification of CR-225 (first pass)

Head: 7987e83bdca2175933c099685fcbce79b4dffaf2 (branch chantier/batch-17/cr-225-change-specification-the-board-s-reading, worktree clean)

Verdict: NOT VERIFIED. One claim of the specification fails (the picker's check mark); one part of
E10 is not complete. Everything else proved at this head is below.

Proofs are in `work/verifier/evidence/`; the throwaway scripts (`verify_shots.py`, `cmp2.py`, `qa.py`,
`e7b.py`, `e4_check.py`, `idle.py`) are in `work/verifier/`. The board ran from the worktree's own
code (`uv run --project <worktree> chantier board`) on scratch planning folders (a 3-project surface
holding a copy of this repository's planning folder, and three single-project repos made with the CLI).

## Failed claims

1. Spec "Project picker": "The current line carries a check mark." At 7987e83 the open menu marks the
   current line only with a tinted background (`.menu .row.on` in `css/shell.css`); `ui/picker.js`
   `row()` and the "All projects" row draw no check mark, whereas the prototype (`v6-01`) draws one
   on the right of the current line. Proof: `evidence/compare-picker-pc.png` (and `-phone.png`);
   `Grep check` over `web/` finds no check icon in the picker. Not one of the allowed differences
   (not a later CR's, not English words, not data, not a named fix). The coder's `qa/checklist.md`
   does not list it, and it had no side-by-side image of the picker, the panel or the bottom bar.
2. E10 / Final QA step 3, completeness: the coder's `qa.py` made compare images for Home, Kanban, Batch,
   Costs and All projects only. The Verifier made the missing ones (see E10) but the PR must carry the
   corrected picker; the rest of the set is attached here.

## Claims proved, with command and output (all at 7987e83)

- **E1 (Windows).** `just check` from the worktree: exit 0. Output `evidence/e1-just-check.txt`: ruff
  "119 files already formatted", "All checks passed!", mypy "no issues found in 99 source files",
  `uv lock --check` ok, Biome "Checked 60 files in 21ms. No fixes applied.", pytest "68 passed in
  16.98s" (includes the structure test `test_code_targets.py`), release-notes ok.
  CI on Linux and macOS: UNVERIFIED (CI only).
- **E2.** The coder's two transcripts at this head (`scenario/results/github-20261114-113427.md`: 756/756,
  `gitlab-20261114-115321.md`: 737/737, gate log `work/gates/20261114-101601.log` "result: pass at
  7987e83...") hold, in 16c, `GET /` with the cookie is HTML, policy `script-src 'self'` with no
  `unsafe-inline`; `js/main.js` as text/javascript with an ETag; policy `'self'` only; every module and
  stylesheet answers 200 with its type; a second request answers 304. Extracted lines:
  `evidence/e2-scenario-board-lines.txt`. I did not rerun the 40-minute scenario: I read the transcripts.
- **E3.** Line counts of all 60 static files: `evidence/e3-lines.txt` (largest JS `semantics.js` 171,
  `fr.js` 225; largest CSS `shell.css` 251; none over 300). One module per view: home, kanban, batch
  (+ batch-graph, batch-prs, batch-pr-card), costs, overview. `innerHTML` appears only in
  `core/dom.js:41` (`element.innerHTML = textOf(markup)`); no `style=`, `insertAdjacentHTML`, `eval` or
  `document.write` under `web/`; colours (`#hex`) only in `tokens.css`.
- **E4.** `evidence/browser-run.txt`, `evidence/e4-precise.txt`: a CR titled
  `Board <b>bold</b> <img src=x onerror=alert(1)>`, a backlog item with the same title and a
  `<script>alert(2)</script>` line in its intent, `evil.svg` (script) and `evil.md` in the CR folder.
  In Home, Kanban, Batch, Costs and both panels: 0 `img[src=x]`, 0 `[onerror]`, the only `script` in the
  page is `main.js`, the markup is shown as text, 0 dialogs, 0 console messages, 0 failed requests.
  `evil.svg` shows "cannot be shown here" with a Download link; `evil.md` shows `<script>...` as text.
  Minor oddity (not a failure): in `evil.md`, `[l](javascript:alert(5))` renders as `l)` (the
  renderer's link pattern stops at the first `)`); it is not a link and runs nothing.
- **E5.** `evidence/e5-tree.txt`, `e5-panel-spec-pc.png`, `e5-panel-image-pc.png`: CR-222's folder
  (70 files) opens in the panel: top files (`01-intent.md` ... `depends.json`), `evidence/ · 43` with its
  nested `prototype/v*-*.jpg|png` names, `intake/ · 2`, `prototype/ · 8` with `v1/data.js`,
  `v1/index.html`, `v1/snapshot.py`, `work/ · 11`. A PNG opens as an image (naturalWidth 510).
  `prototype/data.js` is listed as 1.5 MB and, when clicked, says "too large to show as text".
- **E6.** On the Batch view with a panel open: `chantier note` and `chantier round` from the CLI;
  within 9 s the page shows "r2/3" with no reload, the panel is still open, its head unchanged.
  Idle: 0 DOM mutations in `#view` over 13 s with no data change (`evidence/idle-redraw.txt`).
- **E7.** Scratch batches made with the CLI: `evidence/e7-parallel|series|stack-batch-pc.png` and
  `e7b-*-batch-pc.png` (with one CR handed back ready, PR #61/#71/#81), texts `e7b-*-pr-column.txt`.
  Shown with the spec's words: parallel hint "...in the order they became ready; the release after the
  others" and "on main"; series hint "From bottom to top..." and the series band sentence; stack hint
  "The stack is not built and verified on the forge yet: its PRs stay drafts...", "Drafts, not to
  review yet · 1", "on main · not stacked yet", "handed back, draft PR"; blocked CR with a red group;
  queued CR "waits" (orange); an open dependency (`↳ 1`); a release; levels "No dependency" / "Level 1:
  after level 0". Live batch-17 (`compare-batch-pc.png`) shows a draft "on CR-222, its open
  dependency · not stacked yet". NOT shown by a scratch screenshot: a fix CR's card ("on main, outside
  the stack") and the series "draft until it merges" base on a second CR (the CLI needs a worktree and
  pushed branch per CR; a fix was set in `batch.json` of the stack case but has no PR). Partial.
- **E8.** In-project (the repository's own planning folder, board on port 8824): no picker button, nav
  "Home, Kanban 47, Batch batch-17, Costs". Surface of three projects (chantier = copy of this
  repository's planning folder, empty, small): menu "Planning surface · 3 projects", "All projects",
  one line per project with its mark, dot and "batch-NN · state · N in intake" / "no batch";
  overview shows only Home in the sidebar and the bottom bar, no counts, no actions button on PC;
  `?p=*&v=kanban` opens `?p=chantier&v=kanban`. `evidence/picker-pc|phone.png`, `overview-pc|phone.png`,
  `bottombar-project-phone.png`, `bottombar-all-phone.png`, `e8-in-project-home.png`.
- **E9 (cold cache, Windows).** `UV_CACHE_DIR` and `npm_config_cache` set to new empty folders outside
  the repository: `just lint` exit 0 in 13.7 s, downloading nodejs-wheel-binaries (40.5 MiB); Biome
  "Checked 60 files ... No fixes applied."; versions printed: `Version: 2.6.7` (Biome), nodejs-wheel
  24.19.0. `evidence/e9-cold-lint.txt`. Cold fetch on Linux and macOS runners: UNVERIFIED (CI only).
- **Keyboard, console, origins.** Enter on a focused card opens the panel, Escape closes it, Escape
  closes the picker menu. Across all runs (PC and 375x812 touch): 0 console errors or warnings,
  0 failed requests, 0 requests to another origin, 0 dialogs (`evidence/browser-run.txt`, last lines).
- **E10 (side by side, PC and phone).** `evidence/compare-<view>-<pc|phone>.png`, each captioned with the
  view, width, v6 reference and `head 7987e83`: home, kanban, batch, costs, all (coder's `qa.py`,
  re-run by me on a fresh scratch surface) and picker-pc, picker-phone, panel-spec-pc,
  panel-spec-phone, panel-image-pc, bottombar-project-phone (mine, `cmp2.py`). Prototype `data.js`
  regenerated by `snapshot.py` from the same planning folder. Re-judged differences (all allowed,
  class in brackets): English/French words [words]; prototype `+ New`, Triage, Labels row, Autosync
  card, snapshot banner, green autosync dot on phone [later CRs]; example projects, "0 PRs to review",
  spent $125 vs $124 and ages [real data]; Costs has no v6 shot. The one that is not allowed: the
  picker check mark (failed claim 1). No compare image for the bottom bar on "All projects" and for the
  swiped second Kanban column on the phone (board shots only: `bottombar-all-phone.png`).

## Known and accepted (not failures)

Static folder is `board/web/` (spec says `static/`); JS cap 300 lines; Biome replaces ESLint, Stylelint
and Prettier (no cyclomatic or nesting rule: cognitive complexity 10 and the structure test stand in; no
`noUndeclaredVariables` rule seen in `biome.json`); a stack's PRs stay drafts (no stack-verified fact in
the record); `evil.svg` offered as a download; real phone is the user's ("not checked on a real phone");
CI on Linux and macOS UNVERIFIED.

## Needed to reach VERIFIED

Draw the check mark on the current line of the picker menu (project rows and "All projects", PC and phone),
update `compare-picker-*.png`, and name the fix CR / bottom-bar-on-All comparison in the PR if kept.

---

# Second verification (move 7987e83..b398cd4)

Head: b398cd487cdde724e00f6268a1e1e0ea522162b4 (worktree clean). Verdict: VERIFIED (Windows; CI on Linux and macOS UNVERIFIED; long gate waived by the user).

- Picker claim (failed at 7987e83): proved. Board run from the worktree on a scratch 3-project surface (HOME, USERPROFILE, CLAUDE_CONFIG_DIR at scratch folders; process stopped). The current line carries a check mark on a project row (chantier) and on "All projects", PC and 375px phone: evidence/compare-picker-pc.png, -phone.png, -all-pc.png, -all-phone.png, captioned head b398cd4. Other lines carry none.
- `just check` at b398cd4, Windows: exit 0 (ruff 139 files formatted, mypy 119 files no issues, lock ok, Biome 60 files no fixes, pytest 69 passed including the structure test, release-notes ok).
- Carried from 7987e83: E2 (scenario 16c transcripts), E3-E8, E10 other images, keyboard/console - the restack touched CLI core/declare modules and not the board's web files; not re-run, and the scenario step 16c was not rerun (long gate waived). The restack's 915/594-line diff is in crs/ids/records/declare and tests, covered only by the pytest and mypy results above.
- Still not shown: fix-CR card and series "draft until it merges" on a scratch screenshot; bottom bar comparison on All projects.


---

# Third verification (rebase move b398cd4..6675cfe)

Head: 6675cfedb982cd910c707f93a784d2edad76f1f2 (worktree clean). Verdict: VERIFIED (Windows; CI on Linux and macOS UNVERIFIED; long gate waived by the user).

- `just check` from the worktree: exit 0 (ruff 138 files formatted, mypy 118 files no issues, lock ok, Biome 60 files no fixes, pytest 69 passed, release-notes ok).
- Board smoke at 6675cfe, run from the worktree's code on a scratch 3-project surface (HOME, USERPROFILE, CLAUDE_CONFIG_DIR at scratch folders; process stopped by id): the picker's current line carries a check mark on a project row (alpha) and on "All projects", PC 1400px and phone 375px (the other lines carry none); Home and Kanban load; 0 console errors or warnings, 0 HTTP errors. Shot: scratchpad/pick-phone-proj.png.
- Carried from b398cd4: E2-E10, keyboard, picker compare images - the move replayed the same 4 commits with no conflict; only the base changed.


---

# Fourth verification (rebase move 6675cfe..6752f2e)

Head: 6752f2e02ea1a1cc55e5f5e961748ed9d57f4b2f (worktree clean). Verdict: VERIFIED (Windows; CI on Linux and macOS UNVERIFIED; long gate waived by the user).

- `just check` from the worktree: exit 0 (ruff 140 files formatted, mypy 120 files no issues, lock ok, Biome 60 files no fixes, pytest 69 passed, release-notes ok).
- Board smoke at 6752f2e, from the worktree's code on a scratch 3-project surface (alpha, beta, chantier; HOME, USERPROFILE, CLAUDE_CONFIG_DIR at scratch folders; process tree stopped by id): the picker's current line carries exactly one check mark on a project row (alpha) and on "All projects", PC 1400px and phone 375px; Home, Kanban, Batch and Costs load; 0 console errors or warnings, 0 HTTP errors. Shot: scratchpad/v4-pick-pc.png, v4-pick-phone.png.
- Carried from 6675cfe: E2-E10, keyboard, compare images - the move replayed the same 4 commits with no conflict; only the base changed. The file panel was not opened in this smoke.


---

# Fifth verification (restack 6752f2e..6b6512c)

Head: 6b6512c1740457f3e66637012ddf0e829558baf9 (worktree clean). Verdict: VERIFIED (Windows; long gate waived). just check exit 0 (mypy 122 files, pytest 69 passed, Biome 60 files). No board web file differs from 6752f2e; board smoke carried. CI at check time: just check on ubuntu, macos, windows pass; eval-dry-run pass; scenario pending.
