## Summary

The role cards and prompts are far too heavy. This PR writes the next set of small cards, with their
rare parts moved to help topics: the Foreman, the Chief of Staff, the Griller, the shared files, the
host files and the four `SKILL.md` texts. Everything the new set holds is under `skills/chantier/cards-next/`, which nothing loads until the
later swap. The only files outside it are nine added quiz cases,
`evals/quiz/chief-of-staff/a8-*.json`: `a8-ask-delete`, `a8-ask-release`, `a8-ask-stop-process`,
`a8-chained-subcommand-refused`, `a8-gh-pr-edit-base-refused`, `a8-gh-pr-ready-refused`,
`a8-push-refused-cr-branch`, `a8-push-refused-default-branch` and `a8-rebase-refused-cr-branch`.
The base is `main`.

## Deliverables

| Area | Added under `skills/chantier/cards-next/` |
| --- | --- |
| Foreman | `foreman.md`, its topics |
| Chief of Staff, Griller | `chief-of-staff.md`, `griller-skill.md`, one sentence of `griller.md`, their topics, quiz cases under `evals/quiz/chief-of-staff/` |
| Shared | `concepts.md`, `pr-template.md`, `release-template.md`, `status-layout.md`, `routing.md`, `init.md`, `review-step.md`, `sync-checkout.md`, `ticket-summary-example.md`, `forges/` |
| Hosts | `hosts/claude-code.json` and `copilot.json` (byte copies), `hosts/claude-code.md` (allow rules), `topics/host-*.md` |
| Skills | `skills/{chantier,chief-of-staff,griller,status}-SKILL.md` |
| Index | `topics.json`: 240 topics |

Choices made: the cards "settle alone" four refused-forge routes and ask first for the rest; direct mode
reads the Foreman card through `brief foreman --epoch <n>` (no CLI change); a rule that protects the
user or the repository stays in the floor, a card or a refusal.

Sizes (LF bytes), shared and host files, today's against new:

| File | Today | New | Target |
| --- | ---: | ---: | --- |
| concepts.md | 73,286 | 26,100 | none set |
| pr-template.md | 16,801 | 12,032 | none set |
| release-template.md | 12,155 | 7,002 | none set |
| status-layout.md | 17,475 | 11,486 | none set |
| titles.md (now `topics/titles.md`) | 2,684 | 1,495 | 1,500, within |
| ticket-summary-example.md | 1,422 | 1,308 | none set |
| routing.md | 5,016 | 4,790 | none set |
| init.md | 10,041 | 6,171 | none set |
| review-step.md | 3,950 | 1,497 | 1,500, within |
| sync-checkout.md | 4,801 | 1,202 | 1,500, within |
| forges/github.md, gitlab.md | 739, 744 | 592, 595 | not larger, within |
| hosts/claude-code.json, copilot.json | 25,243, 22,372 | same | byte-identical |
| hosts/claude-code.md | 109,857 | 23,319 | allow rules only, none set |
| hosts/copilot.md | 18,947 | none (topics) | none set |
| floor.md | 554 | 554 | 1,200, within, byte-identical |
| topics/host-*.md (33 files) | part of the above | 37,088, largest 1,500 | 1,500 each, within |
| skills: chantier, chief-of-staff, griller, status | 3,537, 3,664, 3,223, 3,644 | 2,705, 2,785, 2,347, 2,784 | none set |

Role cards of this PR against their budgets: `foreman.md` 36,927 to 3,997 (4,000);
`chief-of-staff.md` 32,067 to 5,999 (6,000); `griller-skill.md` 3,621 (4,000); `griller.md` 10,757 to
1,925 (2,000). `cr-driver.md` 3,749 and
`stack-driver.md` 3,783 (4,096). Cards over budget are in Known gaps.

`brief <role>` bytes, Claude Code, today's cards against `--cards skills/chantier/cards-next`:

