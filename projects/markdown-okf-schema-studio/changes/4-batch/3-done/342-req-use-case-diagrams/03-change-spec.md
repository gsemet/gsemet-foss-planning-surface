# Change specification: a use-case diagram on each StRS, on GitHub and on the requirements site

Short name: `uc-diagrams`. No tracker issue (verbal origin: the requirements gardening audit,
`changes/1-inbox/requirements-gardening/evidence/audit-synthesis.md`, "Diagrams on the GitHub
Pages site", and `audit-crosscutting.md` section B).

Read the project's `.agents/constitution.md` before starting; its rules and the project guidelines rank above this specification.

## Goal

A StRS (a use case) can carry a small diagram that a reader sees at once: who takes part and what
happens. The same Mermaid text shows as a drawing on GitHub (native rendering) and on the
requirements pages of the published site, where it is drawn at site build time, so the page stays
light and needs no JavaScript. A StRS without a diagram looks exactly as it does today. This CR
adds the rule and the site rendering; it writes no diagram for the 80 StRS.

## Decisions carried from `02-answers.md`

- uc-diagrams-Q1, kind: chosen per StRS by what explains it best. A sequence diagram by default
  (writer, preview, VS Code, file); an actors diagram when several roles take part; a state
  diagram for a mode (edit on/off).
- uc-diagrams-Q2, rendering: pre-rendered to SVG at site build time, not in the reader's browser:
  light page, works without JavaScript, rendering checked by a test.
- uc-diagrams-Q3, theme: corrected by uc-diagrams-Q5 (Q3 rested on the wrong belief that the
  site has a dark mode; `SwRS-MDOKFSTUDIO-CORE-086` forbids one).
- uc-diagrams-Q5, dark variant: the cream variant only. The theme stays a parameter of the
  renderer. CORE-086 is unchanged.
- uc-diagrams-Q6, a diagram that fails to render: the site build fails with the StRS id and
  Mermaid's message.
- uc-diagrams-Q7, no SwRS IDs in a diagram: one sentence in the guideline; the diagram speaks of
  actors.
- uc-diagrams-Q8, clipped labels: the risk is accepted; one flowchart and one state diagram are
  checked on the CI-built site before merge; the label decision stays with backlog
  `mermaid-svg-text-labels`.
- uc-diagrams-Q4, mandatory: the section stays optional in this CR. Making it mandatory for every
  in-force StRS, with a check, comes once the six req-garden CRs are done, not here.
- Way: short specification, not reviewed by the owner; a spec critic runs (the published site
  changes).
- Order: this CR lands after `req-marker-gate` (`depends.json`: `{"after": ["req-marker-gate"]}`)
  and writes its companion marker line in that CR's rule-3 form (section 6).
- From the request: PlantUML is out (GitHub does not render it).

## What changes

### 1. The rule: `requirements/guidelines/project.guidelines.md`

Add a section "Use case diagram of a StRS", next to "Main paths of a StRS":

- A StRS may carry an authored `### Use case diagram` section holding exactly one
  ```` ```mermaid ```` fence and nothing else but an optional one-line caption sentence.
- It sits after the last authored section (usually `### Rationale and constraints`) and before
  `### Main paths`; never inside nor after Main paths, because `mainPaths.ts:37` and
  `scripts/check_main_paths.py` end that section at the next `### ` heading.
- Kind, per the decision above: `sequenceDiagram` by default; `flowchart` with one node per role
  for an actors diagram; `stateDiagram-v2` for a mode.
- Optional in this release of the rule; say that a later change makes it mandatory with a check.
- The diagram speaks of actors (the writer, the preview, VS Code, the file), never of SwRS: no
  SwRS ID in a diagram, so it does not compete with the Main paths map.
- PlantUML is not allowed: GitHub does not render it.
- okfreq validates the section with no error (tested in the audit). GitHub renders a Mermaid
  fence natively; for this rule it is not yet proved (the audit tested okfreq only): the PR
  scenario below checks it on a GitHub branch preview, and the guideline states it once checked.
  GitHub's Mermaid version may differ from the site's `mermaid ^12.2.0`, so a diagram can look
  different, or fail, on one side only; the guideline says so.

Update the Main paths paragraph that says the section "sits after the last authored section" so
that both rules agree (the diagram, when present, comes just before Main paths).

### 2. The model: `test/site/requirementsViewer/model.ts`

- New exported pure function `parseUseCaseDiagram(text: string): string | undefined` (it may live
  in a new file `test/site/requirementsViewer/useCaseDiagram.ts` with the renderer below): from the
  body cut at `<!-- okf:links:start -->` (`bodyOf`), find the `### Use case diagram` heading, take
  the section up to the next `#{1,3} ` heading or `<!--`, and return the source of its first
  ```` ```mermaid ```` fence (trimmed), or `undefined` when there is no section or no fence.
- `Requirement` gets `diagram?: string`, set for an active StRS only, in `parseRequirementsReport`.
- `ViewerModel` gets `diagrams: Map<string, UseCaseDiagram>` (StRS id to rendered SVG), empty after
  parsing; the writer fills it.

### 3. The renderer: new `test/site/requirementsViewer/useCaseDiagram.ts`

- `renderUseCaseDiagrams(sources: ReadonlyMap<string, string>, theme = CREAM_DIAGRAM_THEME): Promise<Map<string, UseCaseDiagram>>`:
  the theme (the Mermaid `themeVariables`) is a parameter; the site passes only the cream one.
- One headless Chromium for all diagrams (`chromium` from `playwright-core`, the pattern of
  `test/site/socialCard.ts:120-145`), started only when at least one source exists; the same clear
  error as the social cards when Chromium does not start ("run `just dev` to install it").
- One blank page; load `node_modules/mermaid/dist/mermaid.min.js` (the `mermaid ^12.2.0` already in
  `package.json`; no new dependency) with `page.addScriptTag({ path })`; `mermaid.initialize` with
  `startOnLoad: false`, `securityLevel: "strict"`, `theme: "base"`, and `themeVariables` built from
  the cream `SITE_TOKENS` of `test/site/siteTheme.ts` (`background` transparent, `primaryColor`
  `--paper`, `primaryTextColor` `--ink`, `primaryBorderColor` `--line`, `lineColor` `--soft`,
  `secondaryColor` `--quote-bg`, `tertiaryColor` `--bg`, `fontFamily` the site sans stack); wait
  for `document.fonts.ready`; then `mermaid.render("ucd-<short id>", source)` per StRS, so SVG ids
  never collide.
- One variant, cream (uc-diagrams-Q5): no dark variant, no `prefers-color-scheme` rule.
- A render error fails the site build (uc-diagrams-Q6): the error names the StRS id, its file and
  Mermaid's message, for example
  `Cannot draw the use case diagram of StRS-MDOKFSTUDIO-TABLE-002 (requirements/tiers/strs/…/StRS-MDOKFSTUDIO-TABLE-002.md): <Mermaid message>`.

### 4. The writer: `test/site/requirementsViewer/write.ts`

- `writeRequirementsViewer` (already async) loads the model once, collects the `diagram` sources of
  the active StRS, renders them, stores them in `model.diagrams`, then writes the pages and the
  social cards. `writeViewerPages` stays synchronous for its existing tests: it takes the model's
  `diagrams` as filled (empty when not rendered), for example through an optional parameter.
- No new file is copied to the site: the SVG is inline.

### 5. The page: `test/site/requirementsViewer/pages.ts`, `viewer.css`

- In `useCasePage`, when `model.diagrams` has the StRS, insert under the `user_need` blockquote and
  before "How it is split":
  `<h2>Use case diagram</h2>` then `<figure class="ucd" role="img" aria-label="Use case diagram of <title>">` + the SVG + `</figure>`.
- A StRS without a diagram: the page body is byte-identical to today.
- `viewer.css`: `.ucd` with the paper background, the line border and radius already used by
  `.map`, `overflow-x:auto`, and `.ucd svg{max-width:100%;height:auto}`.
- No script, no stylesheet link, no `prefers-color-scheme` rule (CORE-086 holds).

### 6. Requirements (okfreq)

- New SwRS in `rendering-core`, created `proposed`
  (`uv run --no-sync --group requirements okfreq new … --lifecycle proposed`), derived from
  `StRS-MDOKFSTUDIO-TRUST-014` like CORE-069 and CORE-080..086: "The site requirements viewer shows
  the use case diagram of a StRS". Scenarios:
  - nominal: a StRS with a `### Use case diagram` Mermaid fence; the site is built; its use-case
    page shows the diagram as an inline SVG in the site's colours under the user need, readable
    without JavaScript;
  - boundary: a StRS with no section, or a section with no Mermaid fence; its page is unchanged;
  - refusal: a fence Mermaid cannot draw; the site build fails with the StRS id and Mermaid's
    message.
- `@implements_req` on that ID in `src/core/render/requirementsViewer.markers.ts` (the companion
  of `test/site/requirementsViewer/write.ts`, which already carries CORE-069..085, since
  `test/site/` carries no implementation markers), written in `req-marker-gate`'s rule-3 form, with
  the code point that implements it, a name found in the host file or its folder:
  `// @implements_req SwRS-MDOKFSTUDIO-CORE-<NNN> — renderUseCaseDiagrams` (`renderUseCaseDiagrams`
  lives in `useCaseDiagram.ts`, in the host's folder). `@tests_req` at each test listed below, one
  ID per marker block as that CR's rule 2 asks.
- The parent and the marker place are provisional: the sibling CR `req-garden-core-diagrams-trust`
  moves the site SwRS (CORE-069, CORE-080..086) out of TRUST-014 and removes the companion marker
  lists. The new SwRS is one of the site SwRS that CR reparents and whose marker it moves; this CR
  follows today's pattern so that the two CRs merge in either order.
- `just requirements-update`, its generated files committed, and a dated entry in
  `requirements/tiers/log.md`.

## Out of scope

- Writing the diagrams of the StRS: each restructure (req-garden) CR writes the diagrams of its
  StRS.
- Making the section mandatory and a check of it (after the six req-garden CRs).
- PlantUML, Vega or committed SVG files next to the StRS.
- Showing other StRS sections (Normative behavior, Rationale) on the page.
- Mermaid in the docs pages of the site (`renderMyst` placeholders).
- The writing skill: this is not a Studio rendered syntax, so `skills/` is unchanged.
- CI: no job is added or changed. `just ci-gallery` already builds the site with Chromium for the
  social cards on the same machine, so the diagrams need nothing new there.

## Evidence

- `test/site/requirementsViewer/useCaseDiagram.test.ts` (new), each test with `@tests_req`:
  - extraction: section with a fence; no section; section without a fence; two fences (first
    taken); a `### Use case diagram` inside the links block is ignored;
  - rendering: one sequence fixture renders to an `<svg` with the cream ink colour and no
    `<script`; skipped with a message when Chromium cannot start, as `socialCard.test.ts:68-70`;
  - a broken fence makes the render reject with the error naming the StRS id and Mermaid's
    message.
- `pages.test.ts`: with a diagram, the figure sits after the blockquote and before "How it is
  split"; without one, the body matches the one built before the change.
- `fixture.ts`: one StRS text with a `### Use case diagram` section before its Main paths;
  `model.test.ts`: `diagram` is set on it and Main paths still parse.
- `write.test.ts`: the existing assertions still hold (no dark rule, CORE-086).
- Commands: `just check`, `just requirements-lint`, `just requirements-update`,
  `just requirements-report`, then `just preflight` (on Windows the static stage; the site build
  runs in CI's `ci-gallery`).
- Scenario for the PR (every step required; screenshots in the PR body):
  1. On a scratch branch off the PR branch (for example `uc-diagrams-sample`, never merged), give
     three StRS a `### Use case diagram` section: one `sequenceDiagram`, one `flowchart` (actors)
     and one `stateDiagram-v2`. These samples are not part of the PR: writing the diagrams stays
     out of scope.
  2. Site: run `just requirements-report` then `fnm exec -- npm run site`; open
     `out/site/requirements/<area>/<StRS id>/index.html` of each, with JavaScript off; each diagram
     shows in the site's colours with no label cut; screenshot.
  3. GitHub: push the scratch branch and open each StRS file on github.com; each fence is drawn as
     a diagram; screenshot. This is the check of the GitHub claim in the guideline; note in the PR
     body any difference from the site drawing (GitHub's Mermaid version may differ from 12.2.0).
  4. Clipped labels (uc-diagrams-Q8): build the site in CI for the scratch branch
     (`gh workflow run ci.yml --ref uc-diagrams-sample`, or its push), download the site artifact of
     `ci-gallery`, and open the flowchart and the state diagram pages: no label is cut; screenshot
     both in the PR body. A cut label is reported in the PR body and in backlog
     `mermaid-svg-text-labels`; it does not change the label technique in this CR.
  5. Delete the scratch branch, local and remote, once the screenshots are in the PR body.
