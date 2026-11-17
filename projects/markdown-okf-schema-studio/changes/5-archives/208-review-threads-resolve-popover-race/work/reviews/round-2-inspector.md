# CR 208, round 2, Inspector review

Worktree: `markdown-okf-schema-studio-wt-208`, uncommitted diff against `origin/main`.

Verdict: **APPROVE**, as a hardening commit. The cause of the stress flake is not proven here.

## 1. Cause claims

- `git diff | grep -i 'cause|flake|race'` finds one line, in `requirements/tiers/log.md`:
  "This hardens that path; it is not the proven cause of the review-threads stress flake, which
  most likely came from the delete-then-move gap of the file rename, fixed separately
  (test/host-vscode/fileRename.test.ts)." This is accurate and matches the round-1 analysis.
- The log now says a failed read "could close an open popover". It no longer says that one did.
- The test was renamed to `a busy or denied read of the comments file posts no empty list`. Its
  comment says "A failed read could close the popover". No text in the diff calls the change the
  cause.

## 2. SwRS and index wording

- In REVIEW-012, the statement clause "never from a read that failed" is the same in the
  description, the normative text and the index line.
- The refusal scenario has two rows: busy, denied or interrupted posts nothing; missing posts the
  empty list. They match the code: `isFileNotFound` gives `undefined`, and every other error gives
  `UNREADABLE`, which returns before the hash is recorded.
- The verification method names both new tests by their real titles. The criteria clause "returns
  before posting and before recording its text hash" matches the code.
- The req stays `proposed`, and only that req's scenario was edited. That is acceptable, as in
  round 1.

## 3. fileRename citation

- `test/host-vscode/fileRename.test.ts` exists. Its tests carry `@tests_req
  SwRS-MDOKFSTUDIO-REVIEW-054` ("a rename with overwrite replaces the target in one step, never
  deleting it first"; "rewriting a review comments file through the VS Code host never leaves it
  missing").
- REVIEW-054 already lists that file as a verification method, and its scenario "A write replaces
  the file in one step" matches.
- The test came from 5f0f3be0, which is on `origin/main`. The citation is accurate, and round-1
  optional item 3 is met.

## 4. Diff scope and gates

- `git diff --stat` shows the 5 expected files, +81/-9: log.md, REVIEW-012, the review-annotations
  index, `src/session/features/comments.ts` and `test/session/reviewReqComments.requirements.test.ts`.
  `git status` shows no other change.
- The `comments.ts` hunk did not change in substance since round 1 (correct, see round 1 §3).
- `npx tsc -p .` is clean. `node --test out/test/session/reviewReqComments.requirements.test.js`
  passes 15/15, both new tests included.

## Nits (non-blocking)

- Test line 387, the comment "The next post (the watcher event) cannot read…", is 172 characters.
  The longest other lines in the file are about 128. It could be wrapped.
- Proof that the flake is gone still has to come from heavy `stress` runs on main after 5f0f3be0
  (round-1 required item 2). That belongs in the PR body or the driver report, not in this diff.