| Role | Today | New |
| --- | ---: | ---: |
| coder | 9,575 | 6,569 |
| conflict-resolver | 8,859 | 6,460 |
| debugger | 8,648 | 6,247 |
| inspector | 11,010 | 6,966 |
| investigator | 8,520 | 6,452 |
| verifier | 19,547 | 8,078 |
| retro-critic | 4,225 | 2,889 |
| demo-explorer | 4,746 | 2,936 |
| chief-of-staff | 22,322 | 24,657 |
| griller | 6,349 | 6,747 |
| foreman | 55,206 | 22,276 |
| cr-driver, staged card, role only | 59,216 | 8,010 |
| release-driver, staged card, role only | 59,216 | 8,070 |
| stack-driver, staged card, role only | 59,216 | 8,044 |
| qa-driver, staged card, role only | 59,216 | 5,828 |
| spec-writer, on an inbox item | 4,815 | 3,228 |
| spec-critic, on an inbox item | 5,290 | 3,133 |
| board-griller, on an inbox item | 11,964 | 3,132 |
| direct mode: chief-of-staff, then `foreman --epoch 1` | 77,528 | 46,933 |

Host claude, no unit but where a row says otherwise. Every row was measured in one run on the cards of
this PR's last commit. A unit's brief also holds the unit's facts from the record, so the six workers'
bytes, measured on this change's unit, move between measurements on both sides (today's coder brief:
9,575 here, 9,790 and 9,116 in earlier measurements). Start readings before this change, as the specification gives
them (declared / measured): Foreman 91 / 144 KB, Chief of Staff 202 / 218 KB, Griller 145 / 36 KB.

The two new briefs that grow hold the whole new card, where today's holds a short `SKILL.md` that
sends the session to more readings.

## Blast radius

Nothing loads `cards-next/`; a plain `git revert` removes it.

Grade: 1

## Autonomous decisions

- "Retry once only on a transient network error" is dropped: a launcher failure is a stop.
- Five questions took a default without the owner, each to confirm by the owner: the override of a
  Foreman's worktree stop by the user's words in its chat is dropped (only stop and hold remain); a
  branch that is not the CR's own is never force-pushed, the default branch is never pushed, and any
  other push is asked first and run once on the yes; direct mode runs the separate
  `brief foreman --epoch <n>`, with no CLI change; the later budget freeze takes the sizes this
  change reaches; the router skill runs no brief of its own and has no router card.
- The startup report sentence, "read every manifest reading before an action" and the review step's
  "cd into the worktree" are dropped as given by the commands and the brief.
- "Never tell unproved behaviour as fact" is filed as host-trial bookkeeping, with the proof files;
  the Chief of Staff's card also holds it ("or as fact what the host marks unproved"). The Foreman
  card's two notes that a Copilot path is unproved (B012, B017) are dropped as bookkeeping.
