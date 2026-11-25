# SC21 evidence: inventory of the Foreman's rules

Round 1. Ids (`FM-nnn`) are drafts that child 26 replaces. The new card and topics are in `skills/chantier/cards-next/` (`foreman.md`, `topics/`, `topics.json`).

## How the sources were walked

- The sources are `skills/chantier/references/foreman.md` (393 lines) and its eight pieces at the worktree's base: foreman-stack (197 lines), foreman-merge (139), foreman-hold (87), foreman-lost-driver (130), foreman-conflict (45), foreman-release (48), foreman-refused (163), foreman-pause (25).
- Same columns and kinds as `cards-inventory-drivers.md`: kind a protects the user or the repository, b inferable, c incident, d trial bookkeeping, e CLI-printable, f duplicate. When unsure, a. A protecting rule (F5) is never "inferable": it sits in the card (Never), the floor or a refusal.
- Granularity: one row per section or bullet group of a source, by its line range, a group holding several rules is split in the `behaviour` column; the B rows of the specification's section 4 ("The user's boundaries", `foreman.md:59-184`) are one row each, B1a to B7f, with their final home. Pure transitions ("Next:", "read X when Y") get no row. The old moment and startup machinery is replaced by `brief` and `help` (kind e).
- Checks: `grep` names a phrase to look for in the card or topic; `help` means `$CHANTIER help <topic>` prints it (`load_topics` loads `topics.json`, every reading exists, every role is in `roles.yaml`, every `review_by` is `0.16.0`); `quiz` names the case for child 25. No quiz was run: the quiz command is in `work/r1.md`.
- Roles of every topic row: `foreman` and `chief-of-staff`. `lease` and `refused-push` are shared rows that now carry both roles.

## foreman.md and its sections outside "The user's boundaries"

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-001 | foreman | every run | Runs in the background for the Chief of Staff, drives the batch's CRs through Drivers; never codes | foreman.md:1-19 | a | card foreman.md (goal, You own) | grep 'You own' foreman.md |
| FM-002 | foreman | start | Startup core, rules, moments, the entry reads | foreman.md:186-203 | e | `brief foreman` and `help` | brief builds |
| FM-003 | foreman | start | The means: the commands (`next`, `judge`, `take`, `status`, `inbox`, `asks`, `agents set`) and the epoch | foreman.md:204-393 | e/a | card Start, Messages; the commands print `next:`; `judge` words the asks | grep 'judge' foreman.md |
| FM-004 | foreman | a Driver's hand-back | Reads it, judges it, asks once; sends `judge`'s line unchanged with `--record` | foreman.md:204-260 | a | card (the asks bullet), `take-back` | grep 'unchanged' foreman.md |
| FM-005 | foreman | a ready CR | The `ready`, `final` and `pong` lines | foreman.md:260-330 | a | card, reply lines byte for byte | grep 'pong' foreman.md |
| FM-006 | foreman | rare lines | chain, unconfirmed, switched to direct mode, merged early, release, parked, push, pushed, rebase | foreman.md:330-393 | c | topics `chain`, `mode-switch`, `merge`, `release-take`, `park`, `refused-push`, `refused-rebase` | help |
| FM-007 | foreman | heartbeat | Wakes: a note does not wake; `inbox` | foreman.md | e | topic `wakes`; card Messages | help wakes |
| FM-008 | foreman | `next` names an order | Open orders of the Chief of Staff, `order done` | foreman.md | a | topic `orders` | help orders |
| FM-009 | foreman | batch end | Cleanup of the kept worktrees | foreman.md | a | topic `cleanup`; card never 6 | help cleanup |
| FM-010 | foreman | escalation | A model escalation order | foreman.md | b | topic `escalation` | help escalation |
| FM-011 | foreman | QA | A QA order | foreman.md | a | topic `qa-order` | help qa-order |
| FM-012 | foreman | chains | A CR waiting on another | foreman.md | a | topic `chain` | help chain |

