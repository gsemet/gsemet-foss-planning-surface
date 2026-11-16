# Verification of CR-219 at 0c4838f

Checked against the spec's Evidence section, on the diff `origin/main...HEAD` (7 files).

- Queue (tickets in `.long-gate.queue/`, first live ticket tries the lock, dead pids deleted, ticket removed in every exit path): matches the spec in `commands.py`.
- Hour per holder (restarts on a new holder key, `pg<m>` ignored; second wait counted from its own start): matches.
- Refusal wordings: match the spec text, exit 2, name the holder read at refusal time.
- Waiting-note prefix kept (`waiting for the long gate of ...; queued ahead: ...`).
- Scenario: the arrival-order check and the killed-waiter check are present and passed (reported green at 0c4838f, CI green).
- Fresh planning folder: ran `init` in a temp git repo, `.gitignore` lists `.long-gate.queue/`.
- Refusal proof: `evidence/04-refusal-proof.md` shows the refusal naming CR-B after the holder changed; its text equals the code's string. Not re-run (driver script not kept).
- Cards and docs (driver.md, concepts.md, docs/gates.md, cli help): as specified; no agent file touched.

Nits, not blocking: some edited lines exceed the usual wrap (driver.md line 58, docs/gates.md line 11, state.py IGNORED line).

Verdict: VERIFIED.