- Lines were added to cards and topics of earlier families: rules whose home must be a card, one link
  fix or more, and pointers to `help session-shell` and `help cr-review-step` (which go beyond the
  two permitted reasons; they keep the folder-change ban and the review step's brief reachable). Topic
  lines were also edited where the new set had lost or misstated a rule of today's cards, or held a date,
  CR id or trial story the specification bans (the topic
  row marked "rules put back" below), which goes beyond them too. Each, with its line:

| File and line (under `cards-next/`) | Change |
| --- | --- |
| chief-of-staff.md 13, 14, 16, 24, 27, 29 | writes on the user's yes; stopping a Foreman or a process the session did not start, its own board or watcher too, only on a yes, never by name, pattern or PID; `cancel` only after an ordered drop; no tracker text naming a CR, batch, role or cost; CR work never in a scratchpad, temp or host-settings folder, nor only in chat or memory, no secret or personal data in a CR folder; never tell as fact what the host marks unproved |
| chief-of-staff.md 10, 17, 22, 23 | the push rail covers a protected branch too; the ask-first push is the session's own; never message or stop a Driver in Foreman mode; never edit `summary.json` by hand |
| chief-of-staff.md 26 | `abandon` and `restore` only on the user's word, with priority, labels and groups (for the later review) |
| chief-of-staff.md 3, 10, 16, 20, 31, 32, 39, 41 | wording trims for the 6,000 budget; pointers to new topics; on `init` or "I am new here", run `$CHANTIER init` and give the tour of `init.md` |
| griller-skill.md 5, 24, 29, 31; griller.md 7 | the CR-work never (scratchpad, temp or host-settings folder, or only chat or memory), a pointer, no secret in the CR folder; `depends.json` only when a CR needs another's result; no `triage` for a CR marked for the running batch |
| foreman.md 13, 14, 15, 16 | `gate --first` only for a critical-path CR or the user's next merge, not on a Driver's say; never switch the mode; an image note goes in the ask's added sentence, the one sentence it may add; other asks: `help ask-lines`; stop stray background tasks by id, none outlives the heartbeat, a refusal rules over `next` |
| foreman.md 20, 21 | a granted merge takes the judged head only, no open PR below, reread before a retry; never drop a hand-back; a local run is owed at that head and a waiver must name it; an absent gate never means success (`help long-gate`) |
| foreman.md 22 | the fast-forward is `--no-overwrite-ignore`, of a clean main checkout; a Driver's refused push or rebase checked (`help refused-push`, a push judged too); no failed or protected push retried, no branch protection read; no comment on a dropped CR's PR, its branch kept; stop no sync holder |
| foreman.md 25, 27, 29 | a Driver is replaced only by `help lost-restart`, never on silence alone; the CR-work, secrets and personal-data never; a past fact with no source is said unknown |
| foreman.md 38 | Rare: only `$CHANTIER help --for foreman`; the topic names are cut (`long-gate` and `refused-push` are named at never 2 and 3) |
| foreman.md 3, 6-10, 17, 24, 26, 31 | wording trims for the 4,000 budget |
| cr-driver.md 5 and 16, stack-driver.md 5 and 16, release-driver.md 16 | fresh workers per round or move, and the checker never wrote the change (line 5); no rebase with `--rebase-merges`, `--exec` or `-x` (line 16) |
| inspector.md 5, 22 | a check red on the default branch is reported, never fixed there; the `worker-shell` pointer shortened |
| coder.md 13, conflict-resolver.md 15, debugger.md 13, demo-explorer.md 13, investigator.md 16, verifier.md 18, cr-driver.md 18 | the same temp-folder and secrets never; `coder.md` also large binaries other than the retained prototype |
| cr-driver.md 20 | never start an agent in place of one that may still run |
| cr-driver.md 26, qa-driver.md 18, release-driver.md 25, stack-driver.md 27, spec-writer.md 15, retro-critic.md 22-23, spec-critic.md 18-19 | pointers |
| qa-driver.md 10, 13; release-driver.md 14, 18, 19; stack-driver.md 18-20; spec-writer.md 11 | never touch an issue, never publish private data, the temp-folder never, one agent at a time |
| release-driver.md 7 | an image upload is irreversible; published notes use the reviewed text or stay a draft |
| topics: cr-rounds 4, refused-push-chief-p1 3 and 6, release-notes 4, ticket-summary-p2 7, titles 4, worker-shell 9 | pointer, scoping, links, a folded rule, the folder-change ban |
| topics, rules put back: allow-rules 4, allow-rules-more-p1 3, allow-rules-more-p2 3, batch-close-p1 3, batch-close-p2 3 and 4, batch-close-stopped-p2 5, batch-pause 3 and 5, batch-plan 3 and 4, batch-plan-cut-p1 1, 3 and 4, batch-plan-cut-p2 1, 3 and 4, batch-plan-mode-p1 1, 3 and 4, batch-plan-mode-p2 1, 3, 4 and 5, batch-plan-mode-p3 1, 3, 4 and 5, batch-plan-show-p1 1 and 3, batch-plan-show-p2 1, board-lines 4, board-p1 3, board-p2 3 and 4, board-restart 3 and 7, chain 4 and 5, chain-conflict 4, compacting-p2 3, config-p1 1 and 3, config-p2 1, 3 and 4, config-p3 1, 3, 4 and 5, conflict-check 5, delivery-time-p2 3 and 6, demo-p1 3 and 5, direct-mode-accept-p1 3, direct-mode-accept-p2 4, direct-mode-epoch-p1 3, direct-mode-p2 3, direct-mode-p3 4, drop 4, first-turn-p1 5, first-turn-p2 3, 4, 5 and 6, foreman-start-more 4, foreman-start-p1 3, foreman-start-p2 3, forge-permissions-gitlab 3 and 5, forge-permissions-p1 1, 3, 4, 5, 6 and 8, forge-permissions-p2 1, 3 and 4, forge-permissions-say 3, grill-backlog-p1 3, 5 and 6, grill-backlog-p2 3 and 4, grill-critic 3 and 4, grill-critic-steps 5, 6 and 7, grill-options 3, grill-outside-pr 4, 5 and 7, grill-series 4, 7, 8 and 9, grill-specify-p1 5 and 7, grill-specify-p2 4, griller-worktree 3 and 5, lease 3 and 7, lease-steering 4, 5, 6, 7 and 8, long-gate 3 and 7, long-gate-waiver 4 and 5, lost-driver 8, lost-outside 3, 5 and 7, lost-silent 6, main-checkout-p1 1 and 3, main-checkout-p2 1, 3, 4, 6, 8 and 9, merge-gaps-p1 1, 3, 4, 5 and 6, merge-gaps-p2 1, 3, 4, 5, 6 and 7, merge-recorded 5, 6 and 7, merge-series-stack-p1 5, merge-series-stack-p2 3, merge-stack-gitlab 3, merge-stack-ready-p1 3, merge-stack-ready-p2 3 and 6, merge-under-grant 3 and 7, merge-words-p1 1, 3 and 4, merge-words-p2 1, 3 and 4, mode-switch-p1 1, 3, 5, 7 and 8, mode-switch-p2 1, 3, 4, 5 and 6, options 5, orders 8, orders-queue 3 and 4, pr-extras 3, 4, 5, 8 and 9, pr-gitlab 3 and 4, project-rules-p1 1, 3, 5 and 6, project-rules-p2 1, 3 and 4, recovery 6, refusals-to-say-more 3, refusals-to-say-p1 3 and 6, refused-push-chief-p2 3, refused-push-gate 3, 4, 5 and 6, refused-push-route 4, refused-push-run 4, refused-push-steering 3, 4, 6 and 7, refused-rebase 5, release-chief-after-p1 3, release-chief-after-p2 4 and 5, release-chief-auto-p1 3, release-chief-p1 3, release-chief-p2 4, release-notes 3, 5, 6 and 8, release-take 4 and 6, reload 3, remote-login 3, retro 3, retro-critic 4 and 5, retro-route-chantier-p1 6, retro-route-p2 4, rounds-exception 3, seat-handover 5, seat-p1 4, seat-p2 3, 6 and 7, session-start 3 and 4, session-start-surface-p2 3, stack 5 and 6, stack-changes-chief-p1 3 and 4, stack-changes-chief-p2 3, stack-checks 6, stack-deliver 3, stack-ends 5, stack-grows 4, stack-outside 4 and 5, stack-run 3, stack-takes 4, steering-reports-p1 4 and 6, steering-reports-p2 3 and 4, take-back 3, 4, 5 and 7, ticket-summary-p1 5, 6 and 7, ticket-summary-p2 3, 4 and 5, ticket-summary-post-p1 4, 7 and 8, ticket-summary-post-p2 3, 4 and 5, titles 7 and 8, trials-p1 1, 3 and 4, trials-p2 1, trouble-gate 6, wakes-forge 6, wakes-p1 1, 3, 4, 5 and 6, wakes-p2 1, 3 and 4, watcher 4 and 6, watcher-board-p1 1, 5 and 6, watcher-board-p2 1 and 3, watcher-events-p1 1, 3 and 4, watcher-events-p2 1, 3, 4, 5, 6 and 7, watcher-lines-p1 1 and 4, watcher-lines-p2 1 and 5, watcher-pull 6, worker-shell 8 and 14, writer 3 | a lost or misstated rule or its wording, a date, CR id or trial story the specification bans, or a split file's lines; each rule's home and line are in the four inventories |
| topics.json | the new topics indexed; `sync` also reads `sync-checkout.md`; `direct-mode` also reads the files of `direct-mode-switch`; `mode-switch`'s trigger names `order mode`; the split topics list their parts; `ready-asks` and `ask-lines` serve the Foreman and the Chief of Staff |

## Known gaps

- `foreman.md` has eight nevers where the specification sets seven: the eighth (CR work in a scratchpad or
  temp folder; a secret or personal data in a CR folder) protects the user, and F5 puts such a rule on a
  card, in the floor or in a refusal.
- The rule that repository text is in English is filed under `worker-shell` (`topics.json`), whose roles
  hold no Driver and no Foreman; for those, only `pr-template.md` says it, for the PR.
- Do not merge on its own: this merges with the rest of the card rewrite program as one unit, after
  the program's evaluation campaign.
- No real run: it belongs to that campaign. Every Copilot claim is untested.
- `just quiz` was not run: no score exists for the new cards. It is owed for chief-of-staff, coder,
  conflict-resolver, cr-driver, debugger, demo-explorer, foreman, griller, release-driver,
  stack-driver and verifier; the new push and ask-first cases need at least 1 of 3. Four planned cases
  are not written, as they have no rule id the loader accepts (`a8-ask-settings-json`,
  `tracker-approval`, `direct-brief-foreman`, `griller-tracker-never`).
  The changes edit the Foreman's, the Chief of Staff's, the Griller's and the Coder's cards, the shared files,
  the skill texts and many topics: their score is owed at the final head. Plans only, no spend (costs of an
  earlier version of the cards): chief-of-staff with griller 54 runs, about
  $25.34; foreman 33 runs, about $15.40; coder, conflict-resolver, debugger, demo-explorer and
  verifier 24 runs, about $8.51; the three Driver roles cannot be planned (`roles.yaml` names
  `driver.md`). The first two are above the default `--max-usd 10`.
- `brief` for all 18 roles is not met: 11 of 18 exit 0 with `--cards`. The four Drivers are refused
  because `roles.yaml` names `driver.md`, which the new set does not hold (it must change at the swap;
  the sizes above use a staged copy). spec-writer, spec-critic and board-griller are refused on a CR
  folder of a running batch, as today's cards are (the sizes above use an inbox item).
- Cards over budget (only the owner raises a budget): coder 1,603 (+103), demo-explorer 1,612 (+112),
  retro-critic 1,565 (+65), spec-critic 1,572 (+72), spec-writer 1,667 (+167), verifier 3,112 (+112),
  release-driver 3,809 (+737). The first six were within before the shared-files pass.
- 24 topics over 1,500 bytes, all from the base: ci-beside-gate 2,052, ci 1,589, closing 1,888,
  conflicts 2,238, cr-handback 1,506, cr-rounds 2,061, cr-ship 2,413, cr-workers 1,624, handback-other
  2,030, pr-extras 1,896, pr-images 1,882, refused-push 1,544, release-merged 2,845, release-notes
  2,055, release-ship 2,306, retake-notes 1,871, retake-stack 1,818, retake 2,328, stack-changes 2,354,
  stack-hold 2,232, stack-make 1,742, stack-restack 1,832, trouble-remote 1,582, trouble-worker 2,173.
- The Chief of Staff's "Never" list has 14 items against a cap of about 5. Three are not in the planned
  list: "widen a grant, or approve an irreversible action, without the user's own word", "state a
  past fact in a brief without its source" and the never on CR work in a temp folder and on secrets or
  personal data in a CR folder.
- No byte target is set for `concepts.md`, `pr-template.md`, `release-template.md`,
  `status-layout.md`, `routing.md` and `init.md`: the owner may set one before budgets are frozen.
- The router skill runs no brief: it asks the role or behaves as the Chief of Staff.
- To confirm: a branch that is not a CR's own is pushed only once on a yes, and the default branch and
  its force push never.
- "Never fix a check red on the default branch there" is stated in `inspector.md` only, not in
  `verifier.md` or the `ci` topic; no card names the forge's "Update branch" button (the `ship`
  refusal covers it).
