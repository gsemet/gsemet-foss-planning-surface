# Fable review: the cleanup plan for the cards and the CLI

2026-11-27, on chantier main at 4d12a5b. A proposal: nothing is deleted or started without the
owner's word. The verdict for every file is in `fable-review-verdicts.md`, beside this file.

## In short

- The 240 topics are not 240 subjects. They are 296 small pages, of which 105 are pieces of 50
  texts cut to fit a size limit, and 67 of the 240 names only print other topics again.
- Read page by page: 17 % of the topic text can be deleted now, 51 % is mechanical and belongs in
  the CLI's output, 32 % is worth keeping, and that 32 % shrinks to about 40 KB once written plainly.
- Target: about 55 files and 130 KB instead of 330 files and 620 KB; about 24 guides, one theme
  each, instead of 240 topics; a Chief of Staff that boots on 8 KB instead of 24.6 KB.
- The cleanup is mostly a CLI programme (complete what the CLI prints), not a rewrite of prose. The
  last rewrite failed on size; this plan cuts by deletion first, then one family at a time.

## 1. What the 240 topics are

`help <topic>` prints one or more pages of `references/topics/`. Counted from `topics.json`:

| kind of topic | count | what it is |
|---|---:|---|
| one page | 126 | a rare case, 0.2 to 2.8 KB |
| one text cut in `-pN` parts | 47 names, 105 pages | a text over 1,500 bytes, cut in the middle of its subject (`merge-github.md` starts at step "4.") |
| aggregate | 67 | a name that prints other topics' pages again: `help steering` prints 25 pages, 26 KB |

Fourteen families a person can grasp (the 296 pages, read whole; sizes in KB):

| family | pages | KB | delete | to CLI | keep (card) | keep (guide) |
|---|---:|---:|---:|---:|---:|---:|
| A Driver on its CR (rounds, ship, CI, conflicts, hand-back) | 30 | 45.6 | 3.9 | 27.0 | 3.2 | 11.5 |
| Host notes (Claude Code, Copilot) | 33 | 39.8 | 21.3 | 8.6 | 0.0 | 9.9 |
| Stack batches | 27 | 37.1 | 2.6 | 23.6 | 0.0 | 11.0 |
| Session, seat, board, watcher | 34 | 35.0 | 11.8 | 17.6 | 0.0 | 5.5 |
| Starting a batch (plan, trials, permissions, config) | 29 | 33.6 | 3.5 | 23.3 | 0.0 | 6.8 |
| Steering a running batch (orders, wakes, reports) | 27 | 29.4 | 2.6 | 22.7 | 0.9 | 3.2 |
| Grill, backlog, tickets | 19 | 22.3 | 3.6 | 4.3 | 2.9 | 11.5 |
| Release | 17 | 22.1 | 0.4 | 7.5 | 0.0 | 14.2 |
| Refused push or rebase | 16 | 17.6 | 1.3 | 15.2 | 0.0 | 1.2 |
| Ending a batch (close, retro, demo) | 16 | 16.7 | 3.4 | 5.5 | 0.0 | 7.8 |
| Lost Drivers, leases, recovery | 12 | 16.0 | 0.0 | 7.7 | 1.5 | 6.8 |
| Merge and asks | 13 | 14.7 | 1.0 | 10.2 | 0.9 | 2.7 |
| Direct mode | 12 | 12.8 | 2.7 | 6.5 | 0.0 | 3.6 |
| Workers (Verifier, Inspector, shell rules) | 11 | 12.8 | 2.8 | 1.8 | 6.7 | 1.5 |
| **all** | 296 | 355.6 | 60.8 | 181.5 | 16.1 | 97.2 |

My judgement of what a capable model needs. Very little of it as text. Most pages are a fixed
sequence of commands, a line format, a count or a wording: things the CLI can do or print at the
moment they are needed. What a model truly cannot work out alone is small: the user's limits (what
is never done without their word), a few traps of the host (a notice that looks like an order), and
judgement in rare cases (a release half done, a Driver that looks dead, what to ask in a grill).
The helpers' estimate of that text, written plainly: about 40 KB for the 296 pages.

Why the pages still feel heavy although boot is lighter:
- The text was cut, not reduced. The old cards' sentences moved into pages of 1,500 bytes.
- The same procedure is told several times: the refused push in 16 pages for three roles; the
  restart of a Driver (4 commands) in at least 8 pages.
