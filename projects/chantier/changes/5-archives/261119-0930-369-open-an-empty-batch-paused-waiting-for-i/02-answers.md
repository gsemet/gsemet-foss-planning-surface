# Answers

1. Q: What is it for? User, 2026-11-18: "ouvre un nouveau batch dans un nouveau foreman en attente
   d'un nouveau CR", then "fait une CR qui permet de faire un batch vide directement en pause".

2. Q: The concept around it? User, 2026-11-18: "on va l'appeler factory: dès qu'une idée est en
   ready elle part dans le batch qui reste toujours ouvert. il faudra bien le documenter dans le
   readme". The factory mode itself (auto-join, the batch that stays open, the README section) is
   the CR `ready-joins-waiting-batch`, stacked on this one; this CR only makes the empty paused
   batch, and its output and docs may call such a batch "a factory batch waiting for its first
   CR" once that CR lands. Here, no factory behaviour.

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- A batch opened empty, never steered (no Foreman claimed, no `take`), that the user asks to close:
  `close` accepts it; its cost reads "none: no session steered it", never $0.00. No Known gap.
- `--autonomous-releases N` and `--grant-fixes` with no CR keep today's refusal (they need
  `--release`); the grant comes later with `order add --release`, then `order grant`, as today.

## Settled by the Chief of Staff (spec critic, 2026-11-18)
- Direct mode on a batch opened empty: the Chief of Staff claims the batch (its epoch) just before
  its first `take`, not at `open`, so the wait costs the batch nothing. A Foreman claims at its
  start as today; the wait of a Foreman with no CR counts in the batch's spend.
- One CR, as specified: the pane and web-board display ship with the CLI part; the pane
  screenshot stays a Known gap until the user gives one.

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- `chantier open` with no CR is accepted: the batch is numbered, its record, `brief.md` and STATUS
  files are written, and it is born paused, with no CR. All of `open`'s options keep their
  meaning (`--slots`, `--budget`, `--mode`, `--direct`, `--default-branch`, `--remote`,
  `--autonomous-releases`, `--grant-fixes`); `--release N` with no CR is refused (it names an
  item), with that reason.
- No new flag: no CR given is the empty batch. Its output says it is paused with no CR and names
  the next step: `order add <folder> --batch <batch>` for each CR, then start the Foreman (or, in
  direct mode, `take`).
- It is the same paused state as a batch whose last CR ended: `order add` joins it and leaves it
  paused; the first `take` sets it running. Nothing new in that path.
- One batch per project still holds: an empty paused batch is an open batch, so a second `open`
  is refused as today, with the empty batch named.
- Foreman mode: the Chief of Staff may start the Foreman right after an empty `open`. The Foreman
  claims its epoch and waits, with no Driver to start, until an order arrives; it is ready, not
  done. Its cards say so.
- `close` of a batch that never held a CR is accepted: it archives no CR, its cost is the steering
  spent, and its record and retro say "no CR".
- `status`, the board and the CR board pane show the empty batch as paused, "no CR yet". The
  watcher refuses a paused batch as today; once the first `take` sets the batch running the
  watcher starts as usual.
- The Chief of Staff's plan for an empty batch shows the mode, slots, budget, team and who steers;
  the floor and the delivery time are "none yet: no CR".