## foreman-stack.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-020 | foreman | a stack batch | Behaves as a parallel batch until the first stack; `alone asks`; the shape line; `--outside-stack` only on an order that carries the user's word, reason starting with the order id | foreman-stack.md:1-50 | a | topic `stack`; refusal `check_shape` | help stack |
| FM-021 | foreman | a ready CR behind a draft PR | Waits; the ask about a blocked CR names the ready one behind; the final-order take ends the wait | foreman-stack.md:21-50 | b | topic `stack` | help stack |
| FM-022 | foreman | `shape: through the stack` note | Follows the shape line's `next` | foreman-stack.md:21-50 | e | topic `stack` | help stack |
| FM-023 | foreman | the first take and each later take | The CLI computes each base; pass it unchanged; `merged:` notes during a stack driver; `not on its place` rebase notes; the final-order take; park | foreman-stack.md:51-97 | a | topic `stack-grows` | help stack-grows |
| FM-024 | foreman | `deliver by <time>` | Free slots to the CRs that can join by then; at the time the stack as it stands is asked, local-gate clause included | foreman-stack.md | a | topic `stack-deliver` | help stack-deliver |
| FM-025 | foreman | a stack driver to run | `take stack`, never the driver itself; `agents set stack`; the hand-back lines and the asks (`stack-ready-to-merge`, partial and complete); the local-gate clause sent only with `passed`; context, lost and anomaly hand-backs | foreman-stack.md:98-152 | a | topic `stack-run` | help stack-run |
| FM-026 | foreman | a drop in a stack, a heavy CI | `drop:` notes, the held CR's drop, `heavy-ci` ask | foreman-stack.md | a | topic `stack-drop` | help stack-drop |
| FM-027 | foreman | the stack on the forge | The five checks, gaps recorded, `insert:` sequence, no PR edited by the Foreman | foreman-stack.md:153-175 | a | topic `stack-checks` | help stack-checks |
| FM-028 | foreman | a merge in a stack | A restack when a native stack is on the forge; the folded CR; rebase notes before the first stack; the choice said in one clause | foreman-stack.md:176-197 | a | topic `stack-merge` | help stack-merge |

## foreman-merge.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-030 | foreman | `order merged`, by mode | What each mode does after a merge | foreman-merge.md:3-41 | a | topic `merge` | help merge |
| FM-031 | foreman | the main checkout after a merge | The fast-forward is the only move; clean checkout; the planning checkout never touched | foreman-merge.md:42-88 | a | card never 3 and 4; topics `main-checkout`, `sync` | grep 'fast-forward' foreman.md |
| FM-032 | foreman | merging on GitHub | A release or a fix merged only under the grant; the merge command and its refusals | foreman-merge.md:89-113 | a | card never 1; topic `merge-under-grant` | help merge-under-grant |
| FM-033 | foreman | a CR taken back from ready | A note, `status` first, `wait clear`, no ask | foreman-merge.md:114-139 | a | topic `take-back`; card Messages | help take-back |

## foreman-hold.md, foreman-lost-driver.md, foreman-conflict.md, foreman-release.md, foreman-pause.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-040 | foreman | an order to hold | A held CR: what is held, what waits, how it is released; a held CR's drop | foreman-hold.md:3-31 | a | topic `hold` | help hold |
| FM-041 | foreman | an outside wait | Parking a CR on a wait, out of the stack, `take stack --note park` | foreman-hold.md:32-61 | a | topic `park` | help park |
| FM-042 | foreman | a switch to direct mode | Hands the batch to the Chief of Staff, what stays recorded | foreman-hold.md:62-87 | c | topic `mode-switch` (review_by 0.16.0) | help mode-switch |
| FM-043 | foreman | a `working` CR whose Driver ended | `inbox`, the host's end, `agents set <cr> -`, the resume note, a new Driver | foreman-lost-driver.md:3-70 | a | topic `lost-driver`, `lost-restart` | help lost-driver |
| FM-044 | foreman | a `blocked context:` hand-back | Take back with `resume:`, a new Driver | foreman-lost-driver.md | a | topic `lost-context` | help lost-context |
| FM-045 | foreman | a Driver stopped from outside | The user or a tool stopped it; no restart without a word | foreman-lost-driver.md | c | topic `lost-outside` (review_by 0.16.0) | help lost-outside |
| FM-046 | foreman | ready CRs with PRs in a parallel batch | `conflicts <cr> --epoch <n>`; the git is the CLI's (`git merge-tree`); the ask `conflict ... switch to a stack?` | foreman-conflict.md:3-45 | a | topic `conflict-check` | help conflict-check |
| FM-047 | foreman | the release CR | Take it last; the tag, the notes; the grant | foreman-release.md:3-48 | a | topics `release-take`, `release-tag`; card never 1 | help release |
| FM-048 | foreman | the batch's end | The retro: `retro draft`, the points, the critic | foreman-pause.md:3-25 | b | topics `retro`, `retro-critic` | help retro |
| FM-049 | foreman | a hand-over, a stopped writer | Rare incident readings | foreman.md | c | topics `handover`, `writer-off` (review_by 0.16.0) | help handover |

