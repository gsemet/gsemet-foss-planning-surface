# Allow rules: the Chief of Staff asks to add the missing ones, and adds them on the user's yes

## Goal

When the user's Claude Code settings lack the allow rules chantier's agents need, the Chief of
Staff asks the user whether to add them, and adds them on the yes, instead of only showing a
block. When the host refuses that edit, the user gets one command line to run at the computer.
`init` runs every check a user's machine needs and, for each missing piece, asks and fixes it.
The recommended set loses the two release rules: a release's publication stays asked by the host,
by design.

Why (batch-17, 2026-11-13): preflight's P10 warned "14 of 16 commands … are not allowed" at the
batch's start; the warning was not put to the user as a question. The Drivers' force pushes after
each rebase (`git -C <worktree> push --force-with-lease …`) were then refused by auto mode's
classifier, went Driver → Foreman → Chief of Staff, and one Driver ran out while it waited.

## Ordering

This CR runs in batch-17 after CR-221 (python-inline-deps), and `depends.json` says so
(`{"after": ["python-inline-deps"]}`). CR-221 reworks the CLI's Python: PEP 723 dependencies, the
split of `commands.py` into modules, `ruff` and `mypy --strict` clean, files at most 400 lines,
functions at most 50 lines, and `tests/test_structure.py` split by subject. This change lands on
the reworked code and must meet the same targets. In CR-221's split:

- `_SAMPLES` (renamed `SAMPLES` once it is used from another module), `RECOMMENDED_ALLOW`,
  `rule_matches`, `_sample_groups` and `commands_not_allowed` live in
  `skills/chantier/scripts/cli/src/chantier/commands/permissions.py`;
- `preflight` (the P10 line) lives in `commands/preflight.py`;
- the P10 tests live in the test file CR-221 gives the preflight allow-rules smoke run (its
  example name is `tests/test_cli_runs.py`), and the block-versus-list test lives in the plugin
  files test (its example name is `tests/test_plugin_files.py`).

The line numbers and names below are today's (`commands.py` on `main`, commit `bfe527d`). The
Driver finds them again in the reworked modules.

## What changes

### 1. The CLI: the release commands leave P10 (answer 2)

`commands.py` today, lines 177–353:

- `_SAMPLES` (lines 185–211): remove the two release rows,
  `("gh-release", "gh release create v1.2.3 …", "gh release create*")` and
  `("glab-release", "glab release create v1.2.3 …", "glab release create*")`.
- `_sample_groups` (lines 280–311): remove the `gh-release` and `glab-release` groups
  (lines 301–304). They existed only to add the release rows. Once they are gone, the reading of
  the project's rules there (lines 292–300: `project_instructions`, `surface_instructions`,
  `_linked`) serves nothing else. Remove it too, and the function's `repo` argument if nothing
  else uses it. Update the docstring ("the publication when the project's rules name it" goes).
- `RECOMMENDED_ALLOW` (lines 214–215) is built from `_SAMPLES` and follows on its own. It loses
  `Bash(gh release create*)`, `PowerShell(gh release create*)`, `Bash(glab release create*)` and
  `PowerShell(glab release create*)`.
- The comment above `_SAMPLES` stays true: the order is still the order of the host card's table.
- The P10 line in `preflight` (lines 436–443) keeps its shape and its warn-only state. It still
  ends with `the block is in hosts/claude-code.md, "Allow rules"`. The Chief of Staff's question
  reads the rules from the `(add …)` parts the line already prints.

The counts after the change, with `SendMessage` counted as one: 14 commands on a GitHub project
without the `gh stack` extension and 15 with it. Before the change it was 16 when the project's
rules name `gh release create`, as chantier's own `CONTRIBUTING.md` does. A GitLab project has
12; a remote on neither forge has 18.

The CLI gets no new command and writes nothing new. The Chief of Staff edits the settings itself,
with its own tools: `AGENTS.md` keeps the CLI to the planning folder, and a new CLI tool comes
only from measured token cost.

### 2. `skills/chantier/references/hosts/claude-code.md`

- **"Configuration" (lines 111–112).** Replace "chantier never writes the user's settings:
  preflight's P10 compares, the user adds." with the named exception: "chantier writes the user's
  settings in one case only: on the user's yes, the Chief of Staff adds to
  `~/.claude/settings.json` the allow rules P10 named, and nothing else there. Preflight's P10
  compares; the Chief of Staff asks."
- **"Who reads it, when" (lines 118–120).** The Chief of Staff no longer "gives the user the
  block". It asks the question of `chief-of-staff.md` (section 4 below), and adds the rules on the
  yes. It gives the command line of "Allow rules to add" only when the host refuses the edit, or
  when the file cannot be read.
