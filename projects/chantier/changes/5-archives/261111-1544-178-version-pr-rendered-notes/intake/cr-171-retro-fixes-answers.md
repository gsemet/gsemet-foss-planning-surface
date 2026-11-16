# Answers: cr-171-retro-fixes

## Decisions of 2026-11-11 (points 2 and 3; point 1 moved to `worker-write-guard-redesign`)

Decided by a Fable advisor on the user's delegation: "Grille tout avec une session fable je ne sais pas te répondre…"

1. **Point 2 is a card change only.** `driver.md` says a Driver reads its `team:` lines with
   `handoff` (or keeps those `take` printed), and that `round` is run only to start a round,
   just before a Coder. Reason: `handoff` already prints the `team:` lines on main and counts
   nothing; the card's "as the `team:` lines of `round` print them" is what misled the Driver.
2. **The CLI does not change for point 2.** No new refusal, no "dry" `round`. Reason: the means
   exists; the rule on new CLI tools asks for a measured cost, and one lost round is a wording
   defect.
3. **Point 3: no line that starts with "Driver" ever names the steering session or its own
   subagents.** In every output of `cost` (the lines, `--explain`, the summary of `pause` and
   `close`), the steering session reads as the Foreman or `Chief of Staff, steering the batch`,
   and its subagents that belong to no CR as `Foreman's own subagents` or `Chief of Staff's own
   subagents`, in Foreman mode and in direct mode alike. Reason: the user reads "Driver" as a
   CR's Driver; a wrong name makes the split unreadable.
4. **Point 3 is partly done on main; the CR covers what is left.** The breakdown lines already
   use the two "own subagents" labels. The summary's `Driver <type> with its workers` lines still
   print the steering session of a direct batch as `Driver chief-of-staff with its workers`: that
   line goes (its figure is the steering row's). Reason: checked on main at 24cc7eb.
5. **Where the host gives no parent link (Copilot), nothing changes:** an agent's line says only
   its type. Reason: who is whose cannot be measured there, and nothing is guessed.
6. **Point 3 goes into the same CR as `cost-unknown-model` and `report-template`;** point 2
   rides with another small `driver.md` change (`version-pr-rendered-notes`). Reason: same
   files, one long gate each.
