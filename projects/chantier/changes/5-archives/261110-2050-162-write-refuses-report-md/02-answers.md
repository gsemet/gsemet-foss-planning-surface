# Answers

## Grill of 2026-11-10, batch-09 paused

1. **If the cause is outside chantier's reach.**
   - The recommendation was to rename the card.
   - The user: "Pas de raison il faut trouver pourquoi".
   - No rename and no documented limit up front: the CR finds the cause first.
2. **Other files named `report.md`.**
   - The question: should the CR cover every `report.md` chantier has agents write (for example the release CR's `report.md`), or the card alone?
   - The user: "Je pense pas que ce soit lié sur le nom du fichier, cherche dans les log pourquoi avec un agent explore".
   - The user doubts the file name is the cause.
   - The Chief of Staff searches the logs with an Explore agent, now, before the grill goes on.
   - **What the logs show** (Explore agent, checked by the Chief of Staff):
     - The Coder of CR-159 status-command called Write on `skills\chantier\references\report.md` in its worktree, at 2026-11-10T15:26:13Z.
     - The tool refused it before any permission check: "Subagents should return findings as text, not write report files. Include this content in your final response instead."
     - This is a guard built into Claude Code against subagents writing report files. It is not a chantier rule, a setting or a hook.
     - Ruled out: the read-before-write rule (it has its own error), a path outside the session's folders (a Write to the same worktree went through later), a permission rule or hook (none found), the Coder's tools (Write is listed).
     - The same Coder's other Writes went through, for example `skills\status\SKILL.md`. No other agent hit this error that day.
     - So the file name does matter: the guard matched `report.md`. Its exact matching rule is not known. `progress-report.md` was written by an agent the same day without this error.
   - **Second round of questions, after the logs.**
     - **What the CR does about the card.** The user asked: "C'est pour forcer à retourner le rapport en text à l'appelant, rappel moi à quoi sert ce fichier ?" The Chief of Staff explains, and the question is asked again.
     - **Other file names.** The user chose "Tout vérifier (Recommandé)": the CR lists every file a chantier subagent writes, tries each name, and renames only the ones the guard refuses, with proof.
     - **The card, asked again.** The Chief of Staff explained:
       - `skills/chantier/references/report.md` is a card of the skill, chantier's source, that describes the shape of the reports. It is not a report returned to a caller.
       - The guard blocked the Coder wrongly, because of the name.
     - The user then chose "Renommer, prouvé (Recommandé)":
       - the card gets a name that does not look like a report, for example `report-format.md`;
       - every link to it is updated;
       - a subagent proves it can write the new name.
3. **Triage.**
   - The user chose "Spec à relire (Recommandé)".
   - The spec-writer writes the specification, and the user reviews it before any batch.

## Grilled enough (2026-11-10)

- After the full restatement, the user: "Oui le chief of staff peut écrire les rapports.md lors de l'archivage."
- The CR is grilled enough. It stays in P1.
- **The Chief of Staff's own writes stay as they are.** It may keep writing files named `report.md` when it archives, such as a release CR's `report.md`. Only subagents' names are in scope.
- The user's go for the spec-writer: "Lance le reste".

## The specification's open questions (2026-11-10)

1. **The card's name.** The user chose "report-format.md (Recommandé)".
2. **Recording the guard in the host's reference.** The user chose "Oui, la noter (Recommandé)". `hosts/claude-code.md` gets one line with the guard, its text, and the names proved refused and accepted.
3. **A project file the guard refuses** (for example `docs/report.md`). The user chose "S'arrêter, signaler (Recommandé)". The agent stops and reports the refusal, as concepts rule 7 says ("Refusals are reported, never worked around"). The user decides. Nothing changes in that rule.
4. **Names the Chief of Staff's study subagents choose.** The user chose "Oui, une ligne (Recommandé)". `concepts.md` ("Starting an agent") tells them to avoid a file name that looks like a report.
- Then the user: "Plus de question. Livre le max".

## The Driver's blocked question (2026-11-10, round 1)

- **The probe:**
  - The Write tool refused, for a subagent, both `report-format.md` (the chosen name) and `findings.md` (the QA driver's file).
  - It accepted every other name, `progress-report.md` included. See `evidence/name-probe.md`.
- **The question:** another name for the card and for the QA file.
- **No question to the user:** they had said "Plus de question. Livre le max", so the Chief of Staff chose names with neither "report" nor "findings" in them:
  - the card: `skills/chantier/references/status-layout.md`;
  - the QA driver's file: `qa-notes.md`.
- Both must pass the Write probe. If one is refused, the Driver picks another name with neither word in it, probes it again, and says so in the PR.
- The user may change the names when reviewing the PR.

## The guard's rule, and the user's naming (2026-11-10)

- The user pointed to a Reddit post (https://www.reddit.com/r/ClaudeAI/s/6Q26dQpmUm): "Trouve la règle et contourne le, met un fichier 04-result ou quelque chose comme ca".
- Reddit could not be read from this session: both WebFetch and the browser pane refused the site.
- A web search found the rule in user reports on GitHub:
  - anthropics/claude-code issue #44657: "Subagent Write tool rejects .md files named report/summary/findings/analysis — no opt-out";
  - anthropics/claude-code issue #101519.
- **The rule:** a subagent's Write is refused for a `.md` file whose name starts with `report`, `summary`, `findings` or `analysis`, whatever the case.
  - Only the file name is checked, so a prefix such as `42-findings.md` passes.
  - Permissions, a `tools: Write` grant and allow rules do not change it.
  - This matches the probe: `report.md`, `report-format.md` and `findings.md` were refused; `progress-report.md` was accepted.
- **"Contourne" means avoiding these names, not bypassing the guard.** The rule stays: an agent never writes such a file through the shell.
- **The names:**
  - The QA driver's file becomes `04-result.md`, after the CR folder's numbered files, as the user suggested.
  - The card keeps `status-layout.md`: it does not start with any of the four words.
  - `hosts/claude-code.md` records the rule, with its sources and the probe. `concepts.md` tells every subagent that writes a file not to start its `.md` name with one of the four words, and suggests a numbered name such as `04-result.md`.
