## Summary

The role cards and prompts are far too heavy. This PR writes the next set of small cards, with their
rare parts moved to help topics: the Foreman, the Chief of Staff, the Griller, the shared files, the
host files and the four `SKILL.md` texts. Everything is under `skills/chantier/cards-next/`, which
nothing loads until the later swap. The base is `main`.

## Deliverables

| Area | Added under `skills/chantier/cards-next/` |
| --- | --- |
| Foreman | `foreman.md`, its topics |
| Chief of Staff, Griller | `chief-of-staff.md`, `griller-skill.md`, one sentence of `griller.md`, their topics, quiz cases under `evals/quiz/chief-of-staff/` |
| Shared | `concepts.md`, `pr-template.md`, `release-template.md`, `status-layout.md`, `routing.md`, `init.md`, `review-step.md`, `sync-checkout.md`, `ticket-summary-example.md`, `forges/` |
| Hosts | `hosts/claude-code.json` and `copilot.json` (byte copies), `hosts/claude-code.md` (allow rules), `topics/host-*.md` |
| Skills | `skills/{chantier,chief-of-staff,griller,status}-SKILL.md` |
| Index | `topics.json`: 234 topics |

Choices made: the cards "settle alone" four refused-forge routes and ask first for the rest; direct mode
reads the Foreman card through `brief foreman --epoch <n>` (no CLI change); a rule that protects the
user or the repository stays in the floor, a card or a refusal.

Sizes (LF bytes), shared and host files, today's against new:

| File | Today | New | Target |
| --- | ---: | ---: | --- |
| concepts.md | 73,286 | 18,394 | none set |
| pr-template.md | 16,801 | 11,849 | none set |
| release-template.md | 12,155 | 6,758 | none set |
| status-layout.md | 17,475 | 10,992 | none set |
| titles.md (now `topics/titles.md`) | 2,684 | 1,428 | 1,500, within |
| ticket-summary-example.md | 1,422 | 1,308 | none set |
| routing.md | 5,016 | 4,790 | none set |
| init.md | 10,041 | 6,171 | none set |
| review-step.md | 3,950 | 1,385 | 1,500, within |
| sync-checkout.md | 4,801 | 1,115 | 1,500, within |
| forges/github.md, gitlab.md | 739, 744 | 587, 590 | not larger, within |
| hosts/claude-code.json, copilot.json | 25,243, 22,372 | same | byte-identical |
| hosts/claude-code.md | 109,857 | 23,160 | allow rules only, none set |
| hosts/copilot.md | 18,947 | none (topics) | none set |
| floor.md | 554 | 554 | 1,200, within, byte-identical |
| topics/host-*.md (33 files) | part of the above | 36,066, largest 1,490 | 1,500 each, within |
| skills: chantier, chief-of-staff, griller, status | 3,537, 3,664, 3,223, 3,644 | 2,650, 2,730, 2,292, 2,729 | none set |

Role cards of this PR against their budgets: `foreman.md` 36,927 to 3,999 (4,000);
`chief-of-staff.md` 32,067 to 5,999 (6,000); `griller-skill.md` 3,497 (4,000); `griller.md` 10,757 to
1,925 (2,000). Cards over budget are in Known gaps.

`brief <role>` bytes, Claude Code, today's cards against `--cards skills/chantier/cards-next`:

| Role | Today | New |
| --- | ---: | ---: |
| coder | 9,595 | 6,519 |
| conflict-resolver | 8,879 | 6,480 |
| debugger | 8,668 | 6,267 |
| inspector | 11,030 | 6,985 |
| investigator | 8,540 | 6,472 |
| verifier | 19,567 | 8,098 |
| retro-critic | 4,225 | 2,889 |
| demo-explorer | 4,746 | 2,936 |
| chief-of-staff | 22,322 | 24,657 |
| griller | 6,349 | 6,623 |
| foreman | 55,206 | 22,278 |
| cr-driver, staged card, role only | 59,216 | 7,840 |
| release-driver, staged card, role only | 59,216 | 8,020 |
| stack-driver, staged card, role only | 59,216 | 7,875 |
| qa-driver, staged card, role only | 59,216 | 5,828 |
| spec-writer, on an inbox item | 4,815 | 3,228 |
| spec-critic, on an inbox item | 5,290 | 3,133 |
| board-griller, on an inbox item | 11,964 | 3,132 |