- Nothing leads to most pages. The CLI's source names about 10 topics; the others are reached only
  through a list in a card (29 names in the Chief of Staff's card, 19 in the CR Driver's), which is
  the opposite of progressive disclosure: the model must guess which of 29 names fits.
- Pages contradict each other and the CLI (about 45 cases found, appendix section E;
  examples: a page gives `taskkill /PID` where the card forbids stopping by PID; a page has the
  agent run `git worktree remove --force` where the CLI's own cleanup uses no `--force`; the
  watcher "outlives the heartbeat" in one page and is stopped with it in the next).

## 2. The tests that decide a text's fate

Applied to each page in this order; the first that fits decides.

1. **Inferable: delete.** A capable model does it alone (general engineering sense), or the CLI's
   output already says it (a refusal's text, a `next:` line, a command's `--help`). Where the output
   nearly says it, complete the output and delete the instruction. Also deleted: a second copy, a
   trial note, history, a sentence about output the CLI no longer prints.
2. **Mechanical: the CLI.** A fixed sequence, a format, a count, a wording, a check. In order of
   preference: the CLI does it; a refusal names the next command; a `next:` line gives the step; the
   command prints the exact line to send. No page then explains it.
3. **Protects the user or the repository: a refusal, plus one line.** A CLI or hook refusal where
   code can hold it, and one short line in the floor or the role's card. Never in a guide alone.
4. **Judgement in a rare case: a guide.** One theme, one page, reached from a CLI line at its moment.
5. **A fact of the host a model cannot know: a host row**, printed on demand by `host <capability>`.

A text that passes none of the five is deleted.

