# Study v2: the card mechanism, redone on origin/main

Fable study for `simplify-cards-and-prompts`, 2026-11-24, on `origin/main` at `8a960d34`
(chantier 0.15.1 plus 21 commits beyond `3c29dd7c`, the base of the first study,
`work/study-fable.md`). Read-only: the tree was read from `git archive origin/main`, no card,
wrapper or code was changed, no writing `chantier` command was run, the main checkout was not
touched. Sizes are LF bytes (the form `test_start_reading.py` measures); the first study gave raw
bytes, about 1 % more.

## 1. Summary (one page)

**CR-471 cut the three big cards into 32 pieces by moment and deleted no text. The cards are now
829 KB (800 KB at the base, +3.6 %). The declared start reading fell a lot for the Foreman and
the Chief of Staff; the real reading is not measured yet, and for a session that runs a whole
batch the total is about the same as before.**

| Role | Declared start reading, base | Declared, origin/main (Claude / Copilot) | Measured real reading on the OLD cards (mean) | First study's target |
| --- | --- | --- | --- | --- |
| Chief of Staff | 380 KB | 202 KB / 111 KB | 218 KB (n=5) | 40 KB |
| Foreman | 292 KB | 91 KB / 84 KB | 144 KB (n=3) | 25 KB |
| Griller | 162 KB | 145 KB / 54 KB | 36 KB (n=6) | 12 KB |
| CR driver | 25.1 KB | 27.2 KB | 44 KB (n=279) | 12 KB |
| Stack driver | 66.3 KB | 34.1 KB | 56 KB (n=35) | 15 KB |
| Release driver | 47.5 KB | 25.8 KB | 28 KB (n=16) | 10 KB |
| QA driver | 36.1 KB | 24.1 KB | no run | 5 KB |
| Verifier | 23.1 KB | 24.0 KB | 17.5 KB (n=341) | 4 KB |
| Other workers | 11 to 15 KB | +0.8 KB each | 4 to 11 KB | 3 KB |

Five facts that change the first study:

1. **No role has yet run on the new cards on this machine.** The plugin loads from the main
   checkout, which is still at `3c29dd7c` (21 commits behind `origin/main`). Every card read in
   the transcripts, the 156 runs after CR-471's merge included, is of the old files. The "after"
   column above is a declaration, held by a test, not a behaviour.
2. **The cut moved text; it removed none.** Entry cards are 32 KB (Chief of Staff), 37 KB
   (Foreman) and 55 KB (Drivers), against budgets of 6, 4 and 4 KB in the first study. Trial
   marks, dates and batch names are untouched (113 "unproved", 68 dates in
   `hosts/claude-code.md`, same count in both trees).
3. **Most of the Foreman's declared cut comes from reading sections of `concepts.md` and of the
   host card, not from the card's cut:** 136 of the 201 KB saved. Real Foremen already read
   only 8.8 KB of `concepts.md` and 66 KB of the host card, so the expected real gain is 0 to
   30 %, not 69 %.
4. **None of the proposed tools exists.** The CLI has the same 47 commands: no `next`, `help`,
   `brief`, `msg`, `inbox`, `judge`, `conflicts`, `retro`, `reply-check`, `host`, `roles`. What
   landed is partial: a `batch:` state line and `handed back:` lines in `status`, a Foreman
   watcher for three forge events, `watch --stream`, a `restack owed:` line, lease refusals that
   name the command.
5. **The pieces are ready-made help topics, with no carrier.** A role reaches a piece by
   remembering a list of moments, opening a 5.4 KB JSON manifest and resolving `@` references.
   The CLI names a card file in two outputs only. `help <topic>` and "the refusal names the
   topic" would now cost little: the 32 files exist (median 6.5 KB, 0.9 to 37.8 KB).

The first study's design stands. Its order of work changes: the cut by moment is done as files,
so the next steps are the carrier (CLI), the shrinking of the entry cards and the host card, and
a real measure of the new cards before more text moves.

## 2. Measures

### 2.1 Sizes, base against origin/main

| Family | Base (`3c29dd7c`) | origin/main | Change |
| --- | --- | --- | --- |
| Chief of Staff | 204.1 KB, 1 file | 210.3 KB, 10 files | +6.2 KB |
| Foreman (without `foreman-stack.md`) | 84.7 KB, 1 file | 89.6 KB, 8 files | +4.9 KB |
| Drivers | 134.0 KB, 1 file | 137.7 KB, 17 files | +3.7 KB |
| `foreman-stack.md` | 16.5 KB | 16.5 KB | +0.1 KB |
| `concepts.md` | 73.0 KB | 73.3 KB | +0.3 KB |
| Host cards (2) | 127.1 KB | 128.8 KB | +1.7 KB |
| Session-start (3) | 24.8 KB | 26.8 KB | +2.1 KB |
| Worker cards (11) | 53.6 KB | 53.6 KB | 0 |
| Templates and layouts | 52.7 KB, 7 files | 61.9 KB, 8 files | +9.2 KB (`release-template.md` 5.4 to 12.2 KB, new `reload-rules.md` 1.6 KB) |
| Cores and manifest | 7.4 KB | 8.2 KB | +0.8 KB (manifest 4.6 to 5.4 KB) |
| **All of `references/`** | **800.0 KB, 37 files** | **829.0 KB, 70 files** | **+29.1 KB** |

