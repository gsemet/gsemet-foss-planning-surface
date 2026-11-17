# CR 211 — Inspector review, round 1

Worktree: `markdown-okf-schema-studio-wt-211` (base `b9118506`). Scope: `git diff` plus
`scripts/new-features.py`; 29 untracked scenario/synth files spot-checked.

## Verdict: CHANGES REQUESTED

Items 1–4 are done and work (gates and dry runs below). Item 5 is not done: the no-op sweep still
derails on the case that caused the problem (the `*Next: [Chapter N](…)*` closing line of every
chapter), because both safeguards miss it (findings 1 and 2).

## Findings

1. **major**: `scripts/noop-sweep.mjs:30-34` (and the unused helper `isLinkOnly`, `:21-24`). The
   link-only test requires the block text to *equal* its links' text. The real target is
   `*Next: [Chapter 7 — Harness Engineering](07-harness-engineering.md)*` (06-guidelines-governance.md:513,
   the same in every chapter) and the shipped fixture `synth/linkonly.md` is `*Next: [Related](related-target.md)*`.
   Here the text is "Next: Chapter 7 …" and the link text is "Chapter 7 …", so `linkOnly` is false
   and the block gets clicked. The click lands at `x+min(40,w/2)`, which is on the link right after
   "Next: ". **Fix:** test the click point itself. In the page, compute the point the sweep will
   click from `getBoundingClientRect()` and check
   `D.elementFromPoint(px, py)?.closest('a[href]')`. If it hits a link, try another point in the
   block that is not on a link (for example the start of the first text node outside an `<a>`, or
   `x+4`), and if no such point exists, mark the block `linkOnly`/skipped. A looser rule also works,
   such as "the block has a link and its non-link text is at most about 12 characters". Either way,
   keep the in-page code and the exported helper the same, or delete the helper (now it is dead
   code that differs from the real logic).
