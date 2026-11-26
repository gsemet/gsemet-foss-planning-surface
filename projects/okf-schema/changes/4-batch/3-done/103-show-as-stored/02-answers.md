Short name: `show-raw`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: `show` re-serializes the
  frontmatter (flow mappings and lists become block style, a datetime is rewritten and quoted,
  YAML comments are dropped) and prints `trust: <tier>` on stdout between the closing `---` and
  the body (`src/okf_schema/cli.py:766`), plus `stale: true` when stale.
- A file with no frontmatter is shown with an invented block `---`, `{}`, `---`.
- A file whose frontmatter is not valid YAML is shown with `{}`: the stored frontmatter does not
  appear at all, exit code 0, nothing on stderr.
- No test, tutorial or skill reads the `trust:` line of `show` (searched in `tests/`, `docs/`,
  `skills/`, `examples/`, `scripts/`). `SwRS-OKFSCHEMA-CORE-006` names `stale: true` in a
  scenario; `SwRS-OKFSCHEMA-CORE-005` covers `show`.
- The Python API `show_bundle` returns `ConceptDetail(frontmatter, body, trust_tier, stale)`,
  without the stored text.
- CR 56 changes the same function and command; this item stacks on it.

## 2026-11-25: grill, user's answers

1. show-raw-Q1: **Standard output.** Free answer: "Pourquoi aurait on besoin de reconstruire le
   frontmatter au lieu d’afficher juste le fichier brut". Read with answer 3 as option A, the
   stored file as it is; to be confirmed at the restatement.
2. show-raw-Q2: **trust and stale.** "C. Supprimer": `show` no longer prints them.
3. show-raw-Q3: **Damaged files.** Free answer: "Affiche juste le contenu du fichier, show ne
   valide pas". No parsing check, no warning, no failure for a file without frontmatter or with
   invalid YAML.
4. show-raw-Q4: **API.** "A. Champ raw (recommandé)": the result of `show_bundle` gains a field
   with the exact stored text; the current fields do not change.
5. show-raw-Q5: **Trust tier no longer in any command.** "A. Accepter (recommandé)": the source
   stays the file's `verified` field, which `show` now prints faithfully (the option's words);
   `list` keeps its `[STALE]` marker and the API keeps `trust_tier` and `stale`. No new CR.
6. show-raw-Q6: **Release.** "A. fix → 0.18.2 (recommandé)": a `fix(show): ...` commit, like
   CR 56.
7. show-raw-Q7: **Grilled enough.** "A. batch-01 (recommandé)": specify it for the running
   batch, stacked on 56. The restatement shown with the question carried the reading of
   answers 1 and 3 (the stored file, byte for byte, nothing added, no validation).

Destination: running batch batch-01.

Spec critic: yes, it changes the output of a command and the public API.

8. show-raw-Q8: **Ticket summary.** "A. Commentaire (recommandé)": post
   `work/issue-comment.md` on issue 58, no plan artifact.

   Posted on https://github.com/gsemet/okf-schema/issues/58, 2026-11-25: comment
   https://github.com/gsemet/okf-schema/issues/58#issuecomment-7172912278; plan "none"; demo
   "none".

## 2026-11-25: a command for the trust level

Unprompted, the user: "Tu peux rajouter une commande dédiée pour afficher le niveau de
confiance et le documenter". This replaces the part of answer 5 that left the trust tier in no
command (and the sentence of the posted comment saying so).

9. show-raw-Q9: **Shape of the command.** First answer: "Je ne sais pas, c’est l’histoire du
   trust supprimé de la commande show". Asked again, simpler: "A. Les 2 lignes (recommandé)":
   `okf-schema trust --path <bundle> <concept>` prints exactly what `show` added (`trust: <tier>`,
   and `stale: true` when stale), nothing more; no listing of the whole bundle. Documented.
10. show-raw-Q10: **Where.** "A. Dans 58 (recommandé)": same CR, one pull request, so the removal
    and its replacement land together. It becomes a `feat`: the release is 0.19.0 instead of
    0.18.2 (replaces answer 6).
11. show-raw-Q11: **A concept file that is not UTF-8.** "A. Afficher les octets (recommandé)":
    `show` prints the file's exact bytes, exit 0; the API `show_bundle` keeps failing.
12. show-raw-Q12: **Wrong trust tier for actor forms of the specification** (the OKF 0.2 check
    found that a concept verified by `reference_agent/gemini-2.5-pro` is read as unverified, so
    the new command would print a wrong level). "B. CR séparé": a separate fix, stacked before
    this CR in the same batch.

## 2026-11-25: after the spec critic, second pass (3 findings fixed without the user; 1 question, the specification's)

13. show-raw-Q13: **`trust` on a concept file that is not UTF-8.** "A. Message clair
    (recommandé)": one error line on stderr and exit code 2, no traceback (the option's preview:
    `Error: Concept file is not valid UTF-8:` followed by the file's path).

## 2026-11-25: ticket correction

Asked: post `work/issue-update.md` on issue 58, the earlier comment being wrong (the `trust`
command, release 0.19.0). "A. Poster (recommandé)".

Posted on https://github.com/gsemet/okf-schema/issues/58, 2026-11-25: comment
https://github.com/gsemet/okf-schema/issues/58#issuecomment-7174489485; plan "none"; demo
"none".

## 2026-11-25: pull request link and release announcement

Said while answering the same question for issue 56: "Oui, poster. poste les liens quand tu les
as, et quanbd la release sera faite tu postes des commentaires pour annoncer la dispo". No further
question is needed for either comment.

Due: the pull request link on https://github.com/gsemet/okf-schema/issues/58 once the pull request
exists, then the release announcement once the release holding it is published.

Posted on https://github.com/gsemet/okf-schema/issues/58, 2026-11-26: comment
https://github.com/gsemet/okf-schema/issues/58#issuecomment-7177266224 (`work/issue-followup.md`,
the link to https://github.com/gsemet/okf-schema/pull/73); plan "none"; demo "none". Still due: the
release announcement.

Posted on https://github.com/gsemet/okf-schema/issues/58, 2026-11-26: comment
https://github.com/gsemet/okf-schema/issues/58#issuecomment-7185041662 (`work/issue-release.md`,
released in 0.19.0); plan "none"; demo "none".