The pieces (LF bytes):

| Chief of Staff | | Foreman | | Drivers | |
| --- | --- | --- | --- | --- | --- |
| `chief-of-staff.md` (entry) | 32,068 | `foreman.md` (entry) | 36,927 | `driver.md` (entry, 17 sections) | 54,955 |
| `-grill` | 37,371 | `-refused` | 13,460 | `driver-trouble` | 13,350 |
| `-steering` | 31,241 | `-lost-driver` | 11,440 | `stack-driver-changes` | 9,868 |
| `-merge` | 21,204 | `-merge` | 10,853 | `driver-retake` | 9,396 |
| `-batch-start` | 20,702 | `-hold` | 6,553 | `driver-conflicts` | 7,694 |
| `-any` | 19,819 | `-release` | 4,430 | `driver-pr-extras` | 6,240 |
| `-direct` | 19,600 | `-conflict` | 3,789 | `driver-handback-other` | 5,709 |
| `-batch-end` | 15,113 | `-pause` | 2,132 | `stack-driver-make` | 5,605 |
| `-release` | 11,846 | | | `driver-refused` | 4,577 |
| `-writer` | 1,346 | | | `release-driver-merged` | 4,453 |
| | | | | `stack-driver-restack`, `release-driver-notes`, `driver-session` | 3,562; 3,167; 3,044 |
| | | | | `stack-driver-joins`, `driver-matrix`, `release-driver-end`, `release-driver-ship` | 2,172; 1,658; 1,321; 896 |

Inside the entry cards the weight is where it was: `foreman.md` "Your means" 18.1 KB and "The
user's boundaries" 12.1 KB (`foreman.md:204`, `:59`); `chief-of-staff.md` "The project" 12.2 KB
and "Entry points" 8.5 KB (`:91`, `:19`); `driver.md` "Stack driver" 11.3 KB (`:443`).
`hosts/claude-code.md` is 109.9 KB, its "Configuration" 45.0 KB and "Tools" 21.4 KB.

The wrappers (`agents/`, `com.github.copilot/agents/`) are byte-identical in both trees. The
four `SKILL.md` went from 16.6 to 14.2 KB; one paragraph of 2,310 bytes (the `$CHANTIER` launch)
is still word for word in all four (2,656 bytes at the base).

### 2.2 Declared readings (computed from `startup-manifest.json`)

Script: boot = the cores, the manifest, the wrapper or skill, the role's `startup_sections`;
start reading = boot plus the first action(s), each byte once, `@action` references expanded,
the `{claude, copilot}` readings resolved per host. My figures equal the `AFTER` table of
`tests/test_start_reading.py:22-36` to the byte, and its comment's base figures (`:19-20`).

| Role | Boot, base | Boot, new | Start, base | Start, new Claude | Start, new Copilot |
| --- | --- | --- | --- | --- | --- |
| Chief of Staff | 11,636 | 11,708 | 380,314 | 202,396 | 111,492 |
| Griller | 11,197 | 11,267 | 162,192 | 145,087 | 54,183 |
| Foreman | 7,740 | 8,566 | 292,020 | 91,019 | 83,545 |
| CR driver | 8,519 | 10,541 | 25,134 | 27,180 | 27,246 |
| Stack driver | 8,542 | 10,564 | 66,302 | 34,054 | 34,116 |
| QA driver | 8,468 | 10,490 | 36,137 | 24,122 | 24,192 |
| Release driver | 8,577 | 10,599 | 47,462 | 25,806 | 25,866 |
| Verifier | 8,556 | 9,382 | 23,137 | 23,963 | 24,030 |
| Inspector | 8,552 | 9,378 | 14,596 | 15,422 | 15,484 |
| Coder | 8,531 | 9,357 | 13,140 | 13,966 | 14,000 |
| Other workers | 8.2 to 8.7 KB | +826 | 11.2 to 12.5 KB | +826 | +826 |
| Board-griller | 10,242 | 11,096 | 18,692 | 19,655 | 19,748 |

