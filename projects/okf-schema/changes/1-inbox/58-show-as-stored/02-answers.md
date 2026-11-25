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
