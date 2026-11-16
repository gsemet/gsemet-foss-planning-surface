# CR-159 investigation (worktree batch-09-CR-159, base origin/main)

Rules (`$CHANTIER rules`): AGENTS.md, CONTRIBUTING.md, README.md, chief-of-staff.md, scenario/README.md, evals/README.md, docs/release-process.md.
Relevant: `just check` must pass; cards change => `just scenario`; never edit a version by hand; CLI knows no role; tests few; no HOST_TOOLS in cards.

## 1. The "Reports" bullet (chief-of-staff.md lines 240-266, in "While it runs")
Starts at "- **Reports:** name every CR by its number and slug together..." (line 240) and ends at line 266 "(only a Tips line can follow it, see below)." Includes sub-bullets **Progress** (249-258) and **Completion** (259-266). Next bullet "- **Steering:**" at 267.
Other report rules elsewhere in the card, to decide for report.md:
- l.236-239 **Status** bullet: "Before a report, run `$CHANTIER status --refresh` with no epoch: it records the current spend and STATUS.md and leaves the Foreman's heartbeat alone." (spec says this goes to report.md; the rest of the Status bullet - `status [--notes]`, PR links, STATUS.md for user, 🔴 is a question, never read transcript - stays.)
- l.27 table row: Completion report on `final` / pause (trigger; stays).
- l.316-335 **Cost** bullet: cost table of a report (lines of `cost`, as printed and in that order; Foreman line / `Chief of Staff (steering)`, Driver types, worker types, own `Chief of Staff:` line with two figures and context size; group nothing; `not measured`; session not in spend). Sub-bullet **Explaining the figures** (`cost --explain`, Completion report). The spec lists "the cost table and `cost --explain`" for report.md: these ARE report rules, so they move (or report.md points to them; decide with the Verifier: "no rule lost" is simplest if moved whole).
- l.342-356 **Tips** bullet (💡 line after For you, examples incl. "Status"): spec says report.md holds the Tips line; the general tip rule/examples list (compact, /chantier-board, "What did it cost?", "File this"...) applies beyond reports. Suggest: keep the Tips bullet in chief-of-staff.md, report.md holds only the rule for a report (💡 line after **For you**, none when a question/blocker, names only what chantier answers, may name `/chantier:status`).
- l.297 chain: "Your next report has a line with the chain and its reason." (a report content rule; keep or copy one line into report.md).
- l.358-359 pause: "Give the Completion report" (trigger; stays). l.416 "in the report's shape"; l.469 "end the Progress report with the offer of a demo" (stacked CRs; a Progress-report rule, candidate for report.md); l.504 release: writes latest Progress report to release CR as `report.md` (a different file, in CR folder: beware name clash only in wording, not files).
- Also concepts.md: "A CR's name", "ready PR" (referenced, stays). "MR" vs "PR" rule is inside the bullet (241-242).
Note chief-of-staff.md has icons as mojibake-safe UTF-8; keep UTF-8 without BOM. The spec file itself shows mojibake (ðŸŸ ) when read by PowerShell: only a console decoding issue, but check encoding of new files.

## 2. skills/griller/ as model
`skills/griller/SKILL.md` (24 lines): front matter `name`, `icon`, `color`, `description`; H1; line `chantier-version: 0.8.0` (regex `^chantier-version: V$`); paragraph defining `$CHANTIER` via `../chantier/`; "You are a **Griller**. Read [concepts](../chantier/references/concepts.md), ... now." Links relative to `../chantier/references/`.
skills/status/SKILL.md copies that; name `status`; read only `../chantier/references/report.md` (not concepts/session-start). Note report.md refers to concepts.md ("A CR's name", "ready PR"): the status skill reads report.md only per spec, so report.md should carry what it needs inline or the spec's "reads report.md only" tolerates its links (decide).
Router skills/chantier/SKILL.md l.8 lists `/chantier:chief-of-staff` and `/chantier:griller`: may add `/chantier:status`.