A sixth test applies to what is kept (the owner's words of 2026-11-27): **a guide names no harness
and no forge tool.** It says "start a Driver", "the PR", "mark it ready", never `SendMessage` or
`gh pr ready`; the model adapts (PR to MR, one tool to another). What differs by host or forge is
served by the CLI, one row at a time. Today 54 topic pages name a harness or its tools (32 `host-*`
pages and 22 others) and 62 name a forge, 50 of them with `gh` or `glab` command lines.

What replaces the page-size limit. No test enforces the 1,500 bytes (searched in the tests: none
found); it comes from the rewrite's specifications (`507-sc21-cards-foreman`, section 3: "at most
1,500 bytes", "a source too big is split"). It is replaced by three rules, each one test:
no file named `-pN`; one total size for the whole `references` folder; one size per role's boot.
A page may be 4 KB if its theme needs it. Budgets per card and per page (answer 9 of the rework,
M1, M2) go: they are what produced the cutting.

## 3. The verdicts

Every topic page, root card and host file has its row in `fable-review-verdicts.md` (name, verdict,
destination, reason). Totals for the 296 pages:

| verdict | pages | KB |
|---|---:|---:|
| delete: inferable | 17 | 17.4 |
| delete: duplicate | 33 | 28.2 |
| delete: stale or history | 15 | 15.2 |
| to the CLI | 148 | 181.5 |
| keep as card lines | 15 | 16.1 |
| keep in a guide | 68 | 97.2 |

Read whole: all 296 topic pages (by four helper readers, one slice each), and the floor, the Chief
of Staff, Foreman, CR Driver and review-step cards. Sampled only: the other root cards, `concepts.md`,
the templates, the host files (structure and marks counted by script). Not read: the four `SKILL.md`,
the agent wrapper files, the hooks' code. Most "the CLI already prints this" claims come from the
pages' own wording and are marked `exists?` in the appendix: each is checked when its CR is specified.

## 4. The target

### 4.1 The card set (about 55 files, about 130 KB)

| what | files | size | holds |
|---|---:|---|---|
| `floor.md` | 1 | under 1 KB | the rules nothing overrides |
| role cards | 19 | 1.5 to 5 KB each, 50 KB in all | who you are, what you own, your nevers, your reply. No procedure, no list of topics |
| guides (`references/guides/<theme>.md`) | about 24 | 1 to 4 KB each, 45 KB in all | one theme each: the rare cases that need judgement |
| formats | 3 | 13 KB in all | PR writing rules, release notes, the tour (`init`) |
| host rows | 2 | 25 KB each, read one row at a time | this host's tool for a capability |
| forge notes, role index, guide index | 5 | 20 KB | data |

The guides, by reader (names are proposals):
- Drivers: `rounds`, `conflicts`, `trouble`, `stack-driver`, `release-driver`, `images`.
- Steering (the Foreman, and the Chief of Staff in direct mode): `lost-driver`, `merge`, `stack`,
  `release`, `gates`, `retro`, `direct`.
- Chief of Staff and Griller: `grill`, `tickets`, `session`, `batch-start`, `batch-end`, `board`,
  `permissions`, `reports`, `release-chief`.
- Everyone: `words` (the glossary of `concepts.md`, 3 KB), `shell` (the eight shell rules, today in
  three files).

Gone: `concepts.md` but its glossary, `routing.md`, `status-layout.md` (the CLI prints the report),
`sync-checkout.md`, `hosts/claude-code.md` (to `docs/`), the 33 `host-*` pages (about 10 become
host rows, the trial history is already in `docs/proofs/`), every `-pN` page, every aggregate name.

### 4.2 Progressive disclosure: three levels

**Level 0, at boot (the brief).** The role's card, the floor, the unit's facts. Not the host rows:
today the Chief of Staff's brief is 24.6 KB of which about 17 KB is the text of 37 host rows, most
marked untested (lines 69 to 326 of 328). The brief prints the rows' names only, one line in all;
`host <capability>` prints one row when it is needed. Target: Chief of Staff and Foreman 8 KB,
CR Driver 7 KB, Griller 5 KB, workers as today.

**Level 1, at the moment (the CLI's output).** This is the main carrier. Every command ends with
its `next:` line; every refusal says what, why and the command that gets out; a watcher line ends
with what to do (record, or tell only). When a rare case starts, that line names the guide:
`next: help lost-driver`. The model never has to choose a guide from a list.

**Level 2, on demand.** `help <guide>` prints one page; `<command> --help` gives the arguments;
`help --for <role>` lists the role's guides (at most 9) and, new, its commands (a Driver sees its
14 commands, not 57).

**Never loaded.** Another role's guides; the other host's rows; trial history (`docs/proofs/`); the
rule inventory; a page "for completeness".

How a role finds its page: from the CLI line that names it, at the moment. A test keeps it true:
every guide is named by at least one CLI string (a `next:` line, a refusal, a state line); a guide
no CLI line names is either wired or deleted. A card may name at most three guides.

### 4.3 The CLI: organised, and completing its own output

Today: 57 commands in one flat list (`chantier --help`), `order` with 17 kinds. The count will not
drop much (about 48); what changes is the order, and that each role sees only its own.

Printed in six groups (argparse groups: no rename, no risk):

| group | commands |
|---|---|
| session | `preflight`, `init`, `seat`, `rules`, `playbook`, `host`, `help`, `brief` |
| backlog | `file`, `triage`, `summary`, `validate` |
| batch (Chief of Staff) | `open`, `order`, `status`, `asks`, `cost`, `retro`, `close`, `cancel` |
| steering (Foreman) | `foreman`, `next`, `judge`, `conflicts`, `agents`, `msg`, `stack`, `forge-stack`, `pause`, `restart` (new) |
| unit (Drivers, workers) | `take`, `round`, `note`, `gate`, `push`, `ship`, `ci` (new), `pr` (new), `verdict`, `handback`, `handoff`, `lease`, `wait`, `release` |
| board | `board serve`, `watch`, `link`, `live`, `login`, `logout`, `sync`, `journal` |

Folded, each old name kept as an alias for one release (two other projects use the plugin):
`abandon` and `restore` into `triage`; `park` into `order park`; `inbox` into `msg --read`;
`interests` into `journal`; `log` into `handoff --log`; `access` into the refusals themselves and
`next <cr>`; `phase` set by `round`, `ship`, `gate` and `verdict` (not verified that none does it
already); `serve`, `webui`, `live`, `login`, `logout`, `watch` under `board`.

Completing existing output (cheap, each empties pages; "exists?" to check per CR):

| move | pages it empties | KB |
|---|---|---:|
| `next <cr>` gives every step of the Driver's path, and names the guide of a rare case | `cr-ship`, `closing`, `restart`, `retake*`, `conflicts-early-push`, `release-end`, `ci-beside-gate` | 14 |
| `next --epoch` and each order's `next:` line print the exact `take <cr> --note "…"` per CR after a merge, drop, hold, park, mode switch | `merge`, `mode-switch*`, `hold`, `park-back`, `stack-drop`, `stack-ends`, `orders`, `escalation` | 14 |
| every refusal names its next command (answer 9, M9, not done) | `lease*`, `handback-refused`, `retake-stack`, `stack-record`, `refusals-to-say*` | 13 |
| `judge` words the whole merge ask, stack included | `merge-stack-ready*`, `merge-series-stack*`, `merge-words-p1`, `stack-asks`, `local-gate`, `long-gate-waiver` | 15 |
| `status --report` prints the report filled, its Notes and the delivery floor | `status-layout.md`, `status-notes*`, `steering-reports*`, `delivery-time*` | 20 |
| each watcher line ends with its `next:` | `watcher-events*`, `watcher-lines*`, `watcher-pull`, `merge-recorded` | 7.5 |
| `seat` prints the role, the one question and the title to set | `seat*`, `titles`, `reload` | 6 |
| `open --dry-run` prints the plan (CRs, waits, slots, budget, mode) | `batch-plan*`, `batch-plan-show*`, `batch-plan-mode-p2/p3` | 6 |
| `brief` writes every started role's prompt (Foreman, spec-writer, spec-critic, demo-explorer, review step) | `foreman-start-p2`, `grill-specify-p1`, `cr-review-step`, `cr-prompt`, `cr-workers` | 7 |

New commands (each needs the owner's word, see section 8):

| command | replaces | KB |
|---|---|---:|
| `push <cr> --epoch <n>` and `rebase <cr> --epoch <n>`: the steering session's run of a Driver's refused push or rebase, with the checks as rails | the whole refused-push family, in three roles' pages and two cards | 17 |
| `restart <unit> --cause "<text>"`: clears the Driver, takes again with the note, counts the repeats | `lost-restart`, `lost-context`, `lost-outside`, `take-back` | 6 |
| `ci <cr>`: the checks at the pushed head, the wait, the note | `ci`, `ci-no-check`, half of `trouble-remote` | 4 |
| `pr body <cr>` and `pr check <cr>`: the factual parts of the PR body from the record, and the audit | `verifier-description`, `verifier-review-box`, most of `pr-template.md` | 10 |
| the main checkout's fast-forward done by `order merged` | `main-checkout*`, `sync` | 4 |
| `preflight --add-rules`: writes the allow rules on the user's yes; P9 as code | `allow-rules*`, `host-allow-*`, `forge-permissions*` | 14 |

### 4.4 Host and forge: abstract guides, differences served by the CLI

What already carries the differences, and is kept: `hosts/<host>.json` printed by `host
<capability>`; the forge connectors in the code (`connectors/github.py`, `gitlab.py`), which
`forge-stack`, `ship` and the hub use; and two tests that forbid a host tool or a forge tool in the
startup cards. The two forge notes (0.6 KB each) say almost nothing a model does not know.

- **Hosts.** No guide is host-specific: zero exceptions. The 33 `host-*` pages go; about 10 of their
  facts are real traps and become host rows (the turn-end notice, Auto-fix events, a silent Driver,
  a session started from Remote Control, `/loop` with no interval, the 10-message limit, refused
  file names, and the allow rules, which are a Claude Code notion). A guide says the capability
  ("stop the Driver by the host's means"); `host <capability>` gives the tool. Marks today: Claude
  Code 13 rows proved, 37 untested; Copilot 0 proved, 50 untested; the CLI already says "never tried
  for real here" on an untested row (answer 16). Five pages only say "nothing is known on Copilot".
- **Forge.** One vocabulary, "PR". The guides give no `gh` or `glab` line: a model knows both tools.
  The frequent forge steps are done or printed by the CLI in the forge's own form (`ship`, the new
  `ci`, `order merged` confirming the merge, `forge-stack`), so the context holds neither syntax.
  The few real differences (a native stack on GitHub and a chain of MRs on GitLab; GitHub's
  asynchronous merge taking the PRs below; closing verbs) become forge rows, printed by a `forge
  <capability>` command, the twin of `host`, with the same "never tried here" sentence: it replaces
  the "unproved on GitLab" lines spread over about a dozen pages. A concept a forge lacks is still
  written abstractly; the row says what that forge does instead.
- **Exceptions.** None proposed. If one appears, it is a host or forge row, not a page.
- **My proposal, beyond the owner's words** (they named `references/topics`): the same rule for the
  root cards; four of them name a harness or forge tool today (`chief-of-staff.md`, `concepts.md`,
  `routing.md`, `status-layout.md`). The two existing tests are extended to the guides.

## 5. What protects the user, and where it lives afterwards

Nothing below may be lost. "Refusal" means code holds it; the line stays in the card too.

| rule | lives in |
|---|---|
| Never merge without the user's word; "you can merge" only after the ready line | floor 1; `judge` words a held state, never "ready to merge" for a PR that must wait (batch-31's CR-510) |
| Rebase only, `--force-with-lease`, the CR's own `chantier/*` branch, never the default branch even on a yes | floor 2; refusal of `push` (exists) and of the new steering `push` and `rebase` |
| Never discard work: no `stash`, `reset --hard`, `add -A`, no forced cleanup of the main checkout | floor 5; hook refusal for a Driver's shell (new; answer 22 filed a hook deny list apart) |
| A Driver and its workers write only where `writes:` says, never in `.git`, never in the main checkout | the write guard hook (exists on Claude Code; nothing on Copilot) |
| An irreversible release action waits for the user; `publication done:` only from the user's quoted words; "auto" covers one release only; the tag step is never the Driver's | floor 6; `release go` refusal (exists); release cards |
| No grant lets a session merge a stack that holds the release PR | refusal in `release go` (to add) |
| Only the user starts work; a board mark or "rescan" is no go; another project's CR is never run | floor 7; refusal of `open` and `order add` for another project's CR (to add) |
| No image shows the username or home folder; a leak found is replaced and told | floor 8; guide `images` |
| A refusal is reported with its exact text, never worked around, never retried another way, never by changing the permission settings | floor 9 (add the last six words) |
| Never stop a process by name, pattern or PID; the board and watcher start and stop on the user's yes | floor 10; fix `board-p1`, which gives `taskkill /PID` |
| `settings.json`: only the allow rules, only added, on the user's yes; a rule of the user's is never edited | the Chief of Staff card today; a CLI write that can only add (decision 3) |
| A tracker comment or a public issue holds no CR number, batch, role, cost or private path; posted only on a recorded yes | Chief of Staff card; a pattern check in the posting step (to add) |
| Never a second Driver on one CR: silence is no proof of death; after a mode switch every old Driver is checked ended | `take` refuses on a live lease (exists); `restart` and `foreman set` refuse on a live lease (to add) |
| A CR found merged, or with a PR already: nothing pushed, no second PR | refusal of `push` and `ship` (to check) |
| A waiver of the long gate is recorded with the user's words and a follow-up CR | `order waive` (exists); `judge` refuses a claimed waiver that is not recorded (to add) |
| A host notice (turn end, Auto-fix) is no order and no ask | one line in the Foreman and Chief of Staff cards; host row |
| The seat moves only on the user's word; `abandon`, `restore`, priorities only on the user's word | Chief of Staff card (as today) |
| The planning surface is committed and pushed only by its writer | cards (as today) |
| Record each grill answer at once in the user's words; never decide "grilled enough" alone | Griller and Chief of Staff cards |