(The first study's "declared boot" column used another definition: 36 KB for the Chief of Staff
with the session-start files, 6 KB for the Foreman, 11 KB for a Driver. The table above uses the
test's definition for both trees.)

Per action, origin/main (Claude; Copilot differs only where a host card is read):

| Action | Bytes | Action | Bytes |
| --- | --- | --- | --- |
| `chief-of-staff` (entry, with `@session-start`) | 190,688 (Copilot 99,778) | `batch` (Foreman entry) | 82,453 (Copilot 74,798) |
| `session-start` | 123,063 (Copilot 32,153) | `foreman:merge` | 10,853 |
| `chief-of-staff:grill` | 38,717 | `foreman:hold` | 6,553 |
| `chief-of-staff:batch-start` | 20,702 | `foreman:lost-driver` | 16,514 |
| `chief-of-staff:steering` | 44,701 | `foreman:conflict` | 3,789 |
| `chief-of-staff:merge` | 21,204 | `foreman:release` | 4,430 |
| `chief-of-staff:batch-end` | 15,113 | `foreman:refused` | 13,460 |
| `chief-of-staff:direct` | 56,527 | `foreman:pause` | 2,132 |
| `chief-of-staff:release` | 11,846 | `foreman:reference` | 155,120 (Copilot 64,210) |
| `writer` | 74,632 | `batch:stack` | 16,546 |
| `cr-driver` | 14,487 | `stack-driver` | 21,338 |
| `cr-driver:ship` | 13,805 | `stack-driver:restack` | 14,232 |
| `cr-driver:closing` | 5,552 | `stack-driver:make` | 8,996 |
| `cr-driver:retake` | 9,396 | `stack-driver:changes`, `:joins` | 9,868; 2,172 |
| `driver:trouble` | 13,350 | `release-driver` | 13,055 |
| `driver:refused` | 18,037 | `release-driver:ship`, `:notes`, `:merged`, `:end` | 11,566; 3,167; 4,453; 4,712 |
| `driver:conflicts`, `:handback-other`, `:pr-extras`, `:session` | 7,694; 5,709; 6,240; 3,044 | `qa-driver` | 11,480 |
| `deliver` (`pr-template.md`) | 16,801 | `release` (`release-template.md`) | 12,155 (5,447 at the base) |

Declared whole paths, each byte once (Claude):

| Path | Base | origin/main |
| --- | --- | --- |
| Chief of Staff, one whole batch in Foreman mode (start, grill, batch-start, steering, merge, batch-end, status) | 397 KB | 360 KB (Copilot 269 KB) |
| Chief of Staff, a grill-only session (start, grill) | 380 KB | 241 KB |
| Foreman, usual batch (batch, merge, pause, hold) | 292 KB | 111 KB |
| Foreman, every piece but `foreman:reference` | 292 KB | 149 KB |
| CR driver, usual run (start, ship, closing, deliver) | 61.3 KB | 63.3 KB |
| Stack driver (start, restack, make) | 66.3 KB | 57.3 KB |
| Release driver (every step, with the template) | 52.9 KB | 61.9 KB |

Where the declared cuts come from:

- **Foreman, -201 KB:** the Claude host card whole (108.5 KB) became its "Tools" and "Heartbeat"
  (22.9 KB): -85.6 KB; the other host's card left the reading: -18.7 KB; `concepts.md` whole
  (73.0 KB) became "Starting an agent" and "Rules" (22.7 KB): -50.4 KB; `foreman.md` 84.7 to
  36.9 KB: -47.7 KB. The cut of the card is 24 % of the gain.
- **Chief of Staff, -178 KB on Claude:** `chief-of-staff.md` whole (204.1 KB) became the entry
  card and `-any` (51.9 KB): -152 KB; the Copilot card left: -18.7 KB. The Claude host card
  whole (109.9 KB) is still in the start reading, through `session-start` (`@host`): it is 54 %
  of the 202 KB.
- **Griller on Claude, 145 KB:** 110 KB of it is the same host card whole.
- **CR driver, +2.0 KB; QA driver, -12 KB; stack and release drivers, about half:** the three
  other Drivers no longer read the ship sections at start.
- **Every worker, +826 bytes:** the manifest grew (4,556 to 5,429 bytes) and it is in the boot.

### 2.3 Measured reading (transcripts)

**Re-measured, on the old cards.** Script over the Claude Code transcripts of
`~/.claude/projects` (2,825 files changed since 2026-11-20): for each run, the bytes of the
`Read` results of card files (file content, without line numbers) and of shell reads that name a
card path, each tool result counted once; a subagent's role from its `meta.json` agent type, a
Foreman from the first line `chantier Foreman n°`, a Chief of Staff or Griller from its skill.
For the window from 2026-11-20 21:00 UTC (the first study's, as far as I can tell: the run
counts match it):

| Role | Runs | Median / mean (v2) | First study (median / mean) | Largest files per run (v2) |
| --- | --- | --- | --- | --- |
| Chief of Staff | 5 (reads in the window only) | 202 / 218 KB, max 382 | 343 / 343 (n=2, whole sessions) | `chief-of-staff.md` 82 KB, host card 40 KB, `session-start.md` 21 KB, `foreman.md` 14 KB |
| Foreman | 3 | 139 / 144 KB, max 159 | 165 / 157 | host card 66.5 KB, `foreman.md` 54 KB, `foreman-stack.md` 11 KB, `concepts.md` 8.8 KB |
| Griller | 6 | 31 / 36 KB, max 115 | 56 / 81 (n=8) | `chief-of-staff.md` 16 KB, host card 9 KB, `griller.md` 3 KB |
| CR driver | 279 | 43 / 44 KB, max 125 | 45 / 46 (n=277) | `driver.md` 29 KB, `pr-template.md` 6 KB, `concepts.md` 4.7 KB, manifest 3.6 KB |
| Stack driver | 35 | 47 / 56 KB | 50 / 58 | `driver.md` 50 KB |
| Release driver | 16 | 31 / 28 KB | 32 / 30 | |
| Verifier | 341 | 14.6 / 17.5 KB | 15 / 18 | `verifier.md` 14.5 KB, `pr-template.md` 2.3 KB |
| Inspector | 339 | 6.0 / 10.9 KB | 6 / 11 | `inspector.md` 6.0 KB, `pr-template.md` 3.3 KB |
| Coder | 258 | 4.6 / 8.4 KB | 5 / 9 | |
| Spec-writer | 178 | 3.3 / 8.7 KB | 7 / 12 | |
| Spec critic | 103 | 4.1 / 9.4 KB | 6 / 11 | |
| Conflict resolver, Debugger, Investigator, Retro critic | 70, 33, 17, 11 | 3.6 to 4.5 / 3.6 to 6.2 KB | 3 to 5 / 4 to 7 | |

Total: 32.4 MB of card text in 1,806 runs (first study: about 38 MB in 1,829; my counter is
stricter on what is a card read). The CR driver is 38 % of it, the Verifier 18.5 %, the
Inspector 11 %. The per-file figures of the Chief of Staff, Foreman, Griller and Drivers are
from the wider window (from 2026-11-20 00:00 UTC, 2,282 runs, 44.0 MB).

**Reused from the first study, not re-measured:** the CLI output per session (Foreman 184 KB
over 180 calls, Chief of Staff 173 KB over 172 calls), the 17,000-token floor of a worker before
any card, the `status` size of batch-31 (5.5 KB). My own count of CLI output is partial (my
pattern misses some launch forms): 146 to 252 KB per Foreman session for 128 to 252 calls, on
three whole sessions, the same order as the first study.

**Post-CR-471 real reads: none exist.** CR-471 merged on 2026-11-24 at 11:39 UTC. After it, 156
runs read 2.93 MB of cards: all from the main checkout's old files (37 files in `references/`,
`chief-of-staff-any.md` absent), but 9 KB of piece files that batch-31's own Coders and
Inspectors read in their worktrees while changing them. The two Foremen alive after the merge
read no card in that time. What exists instead:

- three read-only "Fable readings" of the split, one per role, run for CR-471
  (`4-batch/3-done/471-…/work/fable-readings-findings.md`): no rule lost (334 of 334 blocks,
  1,128 sentences, 254 paragraphs), 20 findings on rules that no longer arrive at their moment
  or pointers left on the old layout; the commit `25c8cef9` says it fixed findings 1 to 5 of each
  role, `a94085d3` three more pointers. Chief of Staff 6, Foreman 6 and Drivers 6 to 8 are not
  in those commits' messages;
- the declared figures of 2.2.

**What the old real reading says about the new declared one:**

- The Foreman read 144 KB per batch on the old cards while 292 KB were declared: it already
  skipped most of `concepts.md` and a third of the host card. Its new declared start is 91 KB
  and a usual batch 104 to 150 KB with its pieces. The real gain is unknown and bounded at about
  30 %.
- The Chief of Staff read about 218 KB per session window on the old cards. Its new start alone
  declares 202 KB, and a whole batch 360 KB.
- The Griller reads 36 KB where 145 KB are declared: it skips the host card. The declared
  reading is not what roles do, in both directions.
- The CR driver reads 44 KB where the start declares 27 KB and the usual run 63 KB: it reads
  about two thirds of what its path lists. Its figures did not move with CR-471.
- Workers still ignore the cores and the manifest (about 0.2 KB per Verifier run), and nothing
  breaks: their printed opening lines still name only the card (`plugin_files.py:297`).

### 2.4 What the CLI prints now

Changed since the first study:

| Output | Change | Place |
| --- | --- | --- |
| `status` | second line `batch: shape …; slots n/m; steering …; rounds …; budget …; long gate owed: …; merges: the user…; rules: <path>/reload-rules.md` | `status/ready_line.py:110-128`, `commands/batch_status.py:308-310` |
| `status` | one `handed back:` line per ready CR: icon, word, PR link, `do not merge: waits for …`, `gaps:`, `owed before the merge:`, the long gate's result; "the agent copies them and judges nothing" | `status/ready_line.py:1-3`, `:85-107` |
| `status` | still one row per CR at each call, merged ones included; no `--since`, no delta | `commands/batch_status.py:320-323`, `declare/batch_status.py:19-35` |
| `watch --stream` | prints each block of events with a `still watching` line and runs on | `declare/watch.py:52-58`, `hub/watch_lines.py:62-65` |
| `watch`, run by the batch's Foreman | reads only its batch's `merged@1`, `checks-red@1` and `wait-cleared@1` lines, starts no server, ends when the batch closes or records another Foreman | `hub/watch_lines.py:68-84`, `hub/watch_reads.py:47-61` |
| `order merged` | `restack owed: … stood on <cr>'s branch; … send it the note …` in a stack batch | `commands/orders_merged.py:78` (`restack_line`) |
| `order after` | `--add`, `--remove`; a CR named by id, slug or path; the refusal lists the accepted forms | `commands/orders_after.py` |
| lease refusals | name the command to run | `core/leases.py:202-227` |
| `take`, `round`, `handoff` | print the base of the CR's place and the forge's base beside it | `commands/facts.py` |

