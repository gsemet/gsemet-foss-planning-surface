# Change Specification: a session whose chantier CLI cannot run stops at once

## Goal

When `$CHANTIER` cannot run, the session stops, in every mode and every role. Seen on 2026-11-17
(the owner's screenshot): a session wrote "chantier's CLI won't start here and its packages can't
be fetched, so I'm proceeding without it" and went on working. The owner's word: « non si le CLI
ne peut pas être lancé il faut arrêter tout de suite ».

Today the stop rule covers only one case. `startup-core.md` says: "Run the official `$CHANTIER`
preparation ... If it fails, report its exact diagnostic and stop role initialization". The four
`SKILL.md` files link it only to the dev mode's `uv sync` ("a failure follows `startup-core.md`").
Three cases have no rule:

- the plugin mode (`uvx --from "<plugin root>" chantier --skill ...`) failing;
- a later `$CHANTIER` call failing (a fetch refused, a sandbox with no network, a cloud session, a
  crash on start);
- an agent reading the "a skill or tool ... the session lacks is not a stop: ... work without it"
  lines as permission to go on.

This CR makes it one rule, in the common startup core that every role reads at boot. It also
excludes the CLI, by name, from every "work without it" line.

This change touches only cards and tests. It changes no CLI code, no agent file and no manifest
entry; only the manifest's `limit` field may change (see "The startup byte budget").

## The rule (decisions of `02-answers.md`)

If `$CHANTIER` cannot run, the session reports the exact error and stops. This holds:

- in the dev mode (`uv sync --locked --project` or `uv run --no-sync --project`) and in the
  plugin mode (`uvx --from`);
- at the start or at any later call: a fetch refused, a sandbox with no network, a cloud session,
  a crash on start.

**What "cannot run" means.** Only the launch itself fails: `uv` or `uvx` cannot set the CLI up or
start it (a fetch refused, no network, a sync or install error), or the CLI crashes before the
command runs (an import error, a traceback at startup). These keep their existing handling and
are not this rule's stop:

- a CLI refusal (`rails.py` refusing an action, with its message);
- a command's own error exit (the command ran and reported an error);
- a host's permission denial (the host refused to run the command).

After it stops, the session:

- does no work as its role;
- takes no seat: no `seat take`, and no seat written by any other means;
- writes nothing in the planning folder, by any tool;
- never goes on "without it".

The rule holds for every role: Chief of Staff, Griller, the router, the status skill, Foreman,
every Driver kind and every worker (Investigator, Coder, Inspector, Debugger, Verifier, Conflict
resolver, Demo explorer, Spec-writer, Spec critic, Retro critic, an extra review step).

**Who it reaches.**

- A steering session (the Chief of Staff, a Griller, the router, the status skill) tells the
  user.
- An agent started by another (a Foreman, a Driver, a worker, a Chief of Staff's subagent) ends
  its turn. Its reply to its parent is the error. It cannot use `$CHANTIER handback` or
  `$CHANTIER note`, so the reply is plain text that quotes the error exactly.
- The parent applies the same rule to itself only if its own `$CHANTIER` fails. Otherwise it
  handles the child's reply under the rules it already has. This CR adds no new parent handling.

**No retry loop, no repair.**

- None of these: an upgrade, a reinstall, a substitute launch (another `uv`/`uvx` form, another
  source, a cached copy, `pip`, a direct `python -m`), a repair, or any other route.
- One plain retry of the same command is allowed only when the error itself is a transient
  network error (for example a connection reset or a timeout while fetching). If that retry also
  fails, the session stops.

**The exception lines.** Every line that says a skill or tool a role lacks "is not a stop" and
the role "works without it" names the CLI as excluded.

## What changes

### `skills/chantier/references/startup-core.md` (the common core every role reads at boot)

Replace its second paragraph, the one from "Run the official `$CHANTIER` preparation" to "failed,
unavailable, and not performed." The new paragraph:

- Keeps the preparation sentence ("Run the official `$CHANTIER` preparation for the selected
  source and version.").
- States the rule above in full:
  - both modes, at startup or at any later call;
  - "cannot run" means only a launch failure (uv or uvx cannot set it up or start it, or it
    crashes before the command runs); a CLI refusal, a command's own error exit and a host's
    permission denial keep their existing handling;
  - the exact error reported;
  - no work as the role, no seat, nothing written in the planning folder, never "without it";
  - no upgrade, reinstall, substitute launch, repair, or other source or tool;
  - the one plain retry, only on a transient network error;
  - a steering session tells the user; a started agent ends its turn with the error as its reply.
- States that this rule is not the "a skill or tool the role lacks" case: the CLI is never a tool
  a role works without.
- Keeps the paragraph's last sentences unchanged in meaning ("Other checks are read-only and
  block only the actions whose prerequisite failed; distinguish failed, unavailable, and not
  performed.").

The wording is the Driver's. It is plain English in the card's style and holds every point
above. The paragraph is written once, here. The cards below point to it and never copy it.

### The four `SKILL.md` files

These are `skills/chantier/SKILL.md`, `skills/chief-of-staff/SKILL.md`,
`skills/griller/SKILL.md` and `skills/status/SKILL.md`.

- In the mode paragraph (the one that starts "`$CHANTIER` is the CLI, one launch in two modes"),
  "(a failure follows `startup-core.md`)" today covers only the `uv sync`. Change it so that a
  failure of the sync, or of `$CHANTIER` in either mode at any call, follows `startup-core.md`.
  Two ways work: move the pointer to the end of the paragraph, or make it read "any failure of
  the sync or of `$CHANTIER`, in either mode: `startup-core.md`". The four paragraphs stay
  identical to each other except for the path forms they already differ by (`<this skill's
  folder>` in the router, `<../chantier made absolute>` in the others).
- The forms `test_plugin_files.py` asserts stay present in each file: `uv run --no-sync
  --project`, `uv sync --locked --project`, `uvx --from`, `--skill`, `.git`.

### The "work without it" lines: the CLI named as excluded

Each line below keeps its meaning for skills and tools. It gains one short clause: the CLI
(`$CHANTIER`) is never such a tool, and a CLI that cannot run is a stop (`startup-core.md`). One
form works: "(never `$CHANTIER`: a CLI that cannot run is a stop, `startup-core.md`)". Use the
same clause in every file.

- `skills/chantier/references/concepts.md`:
  - "Rules", rule 2 ("No fallback"), the sentence "A skill or tool the playbook says a role needs
    and the session lacks is not a stop: ...";
  - the `Needs:` bullet ("An agent that does not have one of them says so in a note and does its
    part without it (rule 2)").
- `skills/chantier/references/chief-of-staff.md`:
  - "Hard rules", "No fallback", the sentence "A skill or tool the playbook says a role needs and
    your session lacks is not a stop: ...";
  - "Required skills and tools", the paragraph that says the role "works without it".
- `skills/chantier/references/driver.md`: the `Needs:` sentence ("A `Needs:` you cannot meet is a
  `$CHANTIER note`, and you do your part without it.").
- The no-fallback bullet in each worker card: `coder.md`, `conflict-resolver.md`,
  `debugger.md`, `demo-explorer.md`, `inspector.md`, `investigator.md`, `review-step.md`,
  `verifier.md`, all under `skills/chantier/references/`. Each holds "A skill or tool the
  playbook says the role needs but the session lacks is not a stop: say so in a note and work
  without it, never by another means."

The Driver also greps the cards and the four `SKILL.md` files for any other "not a stop", "work
without it", "works without it" or "part without it" line about a missing skill or tool. It adds
the same clause to each one it finds and names them in its delivery. These lines are not about a
missing skill or tool and stay as they are:

- `concepts.md`'s "No escalation printed ... It is not a stop and not a look-alike";
- the "without its hand-back" lines.

### The startup byte budget

`skills/chantier/scripts/cli/tests/test_startup_manifest.py` caps each role's startup reading
(and its reload reading) at `STARTUP_LIMIT = 12_288` bytes. `startup-core.md` is read by every
role, so every role grows by the paragraph's net growth. Measured on `main` at 5717626d
(`pytest skills/chantier/scripts/cli/tests/test_startup_manifest.py -s`), the tightest roles are:

| Role | Host | Startup bytes | Reload bytes | Headroom at reload |
| --- | --- | --- | --- | --- |
| chief-of-staff | copilot | 11539 | 12282 | 6 |
| chief-of-staff | claude | 11533 | 12276 | 12 |
| router | copilot | 11506 | 12249 | 39 |
| router | claude | 11500 | 12243 | 45 |
| status | copilot | 11091 | 11834 | 454 |
| griller | copilot | 10996 | 11739 | 549 |

Every other role has more than 1400 bytes of headroom.

- The limit stays as it is if the rule fits. The Driver first makes room in the files the tight
  roles read at boot:
  - First, write the new `startup-core.md` paragraph so that it replaces the old one rather than
    adding to it. Keep it short.
  - Then trim wording in the four `SKILL.md` files, which are read whole at boot by the
    chief-of-staff, router, griller and status roles.
- A trim may only remove wording or repetition, for example a phrase said twice or a restatement
  of what a deferred card already holds. It never drops a rule. The Driver names each trim in
  its delivery.
- If, after those trims, the rule still cannot fit under the limit for the chief-of-staff and
  router roles without dropping a rule, the limit may rise by what the rule needs, at most 256
  bytes (to at most 12544). The PR names the new figure and its reason (the measured bytes of
  the tight roles, before and after, and the trims already made). Beyond 256 bytes, the Driver
  stops and reports `blocked` with the measured numbers.
- The figure lives in three places, changed together, to the same value:
  - `skills/chantier/references/startup-manifest.json`, `"limit": 12288` (line 3);
  - `skills/chantier/scripts/cli/tests/test_startup_manifest.py`, `STARTUP_LIMIT = 12_288`
    (line 10), asserted equal to the manifest's `limit` at line 132 and used as the cap at lines
    157 and 159;
  - `skills/chantier/scripts/cli/tests/test_plugin_files.py`, `STARTUP_LIMIT = 12_288` (line 63),
    defined there and not used in that file today: change it with the others, or remove it if
    it stays unused.

## Evidence

All checks read the shipped files from the repository, at the head under test. No test prepares
a copy of a card.

1. **One new parametrized test** goes in `skills/chantier/scripts/cli/tests/test_plugin_files.py`,
   or beside the existing `SKILL.md` loop at its lines 382-392. It reads the shipped files:
   - `startup-core.md` holds the rule's load-bearing words. Check these by plain substring or
     regex on the shipped file: both modes or "any later call", "exact error", "stop", no seat,
     nothing written in the planning folder, the transient-network single retry, and the CLI
     excluded from the "work without it" case, and the "cannot run" scope (a launch failure only;
     a refusal, an error exit and a permission denial keep their handling). The Driver picks the exact phrases from its own
     wording and keeps the list short.
   - Each of the four `SKILL.md` files points every `$CHANTIER` failure, not only the sync, to
     `startup-core.md`.
   - Each file in the list above that holds a "work without it" or "is not a stop" sentence about
     a missing skill or tool also holds the exclusion clause. Parametrize over the file list and
     check the clause's fixed text.

   The test stays fast. `just test` stays within its budget in `AGENTS.md`.
2. **The startup budget:** `just test` passes `test_startup_manifest.py` on both hosts. The
   delivery quotes its `-s` output for the chief-of-staff, router, griller and status rows, before
   and after. If the limit rose, the three places hold the same new figure, at most 12544, and
   the PR names it and its reason.
3. `just check` green at the pushed head (Linux, macOS, Windows through CI).
4. **The long gate:** this is a change to the cards, so the pipeline's `just scenario
   (ubuntu-latest)` job must be green at the PR's head before the PR is ready (`AGENTS.md`). No
   new scenario step is added. The scenario runs the CLI with no model, so it cannot exercise a
   session that stops, and the cards' text is proved by item 1.
5. `just eval-dry-run` is not owed: nothing under `skills/chantier/scripts/cli/src/` or
   `evals/kit/` changes.
6. `just mod` is not owed: nothing under `hooks/` or `types/` changes.

No host and default matrix. The rule's text is the same on Claude Code and Copilot, in the dev
mode and the plugin mode, and depends on no configured value. The per-host byte measurement is
the existing test's own parametrization, not a matrix.

## Out of scope

- Any CLI code: no new command, no new refusal, no preflight line. P5 (`uv`, `git`) stays as it
  is.
- The agent files (`agents/*.md`, `com.github.copilot/agents/*.agent.md`). They already point to
  the startup core, and their bodies stay identical on both hosts.
- `startup-manifest.json`: no new entry. `startup-core.md` is already the common reading of every
  role. Only its `limit` field may change, under "The startup byte budget".
- How a parent handles a child's error reply. Its existing rules hold.
- A CLI refusal, a command's own error exit and a host's permission denial: their existing
  handling holds.
- Missing skills and tools other than the CLI. They keep their "warn, note, work without it"
  behaviour.

