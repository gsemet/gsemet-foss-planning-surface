# Batch-17 retro: GitHub issue drafts (chantier points)

Drafted 2026-11-14 by the Chief of Staff from `5-archives/batches/batch-17.md` (the retro, after
an Opus critic). Nothing is posted. The user picks which become CRs of batch-18 and which are
posted as issues. Points already covered by a batch-18 CR are marked.

1. **Drivers run git only in their worktree.** A Driver rebased in the main checkout instead of
   its worktree (CR-245, aborted at once). Fix: the Driver and conflict-resolver cards run every
   git command as `git -C <worktree>`; the main checkout is read-only except the post-merge
   fast-forward.
2. **One restack pass after each native stack merge.** GitHub's native stack merge rewrites the
   branches above the merged one, so every child needed a restack and fresh CI. Fix: the
   stack-driver card plans one restack pass right after each stack merge, siblings pushed at once.
3. **A blocked CR's ready hand-back is accepted with a note.** A blocked hand-back keeps the CR
   blocked, so its later ready hand-back is refused until the Foreman takes it back with
   `take --note`. Fix: `handback ready` from the recorded Driver of a blocked CR is accepted with
   a note.
4. **A long-gate waiver is recorded per CR.** CR-228 thought its gate was waived; the follow-up
   gate on main was left to memory. Fix: the Foreman records a waiver and its scope as an order on
   each CR it covers, and files the follow-up at the waiver. *(Mostly covered by gate-rules, rule 4.)*
5. **`forge-stack create` builds from the ready CRs.** It refused while some CRs were still
   queued. Fix: it builds from the ready CRs and leaves the queued ones to a later `rebuild`.
6. **Worker reply templates.** Out-of-format Inspector and Verifier replies (APPROVED for APPROVE,
   missing head, extra keys) on four CRs each cost a restart. Fix: the inspector and verifier
   cards end with the exact reply template; `verdict`'s refusal names the accepted words.
   *(Close to worker-reply-length.)*
7. **Sync once, then `--no-sync`, on Windows.** A running gate or the board holds
   `.venv\Scripts\chantier.exe`, so after a fast-forward every `uv run --locked` failed with os
   error 32; and the Chief of Staff's `uv run --no-sync` board start failed on a stale .venv
   (uvicorn missing). Fix: chantier's own-checkout run line syncs once at batch start, before the
   board starts and after any merge that changes `uv.lock`, then runs with `--no-sync`; preflight
   says so on Windows.
8. **Board write-path tests use a scratch planning folder.** CR-226's smoke test wrote a
   self-nesting tree inside the live record. Fix: the Driver card points tests and smoke runs of
   the board's write paths at a scratch planning folder.
9. **`.git/info/exclude` is out of bounds.** CR-248's Driver wrote to it. Fix: the Driver card
   names it; ignores go in the worktree's own files or not at all.
10. **Stacked CRs read their base from the forge.** `take`, `handoff` and `ship` printed
    `base origin/main` for stacked CRs. Fix: they take the base from the PR's base when a PR exists.
11. **The Inspector reviews the round's last commit.** CR-228's round-4 Inspector approved
    073cfc5, then 6860065 was pushed. Fix: the Driver card has the Inspector review the last commit.
12. **The Driver brief carries the Foreman's address.** CR-252's first `pr` message was lost.
    Fix: the Foreman card's Driver brief always carries it.
13. **The spec critic splits bundled CRs.** CR-221 ($23.27) and CR-225 ($21.77) cost about five
    times the median: a refactor bundled with a lint cleanup, several views in one CR. Fix: the
    spec-critic flags such a spec and the grill splits it.
14. **The stack's merge line carries each CR's open gaps.** PR #197 merged as the bottom of a
    stack with its "no pane screenshot" gap open. Fix: the `stack-ready-to-merge` line carries
    each CR's gaps; the Chief of Staff applies the pane-screenshot rule before offering the stack.
15. **The Chief of Staff marks asks read as it acts.** 45 asks were left unread, so CR-228's
    blocked ask looked like the rest. Fix: the Chief of Staff runs `asks --read A-<k>` in the
    turn it relays or orders on an ask.

Not drafted (project points): CR-228's stale screenshots (CONTRIBUTING: rerun
`just docs-screenshots` when the board's drawing changes); the 0.9.0 notes and `batch-pace.svg`.