Unchanged: 47 commands; `take`, `round` and `handoff` still print every worker role's opening
lines (`commands/facts.py:164`, `plugin_files.py:270-298`); the Driver's prompt is still a
skeleton to copy, whose reading lines name `startup-core.md`, the cores, the manifest and the
card (`driver_prompt.py:172-175`); `next:` lines exist in 4 places (`commands/endpause.py:47`,
`commands/opening.py:277`, `:333`, `rails_release.py:215`).

`--help` already states rules, and more than before: the top help is 13.3 KB (12.3 KB at the
base), the 47 command helps total 31.1 KB; `watch --help` (1.0 KB) holds the watcher's whole
contract (`declare/watch.py:7-25`), `order` 2.8 KB, `gate` 1.1 KB, `status` 1.1 KB. A role that
stumbles on a command gets its rule there today.

The journal still has 11 event types (`hub/schemas.py:187-293`), none written by one agent for
another.

## 3. What the cards hold, by kind

The first study's split (a to f) holds for origin/main: CR-471 moved blocks between files, and
its own readings count zero lost. I did not redo the estimate. What I checked:

- **(d) trial bookkeeping, unchanged:** `hosts/claude-code.md` holds 113 occurrences of
  "unproved", 56 of "proved" and 68 dates; `hosts/copilot.md` 33 and 4. The cards hold 75 dates
  and 73 batch names in both trees. (The first study gave 54 and 47: it counted another way; my
  count is the same on both trees.)
- **(f) duplicated, mostly unchanged:** the `$CHANTIER` paragraph, 2.3 KB, in the 4 `SKILL.md`;
  "No fallback" restated in 7 worker cards (`coder.md:20`, `inspector.md:18`, …) and in
  `startup-core.md`; the first-line refusal in the 30 wrappers.
- **(f) contradictory, one fixed, two left:** the manifest no longer lists both hosts' cards for
  one host (the `{claude, copilot}` readings and `@host`). Left: `role-core.md` ("at boot read
  only the cores, your wrapper and the manifest's startup sections") against the worker wrappers
  ("Your card …: read it first, before any other step", `agents/coder.md`); and the prompt
  template of `concepts.md:520` (cores and manifest) against the worker lines the CLI prints
  (card only).
- **New with the cut:** a role now needs the list of moments (`foreman.md:186-202`,
  `chief-of-staff.md:232-246`, `driver.md:19-26` and `:636-658`), the manifest and its `@`
  references to find a piece. `foreman:reference` reads the Claude host card whole (155 KB with
  "Words") for one section. `driver:refused` reads `foreman-refused.md` too (18.0 KB for a
  4.6 KB piece). The Chief of Staff's any-moment rules became one 19.8 KB piece read at every
  start (`chief-of-staff-any.md`), which is why its start grew by 21 KB inside CR-471
  (`work/from-cut-prompt-token-cost.md`).

## 4. The target design, item by item

### 4.1 The ten lines of the first study

| # | Design line | State on origin/main |
| --- | --- | --- |
| 1 | A card is a contract of 2, 4 or 6 KB | **Not done.** Entry cards 32, 37 and 55 KB; worker cards unchanged. Still the goal. |
| 2 | One shared floor of 1.2 KB added by the CLI | **Not done.** Closest thing: `concepts.md#Rules` (8.85 KB, `:711`) is now a declared reading of the Foreman's `batch` action; `reload-rules.md` (1.6 KB) is a four-rule floor for after a compaction, named by the `batch:` line. |
| 3 | The CLI writes the whole prompt (`brief`) | **Not done.** No command; the skeleton and the opening lines are as before. |
| 4 | Procedure leaves the cards; `next` and `next:` lines | **Not done.** No `next`; 4 `next:` lines; `restack owed:` and the lease refusals are the same idea, one case each. |
| 5 | Rare cases become help topics | **Half done, as files.** 32 pieces by moment, each a manifest action; no `help` command, no refusal or state line that names a piece. Median piece 6.5 KB against a 1.5 KB topic budget. |
| 6 | `state:` line and a delta | **Partly done.** The `batch:` line is a state line on `status` (not on watcher lines). No delta: `status` lists every CR at each call. |
| 7 | Messages through the board (`msg`, `inbox`) | **Not done.** The Foreman's watcher carries forge events only. Hand-backs, orders and notes still travel by the host's means. |
| 8 | Checkable "never" rules become refusals | **Not done.** The hook's guard is unchanged since the base (see 4.3). |
| 9 | Proof log outside the cards | **Not done.** Marks and dates unchanged. |
| 10 | A test holds every card under a byte budget | **Partly done, in another form.** `test_start_reading.py` holds each role's start reading at or below a figure, per host. It is a ratchet on the start reading, not a budget on a card, and it was raised twice in a day (CR-479 for the Foreman's watcher, CR-478 +1.8 KB: `:17-23`). |