The readers listed 96 protective statements in the pages (appendix section D); the table above
groups them. That list is the acceptance evidence of section 7.

## 6. The order of work

Cut so that no CR rewrites more than about 25 KB of source text or touches more than one family,
and so that deletion never waits for new code. `(D)` needs a decision of section 8.

**Step 1: delete at once, low risk (3 CRs, no code but tests' file names).**
1. Delete the 65 pages with a delete verdict (60.8 KB) and their entries; fix the pointers. Two CRs
   of about 33 pages (Chief of Staff side; Foreman, Driver and host side). Evidence: the diff is
   deletions only; `help` lists no dead name; the tests that name a page still pass or are updated.
2. Delete the 67 aggregate names from `topics.json` (they add no text). Evidence: no CLI string or
   card names one (today the CLI names `lease`, `watcher`, `board`, `stack`, `stack-merge`,
   `refused-push`, `merge`, `host-allow-not-add`; `refused-push` and `stack` become pages).

**Step 2: one theme, one page, without rewording (1 CR, scripted).**
3. Join every `-pN` set into one file (105 pages become 50). Add the test "no `-pN` file" and
   remove the page-size target. Evidence: a script shows each joined file equals its parts in order.

**Step 3: the boot (2 CRs, small code).**
4. `brief` prints host rows by name only; lower the brief ceilings in `test_brief_bytes.py`.
   Evidence: `brief chief-of-staff` under 9 KB, `brief foreman` under 9 KB; `host <row>` unchanged.
5. `help --for <role>` lists the role's commands; `chantier --help` in six groups; the folds as
   aliases. Evidence: `--help` output; old names still run.

**Step 4: the CLI completes its output, one family per CR (9 CRs).** Each CR: the code, its tests,
and the deletion of the pages it empties, in the same PR, so text never waits without a home.
Order by gain: 6. `status --report` and the delivery floor; 7. `judge` for the stack ask;
8. `next <cr>` for the Driver's path; 9. `next --epoch` fan-out; 10. refusals name their next
command; 11. watcher lines; 12. `seat`; 13. `open --dry-run`; 14. `brief` for the remaining roles.
Evidence for each: the scenario shows the new line at its moment; the emptied pages are gone.

**Step 5: new commands (D), one per CR (6 CRs):** 15. steering `push` and `rebase`; 16. `restart`;
17. `ci`; 18. `pr body` and `pr check`; 19. the fast-forward in `order merged`; 20. `preflight
--add-rules` and P9. Each is independent of the others; each needs its line in AGENTS.md.

**Step 6: the guides, one family per CR (8 CRs), after that family's step-4 and step-5 CRs.**
Each CR writes 2 to 4 guides (at most 10 KB of new text) from the pages left in the family and
deletes those pages. 21. Driver on its CR; 22. stack; 23. release; 24. lost Drivers and direct mode;
25. merge, gates, retro; 26. grill and tickets; 27. session, board, permissions; 28. batch start,
batch end, reports. Evidence: each kept protective rule of the family found in its new home.

**Step 7: the cards and the gates (3 CRs).** 29. The six big cards rewritten for reading (lists,
short sentences), no rule added or removed, two cards per CR at most. 30. `concepts.md` to `words`,
`routing.md` and `hosts/claude-code.md` out. 31. The five tests of section 7 replace the inventory.

Dependencies: steps 1 to 3 need nothing and can go in one batch, in parallel. Step 4's CRs are
independent of each other. Step 6 waits for steps 4 and 5 of the same family only. Step 7 is last.
A version bump after step 3 and after each later batch, so the two other projects get cards and CLI
that match (the handover found them reading new cards against an old cached CLI).

## 7. The result in numbers, the risks, the proof

| | today | after steps 1 to 3 | at the end |
|---|---:|---:|---:|
| files in `references` | 330 | about 210 | about 55 |
| bytes in `references` | 620 KB | about 545 KB | about 130 KB |
| topics | 240 | about 110 | about 24 guides |
| topic pages | 296 | about 180 | about 24 |
| boot, Chief of Staff | 24.6 KB | about 8 KB | about 8 KB |
| boot, Foreman | 22.9 KB | about 8 KB | about 8 KB |
| boot, CR Driver | 9.3 KB | about 8 KB | about 7 KB |
| largest single `help` answer | 26 KB (`steering`) | about 6 KB | 4 KB |
| commands | 57, flat | 57, in six groups | about 48, each role sees its own |

Risks:
- **The CLI programme is large** (step 4 and 5: 15 CRs). It is where the gain is: without it, about
  180 KB of procedure has no home but text. Steps 1 to 3 pay off alone if the rest is delayed.
- **A rule lost by deletion.** Limited by section 5's list; a deleted page stays in git.
- **More stumbles on rare cases.** Accepted by the owner (answer 3: free on rare cases); a stumble
  seen often is fixed in the CLI's line, not by a new page.
- **Two other projects use the plugin, one with a batch running.** Old command names stay as aliases
  for one release; a running batch reads the cards live from the checkout, so step 1 lands between
  that project's batches or after a version bump.
- **Copilot stays unproved** (50 rows of 50 untested, no hook): this plan changes nothing there.
- **Card rewrites again too big.** Step 7 touches two cards per CR and adds no rule.

Proof that nothing that matters was lost, without an expensive process:
1. The list of protective rules (section 5; 96 statements) is the checklist: each CR that deletes a
   page says, for each protective line in it, where it lives now. A refusal gets one test.
2. Five small tests guard the structure for good: no `-pN` file; total and boot sizes; every guide
   named by a CLI string; no harness or forge tool named in a guide or card (exists for the startup
   cards); every command a card names exists (exists).
3. One real batch on a sandbox project after step 3 and one at the end, read for stumbles.
4. Not kept: the row-by-row inventory (`docs/proofs/cards-inventory.md`, 1.48 MB in the repository,
   329 rows still open, three test files that pin where each old sentence lives). It proves that
   text was kept, not that behaviour was, and it freezes the structure this cleanup removes.

## 8. Where this plan contradicts AGENTS.md or an earlier answer

- **AGENTS.md, "a new CLI tool comes from measured token-costly behaviour, never from
  speculation".** The plan adds about six commands and many output lines. Its measure is the bytes
  of instruction each one removes and batch-31's retro (PR bodies sent back, Drivers restarted by
  hand); not token counts from transcripts.