2. **major**: `scripts/noop-sweep.mjs:108-112`, the navigation detection and the way back.
   (a) The click follows the link to *another Markdown document in the same preview*, and that
   document also has `[data-sphinx-source-line]` elements, so `!!D.querySelector(...)` stays true.
   The navigation is never detected and the later targets come back "not found": exactly the 210
   derail. **Fix:** before the loop, record the shown document's id
   (`D.querySelector('[data-sphinx-source-line]')?.getAttribute('data-sphinx-preview-document')`,
   an attribute the page already sets, see `src/page/features/mappedBlocks.ts:20`), and after each
   click compare it with the current one (wait about 500 ms, since a navigation re-renders
   asynchronously).
   (b) The way back is `Meta+1` then `Alt+ArrowLeft`. On macOS that focuses the text editor and
   moves the caret one word left; it is not "Go Back" (that is `Ctrl+-`), and the preview's history
   belongs to the panel anyway. **Fix:** click the preview's own Back button
   `[data-sphinx-preview-back]` (`src/core/preview/previewToolbar.ts:14`, wired in
   `src/page/modules/historyControls.ts`) with a real mouse click through `box(...)`. Then
   `waitUntil` the document id matches the recorded one, re-enable edit mode, and if it never
   matches, stop the kind with a clear error instead of continuing on the wrong document. Update
   the wording in `references/harness-pitfalls.md:81-87` and `SKILL.md:133-135` ("the document has
   no mapped block any more" is wrong).
3. **major**: `scenarios/c3-1-alert-lazy-continuation-outside.json:1` uses `"file":"synth/admon.md"`,
   but `assets/synth/admon.md` is not shipped, so the replay of QA210-04 cannot run from a fresh
   workspace. The CR ships "the QA 210 replay scenarios and synthetic fixtures". **Fix:** add
   `assets/synth/admon.md` with the fixture text from the archived sheet
   `04-archives/210-qa-campaign-2026-10-31/03-admonitions/c3-1-alert-lazy-continuation.md` (block
   under "Fixture (synthetic) `synth/admon.md`"). `linkonly.md` and the other fixtures are present,
   and every other scenario's `file` resolves (fixtures-visual 01/04/46/68, book 02/08, synth/*).
4. **minor**: `scripts/new-features.py:48-52`. The date comes from the index `Date:` first and from
   the revision's commit date only as a fallback. If a campaign ran days after its revision, PRs
   merged between the revision and the `Date:` are never searched (with `merged:>=Date`) and are
   silently missing from the table. The ancestry filter (`:93-96`) already drops anything inside the
   revision, so an early date costs nothing. **Fix:** with a known revision, use
   `min(rev commit date %cs, Date:)`, ideally one day earlier for the UTC/local offset of GitHub's
   `merged:` qualifier. Also print a warning when `len(prs) == 200` (the `--limit` was hit).
5. **minor**: `scripts/coverage-map.py:126-137`, `last_campaign_rev`. `index_revs` puts the
   canonical `Revision:` first, but the caller then takes the newest sha by commit date across all
   matches, so the priority is lost. An index that mentions a later commit in prose (for example
   "fixed in commit `abc1234`", as in 001's fix-plan files, which the `**/00-index.md` fallback can
   pick up) would replace the recorded revision. **Fix:** when an index has a `Revision:` match,
   use only that sha; take the newest of the prose matches only when no index has a `Revision:`
   line.
6. **minor**: `references/charters.md:121-125`. The charter-agent return has no `NEWFEATURE` line,
   yet the Driver must return `NEWFEATURE <PR> | … | <result>` lines (`:81`) and the Foreman builds
   the table from them (`:131`). The charter prompt only says "state in the return which PR
   behaviours you exercised" (`:119`), in free form. **Fix:** add
   `NEWFEATURE <PR> | <behaviours exercised> | <PASS|finding ids|not run>` to the charter return
   format.
7. **minor**: `references/charters.md:62,70-71`. A Driver's replay window
   (`QA_SESSION=<driver>-replay`) is not counted in its window allowance, so 3 Drivers each
   replaying while a charter runs can exceed the 2–3 window total. **Fix:** state that the replay
   window counts against the allowance (replay only when no charter window of the Driver is open).
   Also add a one-line fallback for when a sub-agent cannot start sub-agents in the harness: the
   Foreman then launches the charter agents of each Driver group itself and the Driver step becomes
   "replay + merge" only.
8. **minor**: `references/use-cases.md:62-63`. E3 and E4 still name `okfreq-examples`, an okf-schema
   corpus that is no longer copied. **Fix:** point them at `fixtures-visual/08-okf-schema.md`,
   `synth/frontmatter-edge.md` and `synth/related-target.md` (or say "no corpus in the workspace;
   build a synth fixture").
9. **nit**: `SKILL.md:8`, `previous-campaigns` metadata still lists only 001; add
   `.agents/changes/04-archives/210-qa-campaign-2026-10-31/`.
10. **nit**: `SKILL.md:72-73` lists the `new-features.py` flags without `--dry-run`, and that is the
    flag that matches the "dry run of the Scope step" wording of Done when. Add it.
11. **nit**: `scripts/setup-workspace.sh:61`, the vault rsync filter order
    `--include='*/' … --exclude='.git/' --exclude='.obsidian/'`: the first rule wins, so `*/`
    already includes `.git/` and `.obsidian/` before their excludes. The behaviour is not new, but
    the line was touched. **Fix:** put the two `--exclude` rules first, and add
    `--prune-empty-dirs`.

Checked and fine:
- engine.mjs coercion: only a field that is exactly one placeholder, under a key in
  `NUMERIC_FIELDS`, with an integer value. Array items inherit the parent key (`keys`/`key` are not
  numeric), and `text`/`type`/`insert` stay strings.
- setup-workspace.sh: `${BOOK_DIR-…}` lets `BOOK_DIR=""` skip the book. `${VAULT_DIR:-}` is safe
  under `set -u`. `copy_corpus` with an empty `src` prints "skipped (not set)". `--clone` is
  unchanged. okf-schema is gone. `output/` is git-ignored.
- coverage-map.py: the regexes match the 210 header ("at commit `b9118506`") and the template
  `Revision:` line. Fallback order: `--since` → `--campaign` → newest `04-archives/*qa-campaign*` →
  legacy 001. `QA_CHANGES_ROOT` is documented, and in a worktree without it the script prints a
  clear note.
- Docs: the Roles chain, parallel Drivers, a total budget of 2–3 windows, the Budgets row per
  Driver, the QA Driver prompt template, the new-feature table, the gap rule ("cannot be
  `completed`"), and the canonical `Revision:` line in the header template. Relative links resolve.
  Edited prose lines are ≤ 100 characters (only tables, prompt code blocks and the front-matter
  `description` are longer).
- Untracked synth/scenario files: synthetic text only ("Ada" and "Ada Lovelace" are placeholders;
  `vault-props.md` is a synthetic vault-style note). No personal notes, no absolute or vault paths.
  All 22 scenario JSON files parse.

## Notes for item 6 (next round)

- `SKILL.md:176` ("at most one JPEG per finding") and the charter prompt `references/charters.md:116`
  ("one evidence JPEG at most") must change to 2 (currently + expected, about 1000 px, `--clip`).
- Add "capture both shots" to the charter prompt Method. Add the evidence paths to the
  `FINDING` return line of both the charter return and the Driver return, so the Foreman can link
  them in triage without opening sheets.
- The triage step (Foreman after the returns) should say that the backlog item's `01-intent.md`
  copies the Currently / Expected block with links to the archived images.

## Gates (re-run by the Inspector)

| Gate | Result |
| --- | --- |
| `bash -n scripts/setup-workspace.sh` | OK |
| `python3 -m py_compile` coverage-map.py, new-features.py, fmt-probe.py, synth/ux25-export.py | OK |
| `node --check` on all 8 `.mjs` | OK |
| `coverage-map.py --campaign …/210-qa-campaign-2026-10-31` | `## Baseline: b9118506 from … (--campaign)`, 0 commits since |
| `coverage-map.py` with `QA_CHANGES_ROOT=<main>/.agents/changes`, no `--campaign` | Falls back to the newest archived QA campaign: b9118506 |
| `coverage-map.py` in the worktree with no env | Clear note "no campaign found … set QA_CHANGES_ROOT"; explores every area |
| `new-features.py --campaign …/210` | Baseline 2026-10-31, revision b9118506; table `(none)`, correct: the 3 user-facing PRs of that day (#230, #234, #236) are ancestors of b9118506 and are dropped |
| `new-features.py --since 2026-10-31` | 3 user-facing + 3 test PRs listed apart (confirms the ancestry filter) |
| `new-features.py --campaign … --dry-run` | Prints the `gh pr list … merged:>=2026-10-31 …` command |
| `setup-workspace.sh` with `QA_ROOT=/private/tmp/…/insp-ws` | rc 0, 192 md files, vault skipped; `--clone t1` OK; `BOOK_DIR= VAULT_DIR=/nonexistent --force` → 134 files, both skipped with messages. Scratch deleted |
| noop-sweep live behaviour | Not run (no VS Code launch allowed); findings 1–2 come from reading the code against the archived c0-1 sheet and the white paper chapters |

The worktree is unchanged by the Inspector (no files added).