- **"Allow rules" table (lines 173–193).** Remove the rows `Bash(gh release create*)` (line 187)
  and `Bash(glab release create*)` (line 192). Under the table, next to the "There is no `gh api`
  rule" paragraph, add one sentence: there is no `gh release create` or `glab release create`
  rule, by design. A release is rare, public and irreversible. The Release driver already waits
  for `release go`, and the host's own check is a second guard at publication.
- **The JSON block (lines 201–245).** Remove its four release lines (229–230, 239–240). It must
  equal `RECOMMENDED_ALLOW` again (the test of section 7).
- **"Auto mode", the batch-15 item (lines 303–307).** This is history and stays. It still names
  `gh release create` among the refused commands.
- **"Allow rules to add" (lines 647–660), the "For you" block.** It becomes the fallback of
  answer 7. Its use: the Chief of Staff gives it when the host refused its edit of
  `~/.claude/settings.json` (typically under Remote Control, where auto mode's classifier may
  forbid it), or when that file cannot be read as JSON.
  - **Where:** at the computer running Claude Desktop, not on the phone, in the user's shell.
  - **Do:** run one command line.
  - **Paste:** that line. It merges exactly the rules P10 named into `permissions.allow` of
    `~/.claude/settings.json`. It creates the file and the keys when they are absent, keeps every
    other key and rule, adds no rule twice, and never replaces or removes anything. It writes
    valid JSON in UTF-8 with no byte-order mark.
  - **You should see:** at the next preflight, `P10 ok`, or a P10 line that no longer names them.

  The card holds the line as a template for each shell: Windows PowerShell 5.1, and a POSIX
  shell. Only the list of rules varies, and the Chief of Staff fills it in. The rules carry the
  project's remote name in place of `origin`, as P10 prints them. The Driver writes both templates
  and runs each once by hand: on a file that is absent, on a file with other keys, and on a file
  that already holds some of the rules. The block stays marked unproved until a user has followed
  it once. The pasteable JSON block of "Allow rules" stays as the reference list; it is no longer
  what the user is told to paste.
- The note "Whether a running session picks up a settings change is unproved" (line 656) stays,
  and the new text of the yes path repeats it (section 4).

### 3. `AGENTS.md` (line 11)

"chantier writes only in the planning folder (…), as plain JSON and Markdown, and a CR's cleaned
archive in its PR when the project asks for it, and fast-forwards a clean main checkout after a
merge it records" gains the exception, in those terms: "… and, on the user's yes, the Chief of
Staff adds to `~/.claude/settings.json` the allow rules preflight's P10 named, and nothing else
there". The same exception goes into the matching sentence of `CONTRIBUTING.md` (line 77) and
`docs/use-cases.md` (line 64), which repeat the rule.

### 4. `skills/chantier/references/chief-of-staff.md`

- **"The project", the P10 paragraph (lines 72–77).** Replace "For a P10 warn, give the 'For you'
  block 'Allow rules to add' of your host's reference with exactly the rules P10 named" with the
  question of answer 3, asked once per session:
  - **The question.** One question in the first message, after the P5/P10 lines: "add these rules
    to `~/.claude/settings.json`?" It lists each rule P10 named, with its risk taken from the
    "Risk accepted" column of the host card's table.
  - **On the yes.** Add exactly those rules to `permissions.allow`. Merge with what is there:
    never replace, never remove, add no duplicate. Create the file or the keys when absent, and
    keep the file valid JSON. Then run `$CHANTIER preflight` again and say what P10 says now. Add
    in one line that whether this running session picks up the change is unproved: a session or
    agent started afterwards reads it.
  - **On a no.** Say once what will be refused: a Driver's force push after a rebase goes Driver →
    Foreman → Chief of Staff, and an unattended batch waits at the first one. Do not ask again in
    the session.
  - **The host refuses the edit.** Say so with the refusal's exact text (concepts rule 7). Then
    give the command line of "Allow rules to add" for the user's shell, and say it needs the user
    at that computer, not on the phone. Try no other way: no other file, no other tool, no retry
    by another route.
  - **`~/.claude/settings.json` cannot be read** (P10 prints `unreadable: …`). Do not write it.
    Say so, and give the command line as for a refused edit, after the user has fixed the file.
  - Nothing else is written in any settings file: not the project's `.claude/settings.json` or
    `.claude/settings.local.json`, and no deny, ask or other key.
