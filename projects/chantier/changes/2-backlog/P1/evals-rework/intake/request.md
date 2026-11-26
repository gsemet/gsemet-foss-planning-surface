# Rework the eval campaigns: names by host, Copilot campaigns ready, reports by date

Filed 2026-11-15 by the Chief of Staff, the user's words (French, translated):

- `ticket-summary`: delete it.
- `full`: rename it `claude-full`.
- `real-foreman`: rename it `claude-real-foreman`.
- `real-direct`: rename it `claude-real-direct`.
- `copilot`: replace it with `copilot-real-foreman` and `copilot-real-direct`. Prepare all of
  it; the user launches the real campaign later, in Copilot.
- Look for anything wrong in the evals.
- Name the reports by date, then hour and minute: `real-direct-2026-11-12-run1.md` becomes
  `2026-11-12-19-41-real-direct-run1.md`.

## What the rename touches

The campaign names appear in about 220 places across 24 files:

- `evals/README.md`, `evals/SCORECARD.md` (its "where seen" column), every runbook,
  `evals/results/claims-v0.10.0.md`;
- `evals/kit/setup.py` (`CAMPAIGNS`), `evals/kit/audit.py`, `evals/kit/dry_run.py`;
- `skills/chantier/scripts/cli/tests/test_cli_units.py` (the set of sandbox campaigns);
- `CONTRIBUTING.md`, the root `README.md`, `docs/release-process.md`;
- the hosts card `skills/chantier/references/hosts/claude-code.md`;
- the release notes of v0.9.0 and v0.10.0. These are published history and are better left
  alone.

## The Copilot campaigns

These are the Copilot counterparts of the two quick Claude campaigns. Each runs the same 5
frozen CRs (`QUICK` in setup.py), with the mode chosen at launch, on the Copilot app:

- **copilot-real-foreman:** a Foreman started with `create_session`, the heartbeat as `/every`.
- **copilot-real-direct:** the Chief of Staff alone.

Each needs the following:

- its runbook, its `CAMPAIGNS` entry and its prompt line in the Copilot form;
- its dry-run case;
- the Copilot prerequisites in the README (today the list names only Claude Desktop);
- its row in the campaigns table.

Today's `copilot` runbook has 1 CR, 1 slot and a $3 budget: it goes. The audit's Copilot part is
still empty ("Still to fill in from a real run"). This CR states what the audit can check before
that first run, and leaves the rest marked unproved.

## Found wrong in the evals (Chief of Staff's reading, 2026-11-15)

1. **A name collision.** The old reports `claude-full-2026-11-03.md`, `claude-full-2026-11-04.md`
   and `claude-full-2026-11-04-ask-only.md` are `claude-planted` runs from before the campaigns
   merged. Renaming `full` to `claude-full` makes them look like runs of the new campaign. The
   date-first renaming should give them the campaign they really ran. The same goes for
   `real-2026-11-05*.md` (a `real-foreman` run on this repository, before the sandbox) and
   `claude-smoke-*`. The README's "Past reports keep their names" paragraph then goes.
2. **Some old reports give no start time.** The real-* runs of 11-12 and 11-15 and
   claude-full-11-03/11-04 state one, in UTC. The rest need one read from their record, or a
   rule for when none is known.
3. **The time zone of the new name.** The reports give times in UTC (19:41 UTC for real-direct
   run 1). Pick one zone, UTC by the reports, and say it in the README.
4. **The ticket summary loses its trial.** `chief-of-staff.md` marks the GitHub ticket summary
   "unproved; trial: the eval `ticket-summary`". Deleting the campaign leaves that rule with no
   trial. Its kit files go with it: `evals/kit/ticket-summary/`, the setup and dry-run cases,
   and `test_cli_units.py`'s check. Then either the card names another trial, or the rule says
   it has none.
5. **`full` has never run**, yet the README says it runs before every release. v0.10.0 shipped
   without it. Either the release rule says what replaces it, or the rename is the moment to
   run it once.
6. **The README lists campaigns in several places by hand:** the intro, "Run a campaign", "A
   sandbox campaign" ("the five sandbox campaigns"), the Auto-fix line, the kit table and
   `audit.py`'s docstring. Today they already disagree: the Auto-fix line leaves out `copilot`.
   One list, written once, avoids that.
7. **The README mixes Claude and Copilot without saying which applies.** "Copilot's report stays
   as it is", and the operator, the trust step, Auto-fix and the 10-message limit are all
   Claude Desktop. With two Copilot campaigns, each host-specific step should name its host.
8. **The results folder holds the claims file** `claims-v0.10.0.md` among the run reports. The
   date-first order should keep the claims files apart, for example in `results/claims/`.

Related: `evals/README.md` ("Campaigns", "The report"), `evals/kit/setup.py`.
