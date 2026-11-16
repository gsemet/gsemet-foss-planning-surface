# Change Specification: PowerShell quoting of `gh --jq`, and the exact `--epoch` list

## Goal

From the retro of batch-13 (2026-11-12), two slips of the steering session (the Chief of Staff
steering a direct batch, on Windows PowerShell 5.1), fixed in the cards only:

1. `gh ... --jq '<expression with spaces>'` reached `gh` split ("accepts 1 arg(s), received 3")
   several times; printing `--json <fields>` plainly worked. The steering session is told so.
2. `order add --epoch 1` was refused by the CLI. The cards' list of the commands that carry
   `--epoch` reads as examples; it becomes the complete list, matching exactly what the CLI
   accepts, with "no other command" said.

The CLI is unchanged (02-answers.md).

## What the CLI accepts (origin/main d6271d4, read for this specification)

`skills/chantier/scripts/cli/src/chantier/cli.py`, `_parser()`: `--epoch` is declared
(`cmd(..., epoch=True)`) on `order`, `foreman`, `status`, `agents`, `take`, `cancel` and
`pause` only. Every other command (`round`, `handback`, `note`, `ship`, `gate`, `verdict`,
`release`, `stack`, `asks`, `open`, `close`, `cost`, `seat`, `board`, `log`, `handoff`, `rules`,
`playbook`) refuses it at parsing (exit 2). Within the seven, `commands.py` narrows it:

| Command | `--epoch` |
| --- | --- |
| `foreman set <id>` | required (the claim: must be the batch's epoch plus one) |
| `foreman transcript <uuid>` | checked (stale: exit 3) |
| `foreman get` | parsed, ignored: not to be listed |
| `status --refresh` | the wake: records the heartbeat, checked |
| `status --stop-heartbeat` | required, checked |
| `status` (plain) | parsed, ignored: not to be listed |
| `take`, `agents set`, `cancel`, `pause` | checked |
| `order done <O-k>` | checked |
| `order merged <cr>` | the Foreman's own merge, checked |
| `order add --fix-for <cr>` | the Foreman's own fix, checked |
| `order` of any other kind (`add` without `--fix-for`, `after`, `drop`, `note`, `rounds`, `slots`, `budget`, `qa`, `mode`, `approve`, `grant`, `confirm`) | refused, exit 2: "only `order merged` and `order add --fix-for` take --epoch" |

The complete list the cards give is therefore: `foreman set`, `foreman transcript`,
`status --refresh` (a wake), `status --stop-heartbeat`, `take`, `agents set`, `order done`,
`order merged`, `order add --fix-for`, `cancel`, `pause`.

## What changes

### 1. `skills/chantier/references/hosts/claude-code.md`, section "Configuration"

Add a subsection between "### Prerequisites" (after its closing paragraph "The last three rows
are not checked: ...") and "### Allow rules":

```markdown
### Windows PowerShell 5.1

On Windows PowerShell 5.1 (the PowerShell tool), a `gh` or `glab` argument that holds spaces or
double quotes, such as a `--jq` or `--template` expression, can reach the program split or
stripped of its quotes (`accepts 1 arg(s), received 3`): print `--json <fields>` alone and read
the JSON, or write the expression with no space and no double quote.
```

This is the host side of `concepts.md` rule 9 ("The host's side of this is in your host's
reference, section Configuration"); rule 9 itself is unchanged.

### 2. `skills/chantier/references/chief-of-staff.md`, "Steering a batch yourself", "Your epoch"

Replace the part of the bullet from "carry `--epoch <n>` on the loop's wakes" to "with no
epoch;" so it reads (the claim sentence before it and the heartbeat and pricing text after it
are unchanged):

```markdown
  <n>`. Carry `--epoch <n>` on exactly these commands and on no other: the claim (`foreman set`,
  `foreman transcript`), the loop's wakes (`status --refresh --epoch <n>`) and the recorded stop
  of your loop (`status --stop-heartbeat`), `take`, `agents set`, `order done`, `order merged`,
  `order add --fix-for`, `cancel` and `pause`. Any other command, or any other `order` kind
  (`order add` without `--fix-for`, `order note`, `order after`...), refuses it (exit 2). Never
  on the refresh before a report, which stays `status --refresh` with no epoch; arm the
```

### 3. `skills/chantier/references/foreman.md`, the epoch line of the start section

Replace:

```markdown
- Every `status --refresh`, `take`, `agents set`, `order done`, `order merged`, `cancel` and
  `pause` carries `--epoch <n>`; exit 3 means another Foreman owns the batch: stop at once.
```

with:

```markdown
- Exactly these commands carry `--epoch <n>`, and no other: `foreman set`, `foreman
  transcript`, `status --refresh` on a wake, `status --stop-heartbeat`, `take`, `agents set`,
  `order done`, `order merged`, `order add --fix-for`, `cancel` and `pause`. Any other command,
  or any other `order` kind, refuses it (exit 2); exit 3 means another Foreman owns the batch:
  stop at once.
```

### Not touched

- The CLI (`cli.py`, `commands.py`, `state.py`): its help already says `order` takes
  "merged --epoch, add --fix-for --epoch", and its refusal message names the two; no change.
- `hosts/copilot.md`: checked. Its "Configuration" only points to rule 9; it records no shell
  and no Copilot trial, and every line there is unproved. The slip was seen on Claude Code's
  PowerShell tool; adding it to Copilot would be a new, unproved Copilot finding. Unchanged.
- `concepts.md`, the agent files (`agents/`, `com.github.copilot/agents/`), `status-layout.md`,
  `session-start.md`, the docs: none lists the epoch commands.
- The scenario: it asserts no text of these card passages (checked: `run_scenario.py` reads
  `foreman.md` only for the suspect and proof-of-death strings). It already proves the CLI side:
  `order add` with `--epoch` and no `--fix-for` exits 2, with `--fix-for` it is accepted (the
  release-fix section), stale epochs exit 3.

## Out of scope

- A CLI change to accept `--epoch` everywhere, or to ignore it where it is refused.
- The Copilot reference (above).
- Any other PowerShell quoting advice (e.g. for `git` or `$CHANTIER` arguments).

## Evidence

- `just check` passes (Linux, macOS, Windows in CI).
- `just scenario` passes: a card change runs the long gate (AGENTS.md; 02-answers.md).
- The list matches the CLI, checked by the Driver in its worktree and named in the PR body:
  `$CHANTIER <cmd> --help` shows `--epoch` for `order`, `foreman`, `status`, `agents`, `take`,
  `cancel`, `pause`, and for none of the other commands; the eleven forms of the list are the
  ones the table above marks required or checked.
- `git grep -n -e "--epoch" -- skills/chantier/references/` shows no card telling a role to put
  `--epoch` on a command outside the list.
- The three edits are in the PR diff and nothing else in the cards changes; edited files stay
  UTF-8 without a byte-order mark.

## Decisions taken

- The PowerShell line names spaces **or double quotes**: Windows PowerShell 5.1's legacy native
  argument passing mangles embedded double quotes as well as splitting, and a `--jq` expression
  usually holds both; the advice (print `--json` plainly, or an expression with neither) covers
  both.
- It goes in its own short subsection of "Configuration" in `claude-code.md`, after
  "Prerequisites", rather than in "Allow rules" (which is about permissions).
- The epoch list includes `foreman set`, `foreman transcript` and `status --stop-heartbeat`,
  which the intent did not name: the brief asks for the list to match exactly what the CLI
  accepts, and the steering session runs all three. `foreman get` and plain `status` are left
  out: the CLI ignores `--epoch` there, so naming them would only invite noise.
- "Refuses it (exit 2)" is stated in both cards, so the steering session reads a refusal as its
  own slip, not as a stale epoch (exit 3).
- No new scenario step: the CLI's behaviour is already asserted; the change is card text,
  which the scenario does not test.
- Copilot reference unchanged (above).

No open question for the user.
