# CR-515 investigation, specification sections 2 to 4

Read at head `4d12a5b`, worktree clean, nothing written there. Section 1 (the open rows) is the other
investigator's file, not read. Paths are repo-relative; `cli/` is `skills/chantier/scripts/cli/`.

## Files, entry points and the smallest change

| path | change |
|---|---|
| `docs/protective-rules.md` | new; annex A plus section 1's lines |
| `docs/proofs/cards-inventory.md` (1,481,779 B), `docs/proofs/cards-inventory-open.tsv` (19,836 B) | delete |
| `cli/tests/test_cards_inventory.py` (8,741 B), `cli/tests/cards_inventory.py` (7,950 B) | delete; only the first imports the second |
| `cli/tests/test_card_homes.py` | docstring (l.1-5), FLOOR (l.16-25), HOMES (l.28-189), one new FLOOR test |
| `cli/tests/test_brief.py` | only if the floor gains an eleventh line |
| `evals/kit/quiz.py`, `evals/kit/dry_run.py`, `evals/README.md` | section C |
| cards, `test_brief_bytes.py` | only for what section 1 restores |

No CLI source, command, refusal or hook changes. Section 2 restores nothing, so it touches no card.

## A. Section 2: the protective rules

Result: 126 lines (the 19 rows of plan section 5 as `P<n>`, the 96 statements of verdicts section D
as `A`, `B`, `C`, `D`, and 11 further lines, `-code`,
`-restart` and `-seat`, for the part of a rule that needs code). **114 `held`,
12 `to add`, 0 `restored here`, 0 not held that one card line could hold.** No floor question is
owed by section 2. The checker found every quoted span of annex A at the head (0 errors; a copy with
two altered spans gave 3 errors).

`to add` lines: `P2-code` (plan step 15, read with card-cleanup-Q2), `P11` (step 20, read with Q3;
quotes AGENTS.md and `chief-of-staff.md` for what protects today), `P13-restart` (step 16),
`P15-code` (step 7, whose text names the stack ask only), and with no plan step: `P3-code`,
`D20-code`, `P12-code`, `P13-seat`, `P14-code`, `A23-code`, `D16-code`, `A24-code`.

The "exists?", "not verified" and verdict claims, settled by reading the code:

| claim | at the head |
|---|---|
| the write guard keeps `writes:` | yes, `hooks/register.tsx`, Claude Code only |
| `push` pushes only a recorded `chantier/*` branch, with the lease | yes, `commands/push.py`; no merged check there |
| a stack with the release PR is never merged under a grant (plan: refusal to add) | held: `rails_release.release_go` answers "merge" while a CR that is not a fix is neither merged nor cancelled, grant or not |
| another project's CR is never run (plan: refusal to add) | held: `lifecycle/stages.py` refuses a folder outside this project's configured folders |
| a merged CR is refused at hand-back | yes, `commands/driver_checks.py:336`; `push` and `ship` check neither merged nor a second PR (`P14-code`) |
| `order add` refuses a non-final specification | partly: it refuses a CR that is not grilled, `lifecycle/running_batch.py` (`D20-code`) |
| `stack --out-of-draft` refuses with no local gate pass | no (`A23-code`) |
| `gate <cr> --stop` refuses another CR's driver | no caller check, `commands/gate.py`; only `--first` refuses a Driver (`A24-code`) |
| a command refuses a seat another live session holds | only `seat take` and `seat leave`, `commands/seat.py` (`D16-code`) |
| `foreman set` refuses a live lease | no (`P13-seat`); `take` does, `core/leases.py` |
| `judge` refuses an unrecorded waiver | no (`P15-code`) |
| a hand-back is never recorded for a Driver | the refusal covers the ready one (needs the lease); a blocked one needs none (note on `B6`) |
| `order merged` reads the forge or fast-forwards | no; both stay card rules (`B1`, `B2`) |

Optional wording, not required by the specification (each rule is already held): plan section 5
words floor 9 with "…never by changing the permission settings" (held by the `P9` pages, which
`cards-delete-pages-chief` moves into `chief-of-staff.md`) and floor 10 with the PID (held by
`chief-of-staff.md`). If the owner wants either: exact floor line, FLOOR, FLOOR_BYTES 1200 (floor is
554 bytes today).

How to finish the file: copy annex A, add section 1's lines in the same four columns
`| id | rule | state | home |` with new unique ids, the state spelled `` `held` ``,
`` `restored here` `` or `` `to add` ``, homes written like the annex's. Then, from any folder:

- `python -I <CR folder>/work/scratch/investigator-check-table.py <worktree> <worktree>/docs/protective-rules.md`
- `python -I <CR folder>/work/scratch/investigator-homes.py <worktree> <worktree>/docs/protective-rules.md`
  (before HOMES is edited)

The checker proves a span is there, not that it says the rule; a refusal span is searched in all CLI
sources, not in the named command's.

## B. Section 3: the tests and the other references

### HOMES

