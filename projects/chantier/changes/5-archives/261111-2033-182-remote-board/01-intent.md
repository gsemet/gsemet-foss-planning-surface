# Intent: a progress board that works in remote

2026-11-10, the user, during batch-09:

> ok donc ce qui me manque en remote c'est une surface de suivi de projet. un genre de mini
> jira. j'ai bien le mod en local mais en remote ca ne marche pas. est ce que tu peux faire un
> petit prototype d'un serveur en python avec uv run qui pourrait tourner en background et
> fournir un suivi d'avancement

- In remote (Remote Control on a phone), the local mod pane is not shown: the user has no view of
  the batches, the CRs and the backlog other than asking "status".
- Prototype by the Chief of Staff: `prototype/board.py`. It is a single-file `uv run --script`
  server that uses only the standard library and reads only. It shows:
  - each batch from `STATUS.json`: the CRs, the spend, the heartbeat and the recent events;
  - the inbox and the backlog by priority;
  - any file under the changes folder.
  The page refreshes every 30 s. It also serves `/api/status`, which returns JSON.
- It knows both layouts: `3-requests` in the project and `4-batches` on the surface.
- Open for the grill:
  - How a phone reaches it. The default `127.0.0.1` is local only; Tailscale or the LAN with
    `--host 0.0.0.0` has no authentication.
  - Whether chantier ships it, as a CLI `board` command or a separate script.
  - Whether it may write anything, such as answering an ask or adding an inbox item.
  - How it relates to the mod and to `planning-repo`'s surface.
- Since then, the batch folder is `4-batch` (CR-158), not `4-batches`.
