# Answers

1. Q: What is it for? User, 2026-11-18: "et une CR qui permet dans ce mode d'envoyer directement
   une CR spécifiée dans le batch de manière automatique" ("ce mode": a batch opened empty,
   waiting for its CRs).

2. Q: Its name and scope? User, 2026-11-18: "super tu appliques ce concept directement on va
   l'appeler factory: dès qu'une idée est en ready elle part dans le batch qui reste toujours
   ouvert. il faudra bien le documenter dans le readme". So: the mode is called **factory** (it
   replaces "auto-join" everywhere below: the record field, `order factory off|on`, the status line
   `factory: on`); a factory batch stays open (see the last points); the README documents it.

## Settled by the Chief of Staff (2026-11-18, after answer 2)
- A factory batch never ends by itself: when its last CR ends, it pauses as today (worktrees and
  branches cleaned), waiting for the next ready CR, and the Chief of Staff offers no retro and no
  close then. The retro and the close happen only on the user's word (`close` as today).
- `open` with no CR opens a factory batch (the mode `open-empty-batch` makes); `open --factory`
  with CRs makes one too. Without either, a batch is not a factory, as today.
- The README gets a section "Factory mode": what it is, how to open one, what joins on its own and
  what does not (a release), how to stop it (`order factory off`), and how it ends (the user's
  `close`). The use-cases docs name it too.
- In the meantime, before this CR is merged, the Chief of Staff applies the concept by hand to
  batch-28: each CR it marks ready joins at once with `order add`, and it offers no close.

## Settled by the Chief of Staff (spec-writer's questions, 2026-11-18)
- `order factory on` turns any open batch into a factory, one opened with CRs and no `--factory`
  included; "without either, a batch is not a factory" is about `open` only.
- `order factory off` makes the batch an ordinary one: the retro and the close offer come at its
  last CR's end, or at once if it is already paused with every CR ended.

## Settled by the Chief of Staff (spec critic, 2026-11-18)
- A release in a factory batch: when a release CR joins (`order add --release`), the factory turns
  off by itself, as `order factory off` does; the batch ends after the release as an ordinary one,
  and the Chief of Staff opens a new factory batch after its close.
- A CR that reaches `3-ready` without joining (a Griller in a worktree, another machine through
  autosync): the Chief of Staff, when it places or sees it, runs `order add` on its own; the
  factory's go covers it. A release CR is still excluded.
- A CR made ready with no specification (automatable) joins like any `triage --ready`.
- CRs already in `3-ready` when a batch becomes a factory (empty `open`, `open --factory`, `order
  factory on`): the Chief of Staff adds them with `order add` at once, the factory's go covering
  them, and names them to the user. Release CRs excluded.

- A release with a factory from the start (`open --factory --release N`), or `order factory on`
  while a release CR is in the batch and not ended: both refused, with the reason (a release ends
  the factory) and the way out (open without `--factory`, or `factory on` after the release).

3. Q: The shape of a factory batch? User, 2026-11-18: "L'idée c'est d'avoir un batch ouvert en
   attente avec 4 slots, sortie en stack grandissante automatiquement, dès qu'une CR est spécifiée
   et mise en ready elle part". So the cards make the Chief of Staff open a factory batch as
   `--mode stack --slots 4` unless the user says otherwise; the stack grows as today (made at two
   PRs handed back ready, each later CR joining on top). The README's "Factory mode" section shows
   that command. No CLI default changes: `open` keeps `parallel` when no mode is given.

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- The mode: a batch opened with no CR records that it takes ready CRs on its own ("auto-join").
  A batch opened with CRs does not; today's path is unchanged for it.
- The trigger: `triage <folder> --ready` while an auto-join batch of the project is open (running
  or paused) moves the CR to `3-ready` and adds it to that batch in the same call, exactly as
  `order add <folder> --batch <batch>` would (same checks, same refusals, same order line). A
  refusal of the add leaves the CR in `3-ready` and says why; nothing else changes.
- The go: the user's go for the empty batch covers each CR that joins it this way; no separate go
  per CR. The user's word can still stop it: auto-join can be turned off and on for the batch by
  an order (`order auto-join off|on --batch <batch> --note "<the user's words>"`), recorded in the
  batch's log.
- Never automatic: a release CR (it needs `--release` and its own go), and a CR filed straight to
  `3-ready` by any other path than `triage --ready`. Those keep `order add`.
- The order line `triage` prints is relayed to the Foreman verbatim, as for `order add`, by the
  session that ran it: the Chief of Staff, or a Griller, who sends it to the Chief of Staff to
  relay. In direct mode the Chief of Staff takes it as usual.
- Joining order: CRs join in the order they become ready; in a stack batch each joins on top, as
  `order add` does today.
- The budget is unchanged: a CR may join past the budget; no Driver starts past it, as today.
- `status`, the board and `brief.md` say when a batch is auto-join ("auto-join: on").