- Inventory homes: of the 4,224 rows of the four inventories, 3,916 name a text home under `cards-next/`.
  A script compared each one's source sentences at the base with its home's words. At least 1,835 of
  them, every row it still flags included, were read by hand against the home, and the losses found were
  fixed. The other rows (at most 2,081) were not read by hand in that pass, and a lost condition worded
  with the home's own words can escape the script. Each of the four inventories lists the
  protecting-looking rows a topic carries, for the later review.
- Rules, or parts of rules, held by no card, floor or refusal: never rewrite an earlier retro section
  (FM-026); a held agent that has ended with no transcript is cleared on the user's word (C-304);
  another session's Driver is cleared only on the user's word that it does not run (C-885, part: the
  close refusal holds "if it is not running").
- The allow-rules table still lists the `uvx` and `uv run` rules; the launcher's rule is stated apart,
  marked unproved (untested on Copilot).
- The byte-identical host JSON still names `session-start.md`, `driver.md` and
  `foreman-lost-driver.md`; `topics/reload.md` still says to read the card again after a compaction.
- `release-template.md`, `routing.md`, `hosts/claude-code.md` and `griller-skill.md` are named without
  a link; `init.md`'s link to `../assets/tour.html`, outside `cards-next/`, resolves today and after the
  swap.
