# PART 3 proofs (round 6)

Worktree `<worktree>`, head `bf4e4c42` plus the uncommitted changes of rounds 4 to 6: nothing is committed, so every command runs against the working tree (the files as they will be committed), and where the specification says `HEAD` the comparison is stated. Byte counts are LF bytes (the checkout has `core.autocrlf=true`). Written by `work/r6/proofs.py`. Paths: `<worktree>` is the CR's worktree, `<surface>` the planning surface's checkout, `<planning>` its `projects/chantier` folder.

## 2. Byte-identical copies

`git hash-object` of the working file (the checkout's filters applied) against the blob at `bf4e4c42` under `references/`.

```text
$ work/r6/proofs.py (proof 2)
floor.md: cards-next 61da01e8b67f8b8eec1845172a29d2466d1cc380 | references at bf4e4c42 61da01e8b67f8b8eec1845172a29d2466d1cc380 | identical; LF content equal: True
hosts/claude-code.json: cards-next 3f2daf7915192a790e2dc17b36d74d3cfd9a1fd0 | references at bf4e4c42 3f2daf7915192a790e2dc17b36d74d3cfd9a1fd0 | identical; LF content equal: True
hosts/copilot.json: cards-next b4dec473e0dab53cbacd334fa29286ce3ccc2ff9 | references at bf4e4c42 b4dec473e0dab53cbacd334fa29286ce3ccc2ff9 | identical; LF content equal: True
```

## 3. Bytes

| file | today | new | target | result |
| --- | ---: | ---: | --- | --- |
| concepts.md | 73,286 | 18,565 | none set (open question 1) | no target |
| pr-template.md | 16,801 | 11,849 | none set (open question 1) | no target |
| release-template.md | 12,155 | 6,758 | none set (open question 1) | no target |
| status-layout.md | 17,475 | 10,992 | none set (open question 1) | no target |
| titles.md -> topics/titles.md | 2,684 | 1,428 | 1,500 if a topic (folded into `topics/titles.md`) | within |
| ticket-summary-example.md | 1,422 | 1,308 | none set (may fold into a topic) | no target |
| routing.md | 5,016 | 4,790 | none set (open question 1) | no target |
| init.md | 10,041 | 6,171 | none set (open question 1) | no target |
| review-step.md | 3,950 | 1,385 | 1,500 | within |
| sync-checkout.md | 4,801 | 1,115 | 1,500 if a topic | within |
| forges/github.md | 739 | 587 | unchanged or smaller (739) | within |
| forges/gitlab.md | 744 | 590 | unchanged or smaller (744) | within |
| hosts/claude-code.json | 25,243 | 25,243 | byte-identical | within |
| hosts/copilot.json | 22,372 | 22,372 | byte-identical | within |
| hosts/claude-code.md | 109,857 | 23,319 | no byte target: Allow rules section only | no target |
| hosts/copilot.md | 18,947 | none | not carried: its text is in `topics/host-*.md` | no target (file not carried) |
| floor.md | 554 | 554 | 1,200, byte-identical | within |
| topics/host-*.md: 33 files | part of the above | 36,066 in all, largest 1,490 | 1,500 each | within |
| topics/<name>.md (others): 235 files | part of the above | 273,512 in all, largest 2,845 | 1,500 each | 24 over (listed below) |
| topics.json | 8,866 | 61,278 | none set | no target |
| skills/chantier-SKILL.md | 3,537 | 2,650 | section 6 (no byte target) | no target |
| skills/chief-of-staff-SKILL.md | 3,664 | 2,730 | section 6 (no byte target) | no target |
| skills/griller-SKILL.md | 3,223 | 2,292 | section 6 (no byte target) | no target |
| skills/status-SKILL.md | 3,644 | 2,729 | section 6 (no byte target) | no target |

New topic files of this uncommitted work (not in `bf4e4c42`): 42, largest 1,490 bytes (host-auto-mode-steering.md); over 1,500: none.

Every topic over 1,500 (each exists at the base head of this round):

| topic file | at bf4e4c42 | new | over by |
| --- | ---: | ---: | ---: |
| topics/ci-beside-gate.md | 2,052 | 2,052 | 552 |
| topics/ci.md | 1,589 | 1,589 | 89 |
| topics/closing.md | 1,888 | 1,888 | 388 |
| topics/conflicts.md | 2,238 | 2,238 | 738 |
| topics/cr-handback.md | 1,506 | 1,506 | 6 |
| topics/cr-rounds.md | 2,037 | 2,061 | 561 |
| topics/cr-ship.md | 2,413 | 2,413 | 913 |
| topics/cr-workers.md | 1,624 | 1,624 | 124 |
| topics/handback-other.md | 2,030 | 2,030 | 530 |
| topics/pr-extras.md | 1,898 | 1,898 | 398 |
| topics/pr-images.md | 1,882 | 1,882 | 382 |
| topics/refused-push.md | 1,544 | 1,544 | 44 |
| topics/release-merged.md | 2,845 | 2,845 | 1,345 |
| topics/release-notes.md | 1,991 | 2,063 | 563 |
| topics/release-ship.md | 2,306 | 2,306 | 806 |
| topics/retake-notes.md | 1,871 | 1,871 | 371 |
| topics/retake-stack.md | 1,818 | 1,818 | 318 |
| topics/retake.md | 2,328 | 2,328 | 828 |
| topics/stack-changes.md | 2,354 | 2,354 | 854 |
| topics/stack-hold.md | 2,232 | 2,232 | 732 |
| topics/stack-make.md | 1,742 | 1,742 | 242 |
| topics/stack-restack.md | 1,832 | 1,832 | 332 |
| topics/trouble-remote.md | 1,582 | 1,582 | 82 |
| topics/trouble-worker.md | 2,173 | 2,173 | 673 |

Role cards of the whole branch (Foreman, Chief of Staff and Griller against their budgets; the others because this round edits them). `references` is today's card at the base; the base's Chief of Staff and Griller cards are the two `SKILL.md`.

| card | references | at bf4e4c42 | new | budget | result |
| --- | ---: | ---: | ---: | ---: | --- |
| foreman.md | 36,927 | 3,897 | 3,998 | 4,000 | within |
| chief-of-staff.md | 32,067 | 5,499 | 5,994 | 6,000 | within |
| griller-skill.md | none | 3,290 | 3,497 | 4,000 | within |
| griller.md | 10,757 | 1,892 | 1,925 | 2,000 | within |
| coder.md | 4,609 | 1,417 | 1,533 | 1,500 | over by 33 |
| conflict-resolver.md | 3,893 | 1,378 | 1,494 | 1,500 | within |
| debugger.md | 3,682 | 1,165 | 1,281 | 1,500 | within |
| demo-explorer.md | 3,422 | 1,496 | 1,612 | 1,500 | over by 112 |
| investigator.md | 3,554 | 1,370 | 1,486 | 1,500 | within |
| retro-critic.md | 2,901 | 1,492 | 1,565 | 1,500 | over by 65 |
| spec-critic.md | 3,729 | 1,499 | 1,572 | 1,500 | over by 72 |
| spec-writer.md | 3,254 | 1,493 | 1,667 | 1,500 | over by 167 |
| inspector.md | 6,044 | 1,999 | 2,000 | 2,000 | within |
| verifier.md | 14,581 | 2,996 | 3,112 | 3,000 | over by 112 |
| cr-driver.md | none | 3,280 | 3,749 | 4,096 | within |
| stack-driver.md | none | 3,321 | 3,783 | 4,096 | within |
| release-driver.md | none | 3,277 | 3,811 | 3,072 | over by 739 |
| qa-driver.md | none | 1,337 | 1,567 | 2,048 | within |

## 4. `brief` for all 18 roles

Command, from the worktree's CLI: `uv run --no-sync --project <worktree> chantier --project <planning folder of chantier> brief <role> [unit] [--lease n] --batch batch-31 [--cards <worktree>/skills/chantier/cards-next]`. The CLI of the main checkout has no `brief` command (exit 2, argparse usage), so the worktree's is the one that runs. Batch-31's host is `claude`, so every row is the Claude column; Copilot is untested.

`brief` records nothing. It writes `<planning surface's git folder>/chantier/briefs/chantier/batch-31/<name>-<role>.md`; each path was written by the new-cards run and then by the today's-cards run, so the files left there hold today's cards. Bytes were read after each run.

study-fable-v2 (section 2.2) gives "boot, base / boot, new / start, new Claude". Its boot is the declared readings (cores, manifest, wrapper or skill, startup sections), another measure than the brief file's bytes.

### The runs as the specification gives them

| role | unit (lease) | new: exit, bytes | old: exit, bytes | study-fable-v2 |
| --- | --- | --- | --- | --- |
| cr-driver | CR-507 (2) | 2, refused | 0, 66,959 | 8,519 / 10,541 / 27,180 |
| release-driver | CR-507 (2) | 2, refused | 2, refused | 8,577 / 10,599 / 25,806 |
| stack-driver | stack (11) | 2, refused | 2, refused | 8,542 / 10,564 / 34,054 |
| qa-driver | O-1 (1) | 2, refused | 2, refused | 8,468 / 10,490 / 24,122 |
| coder | CR-507 | 0, 6,714 | 0, 9,790 | 8,531 / 9,357 / 13,966 |
| conflict-resolver | CR-507 | 0, 6,675 | 0, 9,074 | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| debugger | CR-507 | 0, 6,462 | 0, 8,863 | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| inspector | CR-507 | 0, 7,181 | 0, 11,225 | 8,552 / 9,378 / 15,422 |
| investigator | CR-507 | 0, 6,667 | 0, 8,735 | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| verifier | CR-507 | 0, 8,293 | 0, 19,762 | 8,556 / 9,382 / 23,963 |
| spec-writer | this CR folder | 2, refused | 2, refused | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| spec-critic | this CR folder | 2, refused | 2, refused | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| board-griller | this CR folder | 2, refused | 2, refused | 10,242 / 11,096 / 19,655 |
| retro-critic | none | 0, 2,889 | 0, 4,225 | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| demo-explorer | none | 0, 2,936 | 0, 4,746 | no own row ("Other workers": 8.2 to 8.7 KB / +826 / +826) |
| chief-of-staff | none | 0, 24,652 | 0, 22,322 | 11,636 / 11,708 / 202,396 |
| griller | none | 0, 6,623 | 0, 6,349 | 11,197 / 11,267 / 145,087 |
| foreman | none | 0, 22,277 | 0, 55,206 | 7,740 / 8,566 / 91,019 |

With `--cards`, 11 of 18 roles exit 0 as specified; refused: cr-driver, release-driver, stack-driver, qa-driver, spec-writer, spec-critic, board-griller. **"Each exits 0" is not met.** The refusals, quoted:

```text
$ brief ... (refusals)
[cr-driver, new] exit 2: error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
[release-driver, new] exit 2: error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
[release-driver, old] exit 2: error: brief: CR-507 is a change CR: its Driver is the cr-driver, not release-driver
[stack-driver, new] exit 2: error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
[stack-driver, old] exit 2: error: brief: lease 11 is not stack's live lease
[qa-driver, new] exit 2: error: brief: cannot read <worktree>/skills/chantier/cards-next/driver.md: No such file or directory
[qa-driver, old] exit 2: error: brief: O-1 is not an open QA order of batch-31
[spec-writer, new] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
[spec-writer, old] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
[spec-critic, new] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
[spec-critic, old] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
[board-griller, new] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
[board-griller, old] exit 2: error: brief: <planning>/changes/4-batch/2-actives/507-sc21-cards-foreman is not a CR folder of 1-inbox, 2-backlog/P1..P4 or 3-ready: a spec role works on an item of the inbox, the backlog or `3-ready`
```

Causes:

- The four Drivers, new cards: `roles.yaml` names their card `driver.md`, which `cards-next/` does not hold (it holds `cr-driver.md`, `stack-driver.md`, `release-driver.md`, `qa-driver.md`). `brief` reads the card before the facts, so even a role-only brief is refused. The specification's "For child 24" names the Chief of Staff's and the Griller's `card` only: child 24 must change the Drivers' too (and `concepts.md`'s Driver table, whose card cell stays `driver.md` here by section 2.1).
- The three folder roles: this CR is in `4-batch/`, and `brief` takes an inbox, backlog or `3-ready` folder only (old cards refused the same).
- release-driver, stack-driver, qa-driver, old cards: batch-31 holds no release CR, no live `stack` lease 11 and no open QA order `O-1` (a finished `add` order).

### Extra runs, not the specified ones

A staging folder per Driver (`work/r6/staging/<role>/`: `driver.md` copied from `cards-next/<role>.md`, plus `floor.md`), as the sibling CR-505's evidence did; and an inbox item (`1-inbox/simplify-cards-and-prompts`, a CR folder in the specification's sense) for the folder roles.

| role | unit | new: exit, bytes | old: exit, bytes |
| --- | --- | --- | --- |
| cr-driver (staged) | none (role only) | 0, 8,010 | 0, 59,216 |
| cr-driver (staged) | CR-507 (lease 2) | 0, 15,753 | 0, 66,959 |
| release-driver (staged) | none (role only) | 0, 8,072 | 0, 59,216 |
| stack-driver (staged) | none (role only) | 0, 8,044 | 0, 59,216 |
| qa-driver (staged) | none (role only) | 0, 5,828 | 0, 59,216 |
| spec-writer | the inbox item | 0, 3,228 | 0, 4,815 |
| spec-critic | the inbox item | 0, 3,133 | 0, 5,290 |
| board-griller | the inbox item | 0, 3,132 | 0, 11,964 |

The Chief of Staff's and the Griller's new briefs are larger than the old ones: today's `card` for them is the short `SKILL.md`, which then sends the session to its readings; the new brief holds the whole card.

## 5. Quiz (not run)

No quiz was run (the brief: `just quiz` is not run). Roles whose card changed against `bf4e4c42` (18 of 18; unchanged: none):

| role | cases under `evals/quiz/<role>/` |
| --- | --- |
| board-griller | none: no quiz owed |
| chief-of-staff | yes: quiz owed |
| coder | yes: quiz owed |
| conflict-resolver | yes: quiz owed |
| cr-driver | yes: quiz owed |
| debugger | yes: quiz owed |
| demo-explorer | yes: quiz owed |
| foreman | yes: quiz owed |
| griller | yes: quiz owed |
| inspector | none: no quiz owed |
| investigator | none: no quiz owed |
| qa-driver | none: no quiz owed |
| release-driver | yes: quiz owed |
| retro-critic | none: no quiz owed |
| spec-critic | none: no quiz owed |
| spec-writer | none: no quiz owed |
| stack-driver | yes: quiz owed |
| verifier | yes: quiz owed |

Quiz case change of round 4: `evals/quiz/chief-of-staff/a8-ask-foreign-branch.json` removed, `a8-push-refused-default-branch.json` added.

## 6. Links

306 `.md` and `.json` files under `cards-next/` read; fenced blocks skipped. `skills/*-SKILL.md` links resolve under section 6's mapping (`../chantier/references/` to `cards-next/`, `./` to `skills/<skill>/`); `forges/` links to `docs/` resolve from the same depth as `references/forges/`. Links: 22; broken: 0; no link points into `references/`. Outside `cards-next/`: the two `forges/` links to `docs/`, and one more the specification's wording does not name, `init.md`'s link to the shipped asset `assets/tour.html` (today's link, unchanged; it resolves from the same depth after the swap).

