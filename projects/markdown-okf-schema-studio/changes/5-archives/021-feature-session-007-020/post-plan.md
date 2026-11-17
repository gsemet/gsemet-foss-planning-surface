# Post-plan fixes (user, 2026-10-20) — run after T45, before the final preflight

Source: user review of the visual screenshots. Each item gets a task (P1–P6), same protocol
(Sonnet implementer + Sonnet reviewer, gate, one commit each).

- P1. `toc-column-*` screenshots (e.g. `toc-column-dark-1600.png`): the TOC column is not visible
  in this whole series. Make the scenario open the TOC and assert it is visible; check the product
  if the toggle really fails there.
- P2. No screenshot illustrates the margin break: add a scenario series with a table wider than
  the column in each width mode (Margin, Auto, Full width), so the three modes can be compared
  side by side (T10b only added one README shot in Auto).
- P3. `first-element-gap-empty-900.png` and others show a HUGE top margin. Assess every case
  (empty file, first line a title, a picture, a text, a table, properties table, edit mode,
  first block editor, Start writing) and make the top gap the same in all of them (U6: one
  uniform ~40 px gap; revisit the T09 toolbar-clearance exception).
- P4. `edit-palette-light.png`: the palette sits inside the edit box. It must sit on top of the
  box and be sticky to the viewport (when the edit box is taller than the viewport, the palette
  stays visible). Add a screenshot with a very tall edit box, scrolled.
- P5. Palette mode label "MyST (includes GFM)" → "MyST" (drop the parenthesis).
- P6. MyST mode must show MyST-specific buttons (admonition, figure, …) and the same applies to
  the `/` commands menu of the insert point; add screenshots of the palette and of the `/` menu in
  Strict, GFM and MyST modes. Note: MyST buttons are planned in T28 (admonitions, footnote,
  deflist, math, sub/sup, label), T30 (`{ref}`/`{doc}`, `{cite}`, dropdown, `{table}`, `{kbd}`),
  T31–T32 (image, figure); GFM buttons in T25–T26. After those land, verify the `/` menu follows
  the mode too; if it does not, P6 covers it.

## P7 — Full width mode keeps large left/right margins (U24, 2026-10-20)

In Full width mode the text column still has wide side margins (user screenshot: about 60 px of
empty space each side). Use the same side margins as a table that breaks out to full width in
Auto mode (the table edge sits close to the preview border). Check Margin/Auto/Full side by side
and add the case to the P2 margin-break screenshot set.

## P8 — Floating toolbar on three rows, rows 2–3 collapsible (U28, 2026-10-21)

Current state (screenshot `P8-toolbar-current.png`): row 1 = Refresh, Anchor/link, Edit, Theme;
row 2 = Back, Next, Zoom −, Zoom +, Margin, TOC (summary), Diff (incoming changes).

Wanted:
- Row 1: Refresh, Anchor/link, Edit, plus a new button that collapses/expands rows 2 and 3.
- Row 2: Back, Next, Zoom −, Zoom +.
- Row 3: Theme switch, Margin, TOC (summary), incoming-changes (Diff) toggle.

Assumptions (confirm at implementation): the collapsed state is remembered per workspace like the
other view preferences (T08); collapsed by default = no (expanded); the collapse button has an
aria-label/title and aria-expanded; keyboard order follows the rows. Update the toolbar screenshots
in the README and the visual checks (row composition, no overlap at 360 px, all themes).

## P9 — Exhaustive e2e campaign audit and reorganisation (U29, 2026-10-21)

User's words (French): « faire une vérification exhaustive des campagnes e2e, vérifier qu'il n'y a
pas de doublon, que les screenshots générés sont pertinents et capturent bien la plus grande
variété possible et réaliste d'état de l'extension. Le but est que cette campagne soit la plus
pertinente possible pour de future rework, ainsi que de préparer une génération que je ferais plus
tard de toutes les exigences qui verrouillent les comportements désirés de l'extension. […] les
tests e2e serviront de base de l'existant (ne le fais pas, mais prépare les tests e2e adéquats).
[…] les e2e ont aussi pour role de me donner a moi en tant de product owner un support visuel
pour vérifier si tout est bon, également un sous ensemble serviront pour la documentation ou
README. tu peux réorganiser les screenshots comme tu veux, nom des tests, etc […] si possible en
sous-ensemble logiquement regroupés (pour préparer de futurs groupements des futures exigences). »

