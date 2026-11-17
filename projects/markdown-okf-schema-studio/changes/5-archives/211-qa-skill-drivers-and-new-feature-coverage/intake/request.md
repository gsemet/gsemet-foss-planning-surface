# 211 — QA skill: QA Drivers under the Foreman, new-feature coverage

Owner GO via the Chief of Staff, 2026-10-31. From origin/main, one ready PR touching only `.agents/skills/markdown-studio-exploratory-qa-claude/`, including the QA 210 replay scenarios and synthetic fixtures (no vault content). One clean commit, no force push, never merge.

Backlog intent (verbatim):

> # QA skill: QA Drivers under the Foreman, and every new feature tested
> 
> Filed 2026-10-31 by the Chief of Staff, during campaign 210. Queued after campaign 210 ends: do not
> change the skill while a campaign is running on it.
> 
> ## Intent (owner, 2026-10-31, verbatim French)
> 
> > pour la prochaine fois, dans le skill je voudrais que tu lance un sous agent specialiser dans le
> > foreman (un driver QA). eventuellement plusieurs en //. il faut etre sur que les nouvelles feature
> > sont bien tester
> 
> ## Change to `.agents/skills/markdown-studio-exploratory-qa-claude/`
> 
> 1. **Roles: add a QA Driver.**
>    - The Foreman session is the coordinator. It scopes the campaign, launches the QA Drivers,
>      triages and writes `00-index.md`. It never drives a window except for the smoke check.
>    - A **QA Driver** is a sub-agent specialised in QA. It owns a group of related charters, launches
>      one charter agent per charter (each with its own window and `QA_SESSION`), replays its own
>      High candidates, and returns at most 40 lines to the Foreman.
>    - **Several QA Drivers can run in parallel.** The limit is the machine's total window budget:
>      2 or 3 VS Code windows at a time across all Drivers.
>    - Update the Roles table, the Workflow steps 3–5, the Budgets (one row per Driver) and the prompt
>      template in `references/charters.md`.
> 2. **New features must be tested.**
>    - Scope starts from the PRs merged since the previous campaign's revision:
>      `gh pr list --state merged --search "merged:>DATE"`.
>    - Every user-facing feature or fix gets a row in a **new-feature coverage table** in
>      `00-index.md`: PR, feature, charter that exercised it (or "automated: <test>"), result.
>    - A merged user-facing PR left with neither a charter nor an automated test is a gap. List it
>      under Limits, and the campaign status cannot be `completed`.
>    - Charters for new features run first.
> 3. **Baseline revision.**
>    - Record the campaign's commit in `00-index.md` in a form that `coverage-map.py` reads. Make the
>      script accept it, and fall back to the newest archived campaign.
>    - Campaign 210 had to fall back to the repo root, because 001's `e1b4ad0` predates the
>      extraction.
> 4. **Workspace.** `setup-workspace.sh` expects a `book/` folder this repo does not have, and
>    campaign 210 built the workspace by hand. Make the corpus a parameter (white paper `book/`,
>    visual fixtures, synth, docs, vault copies) and keep okf-schema out.
> 
> 5. **Sweep script.** `noop-sweep.mjs` follows links when it clicks a link-only paragraph. In
>    campaign 210 it derailed the sweeps of chapters 06 and 02, so their tables and fields were not
>    swept. Skip links, or return to the document after a navigation.
> 
> ## Done when
> 
> - The skill describes the coordinator → QA Driver(s) → charter agents chain, with parallel Drivers.
> - A dry run of the Scope step prints the new-feature table for the PRs merged since campaign 210.
> - `coverage-map.py` finds campaign 210's revision.
> - `setup-workspace.sh` runs in this repo with no manual step.

## Item 6 — visual "Currently / Expected" evidence (owner scope addition via the Chief of Staff, 2026-10-31, current round)

QA findings carry visual evidence of "Currently" and "Expected" whenever possible. Change
`references/bug-sheet-template.md` and `SKILL.md`:

1. Each sheet starts with a **Currently / Expected** block, before the steps: a 2-column table, an
   image or diff on each side, one caption line each.
   - **Currently**: a clipped JPEG of the symptom (`shot --clip`), mandatory whenever the symptom is
     visible.
   - **Expected**, by what exists: a shot of the working case when there is one (e.g. the plain
     blockquote that renders right next to the broken alert); otherwise the same shot annotated
     (outline or arrow plus a one-line note of what should be there); for a buffer defect, a pair of
     code blocks: today's diff and the expected diff.
   - If no visual is possible (focus, timing), say why in one line and give the measurements instead.
2. The evidence limit goes from 1 JPEG per finding to 2 (currently and expected), clipped to about
   1000 px.
3. Triage: when a finding becomes a backlog item, the item's `01-intent.md` copies the Currently /
   Expected block with links to the archived evidence images, so the Coder sees the bug without
   opening the campaign. The Currently shot is also the before-shot the fix PR must reproduce.
4. The charter prompt template asks each charter to capture both shots when it writes a sheet.

Applies to the next campaign only; campaign 210's archive stays as it is.

## Item 7: write sheets and the index with the writing skill (owner, via the Chief of Staff, 2026-10-31)

> [!NOTE]
> The owner reads QA sheets and the campaign `00-index.md` in the Studio.

`references/bug-sheet-template.md` says that sheets and the campaign `00-index.md` are written with
`skills/writing-for-markdown-okf-schema-studio/SKILL.md`. Keep it modest: alerts, tables, and the
Currently / Expected images.
