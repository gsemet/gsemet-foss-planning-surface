# Answers: gate-proof-cli-fixes

2026-11-11. The user's word: "fais les 2 CR maintenant", after the batch-11 retro; the user
delegates every design decision ("Grille tout avec une session fable ... je veux juste que
Chantier fonctionne et soit suffisamment générique"). The answers below are the Fable advisor's
decisions, from the code and cards on main; the Chief of Staff accepted them. File references are
to `skills/chantier/scripts/cli/src/chantier/` and `skills/chantier/references/`.

1. **"The commit".** The full SHA of the worktree's HEAD, read before the gate's first command,
   recorded in the event and written as the first line of the gate log with the CR and branch; the
   log's last line gives the result. Today the head is read after the run (commands.py:1720) and
   the log holds only `$ <cmd>` lines (commands.py:1710).
2. **Full SHA everywhere.** Recorded and compared in full in `gate`, `verdict`, `ship`, `handback`,
   `handoff`; a short form only for display. Records already written with a short head match when
   they are a prefix of the full one, so an open batch survives the upgrade (same tolerance as the
   `run is None` case, commands.py:440-442).
3. **Dirty tree at `gate`.** Refused (exit 2) before running, tracked changes and untracked files
   alike, as `verdict` already refuses (commands.py:1751-1753).
4. **HEAD moves during the gate.** Recorded as not passed at either head; the output says the head
   moved.
5. **`handback ready` refuses** (exit 2, one line per cause) when the worktree's HEAD is not the
   head `ship` recorded, the worktree is dirty, the remote-tracking branch is not at that head, or
   the gate or verdict is missing at that head (as today). It runs no fetch (concepts.md:164-166).
6. **`--no-gate`** skips only the gate check; the head, dirty and pushed checks still apply.
7. **CLI and Verifier.** The CLI refuses. The Verifier cites the gate's pass by the log header and
   `handoff`'s checklist at the full SHA in `verify.md`, and runs `gate` itself only when no pass
   exists at that head (worker.md:74-79; commands.py:1375-1381).
8. **Budget in the CLI.** `round` is refused once the budget is spent (exit 5), with a message
   distinct from the round limit so the Driver hands back `budget:` and not `rounds:` (driver.md:96,
   concepts.md:169). Align the `check_budget` docstring (rails.py:155-157), foreman.md:51-52 and the
   `round` help (cli.py:129).
9. **Open past the budget:** `gate`, `verdict`, `ship`, `note` and `handback` ("never skip a proof
   pass to save budget", driver.md:96-97).
10. **Spend figure.** The last recorded `spent_usd` (from the last `status --refresh`); `round`
    prices nothing. No budget or no priced refresh means no refusal (`over_budget`, rails.py:140-142).
11. **Un-drop command.** A new command, `restore <6-trash/item> [--slug <name>]`, no batch argument,
    run on the user's word by the Chief of Staff or a Griller: the reverse of `abandon`
    (commands.py:388-402).
12. **From and to.** From `6-trash` only, always to `1-inbox` (every dropped, cancelled or abandoned
    CR ends in `6-trash`, lifecycle.py:172-179). A merged CR is delivered: new work is a new `file`.
13. **Name and content.** The date stamp is removed, and a former batch CR's number too; content is
    kept whole (intake, intent, answers, specification, work).
14. **Refusals.** Exit 2 with nothing moved when the name is already used in the inbox, backlog,
    `3-ready` or an open batch (`--slug` renames, as `file` has), and when the item is not directly
    under `6-trash`.
15. **A cancelled CR of an open batch.** Restoring is allowed; it stays `cancelled` in that batch,
    is never revived there, and `close` must still work with its folder gone. Its old branch,
    worktree and PR are not touched; the output says so in one line. Re-entering a batch goes
    through `order add`.

## The spec-writer's open questions (2026-11-11, decided by the Chief of Staff under the user's delegation)

16. **HEAD moved during the gate:** exit 4 (external), as a failed gate command.
17. **Round limit and budget both spent:** `round` gives the budget refusal and the Driver hands
    back `budget:`; more rounds alone would not let it go on.
18. **CR numbers are never reused.** A number once given by a batch is never given to another CR,
    even after `restore` strips it from a restored folder and the batch is closed; how the CLI
    ensures it is the implementer's call. The restored CR's `01-intent.md` or notes keep a line
    "formerly CR-<n> of batch-<m>".
19. **Number stripping:** `restore` strips a number only from a folder known to be a batch CR's
    (its record says so), never a leading number of a plain slug such as `2026-plan`.
20. The chief-of-staff.md lines on the push judgement ("at the local short sha") are aligned with
    answer 2, as the spec-writer listed.

## Out of scope

Re-gating or invalidating a `ready` CR after the stack driver moves it; any git write or fetch by
the CLI; a budget check on workers or mid-round; re-pricing at `round`; restoring from `3-done` or
`5-archives`, or straight into the backlog or a batch; reviving a cancelled CR inside its batch;
changing the long gate's commands.

## Touches

The CLI (`gate`, `verdict`, `ship`, `handback`, `handoff`, `round`, new `restore`): `just scenario`
required. Cards: driver.md, worker.md (Verifier), foreman.md, concepts.md, chief-of-staff.md and
griller.md (the `restore` line). No agent file changes.

## Acceptance checks

1. After a passing `gate`, the log's first line holds the CR and the 40-character HEAD, and the
   event holds the same SHA.
2. In a repository with `core.abbrev` set to 12, `gate`, `ship`, `verdict` then `handback ready`
   succeed (fails on main today).
3. `gate` on a worktree with a modified or untracked file exits 2 and runs nothing.
4. A gate command that commits during the run leaves no pass at either head.
5. `handback ready` exits 2 with the named cause for: a commit made after `ship`; a dirty tree; a
   head not pushed; a gate passed only at an earlier head. With `--no-gate` the first three still
   refuse.
6. A batch record holding short-head events from before the change still reaches `handback ready`.
7. With `spent_usd` at or over `budget_usd`, `round` exits 5 with a budget message and the round
   count unchanged; `gate`, `verdict`, `ship` and `handback` still work. With no budget, `round` is
   unchanged, and the round-limit refusal keeps its own message.
8. `restore 6-trash/<stamp>-<slug>` puts `1-inbox/<slug>` back with its files and updates STATUS.md;
   a former batch CR loses its number.
9. A name clash exits 2 with nothing moved, and `--slug` resolves it; an item from `5-archives` is
   refused.
10. After restoring a cancelled CR of a paused batch, `close` (without `--yes`) still runs.
11. driver.md, foreman.md, concepts.md, the rails docstring and the `round` help say the same thing
    about the budget. `just check` and `just scenario` pass on both forges.

Runs in parallel with driver-liveness; no `depends.json`.
