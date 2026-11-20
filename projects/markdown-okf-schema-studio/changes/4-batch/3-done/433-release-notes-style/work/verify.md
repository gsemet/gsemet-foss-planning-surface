# Verify CR-433

Head: a719e649d25e8c92901ed060271c10bdde693e32

All claims judged at a719e649 (`git rev-parse HEAD` in the worktree, clean tree).

1. A1-A7, B (diff `git diff origin/main...HEAD`, one file, +38 -13): "### Writing" holds the approved prompt
   (tone, banned forms); "### Structure" keeps h1, bold verbs line, `<sub>` + rev-list, links line, `---`
   (unchanged hunks); highlights `## <emoji> <what you can now do>`, picture, at most two sentences, the
   three picture rules (joined before/after, no text when picture shows all, setting named
   `markdownOkfSchemaStudio.…`, default, VS Code settings); syntax example allowed; the explanatory
   paragraph and "why it matters" closing removed from highlights (the phrase now appears only in the
   banned list, line 198); smaller changes one line per bullet, bold lead; folded All fixes, Details,
   For contributors; `<kbd>`, coverage rule, Images, Publishing kept; Images states the joined image is
   one file made from the Verifier captures, any tool, the version PR says which; thread tone points to
   "Writing". VERIFIED.
2. `git diff --stat origin/main...HEAD -- CHANGELOG.md scripts/release_notes.py` printed nothing:
   both unchanged. VERIFIED.
3. `just release-notes-check` run by me at the head: `release-notes: docs/releases-notes/2026-11-19-v1.9.3/release-notes.md ok`.
   Driver's `just check` log work/gates/a719e64-check.log first line a719e649d25e8c92901ed060271c10bdde693e32,
   test summaries `ℹ fail 0`. VERIFIED.
4. `gh pr checks 442`: checks, report, static, static-windows, visual pass; the rest skipping (PR rule,
   spec: no heavy CI). VERIFIED.
5. No visible change: no screenshots needed. VERIFIED.
6. PR body (`gh pr view 442`, headRefOid a719e649): renders (sections, table, code fence); Summary,
   Deliverables, Changes match the diff; shows the Writing excerpt and try E; Known gaps "None" correct;
   no images. Review box "approved, committed as a719e649" matches the log note "r1 approved at 36240e0f...,
   committed as a719e649...". The "CI green" box is unticked while CI is green now: the Driver ticks it.
   VERIFIED.

VERIFIED
