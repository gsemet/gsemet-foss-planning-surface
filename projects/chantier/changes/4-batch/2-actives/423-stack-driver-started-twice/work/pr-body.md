## Summary

On Claude Desktop, a background subagent Driver cannot message the session that steers it before its end: its hand-back reaches that session only as its final report. The Claude Code host reference said the opposite (`SendMessage` to `main`, "proved"). In one real batch, a steering session read a Driver's silence as a lost Driver and started a second stack Driver 25 minutes before the first one's hand-back arrived. This PR corrects the host reference, writes down what a Driver really sends, and tells the steering session what a Driver's silence means on this host.

## Deliverables

What changes, by file (card text only, no code):

| File | Before | After |
|---|---|---|
| `skills/chantier/references/hosts/claude-code.md`, row "A Driver messages its steering session" | `SendMessage` to `main`, "proved, same" | the Driver's final report only, once, at its end; the `Steering:` line written out; the mark says what is proved and what was only seen, with a trial |
| `skills/chantier/references/hosts/claude-code.md` | no section on silence | new section "A Driver's silence" (six points, the `ping` point marked unproved with its trial) |
| `skills/chantier/references/foreman.md`, proof of death | a `ping` with no `pong` | same, plus: on a host where a Driver cannot answer before its end, the sign that host's reference names stands in place of the `pong` |
| `skills/chantier/references/driver.md`, `ping` bullet | answer `pong` | same, plus: when the `Steering:` line says nothing reaches the steering session before the end, a `ping` gets no answer |

The `Steering:` line a Driver gets on Claude Desktop (excerpt of the new row):

```text
Steering: the Foreman (session <id>, for the record). Nothing reaches it before your end: send no message. Your one send is your final report (the host's hand-back): its first line is your hand-back line, then every other line due (`anomaly`, `push`), one per line, ... Record an `anomaly` when it happens: `$CHANTIER note <cr> "anomaly: <text>"`. A `ping` needs no answer: go on.
```

Choices: the row and the line hold for every Driver (CR, stack, release, QA); a direct batch from a terminal or VS Code keeps `SendMessage` to `main` (unproved); no new refusal of a second stack Driver, and no CLI or agent file change.

## Blast radius

Grade: 1. Card text only (one host reference, two generic cards); `git revert` restores the previous text.

## Autonomous decisions

- The Driver recorded the round (`round`) after the Coder had run, not before it: an ordering slip with no effect on the files.

## Known gaps

- The host's exact text for a Driver's `SendMessage` to `main` under a Desktop steering session was not recorded when it was seen; the card does not quote one. A trial in the next Foreman batch records it.
- The `ping` read through the `activity` age (a proof of life without a `pong`) is unproved; its trial is written in the card.

<details>
<summary>Details</summary>

## Changes

- `hosts/claude-code.md`: the row's two cells rewritten, keeping the first cell's opening words (the CLI's prompt skeleton finds the row by them); the new section "A Driver's silence".
- `foreman.md`: one pointer in the second proof of death.
- `driver.md`: one sentence in the `ping` bullet.
- `concepts.md` and `routing.md` read and left unchanged (still true).

## Impacts

No visual change. A steering session no longer starts a second Driver on silence; a Driver's `anomaly` is a note on the CR and a line of its final report.

## Test plan

- [ ] New or changed tests (they fail on the previous code) No behaviour change: card text only; existing structure tests read the shipped cards
- [ ] Local gates at `<sha7>`: `just check`
- [ ] Evidence: no before/after visual: card text only
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

- CR-423 "A Driver's only send to a Desktop Foreman is its final report", batch-29.
- Seen in the retro of Studio's batch-06, 2026-11-20.

</details>
