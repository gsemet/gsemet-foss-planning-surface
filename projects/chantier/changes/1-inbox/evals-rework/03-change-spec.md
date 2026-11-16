# Change specification: rework the eval campaigns

## Goal

The eval campaigns get names that say their host, the Copilot campaigns are ready for the user to
launch in the Copilot app, and the reports in `evals/results/` list in the order the runs
happened. On the way, the evals' docs lose what is wrong today: campaign lists written by hand that
disagree, steps that are Claude Desktop's only but do not say so, and old report names that the new
names would make misleading.

| Today | After |
| --- | --- |
| `full` | `claude-full` |
| `real-foreman` | `claude-real-foreman` |
| `real-direct` | `claude-real-direct` |
| `copilot` (1 CR, 1 slot, $3) | removed; replaced by `copilot-real-foreman` and `copilot-real-direct` |
| `ticket-summary` | removed, with its kit |
| `claude-planted` | unchanged |

The published release notes (`docs/release-notes/2026-11-13-v0.9.0/`,
`docs/release-notes/2026-11-15-v0.10.0/`) are history and keep the old names.

## Decisions carried (from `02-answers.md`)

- **D1 (Chief of Staff).** The claims files move to `evals/results/claims/`, apart from the run
  reports.
- **D2 (Chief of Staff).** `evals/README.md` names the campaigns in one table. Every other place
  points to that table instead of listing the campaigns again.
- **D3 (Chief of Staff).** Each host-specific step of the README names its host: Claude Desktop or
  the Copilot app.
- **D4 (Chief of Staff).** The published release notes (v0.9.0, v0.10.0) keep the old names.
- **Q1.** Every report is renamed date first, under the campaign it really ran; the README's "Past
  reports keep their names" paragraph goes.
- **Q2.** The time in a report's name is UTC, the zone of the times written inside the reports; the
  README says so.
- **Q3.** The GitHub ticket-summary rule stays in `chief-of-staff.md`, marked unproved with no trial
  planned. The `ticket-summary` kit goes with the campaign: `evals/kit/ticket-summary/`, its setup
  case, its dry-run case and its check in `test_cli_units.py`.
- **Q4.** `claude-full` runs before a minor or major release; a patch release needs only the quick
  campaigns. This changes `evals/README.md`, `CONTRIBUTING.md` and `docs/release-process.md`.
- **Q5.** `copilot-real-foreman` and `copilot-real-direct` each get their runbook, their setup
  entry and prompt line, their dry-run case, and the Copilot prerequisites in the README. The audit
  checks what every host shares: the run, the judge and the cost. The Copilot-specific checks are
  written after the user's first real run, from its logs, and the runbooks say so. The old
  `copilot` campaign goes.
- **Q6.** Done means `just check` and `just eval-dry-run` pass, and no old campaign name is left
  anywhere except the published release notes (see "Evidence", E3, for the exact search).
- **A7 (Chief of Staff, 2026-11-16).** The ask-only report becomes
  `2026-11-04-19-11-claude-planted-ask-only.md`, its time read from its transcripts. Q1's example
  (`2026-11-03-22-17-...`) used another report's time by mistake.
- **A8 (Chief of Staff, 2026-11-16).** A report that gives no start time takes it from the run's
  records: the batch's `open` in the transcripts. When no record gives it for sure, the name uses
  the time, in UTC, of the commit that added the report, and the PR says so, report by report.
- **A9 (Chief of Staff, 2026-11-16).** The `-smoke` qualifier stays after the campaign:
  `...-claude-planted-smoke.md`.

## What changes

### 1. Runbook folders (`evals/`)

Move with `git mv` so history follows; `setup.prompt_line` builds the runbook path as
`evals/<campaign>/RUNBOOK.md`, so the folder name must equal the campaign name.

| Today | After |
| --- | --- |
| `evals/full/RUNBOOK.md` | `evals/claude-full/RUNBOOK.md` |
| `evals/real-foreman/RUNBOOK.md` | `evals/claude-real-foreman/RUNBOOK.md` |
| `evals/real-direct/RUNBOOK.md` | `evals/claude-real-direct/RUNBOOK.md` |
| `evals/copilot/RUNBOOK.md` | deleted |
| `evals/ticket-summary/RUNBOOK.md` | deleted |
| (none) | `evals/copilot-real-foreman/RUNBOOK.md`, new |
| (none) | `evals/copilot-real-direct/RUNBOOK.md`, new |

