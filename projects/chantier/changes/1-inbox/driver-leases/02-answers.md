# Answers

Short name: `driver-leases`

This CR is Part D of the seven-part split of `planning-server` (the user's answer planning-server-Q7,
2026-11-20, "7 CR séparés"). It was grilled there, not here: the user's answers live in
[`../../2-backlog/P3/planning-server/02-answers.md`](../../2-backlog/P3/planning-server/02-answers.md),
and the grilled reference is that CR's
[`experiments/03-change-spec-all-parts.md`](../../2-backlog/P3/planning-server/experiments/03-change-spec-all-parts.md),
"Part D. Leases".

The answers this CR carries, in the user's words where they are short:

- 2026-11-10: heartbeat/reclaim, borrowed from Beads: "ça vaudrait le coup". Hash IDs rejected
  ("ce serait pas trié et j'ai déjà un slug"): a lease uses the CR's id and small numbers.
- 2026-11-10 (planning-repo, answer 4): a running batch's state stays local to the steering
  machine: a lease lives in `batch.json`, never published.
- 2026-11-20, Q1-Q2: no Board dependency; chantier's journal, surface server and watchers stay the
  channel.
- 2026-11-20, Q3: "tout": leases on the work a Driver holds are in scope; they replace the
  "session file written in the last 5 minutes" heuristic.
- planning-server-Q7: one CR per part; Part D needs Part A (typed journal events) first.
- planning-server-Q8: "Tâche de fond vivante": a Driver's lease stays live while a background
  task recorded for the CR runs (the CI watch), as the long gate today.
- planning-server-Q9: "Exception nommée": `lease` is built and named in AGENTS.md as an exception
  to the measured-cost rule for new CLI tools, citing the user's 2026-11-20 answer ("tout").
- planning-server-Q14: "Baux en attendant": leases serve Copilot's `close` until
  `copilot-close-end-event` (P2) lands; then Copilot reads the agent's end and the lease is only
  shown, as on Claude Code.
- planning-server-Q16: "10 min, constante": 10 minutes, renewed every 3, a constant in the code.
- planning-server-Q20: "Non, affiché seulement": on Claude Code the transcripts stay the exact
  source for `close`; a live lease is only shown.
- planning-server-Q21: "Oui, dans ce travail": QA orders get leases; the QA driver takes and
  renews one as a CR's Driver does.
- 2026-11-20, the coherent split: each part changes, in the same CR as its behaviour, the docs and
  the SVG diagrams (with their `-texts.md`) its change makes false, given as a list, not a search.

## 2026-11-20, settled by the Chief of Staff (the user asks no questions)

Answers to the first specification's open questions:

1. **The stack driver's lease.** `--lease` is required on `forge-stack` and `stack`, as on a
   Driver's commands; the stack driver's facts carry `lease: stack <n>`; the stack lease ends
   when the steering session clears the stack agent (the existing `agents set` form that
   clears it; the spec names it from the code, and adds no `handback stack` command).
2. **The Driver card's cap.** The 45,000-byte cap does not rise. The `claim lost` rule stays on
   the common path (a Driver must act on it at once); the rest of the lease text (reclaim,
   `lease hold`, expiry) moves off the common path, read when it applies; the common path's
   existing text is tightened for what is left.
3. **The QA driver's first `agents set`.** The first `agents set O-k <agent>` after `order qa`
   keeps lease 1; only a later restart starts lease n+1.
4. **The end of a `lease hold`.** The lease renews once when the held child ends, so a long CI
   watch does not end with an expired lease.
5. **Times in lease messages.** UTC, like the record.
6. **`cancel` and `order drop`.** Both end a live lease.