- The Foreman's card says only "Stop no sync holder"; the `sync` topic holds the rest.
- The override of a Foreman's worktree stop by the user's words in its chat is dropped (a default answer, to confirm by the owner), for the later review.
- `judge` does not carry the image note of a hand-back; the Foreman's card (line 15) puts it in the
  ask's added sentence.
- For the swap (a later change): set `roles.yaml`'s card for chief-of-staff (`chief-of-staff.md`), griller
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
- All topic names: allow-rules, allow-rules-more, ask-lines, asks, batch-close, batch-close-stopped, batch-end,
  batch-pause, batch-plan, batch-plan-cut, batch-plan-mode, batch-plan-show, batch-start, board,
  board-lines, board-restart, chain, chain-conflict, checkpoints, ci, ci-beside-gate, ci-no-check,
  cleanup, closing, compacting, config, conflict-check, conflicts, conflicts-early-push,
  conflicts-local-gate, cost, cr-handback, cr-prompt, cr-proof, cr-review-step, cr-rounds, cr-ship,
  cr-workers, delivery-time, demo, direct, direct-mode, direct-mode-accept, direct-mode-epoch, direct-mode-switch,
  driver-question, drop, escalation, first-turn, foreman-start, foreman-start-more, forge-permissions,
  forge-permissions-gitlab, forge-permissions-say, grill, grill-backlog, grill-critic,
  grill-critic-steps, grill-example, grill-options, grill-outside-pr, grill-restate, grill-series, grill-specify,
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
  mode-switch, options, order-drop, order-verbs, orders, orders-queue, park, park-back, pr-extras, pr-gitlab, pr-images,
  pr-template-own, project-rules, qa-order, qa-results, ready-asks, ready-to-merge, recovery, refusals-to-say,
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
  stack-record, stack-restack, stack-run, stack-takes, status-notes, steering,
  steering-messages, steering-reports, sync, sync-offer, take-back, ticket-summary,
  ticket-summary-post, titles, trials, trouble, trouble-gate, trouble-git, trouble-remote,
  trouble-worker, verifier-before-after, verifier-delta-matrix, verifier-description, verifier-images,
  verifier-review-box, verifier-scratch, wakes, wakes-forge, watcher, watcher-board, watcher-events,
  watcher-lines, watcher-pull, where-cr-goes, worker-shell, writer, writer-off.

