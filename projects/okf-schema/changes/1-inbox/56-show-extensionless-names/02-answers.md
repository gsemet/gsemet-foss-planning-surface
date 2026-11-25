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
