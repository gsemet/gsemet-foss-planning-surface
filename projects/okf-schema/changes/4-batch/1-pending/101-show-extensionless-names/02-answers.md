Short name: `show-names`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: `show api/health-check` answers
  "Concept not found"; `show api/health-check.md` works.
- Same run: `show api` (a directory) ends in a `PermissionError` traceback (Windows).
- From the code, not run: `show_bundle` joins `bundle / concept_path` with no containment check,
  so a `../` path outside the bundle is read (`src/okf_schema/api.py:392`).
- `backlinks_bundle` appends `.md` to a target that does not end with it
  (`src/okf_schema/api.py:841`).

## 2026-11-25: grill, user's answers (the options picked)

1. show-names-Q1: **Direction.** "A. Faire accepter (recommandé)": `show` accepts a concept name
   without `.md`.
2. show-names-Q2: **Resolution.** "A. Fichier exact, sinon .md (recommandé)": the exact path when
   it is a file, else `<name>.md`; a directory is never a concept, so `api` resolves to `api.md`
   even when `api/` exists.
3. show-names-Q3: **Directory with no concept.** "A. Corriger ici (recommandé)": in this CR,
   "Concept not found", exit code 2, no traceback.
4. show-names-Q4: **Outside the bundle.** "A. Refuser ici (recommandé)": in this CR, an error and
   exit code 2 for a path leaving the bundle; nothing changes for paths inside it.
5. show-names-Q5: **Symlinks.** Free answer: "Un bundle doit être auto contenu selon la specs
   donc on interdit les liens symbolique qui sortent". A symlink inside the bundle whose target is
   outside it is refused (the real path is judged, links followed).
6. show-names-Q6: **Absolute paths.** "A. Accepter (recommandé)": an absolute path inside the
   bundle stays accepted.
7. show-names-Q7: **API error.** "A. FileNotFoundError (recommandé)": `show_bundle` raises
   `FileNotFoundError` outside the bundle too, with an explicit message.
8. show-names-Q8: **Scope of the symlink rule.** "A. show + nouveau CR (recommandé)": this CR
   changes `show` only; a separate CR (`bundle-outside-symlinks`) handles `validate`, `list`,
   `index`, `backlinks` and `lint`.
9. show-names-Q9: **Grilled enough.** "A. Pour batch-01 (recommandé)": specify it for the
   running batch; it is not taken before the grill of 57 and 58 is over (the option's words).

Destination: running batch batch-01.

Spec critic: yes, it changes what `show` refuses (CLI contract and public API).

10. show-names-Q10: **Ticket summary.** "B. Commentaire seul": post `work/issue-comment.md` on
    issue 56, no plan artifact.

    Posted on https://github.com/gsemet/okf-schema/issues/56, 2026-11-25: comment
    https://github.com/gsemet/okf-schema/issues/56#issuecomment-7170886026; plan "none"; demo
    "none".

## 2026-11-25: after the spec critic (5 findings; 3 fixed by the spec-writer, 2 asked)

11. show-names-Q11: **Where the outside-bundle rule is written.** "B. Nouvelle exigence": create
    now a new proposed requirement "stay inside the bundle"; CORE-005 references it instead of
    carrying the rule, and the follow-up CR `bundle-outside-symlinks` only adds commands to it.
12. show-names-Q12: **Release.** "A. fix → 0.18.2 (recommandé)": a plain `fix(show): ...`
    commit, no `!` and no `BREAKING CHANGE:` section; reading outside the bundle was never
    documented, so it was a defect (the option's words).
13. show-names-Q13: **macOS case.** "A. Documenter (recommandé)": the refusal of an absolute path
    spelled in another case than `--path` is accepted and written in the command reference.