## 3. Places a new skill must join (all must change together)
- `scripts/version.py` TARGETS: add `(ROOT/"skills"/"status"/"SKILL.md", rf"^chantier-version: {V}$", 1)`; `test_every_file_carries_the_same_version` iterates TARGETS, so a missing entry is silent: the new SKILL.md must carry `chantier-version: 0.8.0` and be in TARGETS (do not edit version by hand otherwise).
- `.github/plugin/plugin.json` "skills": add `"./skills/status"` (Copilot manifest DOES list skills; `.claude-plugin/plugin.json` lists none, Claude auto-discovers `skills/*`). `test_manifests_agree` checks each listed skill has SKILL.md.
- `tests/test_structure.py` (skills/chantier/scripts/cli/tests/): `test_three_skills_the_router_and_two_thin_ones_listed_by_copilot` has `names = ("chantier","chief-of-staff","griller")`, checks front name, thin ones contain `../chantier/references/` and `../chantier/scripts/cli/`, and `copilot["skills"] == [f"./skills/{n}" for n in names]` (order matters). Update: add "status" (rename test to four skills / three thin). `test_skill_and_references_links_resolve` globs `skills/*/SKILL.md` and `references/*.md`, so new links are checked automatically. `test_each_host_has_its_reference_and_the_cards_hold_no_host_tool` has a hard list of cards: add "report" (no host tool words, incl. "/compact", "/loop", "/every", `SendMessage`... so report.md must not name host compact commands). No test constrains reference-card count; CARDS/ROLES (agents) unaffected: report.md is not a role card, no agent files.
- Docs/lists that name the skills (text edits, no tests):
  - CONTRIBUTING.md l.10-15: "Three skills ... thin and load the same cards" and the references file list (add `report.md`; "Four skills", status thin).
  - README.md l.143-145 ("one of the three entries", `/chantier:<name>`; command list), l.158 table, l.178 (board opens on chantier/chief-of-staff skill load, "not griller"; see hooks below), l.339-343 repo tree (`skills/griller/` line; references list `chief-of-staff, griller, foreman...`).
  - docs/tutorial-claude-code.md l.32 ("three skills (the router, chief-of-staff and griller)"), l.66-69.
  - skills/chantier/references/hosts/claude-code.md l.21 (skills row, `/chantier:chantier`, ..., `/chantier:griller`) and l.374; hosts/copilot.md l.26 ("the same three ... declared in plugin.json"): update to four.
  - docs/use-cases*.md mention griller only as a role; SVG/diagrams not needed.
  - hooks/register.tsx l.312: board pane opens on loading `chantier`/`chief-of-staff` skill, not griller; check whether `status` should also (probably not; a read-only report). No change needed unless desired; has register.test.tsx.
- chief-of-staff.md Tips: add `/chantier:status` as an example (host-neutral? the Tips list already names `/chantier-board` as Claude-only; on Copilot the entry is the same name; `test` only forbids HOST_TOOLS words).

## 4. Tests that cover the cards' content
Only structure tests; none reads the Reports text. The scenario (scenario/run_scenario.py, 165 KB) checks CLI behaviour (status, cost, rails) and `references/` path in `take` output; it does not read chief-of-staff.md. Moving the bullet cannot break it; `just scenario` is required by AGENTS.md since cards change (runs github then gitlab forge).

## 5. Evidence: a /chantier:status output on a scenario batch
`just scenario` = `uv run --no-project python scenario/run_scenario.py --forge github` then `--forge gitlab`; options `--verbose`, `--keep` (keeps the workspace; transcript in scenario/results/<forge>-<time>.md, not committed). Scenario batch names batch-01 etc. (`w.chantier("status","--batch","batch-01")`). The scenario drives the CLI directly (no LLM), so it cannot run the skill itself.
Evidence plan:
1. Run `uv run --no-project python scenario/run_scenario.py --forge github --keep` (and the gate `just scenario`, both forges) in the worktree; take the kept workspace path from the output.
2. In that workspace, run the three commands the skill runs, with no epoch: `$CHANTIER status --refresh --batch <batch>`, `$CHANTIER status --batch <batch>`, `$CHANTIER cost --batch <batch>`; save the raw outputs to `<folder>/evidence/status-raw.txt`.
3. Follow `report.md` by hand (or by a fresh session reading only report.md) to write the Progress report from those outputs into `<folder>/evidence/status-report.md`; check it against the checklist: header line, legend line of 6 icons copied from `label`, table CR/subject/state/PR-or-MR/cost, explanation under table for any 🟠/🔴, cost table in `cost` order, **For you**, then the optional 💡 line.
4. If possible, a live proof: in a Claude Code session on that workspace type `/chantier:status` (after `/reload-plugins`; worktree skills load only once merged, per AGENTS.md, so run it from the main checkout after merge, or note it as unproved before merge). Record whether it read only report.md.
5. Also store `just check` output and the grep proving no rule lost: a diff of the former Reports bullet text vs report.md (e.g. every sentence of l.236-266, 297, 316-335, 342-356, 469 accounted for).
Caveat to state in the PR: the "no active batch" path (one line plus backlog count from `.agents/changes/STATUS.md`) can be shown on a fresh `init`-ed repo.

## 6. Risks / open points for the Coder
- Spec depends on CR-158 (tree v2: STATUS.md index path `.agents/changes/STATUS.md`; batch STATUS at `4-batch/STATUS.md`): confirmed in the base (commits f85c4c6, 57c195e).
- Decide Tips/Cost/Explaining placement ("no rule lost or changed"): moving Cost and Explaining whole into report.md and leaving a pointer is safest; the Cost bullet also says "on 'status?'" so chief-of-staff must still say when to give a report.
- report.md must be self-sufficient for the status skill (concepts.md links: "A CR's name", "ready PR") or the skill's read list gains a concept: the spec says report.md only, so inline the two needed definitions (a CR's name `CR-<n> slug`; 🔵 only for a ready PR) in report.md.
- Cards must hold no host-tool words (test): `/compact` and similar must stay in hosts/*.md.
- Copilot: status skill's argument-free, so no host difference; plugin.json must list it.
- Untracked `state.py` and `.agents/` in the main checkout: not part of the change.