## The user's boundaries: label to final home

The labels of the specification's section 4. Rows are `FM-` rows of `cards-inventory-foreman.md`. `card:N` is `cards-next/foreman.md:N`; `floor N` is `cards-next/floor.md:N+4`; a file with no folder named here is under the CLI's `src/chantier/`.

| label | protects | rows | final home | topic |
| --- | --- | --- | --- | --- |
| B1a | yes | B001, B003 | floor 1; card:20, card:15 (`judge` words the ask) | - |
| B1b | no | B002 | `judge` carries no icon: the rule disappears (card:15) | - |
| B1c | yes | B063 | refusals `check_shape`, `shape_refusal` (`rails_release.py:192`, `:178`); `judge` prints `no ask:` (`commands/judge.py:58`); card:15 | `stack` |
| B1d | yes | B004, B005 | card:15, card:21; `judge` appends the gaps (`status/judge_words.py:99`) | - |
| B1e | yes | B006 | floor 8; card:15. Known gap: `judge` does not carry an image note | - |
| B1f | yes | B007 | card:21 | `take-back` |
| B1g | no | B008 | topic only | `orders` |
| B1h | yes | B009, B010, B013 | card:21 (B013: topic) | `long-gate`, `local-gate` |
| B1i | yes | B011, B012, B014 | card:21 (B012: dropped, unproved bookkeeping; no host row holds it) | `local-gate` |
| B1j | yes | B015-B017, B019, B022 | card:21, card:15; `judge --local-gate` (`status/judge_words.py:33`); B017: dropped, unproved bookkeeping (no host row holds it), B022: topic | `local-gate` |
| B1k | no | B020, B021 | topic; card:21 points to it | `local-gate` |
| B1l | yes | B023 | card:21 | `long-gate` |
| B1m | yes | B024 | card:21 ("An absent gate never means success.") | `long-gate` |
| B1n | yes | B025-B032 | card:21, card:15; `judge --local-gate` (`status/judge_words.py:33`); B032: topic | `long-gate-waiver`, `local-gate` |
| B1o | yes | B033, B034 | floor 1, 6; card:20; refusal `release go`: "no grant for: …; the user merges it" (`commands/release.py:81`), "no approval for: …" (`:84`) | `merge-under-grant` |
| B1p | yes | B018, B035 | floor 1, 6; card:20, card:21; refusal `check_granted_fix` (`rails_release.py:108`) | `merge-under-grant`, `main-checkout` |
| B2 | yes | B036, B037 | refusals `check_slot`, `check_budget`, `check_round` (`rails.py:57`, `:222`, `:305`); floor 9 | - |
| B2b | no | B038 | topic only | `escalation` |
| B3 | no | B039 | none (inferable: the refusals name the next command) | - |
| B4 | no | B040-B042 | topic only | `orders` |
| B5a | yes | B043, B044 | card:14; floor 7; refusal "cannot pause <batch>: …" (`commands/closing.py:95`) | `orders` |
| B5b | yes | B045 | refusal "cancel <cr>: no destination recorded; …" (`commands/release.py:137`) | `orders` |
| B5c | yes | B046-B051 | card:29; refusal "<cr> is <status>: a Driver takes it back only with `--note` …" (`rails.py:249`); B047-B051: inferable or topic | `take-back` |
| B5d | no | B052 | topic only | `take-back` |
| B6 | yes | B053, B054 | card:24, with "stop" and "hold" only (the third case is dropped, answer 8) | - |
| B7a | yes | B055 | card:22 | - |
| B7b | yes (the named exception) | B056, B065 | card:22 | `drop` |
| B7c | yes | B057-B059 | card:22, card:25; floor 5; B057: topic | `cleanup` |
| B7d | yes | B060, B062 | card:22; floor 5 | `main-checkout` |
| B7e | yes | B061 | `chantier conflicts` runs the check (`commands/conflicts.py`); card:22 bounds the Foreman's git; floor 5 | `conflict-check` |
| B7f | yes | B064 | card:22 | `refused-push`, `refused-rebase` |