## foreman-refused.md

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-050 | foreman | `[driver <cr>→foreman] push <branch> <expected> <local>` | The ladder; the check (`chantier/*`, not the default branch, `--force-with-lease`); `handoff`'s branch must match; a branch not `chantier/*` is never pushed | foreman-refused.md:3-69 | a | card never 3 (route push after the check); topic `refused-push-steering` | grep 'refused push' foreman.md; help refused-push |
| FM-051 | foreman | a push to judge | The read-only judgement; the gate-at-the-head check and its skips; two refusals taken back; not legitimate: `asks` | foreman-refused.md:24-56 | a | topic `refused-push-judgement` | help refused-push-judgement |
| FM-052 | foreman | a legitimate push | P10's route rule; the route form, one command per branch; the notes; the host refuses you: line to the Chief of Staff; failed lease and protected branch: never retried | foreman-refused.md:70-113 | a | topic `refused-push-route` | help refused-push-route |
| FM-053 | foreman | the answer to a refused push or rebase | Taken back by the restart path, no ping to a Driver that handed back | foreman-refused.md:114-130 | a | topic `refused-answer` | help refused-answer |
| FM-054 | foreman | `rebase <branch> <base>` | The same ladder, the check, the rule, one command, a conflict left stopped, never `--exec` | foreman-refused.md:131-163 | a | topic `refused-rebase` | help refused-rebase |
| FM-055 | foreman | a stale lease, `claim lost` | `next`'s item; `take --reclaim` only on the user's word; `lease hold` | foreman.md | a | topic `lease-steering` (row `lease`); card never 6 | help lease |

## "The user's boundaries" (B rows of the specification, section 4)

| id | role | trigger | behaviour | source | kind | new home | check |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FM-B1a | foreman | an ask | Never merge without the user's word; readiness words; a draft is never mergeable | foreman.md:59-184 | a | floor 1; `judge` words it; card never 1 | grep 'Merge' foreman.md |
| FM-B1b | foreman | an ask | An ask's icon is the CR's state | foreman.md:59-184 | b | `judge` carries no icon: the rule disappears | none |
| FM-B1c | foreman | a stack CR ready | Readiness reaches the user through the stack | foreman.md:59-184 | a | refusal `check_shape` / `shape_refusal`; `judge` prints `no ask:`; steps in `stack` | help stack |
| FM-B1d | foreman | a draft's text, `gaps:` | Stay in the ask as written | foreman.md:59-184 | a | `judge` copies verbatim; card never 2 | grep 'unchanged' foreman.md |
| FM-B1e | foreman | an image note | Relay a replaced username or an unuploaded screenshot | foreman.md:59-184 | a | floor 8; `judge` copies the gaps; the card's "send its line unchanged" (Known gap for child 25 if `judge` does not carry such a note) | quiz |
| FM-B1f | foreman | a gap | Invent none, drop none; a gap the body lacks is a take-back with no ask | foreman.md:59-184 | a | card never 2; `take-back` | grep 'gap' foreman.md |
| FM-B1g | foreman | order note `evidence: <path>` | `take <cr> --note "evidence: <path>"` | foreman.md:59-184 | b | `orders` | help orders |
| FM-B1h | foreman | `--no-gate` | The check against the rules (exemption, files, job green at head) | foreman.md:59-184 | a | card never 2; `long-gate` | help long-gate |
| FM-B1i | foreman | a stack's top `--no-gate` | Back when the rules ask a local run | foreman.md:59-184 | a | card never 2; `local-gate` | help local-gate |
| FM-B1j | foreman | a CR owing the local run | Back when not passed | foreman.md:59-184 | a | card never 2; `local-gate`; `judge --local-gate` | help local-gate |
| FM-B1k | foreman | `deliver by` | The ask goes with `not run` or `failed` | foreman.md:59-184 | b | `local-gate`; `judge --local-gate` | help local-gate |
| FM-B1l | foreman | a declared long gate that covers the CR | Take back | foreman.md:59-184 | a | card never 2; `long-gate` | help long-gate |
| FM-B1m | foreman | rules silent on a long gate | `question ... no long gate written down`; absent never means success | foreman.md:59-184 | a | card never 2; `long-gate` | help long-gate |
| FM-B1n | foreman | a waiver | Holds only with the recorded order; does not waive the local run unless it names the gate | foreman.md:59-184 | a | card never 2; `long-gate`, `local-gate` | help long-gate |
| FM-B1o | foreman | a release PR | Merged only under the grant after `release go` says `go` | foreman.md:59-184 | a | floor 6; card never 1; refusal `release go`; `merge-under-grant` | grep 'grant' foreman.md |
| FM-B1p | foreman | a fix | Merged only under the grant, local run passed, `order merged`, then the fast-forward | foreman.md:59-184 | a | card never 1; refusal `check_granted_fix`; `merge-under-grant`, `main-checkout` | help merge-under-grant |
| FM-B2 | foreman | the limits | The CLI's; a refusal is a fact; slots as opened unless `order slots` | foreman.md:59-184 | a | refusals `check_slot`, `check_budget`, `check_round`; floor 9 | none |
| FM-B2b | foreman | a spent budget, a question, an approval | One ask, once | foreman.md:59-184 | b | `judge`, `next` (`due:`); `escalation` | help escalation |
| FM-B3 | foreman | a refusal not understood | `access <cr> --epoch <n>` | foreman.md:59-184 | b | the refusals name the next command; the card says nothing | none |
| FM-B4 | foreman | the rounds exception | | foreman.md:59-184 | b | `orders` | help orders |
| FM-B5a | foreman | orders | The user's word; `pause` waits for them all | foreman.md:59-184 | a | refusal `pause`; card "You own" | grep 'orders' foreman.md |
| FM-B5b | foreman | `cancel` | Moves to the recorded destination; never chosen; a refusal goes up as an ask | foreman.md:59-184 | a | refusal `cancel <cr>: no destination recorded`; `orders` | help orders |
| FM-B5c | foreman | work on a CR handed back | Only through `take --note`; a plain `status` first | foreman.md:59-184 | a | card Messages; `take-back` | grep 'take --note' foreman.md |
| FM-B5d | foreman | blocked with typed waits | `wait clear`, then take back | foreman.md:59-184 | b | `take-back`; `next` names the wait | help take-back |
| FM-B6 | foreman | the chat | Obeys only "stop" and "hold"; a refused command goes to the Chief of Staff | foreman.md:59-184 | a | card never 5 | grep 'hold' foreman.md |
| FM-B7a | foreman | always | Never code, review, commit, rebase, push, edit a PR, create a worktree | foreman.md:59-184 | a | card never 3 | grep 'Code' foreman.md |
| FM-B7b | foreman | a dropped CR | Close or draft its PR | foreman.md:59-184 | a | card never 3; `drop` | help drop |
| FM-B7c | foreman | kept worktrees | Remove once the Driver has ended; a trashed or moved CR's worktree stays | foreman.md:59-184 | a | card never 6; `cleanup` | help cleanup |
| FM-B7d | foreman | the main checkout | The fast-forward is its only move | foreman.md:59-184 | a | card never 3; `main-checkout` | help main-checkout |
| FM-B7e | foreman | the early conflict check | `git merge-tree` only | foreman.md:59-184 | a | `chantier conflicts` runs it; `conflict-check` | help conflict-check |
| FM-B7f | foreman | a refused force push or rebase | The push after the check | foreman.md:59-184 | a | card never 3; `refused-push` steering readings | help refused-push |

