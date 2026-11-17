# 048 — local-undo-macos

From the follow-ups of CR 043 (`01-followup-from-043.md` here). User: "fais une PR pour régler ce
problème" (2026-10-23).

## Problem

Locally on macOS, `npm run test:integration` fails at every undo step: `checkboxToggle.test.ts`
"one undo to restore the original source" and real-input "one undo to restore the paragraph".
Even `executeCommand("undo")` leaves the buffer unchanged. Same on origin/main. The suite stops
there, so the rest of the trusted suite never runs locally. CI (Linux, VS Code 1.143.1) is green.
The user wants the full real-VS Code suite to pass locally on their Mac.

## Decisions (main session, from the user's request)

1. Root cause first. Two hypotheses to separate:
   a. a product bug: the extension's edit path breaks the undo stack (or undo target) on macOS /
      VS Code 1.143.0, which would also hit the user in real use — check manually-equivalent
      paths (WorkspaceEdit vs TextEditor.edit, undo stop, which editor is active, focus in the
      webview vs text editor);
   b. a harness/version issue (native EditContext of 1.143.0, focus, the VS Code build used).
   Compare with VS Code 1.143.1 via the test runner's version/`vscodeExecutablePath` option:
   downloading that test build into the runner cache (`.vscode-test/`) is ALLOWED for this CR (the
   only network use allowed).
2. Fix at the cause: a product fix if (a); if (b), make the local runner reliable (e.g. pin the
   same VS Code version as CI locally by default, documented), never by skipping or weakening the
   undo assertions, never by retries or longer timeouts.
3. Done = full `npm run test:integration` green locally on macOS (counts in the PR), required
   `checks` green, and one manual heavy CI run (`gh workflow run ci.yml --ref <branch> -f heavy=true`)
   green. Local window runs one at a time under `requests/WINDOW-TESTS.lock`.
4. Speed: Opus everywhere, reviewer on the round diff. Rounds: 3.
5. PR written for an external reader.

## Decision 6 (main session, 2026-10-23 16:40)

Also in scope: the local failure "Timed out waiting for the slash menu to open after a line break"
(`test/integration/realInput.test.ts:1076`, scenarioSlashMenu), seen by CR 044 r1 in a full local
run. Same rule: root cause, no retry, no longer timeout. Done still = full local suite green.
