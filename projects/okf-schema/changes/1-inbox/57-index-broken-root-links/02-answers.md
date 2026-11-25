Short name: `index-links`

# Answers

## 2026-11-25: facts checked before the grill

- Reproduced on `origin/main` 2f09cef (0.18.1), Python 3.13: with `api/index.md` present and no
  summary yet for `api` in the root `index.md`, `okf-schema index` writes
  `- [api](./api/) — [Health Check](health-check.md)  [API Endpoint]` in the root.
- Cause: `_get_subdir_description` returns the first non-heading line of the subdirectory's
  `index.md`, list entries included (`src/okf_schema/api.py:1013`). So `okf-schema` writes these
  summaries itself.
- The copied text is then preserved as an authored summary; the next run also removes its trailing
  `[API Endpoint]`, so the output changes between two runs with no source change.
- A fresh bundle gets "Auto-generated index for concepts in `api`." only because the root is
  written before `api/index.md` exists.
- `validate` checks no link in any `index.md` (`validate_index` only raises E3,
  `src/okf_schema/validator.py:863`).
- W2 today reports `a.md#part` and `#top` as broken links (anchors are not stripped,
  `src/okf_schema/_internal/utils.py:38`).
- An existing index entry wins over the concept's frontmatter description: after the description
  changes, `index` keeps the old text. OKF 0.2 section 8 says entries SHOULD carry the concept's
  description.
- Scan of the 27 `index.md` under `examples/`, `requirements/`, `src/`, `docs/`, `skills/`: one
  broken link, in `docs/source/index.md` (Sphinx, not a bundle).

## 2026-11-25: grill, user's answers

1. index-links-Q1: **Summary of a subdirectory.** Not decided yet. Free answer: "Donne moi des
   exemples riches" (asked again with examples).
2. index-links-Q2: **Damaged summaries already written.** "A. Recalculer (recommandé)": `index`
   recomputes a summary only when it starts with a link broken from the root and valid from the
   subdirectory (the bug's signature); anything else is left untouched.
3. index-links-Q3: **W2 in index.md.** "A. Oui, W2 (recommandé)": `validate` reports broken links
   of every `index.md` as W2, as for concepts; `--strict` then fails.
4. index-links-Q4: **Anchor links.** "A. Corriger ici (recommandé)": in this CR, the `#...` part is
   ignored when a link is checked, for concepts and index files.
5. index-links-Q1, asked again with examples: "A. Intro seule (recommandé)": only the sentence
   written before the first list of the subdirectory's `index.md`, its relative links rewritten to
   be valid from the root; else "Auto-generated index for concepts in `<dir>`.". Never a list
   entry or a heading. A schema summary still comes first, and a summary already written in the
   root is still preserved (except the damaged ones of answer 2).

   Fact for the specification: the existing 120-character truncation of that line could cut a
   link in two.
6. index-links-Q5: **Generic text.** "A. Recalculer (recommandé)": the exact generic text is not
   treated as authored; `index` recomputes it on each run, so an introduction added later reaches
   the root.
7. index-links-Q6: **Stale concept descriptions.** "A. Nouveau CR (recommandé)": out of this CR,
   filed apart (`index-stale-descriptions`).
8. index-links-Q7: **Grilled enough.** "A. batch-01 (recommandé)": specify it for the running
   batch; it is not taken before the grill of 58 is over (the option's words).

Destination: running batch batch-01.

Spec critic: yes, it changes what `index` rewrites in users' files and what `validate` reports
(so the result of `--strict`).

9. index-links-Q8: **Ticket summary.** "A. Commentaire (recommandé)": post
   `work/issue-comment.md` on issue 57, no plan artifact.

   Posted on https://github.com/gsemet/okf-schema/issues/57, 2026-11-25: comment
   https://github.com/gsemet/okf-schema/issues/57#issuecomment-7171724924; plan "none"; demo
   "none".

## 2026-11-25: questions after the specification and the spec critic

Answers 10 to 13 settle the two open questions of the specification (Q10, Q12) and the three
behaviour findings of the critic (Q9, Q10, Q11).

10. index-links-Q9: **Introduction ending with `[...]`.** "A. Garder (recommandé)": the trailing
    `[...]` is no longer removed on `./<dir>/` entries, which never get a type tag; the summary is
    stable between runs. Side effect shown with the option: an old subdirectory line ending with
    `[Type]` keeps it.
11. index-links-Q10: **Part of the introduction.** "A. Toute l'intro (recommandé)": everything
    before the first list, on one line, with no sentence splitting. This is the reading of "la
    phrase" of answer 5.
12. index-links-Q11: **Encoded links.** "A. Décoder (recommandé)": the path is percent-decoded
    (`%20`, accents) before checking that it exists, in concepts and index files alike; a link
    really broken is still reported as written.
13. index-links-Q12: **120-character cut.** "A. Avant le lien (recommandé)": keep 120 characters;
    when the cut would fall inside a link, cut before it and append `...`.