- **AGENTS.md, "the agents do the work, git and the forge included", and "the rest of the CLI keeps
  no git write".** The steering `push` and `rebase`, and the fast-forward by `order merged`, are new
  git writes by the CLI. (AGENTS.md already says chantier "fast-forwards a clean main checkout
  after a merge it records"; I found no such code outside the surface writer, and the cards have the
  Foreman do it by hand. Not verified beyond a search.)
- **AGENTS.md, "the Chief of Staff adds to `~/.claude/settings.json` the allow rules".** The plan has
  the CLI write them, so that "nothing else there" is held by code.
- **AGENTS.md, the CLI's forge calls are a closed list.** P9 as code, `ci` and the merge check of
  `order merged` add forge reads. `forge <capability>` is a new read-only tool with no measured cost.
- **AGENTS.md, `help` "prints a help topic whole from … `references/topics.json`".** Kept, but the
  index shrinks and the folder is renamed `guides/`; the sentence needs one word changed.
- **Answer 9 (hard gates: a budget per card and per path, a rule with an id and a check).** The plan
  drops per-card and per-page budgets and rule ids; it keeps a boot budget per role and one total.
- **Answer 10 (keep each rare rule as a help topic for one release, measure which are read, then
  delete).** Nothing measures a read (`help` writes nothing), so the measure cannot happen as
  planned. The plan deletes on reading instead. Every topic already carries `review_by: 0.16.0`.