### 4.2 Budgets (first study, 4.2)

Still the right targets; none is met. The "boot today" column is now, for the three cut roles,
the declared start of section 2.2 (202, 91 and 24 to 34 KB) until real runs are measured. The
boot target (card + floor + host row) needs the host card out of the start: on Claude it is
110 KB of the Chief of Staff's 202 KB and of the Griller's 145 KB, and 23 KB of the Foreman's 91.

### 4.3 Carriers of just-in-time reading (first study, 4.3) and the hook

| Need | Proposed carrier | Exists on origin/main? |
| --- | --- | --- |
| What do I do now | `next`, `next:` lines | No command. 4 `next:` lines. |
| A rare case | `help <topic>`; the refusal names the topic | No command. The pieces exist as files; the role finds them by the moments list. |
| A command's usage and limits | `--help` | Yes, and it states rules (2.4). |
| Where the batch stands | `state:` line, `status --since` | `batch:` and `handed back:` lines, yes; `--since`, no. |
| What a peer says | `msg`, `inbox` | No. |
| How this host does a thing | host row in `brief`, `host <capability>` | No. The "Tools" table is read as a section (21.4 KB). |
| Why a host behaviour is believed | proof log | No. |

**What the hook can refuse (`hooks/register.tsx`, read whole for the guard, `:523-886`):**

- It handles `tool.call` for every tool call and returns `{ deny: <text> }` to refuse
  (`:839-886`). For `Bash` and `PowerShell` it has the whole command string and cuts it into
  segments with their words and redirections (`splitShell`, `:542`; `judgeShell`, `:721`).
- Today it judges only agents whose prompt held a `writes:` line (recorded at `agent.spawn`,
  `:791-837`), and only **where** a shell write lands: a redirection, `tee`, `sed -i`, `cp`,
  `mv`, `rm`, `Set-Content` and the like outside the named folders is refused (`:857-860`).
- `git`, `gh`, `glab` and the chantier CLI are exempt by name (`EXEMPT`, `:668`, `:730`): the
  guard never looks at their arguments. So `git merge`, `gh pr merge`, `git reset --hard`,
  `git clean`, `git stash`, `git push --force` and `pkill` pass.
- A content refusal is therefore a small change in a place that already has the parsed words:
  a deny list on the first words of a segment. Limits that stay: it sees no command inside an
  interpreter's inline code or a script (`:531`); a call it cannot cut passes with a note
  ("a guard at fault must cost nothing", `:530-531`); the main session (Chief of Staff, Foreman) has
  no agent id and no `writes:` line, so it is not guarded today (the `tool.call` handler does
  run for it); Copilot has no hook.
- Also there: `agent.spawn` rewrites the spawn input (the `cwd`, `:814`), and `session.compact`
  adds the reload message after a compaction (`:904-912`). Whether `agent.spawn` may rewrite the
  prompt itself (to add a floor) I did not check: the host's API types are not in the repository.
- `ship` already refuses a head that holds a merge commit (`commands/merge_check.py`, present at
  the base too): the first study listed it as new by mistake.

### 4.4 What moves into code (first study, 4.4)

| Proposed move | State |
| --- | --- |
| Launcher instead of the `$CHANTIER` paragraph | Not done; 2.3 KB in each of 4 skills. |
| `judge <cr>`: the ask worded by the CLI | **Partly done by another road:** `status` prints the `handed back:` line with the gaps, what is owed before the merge and the gate's result, to copy. The card text it replaces is still there ("The user's boundaries", 12.1 KB; `foreman-merge.md`, 10.9 KB). No command records the ask or prints the take-back. |
| `conflicts <cr>`: the early conflict check | Not done; now its own piece, `foreman-conflict.md` (3.8 KB). |
| Order of ship and proof as `next` lines; commands record their phase | Not done. |
| `reply-check` | Not done. |
| `retro draft` | Not done; `foreman-pause.md` (2.1 KB) holds the retro critic. |
| Host card and row from a data file | Not done. |
| The hook records the agent id | Not done (it records the `writes:` folders in its own state). |
| "Never" commands refused by the hook | Not done; feasible (4.3). `ship` refusing a merge commit: already there. |
| Nothing for the watcher's lines | Still true; `session-start-chief-of-staff.md` "The watcher" is 4.1 KB of explanation. |

### 4.5 The Foreman's tools (first study, 4.5)