Scope:
- Inventory every e2e / visual / screenshot scenario (test:e2e, test:visual, realInput, README
  capture scripts): what each covers, the screenshots it produces, overlaps and duplicates.
- Remove or merge duplicates; fill gaps so the campaign covers the widest realistic variety of
  extension states (themes, margin modes, palette modes Strict/GFM/MyST, read-only/untrusted,
  editing, selection, comments incl. orphaned, toolbar collapsed/expanded, error states, narrow
  width).
- Reorganise into logical feature groups (future requirement groups): naming scheme for tests and
  screenshot files by group (e.g. `<group>/<nn>-<state>.png`), one index listing group → scenario →
  screenshot → behaviour locked.
- Mark the subset used by README/docs; keep README image paths working.
- Product-owner view: a browsable gallery/index (Markdown) of all screenshots by group.
- Do NOT generate the requirements themselves; only prepare the e2e base (each scenario states
  the behaviour it locks in one line, as raw material for later requirements).
- Run last among post-plan items (after P1–P8, which add screenshots), before preflight.

## P10 — Requirements baseline with okfreq, full traceability (U30, 2026-10-21)

User's words (French, abridged faithfully): « en P10 tu génèreras ces exigences en utilisant
OKFreq (voir le projet /Users/az02065/Projects/DevTools/okf-schema) […] la base d'exigence de ce
projet que tu pourras utiliser comme exemple. 2 niveaux, StRS (stakeholder, ce qui touche les use
case utilisateur), SwRS (ce qui est directement testable). Rajoute les @implements_req et
@tests_req, porte le calcul des stats, les skills de maintenance, les instructions de maintenance
dans AGENTS.md et la guideline ; je veux toutes les features proposées par okf-req dans ce projet.
Il faudra être exhaustif sur l'intégralité des features de l'extension […] (planifie-le
clairement), la traçabilité dans le code et les tests. Ta difficulté sera de ne pas t'arrêter à
moitié mais de couvrir TOUT l'existant, ce qui est couvert par les tests mais également ce qui a
peut-être été raté. Utilise des sous-agents Opus 5.5 pour l'analyse et Sonnet 5.5 pour les revues
critiques. Assure-toi que cette tâche soit réentrante. »

Runs after P9 (the reorganised e2e campaign is the "existing behaviour" base), before preflight.

Reference model: okf-schema `requirements/` (config.yml with levels StRS/SwRS, `derives_from`,
`strs_test_coverage_mode: linked-swrs-and-validation-test`, markers `@implements_req` /
`@tests_req`, scopes with source_dirs/test_dirs, tiers/_schema, tiers/log.md, guideline =
shipped baseline + local overlay), justfile `requirements-lint` / `requirements-report`, skills
`okfreq` + `okfreq-gardening`, AGENTS.md maintenance section. The `okfreq` CLI is already on PATH
(no install needed; `okfreq install-skills` only copies files into the repo).

Re-entrancy: all P10 state lives in `feature-session/p10-requirements/`:
- `STATE.md` — current step, per-scope status table (inventory / StRS / SwRS / markers / review),
  last commit; updated after every step; a resumed session reads it first.
- `inventory/<group>.md` — feature inventory per group, each line with an `F-<GROUP>-NNN` id,
  evidence (source file:symbol, tests, README/CHANGELOG, archive report) and coverage state
  (tested / untested / doc-only).
- `checklists/*.md` — mechanical lists generated from sources, every item must map to ≥ 1 SwRS:
  package.json contributes (commands, settings, keybindings, menus, views), registered preview
  messages (`previewMessages.ts`), palette buttons and `/` menu entries per mode, toolbar buttons,
  CHANGELOG bullets since 0.1, archive reports 001–020, P9 e2e scenarios.
- `reviews/` — Sonnet critical review per scope and the final completeness review.
- Each step is idempotent: requirement files are created with `okfreq new` (IDs never reused),
  re-runs skip done items listed in STATE.md.

