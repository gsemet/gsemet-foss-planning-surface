# 058 — image-paste-empty-file

From backlog `P2/image-paste-empty-file` (`01-intent.md` moved here). Started by the overnight
chain the user asked for on 2026-10-23 ("the 2 other CRs on top of the refactor").

## Decisions

1. Follow the flake process of `.agents/guidelines/ci.guidelines.md` rule 12:
   - collect the evidence: in
     [run 40016132398](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40016132398),
     round 4/20 of the image-paste stress scenario saved an empty file;
   - trace every code path that can create the file before its bytes are written (the page sends
     the bytes, the host writes them, the test reads them);
   - prove the cause.
2. Fix it at the cause with a deterministic readiness signal: no retry, no sleep, no raised
   timeout. If the product can create an empty file, fix the product (write atomically, or only
   once the bytes are known). Failure messages carry diagnostics (file size, write state).
3. Keep the image-paste scenario in the stress list. The proof is a manual heavy run
   (`gh workflow run ci.yml --ref <branch> -f heavy=true`) whose stress job passes. Run local real
   VS Code tests under the window lock if the screen is unlocked; otherwise the CI heavy runs are
   the proof, and the PR says so.
4. The code lives in the refactored layout of the 056 branch. Branch
   `changes-requests/058-image-paste-empty-file`, created from
   `changes-requests/056-refactor-host-neutral-core`. The PR targets that branch: it stacks on the
   refactor PR #51. No assets branch unless a visible change appears.
5. Opus, 3 rounds. PR for an external reader. Commits end with `Assisted-by: Claude:Opus-5.5`.
   Never merge.
