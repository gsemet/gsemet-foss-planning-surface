# Change Specification: claude-code-config

Recommend and check the Claude Code configuration chantier needs.

Sources: `intake/request.md` (the user's report of 2026-11-09: one week, 33 sessions, 575
subagents), `intake/doc-check.md` (what the official Claude Code docs confirmed on 2026-11-09),
`02-answers.md` (the grill of 2026-11-10). Base: v0.8.0 (`d670e24`).

## Goal

In the user's terms: fewer auto-mode interruptions, and long sessions that hold. chantier says
what to configure to run on Claude Code (the allow rules, each with the risk it accepts; what
must stay refused and why; compaction; the prerequisites), checks it at start next to its other
host checks, gives the user the exact JSON block to add, and never changes the user's settings
itself. Its own agents stop causing the errors seen that week: long chained commands, writes to a
file they have not read, leading assignments.

## Decisions carried from `02-answers.md`

| # | Decision (2026-11-10) | Where it lands below |
| --- | --- | --- |
| D1 | One CR. No new reference file: the configuration goes into the existing host reference `skills/chantier/references/hosts/claude-code.md`, filled in properly; `hosts/copilot.md` gets what applies to Copilot | Area 1, Area 2 |
| D2 | The CR makes sure the reference is read at the right moment by the roles that need it (the Chief of Staff, the Foreman and the Drivers read `hosts/<host>.md`; the workers read only their card and `concepts.md`) | Area 1 "Who reads it, when", Area 3, Area 5 |
| D3 | Push rule unchanged (`concepts.md` rule 8): a plain push when nothing is rewritten, `--force-with-lease` after a rebase; `git -C <worktree>` accepted. The reference recommends allow rules for both forms | Area 1 "Allow rules", Area 3 |
| D4 | The check runs at each batch's preflight, and once at the Chief of Staff's first turn (and in the `init` tour), with the JSON block to add | Area 4, Area 5, Area 6 |
| D5 | A missing allow rule warns and never fails preflight (chantier works with no setup); a missing tool the batch needs (git, gh or glab, uv) fails it | Area 4 |
| D6 | The command-hygiene rules (one command per call, read before overwrite, no leading assignment) go into `concepts.md`, read by every agent, workers included; the host reference keeps what is proper to Claude Code (allow rules, auto mode, compaction) | Area 3, Area 1 |
| D7 | The points the docs do not confirm are written as unverified, not settled | every Claude Code claim below carries its mark |
| D8 | (open questions, 2026-11-10) Add `glab mr create*` and `glab ci status*`, Bash and PowerShell, same risk text as `gh` | Area 1 "Allow rules", Area 4 |
| D9 | P10 also reads `.claude/settings.local.json`; not managed settings | Area 4, Area 1 "Allow rules to add" |
| D10 | Compaction: the documented facts plus the tutorial's values (`idleCompaction` on, `autoCompactWindow` 400000), marked as a recommendation, not a proved fact | Area 1 "Compacting" |
| D11 | Keep `git push -u origin chantier/*`; a remote not named `origin` is not covered, and the reference says so | Area 1 "Allow rules" |
| D12 | Which rules and tools P10 checks, and PowerShell vs Bash per OS: left to the Driver's judgment, this specification's choices as the default; the Verifier proves the result | Area 1 "Prerequisites" and "Allow rules", Area 4 |

## Marks

`claude-code.md` already marks each behaviour **proved**, **documented** or **unproved**. Use
them, mapped from `intake/doc-check.md`:

- doc-check "verified" → **documented**, with the page's link
  (`https://code.claude.com/docs/en/<page>`, the page doc-check names; open each link once and
  use the URL that resolves).
- doc-check "unverified", "not documented", "not explained by the docs" → **unproved**, with the
  words "not documented (checked 2026-11-09)" or "unverified" and the trial that would settle it.
  Never written as a fact, never as a recommendation the user can rely on.

## Area 1: `skills/chantier/references/hosts/claude-code.md`

### Sections this CR owns (to avoid a collision with `multi-session-chief-of-staff`)