From annex A alone: **210 homes, 122 kept (65 distinct), 88 dropped; keys removed:
`test_triage_moves`, `test_board_running_lane`.** Per key, the new value, the kept lines and the
dropped names are in annex B (the PR's Deliverables). Section 1's lines can only add kept homes:
rerun the script on the final file, and add to HOMES any home a section 1 restore needs that no key
holds.

Reading of "names it" that the script applies (state it in the PR): a topic is kept when a `held` or
`restored here` line names `topics/<name>.md` or `topics/<name>-pN.md`, so an aggregate name whose
rules sit in another page is dropped; a card when a line quotes it (with `#heading`, a span under
that heading); a skill or host row when a line names it; every floor home (`floor 4` is cited by no
line and stays by the specification's rule).

### The rest of `test_card_homes.py`

- Docstring, for instance: "Each protective rule of `docs/protective-rules.md` that lives in a card,
  a skill, the floor or a host row keeps its home there. A key is the test file that first held the
  pins."
- FLOOR gains `2: "Rebase only, with ``--force-with-lease``, and only on the CR's own branch."`
  (single backticks in the file) and `8: "No image shows the username or the home folder."`.
- New test, for instance:

```python
def test_the_floor_reads_word_for_word() -> None:
    lines = (REFS / "floor.md").read_text(encoding="utf-8").splitlines()
    assert [ln for ln in lines if ln[:1].isdigit()] == [f"{n}. {FLOOR[n]}" for n in sorted(FLOOR)]
```

- `_file_gone` (l.192-203), `_gone` (l.206-215),
  `test_every_rule_pinned_in_a_removed_card_has_its_home` (l.218-222) and
  `test_a_home_that_is_gone_is_named` (l.225-227, cases topic, card, card#heading, host, floor)
  stay unchanged. No other test reads HOMES.
- `test_brief.py`: `FLOOR_BYTES` 1200 (l.22); `test_the_floor_is_short_lf_only_and_holds_the_ten_rules`
  (l.335-342) checks size, no CR, the title and `range(1, 11)`. Unchanged unless an eleventh line.

### `test_brief_bytes.py` ceilings at the head (ceiling, measured, margin in bytes)

cr-driver 11100/11090 (10); demo-explorer 2800/2785 (15); foreman 22600/22554 (46);
chief-of-staff 24400/24351 (49); verifier 5500/5448 (52); griller 6500/6441 (59); coder
4000/3939 (61); spec-writer 3000/2933 (67); spec-critic 2900/2838 (62); retro-critic 2800/2738
(62); board-griller 2900/2837 (63); inspector 4400/4336 (64); investigator 3900/3822 (78);
qa-driver 6300/6220 (80); debugger 3700/3617 (83); stack-driver 10300/10217 (83);
release-driver 10500/10407 (93); conflict-resolver 3900/3871 (29).

### References to the removed files and ids (`git grep -nE "cards-inventory|cards_inventory|inventory_rows|quiz-row-id"`)

21 lines in 6 files: `docs/proofs/cards-inventory.md` 4, `cli/tests/cards_inventory.py` 4,
`cli/tests/test_cards_inventory.py` 4 (all deleted), `evals/kit/quiz.py` 4 (l.78, 431, 443, 484),
`evals/kit/dry_run.py` 4 (l.32, 87, 1654, 1917), `evals/README.md` 1 (l.406). The wider word
"inventor" adds `test_card_homes.py:3` and `quiz.py:432,441`. The 32 `docs/proofs/claude-code.md`
and `copilot.md` links in host topics, `host_rows.py:3` and `test_host_rows.py` stay.

### Only if the floor gains a line (values derived from the count or the text of the floor)

`test_brief.py:22,335-342`; `test_card_homes.py` FLOOR; `evals/kit/quiz.py:93`
(`floor-(?:[1-9]|10)` to `floor-(?:[1-9]|1[01])`); `evals/README.md:405` (`floor-1`..`floor-10`);
`evals/kit/dry_run.py:31` and its FLOOR table (about l.1557-1568); `CONTRIBUTING.md:63` ("the ten
rules"). A change of line 4's words also reaches `test_cli_stop.py:13` and
`test_launch_modes.py:226`; of line 1's, `test_reload_rules.py:17`.

## C. Section 4: the eval kit

`evals/kit/quiz.py`

- delete l.78 `INVENTORY = ROOT / "docs" / "proofs" / "cards-inventory.md"`;
- delete `inventory_rows()` (l.431-434) with its docstring;
- `load_cases` docstring (l.439-442): `rails` are "the ids a case may name beside the floor rules and
  `R-nnn`: the scorecard's J rows.";
- l.443: `rails = scorecard_rails() if rails is None else rails`;
- l.482-484: `raise bad("rules", f"{rule!r} is no floor rule, no J row of evals/SCORECARD.md and no R-nnn id")`.

`evals/kit/dry_run.py`

- l.32: `    quiz-rule-id       a case whose `rules` name a `J` row of `SCORECARD.md` loads; `X-9999` is refused with exit 2, naming the file and the key`;
- l.87 CASES and l.1917 dispatch: `"quiz-rule-id"`, `case_quiz_rule_id`;
- l.1653-1662:

```python
def case_quiz_rule_id(run: Run) -> str:
    known = min(quiz.scorecard_rails())
    for name, rule, expected in (("known", known, 0), ("unknown", "X-9999", 2)):
        folder = run.tmp / f"quiz-rule-{name}"
        quiz_case_file(folder, "cr-driver", "rule", rules=[rule])
        code, _, err = quiz_main("cr-driver", "--plan", "--cases-dir", folder)
        need(code == expected, f"a case with the {name} J row exits {expected}",
             f"{rule}: exit {code}: {err.strip()}")
    need("key rules" in err and "rule.json" in err, "the refusal names the file and the key", err.strip())
    return f"a case naming the J row {known} loads; one naming X-9999 is refused with exit 2"
```

`case_quiz_cases` (l.1665-1688, with its J99 case) is unchanged.

`evals/README.md` l.404-406, "Cases": drop "a row id of `docs/proofs/cards-inventory.md`," so the
list reads `floor-1`..`floor-10`, a `J` row of `SCORECARD.md`, later an `R-nnn` id.

## Risks

- Byte ceilings: a section 1 restore of one line passes almost any margin above (cr-driver 10,
  demo-explorer 15); name the rise, before and after, in Known gaps. A page in a role's start brief
  counts too.
- `test_cards_inventory.py` also held restored rows' spans and checks and the quiz ids. After it,
  only `test_card_homes.py` (names and headings, no span) and the two floor tests pin the cards;
  nothing tests `docs/protective-rules.md` (the specification wants no test), so it can drift.
- Later CRs in the stack edit this file by page name. `cards-delete-pages-chief` deletes pages cited
  by `C4` (`asks`, its only home), `C21` (`demo-p2`), `C22` (`board-lines`), `B19`
  (`sync-offer-p2`), `D11` (`ticket-summary-post-p1`), `P9` and `D14` (`refused-forge-chain`, `P9`
  also `refused-push-chief-more-p2`); its table covers those pages. No line cites a page of
  `cards-delete-pages-crew` (a line its table does not place would stop it: keep section 1's homes
  clear of its 29 pages or see that its table places them). 518 and 519 rewrite aggregate and `-pN`
  names, and 516 to 518 edit HOMES; the PR lists the removed keys.
- Size: annex A is 36 KB, one line per rule; the specification says "short". Trimming homes is
  possible (keep one or two per line) but removes HOMES entries: rerun the script after any trim.
- Tests that glob `docs/*.md` will read the new file: `test_plugin_files.py` (links resolve),
  `test_command_names.py` (no old `board` command), `test_board_read_key.py` (old key words). The
  checker covers these patterns (it refuses any markdown link).

## Questions for the user

None from sections 2 to 4.

## D. Evidence plan

Docs, tests and eval kit (plus cards only if section 1 restores): nothing visible, no screenshot.

| what | before | after (at the PR head, full SHA) |
|---|---|---|
| the removed names are gone | the `git grep -nE` above: 21 lines, 6 files | same command prints nothing |
| the four files are gone, the new one added | - | `git diff --stat origin/main...HEAD` |
| every home is there | - | the checker's output: rows by state, 0 errors; row counts and per-row lines in Deliverables |
| kept, dropped, removed homes | annex B (rerun on the final table) | `test_card_homes.py` passes |
| floor word for word | `floor.md` | the new test and `test_the_floor_is_short_lf_only_and_holds_the_*` pass; the diff of `floor.md` if any |
| quiz rule ids | `quiz-row-id` in `just eval-dry-run` | `quiz-cases` and `quiz-rule-id` pass in `just eval-dry-run` |
| ceilings | the figures above | `test_brief_bytes.py` passes; any raised figure in Known gaps |
| gates | - | `just check`; the pipeline's `just scenario (ubuntu-latest)` for a card change; local `scenario` only on the stack's top CR |

Not shown by any of it: that no protective rule is missing beyond the plan's table, verdicts D and
section 1; that a span still means the rule; the behaviour of an agent with the cards (no `just
quiz`, no real batch: out of scope). I ran neither `just check`, `just eval-dry-run` nor the long
gate.

## Annex A: draft of docs/protective-rules.md

The lines between the two `~~~~` fences, as they are.

~~~~markdown
# Protective rules

The rules of chantier's cards, CLI and hook that protect the user or the repository, with where each
one lives. It replaces the old cards' inventory, removed by this change. A change that deletes or
rewords a home updates its line in the same pull request.

States: `held` (a floor line, a card, a refusal or the hook holds it), `restored here` (added by the
change that made this file), `to add` (needs code that does not exist yet). A card path is relative to
`skills/chantier/references/`; a refusal quotes a span of its message.

A plan step is a step of section 6 of the cleanup plan, in the planning surface:
`projects/chantier/changes/2-backlog/P1/card-inventory-open-rows/work/fable-review-plan.md`.

Ids: `P<n>` is row n of the plan's section 5; `A`, `B`, `C` and `D` number the statements of section D
of the review's verdicts, by slice, in their order.

## 1. Merging and the words about a merge

| id | rule | state | home |
|---|---|---|---|
| P1 | Never merge without the user's word; "you can merge" only after the ready line. | `held` | floor 1 "Never merge without the user's word."; `topics/merge-words-p2.md` "only after the `ready-to-merge` line (or `stack-ready-to-merge`) has reached you"; refusal of `judge` "the merge is the user's" |
| B1 | Check that the forge shows the PR merged into the default branch before `order merged`; unconfirmed records nothing. | `held` | `topics/wakes-forge.md` "A merge the forge does not show: record nothing"; `foreman.md` "`order merged` only for a merge the forge shows" |
| D1 | "You can merge it" only after the ready line, never on a green CI or a draft. | `held` | `topics/merge-words-p2.md` "never on a Driver's progress, a green CI or the forge's look" |
| D2 | A draft on another CR's branch is never called ready. | `held` | `topics/merge-words-p1.md` "a draft on another CR's branch is never "ready"" |

## 2. Rebase and push

| id | rule | state | home |
|---|---|---|---|
| P2 | Rebase only, with `--force-with-lease`, only the CR's own `chantier/*` branch, never the default branch, a yes included. | `held` | floor 2 "Rebase only, with `--force-with-lease`, and only on the CR's own branch."; refusal of `push` "push only pushes a CR's recorded"; `chief-of-staff.md` "the default branch and any force push of it never, a yes included"; `foreman.md` "no other branch even on a yes" |
| B9 | A steering rebase only after the branch check; a conflict stays stopped, no `--abort`, no resolution. | `held` | `topics/refused-rebase-run.md` "leave the rebase stopped (no `--abort`, no resolution)"; `topics/refused-rebase.md` "You resolve nothing." |
| A14 | No forge branch protection is read; a push refused as protected is never retried. | `held` | `foreman.md` "no failed or protected push retried, no branch protection read"; `topics/refused-push-steering.md` "and never retry it"; `topics/refused-push.md` "After a refusal never retry it and never run a raw `git push`." |
| A15 | A steering push only for `chantier/*`, never the default branch, a yes included. | `held` | `foreman.md` "no other branch even on a yes"; `chief-of-staff.md` "never the default or a protected branch"; `topics/refused-push-steering.md` "push nothing, ever; a user's yes does not push it" |
| D13 | A refused push of a non-`chantier/*` or default branch is never pushed, even on a yes. | `held` | `topics/refused-push-chief-p1.md` "push nothing, ever" |
| P2-code | For a refused push or rebase the CLI checks the branch and prints the exact command, and the agent runs it, so the host still checks it (card-cleanup-Q2). | `to add` | plan step 15, steering `push` and `rebase`. Today the rule is held by the lines above. |

## 3. Never discard work

| id | rule | state | home |
|---|---|---|---|
| P3 | Never discard work: no `stash`, `reset --hard`, `add -A`, no forced cleanup of the main checkout. | `held` | floor 5 "Never discard the worktree's work."; `cr-driver.md` "`git reset --hard` or anything that discards the worktree's work"; `topics/trouble-git.md` "never cleaned by force."; `stack-driver.md` "`git reset --hard`, or retarget a PR by hand" |
| A3 | A release's new attempt starts in a new worktree, never `reset --hard` of the old one. | `held` | `release-driver.md` "never `git reset --hard` an old one"; `topics/release-ship.md` "never a `reset --hard` of the old one" |
| A12 | The main checkout is never cleaned by force after a wrong-place git command. | `held` | `topics/trouble-git.md` "never cleaned by force." |
| B2 | The main-checkout fast-forward is only `merge --ff-only --no-overwrite-ignore`; untracked files are never touched. | `held` | `foreman.md` "`--no-overwrite-ignore` fast-forward of a clean main checkout"; `topics/main-checkout-p2.md` "never pull, reset, rebase, stash, clean, checkout, switch, nor a merge without both flags" |
| A13 | A dropped CR's PR is closed with no `--delete-branch` and no comment; a CR moved to the backlog is drafted only. | `held` | `foreman.md` "closing/drafting a dropped CR's PR per its drop order (no comment, branch kept)"; `topics/stack-changes.md` "no `--delete-branch`, no comment" |
| B13 | A dropped CR's PR is closed with no `--delete-branch` and no comment; a trashed or backlog CR's worktree and branch are never removed by the Foreman. | `held` | `foreman.md` "remove a trashed, backlog or `3-ready` CR's worktree"; `topics/drop.md` "no `--delete-branch`, no comment" |
| B18 | Never `rm -rf` or `Remove-Item -Recurse` on `.claude` or on temporary folders named by a wildcard. | `held` | `topics/host-refused.md` "`Remove-Item -Recurse -Force` or `rm -rf` on `.claude`, or on temporary folders named by a" |
| D24 | Before proposing to move a session off a worktree, check that nothing is left behind. | `held` | `topics/session-start.md` "check nothing is left behind" |
| P3-code | A hook refuses `stash`, `reset --hard` and `add -A` in a Driver's shell. | `to add` | no step of plan section 6 brings it (the plan's table: a hook deny list was filed apart). Today the rule is held by the lines above. |

## 4. Where an agent may write

| id | rule | state | home |
|---|---|---|---|
| P4 | A Driver and its workers write only where `writes:` says, never in `.git`, never in the main checkout. | `held` | hook `hooks/register.tsx` (Claude Code only) "is outside the folders this agent may write in"; `cr-driver.md` "the main checkout is read-only for you"; `topics/trouble-git.md` "A Driver and its workers write nothing in the repository's git folder" |
| A11 | A Driver and its workers write nothing in the repository's git folder. | `held` | `topics/trouble-git.md` "A Driver and its workers write nothing in the repository's git folder" |
| A19 | Never use the live `$CHANTIER` line on a scratch project; `git init` it first. | `held` | `verifier.md` "at the live planning folder, or the prompt's `$CHANTIER` at the scratch project"; `topics/verifier-scratch.md` "Never use the prompt's `$CHANTIER` line as printed: it names the live project." |
| A20 | A too-long Windows path is a stop: no shorter folder outside `writes:`. | `held` | `topics/verifier-scratch.md` "no shorter folder outside your `writes:` folders"; hook `hooks/register.tsx` (Claude Code only) "is outside the folders this agent may write in" |
| C17 | A project's clone on a surface is touched only by `git -C <clone>`; a missing clone is cloned only on the user's word. | `held` | `topics/grill-surface.md` "Never touch the project's clone but by `git -C <clone>`."; `topics/grill-surface.md` "is cloned on the user's word" |
| C21 | A demo fixture stays outside the tracked files and is removed at the end; the Chief of Staff's subagent never commits, pushes or writes in a CR worktree. | `held` | `topics/demo-p1.md` "It never starts an implementation: no commit, push, PR, or write in a CR's worktree."; `topics/demo-p2.md` "Prepare any fixture outside the repository's tracked files and remove it at the end."; `chief-of-staff.md` "let a subagent implement" |

## 5. An irreversible release action

| id | rule | state | home |
|---|---|---|---|
| P5 | An irreversible release action waits for the user; `publication done:` only from the user's quoted words; "auto" covers one release only; the tag step is never the Driver's. | `held` | floor 6 "An irreversible release action waits for the user."; refusal of `release go` "every irreversible step waits for their merge"; `chief-of-staff.md` "record "auto" and `publication done:` only from the user's own words, quoted"; `topics/release-chief-auto-p2.md` ""auto" covers this release only"; `release-driver.md` "run a step of the procedure that runs in the main checkout" |
| A4 | Half-done irreversible release work: stop, say exactly what is out, never undo it alone. | `held` | `release-driver.md` "undo half-done irreversible work: `blocked question:` says what is out"; `topics/release-ship.md` "never undo it on your own" |
| A5 | The main-checkout release step (the tag) is never the release driver's. | `held` | `release-driver.md` "run a step of the procedure that runs in the main checkout"; `topics/release-merged.md` "is never yours, in the main checkout or your worktree" |
| A6 | After a publication by someone else, never run the publication command again; check read-only. | `held` | `release-driver.md` "run the publication command again after `publication done:`"; `topics/release-merged.md` "Check read-only" |
| A25 | An image upload in a release is irreversible: `release go` first. | `held` | `release-driver.md` "run `release go`"; `topics/release-evidence.md` "is irreversible: `release go` first." |
| B16 | Run a release step in the main checkout only when the Driver handed it back; refused: change nothing, never force. | `held` | `foreman.md` "run only a step the Driver handed back; refused: change nothing, never force"; `topics/release-tag.md` "change nothing, no other way, never force" |
| D5 | `publication done:` is recorded only from the user's quoted words, never guessed. | `held` | `chief-of-staff.md` "record "auto" and `publication done:` only from the user's own words, quoted"; `topics/release-chief-after-p1.md` "Never relay a `publication done:` note the user did not give" |
| D6 | "auto" covers one release only, never the announcement, a fix, `order confirm` or a budget raise. | `held` | `topics/release-chief-auto-p2.md` ""auto" covers this release only; never an announcement, a fix's start or merge"; `chief-of-staff.md` "Widen a grant or approve an irreversible action, without the user's own word." |

## 6. A stack that holds the release PR

| id | rule | state | home |
|---|---|---|---|
| P6 | No grant lets a session merge a stack that holds the release PR. | `held` | refusal of `release go` "every irreversible step waits for their merge"; `concepts.md` "The steering session merges only under the grant, never a stack that holds it"; `topics/merge-series-stack-p2.md` "no grant lets a steering session merge a stack that holds the release PR". Note: the plan calls the refusal to add; `release go` already answers `merge`, grant or not, while another CR that is not a fix is neither merged nor cancelled |
| D7 | No grant lets a steering session merge a stack that holds the release PR; the user merges a stack. | `held` | `topics/merge-series-stack-p2.md` "no grant lets a steering session merge a stack that holds the release PR"; refusal of `release go` "every irreversible step waits for their merge" |
| B10 | Under a grant on GitHub: no merge with an open PR below; a pending merge is never sent again; read the state before a retry. | `held` | `foreman.md` "the judged head only, no open PR below, reread before a retry"; `topics/merge-github.md` "no new `PUT`"; `topics/merge-under-grant.md` "A release PR or a fix PR is merged only under the grant" |

## 7. Only the user starts work

| id | rule | state | home |
|---|---|---|---|
| P7 | Only the user starts work; a board mark or "rescan" is no go; another project's CR is never run. | `held` | floor 7 "Only the user starts work."; refusal of `open` and `order add` "is not a CR in the configured inbox, priority backlog or 3-ready"; `chief-of-staff.md` "Grill, specify, triage, order or run a CR of another project of the surface without the user's word for that CR". Note: the plan calls the refusal to add; a CR folder outside this project's configured folders is already refused |
| B12 | Never take a held CR; neither it nor the release starts while a CR is held or parked. | `held` | refusal of `take` "only the user's `order unhold"; `topics/hold.md` "Never take a held CR." |
| B21 | A cancelled dependency never frees its CR: ask, do not start it. | `held` | refusal of `take` "it starts once each is"; `topics/chain.md` "a cancelled one stays unmet: ask the user" |
| C9 | On a failed preflight condition: start nothing, offer no other way. | `held` | `chief-of-staff.md` "Start anything after one failed preflight condition, or offer another way."; refusal of `preflight` "preflight FAILED: start nothing"; `topics/batch-plan.md` "On a failure start nothing, offer no other way" |
| C10 | A forced steering mode is never swapped silently. | `held` | `topics/batch-plan-mode-p3.md` "a forced mode is never swapped silently" |
| C15 | An outside PR is archived only on the user's word, never from a forge read of the agent's own. | `held` | floor 7 "Only the user starts work."; `topics/grill-outside-pr.md` "never from a forge read of your own" |
| C16 | Another project's CR: no launch (`order add`, `open`), even on "grill it here". | `held` | `chief-of-staff.md` "Grill, specify, triage, order or run a CR of another project"; `topics/grill-surface.md` "never for a launch (`order add`, `open`)"; refusal of `open` and `order add` "is not a CR in the configured inbox, priority backlog or 3-ready" |
| D20 | The board's `running-batch` mark is a go only for a CR whose specification is final. | `held` | `topics/watcher-board-p1.md` "its specification final (`03-change-spec.md` written, no `work/specifying`"; refusal of `order add` "is not grilled: grill it first" |
| D20-code | `order add` refuses a CR whose specification is not final. | `to add` | no step of plan section 6 brings it. Section D's claim holds only in part: `order add` refuses a CR that is not grilled. |
| D21 | "Rescan" decides nothing: still ask before opening a batch. | `held` | floor 7 "Only the user starts work." |

## 8. Images

| id | rule | state | home |
|---|---|---|---|
| P8 | No image shows the username or the home folder; a leak found is replaced and told. | `held` | floor 8 "No image shows the username or the home folder."; `topics/pr-images.md` "replace the image in the description with a clean capture"; `topics/pr-images.md` "a removed attachment can stay reachable, so the user is told" |
| A16 | A leak found after an upload: replace it, tell the user, say nothing about it in the public PR. | `held` | `topics/pr-images.md` "Nothing about the leak goes in the public PR." |
| A17 | The user's own screenshot that fails the look is not uploaded or copied. | `held` | `topics/pr-images.md` "do not upload or copy it" |
| A18 | A Driver never opens an image file. | `held` | `topics/pr-extras.md` "A Driver never opens an image file" |
| D3 | For an uploaded image that showed the username or home folder, tell the user the old attachment may stay reachable. | `held` | `topics/merge-gaps-p2.md` "that the old attachment may stay reachable on the forge"; `topics/pr-images.md` "a removed attachment can stay reachable, so the user is told" |
| D4 | A screenshot asked of the user uses made-up paths, no username or home folder. | `held` | `topics/merge-gaps-p2.md` "with made-up paths, no username or home folder" |

## 9. Refusals

| id | rule | state | home |
|---|---|---|---|
| P9 | A refusal is reported with its exact text, never worked around, never retried another way, never by changing the permission settings. | `held` | floor 9 "Report a refusal with its exact text; never work around it."; `topics/refused-forge-chain.md` "never a change to the permission settings"; `topics/refused-push-chief-more-p2.md` "or a change to the permission settings" |
| A7 | Never rerun a creating forge command after a network error without checking whether it took effect. | `held` | `topics/trouble-remote.md` "check whether the first attempt took effect" |
| A8 | A forge refusal (4xx, protected branch, failed lease) is never retried as an infrastructure failure. | `held` | `topics/trouble-remote.md` "is no infrastructure failure"; `foreman.md` "no failed or protected push retried" |
| A9 | Never read a verdict, a pass or a choice into a reply out of format, never fix it. | `held` | `topics/trouble-worker.md` "never read a verdict, a pass or a choice into it, never fix it" |
| A10 | A second refused start of a worker is never retried without its model. | `held` | floor 3 "No fallback."; `concepts.md` "never retried without the model or with another" |
| D11 | A failed post is never retried another way; if an artifact fails, the comment is not posted. | `held` | floor 9 "Report a refusal with its exact text; never work around it."; `topics/ticket-summary-post-p1.md` "if an artifact fails, the comment is not posted" |
| D14 | A refused push or rebase: once, unchanged, never `--force`, never another form, never a change to the permission settings. | `held` | `topics/refused-forge-chain.md` "Never a `--force`, never another form of the command, never a change to the permission settings."; `chief-of-staff.md` "A failed lease is told at once, never retried." |
| D22 | A trial refusal is said at once with its exact text; a pass proves nothing for a Driver. | `held` | `topics/trials-p2.md` "said at once with the command and the host's exact text"; `topics/trials-p2.md` "a pass proves nothing for a Driver"; floor 9 "Report a refusal with its exact text; never work around it." |

## 10. Processes, the board and the watcher

| id | rule | state | home |
|---|---|---|---|
| P10 | Never stop a process by name, pattern or PID; the board and watcher start and stop on the user's yes. | `held` | floor 10 "Never stop a process by name or pattern; use `close --yes` only on the user's yes."; `chief-of-staff.md` "never by name, pattern or PID (floor 10)"; `chief-of-staff.md` "started on the session's yes" |
| B19 | Stop a sync holder only if it is this session's own board or watcher, on the user's yes, never by PID. | `held` | floor 10 "Never stop a process by name or pattern; use `close --yes` only on the user's yes."; `chief-of-staff.md` "never by name, pattern or PID (floor 10)"; `sync-checkout.md` "never stop or kill a process"; `topics/sync-offer-p2.md` "by the host's stop of their background shell (never by a"; `skills/chantier/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"; `skills/chief-of-staff/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"; `skills/griller/SKILL.md` "Never stop or kill a process for a sync, nor ask anyone to"; host row `name-env-holders` "never `Stop-Process`, `taskkill` or `kill` on a holder" (`hosts/claude-code.json`; `hosts/copilot.json` "never a stop or a kill of a holder") |
| C22 | The board is stopped only by `serve --restart`, one yes per restart; a refused restart's stop command is printed, never run. | `held` | floor 10 "Never stop a process by name or pattern; use `close --yes` only on the user's yes."; `topics/board-restart.md` "never run by you"; `chief-of-staff.md` "a board another session serves is the user's to stop"; `topics/board-lines.md` "Never stop it yourself except by the restart" |
| D17 | The watcher and the board start only on the session's one yes; never stop another session's watcher. | `held` | `chief-of-staff.md` "started on the session's yes"; `topics/watcher.md` "stop another session's, or start one after the user's no" |

## 11. The host's settings file

| id | rule | state | home |
|---|---|---|---|
| P11 | The user writes the allow rules, from a command the CLI builds for the running system and host; the CLI checks they are in place; no agent writes the settings; each host has its own case (card-cleanup-Q3). | `to add` | plan step 20, `preflight --add-rules`, read in the light of card-cleanup-Q3. Today the Chief of Staff still writes them; what protects the user (only the P10 rules, only added, only on the user's yes) is held by `AGENTS.md` "on the user's yes, the Chief of Staff adds to `~/.claude/settings.json` the allow rules preflight's P10 named, and nothing else there" and `chief-of-staff.md` "Editing `~/.claude/settings.json`: only the P10 allow rules preflight named, merged, nothing else there" (under "Asks first, each only on the user's yes in this turn") |
| B17 | Chantier never removes or edits an allow rule of the user's, never arms or disarms the PR monitor, and has no `gh api` allow rule. | `held` | `topics/host-allow-broad.md` "removes or edits a rule of the user's"; `topics/host-allow-broad.md` "There is no `gh api` rule"; `topics/host-auto-fix.md` "Chantier never arms, disarms or unbinds the PR monitor" |
| C1 | A broad or stale allow rule of the user's is never removed or edited by an agent. | `held` | `topics/allow-rules-more-p1.md` "never remove or edit it" |
| C2 | Nothing but `permissions.allow` of the user's settings file is written. | `held` | `topics/allow-rules.md` "Nothing else is written in any settings file"; `chief-of-staff.md` "only the P10 allow rules preflight named, merged, nothing else there" |

## 12. Tracker comments and public issues

| id | rule | state | home |
|---|---|---|---|
| P12 | A tracker comment or a public issue holds no CR number, batch, role, cost or private path; posted only on a recorded yes. | `held` | `chief-of-staff.md` "Post on a tracker issue a text, plan or demo the user did not approve for that ticket, or one naming a CR, batch, role or cost"; `topics/ticket-summary-p2.md` "No yes, nothing posted"; `topics/retro-route-chantier-p1.md` "ask a yes per issue" |
| D9 | A public chantier issue holds no project name, private path, code, CR number, batch id or person's data. | `held` | `topics/retro-route-chantier-p1.md` "no project name, private path, code or text of the target project, CR number, slug, batch id, or person's name or data" |
| D10 | A tracker comment holds no CR number, slug, batch, role, cost or private path; posted only on a recorded yes for that ticket, by the Chief of Staff only. | `held` | `chief-of-staff.md` "or one naming a CR, batch, role or cost, or let another session"; `topics/ticket-summary-p1.md` "no CR number or slug, batch, round, role, cost"; `topics/ticket-summary-p2.md` "No yes, nothing posted" |
| D12 | No agent closes or reopens an issue by hand; only the PR's closing line does. | `held` | `chief-of-staff.md` "close or reopen an issue by hand"; `topics/ticket-summary-post-p2.md` "No agent closes or reopens an issue by hand" |
| P12-code | A pattern check in the posting step. | `to add` | no step of plan section 6 brings it. Today the rule is held by the lines above. |

## 13. Never a second Driver on one CR

| id | rule | state | home |
|---|---|---|---|
| P13 | Never a second Driver on one CR: silence is no proof of death; after a mode switch every old Driver is checked ended. | `held` | refusal of `take` "is held: lease"; `foreman.md` "never on silence alone"; `topics/direct-mode-switch-p2.md` "Never assume that stopping a session ended its Agent children." |
| B5 | Silence is never a reason to start a second Driver; restart only after a proof of death or its final report. | `held` | `foreman.md` "never on silence alone"; `topics/host-driver-silence.md` "final report: never on silence"; refusal of `take` "is held: lease" |
| B6 | Never record a hand-back for a Driver. | `held` | `topics/lost-silent.md` "Never record a hand-back yourself."; refusal of `handback` "needs --lease <n>". Note: the refusal covers a ready hand-back; a blocked one needs no lease |
| B7 | A Driver stopped and not restarted at once: record `stopped:` and clear its id in the same turn. | `held` | `topics/lost-outside.md` "clear the id in the same turn" |
| B8 | A Driver stopped from outside is restarted with no ask, whatever the host says. | `held` | `topics/lost-outside.md` "no ask, no wait for the user, whatever the host's words" |
| C5 | Never assume that stopping a session ended its Agent children. | `held` | `topics/direct-mode-switch-p2.md` "Never assume that stopping a session ended its Agent children."; refusal of `take` "is held: lease" |
| C6 | After a switch back, every Driver the Chief of Staff owns is stopped before the Foreman claims. | `held` | `topics/direct-mode-back.md` "No Driver of yours runs once the Foreman claims" |
| C7 | A Foreman session is stopped by the user, or by the Chief of Staff on the yes and only by the host's named means. | `held` | `chief-of-staff.md` "Stopping a Foreman or a process you did not start"; `topics/direct-mode-switch-p2.md` "its session is stopped by the user, or by you on the user's yes where the host row names the means" |
| P13-restart | `restart` refuses on a live lease. | `to add` | plan step 16, `restart`. Today `take` refuses a live lease. |
| P13-seat | `foreman set` refuses on a live lease. | `to add` | no step of plan section 6 brings it. Today the rule is held by the lines above. |

## 14. A CR found merged, or with a PR already

| id | rule | state | home |
|---|---|---|---|
| P14 | A CR found merged, or with a PR already: nothing pushed, no second PR. | `held` | `topics/handback-refused.md` "Push nothing, edit nothing, retarget nothing"; `topics/retake.md` "never a second PR" |
| A1 | A CR found merged at hand-back: push, edit, retarget and turn nothing. | `held` | `topics/handback-refused.md` "Push nothing, edit nothing, retarget nothing, turn nothing ready or draft."; refusal of `handback` "no Driver to hand it back" |
| A2 | A CR that shows a `PR:` link at first take: never a second PR, never a new branch. | `held` | `topics/retake.md` "never a new branch"; `topics/retake.md` "never a second PR" |
| P14-code | `push` and `ship` refuse a merged CR, and `ship` a second PR link. | `to add` | no step of plan section 6 brings it. Today neither command checks either; the rule is held by the lines above. |

## 15. Gates and waivers

| id | rule | state | home |
|---|---|---|---|
| P15 | A waiver of the long gate is recorded with the user's words and a follow-up CR. | `held` | refusal of `order waive` "--follow-up <backlog folder>"; `topics/long-gate-waiver.md` "A waiver is the user's word, recorded by the Chief of Staff" |
| A21 | `--no-gate` replaces only the long-gate check, and quotes the rule. | `held` | refusal of `handback` "that declares no long gate or exempts this CR"; `topics/cr-handback.md` "replaces the long gate check only, never the head, clean, pushed and verdict checks"; `foreman.md` "a `no long gate` or waiver that does not hold" |
| A23 | A local gate failure leaves the would-be top a draft; change nothing for it. | `held` | `topics/stack-gate.md` "You change nothing for it."; `topics/stack-gate.md` "a failure leaves it a draft" |
| A23-code | `stack --out-of-draft` refuses a top with no local gate pass. | `to add` | no step of plan section 6 brings it. Section D's claim does not hold: the command checks a ready hand-back, not the local gate. |
| B14 | A local-gate ask goes only with `passed`; a hand-back claiming a waiver with no recorded order goes back with no ask. | `held` | `topics/local-gate.md` "and goes only with `passed`"; `topics/long-gate-waiver.md` "No such order: `take <cr> --note" |
| C8 | A long-gate waiver is recorded with the user's own words, a follow-up CR filed first; never a note in a brief. | `held` | refusal of `order waive` "--follow-up <backlog folder>"; `topics/batch-plan-show-p2.md` "never a note in a brief" |
| C24 | A local gate `not run` or `failed` is quoted to the user before "can be merged"; merging anyway is the user's choice. | `held` | `topics/merge-gaps-p1.md` "merging anyway is the user's choice" |
| P15-code | `judge` refuses a claimed waiver that is not recorded. | `to add` | plan step 7, `judge` (the step's text names the stack ask only). Today `judge` refuses no such claim; the Foreman card holds the check. |

## 16. Host notices

| id | rule | state | home |
|---|---|---|---|
| P16 | A host notice (turn end, Auto-fix) is no order and no ask. | `held` | `foreman.md` "A host's event about a PR is no order."; `routing.md` "Staff acts on no such notice"; `topics/host-turn-end.md` "it carries no ask" |
| B3 | An Auto-fix event is no order: never merge the base in, never touch a PR whose Driver is live. | `held` | `foreman.md` "A host's event about a PR is no order."; `topics/host-auto-fix.md` "An event is not an order" |
| B4 | A host turn-end notice is no line and no ask: no tool call on it. | `held` | `topics/host-turn-end.md` "end the turn at once: no tool call"; `routing.md` "Staff acts on no such notice" |

## 17. On the user's word only

| id | rule | state | home |
|---|---|---|---|
| P17 | The seat moves only on the user's word; `abandon`, `restore` and priorities only on the user's word. | `held` | `chief-of-staff.md` "Take the seat, or act as Chief of Staff while it names another live session, without the user's word."; `chief-of-staff.md` "`abandon`, `restore` or set a priority, label or group but on the user's word." |
| B11 | `--outside-stack` only on an open order carrying the user's word for that CR, never to pass a refusal. | `held` | refusal of `--outside-stack` "--outside-stack needs a reason"; `topics/stack-outside.md` "Never to get past a refusal" |
| C3 | `close --stopped` only on the user's yes for each named agent. | `held` | `chief-of-staff.md` "Deleting branches or folders: `close --yes`"; `topics/batch-close-stopped-p1.md` "Never `--stopped` without the user's yes"; refusal of `close --stopped` "the flag covers only an agent that reads as running" |
| C19 | An install only on the user's yes; `gh auth login` stays the user's; chantier changes no forge setting. | `held` | `chief-of-staff.md` "never a forge or app setting"; `topics/init-tools.md` "`gh auth login` is interactive and stays the user's" |
| C20 | `long_gate` lines are written to `chantier.yaml` only on the user's yes. | `held` | `chief-of-staff.md` "project file writes"; `topics/init-checks.md` "written only on the user's yes" |
| D8 | Never choose a dropped CR's destination for the user. | `held` | refusal of `order drop` "ask the user when they have not said it"; `topics/order-drop.md` "Never choose for the user" |
| D15 | The seat moves only on the user's word and the new session's acknowledgement; no running Driver is stopped or moved. | `held` | `chief-of-staff.md` "Take the seat, or act as Chief of Staff"; `topics/seat-handover.md` "A running Driver is never stopped nor moved."; refusal of `seat take` "take it over only on the user's word" |
| D16 | Two live Chiefs of Staff: do no Chief of Staff work until the user chooses. | `held` | `chief-of-staff.md` "act as Chief of Staff while it names another live session"; `topics/seat-p2.md` "do no Chief of Staff work until the user chooses" |
| D16-code | A command refuses a session whose seat another live session holds. | `to add` | no step of plan section 6 brings it. Today only `seat take` and `seat leave` refuse. |
| D18 | The board is exposed on the network only on the user's word. | `held` | `topics/remote-login.md` "on the user's word, `board.host: network`" |
| D19 | `cancel` only after a drop the user ordered, never to stop a CR that goes on. | `held` | `chief-of-staff.md` "`cancel` follows only a drop the user ordered"; `topics/recovery.md` "never use it to stop the processes of a CR that goes on" |
| D23 | A `chantier.yaml` long-gate entry is written in the main checkout only on the user's yes. | `held` | `chief-of-staff.md` "project file writes"; `topics/project-rules-p2.md` "written on the user's yes in the code repository's root `chantier.yaml`" |
| D25 | A rounds exception only for a red the batch caused, one per cause, never above `max_rounds` + 2; every other grant is the user's. | `held` | `topics/rounds-exception.md` "never above `max_rounds` + 2"; `topics/rounds-exception.md` "Every other grant of rounds stays the user's." |

## 18. The planning surface

| id | rule | state | home |
|---|---|---|---|
| P18 | The planning surface is committed and pushed only by its writer. | `held` | `chief-of-staff.md` "Commit, pull, push or force-push the planning surface: its writer does."; `griller-skill.md` "commit, pull and push nothing"; refusal of `a write command` "the surface's writer is not running: nothing written" |
| C18 | A Griller in a surface worktree commits nothing, opens no PR and runs no `triage` or `summary` command. | `held` | `griller-skill.md` "run no `triage`"; `topics/griller-worktree.md` "run no `triage` and no `summary` command there" |

## 19. The grill

| id | rule | state | home |
|---|---|---|---|
| P19 | Record each grill answer at once in the user's words; never decide "grilled enough" alone. | `held` | `griller-skill.md` "Record each answer in `02-answers.md` at once"; `griller-skill.md` "Restate in full before "grilled enough?"."; `griller.md` "each answer recorded in `02-answers.md` at once"; `topics/grill-restate.md` "Never decide alone that a CR is grilled enough." |
| C11 | Record every answer or decision at once, with the date and the user's words. | `held` | `griller-skill.md` "Record each answer in `02-answers.md` at once"; `topics/grill-backlog-p1.md` "Record at once, with date and words" |
| C12 | Never decide alone that a CR is grilled enough; ask only after a full restatement. | `held` | `griller-skill.md` "Restate in full before "grilled enough?"."; `topics/grill-restate.md` "Never decide alone that a CR is grilled enough." |
| C14 | A critic finding that touches behaviour, scope or risk is a question to the user. | `held` | `topics/grill-critic-steps.md` "a finding that touches behaviour (scope, behaviour, risk) is a question" |

## Statements no row of the plan's table groups

| id | rule | state | home |
|---|---|---|---|
| A22 | Never skip a proof pass to save budget. | `held` | `topics/handback-other.md` "Never skip a proof pass to save budget" |
| A24 | Never stop another CR's gate, nor your own because it is slow. | `held` | `cr-driver.md` "run `gate <cr> --stop` on another CR's gate"; `topics/trouble-gate.md` "Never because it is slow" |
| A24-code | `gate <cr> --stop` refuses a caller that does not drive that CR. | `to add` | no step of plan section 6 brings it. Section D's claim does not hold: the command stops the named CR's gate for any caller. |
| B15 | `gate --first` only for the critical path or the user's next merge, never at a Driver's request. | `held` | `foreman.md` "`gate --first`: a critical-path CR or the user's next merge only, not on a Driver's say."; `topics/long-gate.md` "nor at a Driver's request alone"; refusal of `gate --first` "a Driver never moves its own gate" |
| B20 | Never chain a started CR; a shared file alone is no reason. | `held` | `topics/chain.md` "A shared file alone is no reason, and a CR that has started is never chained."; refusal of `order after` ", not queued" |
| B22 | The retro critic's verdicts are followed as given; its brief carries evidence, never an argument. | `held` | `retro-critic.md` "Judge the evidence, not an author's argument or preference."; `topics/retro-critic-write.md` "Follow the verdicts as given"; `topics/retro-critic.md` "never your argument, ranking or preference" |
| C4 | `asks --read all` is never used to clear the list. | `held` | `topics/asks.md` "never to clear the list" |
| C13 | The spec critic never edits the specification and runs once. | `held` | `topics/grill-critic.md` "runs once per specification, never in a loop" |
| C23 | No delivery time without its floor; none when the gate's time is unknown; no gate run to measure it. | `held` | `chief-of-staff.md` "Tell a delivery time but from the terms of `help delivery-time`"; `topics/delivery-time-p2.md` "run no gate to measure it" |
~~~~

## Annex B: HOMES per key, from annex A alone

#### test_role_cards_split: 38 kept, 33 dropped (of 71)
- new topics string: "batch-close-stopped batch-plan batch-plan-mode delivery-time grill-backlog handback-other hold main-checkout merge-gaps merge-series-stack merge-under-grant merge-words pr-extras recovery refused-push refused-rebase release-merged release-ship retake retro-critic retro-route-chantier stack-changes trials trouble-gate trouble-git trouble-remote trouble-worker"
- new list: ['card chief-of-staff.md', 'card foreman.md', 'card release-driver.md', 'card stack-driver.md', 'card verifier.md', 'floor 1', 'floor 10', 'floor 5', 'floor 6', 'floor 7', 'floor 9']
- kept, with its lines: topic batch-close-stopped = C3; topic batch-plan = C9; topic batch-plan-mode = C10; topic delivery-time = C23; topic grill-backlog = C11; topic handback-other = A22; topic hold = B12; topic main-checkout = B2; topic merge-gaps = D3 D4 C24; topic merge-series-stack = P6 D7; topic merge-under-grant = B10; topic merge-words = P1 D1 D2; topic pr-extras = A18; topic recovery = D19; topic refused-push = A14; topic refused-rebase = B9; topic release-merged = A5 A6; topic release-ship = A3 A4; topic retake = P14 A2; topic retro-critic = B22; topic retro-route-chantier = P12 D9; topic stack-changes = A13; topic trials = D22; topic trouble-gate = A24; topic trouble-git = P3 A12 P4 A11; topic trouble-remote = A7 A8; topic trouble-worker = A9; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; card foreman.md = B1 P2 A14 A15 B2 A13 B13 B16 B10 A8 P13 B5 A21 P16 B3 B15; card release-driver.md = A3 P5 A4 A5 A6 A25; card stack-driver.md = P3; card verifier.md = A19; floor 1 = P1; floor 10 = P10 B19 C22; floor 5 = P3; floor 6 = P5; floor 7 = P7 C15 D21; floor 9 = P9 D11 D22
- dropped: topic batch-pause, topic compacting, topic conflict-check, topic conflicts, topic cr-prompt, topic cr-rounds, topic direct-mode, topic forge-permissions, topic lease, topic lost-driver, topic matrix, topic merge, topic merge-stack-ready, topic mode-switch, topic options, topic park, topic refusals-to-say, topic refused-push-answer, topic release-chief, topic release-end, topic release-notes, topic release-take, topic retro-route, topic stack, topic stack-changes-chief, topic stack-joins, topic stack-make, topic stack-run, topic steering-messages, topic steering-reports, topic take-back, topic writer, card debugger.md

#### test_startup_manifest: 9 kept, 4 dropped (of 13)
- new topics string: "grill-surface seat session-start"
- new list: ['card chief-of-staff.md', 'card concepts.md#Starting an agent', 'card foreman.md', 'card griller-skill.md#Never', 'skill chief-of-staff', 'skill griller']
- kept, with its lines: topic grill-surface = C17 C16; topic seat = D16; topic session-start = D24; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; card concepts.md#Starting an agent = A10; card foreman.md = B1 P2 A14 A15 B2 A13 B13 B16 B10 A8 P13 B5 A21 P16 B3 B15; card griller-skill.md#Never = P18 C18; skill chief-of-staff = B19; skill griller = B19
- dropped: topic first-turn, topic foreman-start, topic reload, topic restart

#### test_session_start_split: 10 kept, 4 dropped (of 14)
- new topics string: "board-lines board-restart seat sync-offer watcher"
- new list: ['card chief-of-staff.md', 'card griller-skill.md#Never', 'card sync-checkout.md', 'skill chief-of-staff', 'skill griller']
- kept, with its lines: topic board-lines = C22; topic board-restart = C22; topic seat = D16; topic sync-offer = B19; topic watcher = D17; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; card griller-skill.md#Never = P18 C18; card sync-checkout.md = B19; skill chief-of-staff = B19; skill griller = B19
- dropped: topic board, topic reload, topic titles, topic wakes

#### test_stack_chain_cards: 6 kept, 4 dropped (of 10)
- new topics string: "cr-handback refused-push release-ship retake"
- new list: ['card cr-driver.md', 'card stack-driver.md']
- kept, with its lines: topic cr-handback = A21; topic refused-push = A14; topic release-ship = A3 A4; topic retake = P14 A2; card cr-driver.md = P3 P4 A24; card stack-driver.md = P3
- dropped: topic retake-notes, topic stack-grows, topic stack-record, topic stack-restack

#### test_stack_shape: 5 kept, 4 dropped (of 9)
- new topics string: "batch-plan-mode merge-series-stack stack-outside"
- new list: ['card foreman.md', 'floor 7']
- kept, with its lines: topic batch-plan-mode = C10; topic merge-series-stack = P6 D7; topic stack-outside = B11; card foreman.md = B1 P2 A14 A15 B2 A13 B13 B16 B10 A8 P13 B5 A21 P16 B3 B15; floor 7 = P7 C15 D21
- dropped: topic stack, topic stack-checks, topic stack-merge, topic stack-takes

#### test_reload_rules: 6 kept, 3 dropped (of 9)
- new topics string: "batch-plan-mode merge-gaps merge-series-stack merge-words"
- new list: ['card foreman.md', 'floor 1']
- kept, with its lines: topic batch-plan-mode = C10; topic merge-gaps = D3 D4 C24; topic merge-series-stack = P6 D7; topic merge-words = P1 D1 D2; card foreman.md = B1 P2 A14 A15 B2 A13 B13 B16 B10 A8 P13 B5 A21 P16 B3 B15; floor 1 = P1
- dropped: topic merge-recorded, card status-layout.md, card status-layout.md#The rules of every report

#### test_came_back: 16 kept, 19 dropped (of 35)
- new topics string: "hold order-drop project-rules refused-push refused-push-chief refused-push-chief-more retake stack-changes watcher-board"
- new list: ['card chief-of-staff.md', 'card cr-driver.md', 'card foreman.md', 'card routing.md', 'floor 10', 'floor 7', 'floor 9']
- kept, with its lines: topic hold = B12; topic order-drop = D8; topic project-rules = D23; topic refused-push = A14; topic refused-push-chief = D13; topic refused-push-chief-more = P9; topic retake = P14 A2; topic stack-changes = A13; topic watcher-board = D20; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; card cr-driver.md = P3 P4 A24; card foreman.md = B1 P2 A14 A15 B2 A13 B13 B16 B10 A8 P13 B5 A21 P16 B3 B15; card routing.md = P16 B4; floor 10 = P10 B19 C22; floor 7 = P7 C15 D21; floor 9 = P9 D11 D22
- dropped: topic batch-close, topic checkpoints, topic driver-question, topic merge-recorded, topic merge-stack-ready, topic park, topic park-back, topic refused-push-answer, topic refused-push-route, topic refused-push-run, topic restart, topic retake-notes, topic retro, topic session-start-surface, topic stack-changes-chief, topic stack-drop, topic steering-messages, topic take-back, topic where-cr-goes

#### test_release_tag: 2 kept, 0 dropped (of 2)
- new topics string: "release-merged release-tag"
- new list: []
- kept, with its lines: topic release-merged = A5 A6; topic release-tag = B16

#### test_rebase_rules: 2 kept, 0 dropped (of 2)
- new topics string: "refused-push refused-rebase"
- new list: []
- kept, with its lines: topic refused-push = A14; topic refused-rebase = B9

#### test_triage_moves: 0 kept, 1 dropped (of 1)
- dropped: topic session-shell

#### test_cli_stop: 5 kept, 4 dropped (of 9)
- new topics string: ""
- new list: ['card concepts.md#Starting an agent', 'floor 3', 'floor 4', 'floor 9', 'skill chantier']
- kept, with its lines: card concepts.md#Starting an agent = A10; floor 3 = A10; floor 4 = floor home, no line; floor 9 = P9 D11 D22; skill chantier = B19
- dropped: topic config, topic cr-workers, topic session-shell, topic worker-shell

#### test_watcher_step: 1 kept, 3 dropped (of 4)
- new topics string: "watcher"
- new list: []
- kept, with its lines: topic watcher = D17
- dropped: topic foreman-start, topic watcher-events, topic watcher-lines

#### test_event_audience: 2 kept, 1 dropped (of 3)
- new topics string: "seat"
- new list: ['card chief-of-staff.md']
- kept, with its lines: topic seat = D16; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23
- dropped: topic watcher-events

#### test_board_restart: 4 kept, 2 dropped (of 6)
- new topics string: "batch-close-stopped board-restart"
- new list: ['card chief-of-staff.md', 'floor 10']
- kept, with its lines: topic batch-close-stopped = C3; topic board-restart = C22; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; floor 10 = P10 B19 C22
- dropped: topic board, host run-board

#### test_board_running_lane: 0 kept, 1 dropped (of 1)
- dropped: topic where-cr-goes

#### test_command_names: 2 kept, 0 dropped (of 2)
- new topics string: ""
- new list: ['card sync-checkout.md', 'skill chief-of-staff']
- kept, with its lines: card sync-checkout.md = B19; skill chief-of-staff = B19

#### test_release_template_card: 2 kept, 1 dropped (of 3)
- new topics string: "pr-extras release-evidence"
- new list: []
- kept, with its lines: topic pr-extras = A18; topic release-evidence = A25
- dropped: card release-template.md#The notes

#### test_launch_modes: 12 kept, 4 dropped (of 16)
- new topics string: "batch-close-stopped board-lines board-restart sync-offer"
- new list: ['card chief-of-staff.md', 'card concepts.md#Starting an agent', 'card sync-checkout.md', 'floor 10', 'floor 4', 'skill chantier', 'skill chief-of-staff', 'host name-env-holders']
- kept, with its lines: topic batch-close-stopped = C3; topic board-lines = C22; topic board-restart = C22; topic sync-offer = B19; card chief-of-staff.md = P2 A15 C21 P5 D5 D6 P7 C9 C16 D14 P10 B19 C22 D17 C2 P12 D10 D12 C7 P17 C3 C19 C20 D15 D16 D19 D23 P18 C23; card concepts.md#Starting an agent = A10; card sync-checkout.md = B19; floor 10 = P10 B19 C22; floor 4 = floor home, no line; skill chantier = B19; skill chief-of-staff = B19; host name-env-holders = B19
- dropped: topic session-shell, topic session-start-surface, topic status-notes, topic worker-shell

total 210, kept 122, dropped 88, distinct kept 65, removed keys ['test_triage_moves', 'test_board_running_lane']
