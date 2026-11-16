# Review the default rules for running long gates

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

## The user waives long gates in a stack (added 2026-11-14)

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