The P1 `multi-session-chief-of-staff`, which since 2026-11-10 carries the former
`skill-entry-points` (merged by the user), also edits this file (its answer Q9: a remote or app session often
starts in a linked worktree; it writes that in the "Classes of session" part and the start
checks). This CR owns only:

1. a new section **`## Configuration`**, inserted after `## Heartbeat` and before
   `## Compacting`, with its subsections listed below;
2. the existing section **`## Compacting`**, rewritten;
3. a new subsection **`### Allow rules to add`** at the end of `## The "For you" block`, after
   `### \`/compact\``.

This CR does not touch the file's introduction, `## Tools`, `## Heartbeat`,
`## Classes of session`, `## A Foreman in a worktree asks`, `## Reusing the last Foreman` or the
existing "For you" subsections. If `multi-session-chief-of-staff` merges first, rebase onto it and keep its
text in those sections as it is.

### `## Configuration`

Opening paragraph: what the user configures so chantier runs on Claude Code with few
interruptions; chantier never writes the user's settings; preflight's P10 compares, the user
adds.

#### `### Who reads it, when`

- The Chief of Staff, at its first turn of a session and at each batch's preflight: it runs the
  check (P5, P9, P10) and gives the user the block of "Allow rules to add" for what is missing.
- The Foreman and the Drivers read this file with their card (their prompts already name it):
  "Auto mode" tells them what a refusal means and that it is reported, never worked around.
- The workers do not read this file; what they need (one command per call, read before you
  overwrite, no leading assignment, `git -C`) is in `concepts.md`, rule 9.

#### `### Prerequisites`

A table: tool, who needs it, how chantier checks it, and what happens when it is missing.

