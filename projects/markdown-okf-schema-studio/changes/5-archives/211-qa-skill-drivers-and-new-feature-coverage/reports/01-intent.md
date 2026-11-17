# QA skill: QA Drivers under the Foreman, and every new feature tested

Filed 2026-10-31 by the Chief of Staff, during campaign 210. Queued after campaign 210 ends: do not
change the skill while a campaign is running on it.

## Intent (owner, 2026-10-31, verbatim French)

> pour la prochaine fois, dans le skill je voudrais que tu lance un sous agent specialiser dans le
> foreman (un driver QA). eventuellement plusieurs en //. il faut etre sur que les nouvelles feature
> sont bien tester

## Change to `.agents/skills/markdown-studio-exploratory-qa-claude/`

1. **Roles: add a QA Driver.**
   - The Foreman session is the coordinator. It scopes the campaign, launches the QA Drivers,
     triages and writes `00-index.md`. It never drives a window except for the smoke check.
   - A **QA Driver** is a sub-agent specialised in QA. It owns a group of related charters, launches
     one charter agent per charter (each with its own window and `QA_SESSION`), replays its own
     High candidates, and returns at most 40 lines to the Foreman.
   - **Several QA Drivers can run in parallel.** The limit is the machine's total window budget:
     2 or 3 VS Code windows at a time across all Drivers.
   - Update the Roles table, the Workflow steps 3–5, the Budgets (one row per Driver) and the prompt
     template in `references/charters.md`.
2. **New features must be tested.**
   - Scope starts from the PRs merged since the previous campaign's revision:
     `gh pr list --state merged --search "merged:>DATE"`.
   - Every user-facing feature or fix gets a row in a **new-feature coverage table** in
     `00-index.md`: PR, feature, charter that exercised it (or "automated: <test>"), result.
   - A merged user-facing PR left with neither a charter nor an automated test is a gap. List it
     under Limits, and the campaign status cannot be `completed`.
   - Charters for new features run first.
3. **Baseline revision.**
   - Record the campaign's commit in `00-index.md` in a form that `coverage-map.py` reads. Make the
     script accept it, and fall back to the newest archived campaign.
   - Campaign 210 had to fall back to the repo root, because 001's `e1b4ad0` predates the
     extraction.
4. **Workspace.** `setup-workspace.sh` expects a `book/` folder this repo does not have, and
   campaign 210 built the workspace by hand. Make the corpus a parameter (white paper `book/`,
   visual fixtures, synth, docs, vault copies) and keep okf-schema out.

5. **Sweep script.** `noop-sweep.mjs` follows links when it clicks a link-only paragraph. In
   campaign 210 it derailed the sweeps of chapters 06 and 02, so their tables and fields were not
   swept. Skip links, or return to the document after a navigation.

## Done when

- The skill describes the coordinator → QA Driver(s) → charter agents chain, with parallel Drivers.
- A dry run of the Scope step prints the new-feature table for the PRs merged since campaign 210.
- `coverage-map.py` finds campaign 210's revision.
- `setup-workspace.sh` runs in this repo with no manual step.
