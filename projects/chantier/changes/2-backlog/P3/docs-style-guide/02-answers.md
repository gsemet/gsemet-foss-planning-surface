# Answers

## Settled by the Chief of Staff (2026-11-18, the user asks no questions)
- Split from `docs-sphinx-rtd` on its spec-critic's finding; the user's own words on style are in
  that CR's 02-answers.md and intake, and hold here.
- The Inspector checks a changed docs page against the guide, through one `AGENTS.md` rule
  (docs-sphinx-rtd Q2, A); the guide is a backticked path, not a link.

## Settled by the spec-writer (2026-11-18)

Points with no user-visible behaviour, decided while writing `03-change-spec.md`:

- Each guide rule has a short id (`S1`...) that the review table and the Inspector's items cite.
- A broken guide rule on a changed page is a `blocking` Inspector item: the `AGENTS.md` rule makes
  the guide a project rule, which the Inspector's card already holds as blocking. No card changes.
- The review fixes how pages say things, not what they say: no page added, removed, renamed or
  moved, no image added or removed; a false statement found is named in Known gaps, not fixed here.
- The review is one table, one row per page, in `work/verifier/evidence/` and quoted in the PR.
- The README's prose, `docs/demo/`, `docs/release-notes/` and the `*-texts.md` are not reviewed.
- No mechanical lint of the guide's rules (the user chose guide, review and examples).
- One test reads the shipped `AGENTS.md`, `CONTRIBUTING.md` and `docs/STYLE.md`: the guide is named
  in backticks in both, and `chantier rules`' link walk does not reach it.

- Back from the trash (2026-11-20): dropped from batch-28 on the user's word so v0.14.0 could ship; user, 2026-11-20: "En backlog P2". Its draft PR #347, worktree and branch are kept: the next Driver resumes them.

# Decision (2026-11-25, the owner, in chat)

"tu vas te concentrer sur livrer les CR 507 a 514 sur le rework. tu vas annuler les specs de tous les autres mais eviement pas perdre les reponses que j avais donnee en interview. Avec le rework en cours il faudra refaire la specification de tout, et on fera ca dans un batch 32."

The specification is cancelled: it is kept for reference in `work/spec-before-rework.md`, and is to be written again after the rework, from these answers, for batch-32.

Destination: none for now; to specify again for batch-32.
