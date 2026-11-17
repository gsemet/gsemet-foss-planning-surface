# Inbox items absorbed into this CR

Scen-Q1 (2026-11-14): the user chose to fold the three gate items into this CR. Their intake, verbatim:

## From `long-gate-after-batch-17`

### Run the long gate on main after batch-17 and fix what it finds

Filed 2026-11-14 by the Chief of Staff, on the user's word: "finaliser ce batch le plus vite
possible quite à fixer les CI longue par la suite".

From about 12:50 on 2026-11-14, batch-17's PRs were merged without the local long gate
(`just scenario` on Windows, GitHub and GitLab): GitHub CI green at the head was accepted in its
place (`just check` on Linux, macOS and Windows, `just scenario` on Linux, `just eval-dry-run`).
Each waived CR records it, and its hand-back carries `--no-gate`.

What this CR does once batch-17 is merged: run the long gate (`just check`, `just scenario`) on
main on Windows, the GitHub and the GitLab scenarios, and fix any failure, one commit per cause.
Done when the long gate passes on main.

## From `gate-priority`

### Gate queue and push order: put the user's next merge first

Filed 2026-11-14 by the Chief of Staff, on the user's word: a CR for after batch-17.

Two rules in the cards slow down the PR the user will merge next:

1. Long gates run in arrival order (`concepts.md`, "Long gates run one at a time, in arrival
   order"; `driver.md`, the long gate). The CR whose merge comes next for the user (the stack's
   lowest open PR, then its children once restacked on main) should take the first place in the
   queue; queued gates yield to it; a gate already running is never stopped.
2. The Driver pushes only after the long gate (`driver.md`, "Rebase first, so the long gate passes
   on the head you push"). For a PR that already exists, after a rebase or a restack, the Driver
   should push at once with `--force-with-lease`, the PR kept in draft, so CI runs while the gate
   waits in the queue; the PR leaves draft only when the long gate and CI have both passed at the
   same head. A new PR still waits for its long gate, as `AGENTS.md` requires.

The principle missing from the cards: what unblocks the user's next merge goes first.

#### Evidence (batch-17)

- CR-237 (PR #171) rebased cleanly onto main at about 11:24, waited for CR-225's running gate,
  started its own at 11:53, passed at 12:29, and was pushed only then: CI started at 12:30.
  About an hour lost on the PR the user was waiting to merge.
- The Foreman applied both rules by direct order of the Chief of Staff during the batch, then
  extended rule 2 to CR-240, which had no PR yet, against `AGENTS.md`; corrected before any PR
  was opened.

## From `long-gate-defaults`

### Review the default rules for running long gates

Filed 2026-11-14 by the Chief of Staff, on the user's word: "que l'on revoit ensemble les règles
par défaut d'exécution des Gates longues". For after batch-17; to grill with the user, not
before.

Batch-17 showed the default long-gate rules cost hours on the path to the user's merges:

- Long gates run one at a time, in arrival order; the PR the user merges next waited behind
  another CR's gate.
- A rebased PR was pushed only after its long gate, so the forge's CI started late.
- Every rebase, even a clean one onto a docs-only change, ran a full long gate again.
- The user waived the local long gate for the rest of the batch (Rebase-Q1 A, then the whole
  batch from about 12:50), keeping GitHub CI green at the head as the proof.

What to decide together: when a long gate is needed by default (new PR, rebase with or without a
conflict, after a merge below), what the forge's CI can replace, how the queue is ordered, and
what a project says in its `AGENTS.md` to choose.

#### The user waives long gates in a stack (added 2026-11-14)

The user's words: "j'aime bien cette idee que l'utilisateur accepte dans le cas d'une stack de
désactiver d'eventuelle gate longue. il faudra que ca apparaisse dans la status, le mod, la ui
webview".

In batch-17's stack the user's rule was: one long gate on the top PR only. The lower PRs go
green as soon as CI is 5/5, CLEAN, VERIFIED and handed back. The top PR validates them, and a fix
goes on the top PR or on a PR above it. New CRs that join the stack run no long gate (the batch
waiver).

To grill: make this a choice the user accepts for a stack (per batch, at the go or during the
run), and show it wherever the batch is shown. That means `chantier status` (text and
`STATUS.md`/`STATUS.json`), the CR board pane (the mod, `hooks/register.tsx`) and the web view
(`chantier board`). Each CR shows whether its long gate was waived, and which PR carries the
stack's validating gate.

Related items: `gate-priority` (queue order and early push), `long-gate-after-batch-17` (the
long gate on main after the batch).