- **"Forge permissions (P9)", "What the user hears" (lines 345–355).**
  - "The missing host rules are exactly the ones P10 named" stays, now pointing to the question.
  - The "release's publication" line (lines 353–355) becomes: the release's publication, when the
    project's release procedure runs it, stays asked by the host, by design (no rule is
    recommended for it, and it is not a missing rule). When the account can publish, the Release
    driver runs the publication and the host asks or judges it. When the host refuses, "the
    publication is yours: you will be asked to run `<the command>`". The user is told now, not at
    the end.
  - "At step 1 the same check runs again; the plan's message repeats only what is still missing"
    stays.
- **"Starting a batch", step 1 (lines 363–367).** Replace "which warns and never fails: give the
  user the block for the rules it names, then go on" with: it warns and never fails. If the
  question was not asked yet in this session, ask it (as in "The project"), and act on the answer
  before the plan. If it was asked and the user said no, repeat in one line what is still missing,
  with no question. Then go on. P10 never blocks the go.

### 5. `skills/chantier/references/session-start.md`

- Line 31, "what the configuration checks add to the first message (P5, P9, P10), which goes in
  the same message": add that P10's warning comes as the Chief of Staff's question
  ([chief-of-staff](chief-of-staff.md), "The project").
- Section 4, the introduction's bullet "Zero configuration" (lines 145–148), "Everything chantier
  writes is Markdown and JSON in the planning folder": add "and, on your yes, the allow rules in
  your Claude Code settings".

### 6. `skills/chantier/references/init.md` (answer 8; in scope)

The tour's step 1 (lines 80–83) today explains the host's configuration only: "the user adds
them themself, like the `.gitignore` line. The tour writes nothing in the user's settings." It
changes. The tour runs every check a user's machine needs:

- preflight's P5 (`uv`, `git`) and P10 (the allow rules);
- P9 with the forge's rights and branch rules ("Forge permissions" of `chief-of-staff.md`);
- the long gate written in `AGENTS.md`.

For each missing piece it asks and fixes it:

- **The allow rules:** answer 3's question and write, and answer 7's command line when the edit
  is refused (section 4).
- **The long gate:** already proposed as exact `AGENTS.md` lines and written on the user's yes.
  That stays.
- **Missing tools and forge rights:** see the open points for what "fix" means there.

The sentence "The tour writes nothing in the user's settings" is replaced with: "The tour writes
in the user's settings only the allow rules P10 named, on the user's yes, as the Chief of Staff
does at a first turn." When the first turn already asked the P10 question in this session, the
tour does not ask it again. It says what P10 says now.

### 6b. `README.md`, "Install" (answer 9; in scope)

The section "Install" (lines 172–209) ends with one more step, after the paragraph on `uv`, `git`
and the forge's CLI: once after installing, open a session on the project and run
`/chief-of-staff init` (on Claude Code, `/chantier:chief-of-staff init`). Say in one or two
sentences what it checks and fixes:

- it checks `uv` and `git`, and the forge's CLI and its rights and branch rules;
- on Claude Code, it checks the allow rules and adds the missing ones on your yes (or gives you
  one command line to run at your computer);
- it checks the long gate in `AGENTS.md`, and writes the lines on your yes.

The "Use" table's row for "init", "I am new here" (line 217) adds "and the checks of your
machine, each missing piece asked and fixed". Its "five stage folders" is not this CR's to
correct.
### 7. The tests (in CR-221's split of `tests/test_structure.py`)

- `test_the_allow_rules_json_block_lists_exactly_what_preflight_checks` (line 380 today) keeps
  its shape. It passes once the block and the samples agree. Add one assertion: no rule of
  `RECOMMENDED_ALLOW` contains `release create`.
- `test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them` (line 391 today): add one
  assertion with the test's existing means. Give the test repository's `AGENTS.md` a line that
  names `gh release create`. Then `RECOMMENDED_ALLOW` in the settings gives `P10 ok`, and the
  warning line never names a release rule. No new test function is needed. The structure tests
  stay few (`AGENTS.md`).

### 8. What follows: the scenario and the docs

- `scenario/run_scenario.py` (lines 545–571) imports `RECOMMENDED_ALLOW` (from its new module
  after CR-221) and checks P10 warn, equivalence and P10 ok. These checks keep passing unchanged.
  Add one check to the same step: the P10 warning names no `release create` rule. The scenario
  cannot run the Chief of Staff's question: that is an agent's behaviour, proved in a real
  session (see "Evidence").
- `docs/tutorial-claude-code.md`:
  - lines 130–133, "the Chief of Staff gives you the allow rules to add … chantier never edits
    your settings itself", become: it asks you, and adds them to `~/.claude/settings.json` on your
    yes, or gives you one command line to run at your computer when the host refuses;
  - the troubleshooting item of lines 249–251 says the same.