| file:line | link | resolves to |
| --- | --- | --- |
| chief-of-staff.md:41 | `init.md` | cards-next/init.md |
| concepts.md:14 | `pr-template.md` | cards-next/pr-template.md |
| forges/github.md:4 | `../../../../docs/forge-connectors.md` | docs/forge-connectors.md (outside cards-next/, from the target depth) |
| forges/gitlab.md:4 | `../../../../docs/forge-connectors.md` | docs/forge-connectors.md (outside cards-next/, from the target depth) |
| init.md:17 | `../assets/tour.html` | assets/tour.html (outside cards-next/, from the target depth) |
| skills/chantier-SKILL.md:23 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/chantier-SKILL.md:25 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/chief-of-staff-SKILL.md:25 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/chief-of-staff-SKILL.md:27 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/griller-SKILL.md:24 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/griller-SKILL.md:26 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/status-SKILL.md:23 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/status-SKILL.md:25 | `../chantier/references/sync-checkout.md` | cards-next/sync-checkout.md |
| skills/status-SKILL.md:31 | `../chantier/references/status-layout.md` | cards-next/status-layout.md |
| topics/inspector-audit.md:5 | `../pr-template.md` | cards-next/pr-template.md |
| topics/inspector-audit.md:6 | `../concepts.md` | cards-next/concepts.md |
| topics/spec-writer-extras.md:6 | `../concepts.md` | cards-next/concepts.md |
| topics/spec-writer-extras.md:7 | `../concepts.md` | cards-next/concepts.md |
| topics/ticket-summary-p2.md:5 | `../ticket-summary-example.md` | cards-next/ticket-summary-example.md |
| topics/trouble-worker.md:7 | `../concepts.md` | cards-next/concepts.md |
| topics/verifier-delta-matrix.md:9 | `../concepts.md` | cards-next/concepts.md |
| topics/verifier-description.md:11 | `../pr-template.md` | cards-next/pr-template.md |