- **Answer 17 (a read-and-compare review, the inventory as that review).** Replaced by section 5's
  list of protective rules; the inventory and its tests are retired.
- **Answer 1 ("Fixed: the roles").** Kept. The 19 role cards are not the weight (50 KB in all).
- **AGENTS.md's own length** (its CLI-scope paragraph is several times a role card, and every
  session working on chantier reads it): the same illness, outside this review's scope.

## 9. The decisions for the owner

1. **Delete now, or measure first?** Your earlier answer was to keep each rare page one release and
   delete the ones nobody read. Nothing counts the reads, so that would mean waiting without
   learning anything. *Recommendation: delete the 65 pages now (step 1); they stay in git.*
2. **May the CLI do a few git and forge actions itself that agents do by hand today?** Namely: the
   Foreman's run of a Driver's refused push or rebase, the update of the main checkout after a
   merge, reading the CI's result. Today these are pages of instructions and the source of most
   refused-command trouble. *Recommendation: yes, each with strict limits written in AGENTS.md, as
   was done for `chantier push`.*
3. **May the CLI write the allow rules in your Claude settings itself, after your yes?** Today the
   Chief of Staff edits the file by hand, guided by seven pages. *Recommendation: yes; the command
   can only add the rules it printed, and nothing else in the file.*
4. **Drop the sentence-by-sentence inventory of the old cards?** It is a 1.5 MB file and three tests
   that check every old sentence still has a place. It makes each cleanup step expensive and proves
   little. *Recommendation: yes; replace it by the short list of rules that protect you (section 5),
   each held by a refusal or a card line, and by one real batch on a test project.*
5. **How far now?** Steps 1 to 3 are cheap and safe: 330 files become about 210, the Chief of Staff
   and the Foreman boot on a third of today's text, no more `-p1`, `-p2`. Steps 4 to 7 are the real
   cleanup and about 26 small CRs. *Recommendation: steps 1 to 3 in one batch now, with a version
   bump; then steps 4 to 7 family by family, the families you use most first (a Driver on its CR,
   merge, stack).*