- `skills/chantier/references/driver.md` (lines 558–564): the publication step "when the host
  allows it by its named rule ([claude-code], 'Allow rules')" becomes "when the host lets it
  through (no rule is recommended for it, by design: the host asks or its classifier judges)".
  The refusal path (`handback blocked approval: publish: <the exact command>`) is unchanged.
- No other doc quotes "16 commands"; the Driver greps for `16`, `release create` and "never
  writes the user's settings" / "never edits your settings" once more over `docs/`, `scenario/`,
  `README.md` and the cards, and updates what it finds.
- Both agent files of a role change only if their body names the release rule or the settings
  rule. Today none does. If one does, `agents/` and `com.github.copilot/agents/` change together,
  with identical bodies.

## Out of scope

- The eval kit: `evals/kit/setup.py`'s `allow_rules` writes a sandbox workspace's
  `.claude/settings.local.json` with a versioned `gh release create <tag> *` rule for unattended
  release campaigns. `evals/README.md` lines 157–160 describe it. Both stay as they are.
- The Copilot host: P10 runs on Claude Code only, so `hosts/copilot.md` is unchanged.
- Any rule outside P10's list. That covers `mcp__ccd_pr__set_monitor`, the `Edit(…/**)` rule,
  deny or ask rules, and the project's or local settings files.
- The user's own settings: already done (answer 5). On this repository, P10 says "1 of 16 not
  allowed" (`gh release create`) today, and will say `P10 ok` once this CR is merged.
- The `.gitignore` line of the tour: it stays explained only (see the open points).

## Evidence

- `just check` passes on Linux, macOS and Windows, with CR-221's lint and type targets (`ruff`,
  `mypy --strict`, files at most 400 lines, functions at most 50).
- `just scenario` passes (this change touches the CLI and the cards), with the added P10 check.
- By hand, on this repository after the merge, with the user's current settings:
  `$CHANTIER preflight` prints `P10 ok`.
- By hand, the two command-line templates of "Allow rules to add": each one run once on a scratch
  home folder, in the three cases of section 2. The result is valid JSON with no byte-order mark,
  read back by `preflight` as `P10 ok`. The outputs go in the PR's Deliverables.
- In a real session (the PR's Known gaps names it until it is done): a Chief of Staff on a
  settings file that lacks rules asks the question, writes on the yes, and reports P10 again. A
  refused edit (Remote Control) gives the command line.

## Open points (each with the default this specification takes)

1. **What `init` "fixes" for a missing tool or a forge right.** Default: chantier installs no
   tool and changes no forge setting. The tour asks, then gives the exact install command or
   forge change for the user to run. Only the allow rules and the long gate's `AGENTS.md` lines
   are written by chantier.
2. **The `.gitignore` line in `init`.** Default: unchanged, explained only. It is not a machine
   check, and it is a write in the project outside the planning folder.
3. **A Griller's first turn.** Default: a Griller does not ask or write. It reports the P10 line
   and says that the Chief of Staff asks.
4. **The command line's form.** Default: a template per shell in the host card's "Allow rules to
   add", with only the rules filled in by the Chief of Staff, and no new CLI command. The other
   option was a CLI command the user runs, which would put a settings write in the CLI.
5. **After a no, at a later batch's step 1 in the same session.** Default: one line naming what is
   still missing, with no question. A new session asks again.

## Decisions after the specification (they replace the open points they name)

The Chief of Staff with the user, 2026-11-13 (asked in French, recorded in English).

- **`init` installs the forge tools, on the user's yes** (the user: "init recommande d'installer gh
  si nécessaire, avec l'extension stack, essaye de faire les modifs, et s'il n'y arrive pas donne
  les commandes à l'utilisateur"). This replaces open point 1 for the tools: when the project's
  forge is GitHub and `gh` is missing or not logged in, or the `gh stack` extension
  (github/gh-stack) is not installed, `init` recommends it, says why (the stack driver then makes
  the stack on GitHub with it), asks, and on the yes runs the install itself with the platform's
  usual installer (for instance `winget install --id GitHub.cli` on Windows, `brew install gh` on
  macOS, the distribution's package on Linux; `gh extension install github/gh-stack`); `gh auth
  login` is interactive and stays the user's. The same for `glab` on a GitLab project (no stack
  extension). When an install is refused by the host or fails, it gives the user the exact
  commands to run at the computer, as for the allow rules (answer 7). It checks the result
  (`gh --version`, `gh extension list`) and says what it found. Forge settings (rights, branch
  rules) stay as open point 1 says: the exact change for the user to make.