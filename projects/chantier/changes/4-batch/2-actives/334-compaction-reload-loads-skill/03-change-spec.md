# Change Specification: the automatic reload after a compaction loads the role's skill again

## Goal

After a compaction of a chantier session's main loop, the session calls its role's skill again
(with the argument `reload`) instead of reading only the short cores. Today the `session.compact`
hook adds a line that sends the model to `session-start.md`, "5. Reload"; the role's own
`SKILL.md` is never injected again, so the compacted session works from the summary's memory of
it. The new line names the session's role only, and tells the model to call its chantier skill
again with `reload`; the model finds the skill among its installed ones. A hook cannot call a tool;
the message is the strongest means it has.

Whichever chantier skill the model then calls, the reload lands on the right role: the role
skills and the router read the seat first and, when the seat says the session holds another role,
load that role's skill with `reload` (the user's answers to reload-Q1 and reload-Q2). Calling a
skill with `reload` treats the pane as any skill load does today: it goes back to its first page
(reload-Q4, which replaces reload-Q3).

## What changes

### 1. The hook (`hooks/register.tsx`)

- **`RELOAD_LINE` is replaced** by a function of the role, e.g. `reloadLine(role)`, building
  (the user's wording, 2026-11-17):

  - `chief-of-staff`: `You are the Chief of Staff in a chantier session; after this compaction, call your chantier skill again with the argument reload.`
  - `griller`: `You are the Griller in a chantier session; after this compaction, call your chantier skill again with the argument reload.`
  - `chantier` (the router, alone: no role yet): `You are in a chantier session; after this compaction, call your chantier skill again with the argument reload.`

  The line names no skill (no `chantier:chief-of-staff`, no slash command): the user's decision.
  It no longer names `session-start.md` nor asks for the "rules reloaded" line itself: the skill,
  called with `reload`, does that (section 2 below).

- **Which role: the last one loaded.** The `roles` atom (`plugin: 'chantier', key: 'roles'`,
  ~line 52) keeps the role skills in load order. Today `skill.prompt` (~line 709) appends a name
  only when absent, so a re-load does not move it. Change the update to move the name to the end
  (`[...list.filter(n => n !== name), name]`), so the last element is the last loaded (this also
  makes a reload that loads the other role's skill, section 2, the new last role). The value's
  shape (a list of strings) is unchanged: keep the tag `roles-1`. The hook picks the last element
  of the list that is not `chantier`; when none, `chantier`. One role per message, never a list.
  The atom can still name a role the session has left (a role change on the user's word, a fork:
  `session-start.md` ~105-121 and ~207-210 change the role with no skill load); the seat, read by
  the skill at the reload, corrects it (section 2).

- **`session.compact` (~line 722)**: conditions unchanged (main loop only: no `agentId`; trigger
  `manual` or `auto`; at least one role skill loaded; `result.skip` passed through; never vetoes).
  Only the message text changes: `reloadLine(<the role picked>)` in place of `RELOAD_LINE`. Update
  the comments at ~line 51, ~line 719 and the `roles` atom's doc in `types/index.d.ts` (~163) to
  say "the reload message" (only if `just mod` keeps `types/` as written; see Out of scope).

- **The pane on a reload: unchanged** (reload-Q4, the user's answer, replacing reload-Q3). The
  engine's `skill.prompt` event carries no argument, so the hook cannot tell a reload from a load;
  a pane skill called with `reload` opens the pane as today, back on its first page. The user
  accepts it. `skill.prompt` changes only by the roles update above.

- `PANE_SKILLS`, `ROLE_SKILLS` and what the pane draws are not touched. The pane screenshot rule
  of `AGENTS.md` covers a change to what the pane draws (its rendering, or the `STATUS.json`
  fields it shows); this change touches neither: no screenshot is due, and the PR's Known gaps
  does not name one.

### 2. The skills honour `reload`, and the reload follows the seat

- **`skills/chief-of-staff/SKILL.md`**: replace line 38 (`"chantier reload" follows
  session-start.md, "Reload".`) with:
  `With the argument reload, or on the words "chantier reload", follow session-start.md, "5.
  Reload", with $CHANTIER as this file defines it but no uv sync; nothing else of this file.`
  A `reload` first word does not set the session's mode (`foreman`/`direct`): the mode in force
  stays (the surface's when none was set). In the frontmatter `description`, after "a first word
  `foreman` or `direct` forces one", add "; the argument `reload` reloads its rules after a
  compaction".
- **`skills/griller/SKILL.md`**: replace lines 30-31 with the same sentence. Add to its
  `description`: "The argument `reload` reloads its rules after a compaction."
- **`skills/chantier/SKILL.md`** (the router), lines 30-31: replace with the same sentence, plus
  the delegation (reload-Q2): "In a session that holds a role (the reload message names the Chief
  of Staff or the Griller, or the seat names this session), load that role's skill with the
  argument `reload` by the host's means instead; with no role, ask no role." Its frontmatter
  `description` already names "chantier reload": unchanged.
- **No `uv sync` on a reload.** No card says so today (`session-start.md`, "5. Reload", is silent
  on it; the sync rule is "once, before the first `$CHANTIER` command" of the session): the
  sentence above is what rules it out, and "5. Reload" says it too (section 3).

### 3. The cards

- **`skills/chantier/references/session-start.md`, "5. Reload"** (~216-225):
  - **Trigger** becomes: "'chantier reload', the argument `reload` of the router, `chief-of-staff`
    or `griller`, or the host's automatic reload (which tells the session to call its chantier
    skill with `reload`). With no role, it starts the router."
  - **Does** opens with the seat (reload-Q1): "Read `$CHANTIER seat` first. The seat names this
    session: the role is the Chief of Staff. It names another session: the role is the Griller.
    The seat is free (none, or left by `seat leave`): the role is the Griller; take no seat. When that role is not the one of the skill called with
    `reload` (the role the reload message named, or the router's delegation), load the other
    role's skill with `reload` by the host's means, and that skill's reload goes on (it reads the
    seat, which agrees: one hop at most). The router with no role in the message and no seat
    naming this session reloads itself." Then, unchanged: ask no role question or introduction,
    make no batch change; read only (`$CHANTIER seat`, `$CHANTIER status`): no order, `take`,
    heartbeat, Driver, or message; add "no `uv sync`". A hop renames the session when its title
    no longer matches (section 3's rule, "whenever it changes"); it takes and leaves no seat.
  - **Says**: one line saying the rules were reloaded, plus the active batch's status, as today;
    with a free seat, the reload line also says the seat is free (the user may say "become chief of
    staff").
- **`skills/chantier/references/session-start.md` ~105-121, ~207-210** (role changes with no skill
  load): unchanged; the reload's seat reading above is what reconciles them.
- **`skills/chantier/references/hosts/claude-code.md`**:
  - **The skills row (line 26)**: add `/chantier:chief-of-staff reload` and
    `/chantier:griller reload` beside `/chantier:chantier reload`, and say the argument `reload`
    of the two role skills is **unproved** until seen; its trial is the one of "Reload after a
    compaction" (~491).
  - **"Reload after a compaction" (~478-494)**: the added message is now the role line ("You are
    the <role> in a chantier session; after this compaction, call your chantier skill again with
    the argument reload."; the router's line when no role), the role being the last role skill
    loaded; the skill then reads the seat and follows "5. Reload" (loading the other role's skill
    when the seat says so). The trial becomes: a Chief of
    Staff session, `/compact`, then the next
    turn calls a chantier skill with `reload` (Skill tool call visible: record which one the model
    picked, the role's or the router) and the answer opens with the reloaded line. Still **unproved** until seen. The manual reload line (~493) adds
    `/chantier:chief-of-staff reload` and `/chantier:griller reload`.
- **`skills/chantier/references/hosts/copilot.md`**: line 45, "or the argument `reload`" stays
  true for the three skills; reword to "the argument `reload` (router, `chief-of-staff`,
  `griller`)". "Reload after a compaction" (~92) unchanged (no mod on Copilot).

### 4. The docs

- **`README.md` line 278**: the left cell becomes `"chantier reload" (`/chantier:chantier
  reload`, `/chantier:chief-of-staff reload`, `/chantier:griller reload`)`; the right cell ends
  "on Claude Code the plugin also tells the session, at every compaction, to call its role skill
  again with `reload`".
- **`CONTRIBUTING.md` ~122, ~145**: they say "the automatic reload" / "the reload after a
  compaction", which stays true; no change unless a line describes the message's content (none
  does today).
- Release notes of past versions: not touched.

### 5. The tests (`hooks/register.test.tsx`, ~842-902)

- `RELOAD` (~851) becomes the expected lines; the test "a compaction of a session that loaded a
  role skill ends with the reload line" checks, for `chantier:chief-of-staff`, that the last
  message equals the Chief of Staff line, for `auto` and `manual`.
- Add one parametrized case for the choice of role: loads `chantier` then `griller` -> the Griller
  line; `griller` then `chief-of-staff` then `griller` -> the Griller line (move to end);
  `chantier` alone -> the router line. The last message names no skill (`not.toContain('chantier:')`).
- The three other compaction tests (no role, subagent, never vetoes) are unchanged.

## Out of scope

- The CLI (no change), what the pane draws, `STATUS.json`, `types/` beyond the `roles` doc comment
  (and only if `just mod` keeps it), Copilot's automatic reload (no mod there), the `status` skill
  (not a role), any batch behaviour.
- Loading a role's skill on a role change outside a reload (`session-start.md` ~105-121,
  ~207-210): unchanged.
- Running a slash command or a tool from the hook (impossible).

## Evidence

- `just mod` passes (a change to `hooks/`), run by the Driver before the PR.
- `just check` passes (includes the hook tests above).
- The pipeline's `just scenario (ubuntu-latest)` green at the PR's head (the cards change).
- Windows: the batch's top-of-stack local `just scenario` per `AGENTS.md`.
- Known gaps (the PR names them, so the ready line quotes them): the automatic reload is not seen
  in a real session; only the real-session trial of `claude-code.md` (~491) proves which skill the
  model calls on the message (the role's or the router) and that the seat hop and the router's
  delegation load the right one; the argument `reload` of `/chantier:chief-of-staff` and
  `/chantier:griller` is unproved until that trial.