| Tool | State |
| --- | --- |
| `next --epoch` | Not done. |
| `state:` line | Done on `status` as the `batch:` line; it lacks the counts by state and the due list. |
| The Foreman's own watcher | **Done for forge events** (merge, red CI, wait met), with a 55-minute timer as the wake (`hosts/claude-code.md:74`). It does not carry a hand-back, an order or a message, and it never runs for a batch steered directly (`e20ca207`). |
| `status --since` | Not done. |
| `judge`, `conflicts`, `brief`, `msg`, `inbox`, `retro draft`, `help` | Not done. |
| `order merged` fast-forwards or prints the one command | It prints `restack owed:` in a stack batch; the fast-forward was already the CLI's. |

`foreman-stack.md` is still one 16.5 KB card read whole by `batch:stack`.

### 4.6 and 4.7 The proof log, outside roles

Unchanged and not started. One fact for 4.7: the 30 wrappers did not change with CR-471, so a
generated wrapper still fits.

## 5. Proving that no behaviour is lost

**Still true:** the inventory, the four checks, the situation quiz. **New material that helps:**

- CR-471 made a table "words, old card#section, new file#section, action" for every moved block
  (`4-batch/3-done/471-…/work/tables.md`, 21.8 KB) and `tests/test_role_cards_split.py` holds
  that every rule is reached by an action. This is a seed of the inventory for three roles,
  at block level, without the kind (a to f) and without "new home".
- The three Fable readings are a first form of check 3, read-only and without a judge.
- `test_start_reading.py` gives the per-role, per-host measure the first study asked for in CR 1,
  for the declared reading. The transcript measure (the real reading) is still missing as a tool.

**The ten rules, where they are now:**

| # | Rule | Place on origin/main |
| --- | --- | --- |
| 1 | Never merge without the user's word | `concepts.md:736`, `foreman.md:61`, `chief-of-staff.md:72`, `chief-of-staff-merge.md:84`, `reload-rules.md:8`; printed by `status` ("merges: the user", `ready_line.py:126`) |
| 2 | Rebase only; `--force-with-lease` on its own branch | `concepts.md:743-751`, `driver.md:166` ("Means: rebase and push"), `driver_prompt.py:117-138` (`Rewrites:`), `chief-of-staff-steering.md:147` |
| 3 | No fallback | `startup-core.md` (third paragraph), `concepts.md:725`, 7 worker cards |
| 4 | A CLI that cannot run is a stop | `startup-core.md` (second paragraph) |
| 5 | Never discard the worktree's work | `driver.md:334`, `:538`, `driver-retake.md:103` |
| 6 | An irreversible release action waits for the user | `driver.md:615-619`, `chief-of-staff-release.md:78`, `foreman-release.md:11` |
| 7 | Only the user starts work | `chief-of-staff.md:69` |
| 8 | No image shows the username or home folder | `driver-pr-extras.md:38`, `chief-of-staff-merge.md:44` |
| 9 | Refusals reported with their exact text | `chief-of-staff-steering.md:114`, `:179`, `:198`; `concepts.md:739` (rule 7) |
| 10 | Never stop a process by name or pattern; `close --yes` only on the user's yes | `coder.md:33`, `conflict-resolver.md:28`, `chief-of-staff.md:310`, `chief-of-staff-batch-end.md:39` |

Rule 8 is now in a piece a Driver reads only for "an image and the look" (`driver:pr-extras`),
and rule 5's stack form is in `driver-retake.md`: two protecting rules that the cut made
conditional. This is the risk the floor (design line 2) removes.