Text naming `references/` (not links), quoted:

```text
$ git grep --untracked -n "references/" -- skills/chantier/cards-next  (long lines cut at 220)
skills/chantier/cards-next/concepts.md:82:- An extra review step (a review of the project's `AGENTS.md` `chantier` section) gets no printed opening lines: the Driver writes its prompt (`help cr-review-step`), with `Read 
skills/chantier/cards-next/skills/chantier-SKILL.md:23:At a session's start, at a batch's start and after a merge that changes `uv.lock`, the steering session, and no other, syncs, with `--sync` first: `uv run --script "
skills/chantier/cards-next/skills/chantier-SKILL.md:25:Exit 127 (`chantier launcher: uv is not on PATH (uv is the one tool chantier needs)`) or any other failure of the launcher is a stop: report its text, never another 
skills/chantier/cards-next/skills/chief-of-staff-SKILL.md:25:At a session's start, at a batch's start and after a merge that changes `uv.lock`, the steering session, and no other, syncs, with `--sync` first: `uv run --sc
skills/chantier/cards-next/skills/chief-of-staff-SKILL.md:27:Exit 127 (`chantier launcher: uv is not on PATH (uv is the one tool chantier needs)`) or any other failure of the launcher is a stop: report its text, never an
skills/chantier/cards-next/skills/chief-of-staff-SKILL.md:29:Cards: `../chantier/references/`; CLI: `../chantier/scripts/cli/`.
skills/chantier/cards-next/skills/griller-SKILL.md:24:At a session's start, at a batch's start and after a merge that changes `uv.lock`, the steering session, and no other, syncs, with `--sync` first: `uv run --script "<
skills/chantier/cards-next/skills/griller-SKILL.md:26:Exit 127 (`chantier launcher: uv is not on PATH (uv is the one tool chantier needs)`) or any other failure of the launcher is a stop: report its text, never another c
skills/chantier/cards-next/skills/griller-SKILL.md:28:Cards: `../chantier/references/`; CLI: `../chantier/scripts/cli/`.
skills/chantier/cards-next/skills/status-SKILL.md:23:At a session's start, at a batch's start and after a merge that changes `uv.lock`, the steering session, and no other, syncs, with `--sync` first: `uv run --script "<p
skills/chantier/cards-next/skills/status-SKILL.md:25:Exit 127 (`chantier launcher: uv is not on PATH (uv is the one tool chantier needs)`) or any other failure of the launcher is a stop: report its text, never another co
skills/chantier/cards-next/skills/status-SKILL.md:27:Cards: `../chantier/references/`; CLI: `../chantier/scripts/cli/`.
skills/chantier/cards-next/skills/status-SKILL.md:31:Read [status-layout](../chantier/references/status-layout.md), only for this action, and nothing else of chantier: not the main skill, not the Chief of Staff's card, n
skills/chantier/cards-next/topics/cr-review-step.md:7:Read <skill>/references/review-step.md;
skills/chantier/cards-next/topics/demo-p1.md:5:- The study: on a yes start the `demo-explorer` with the prompt of "Starting an agent", a `Read <skill>/references/demo-explorer.md;` line and the rules line, the first line
(exit 0)
```

## 7. `topics.json`

Throwaway script `work/r5/topics_check.py`, with `load_topics` from `commands/help.py`. No base name is renamed.

```text
$ uv run --no-sync --project <worktree> python work/r5/topics_check.py
load_topics: 234 topics loaded
readings resolved: 415 (0 with a #heading, 27 host maps)
CLI `help <word>` matches: --for, board, from, h, lease, lists, merge, of, refused-push, stack-merge, takes, topic, topics, watcher
  not topic names (prose or code): --for, from, h, lists, of, takes, topic, topics
base names: 38; missing from cards-next: none
roles.yaml roles: 18; topic roles outside it: none
review_by: 37 topics, values ['0.16.0']
topic names cited in cards-next: 182; not in topics.json: none
topic files no topic reads: none
(exit 0)
```

## 8. The Driver table

`driver_prompt.driver_table()` reads `skill_dir()/references/concepts.md`; for the new file `skill_dir` was pointed at a staging folder holding a copy of `cards-next/concepts.md` (`work/r6/dp-stage/`).

```text
$ work/r6/proofs.py (proof 8)
parser from <worktree>/skills/chantier/scripts/cli/src/chantier/driver_prompt.py
rows, references/concepts.md: 4
rows, cards-next/concepts.md: 4
equal, cell for cell: True
['`cr-driver`', '`take <cr>`, a CR of kind `change` or `fix`', '`driver.md`', 'the CR folder, then the absolute archive path when `take` prints one', 'yes', 'own branch']
['`release-driver`', '`take <cr>`, a CR of kind `release`', '`driver.md`', 'none', 'none', 'own branch']
['`stack-driver`', '`take stack`', '`driver.md`', 'none', 'yes', 'batch branches']
['`qa-driver`', '`order qa`', '`driver.md`', 'none', 'none', 'none']
```

```text
$ git grep --untracked -n "Change Request" -- skills/chantier/cards-next/concepts.md
skills/chantier/cards-next/concepts.md:20:## Change Request (CR)
(exit 0)
```

## The Allow rules section (section 3)

The named test reads today's `references/hosts/claude-code.md`, which this child does not edit; `work/r5/allow_check.py` runs the same assertions on `cards-next/hosts/claude-code.md`.

```text
$ pytest skills/chantier/scripts/cli/tests/test_cli_runs.py::test_the_allow_rules_json_block_lists_exactly_what_preflight_checks
.                                                                        [100%]
1 passed in 0.10s
(exit 0)
```

```text
$ python work/r5/allow_check.py
allow-rules assertions pass on cards-next/hosts/claude-code.md: 73 rules, 52 samples, 4 capability rows
(exit 0)
```

`hosts/claude-code.md`: 109,857 bytes today, 23,319 new. Round 5 cut the dated trial text and stories from the kept section; round 6 completed the Mark of lines 20 and 151 (a refusal with or without the rule set in place). Against the file before the cut (`work/r5/claude-code.before.md`): the fenced JSON block is equal; in the Allow rules table the rule cells are unchanged, the Mark cell of every row is shortened, and so are several use and risk cells; in the Capabilities table the Mark cell of all four rows changed and no other cell: lines 151, 153 and 154 lose the `(rule form)` qualifier, lines 151 and 152 their bold; line 151 also loses its batch ids, a date, the quoted refusal reason and the `foreman-refused.md` pointer (the refused routes are now named by `help refused-push` and `help refused-rebase`); lines 153 and 154 word the unproved native-stack merge more briefly. The cut stories are already told in `docs/proofs/claude-code.md`.

## 9. `just test`

No test is added or changed (`git diff --name-only` against the base shows nothing under any `tests/` folder). Base and head times were not measured separately.

## 10. Inventory and completeness table

`evidence/cards-inventory-host-and-shared.md` (how the sources were walked, the rows, the manifest action table, the completeness table, the sibling-card edits with their lines), written by `work/r5/gen.py`; round 6 changed its rows with `work/r6/host_rows.py` and its sibling-card table by hand.

## 11. Unloaded

Run against the working tree with `--untracked`, since nothing is committed.

```text
$ git grep --untracked -n cards-next -- . ":(exclude)skills/chantier/cards-next"
(no line; exit 1)
```

```text
$ git grep --untracked -n "Read this short role contract at boot\|# chantier-agent:\|chantier board" -- skills/chantier/cards-next
(no line; exit 1)
```

## 12. Gates (round 6, on the uncommitted working tree)

- `just check` from the Bash tool, `NO_COLOR` not set: exit 0, `2932 passed, 20 skipped`.
- In round 5 the same command from the PowerShell tool, whose environment sets `NO_COLOR=1`, exited 1 on two cases of `test_live_ready.py::test_the_interactive_screen_links_the_pr_and_colours_the_state_words` (it expects colour codes, which rich drops under `NO_COLOR`); not rerun in round 6. No file of `src/` or `tests/` is changed since the base.
- The allow-rules test, its twin on the new card, `load_topics` and the 1,500-byte limit of the new topics: run by `work/r6/proofs.py` (the sections above).
- Not run here: `just quiz`, `just scenario (ubuntu-latest)` and the local `scenario` gate (they need the pushed head; the Driver's part).

## Known gaps

- **"Each exits 0" (item 4) is not met**: cr-driver, release-driver, stack-driver, qa-driver, spec-writer, spec-critic, board-griller are refused as specified (quoted above). The four Drivers with `--cards` need `roles.yaml`'s `card` changed at the swap (child 24).
- **Cards over budget** (Q4): `coder.md` 1,533 (over by 33; 1,417 at `bf4e4c42`); `demo-explorer.md` 1,612 (over by 112; 1,496 at `bf4e4c42`); `retro-critic.md` 1,565 (over by 65; 1,492 at `bf4e4c42`); `spec-critic.md` 1,572 (over by 72; 1,499 at `bf4e4c42`); `spec-writer.md` 1,667 (over by 167; 1,493 at `bf4e4c42`); `verifier.md` 3,112 (over by 112; 2,996 at `bf4e4c42`); `release-driver.md` 3,811 (over by 739; 3,277 at `bf4e4c42`). The bytes are rules whose home must be a card (kind a) and the pointer to `help session-shell`; a sibling card's other lines are not this child's to cut (section 1), and only the owner raises a budget. `retro-critic.md` and `spec-critic.md` are over by the pointer line alone: without it they are within, and the folder-change ban reaches them through the topic's role list only.
- **Topics over 1,500** (Q4): 24, listed in item 3; all exist at `bf4e4c42`. Round 5 grew `release-notes.md` and `cr-rounds.md` (a link and a pointer).
- Real run not done (child 28). Quiz not run (item 5). Copilot untested.
- Do not merge: merges with children 19 to 28 as one unit, after child 28's campaign.