In the three Claude runbooks: every old name becomes its new one (titles, the setup line, the prompt
in its `text` block, links between runbooks such as `../real-foreman/RUNBOOK.md`, the report path,
"as `full` and real-foreman say (J15)", "They are the only human steps a `full` run may have"). The
report path each names follows the new rule (section 3, "Report names"):
`results/<YYYY-MM-DD-HH-MM>-claude-full-run<n>.md`, and the same for the quick ones.
`claude-real-foreman`'s "Cost and time" row links the renamed run 2 report.

`evals/claude-planted/RUNBOOK.md`: line 36 links the renamed runbooks; line 119's report path
`results/claude-planted-<date>.md` becomes `results/<YYYY-MM-DD-HH-MM>-claude-planted.md`.

### 2. The two Copilot runbooks (new)

Both are the Copilot counterparts of `claude-real-foreman` and `claude-real-direct`: the same 5
frozen CRs (`QUICK` in `setup.py`: `delete-item`, `edit-item`, `status-filter`, `json-api`,
`stats-page`), no release, the mode chosen at launch (`stack`, `parallel` or `series`), 3 slots, a
$20 budget, the raise on a first `budget:` ask to $30. They follow the sandbox campaign text of the
README, as the Claude quick runbooks do, and differ where the host differs. Each holds:

- **What it covers.** `copilot-real-foreman`: a Foreman started with `create_session`, the
  heartbeat as `/every`, armed by the Chief of Staff in the Foreman's chat on its `ready <batch>`
  (`hosts/copilot.md`, "Heartbeat"), the Drivers in the background (`task`), the cost through
  `copilot-session-usage`. `copilot-real-direct`: the Chief of Staff alone, no Foreman, its own
  `/every` (`hosts/copilot.md`: unproved).