Close behind: `foreman.md:162` (the Foreman's chat obeys only "stop" and "hold"),
`chief-of-staff.md:313` (nothing posted on a tracker issue unapproved), `startup-core.md`
("a host path not exercised is labelled untested").

## 6. Order of work, revised

| CR | Content | Change from the first study |
| --- | --- | --- |
| 1. Measure the new cards for real | the transcript measure as a tool (per role: card bytes, files, turns, cost); one batch run on origin/main's cards; the per-role result beside section 2.3 | **Changed, and first.** The declared figures exist and are tested; the real ones do not. Needs the main checkout on origin/main. The inventory starts from CR-471's `tables.md`. |
| 2. The carrier for the pieces | `help <topic>` printing a piece (an action of the manifest); refusals, the `handed back:` and `batch:` lines and the watcher's lines name the topic; the moments lists shrink to a pointer | **New, from old CR 4.** Cheap now that the pieces are files; it removes the manifest and its `@` references from the role's path. |
| 3. The host card out of the start | the "Tools" row a role needs printed with its prompt (data file per host, mark as one word); `session-start` and `foreman:reference` stop reading the card whole; proof log for the marks | **Old CR 2 and part of CR 3, merged and raised:** it is 110 KB of the Chief of Staff's and Griller's start. |
| 4. Quick cuts | the launcher; `status --since` and merged CRs as a count; `handoff` without every role's opening lines; `driver:refused` without the Foreman's piece | Old CR 3, minus "the manifest lists only the session's host" (done). |
| 5. The tools | `next` and `next:` lines, `brief`, `conflicts`, `retro draft`, `msg` and `inbox` (with the Foreman's watcher reading them), the ask recorded from the `handed back:` line | Old CR 4, smaller: the state line, the Foreman's watcher and the ask's wording are partly there. |
| 6. Refusals | the hook's deny list for the "never" commands, for guarded agents first | Old CR 5; `ship`'s merge-commit refusal exists. Feasible in `judgeShell`'s segments. |
| 7. The rewrite, by family | entry cards and pieces to their budgets, behind a `cards:` key, each family against the quiz and one campaign | Old CR 6. Its input changed: per moment, a piece to shrink into a topic, not a section to find in a 200 KB card. |
| 8. Roles as data | role format, lint, generated wrappers | Old CR 7, unchanged. |
| 9. Removal | old cards, manifest, cores | Old CR 8, unchanged. |

CR 1 to 4 change no rule. CR 2 and 3 together are the largest declared cut that needs no
rewrite: about 110 KB at each Chief of Staff and Griller start on Claude, and the 5.4 KB
manifest out of every boot.

A caution from CR-471 itself: a split by moment grew the Chief of Staff's start by 21 KB because
any-moment rules had to go somewhere, and two later CRs raised the tested figures the same day.
Without the byte budget as a gate (decision 12) and the floor (decision 9), each new CR adds to
the entry cards as before.

## 7. Decisions for the owner

Numbering kept from the first study. "Unchanged" means the question and the recommendation
stand as written there.

1. **May a prose "never" become a refusal?** Unchanged. Now checked: the hook has the parsed
   command and a deny path; `git`, `gh` and `glab` are exempt today. It covers started agents
   with a `writes:` line; guarding the main session is a second question (it has no such line).
2. **How much stumbling is accepted?** Unchanged.
3. **Is `next` an order or advice?** Unchanged.
4. **Rare incident patches with no trigger:** **changed.** They are now pieces with a named
   moment. The question becomes: a piece whose moment no CLI line can name, keep it as a topic
   found only through the moments list, or drop it until the case returns? Recommendation:
   keep the piece as a topic for one release, measure which topics are ever read, then drop.
5. **May a Driver message the Foreman during its run?** **Changed in its base:** the Foreman
   now has a watcher, for forge events only. The question becomes whether that watcher also
   carries agents' messages (`anomaly`, `blocked`). Recommendation unchanged: yes for those two.
6. **May the CLI word the asks?** **Partly decided by the code:** `status` already prints the
   `handed back:` line to copy. Left to decide: whether a command also records the ask and prints
   the take-back, so the card text on wording can go.
7. **Does the user still hear "not tested"?** Unchanged.
8. **What may an outside role be?** Unchanged.
9. **One floor for all roles?** Unchanged, and more pressing: two of the ten rules now sit in
   pieces read only on a condition (section 5).
10. **Does direct mode keep the Foreman's tools?** Unchanged. Today `chief-of-staff:direct`
    reads `foreman.md` (56.5 KB with its own piece) and the Foreman's watcher never runs there.
11. **Both card sets for two releases?** Unchanged.
12. **Is the byte budget a gate?** **Changed:** a gate exists on the start reading, and its
    figures were raised twice in one day. The question becomes: are the figures frozen, so that
    a CR that adds a rule must remove as many bytes or put the rule in code or in a topic?
    Recommendation: yes, frozen per role, lowered at each CR of the rewrite.
13. **New. Is the next step the carrier or more cutting?** Options: build `help <topic>` and the
    naming lines first (revised CR 2); or shrink the entry cards first. Recommendation: the
    carrier first, since the pieces exist and nothing proves yet that roles read them at their
    moment.
14. **New. Is a real run on the new cards required before the next card CR?** Recommendation:
    yes, one batch, measured with the tool of revised CR 1.

## 8. What I could not check

- **No real run on the post-CR-471 cards** exists on this machine; every "new" figure for a
  role's reading is declared, not observed. Whether roles read a piece at its moment is unknown.
- **Small samples:** Chief of Staff n=5 (reads inside the window, not whole sessions), Foreman
  n=3, Griller n=6. 112 runs were not classified (0.9 MB of card reads).
- **No run seen:** QA driver, demo explorer, board-griller, any Copilot role.
- **The first study's window and counter** are inferred from its run counts; my total is 32.4 MB
  where it gave about 38 MB.
- **CLI output per session** was not re-measured properly (my pattern misses some launch forms).
- **The split by kind (a to f)** was not redone; I checked only the counts of trial marks, dates
  and the named duplicates.
- **Which findings of the Fable readings are fixed:** read from two commit messages, not checked
  finding by finding.
- **The host's hook API:** whether `agent.spawn` may rewrite a prompt, and whether a refusal can
  be scoped to the main session by role; the types are not in the repository.
- **The hook's behaviour in a real session** was read, not run; `just mod` was not run.
- **Cost in money**, the cache re-reads and the skills' own load: as in the first study, not
  computed.
- **No eval was run** and no card text was tried on a model.