Steps:
1. P10.0 Setup (orchestrator): `okfreq init`, config.yml (prefix `StRS-MDOKFSTUDIO` / `SwRS-MDOKFSTUDIO` (U31)
   — scopes = P9 groups mapped to `src/` and `test/` dirs), schemas,
   guideline (baseline + overlay), `okfreq install-skills` (okfreq, okfreq-gardening), AGENTS.md
   maintenance section, justfile `requirements-lint` / `requirements-report` (+ include in
   preflight/check like okf-schema), stats report (`okfreq status` / `generate-report`), tiers/log.md.
2. P10.1 Inventory (Opus subagents, one per group, high effort): read code, tests, README,
   CHANGELOG, archives, settings; list every behaviour incl. untested and error/edge paths.
   Sonnet critic per group: "what did the inventory miss?" against the checklists.
3. P10.2 StRS per scope (Opus): user use cases, stakeholder-observable SHALL + user need.
4. P10.3 SwRS per scope (Opus): one bounded testable SHALL each, GIVEN-WHEN-THEN, derives_from.
   Sonnet critical review per scope (testability, overlap, missing behaviours, EARS quality).
5. P10.4 Traceability (Sonnet implementers, per scope): `@implements_req` near implementation,
   `@tests_req` in unit/integration/e2e tests; StRS markers only on real validation tests (e2e).
   `okfreq update-coverage`, `validate --prose --check-links`, `lint`, `trace --json`.
6. P10.5 Gap closure: SwRS without tests → add tests where feasible (gate B/T/E), otherwise list in
   a gap report with reason; behaviours found in code but absent from docs → flagged to the user.
7. P10.6 Completeness audit (Sonnet, critical): every checklist item → SwRS → implementation
   marker → test marker; stats report; nothing left at "draft placeholder".
8. Commits per step (Conventional Commits, `Assisted-by` trailer), landing report
   `archives/0NN-requirements-baseline`.

## P11 — `/` command menu with completion, Notion/Obsidian style (U32, 2026-10-21)

User's words: « Oui je veux un menu / comme dans notion ou obsidian, avec complétion etc ».
Runs after P8 and BEFORE P9/P10 (so the e2e audit and the requirements cover it).

Expected behaviour (to confirm details at implementation, defaults chosen like Notion/Obsidian):
- In a block editor (and the insert point / Start writing editor), typing `/` at the start of a
  line or after whitespace opens a floating menu anchored at the caret.
- The menu lists the same actions as the palette, filtered by the palette mode (single source of
  truth: `action.modes` + `MODE_RANK`), with label, icon and shortcut hint, grouped by category.
- Typing after `/` filters with fuzzy completion (label + aliases, e.g. `/h2`, `/table`, `/note`);
  ↑/↓ move, Enter/Tab apply, Escape closes and keeps the typed text; Backspace past `/` closes.
- Applying removes the `/query` text and runs the action exactly as the palette button would
  (same undo behaviour, one undo step).
- Mouse: click applies; the menu stays inside the viewport (flips above near the bottom).
- No match: "No command" row; `/` inside code spans/fences or URLs does not open the menu.
- Accessibility: role=listbox/option, aria-activedescendant, live count.
- Tests: page unit tests (filtering per mode, keyboard, removal of the query), real-input
  integration scenario, visual screenshots of the menu in Strict/GFM/MyST, filtered state, no-match.
- README section + CHANGELOG bullet; glossary term **Slash menu**.

## PR — GitHub pull request before P10 (U33, 2026-10-21)

User's words: « juste avant de faire la rétro-ingénierie des requirements, tu prépares la PR pour
GitHub et t'assures de l'envoyer sur GitHub pour qu'elle passe ».
Runs after P9 (all post-plan feature work committed), before P10.
- Remote `origin` = github.com/gsemet/markdown-okf-schema-studio; branch `dev/gsemet` → base `main`
  (52+ commits ahead at c35f34a). `gh` is authenticated as gsemet.
- Run `just preflight` locally first (green), then `git push -u origin dev/gsemet` (this push is
  explicitly authorised by U33; no force push), then `gh pr create --base main` with a PR body
  summarising the features per archive (007–020 + post-plan), manual checks and open questions;
  body ends with the Claude Code line per the attribution reminder.
- Watch CI (`.github/workflows/ci.yml`) with `gh pr checks --watch`; fix failures with new commits
  (never rewrite pushed history) until green. Report the PR URL to the user.