| Tool | Needed for | Checked by | Missing |
| --- | --- | --- | --- |
| `git` | every Driver, the CLI's reads | P5 (CLI) | preflight fails |
| `uv` | `$CHANTIER` (`uv run --script`) | P5 (CLI) | preflight fails |
| `gh` or `glab`, logged in to the remote's host | the Drivers' PRs and CI | P9 (the Chief of Staff: `gh auth status` / `glab auth status`) | preflight fails |
| `python` | none directly: `uv run --script` provides the interpreter | not checked | say so; on Windows a `python` that resolves to the Microsoft Store alias fails (seen 15 times in the user's week): the fix is the user's (App execution aliases), unproved as to which roles call `python` |
| `bash` | Claude Code's Bash tool on POSIX | not checked | unproved whether chantier needs it on Windows, where the PowerShell tool is used |
| `claude` | not a batch's need | not checked | seen missing from PATH 5 times in the user's week; no card calls it |

The last three rows are not checked: the default of D12, which the Driver may change on its judgment, saying why in the PR.

#### `### Allow rules`

How rules match (each line **documented**, link: permissions):

- `*` matches anywhere; `cmd *` (with a space) is a word boundary and also matches bare `cmd`.
- `Bash(git push …)` does not match `git -C <path> push …`: the `-C` form needs its own rule.
- `PowerShell(...)` rules have the Bash shape; aliases are canonicalized; matching is
  case-insensitive.
- A compound command passes only when every part is allowed (Bash: `&&`, `||`, `;`, `|`, `&`,
  newline; PowerShell: `|`, `;`, and `&&`, `||` from PowerShell 7).
- Bash: an allow rule does not match past a leading assignment (`X=1 cmd`), except known-safe
  environment variables; deny and ask rules do. PowerShell assignments (`$w='…'; cmd`):
  **unproved**, not documented (checked 2026-11-09).
- `mcp__<server>__<tool>` is an exact tool name; a bare tool name matches all its uses.
- `Edit(~/path/**)`: `~` is the home folder, `**` gitignore-style; an Edit rule covers Write and
  NotebookEdit (tools-reference).
- Settings precedence: managed > command line > local > project > user; deny > ask > allow; a
  user deny blocks a project allow (settings, permissions).

Then the recommended rules, one table row each: the rule, what chantier does with it (the card
and the command), the risk it accepts, its mark. The rows are exactly the list `P10` checks
(Area 4), in this order:

| Rule | chantier's use | Risk accepted | Mark |
| --- | --- | --- | --- |
| `Bash(git push --force-with-lease*)` and `PowerShell(…)` | a Driver's push after a rebase (`driver.md`, Push) | any `--force-with-lease` push, to any branch, and any flag after it | documented (rule form) |
| `Bash(git -C * push --force-with-lease*)` and `PowerShell(…)` | the same from outside the worktree, the form refused 4 times as "Git Destructive" | as above, in any repository the `-C` path names | documented (rule form) |
| `Bash(git push -u origin chantier/*)` and `PowerShell(…)` | a Driver's plain push (`driver.md`: `git push -u <remote> <branch>`, branches `chantier/<batch>/…`) | `*` matches any further text, so a flag added after the branch passes too; a remote not named `origin` is not covered | documented (rule form) |
| `Bash(git -C * push -u origin chantier/*)` and `PowerShell(…)` | the same with `git -C <worktree>` | as above | documented (rule form) |
| `Bash(uv run --script *chantier.py *)` and `PowerShell(…)` | every `$CHANTIER` command (`merge`, `ship`, `spawn`… were refused 5 times) | any script whose path ends in `chantier.py` | **unproved**: whether auto mode drops it as a "package-manager run command" is not documented (checked 2026-11-09); trial: enter auto mode with the rule set, run `$CHANTIER status`, see whether the classifier is asked |
| `Bash(gh pr create*)` and `PowerShell(…)` | a Driver opens its PR (refused once as "Git Destructive") | any PR on any repository `gh` can reach | documented (rule form) |
| `Bash(gh pr checks*)` and `PowerShell(…)` | a Driver reads its CI | read-only | documented (rule form) |
| `Bash(glab mr create*)` and `PowerShell(…)` | a Driver opens its MR on GitLab (`driver.md`: `glab mr create --draft`) | any MR on any project `glab` can reach | documented (rule form) |
| `Bash(glab ci status*)` and `PowerShell(…)` | a Driver reads its CI on GitLab (`glab ci status --live`) | read-only | documented (rule form) |
| `SendMessage` | the Foreman and the Drivers message each other (refused twice) | any message between this session's agents and sessions | **unproved**: `SendMessage` as a rule is not documented (absent from tools-reference, checked 2026-11-09); trial: set it, enter auto mode, have the Foreman message a Driver |

Below the table, the same rules as one JSON block, complete, ready to paste into the
`permissions.allow` array of `~/.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(git push --force-with-lease*)",
      "PowerShell(git push --force-with-lease*)",
      "...every rule of the table, in its order, Bash then PowerShell..."
    ]
  }
}
```

(The Driver writes the full list; a structure test compares it with the CLI's, Area 7.)

Then two rules the reference describes but P10 does not check (the default of D12):

- `mcp__ccd_pr__set_monitor`: Claude Desktop's PR monitor (auto-fix), refused twice in the
  user's week. No chantier card uses it. Risk: the session arms auto-fix on a PR. Rule form
  documented; the tool itself is Claude Desktop's, unproved here.
- `Edit(<the folder that holds the repository and its .worktrees>/**)` (the user's form:
  `Edit(~/Projets/**)`): lets agents edit in the CR worktrees next to the repository. Risk: every
  file below that folder. Not checked: the path is the user's.

What not to add, and why (**documented**, permission-modes, auto-mode-config): auto mode drops
on entry, and restores on leaving, broad rules: `Bash(*)`, `PowerShell(*)`, interpreter
wildcards, package-manager run commands (`PowerShell(uv run *)`), every `Agent` rule and every
`Monitor` rule. So no `Agent(chantier:cr-driver)` rule is recommended: starting a Driver in auto
mode stays the classifier's call (refused 3 times in the user's week). The `Agent(Name)` form
exists (documented); plugin agent names in it (`chantier:<role>`): **unproved**, not documented.

#### `### What stays refused`

No allow rule for these; when the host refuses or asks, the agent reports it (concepts rule 7),
and chantier does not do them unasked. Each with why (from the request's section 2):

- `git commit --amend --reset-author`: rewrites authorship.
- `git branch -D` with `git push origin --delete`, and `git update-ref -d`: delete refs; the
  Foreman's removal of a merged CR's branch and the Chief of Staff's of a dropped CR's (on the
  user's word) stay asked, not allowed.
- `Remove-Item -Recurse -Force` (or `rm -rf`) on `.claude`, or on temporary folders named by a
  wildcard (`claude-eval-*`, `chsmoke-*`): a pattern can reach what is not chantier's.

#### `### Auto mode`

- Allow, ask and deny matches resolve at once in auto mode, without the classifier, except
  protected paths, critical-path `rm`/`rmdir` and per-command domains (**documented**,
  permission-modes).
- The classifier label "Git Destructive" and `claude auto-mode defaults`, which lists the
  classifier's rules: **documented** (auto-mode-config). The labels "Merge Without Review" and
  "Create Public Surface", seen in the user's week: **unproved**, not documented.
- A refusal is reported with its exact text (concepts rule 7). A refused force push takes the
  route already written (`driver.md`, `foreman.md`: Driver → Foreman → Chief of Staff).

#### `### What the docs do not say`

One list, each **unproved**, "not documented (checked 2026-11-09)":

- `CLAUDE_CODE_ENTRYPOINT` and its values (`claude-desktop`): preflight P1 relies on it, and it
  holds in use; the env-vars page does not list it.
- The exact text "File has not been read yet". Documented: a Write to an existing file not read
  first fails on older models; newer models may overwrite under conditions (v2.1.228+)
  (tools-reference). Seen 177 times in the user's week, mostly from subagents.
- PowerShell assignments and allow rules; `SendMessage` as a rule; plugin names in `Agent(…)`;
  the auto-mode fate of `uv run --script *chantier.py *` (as above).

### `## Compacting` (rewritten)

Keep what is there (auto-compact on by default; `/autocompact` and `autoCompactWindow`; `/compact`
continues the conversation, `$CHANTIER cost` keeps the transcript, `/clear` may replace it; no
role runs it, the person types it) and add, each **documented** (settings-reference,
prompt-caching):

- `autoCompactWindow`: 100000 to 1000000; the default is tuned per model; capped at the model's
  context window.
- `idleCompaction`: default true; compacts after about an hour idle; Claude Code v2.1.290 and
  later.
- The prompt cache lasts 1 h on a subscription within plan usage, 5 min on an API key or a cloud
  provider; `promptCacheTtl` sets it. Why it matters: Chief of Staff and Foreman sessions last
  days (393 messages and 50 compactions in 45 h for one), with pauses past the cache's life.
- **Unproved**, not explained by the docs: sessions with `autoCompactWindow: 300000` compacting
  around 165 to 170k tokens (the user's week). Trial: one session, the setting read back with
  `/autocompact`, the token count at the first compaction recorded here.

Then a **recommendation** (D10), labelled as such, never as a proved fact: the values
`docs/tutorial-claude-code.md` already gives: keep `idleCompaction` on (its default), and set
`autoCompactWindow` to 400000 in `~/.claude/settings.json` for the Chief of Staff's and the
Foreman's sessions (the plugin's agents carry 200,000 in their files). Why: long sessions with
pauses past the cache's life. Whether 400000 holds given the unexplained 165-170k compaction above
is unproved: the same trial settles it. Give the JSON as the tutorial does:

```json
{ "idleCompaction": true, "autoCompactWindow": 400000 }
```

### `### Allow rules to add` (in "The \"For you\" block")

The block the Chief of Staff gives when P10 warns, in the four parts of that section:

- **Where:** the computer running Claude Desktop, the file `~/.claude/settings.json` (or the
  project's `.claude/settings.json`, which the team shares through git, or
  `.claude/settings.local.json`, the user's own in this project).
- **Do:** open the file; add the lines below to `permissions.allow` (create the key if absent);
  save; then start a new session. Whether a running session picks up a settings change is
  **unproved** (not in doc-check): the Driver checks the settings page and writes what it says,
  with its mark; if it says nothing, the block keeps "start a new session".
- **Paste:** only the missing rules P10 named, as JSON strings, in their table order, copied from
  "Allow rules"; complete, no placeholder.
- **You should see:** at the next preflight, `P10 ok`.

Mark it unproved until followed once by hand, like every "For you" block.

## Area 2: `skills/chantier/references/hosts/copilot.md`

Add a section **`## Configuration`** after `## Heartbeat`:

- Prerequisites: the same as Claude Code's for a batch: `git` and `uv` (P5), `gh` or `glab`
  logged in (P9). P10 does not run on Copilot.
- No permission configuration is recorded for Copilot: **unproved**; nothing is recommended
  until a Copilot trial records one.
- The command hygiene of `concepts.md` rule 9 applies on both hosts.

## Area 3: `skills/chantier/references/concepts.md`

- Rule 8 (Git): add one sentence: `git -C <worktree>` is accepted for any git command; the push
  rule is unchanged (plain when the remote branch is an ancestor, `--force-with-lease` after a
  rewrite).
- New rule 9, **Commands and files**, host-neutral (no tool name of `HOST_TOOLS` in the text,
  `tests/test_structure.py` checks it):
  - One command per call when you can. A chain (`a; b`, `a && b`, a pipe) passes the host's
    allow rules only if every part does, and a refused part stops the whole call.
  - No leading assignment before a command (`X=1 cmd`, `$w='…'; cmd`): write the value into the
    command itself; an allow rule does not see past it.
  - Read a file before you overwrite it; to change part of a file, edit it rather than rewrite it.
  - Where to read the host's side: your host's reference, section "Configuration" (the workers
    do not need it).

## Area 4: the CLI, `skills/chantier/scripts/cli/src/chantier/commands.py` (`preflight`)

`preflight` stays one command, all or nothing on its FAIL lines; it gains one non-failing line.

- **P5** now checks `git` as well as `uv` (`shutil.which`): good text `chantier <v>, uv and git
  found`; bad text names each missing tool and the versions as today. Missing `git` fails (D5).
- **P10** (new; Claude Code host only, `host == "claude"`; no line on Copilot):
  - A constant `RECOMMENDED_ALLOW` (tuple of strings) in `commands.py`, in the table's order of
    Area 1: the Bash and PowerShell form of each command rule (`glab` included), then
    `SendMessage`.
  - On POSIX (`os.name != "nt"`) only the `Bash(…)` rules and `SendMessage` are compared; on
    Windows all of them (the default of D12).
  - It reads `permissions.allow` from `Path.home() / ".claude" / "settings.json"`, from
    `<repo root>/.claude/settings.json` and from `<repo root>/.claude/settings.local.json` (D9;
    not managed settings), UTF-8, `json.loads`; a file absent is an empty list; a file
    unreadable or malformed is named in the line, never an error exit.
  - A rule counts as present only when its exact string is in one of the three lists. It does not evaluate
    wildcards: the line says "not found as written", so a user whose broader rule covers it knows.
  - All present: `P10 ok   the recommended allow rules are in your settings`.
  - Some missing: `P10 warn <k> of <n> recommended allow rules not found as written in your
    settings (~/.claude/settings.json, .claude/settings.json, .claude/settings.local.json): <rule>,
    <rule>, …; the block is in hosts/claude-code.md, "Allow rules"`. One line.
  - A `warn` never changes the exit code nor the verdict line (D5).
  - It writes nothing, anywhere.
- The `check` helper gains the third state `warn` (same width as `ok  ` and `FAIL`).
- The line `P2, P3, P9 and 'not unattended' are the Chief of Staff's own checks` is unchanged.
- Output stays within ten lines (P1, P4, P5, P6, P7, P8, P10, the own-checks line, the verdict;
  P6 twice only when no repository is found, where P10 still runs on the home file alone).
- `skills/chantier/scripts/cli/src/chantier/cli.py`: the help of `preflight` becomes "check P1,
  P4–P8 and P10; exit 2 if any fails (P10 only warns)".
- No new command, no new dependency; portable (POSIX and Windows, UTF-8).

## Area 5: `skills/chantier/references/chief-of-staff.md`

- `## The project` (start of each session), after the `$CHANTIER rules` sentence: once per
  session, at your first turn, run `$CHANTIER preflight` and P9's check; tell the user only what
  P5, P9 and P10 say (the other conditions are a batch's, and `multi-session-chief-of-staff` owns what is
  said about P6 and P7 at start); for a P10 warn give the "For you" block "Allow rules to add" of
  your host's reference with the missing rules; a missing tool is said with what to install.
  Nothing blocks the user's request there. Do not touch `SKILL.md`'s "First turn"
  (`multi-session-chief-of-staff` rewrites it); if that CR has merged and holds a start check, put this
  report in the same first message.
- `## Starting a batch`, step 1: P5 now names `uv` and `git`; add "P10 (Claude Code: the
  recommended allow rules) warns and never fails: give the user the block for the missing rules,
  then go on".

## Area 6: `skills/chantier/references/init.md`

- Step 5, "Getting started here": add one item: the host's configuration, from preflight's P5
  and P10 and P9: the missing tools, and the "Allow rules to add" block for the missing rules,
  explained only; the user adds them themself, like the `.gitignore` line. The tour writes
  nothing in the user's settings.
- Step 1, the exit-2 explanation: add `git` to what chantier needs (it is there implicitly; name
  it).

## Area 7: tests, scenario, docs

- `skills/chantier/scripts/cli/tests/test_structure.py` (few and fast):
  - one new test: the JSON block under "Allow rules" in `hosts/claude-code.md`, parsed, lists
    exactly `commands.RECOMMENDED_ALLOW`, in order;
  - extend `test_a_foreman_batch_takes_added_work_and_a_direct_preflight_leaves_out_p2` (or one
    new test) with `HOME` and `USERPROFILE` set to a temporary folder: with no settings file,
    `preflight` prints a `P10 warn` line and still exits 0; with a `.claude/settings.json` that
    holds every rule, `P10 ok`; a rule found only in `.claude/settings.local.json` counts; on
    `CHANTIER_HOST=copilot`, no P10 line.
  - `conftest.py`: tests that run `preflight` must not read the developer's own home: point
    `HOME` and `USERPROFILE` at a temporary folder in the `chantier` fixture or in the test.
- `scenario/run_scenario.py`, "## 1. Setup and preflight": two checks: preflight on Claude
  Desktop with no settings prints `P10 warn`, names a missing rule and still passes; with the
  rules written in a temporary home's `.claude/settings.json`, `P10 ok`. Update
  `scenario/README.md`'s list to match.
- `docs/tutorial-claude-code.md`: section 5, the preflight list gains `git` and "the allow rules
  it recommends (a warning only)"; a short paragraph points to the host reference's
  "Configuration" for fewer auto-mode interruptions; "If something goes wrong" gains one line: a
  classifier refusal of a chantier command → the allow rules of that section.
- No version edit (`just version` is the release's).

## Out of scope

- chantier never writes the user's settings (`~/.claude/settings.json`, `.claude/settings*.json`).
- No new CLI command; no wildcard evaluation of the user's rules.
- No allow rule for `Agent`, nor for the commands of "What stays refused".
- The start checks of a session in a linked worktree (P6, P7 at start, moving to the main
  checkout): `multi-session-chief-of-staff`.
- `SKILL.md`'s "First turn" and entry-points table: `multi-session-chief-of-staff`.
- Copilot permission configuration: nothing is recorded until a trial.
- Changing the agents' files (`agents/`, `com.github.copilot/agents/`): their bodies are unchanged;
  the cards carry the contract.

## Evidence

- `just check` passes (Linux, macOS, Windows): the structure tests above, links resolve, cards
  hold no host tool.
- `just scenario` passes (a CLI change): the two new P10 checks and the existing preflight checks.
- At the pushed head, in this repository on Windows: `uv run --script
  skills/chantier/scripts/cli/chantier.py preflight` with the user's real settings prints a P10
  line (ok or warn naming the missing rules) and its exit code is unchanged by it; the output is
  kept as evidence.
- A reader check: every row of "Allow rules" and every claim of "Configuration" and
  "Compacting" carries a mark; each "unproved" names its trial or says "not documented (checked
  2026-11-09)"; each doc-check row appears with the same verdict.

