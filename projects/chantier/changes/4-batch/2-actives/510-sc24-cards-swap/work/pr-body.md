<!-- title: feat(cards)!: swap in the new role cards and remove the old set -->

## Summary

The plugin held two sets of role cards: the old one that every session loaded, and a new, smaller one staged beside it. This change makes the new set the only one: roles get their card, the shared floor rules and their facts from `chantier brief`, and the old cards, their startup core and their startup manifest are removed.

## Deliverables

One card set, and one way to start an agent.

| | Before (`88d9ab4`) | After |
| --- | --- | --- |
| Card sets | `references/` (loaded) and `cards-next/` (staged) | `references/` only |
| A role's start | startup core, manifest, role card sections | `brief <role> <unit>`: card, floor, facts, host rows |
| `take`, `take stack`, `order qa` | print a Driver prompt skeleton | print the lease and the `brief` command |
| `round`, `handoff` | print each worker's opening lines | print one `workers:` line naming `brief` |

```mermaid
flowchart LR
  S[steering session] -->|take| C[CLI]
  C -->|brief command| S
  S -->|brief| F[brief file: card, floor, facts, host rows]
  S -->|short prompt| D[Driver]
  D --> F
```

## Blast radius

Grade: 3. Every role's contract and the way every agent is started change at once. A rollback is a revert of this change together with the changes stacked with it.

## Autonomous decisions

- The launcher is not switched in the cards: they keep today's `$CHANTIER` paragraph and sync commands, because the launcher leaves the CLI running after its stop on Windows.
- `take` prints the `brief` command and only `brief` writes brief files (default taken without the owner, to be confirmed).
- The board Griller's fixed brief does not name the floor (default taken without the owner, to be confirmed).
- `brief` prints a `Note:` line, read from the `take` event or the QA order's note, so that a note given at `take` is not lost.
- `take` prints two lines that start with `brief:`: the command, and the fact about `brief`.
- `roles.yaml` `reply:` names a level-1 heading where a card holds its reply block under its title.
- The CLI's facts builder is split in two (a CR's facts, with the `workers:` line, and a worker's facts) instead of taking a flag.
- The board Griller's brief ends its card line once the host clause is gone; the unused host file lookup is removed.
- A configuration refusal names the host's row file; the access refusal cites the floor rule instead of a removed card.
- The hook's reload message says "through your skill's `$CHANTIER` command".
- The tests' file-and-heading pins are gathered in one test; the board read-key test now scans the topics too.

## Known gaps

- Do not merge alone: merges with the changes stacked below and above it as one unit, after the real-run campaign.
- Real run not done: it is the last change of the stack.
- Launcher not switched: it leaves the CLI running after its stop on Windows.
- The board Griller does not read the floor.
- Some new cards still describe output the CLI no longer prints (a worker's opening lines, the worker `writes:` line, the prompt skeleton of `take` and `order qa`): `topics/cr-workers.md`, `concepts.md` ("The prompt" and its template), `topics/trouble-worker.md`, `foreman.md`, `topics/direct-mode-p2.md`, `topics/direct-mode-switch-p4.md`, `topics/qa-order.md`, `topics/order-verbs-p1.md`. Card content was not rewritten here; these sentences must be fixed before a real batch runs on these cards.
- A worker's agent file refuses a prompt that names no path to its card (`coder.md`), while the short prompt of `brief` names `.../<unit>-coder.md`. Not tried with a real agent.
- The generic agent's contract heading still says "after the opening lines", though it is now in the worker's brief.
- Three data files kept byte-identical still hold removed file names: `hosts/claude-code.json` (`driver.md`, `session-start.md`) and `hosts/copilot.json` (`session-start.md`, `foreman-lost-driver.md`).
- Wording of the old set not found in the new one: some sentences of the sync offer, "A release with no PR yet is no anomaly", the Foreman's pointer to `help session-shell`; "say it once to the user as printed" became "offer the restart once".
- The eval kit, the scenario and the docs are not yet moved to the new set.
- The type checker's warnings on `hooks/register.tsx` were there before.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/references/` now holds the new cards; the old files and the staging folder are removed. The floor, the two host row files and the review step's reply block are unchanged.
- The four skills' `SKILL.md` carry the new texts.
- `skills/chantier/roles.yaml` and the agent files of both hosts point at the new cards and replies.
- The CLI (`take`, `take stack`, `order qa`, `round`, `handoff`, `brief`, `open`, `foreman set`, `status`, `preflight`, the board Griller and refusal texts) names only files that exist.
- `hooks/register.tsx`: the reload message after a compaction names the floor.
- Tests: new checks of the names the CLI prints, of where each rule lives and of each brief's size; tests of removed pieces deleted or converted.

## Impacts

Sessions load the new cards. No visual change.

## Test plan

- [ ] New or changed tests (they fail on the previous code)
- [ ] Local gates
- [ ] Evidence
- [ ] Review: approved
- [ ] Verified
- [ ] CI green

## Internal references

- CR-510 sc24-cards-swap, batch-31; stacked on CR-507 (PR 487).

</details>
