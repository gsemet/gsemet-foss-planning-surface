# Final Inspector (Opus) on the release artefacts after #209 — CHANGES REQUIRED

1. HIGH analysis l.4/40/43/183: stack id is 217, not 210; merge command `gh stack merge 217 --rebase --yes`;
   never pass a bare 197 (resolved first as a stack number). `--rebase` correct (only rebase allowed).
2. HIGH analysis merge section + checklist: #197 must leave draft first (`gh pr ready 197`); stack merge refuses drafts.
3. MEDIUM: commits 5f598767 (adds zz-rerun-proof.yml) and a588f28b (removes it) sit on #207's branch; drop
   them (they belong to #209's proof), restack; reword #209 body ("throwaway workflow, not merged");
   analysis l.54-58 → "dropped from the branch before the merge; it never lands on main".
4. MEDIUM overclaim (#202): CHANGELOG l.17 → "Two causes of a comment thread losing its highlight and badge
   after an edit are fixed: a new thread no longer stays invisible…"; release-notes l.5 → "- Two causes of a
   comment thread losing its highlight or badge are fixed: a new thread no longer stays hidden until a
   reload, and threads are placed again after a reload from disk, a revert, an undo to the saved text, or an
   edit while the comments file is saved."
5. LOW analysis l.106: pages needs `[tag-release, integration, stress, report]`.
6. LOW release-notes l.6: add "and they stay HTML labels".
7. INFO: the two report files are tracking files (git-ignored), not shipped.
