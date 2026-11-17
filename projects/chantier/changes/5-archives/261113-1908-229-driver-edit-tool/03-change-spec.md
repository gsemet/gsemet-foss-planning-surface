# Change Specification: the CR Driver and the stack driver get the Edit tool

## Goal

From batch-16's retro (point 2), reviewed by an advisor: the CR-215 Driver had to rewrite its
whole PR body with Write to change part of it, because the `cr-driver` agent has no Edit. The user
agreed to give the Drivers their editing tools ("ok pour les outils d'edition"). The CR Driver and
the stack driver get Edit on Claude Code, as the Release driver already has, and the CR Driver's
card stops saying that the body is "always written with the Write tool", so that a Driver changes
part of `pr-body.md` with Edit, as [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md)
rule 9 already asks ("to change part of a file, edit it rather than rewrite it"; "written with the
host's Write tool (Edit to change it)").

## Decisions carried from `02-answers.md`

| Decision | Where this spec carries it |
| --- | --- |
| 1. The proposal as filed is the scope; points it does not settle take this spec's defaults, listed as open points | "What changes", "Open points" |
| 2. The CR joins the running batch-17 | "Order in batch-17" |
| 3. The Drivers get editing tools | "What changes", areas 1 and 2 |

## What was checked before writing (the request's "first confirm")

- **The write guard already holds Edit.** `hooks/register.tsx` judges `Write` and `Edit` on
  `file_path` and `NotebookEdit` on `notebook_path` (the field picker near line 587), and refuses
  a call outside the `writes:` folders with the same message for all three;
  `hooks/register.test.tsx` already covers Edit (the loops on `['Write', 'Edit', 'NotebookEdit']`
  near lines 875 and 886, and the empty-path pass near line 1022). The host reference
  (`skills/chantier/references/hosts/claude-code.md`, "The write guard") says the same. A CR
  Driver's Edit is therefore held to its `writes:` folders (its CR folder, and the archive path
  when `take` prints one) with no change to `hooks/`. **`hooks/` does not change, so `just mod`
  does not apply.**
- **The stack driver is not guarded** (the same host reference, "Not guarded": it gets no
  `writes:` line). Its Edit is unguarded exactly as its Write already is; this CR changes nothing
  there.
- **Copilot needs no change.** Copilot's `edit` tool covers both writing and editing a file, and
  every Driver on Copilot already lists it
  (`com.github.copilot/agents/chantier-cr-driver.agent.md` and
  `chantier-stack-driver.agent.md`: `tools: ["agent", "execute", "read", "edit", ...]`). The
  request's "add Edit on both hosts" is thus met on Copilot as it stands. The agent bodies, which
  `AGENTS.md` asks to keep identical across hosts, do not change: only the Claude Code
  frontmatter's `tools:` line does, and `test_structure.py` compares bodies, not tool lists
  (beyond the `Agent`/`agent` pair, which this CR does not touch).

## What changes

### 1. `agents/cr-driver.md` (Claude Code)

The frontmatter's `tools:` line gains `Edit`, placed as in `agents/release-driver.md` (after
`Read`):

```
tools: Agent, Bash, PowerShell, Read, Edit, Write, Grep, Glob, SendMessage, Monitor
```

Nothing else in the file changes.

### 2. `agents/stack-driver.md` (Claude Code)

The same:

```
tools: Agent, Bash, PowerShell, Read, Edit, Write, Grep, Glob, SendMessage, Monitor
```

Nothing else in the file changes.

### 3. `com.github.copilot/agents/` (Copilot)

No change (see "What was checked"). The PR says so in its description, so a reviewer does not
read the missing Copilot diff as a forgotten twin.

### 4. The card: `skills/chantier/references/driver.md`

The sentence in the "Push" bullet (near line 101):

> The body is always written with the Write tool and posted from that file, as in
> [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), rule 9, never as text in the command.

becomes, in substance:

> The body is a file written with the host's Write tool and changed with its Edit tool, and is
> posted from that file, as in [concepts](https://github.com/gsemet/chantier/blob/main/skills/chantier/references/concepts.md), rule 9, never as text in the command.

The rest of the bullet (the GitLab form, the audit read before each post) stays as it is. The
Driver word-smiths the exact sentence; the requirement is: Write to create, Edit to change part of
it, posted from the file, never typed in the command, and no wording that tells a Driver to
rewrite the whole file to change part of it.

### 5. Other places checked, unchanged

- `skills/chantier/references/concepts.md` rule 9 already says "Write tool (Edit to change it)".
- `skills/chantier/references/hosts/claude-code.md`, "The write guard", already names Edit.
- No card, doc or test lists a Driver's tools; nothing else names the Drivers' lack of Edit
  (searched: `no Edit`, `Write only`, `tools:` outside the agent files).

## Out of scope

- `hooks/` and its tests (already correct, see above); `just mod` therefore not run.
- The CLI (`skills/chantier/scripts/cli/`), including `tests/test_structure.py`: no new structure
  test is added (the project keeps those few; the frontmatter is read by the host).
- The Copilot agent files.
- Any role other than the CR Driver and the stack driver (see open point 1 on the QA driver).
- The plugin's version: agent files keep `# chantier-agent: 0.9.0`; no version is edited by hand.

## Order in batch-17

This CR touches no CLI code: not `commands.py`, not any module CR-221
(`.agents/changes/4-batch/2-actives/221-python-inline-deps/`) splits, not `test_structure.py`
(which CR-221 splits by subject). **It need not wait for CR-221**: no `depends.json`. CR-221's
own out-of-scope list excludes "any change to the cards, the agents, `hooks/`", so the two touch
disjoint files.

## Evidence

1. **E1, the diff:** exactly three files change: `agents/cr-driver.md` and
   `agents/stack-driver.md` (one `tools:` line each, `Edit` added) and
   `skills/chantier/references/driver.md` (the one sentence). `git diff --stat main` shows it.
2. **E2, `just check`** passes (the agent-file structure tests among it: same body on both hosts,
   frontmatter readable, no BOM).
3. **E3, `just scenario`** passes at the PR's head, as `AGENTS.md` asks for a change to the cards.
4. **E4, the guard holds a Driver's Edit:** `hooks/register.test.tsx`'s existing Edit cases pass
   in `just check` (no new test). In the PR, the Driver quotes those test names as the proof that
   an Edit outside the `writes:` folders is refused.
5. **E5, a real use (after merge, for the record):** a CR Driver of a later batch, started from
   the main checkout once this lands (or after `/reload-plugins`), changes part of its
   `pr-body.md` with Edit, and its Edit of a file outside its `writes:` folders is refused with
   the guard's message. Not provable in this CR's own PR, since its Driver runs the agent file
   from before the merge; the PR's Known gaps names it.

## Open points (default taken)

1. **The QA driver** (`agents/qa-driver.md`) also lacks Edit on Claude Code (it has Write) and
   also writes files it may change in part (its findings in a work folder). The request names
   only the CR and stack drivers. Default: **left out**, per answer 1 ("the proposal as filed");
   the Chief of Staff may offer it as an inbox item.
2. **Other roles with Write but no Edit** (Spec-writer, Investigator, Debugger, Verifier, Demo
   explorer). Default: **left out**, same reason.
3. **The Copilot side** is taken as already met by its `edit` tool. Default: **no Copilot change**;
   if the user wants the request's "both hosts" read as an explicit diff on Copilot too, there is
   nothing to add there.