- **The table.** Setup: `uv run --no-project python evals/kit/setup.py copilot-real-foreman
  <workspace>` (after `sandbox.py reset --yes`); CRs; Open (the line setup prints, with `--mode
  <mode>`, and `--direct` for `copilot-real-direct`); Mode; Team (the plugin's Copilot agents).
- **Start.** A new chat of the Copilot app opened on the workspace, with the `prompt` line setup
  printed last. Prompt templates (plain text, the form today's `copilot` runbook uses, since how
  Copilot passes the skill's `foreman` or `direct` argument is unproved, `hosts/copilot.md`, "The
  skills"; the mode is the user's word, which `chief-of-staff.md`, "Starting a batch", takes):
  - `Run the chantier eval campaign copilot-real-foreman in <stack|parallel|series> mode, with a Foreman: follow <this checkout>/evals/copilot-real-foreman/RUNBOOK.md.`
  - `Run the chantier eval campaign copilot-real-direct in <stack|parallel|series> mode, in direct mode: follow <this checkout>/evals/copilot-real-direct/RUNBOOK.md.`

  Marked **unproved** until the campaign's first run; its report says what the app did.
- **The user's turns.** The go; each `ask ready`: `sandbox.py merge <n>` from the workspace, alone,
  then `$CHANTIER order merged CR-<n>` and its line (direct: the Chief of Staff's own `order merged
  --epoch` and fast-forward, as in `claude-real-direct`); a question, a stuck CR, a `budget:` ask as
  the README says; `final`: the audit, the cost, `close --yes`. **The real user's step:** deleting
  the `/every` (Foreman: in the Foreman's chat; direct: in the Chief of Staff's chat), each time
  the Chief of Staff says to (at the pause, when the Foreman ends its heartbeat, and at the end),
  since neither the Foreman nor the Chief of Staff can end `/every` (`hosts/copilot.md`,
  "Heartbeat", lines 47-48). The runbook names it as the one step that waits on the real user. No
  Auto-fix step and no `mcp__ccd_pr__set_monitor`: they are Claude Desktop's. No 10-message limit:
  it is Claude Desktop's; Copilot's own limits are not recorded, and a refused send is reported as
  a finding.
- **Expected.** Every CR `merged` (or `cancelled`, with its reason); the judge `pass` on every
  merged CR and on `main`; at least one heartbeat in the event log; `chantier cost` prints a
  breakdown with an `Agent <type>` line per agent type. For `copilot-real-direct`, the steering
  share is `not measured`: the CLI does not price the Chief of Staff's session on Copilot
  (`chief_line` in `commands/cost/sessions.py`).
- **The audit.** `audit.py <workspace> --sandbox` before `close --yes`. On Copilot it checks only
  what every host shares (the run, the batch's events and ending, the forge, the judge, the cost),
  with no rail ids and no scorecard. A section "Still to write from the first real run" says: the
  Copilot-specific checks (roles, prompts and tools, from the host's logs) are written after the
  user's first real run, from its logs.
- **The report.** `results/<YYYY-MM-DD-HH-MM>-copilot-real-foreman-run<n>.md` (or `-direct-`), in a
  worktree on its own branch with its PR; the cost read after `close --yes` from the closed batch's
  record; no scorecard section, the audit's checks and judge pasted instead.

### 3. `evals/README.md`

- **One campaigns table (D2).** The table under "Campaigns" gains a `Host` column (Claude Desktop
  or the Copilot app) and lists the six campaigns: `claude-full`, `claude-real-foreman`,
  `claude-real-direct`, `claude-planted`, `copilot-real-foreman`, `copilot-real-direct`. The
  `ticket-summary` and `copilot` rows go. The two Copilot rows: cost "budget $20; measured by the
  first run", last run "not run yet". `claude-planted`'s last-run link points to the renamed
  report. Every other list of campaigns becomes a pointer to this table ("the sandbox campaigns of
  the [table](#campaigns)"): the intro (line 6), "Run a campaign" (line 64), "A sandbox campaign"
  ("the five sandbox campaigns", line 69), the Auto-fix line of "Before you start" (line 213), the
  kit table's rows, and the root `README.md` (lines 315-316).
- **Host-specific steps (D3).** Each one names its host: in Prerequisites, Claude Desktop's items
  (the app at the desk and its trust step; Auto-fix and auto-archive off) are marked "On Claude
  Desktop", and a new "On the Copilot app" group holds the Copilot prerequisites: the Copilot app;
  the chantier plugin installed from this checkout (`copilot plugin marketplace add <this
  checkout>`, then `copilot plugin install chantier@chantier`, unproved from a local checkout until
  the first run); `uv` able to fetch `copilot-session-usage` once for the cost. "The operator",
  "Auto-fix during the run", the `.claude/settings.local.json` paragraph and "The host's limits"
  (already Claude Desktop's by its first line) each say which host they hold for; the Copilot
  operator's line points to the Copilot runbooks. In "The operator" (line 129), "Nothing waits on
  the real user" is marked Claude Desktop's; on the Copilot app, deleting the `/every` is the real
  user's step, as each Copilot runbook says (section 2, "The user's turns"). "Copilot's report
  stays as it is" (intro) and "Copilot's audit has no rail ids and no scorecard yet" become: a
  Copilot campaign's report has no scorecard until the audit's Copilot checks exist.
- **Ticket summary.** Every mention goes: the intro, step 4 of "Preparation" (the `ticket-summary`
  sentence), setup's step (lines 106-107), the settings paragraph ("not for `ticket-summary`"), the
  kit table's `setup.py` row (its `ticket-summary` sentence) and the `kit/ticket-summary/` row, the
  dry-run row's `ticket-summary` setup case.
- **Report names (Q1, Q2, A7-A9).** The paragraph "Past reports keep their names..." (lines 50-52)
  goes. In its place: a report is `results/<YYYY-MM-DD-HH-MM>-<campaign>.md`, and
  `results/<YYYY-MM-DD-HH-MM>-<campaign>-run<n>.md` for a sandbox campaign; the date and time are
  when the batch opened (its `open`), **in UTC**, the zone of the times written inside the reports;
  an older report kept a qualifier of its old name after the campaign (`-ask-only`, `-smoke`,
  `-v0-5-0`). One sentence adds: the PR prefix's date is setup's local date
  (`datetime.date.today()` in `setup.py`), while the report's name is the `open` time in UTC, so
  the two dates can differ around midnight. The same rule replaces the paths in "The report" of "A
  sandbox campaign" (line 182), step 6 of "The steps" (line 274) and the runbooks. The prefix
  example (line 110) becomes `[eval 4 2026-11-14 claude-full]`. The workspace examples
  `../chantier-eval/<campaign>-<date>` (lines 98, 250) are workspace folders, not reports, and stay.
- **Which campaign (Q4).** "a role or flow change runs one quick campaign (`claude-real-foreman`
  or `claude-real-direct`) in the mode the change touched. Before a minor or major release,
  `claude-full` with both quick Claude campaigns, in the modes the release's claims file names; a
  patch release needs only the quick campaigns. `claude-planted` after a change to how a batch
  handles failures. A change to Copilot's mechanics: `copilot-real-foreman` or
  `copilot-real-direct`, which the user runs in the Copilot app." The sentence "`full` goes past
  [the 10-message limit]" names `claude-full`.
- **Claims (D1).** "Before a release: the claims" names `evals/results/claims/claims-vX.Y.Z.md`;
  the report template's "Claims" section keeps the file name `claims-vX.Y.Z.md`.
- **The kit table.** The `dry_run.py` row lists the new case `copilot-setup` (section 6) and drops
  the `ticket-summary` one.

### 4. `evals/results/`: renames (Q1, Q2, A7-A9) and claims (D1)

All with `git mv`. Each report's title line (`# real-foreman, 2026-11-15, run 2`) and its mentions
of a campaign take the campaign it really ran, by its new name; the figures and findings are left
as written.

| Today | After | Start time, and where it is read |
| --- | --- | --- |
| `claude-full-2026-11-03.md` | `2026-11-03-14-06-claude-planted.md` | the report: "14:06 to 16:07 UTC" |
| `claude-full-2026-11-04.md` | `2026-11-03-22-17-claude-planted.md` | the report: "22:17 UTC on 2026-11-03" |
| `claude-full-2026-11-04-ask-only.md` | `2026-11-04-19-11-claude-planted-ask-only.md` | its transcripts (A7) |
| `claude-smoke-2026-11-04.md` | `2026-11-04-<HH-MM>-claude-planted-smoke.md` | A8: the batch's `open` in the transcripts of the `chantier-eval-smoke*` workspaces under `~/.claude/projects/`, else the commit that added the report |
| `real-2026-11-05.md` (two batches, `eval-real` and `eval-heavy`, on this repository) | `2026-11-05-<HH-MM>-claude-real-foreman.md` (the first batch's `open`) | A8: the `open` in this repository's own transcripts under `~/.claude/projects/`, else the commit that added the report |
| `real-2026-11-05-v0-5-0.md` | `2026-11-05-<HH-MM>-claude-real-foreman-v0-5-0.md` | A8, as above |
| `real-foreman-2026-11-12.md` | `2026-11-12-23-17-claude-real-foreman.md` | the report: `open` at 23:17:15 UTC |
| `real-direct-2026-11-12-run1.md` | `2026-11-12-19-41-claude-real-direct-run1.md` | the report: "about 19:41 UTC" |
| `real-foreman-2026-11-15-run2.md` | `2026-11-15-10-51-claude-real-foreman-run2.md` | the report: opened at 10:51:59 UTC |
| `real-direct-2026-11-15-run3.md` | `2026-11-15-12-43-claude-real-direct-run3.md` | the report: opened at 12:43:06 UTC |
| `claims-v0.10.0.md` | `claims/claims-v0.10.0.md` | n/a |

For each A8 row, the PR body says where its time came from: the transcript file and line of the
`open`, or "the commit that added the report, <SHA>, at <time> UTC: no record gives the `open` for
sure".

**`claude-full` inside the renamed pre-sandbox reports.** Before the sandbox campaigns, `claude-full`
was the old name of today's `claude-planted` campaign. In the four reports renamed to
`claude-planted` and in the two 11-05 reports, a `claude-full` that means that old campaign becomes
`claude-planted` (for example `real-2026-11-05-v0-5-0.md` line 57, "which only `claude-full`
..."). Since `claude-full` is also a new name, no search can tell the two apart: the Driver reviews
each `claude-full` of these six reports by hand, and the PR body names that review, with the
lines changed and those kept.

Every link to a renamed report follows: `evals/README.md` (campaigns table), the
`claude-real-foreman` runbook, `claims/claims-v0.10.0.md` (its "Runs:" line and its Evidence
column; its "Can come up in" column takes the new campaign names, the bare `full` included; line
5's "No `full` campaign" becomes `claude-full`). The links from `claims/` to a report gain `../`.

### 5. `evals/kit/setup.py`

- `CAMPAIGNS`: `full`, `real-foreman`, `real-direct` renamed to `claude-full`,
  `claude-real-foreman`, `claude-real-direct`, with their prompts' campaign word and runbook path;
  `copilot` and `ticket-summary` removed; two entries added:
  - `copilot-real-foreman`: `host: "copilot"`, `mode: "choose"`, the prompt of section 2, one batch
    `{"crs": QUICK, "added": [], "slots": 3, "budget": 20}`;
  - `copilot-real-direct`: the same, its prompt of section 2, and `"direct": True` in its batch.
- The `ticket-summary` code goes: `issue_lines`, the `spec.get("issue")` branches of
  `allow_rules`, `sandbox_main` (the record's `issue`, the `issue` line printed in place of
  `merge`), and the docstring's paragraph.
- The docstring's list of sandbox campaigns becomes a pointer to the README's table.
- Unchanged: a Copilot campaign gets no `.claude/settings.local.json` (`spec["host"] == "claude"`
  only), its `merge` line is printed, its `open` line keeps the `<stack|parallel|series>` blank.

### 6. `evals/kit/dry_run.py`

- Every `full` becomes `claude-full`: the staged batch (`setup.sandbox_main("claude-full", ...)`),
  the prefixes (`[eval 3 2026-11-01 claude-full]`, `[eval 1 2026-11-12 claude-full]`), the
  messages and the docstring.
- The case `ticket-summary-setup` and its function go (`CASES`, `FUNCTIONS`, the docstring).
- `setup-prompt` loops over the five sandbox campaigns of `setup.CAMPAIGNS` (those with
  `batches`), the blank `<stack|parallel|series>` wanted for the four quick ones; the
  `set_monitor` check runs for the Claude ones and, for the Copilot ones, checks that no
  `.claude/settings.local.json` is written. Which is which is read from each entry's `host`
  (`setup.CAMPAIGNS[campaign]["host"]`), not from a campaign name.
- **New case `copilot-setup` (Q5's dry-run case, README "Changing the kit": a new campaign
  behaviour gets its case).** Two parts:
  1. Setup of `copilot-real-foreman` and `copilot-real-direct` on the local sandbox: exit 0; the
     5 `QUICK` CRs in `3-ready/`, each with its `## Eval run` section; the record's `host` is
     `copilot` and its `crs` is `QUICK`; no `.claude/settings.local.json`; one `merge` line; the
     `batch 1` line holds `--mode <stack|parallel|series> --slots 3 --budget 20`, with `--direct`
     for `copilot-real-direct` only; the last line is the `prompt` line.
  2. The audit on a batch whose `host` is `copilot` (staged the way the Driver finds simplest
     through the dry run's existing batch helpers): `audit.py --sandbox` prints the run table with
     `host copilot`, the "Not audited" line for the transcript checks, check lines with no rail id,
     the judge, the cost, the judge's line and the cost line; no `## Scorecard`; exit 0. The cost
     stays offline: `CHANTIER_SESSION_USAGE` points at a stub the case writes, which prints priced
     calls, so no package is fetched.
- **`evals/kit/audit.py`.** A Copilot batch today loses the judge's line and the cost lines
  (`extra` in `main`), because `print_scorecard` returns before printing them when `check.scored`
  is false. They are printed for every host; the scorecard table stays Claude's only. The
  docstring's campaign list (line 15) becomes a pointer to the README's table, and its Copilot
  paragraph says the Copilot checks are written from the first real `copilot-real-*` run's logs.

### 7. Kit files removed (Q3)

`evals/kit/ticket-summary/chat-request.md`, `evals/kit/ticket-summary/issue.md` (the folder).

### 8. `skills/chantier/scripts/cli/tests/test_cli_units.py`

`test_the_sandbox_campaigns_name_only_frozen_crs_with_hidden_tests`: the expected set becomes
`{"claude-full", "claude-real-foreman", "claude-real-direct", "copilot-real-foreman",
"copilot-real-direct"}`; the `ticket-summary` assertions go; `full` reads `sandbox["claude-full"]`;
the quick loop covers the four quick campaigns, each `== setup.QUICK`.

### 9. Cards

- `skills/chantier/references/chief-of-staff.md` line 509: "**GitHub** (unproved; trial: the eval
  `ticket-summary`)" becomes "**GitHub** (unproved; no trial planned)". The rule itself and the
  card `ticket-summary-example.md` stay.
- `skills/chantier/references/hosts/claude-code.md`: "real-direct run 1" (lines 55, 70) becomes
  "claude-real-direct run 1", "real-foreman run 2" (line 124) "claude-real-foreman run 2", "the
  next real-foreman campaign" (line 153) "the next claude-real-foreman campaign".

### 10. Other docs

- `evals/SCORECARD.md`: the intro names "the Claude campaigns of the README's table" instead of a
  list, and says a Copilot campaign's report has no scorecard; the `where seen` column renames
  `full` (bare, as in `| full, claude-planted |`), `real-foreman`, `real-direct` to their new names
  (the Copilot campaigns are not added: no scorecard on Copilot).
- `CONTRIBUTING.md` lines 253-261: the new names; `claude-full` before a minor or major release, a
  patch release only the quick campaigns (Q4); the claims path `evals/results/claims/claims-vX.Y.Z.md`;
  "`copilot` for a change to Copilot's mechanics" becomes `copilot-real-foreman` or
  `copilot-real-direct`, run by the user in the Copilot app.
- `docs/release-process.md`: the claims path (line 31); one sentence on the campaigns before a
  release: `claude-full` and both quick Claude campaigns before a minor or major release, the quick
  ones only before a patch, as `evals/README.md` ("Which campaign") says (Q4).
- Root `README.md` lines 315-316: a pointer to the campaigns table of `evals/README.md`, with no
  list.

## Out of scope

- The published release notes of v0.9.0 and v0.10.0 (D4).
- Running any campaign; `claude-full`'s first run.
- The Copilot-specific audit checks (roles, prompts, tools): after the user's first real run (Q5).
- The CRs in the planning folder (`.agents/changes/`), archived or in the backlog, that name old
  campaigns: the planning folder is not this CR's.
- `hosts/copilot.md`: no line changes; the campaigns will prove its unproved lines later.
- Any CI job: none is added or changed (`just eval-dry-run` already runs on Linux in CI), so the
  cold-cache rule of `CONTRIBUTING.md` is not owed.

## Evidence

- **E1.** `just check` passes (Windows locally; Linux, macOS and Windows in CI).
- **E2.** `just eval-dry-run` passes at the pushed head, its output kept as the Verifier's evidence
  and quoted in the PR body, every case listed, `copilot-setup` and `setup-prompt` included, no
  `ticket-summary-setup`.
- **E3. No old campaign name left (Q6).** On tracked files, excluding `.agents/` and
  `docs/release-notes/2026-11-13-v0.9.0/` and `docs/release-notes/2026-11-15-v0.10.0/`, a PCRE
  search (`git grep -nP`, or the Grep tool with PCRE) finds nothing for each of:
  - `(?<![\w-])real-(foreman|direct)\b`
  - `ticket-summary(?!-example)`
  - `evals/(full|copilot|real-foreman|real-direct|ticket-summary)/`
  - `` `(full|copilot)` `` in `evals/`, `README.md`, `CONTRIBUTING.md`, `docs/release-process.md`
  - `campaign (full|copilot)\b`
  - in `evals/kit/` and `skills/chantier/scripts/cli/tests/test_cli_units.py`: `"(full|ticket-summary)"`
    (a campaign key or argument; `full` and `ticket-summary` are no host value), and
    `^(?!.*\bhost\b).*"copilot"` (a quoted `copilot` on a line that does not read or set a
    `host`: the host value `"copilot"` of section 5 and a check such as `spec["host"] ==
    "copilot"` stay; a campaign key, argument or runbook path `"copilot"` does not)
  - in `evals/SCORECARD.md` and `evals/results/claims/`: `(?<![\w-])full(?=,| \(| \|)` (a bare
    `full` in the "where seen" and "Can come up in" columns)
  - `` results/[^\s`]*-<date> `` (the old report-name patterns, such as `results/<campaign>-<date>.md`,
    `results/full-<date>-run<n>.md` and `results/claude-planted-<date>.md`)
  - `\b(claude-full|claude-smoke|real)-2026-` (the old report names)
  - `results/claims-v` (the claims file's old path)

  The PR body quotes the commands and their empty output. Beside the search, the PR body names the
  by-hand review of `claude-full` in the six renamed pre-sandbox reports (section 4), which no
  search can do.
- **E4.** `git status` shows the reports and runbooks as renames (`R`), not delete and add.
- **E5.** `uv run --no-project python evals/kit/setup.py full <dir>` exits with the campaign list
  naming the six new names (`campaign: one of ...`).
- **E6. Gates the project's rules ask.** The CR changes cards (`chief-of-staff.md`,
  `hosts/claude-code.md`): the pipeline's `just scenario (ubuntu-latest)` job is green at the PR's
  head (AGENTS.md). It changes `evals/kit/`: an independent review of the whole campaign path
  (setup, a run, the audit, the judge) by a reviewer that did not write it, before the merge
  (README, "Changing the kit"). `just test` stays within its time bound. No `hooks/` or `types/`
  change, so no `just mod`.