## Protecting rows and their homes

FM-001 card; FM-004 card; FM-005 card; FM-008 card/orders; FM-009 card never 6; FM-011 qa-order; FM-012 chain; FM-020 refusal `check_shape`; FM-023 stack-grows; FM-024 stack-deliver; FM-025 stack-run; FM-026 stack-drop; FM-027 stack-checks; FM-028 stack-merge; FM-030 merge; FM-031 card never 3, 4; FM-032 card never 1; FM-033 card Messages; FM-040 hold; FM-041 park; FM-043 lost-driver; FM-044 lost-context; FM-046 conflict-check; FM-047 card never 1; FM-050 card never 3; FM-051 refused-push-judgement; FM-052 refused-push-route; FM-053 refused-answer; FM-054 refused-rebase; FM-055 lease-steering and card never 6; FM-B1a, B1c to B1f, B1h to B1j, B1l to B1p, B2, B5a to B5c, B6, B7a to B7f: card never 1 to 7, floor, or a refusal as the row says.

## Inferable rows

FM-003 (the commands print `next:`); FM-002, FM-021, FM-022, FM-048, FM-B1b, B1g, B1k, B2b, B3, B4, B5d (a `next:` or `judge` line carries them, or the rule disappears).

## Check candidates for child 25

- Chat obeys only "stop" and "hold" (FM-B6).
- A note does not wake (FM-007, `wakes`).
- `judge` then send, no merge (FM-004, FM-B1a).
- The `--no-gate` check (FM-B1h).
- A release is not merged without the grant (FM-B1o).
- A refused push of a non-`chantier/*` branch is never pushed (FM-050).
- A session in a worktree.
- `next` against a refusal (FM-B3).

## For child 24: the stack line (no CLI change in this round)

Section 7's text for the stack line:

`shape: stack: read `$CHANTIER help stack` now and after each compaction`

Child 24 changes `src/stack_shape.py`, `shape_line()`, and converts these tests: `test_came_back.py`, `test_stack_shape.py`, `test_reload_rules.py`, `test_role_cards_split.py`, `test_startup_manifest.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`, `test_release_tag.py` and `moved_rules.tsv`.