The two new briefs that grow hold the whole new card, where today's holds a short `SKILL.md` that
sends the session to more readings.

## Blast radius

Nothing loads `cards-next/`; a plain `git revert` removes it.

Grade: 1

## Autonomous decisions

- "Retry once only on a transient network error" is dropped: a launcher failure is a stop.
- The startup report sentence, "read every manifest reading before an action" and the review step's
  "cd into the worktree" are dropped as given by the commands and the brief.
- "Never tell unproved behaviour as fact" is filed as host-trial bookkeeping, with the proof files.
- Lines were added to cards and topics of earlier families: rules whose home must be a card, one link
  fix or more, and pointers to `help session-shell` and `help cr-review-step` (which go beyond the
  two permitted reasons; they keep the folder-change ban and the review step's brief reachable). Each,
  with its line:

| File and line (under `cards-next/`) | Change |
| --- | --- |
| chief-of-staff.md 13, 14, 16, 17, 27 | writes on the user's yes; never stop a process by name or PID; `cancel` only after an ordered drop; its own push is asked first; no CR work in a temp folder, no secret in a CR folder |
| chief-of-staff.md 41 | pointers to new topics |
| coder.md 13, conflict-resolver.md 15, debugger.md 13, demo-explorer.md 13, investigator.md 16, verifier.md 18, cr-driver.md 18 | the same temp-folder and secrets never |
| cr-driver.md 20 | never start an agent in place of one that may still run |
| cr-driver.md 26, qa-driver.md 18, release-driver.md 25, stack-driver.md 27, spec-writer.md 15, retro-critic.md 22-23, spec-critic.md 18-19 | pointers |
| qa-driver.md 10, 13; release-driver.md 14, 18, 19; stack-driver.md 18-20; spec-writer.md 11 | never touch an issue, never publish private data, the temp-folder never, one agent at a time |
| release-driver.md 7 | an image upload is irreversible; published notes use the reviewed text or stay a draft |
| griller-skill.md 24, 31; griller.md 7 | the temp-folder never, a pointer, no secret in the CR folder |
| topics: cr-rounds 4, refused-push-chief-p1 3 and 6, release-notes 4, ticket-summary-p2 5, titles 4, worker-shell 8 | pointer, scoping, links, a folded rule, the folder-change ban |

## Known gaps

- Do not merge: this merges with children 19 to 28 of the program as one unit, after child 28's
  campaign.
- No real run (child 28). Every Copilot claim is untested.
- `just quiz` was not run: no score exists for the new cards. It is owed for chief-of-staff, coder,
  conflict-resolver, cr-driver, debugger, demo-explorer, foreman, griller, release-driver,
  stack-driver and verifier; the new push and ask-first cases need at least 1 of 3. Four planned cases
  are not written, as they have no rule id the loader accepts (`a8-ask-settings-json`,
  `tracker-approval`, `direct-brief-foreman`, `griller-tracker-never`).
- `brief` for all 18 roles is not met: 11 of 18 exit 0 with `--cards`. The four Drivers are refused
  because `roles.yaml` names `driver.md`, which the new set does not hold (it must change at the swap;
  the sizes above use a staged copy). spec-writer, spec-critic and board-griller are refused on a CR
  folder of a running batch, as today's cards are (the sizes above use an inbox item).
- Cards over budget (only the owner raises a budget): coder 1,533 (+33), demo-explorer 1,612 (+112),
  retro-critic 1,565 (+65), spec-critic 1,572 (+72), spec-writer 1,667 (+167), verifier 3,112 (+112),
  release-driver 3,759 (+687). The first six were within before the shared-files pass.
- 24 topics over 1,500 bytes, all from the base: ci-beside-gate 2,052, ci 1,589, closing 1,888,
  conflicts 2,238, cr-handback 1,506, cr-rounds 2,061, cr-ship 2,413, cr-workers 1,624, handback-other
  2,030, pr-extras 1,898, pr-images 1,882, refused-push 1,544, release-merged 2,845, release-notes
  2,063, release-ship 2,306, retake-notes 1,871, retake-stack 1,818, retake 2,328, stack-changes 2,354,
  stack-hold 2,232, stack-make 1,742, stack-restack 1,832, trouble-remote 1,582, trouble-worker 2,173.
- The Chief of Staff's "Never" list has 13 items against a cap of about 5. Two are not in the planned
  list: "widen a grant, or approve an irreversible action, without the user's own word" and "state a
  past fact in a brief without its source".
- No byte target is set for `concepts.md`, `pr-template.md`, `release-template.md`,
  `status-layout.md`, `routing.md` and `init.md`: the owner may set one before budgets are frozen.
- The router skill runs no brief: it asks the role or behaves as the Chief of Staff.
- To confirm: a branch that is not a CR's own is pushed only once on a yes, and the default branch and
  its force push never.
- The inventories' homes were matched by script, not read row by row; rows with protecting wording
  that a topic carries are listed for the later review.
- The allow-rules table still lists the `uvx` and `uv run` rules; the launcher's rule is stated apart,
  marked unproved (untested on Copilot).
- The byte-identical host JSON still names `session-start.md`, `driver.md` and
  `foreman-lost-driver.md`; `topics/reload.md` still says to read the card again after a compaction.
- `release-template.md`, `routing.md`, `hosts/claude-code.md` and `griller-skill.md` are named without
  a link; `init.md` links `../assets/tour.html`, which resolves only after the swap.
- The Foreman's card says only "Stop no sync holder"; the `sync` topic holds the rest. A worktree
  override of the Foreman's old card is dropped, and the image-note rule depends on the hand-back's
  gaps being copied: both for the later review.
- For the swap (child 24): set `roles.yaml`'s card for chief-of-staff (`chief-of-staff.md`), griller
  (`griller-skill.md`) and the four Drivers, and the Driver table's card cell; copy
  `cards-next/skills/<skill>-SKILL.md` to `skills/<skill>/SKILL.md` and check its
  `chantier-version:` line; add the launcher's allow row with its preflight sample and drop
  "unproved"; write the stories the inventory files as incidents.

<details>
<summary>Details</summary>

## Changes

- Files under `skills/chantier/cards-next/` and `evals/quiz/chief-of-staff/` only.
- `topics.json`: every base help name is present, none renamed; every reading resolves; every role is
  in `roles.yaml`.
- Topics marked `review_by: "0.16.0"` (37), with the reason:
  - from the base, rare procedures of workers and Drivers: worker-shell, verifier-scratch,
    verifier-description, verifier-review-box, verifier-delta-matrix, verifier-before-after,
    verifier-images, inspector-audit, spec-writer-extras, trouble-gate, trouble-git, pr-gitlab, matrix;
  - Foreman, rare incidents or switches: lost-outside, mode-switch, handover, writer-off;
  - Chief of Staff and Griller, tied to a host, forge or capability that may settle, or rare:
    grill-outside-pr, remote-login, allow-rules-more, compacting, refused-forge-chain,
    batch-close-stopped, recovery, seat-handover, demo, pr-template-own;
  - shared and host, rare incident or host procedure with no CLI trigger: session-shell,
    host-auto-mode-trials, host-sessions-more, host-remote, host-foreman-worktree,
    host-reuse-foreman, host-for-you-sessions, host-auto-fix, init-checks, init-tools.
- All topic names: allow-rules, allow-rules-more, asks, batch-close, batch-close-stopped, batch-end,
  batch-pause, batch-plan, batch-plan-cut, batch-plan-mode, batch-plan-show, batch-start, board,
  board-lines, board-restart, chain, chain-conflict, checkpoints, ci, ci-beside-gate, ci-no-check,
  cleanup, closing, compacting, config, conflict-check, conflicts, conflicts-early-push,
  conflicts-local-gate, cost, cr-handback, cr-prompt, cr-proof, cr-review-step, cr-rounds, cr-ship,
  cr-workers, delivery-time, demo, direct, direct-mode, direct-mode-accept, direct-mode-epoch,
  driver-question, drop, escalation, first-turn, foreman-start, foreman-start-more, forge-permissions,
  forge-permissions-gitlab, forge-permissions-say, grill, grill-backlog, grill-critic,
  grill-critic-steps, grill-options, grill-outside-pr, grill-restate, grill-series, grill-specify,
  grill-surface, griller-cost, griller-worktree, handback-gate-draft, handback-other, handback-refused,
  handover, hold, host-allow-add, host-allow-add-lines, host-allow-broad, host-allow-extra,
  host-allow-not-add, host-allow-rules, host-auto-fix, host-auto-mode, host-auto-mode-steering,
  host-auto-mode-trials, host-compact, host-configuration, host-driver-silence, host-for-you,
  host-for-you-sessions, host-foreman-worktree, host-heartbeat, host-refused, host-remote,
  host-reuse-foreman, host-sessions, host-sessions-more, host-subagent-signs, host-surfaces,
  host-turn-end, host-write-guard, host-write-guard-shell, init-checks, init-tools, inspector-audit,
  lease, local-gate, long-gate, long-gate-waiver, lost-context, lost-driver, lost-outside,
  lost-restart, lost-silent, main-checkout, matrix, merge, merge-gaps, merge-github, merge-recorded,
  merge-series-stack, merge-stack-gitlab, merge-stack-ready, merge-under-grant, merge-words,
  mode-switch, options, orders, orders-queue, park, park-back, pr-extras, pr-gitlab, pr-images,
  pr-template-own, project-rules, qa-order, qa-results, ready-to-merge, recovery, refusals-to-say,
  refusals-to-say-more, refused-answer, refused-forge-chain, refused-push, refused-push-answer,
  refused-push-chief, refused-push-chief-more, refused-push-gate, refused-push-judgement,
  refused-push-route, refused-push-run, refused-rebase, refused-rebase-chief, refused-rebase-run,
  release, release-chief, release-chief-after, release-chief-approve, release-chief-auto, release-end,
  release-evidence, release-merged, release-notes, release-procedure, release-ship, release-stale,
  release-tag, release-take, reload, remote-login, restart, retake, retake-notes, retake-stack, retro,
  retro-critic, retro-critic-write, retro-lines, retro-route, retro-route-chantier, rounds-exception,
  seat, seat-handover, session-shell, session-start, session-start-surface, spec-writer-extras, stack,
  stack-asks, stack-changes, stack-changes-chief, stack-checks, stack-deliver, stack-drop, stack-ends,
  stack-gate, stack-grows, stack-hold, stack-joins, stack-make, stack-merge, stack-outside,
  stack-record, stack-restack, stack-run, stack-takes, status-notes, status-notes-more, steering,
  steering-messages, steering-reports, sync, sync-offer, take-back, ticket-summary,
  ticket-summary-post, titles, trials, trouble, trouble-gate, trouble-git, trouble-remote,
  trouble-worker, verifier-before-after, verifier-delta-matrix, verifier-description, verifier-images,
  verifier-review-box, verifier-scratch, wakes, wakes-forge, watcher, watcher-board, watcher-events,
  watcher-lines, watcher-pull, where-cr-goes, worker-shell, writer, writer-off.

## Human decisions

- The cards become the smallest possible, with no behaviour lost and progressive disclosure used to
  the full.
- One total rewrite in one pass, then a read-and-compare review; one card set, with no switch.
- A rare incident rule with no CLI trigger becomes a help topic for one release.

## Impacts

No visual change; nothing loads the new files.

## Test plan

- [ ] No behaviour change: no test added or changed
- [ ] Local gates at the head: `just check`
- [ ] Evidence: byte copies, links, topic index, Driver table, unloaded check
- [ ] Review
- [ ] Verified
- [ ] CI green

## Internal references

- CR-507 `sc21-cards-foreman`, with the SC22 and SC23 specifications in the same file.
- The work folder holds the four rule inventories (Foreman, Chief of Staff, Griller, host and shared,
  with the completeness table) and the proofs.

</details>