## Human decisions

- The cards become the smallest possible, with no behaviour lost and progressive disclosure used to
  the full.
- One total rewrite in one pass, then a read-and-compare review; one card set, with no switch.
- A rare incident rule with no CLI trigger becomes a help topic for one release.

## Impacts

No visual change; nothing loads the new files.

## Test plan

- [x] No behaviour change: no test added or changed
- [x] Local gates: `just check` on the tree of the last commit, run before the commit: 2933 passed, 19 skipped
- [x] Evidence on that tree:
  - byte copies: `git hash-object <path>` gives the same blob under `cards-next/` and `references/` for
    `floor.md` (`61da01e8`), `hosts/claude-code.json` (`3f2daf79`) and `hosts/copilot.json` (`b4dec473`);
  - unloaded: `git grep --untracked -n cards-next -- . ':(exclude)skills/chantier/cards-next'` prints no line,
    and `git grep --untracked -n "Read this short role contract at boot\|# chantier-agent:\|chantier board" --
    skills/chantier/cards-next` prints no line;
  - links under `cards-next/`: 22, broken 0, none into `references/`;
  - topic index: 240 topics load, 465 readings resolve, no base name missing;
  - Driver table: the parser reads 4 rows from the old and the new file, equal cell for cell
- [ ] Review: owed at the head (approved at `03f973e`, before the last changes)
- [ ] Verified
- [ ] CI green

## Internal references

- CR-507 `sc21-cards-foreman`, with the SC22 and SC23 specifications in the same file.
- The CR's `evidence/` folder holds the four rule inventories (Foreman, Chief of Staff, Griller, host
  and shared, with the completeness table), the proofs, the boundaries split
  (`boundaries-split.md`) and the acceptance records (`acceptance-records.md`: `just test` seconds at
  base and head, start readings beside the brief sizes, the `just quiz --plan` output, the
  `griller.md` diff and `git diff --stat`).
- For child 24 (specification section 7): `brief foreman` and `status --refresh` are to print, for a
  stack batch, `shape: stack: read `$CHANTIER help stack` now and after each compaction`. Child 24
  changes `src/stack_shape.py`'s `shape_line()`, which prints
  `rules: {skill_dir}/references/foreman-stack.md (reread after a compaction)`, a path the swap
  removes, and converts the tests that read the old Foreman cards: `test_came_back.py`,
  `test_stack_shape.py`, `test_reload_rules.py`, `test_role_cards_split.py`,
  `test_startup_manifest.py`, `test_stack_chain_cards.py`, `test_rebase_rules.py`,
  `test_release_tag.py` and `moved_rules.tsv`.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
